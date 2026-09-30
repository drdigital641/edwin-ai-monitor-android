package sg.edwingarage.readonlybridge

import android.app.Notification
import android.app.Person
import android.service.notification.NotificationListenerService
import android.service.notification.StatusBarNotification

class WhatsAppNotificationNameService : NotificationListenerService() {

    override fun onNotificationPosted(sbn: StatusBarNotification?) {
        if (sbn == null || sbn.packageName != BridgeConfig.WHATSAPP_BUSINESS_PACKAGE) return
        val n = sbn.notification ?: return
        val extras = n.extras ?: return

        val title = extras.getCharSequence(Notification.EXTRA_TITLE)?.toString()?.trim().orEmpty()
        val candidateName = cleanName(title)
        if (candidateName.isBlank()) return

        val phone = extractPhone(n, extras) ?: return
        if (looksLikePhone(candidateName)) return
        val normalizedPhone = normalizePhone(phone)
        if (normalizedPhone.isBlank()) return

        getSharedPreferences(PREFS, MODE_PRIVATE)
            .edit()
            .putString("name_" + normalizedPhone, candidateName)
            .putLong("time_" + normalizedPhone, System.currentTimeMillis())
            .apply()
    }

    private fun extractPhone(notification: Notification, extras: android.os.Bundle): String? {
        val people = extras.getParcelableArray(Notification.EXTRA_PEOPLE_LIST)
        people?.forEach { item ->
            val person = item as? Person ?: return@forEach
            phoneFromUri(person.uri)?.let { return it }
        }

        val messages = Notification.MessagingStyle.Message.getMessagesFromBundleArray(
            extras.getParcelableArray(Notification.EXTRA_MESSAGES)
        )
        messages?.asReversed()?.forEach { message ->
            phoneFromUri(message.senderPerson?.uri)?.let { return it }
        }

        val shortcut = notification.shortcutId.orEmpty()
        val digits = shortcut.replace(Regex("\\D"), "")
        if (digits.length in 10..15) return digits

        return null
    }

    private fun phoneFromUri(uri: String?): String? {
        if (uri.isNullOrBlank()) return null
        val digits = uri.replace(Regex("\\D"), "")
        return digits.takeIf { it.length in 10..15 }
    }

    private fun normalizePhone(value: String): String {
        val digits = value.replace(Regex("\\D"), "")
        return when {
            Regex("^[689]\\d{7}$").matches(digits) -> "65" + digits
            Regex("^65[689]\\d{7}$").matches(digits) -> digits
            else -> digits
        }
    }

    private fun looksLikePhone(value: String): Boolean {
        val stripped = value.replace(Regex("[\\d+\\s()-]"), "")
        val digits = value.replace(Regex("\\D"), "")
        return stripped.isBlank() && digits.length in 8..15
    }

    private fun cleanName(value: String): String =
        value.replace(Regex("[\\n\\r\\t]"), " ")
            .replace(Regex("\\s+"), " ")
            .trim()
            .take(100)

    companion object {
        const val PREFS = "whatsapp_notification_names"
        const val MAX_AGE_MS = 7L * 24 * 60 * 60 * 1000

        fun cachedName(context: android.content.Context, phone: String): String {
            val digits = phone.replace(Regex("\\D"), "")
            val key = when {
                Regex("^[689]\\d{7}$").matches(digits) -> "65" + digits
                Regex("^65[689]\\d{7}$").matches(digits) -> digits
                else -> digits
            }
            if (key.isBlank()) return ""
            val prefs = context.getSharedPreferences(PREFS, MODE_PRIVATE)
            val time = prefs.getLong("time_" + key, 0L)
            if (time <= 0L || System.currentTimeMillis() - time > MAX_AGE_MS) return ""
            return prefs.getString("name_" + key, "").orEmpty().trim()
        }
    }
}
