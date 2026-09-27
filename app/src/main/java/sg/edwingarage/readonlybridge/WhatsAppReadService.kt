package sg.edwingarage.readonlybridge

import android.accessibilityservice.AccessibilityService
import android.graphics.Rect
import android.os.Handler
import android.os.Looper
import android.os.SystemClock
import android.text.format.DateFormat
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo
import java.security.MessageDigest
import java.time.DayOfWeek
import java.time.Instant
import java.time.LocalDate
import java.time.LocalTime
import java.time.ZoneId
import java.time.format.DateTimeFormatter
import java.time.format.ResolverStyle
import java.time.temporal.ChronoUnit
import java.util.Locale

/** Observer only: never performs accessibility actions or sends WhatsApp messages. */
class WhatsAppReadService : AccessibilityService() {
    private var lastScan = -300L
    private val handler = Handler(Looper.getMainLooper())
    private var pendingContact = ""
    private var pendingText = ""
    private var pendingClickAtMs = 0L

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        if (event == null || event.packageName?.toString() != BridgeConfig.WHATSAPP_BUSINESS_PACKAGE) return
        val click = event.eventType == AccessibilityEvent.TYPE_VIEW_CLICKED
        if (!click && event.eventType !in setOf(
                AccessibilityEvent.TYPE_VIEW_SCROLLED,
                AccessibilityEvent.TYPE_WINDOW_CONTENT_CHANGED,
                AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED)) return

        if (click) {
            val source = event.source ?: return
            val sendClick = try {
                source.packageName?.toString() == BridgeConfig.WHATSAPP_BUSINESS_PACKAGE &&
                    source.viewIdResourceName == "${BridgeConfig.WHATSAPP_BUSINESS_PACKAGE}:id/send" &&
                    source.isEnabled
            } finally {
                source.recycle()
            }
            if (!sendClick) return

            val tree = snapshotCurrent() ?: return
            val contact = MonitorRules.contact(tree) ?: return
            val compose = MonitorRules.flatten(tree)
                .filter { it.id == "entry" && it.editable }
                .singleOrNull() ?: return
            if (!MonitorRules.usable(compose.text)) return

            pendingContact = contact
            pendingText = compose.text
            pendingClickAtMs = System.currentTimeMillis()

            // Preserve V2's proven immediate manual-text capture, but do not attach a WhatsApp time yet.
            // Timestamp is independently enriched only after the exact rendered bubble is verified.
            Base44Sender.sendOutgoing(
                this, contact, compose.text, pendingClickAtMs, null,
                "accessibility_send_click_text_only", false
            )

            // Do not manufacture a send time from the click. Wait until WhatsApp renders the
            // outgoing bubble, then bind the clock from that exact bubble to this exact draft.
            handler.postDelayed({ scanPostSend("post_send_250ms") }, 250L)
            handler.postDelayed({ scanPostSend("post_send_800ms") }, 800L)
            handler.postDelayed({ scanPostSend("post_send_1700ms") }, 1700L)
            return
        }

        val elapsed = SystemClock.elapsedRealtime()
        if (elapsed - lastScan < 300L) return
        lastScan = elapsed
        scanHistorical("accessibility_historical_right_bubble")
    }

    private fun snapshotCurrent(): ReadNode? {
        val root = rootInActiveWindow ?: return null
        return try {
            if (root.packageName?.toString() != BridgeConfig.WHATSAPP_BUSINESS_PACKAGE) null
            else snapshot(root)
        } finally {
            root.recycle()
        }
    }

    private fun scanPostSend(trigger: String) {
        val now = System.currentTimeMillis()
        if (pendingClickAtMs <= 0L || now - pendingClickAtMs !in 150L..10_000L) return
        val tree = snapshotCurrent() ?: return
        val contact = MonitorRules.contact(tree) ?: return
        if (MonitorRules.normalize(contact) != MonitorRules.normalize(pendingContact)) return

        val exact = MonitorRules.exactPostSend(
            tree,
            pendingText,
            now,
            DateFormat.is24HourFormat(this)
        ) ?: return

        Base44Sender.sendOutgoing(
            this, contact, exact.text, now, exact.time, trigger, true
        )
        pendingContact = ""
        pendingText = ""
        pendingClickAtMs = 0L
    }

    private fun scanHistorical(trigger: String) {
        val tree = snapshotCurrent() ?: return
        val now = System.currentTimeMillis()
        val contact = MonitorRules.contact(tree) ?: return
        MonitorRules.historical(tree, now, DateFormat.is24HourFormat(this)).forEach {
            Base44Sender.sendOutgoing(this, contact, it.text, now, it.time, trigger, false)
        }
    }

    private fun snapshot(root: AccessibilityNodeInfo): ReadNode? {
        var count = 0
        fun copy(n: AccessibilityNodeInfo, depth: Int): ReadNode {
            require(++count <= 2000 && depth <= 40)
            val r = Rect()
            n.getBoundsInScreen(r)
            val children = ArrayList<ReadNode>()
            for (i in 0 until n.childCount) {
                val child = n.getChild(i) ?: continue
                try { if (child.isVisibleToUser) children.add(copy(child, depth + 1)) }
                finally { child.recycle() }
            }
            val id = n.viewIdResourceName.orEmpty()
            return ReadNode(
                if (id.startsWith("${BridgeConfig.WHATSAPP_BUSINESS_PACKAGE}:id/")) id.substringAfter(":id/") else "",
                n.text?.toString()?.trim().orEmpty(), n.contentDescription?.toString().orEmpty(),
                Box(r.left, r.top, r.right, r.bottom), n.isEditable, n.isScrollable, children
            )
        }
        return try { copy(root, 0) } catch (_: Exception) { null }
    }

    override fun onInterrupt() = Unit
}

