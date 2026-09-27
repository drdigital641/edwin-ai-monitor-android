package sg.edwingarage.readonlybridge

import android.accessibilityservice.AccessibilityService
import android.graphics.Rect
import android.os.Handler
import android.os.Looper
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo
import org.json.JSONArray
import java.time.DayOfWeek
import java.time.Instant
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.LocalTime
import java.time.ZoneId
import java.time.format.DateTimeFormatter
import java.time.format.DateTimeParseException
import java.time.temporal.ChronoUnit
import java.time.temporal.TemporalAdjusters
import java.util.Locale

/**
 * Read-only WhatsApp Business accessibility monitor.
 *
 * v2.1 contract:
 * 1. Never use accessibility observation time or Send-click time as WhatsApp sent time.
 * 2. A trusted timestamp must be read from the exact outgoing bubble whose message text
 *    matches the just-sent draft in the same contact.
 * 3. Historical right-side observations are useful raw evidence, but their timestamp is
 *    explicitly untrusted downstream.
 */
class WhatsAppReadService : AccessibilityService() {
    private val handler = Handler(Looper.getMainLooper())
    private val zone = ZoneId.of("Asia/Singapore")

    private var pendingDraftContact = ""
    private var pendingDraftText = ""
    private var pendingDraftAtMs = 0L

    private var pendingSendContact = ""
    private var pendingSendText = ""
    private var pendingSendClickedAtMs = 0L

    private var lastHistoricalScanAtMs = 0L

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        if (event == null || event.packageName?.toString() != BridgeConfig.WHATSAPP_BUSINESS_PACKAGE) return

        val root = rootInActiveWindow
        if (root != null) refreshDraft(root)

