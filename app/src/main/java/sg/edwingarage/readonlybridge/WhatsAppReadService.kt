package sg.edwingarage.readonlybridge

import android.accessibilityservice.AccessibilityService
import android.graphics.Rect
import android.os.SystemClock
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo

class WhatsAppReadService : AccessibilityService() {

    private var lastFingerprint = ""
    private var lastSentElapsed = 0L

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        if (event == null) return
        if (event.packageName?.toString() != BridgeConfig.WHATSAPP_BUSINESS_PACKAGE) return

        val type = event.eventType
        if (type != AccessibilityEvent.TYPE_WINDOW_CONTENT_CHANGED &&
            type != AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED &&
            type != AccessibilityEvent.TYPE_VIEW_SCROLLED) return

        val root = rootInActiveWindow ?: return
        val screen = Rect()
        root.getBoundsInScreen(screen)
        if (screen.width() <= 0 || screen.height() <= 0) return

        val nodes = mutableListOf<TextNode>()
        collectText(root, nodes)

        val contact = inferContact(nodes, screen)
        val outgoing = inferLatestOutgoing(nodes, screen) ?: return
        val text = outgoing.text.trim()
        if (text.isBlank() || isUiChrome(text)) return

        val fingerprint = "$contact|$text|${outgoing.bounds.left}|${outgoing.bounds.top}"
        val nowElapsed = SystemClock.elapsedRealtime()
        if (fingerprint == lastFingerprint && nowElapsed - lastSentElapsed < 30_000) return

        lastFingerprint = fingerprint
        lastSentElapsed = nowElapsed
        val observed = System.currentTimeMillis()
        BridgeState.saveObservation(this, contact, text, "Observed; uploading…")
        Base44Sender.sendOutgoing(this, contact, text, observed)
    }

    override fun onInterrupt() = Unit

    private data class TextNode(
        val text: String,
        val bounds: Rect
    )

    private fun collectText(node: AccessibilityNodeInfo?, out: MutableList<TextNode>) {
        if (node == null) return

        val r = Rect()
        node.getBoundsInScreen(r)
        val text = node.text?.toString()?.trim().orEmpty()
        if (text.isNotBlank() && r.width() > 0 && r.height() > 0) {
            out += TextNode(text, Rect(r))
        }

        // contentDescription is useful for some WhatsApp UI elements, but avoid duplicating exact text.
        val desc = node.contentDescription?.toString()?.trim().orEmpty()
        if (desc.isNotBlank() && desc != text && r.width() > 0 && r.height() > 0) {
            out += TextNode(desc, Rect(r))
        }

        for (i in 0 until node.childCount) {
            collectText(node.getChild(i), out)
        }
    }

    private fun inferContact(nodes: List<TextNode>, screen: Rect): String {
        val topLimit = screen.top + (screen.height() * 0.22).toInt()
        return nodes
            .asSequence()
            .filter { it.bounds.top in screen.top until topLimit }
            .filter { it.bounds.centerX() > screen.left + screen.width() * 0.18 }
            .filter { it.bounds.centerX() < screen.left + screen.width() * 0.82 }
            .map { it.text }
            .filter { it.length in 2..100 }
            .filterNot { isUiChrome(it) }
            .firstOrNull()
            ?: ""
    }

    private fun inferLatestOutgoing(nodes: List<TextNode>, screen: Rect): TextNode? {
        val minY = screen.top + (screen.height() * 0.18).toInt()
        val maxY = screen.bottom - (screen.height() * 0.10).toInt()
        val rightThreshold = screen.left + (screen.width() * 0.52).toInt()

        // Version 1 deliberately uses only geometry exposed by Accessibility:
        // WhatsApp Business outgoing bubbles are normally aligned on the right.
        // We choose the lowest visible plausible text node on the right side.
        return nodes
            .asSequence()
            .filter { it.bounds.centerX() >= rightThreshold }
            .filter { it.bounds.top >= minY && it.bounds.bottom <= maxY }
            .filter { it.text.length in 1..5000 }
            .filterNot { isUiChrome(it.text) }
            .maxByOrNull { it.bounds.bottom }
    }

    private fun isUiChrome(text: String): Boolean {
        val t = text.trim().lowercase()
        if (t.isBlank()) return true
        if (t.matches(Regex("""\d{1,2}:\d{2}(\s?[ap]m)?"""))) return true
        if (t.matches(Regex("""\d{1,2}/\d{1,2}/\d{2,4}"""))) return true
        return t in setOf(
            "whatsapp business",
            "message",
            "type a message",
            "search",
            "video call",
            "voice call",
            "more options",
            "back",
            "camera",
            "attach",
            "emoji",
            "voice message"
        )
    }
}