internal data class Box(val left: Int, val top: Int, val right: Int, val bottom: Int) {
    val width get() = right - left
    val height get() = bottom - top
    val centerX get() = (left + right) / 2
    fun contains(b: Box) = b.left >= left && b.right <= right && b.top >= top && b.bottom <= bottom
}
internal data class ReadNode(
    val id: String, val text: String = "", val description: String = "",
    val box: Box, val editable: Boolean = false, val scrollable: Boolean = false,
    val children: List<ReadNode> = emptyList()
)
internal data class ManualMessage(val text: String, val time: String)

/** Pure acceptance rules, also exercised by unit tests. Unsupported layouts fail closed. */
internal object MonitorRules {
    private val zone = ZoneId.of("Asia/Singapore")
    private val clock = Regex("^(\\d{1,2}):(\\d{2})(?:\\s*([ap]m))?$", RegexOption.IGNORE_CASE)
    private val ui = setOf("home", "search", "searching", "google search", "new chat", "whatsapp business",
        "chats", "calls", "updates", "communities", "contacts", "select contact", "archived", "settings",
        "workshop status", "message", "type a message", "send", "camera", "attach", "emoji", "voice message",
        "video call", "voice call", "more options", "back", "sent", "delivered", "read", "edited",
        "go to most recent message", "enlarge photo", "view media", "pause ai 30 min", "you deleted this message")
    private val weekdays = DayOfWeek.values().associateBy { it.name.lowercase(Locale.ENGLISH) }
    private val dateIds = setOf("date", "date_header", "date_separator", "date_divider")
    private val timeIds = setOf("date", "timestamp", "message_time")
    fun normalize(s: String) = s.replace(Regex("[\\s\\u00a0\\u202f]+"), " ").trim().lowercase(Locale.ENGLISH)
    private fun noise(s: String): Boolean {
        val n = normalize(s).trimEnd('.', '…')
        return n in ui || n.startsWith("search") || n.startsWith("swipe down") || n.startsWith("button.") ||
            n.startsWith("forward image") || n.startsWith("forward video") ||
            Regex("^page \\d+ of \\d+\\.?$").matches(n)
    }
    fun validContact(s: String) = s.trim().length in 2..500 && !noise(s) && !s.contains('\n')
    fun usable(s: String) = s.trim().length in 1..5000 && !noise(s) &&
        !Regex("-\\s*replied by ai", RegexOption.IGNORE_CASE).containsMatchIn(normalize(s)) &&
        !clock.matches(normalize(s)) && !dateLike(s)
    fun identity(contact: String, text: String, time: String): String {
        // Length prefixes avoid collisions when a contact/message itself contains a pipe.
        val c = normalize(contact)
        val m = normalize(text)
        val input = "${c.length}:$c${m.length}:$m|$time"
        return MessageDigest.getInstance("SHA-256").digest(input.toByteArray(Charsets.UTF_8))
            .joinToString("") { "%02x".format(it) }
    }
    fun flatten(n: ReadNode): List<ReadNode> = listOf(n) + n.children.flatMap { flatten(it) }
    fun contact(root: ReadNode): String? {
        val nodes = flatten(root)
        if (nodes.any { it.id.contains("search", true) && (it.editable || it.id in setOf("search_src_text", "search_bar")) }) return null
        val title = nodes.filter { it.id == "conversation_name" }.singleOrNull() ?: return null
        if (!validContact(title.text) || title.box.top < root.box.top ||
            title.box.bottom > root.box.top + root.box.height * 0.24) return null
        // A title alone is not evidence of an open conversation (e.g. contact info/search results).
        if (nodes.count { it.id == "entry" && it.editable } != 1) return null
        return title.text.trim()
    }
    fun historical(root: ReadNode, now: Long, is24Hour: Boolean): List<ManualMessage> {
        if (contact(root) == null || root.box.width <= 0 || root.box.height <= 0) return emptyList()
        val nodes = flatten(root)
        val title = nodes.single { it.id == "conversation_name" }
        val compose = nodes.single { it.id == "entry" && it.editable }
        val anchors = nodes.filter { n ->
            n.id in dateIds && dateLike(n.text) && n.box.height > 0 && n.box.top >= title.box.bottom &&
                n.box.bottom < compose.box.top &&
                kotlin.math.abs(n.box.centerX - root.box.centerX) < root.box.width * 0.12 &&
                n.box.width < root.box.width * 0.65 &&
                // A date in a message/quote must never become a separator.
                !nodes.any { p -> p !== n && p.id in setOf("message_text", "quoted_text") && p.box.contains(n.box) }
        }.sortedBy { it.box.top }
        val result = LinkedHashSet<ManualMessage>()
        fun walk(n: ReadNode, ancestors: List<ReadNode>) {
            if (n.id == "message_text" && usable(n.text)) {
                val bubble = ancestors.asReversed().take(5).firstOrNull { p ->
                    val items = flatten(p)
                    !p.scrollable && !p.editable && p.box.width > 0 && p.box.height > 0 &&
                        p.box.width < root.box.width * 0.90 && p.box.height < root.box.height * 0.42 &&
                        items.count { it.id == "message_text" } == 1 &&
                        items.count { it.id in timeIds && clock.matches(normalize(it.text)) } == 1 &&
                        items.none { it.id.contains("quoted") || it.id.contains("caption") || it.id.contains("reactions") }
                }
                if (bubble != null) {
                    val b = bubble.box
                    val leftMargin = b.left - root.box.left
                    val rightMargin = root.box.right - b.right
                    val rightSide = b.centerX >= root.box.left + root.box.width * 0.58 &&
                        b.right >= root.box.left + root.box.width * 0.86 && rightMargin >= 0 &&
                        leftMargin >= root.box.width * 0.25 && leftMargin > rightMargin * 2 + root.box.width * 0.08
                    val items = flatten(bubble)
                    val times = items.filter { it.id in timeIds && clock.matches(normalize(it.text)) }
                    val ai = items.any { Regex("-\\s*replied by ai", RegexOption.IGNORE_CASE)
                        .containsMatchIn(normalize(it.text + " " + it.description)) }
                    // More than one clock-bearing node is ambiguous, even when both clocks read alike.
                    val otherClocks = items.any { it !== times.singleOrNull() &&
                        (clock.matches(normalize(it.text)) || clock.matches(normalize(it.description))) }
                    val t = times.singleOrNull()
                    if (rightSide && !ai && !otherClocks && t != null && root.box.contains(b) &&
                        b.contains(n.box) && b.contains(t.box) && b.top >= title.box.bottom &&
                        b.bottom <= compose.box.top && t.box.top >= n.box.top &&
                        anchors.none { it.box.top >= b.top && it.box.top < b.bottom }) {
                        val before = anchors.filter { it.box.bottom <= b.top }
                        val nearest = before.lastOrNull()
                        if (nearest != null && before.filter { it.box.top == nearest.box.top }.map { it.text }.distinct().size == 1) {
                            resolveTime(nearest.text, t.text, now, is24Hour)?.let { result.add(ManualMessage(n.text, it)) }
                        }
                    }
                }
            }
            n.children.forEach { walk(it, ancestors + n) }
        }
        walk(root, emptyList())
        return result.toList()
    }
    fun exactPostSend(root: ReadNode, expectedText: String, now: Long, is24Hour: Boolean): ManualMessage? {
        if (contact(root) == null || !usable(expectedText) || root.box.width <= 0 || root.box.height <= 0) return null
        val nodes = flatten(root)
        val title = nodes.singleOrNull { it.id == "conversation_name" } ?: return null
        val compose = nodes.singleOrNull { it.id == "entry" && it.editable } ?: return null
        val matches = ArrayList<ManualMessage>()

        fun walk(n: ReadNode, ancestors: List<ReadNode>) {
            if (n.id == "message_text" && normalize(n.text) == normalize(expectedText) && usable(n.text)) {
                val bubble = ancestors.asReversed().take(5).firstOrNull { p ->
                    val items = flatten(p)
                    !p.scrollable && !p.editable && p.box.width > 0 && p.box.height > 0 &&
                        p.box.width < root.box.width * 0.90 && p.box.height < root.box.height * 0.42 &&
                        items.count { it.id == "message_text" } == 1 &&
                        items.count { it.id in timeIds && clock.matches(normalize(it.text)) } == 1 &&
                        items.none { it.id.contains("quoted") || it.id.contains("caption") || it.id.contains("reactions") }
                }
                if (bubble != null) {
                    val b = bubble.box
                    val leftMargin = b.left - root.box.left
                    val rightMargin = root.box.right - b.right
                    val rightSide = b.centerX >= root.box.left + root.box.width * 0.58 &&
                        b.right >= root.box.left + root.box.width * 0.86 && rightMargin >= 0 &&
                        leftMargin >= root.box.width * 0.25 &&
                        leftMargin > rightMargin * 2 + root.box.width * 0.08
                    val items = flatten(bubble)
                    val times = items.filter { it.id in timeIds && clock.matches(normalize(it.text)) }
                    val ai = items.any {
                        Regex("-\\s*replied by ai", RegexOption.IGNORE_CASE)
                            .containsMatchIn(normalize(it.text + " " + it.description))
                    }
                    val otherClocks = items.any { it !== times.singleOrNull() &&
                        (clock.matches(normalize(it.text)) || clock.matches(normalize(it.description))) }
                    val t = times.singleOrNull()
                    if (rightSide && !ai && !otherClocks && t != null && root.box.contains(b) &&
                        b.contains(n.box) && b.contains(t.box) && b.top >= title.box.bottom &&
                        b.bottom <= compose.box.top && t.box.top >= n.box.top) {
                        resolveTime("Today", t.text, now, is24Hour)?.let {
                            matches.add(ManualMessage(n.text, it))
                        }
                    }
                }
            }
            n.children.forEach { walk(it, ancestors + n) }
        }

        walk(root, emptyList())
        return matches.distinct().singleOrNull()
    }