        when (event.eventType) {
            AccessibilityEvent.TYPE_VIEW_CLICKED -> {
                // Do not scan synchronously on Send click: the old last bubble can still be on screen.
                // handleSendClick schedules post-render scans after WhatsApp has had time to create the new bubble.
                handleSendClick(event)
            }
            AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED -> {
                scanVisibleConversation("event_window_state")
            }
            AccessibilityEvent.TYPE_WINDOW_CONTENT_CHANGED -> {
                scanVisibleConversation("event_content_changed")
            }
            AccessibilityEvent.TYPE_VIEW_SCROLLED -> {
                scanVisibleConversation("event_scrolled")
            }
            AccessibilityEvent.TYPE_VIEW_TEXT_CHANGED -> {
                scanVisibleConversation("event_text_changed")
            }
        }
    }

    override fun onInterrupt() = Unit

    private fun handleSendClick(event: AccessibilityEvent) {
        val src = event.source ?: return
        if (!isSendButton(src)) return

        val root = rootInActiveWindow ?: src
        val contact = findContactName(root)
        if (!isValidConversationContact(contact)) return

        val current = findComposeText(root)?.trim().orEmpty()
        val recentDraft = if (
            normalize(contact) == normalize(pendingDraftContact) &&
            System.currentTimeMillis() - pendingDraftAtMs <= 5_000L
        ) pendingDraftText else ""

        val message = when {
            isUsableMessageText(current) -> current
            isUsableMessageText(recentDraft) -> recentDraft
            else -> return
        }
        if (isAiReply(message)) return

        pendingSendContact = contact
        pendingSendText = message
        pendingSendClickedAtMs = System.currentTimeMillis()

        // Let WhatsApp render the real bubble. We only trust a timestamp found inside that
        // exact rendered bubble; these delays are observation retries, not send timestamps.
        handler.postDelayed({ scanVisibleConversation("post_send_250ms") }, 250L)
        handler.postDelayed({ scanVisibleConversation("post_send_800ms") }, 800L)
        handler.postDelayed({ scanVisibleConversation("post_send_1700ms") }, 1700L)
    }

    private fun refreshDraft(root: AccessibilityNodeInfo) {
        val contact = findContactName(root)
        if (!isValidConversationContact(contact)) return
        val text = findComposeText(root)?.trim().orEmpty()
        if (!isUsableMessageText(text) || isAiReply(text)) return
        pendingDraftContact = contact
        pendingDraftText = text
        pendingDraftAtMs = System.currentTimeMillis()
    }

    private fun scanVisibleConversation(trigger: String) {
        val now = System.currentTimeMillis()
        val pendingActive = pendingSendClickedAtMs > 0L && now - pendingSendClickedAtMs <= 10_000L
        if (!pendingActive && now - lastHistoricalScanAtMs < 350L) return
        if (!pendingActive) lastHistoricalScanAtMs = now

        val root = rootInActiveWindow ?: return
        val contact = findContactName(root)
        if (!isValidConversationContact(contact)) return

        val dm = resources.displayMetrics
        val screenWidth = dm.widthPixels
        val screenHeight = dm.heightPixels
        if (screenWidth <= 0 || screenHeight <= 0) return

        val allNodes = ArrayList<AccessibilityNodeInfo>()
        collectNodes(root, allNodes)

        val dateAnchors = allNodes.mapNotNull { node ->
            val text = node.text?.toString()?.trim().orEmpty()
            if (!isDateLabel(text)) return@mapNotNull null
            val rect = Rect()
            node.getBoundsInScreen(rect)
            if (rect.isEmpty) null else DateAnchor(text, rect.centerY())
        }.sortedBy { it.y }

        val emitted = HashSet<String>()
        val nearby = JSONArray()

        for (node in allNodes) {
            val raw = node.text?.toString()?.trim().orEmpty()
            if (!isUsableMessageText(raw)) continue
            if (isComposeOrHeaderNode(node)) continue

            val textRect = Rect()
            node.getBoundsInScreen(textRect)
            if (textRect.isEmpty) continue
            if (textRect.centerY() < screenHeight * 0.08 || textRect.centerY() > screenHeight * 0.93) continue

            val bubble = findSmallestTimedBubble(node, screenWidth, screenHeight) ?: continue
            if (!isRightSideOutgoing(bubble.bounds, screenWidth)) continue

            val bubbleTexts = collectText(bubble.node)
            val bubbleDescriptions = collectDescriptions(bubble.node)
            if ((bubbleTexts + bubbleDescriptions).any { isAiReply(it) }) continue

            val clocks = collectClockStrings(bubble.node)
            val timestampText = clocks.singleOrNull() ?: continue
            val message = buildBubbleMessage(bubbleTexts, timestampText)
            if (!isUsableMessageText(message) || isAiReply(message)) continue

            nearby.put(
                bubble.bounds.left.toString() + "," + bubble.bounds.top + "," +
                    bubble.bounds.right + "," + bubble.bounds.bottom + ":" + message.take(180)
            )

            val exactPending = pendingActive &&
                now - pendingSendClickedAtMs >= 150L &&
                normalize(contact) == normalize(pendingSendContact) &&
                normalize(message) == normalize(pendingSendText)

            val dateLabel = nearestDateAnchor(dateAnchors, bubble.bounds.centerY())
            val parsedTime = when {
                dateLabel != null -> resolveWhatsAppIso(dateLabel, timestampText)
                exactPending -> resolveWhatsAppIso("today", timestampText)
                else -> null
            }

            // Trusted exact-send evidence requires a real parsed clock from this same bubble.
            val trustedSameBubble = exactPending && parsedTime != null
            val identity = normalize(contact) + "|" + normalize(message) + "|" +
                (parsedTime ?: "untrusted") + "|" + bubble.bounds.top
            if (!emitted.add(identity)) continue

            Base44Sender.sendOutgoing(
                context = this,
                contactTitle = contact,
                messageText = message,
                observedAtMs = now,
                messageTime = parsedTime,
                trigger = if (trustedSameBubble) "accessibility_exact_post_send_bubble" else trigger,
                selectedBounds = bubble.bounds,
                nearbyCandidates = nearby,
                trustedSameBubble = trustedSameBubble
            )

            if (trustedSameBubble) {
                pendingSendContact = ""
                pendingSendText = ""
                pendingSendClickedAtMs = 0L
                pendingDraftContact = ""
                pendingDraftText = ""
                pendingDraftAtMs = 0L
            }
        }

        if (pendingSendClickedAtMs > 0L && now - pendingSendClickedAtMs > 10_000L) {
            // Fail closed. Do not create a timestamp from observation time.
            pendingSendContact = ""
            pendingSendText = ""
            pendingSendClickedAtMs = 0L
        }
    }

    private data class DateAnchor(val label: String, val y: Int)
    private data class BubbleCandidate(val node: AccessibilityNodeInfo, val bounds: Rect)

    private fun findSmallestTimedBubble(
        start: AccessibilityNodeInfo,
        screenWidth: Int,
        screenHeight: Int
    ): BubbleCandidate? {
        var current: AccessibilityNodeInfo? = start
        repeat(7) {
            val n = current ?: return null
            val rect = Rect()
            n.getBoundsInScreen(rect)
            if (
                !rect.isEmpty &&
                rect.width() > 0 &&
                rect.height() > 0 &&
                rect.width() < screenWidth * 0.92 &&
                rect.height() < screenHeight * 0.42
            ) {
                val texts = collectText(n)
                val clocks = collectClockStrings(n)
                val hasMessage = texts.any {
                    isUsableMessageText(it) && !isClockText(it) && !isDateLabel(it)
                }
                if (clocks.size == 1 && hasMessage) return BubbleCandidate(n, Rect(rect))
            }
            current = n.parent
        }
        return null
    }

    private fun isRightSideOutgoing(rect: Rect, screenWidth: Int): Boolean {
        val center = rect.centerX().toDouble() / screenWidth
        val right = rect.right.toDouble() / screenWidth
        return center >= 0.58 && right >= 0.72
    }

    private fun buildBubbleMessage(texts: List<String>, timestampText: String): String {
        val seen = HashSet<String>()
        return texts.asSequence()
            .map { it.trim() }
            .filter { it.isNotEmpty() }
            .filter { it != timestampText }
            .filterNot { isClockText(it) || isDateLabel(it) || isUiNoise(it) || isDeliveryStatus(it) }
            .filter { seen.add(normalize(it)) }
            .joinToString("\n")
            .trim()
    }

    private fun findContactName(root: AccessibilityNodeInfo): String {
        val knownIds = listOf("conversation_name", "conversation_contact_name", "contact_name", "toolbar_title")
        for (id in knownIds) {
            val value = findByIdSuffix(root, id)?.trim().orEmpty()
            if (isValidConversationContact(value)) return value
        }

        val screenHeight = resources.displayMetrics.heightPixels
        val nodes = ArrayList<AccessibilityNodeInfo>()
        collectNodes(root, nodes)
        return nodes.asSequence().mapNotNull { node ->
            val text = node.text?.toString()?.trim().orEmpty()
            if (!isValidConversationContact(text)) return@mapNotNull null
            val rect = Rect()
            node.getBoundsInScreen(rect)
            if (rect.isEmpty || rect.centerY() > screenHeight * 0.18) return@mapNotNull null
            val id = (node.viewIdResourceName ?: "").lowercase(Locale.ENGLISH)
            if (id.contains("search") || id.contains("tab") || id.contains("menu")) return@mapNotNull null
            text
        }.firstOrNull().orEmpty()
    }

    private fun isValidConversationContact(value: String): Boolean {
        val c = normalize(value).replace(Regex("\\.{3}$"), "").trim()
        if (c.length < 2) return false
        val invalid = setOf(
            "search", "searching", "google search", "new chat", "whatsapp business",
            "chats", "calls", "updates", "communities", "contacts", "select contact",
            "archived", "workshop status", "message", "settings", "chat lock",
            "business account", "edwin ai monitor", "last 30 messages", "today",
            "starred messages", "profile picture", "photo", "save to gallery",
            "text alignment", "vehicle service, cleaning service, car dealership"
        )
        return c !in invalid &&
            !c.startsWith("search") &&
            !c.startsWith("swipe down") &&
            !Regex("^page \\d+ of \\d+\\.?$").matches(c) &&
            !Regex("^history \\(\\d+\\)$").matches(c)
    }

    private fun findComposeText(root: AccessibilityNodeInfo): String? {
        val out = ArrayList<AccessibilityNodeInfo>()
        findNodesByClass(root, "android.widget.EditText", out)
        return out.firstOrNull { it.text?.isNotEmpty() == true }?.text?.toString()
    }

    private fun isSendButton(node: AccessibilityNodeInfo): Boolean {
        val id = node.viewIdResourceName ?: ""
        val desc = node.contentDescription?.toString()?.lowercase(Locale.ENGLISH) ?: ""
        val cls = node.className?.toString() ?: ""
        return id.endsWith("/send") || id.endsWith(":id/send") ||
            desc == "send" || desc == "send message" ||
            (cls.contains("ImageButton") && (id.contains("send") || desc.contains("send")))
    }

    private fun isComposeOrHeaderNode(node: AccessibilityNodeInfo): Boolean {
        val id = (node.viewIdResourceName ?: "").lowercase(Locale.ENGLISH)
        return id.contains("conversation_name") ||
            id.contains("entry") ||
            id.contains("compose") ||
            id.endsWith("/send") ||
            id.endsWith(":id/send")
    }

    private fun isUsableMessageText(text: String): Boolean {
        val t = text.trim()
        return t.isNotEmpty() &&
            !isUiNoise(t) &&
            !isClockText(t) &&
            !isDateLabel(t) &&
            !isDeliveryStatus(t)
    }

    private fun isAiReply(text: String): Boolean =
        normalize(text).contains("-replied by ai")

    private fun isDeliveryStatus(text: String): Boolean =
        normalize(text) in setOf("sent", "delivered", "read", "edited", "seen", "unread")

    private fun isUiNoise(text: String): Boolean {
        val t = normalize(text)
        if (t.isBlank()) return true
        val exact = setOf(
            "search", "search...", "search…", "searching", "searching...", "searching…",
            "new chat", "type a message", "message", "send", "camera", "attach", "emoji",
            "voice message", "video call", "voice call", "more options", "back",
            "go to most recent message", "enlarge photo", "view media", "view image in gallery",
            "pause ai 30 min", "whatsapp business", "you deleted this message",
            "read", "unread", "seen", "sent", "delivered", "edited",
            "remove link preview", "next colour", "previous colour", "event", "poll",
            "quick reply", "block business", "translate messages", "view last 30 messages",
            "full chat", "resume ai"
        )
        return t in exact ||
            t.startsWith("photo, date ") ||
            t.startsWith("view photo") ||
            Regex("^see all \\d+ media$").matches(t) ||
            t.startsWith("colour picker (") ||
            Regex("^\\+\\s*\\d+$").matches(t) ||
            (t.contains("reaction on previous message") && t.contains("view reactions")) ||
            (t.startsWith("voice message,") && t.contains("seconds")) ||
            (t.startsWith("you, voice message,") && t.contains("seconds")) ||
            t.startsWith("button.") ||
            t.startsWith("swipe down") ||
            t.startsWith("forward image") ||
            t.startsWith("forward video") ||
            Regex("^page \\d+ of \\d+\\.?$").matches(t)
    }

    private fun nearestDateAnchor(anchors: List<DateAnchor>, bubbleY: Int): String? =
        anchors.lastOrNull { it.y <= bubbleY }?.label

    private fun isDateLabel(value: String): Boolean {
        val t = value.trim()
        if (Regex("^(today|yesterday)$", RegexOption.IGNORE_CASE).matches(t)) return true
        if (Regex("^(monday|tuesday|wednesday|thursday|friday|saturday|sunday)$", RegexOption.IGNORE_CASE).matches(t)) return true
        if (Regex("^\\d{1,2}[/-]\\d{1,2}[/-]\\d{2,4}$").matches(t)) return true
        if (Regex("^\\d{1,2}\\s+[A-Za-z]{3,9}(?:\\s+\\d{4})?$").matches(t)) return true
        return false
    }

    private fun isClockText(value: String): Boolean =
        Regex("^\\s*\\d{1,2}:\\d{2}(?:\\s?[ap]m)?\\s*$", RegexOption.IGNORE_CASE)
            .matches(value.trim())

    private fun resolveWhatsAppIso(dateLabel: String, clockText: String): String? {
        val date = resolveDate(dateLabel) ?: return null
        val time = parseClock(clockText) ?: return null
        val dt = LocalDateTime.of(date, time)
        val now = LocalDateTime.now(zone)
        if (dt.isAfter(now.plusMinutes(5))) return null
        return dt.atZone(zone).toInstant().truncatedTo(ChronoUnit.MINUTES).toString()
    }

    private fun resolveDate(label: String): LocalDate? {
        val today = LocalDate.now(zone)
        val l = label.trim()
        when (l.lowercase(Locale.ENGLISH)) {
            "today" -> return today
            "yesterday" -> return today.minusDays(1)
        }

        val weekdays = mapOf(
            "monday" to DayOfWeek.MONDAY,
            "tuesday" to DayOfWeek.TUESDAY,
            "wednesday" to DayOfWeek.WEDNESDAY,
            "thursday" to DayOfWeek.THURSDAY,
            "friday" to DayOfWeek.FRIDAY,
            "saturday" to DayOfWeek.SATURDAY,
            "sunday" to DayOfWeek.SUNDAY
        )
        weekdays[l.lowercase(Locale.ENGLISH)]?.let { dow ->
            return today.with(TemporalAdjusters.previousOrSame(dow))
        }

        val patterns = listOf(
            "d/M/yyyy", "dd/MM/yyyy", "d-M-yyyy", "dd-MM-yyyy",
            "d/M/yy", "dd/MM/yy", "d-M-yy", "dd-MM-yy",
            "d MMM yyyy", "dd MMM yyyy", "d MMMM yyyy", "dd MMMM yyyy"
        )
        for (pattern in patterns) {
            try {
                val parsed = LocalDate.parse(l, DateTimeFormatter.ofPattern(pattern, Locale.ENGLISH))
                if (!parsed.isAfter(today)) return parsed
            } catch (_: DateTimeParseException) {}
        }

        for (pattern in listOf("d MMM", "dd MMM", "d MMMM", "dd MMMM")) {
            try {
                val md = java.time.MonthDay.parse(l, DateTimeFormatter.ofPattern(pattern, Locale.ENGLISH))
                var candidate = md.atYear(today.year)
                if (candidate.isAfter(today)) candidate = md.atYear(today.year - 1)
                return candidate
            } catch (_: DateTimeParseException) {}
        }
        return null
    }

    private fun parseClock(value: String): LocalTime? {
        val t = value.trim().uppercase(Locale.ENGLISH).replace(Regex("\\s+"), "")
        val formats = if (t.endsWith("AM") || t.endsWith("PM")) {
            listOf("h:mma", "hh:mma")
        } else {
            listOf("H:mm", "HH:mm")
        }
        for (pattern in formats) {
            try {
                return LocalTime.parse(t, DateTimeFormatter.ofPattern(pattern, Locale.ENGLISH))
            } catch (_: DateTimeParseException) {}
        }
        return null
    }

    private fun collectText(node: AccessibilityNodeInfo): List<String> {
        val out = ArrayList<String>()
        fun walk(n: AccessibilityNodeInfo) {
            n.text?.toString()?.trim()?.takeIf { it.isNotEmpty() }?.let { out.add(it) }
            for (i in 0 until n.childCount) n.getChild(i)?.let { walk(it) }
        }
        walk(node)
        return out
    }

    private fun collectDescriptions(node: AccessibilityNodeInfo): List<String> {
        val out = ArrayList<String>()
        fun walk(n: AccessibilityNodeInfo) {
            n.contentDescription?.toString()?.trim()?.takeIf { it.isNotEmpty() }?.let { out.add(it) }
            for (i in 0 until n.childCount) n.getChild(i)?.let { walk(it) }
        }
        walk(node)
        return out
    }

    private fun collectClockStrings(node: AccessibilityNodeInfo): List<String> {
        val seen = LinkedHashSet<String>()
        (collectText(node) + collectDescriptions(node)).forEach { raw ->
            val direct = raw.trim()
            if (isClockText(direct)) seen.add(direct)
            Regex("(?i)(?<!\\d)(\\d{1,2}:\\d{2}(?:\\s?[ap]m)?)(?!\\d)")
                .findAll(raw)
                .forEach { seen.add(it.groupValues[1].trim()) }
        }
        return seen.toList()
    }

    private fun collectNodes(node: AccessibilityNodeInfo, out: ArrayList<AccessibilityNodeInfo>) {
        out.add(node)
        for (i in 0 until node.childCount) node.getChild(i)?.let { collectNodes(it, out) }
    }

    private fun findNodesByClass(
        node: AccessibilityNodeInfo,
        className: String,
        out: ArrayList<AccessibilityNodeInfo>
    ) {
        if (node.className?.toString() == className) out.add(node)
        for (i in 0 until node.childCount) {
            val child = node.getChild(i) ?: continue
            findNodesByClass(child, className, out)
        }
    }

    private fun findByIdSuffix(node: AccessibilityNodeInfo, suffix: String): String? {
        val id = node.viewIdResourceName ?: ""
        if (id.endsWith("/$suffix") || id.endsWith(":id/$suffix")) return node.text?.toString()
        for (i in 0 until node.childCount) {
            val child = node.getChild(i) ?: continue
            findByIdSuffix(child, suffix)?.let { return it }
        }
        return null
    }

    private fun normalize(value: String): String =
        value.replace(Regex("\\s+"), " ").trim().lowercase(Locale.ENGLISH)
}