    private fun dateLike(s: String): Boolean {
        val n = normalize(s)
        return n in setOf("today", "yesterday") || n in weekdays ||
            Regex("^\\d{1,4}[/-]\\d{1,2}[/-]\\d{1,4}$").matches(n) ||
            Regex("^\\d{1,2} [a-z]{3,9}(?: \\d{4})?$").matches(n)
    }
    fun resolveTime(label: String, clockText: String, now: Long, is24Hour: Boolean): String? {
        val today = Instant.ofEpochMilli(now).atZone(zone).toLocalDate()
        val date = resolveDate(label, today) ?: return null
        val parts = clock.matchEntire(normalize(clockText)) ?: return null
        var hour = parts.groupValues[1].toInt()
        val minute = parts.groupValues[2].toInt()
        val ampm = parts.groupValues[3]
        if (minute !in 0..59) return null
        if (ampm.isNotEmpty()) {
            if (hour !in 1..12) return null
            hour = hour % 12 + if (ampm == "pm") 12 else 0
        } else if (!is24Hour || hour !in 0..23) return null
        val instant = date.atTime(LocalTime.of(hour, minute)).atZone(zone).toInstant()
        if (instant.isAfter(Instant.ofEpochMilli(now).truncatedTo(ChronoUnit.MINUTES))) return null
        return instant.toString()
    }
    private fun resolveDate(label: String, today: LocalDate): LocalDate? {
        val s = normalize(label)
        if (s == "today") return today
        if (s == "yesterday") return today.minusDays(1)
        weekdays[s]?.let {
            val days = (today.dayOfWeek.value - it.value + 7) % 7
            // WhatsApp labels today's messages Today; same weekday is ambiguous across weeks.
            return if (days in 1..6) today.minusDays(days.toLong()) else null
        }
        val numeric = Regex("^(\\d{1,2})[/-](\\d{1,2})[/-](\\d{4})$").matchEntire(s)
        if (numeric != null) {
            val a = numeric.groupValues[1].toInt()
            val b = numeric.groupValues[2].toInt()
            if (a in 1..12 && b in 1..12 && a != b) return null // D/M versus M/D
            val day = if (b > 12) b else a
            val month = if (b > 12) a else b
            return try { LocalDate.of(numeric.groupValues[3].toInt(), month, day).takeIf { !it.isAfter(today) } }
            catch (_: Exception) { null }
        }
        // No guessed year and no SMART normalization of impossible dates (e.g. 31 February).
        for (pattern in listOf("uuuu-MM-dd", "d MMM uuuu", "d MMMM uuuu")) {
            try {
                val formatter = java.time.format.DateTimeFormatterBuilder().parseCaseInsensitive()
                    .appendPattern(pattern).toFormatter(Locale.ENGLISH).withResolverStyle(ResolverStyle.STRICT)
                return LocalDate.parse(s, formatter).takeIf { !it.isAfter(today) }
            } catch (_: Exception) { }
        }
        return null
    }
}

