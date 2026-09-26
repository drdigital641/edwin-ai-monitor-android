package sg.edwingarage.readonlybridge

import android.content.Context
import java.util.UUID

object BridgeState {
    private const val PREF = "bridge_state"
    private const val KEY_DEVICE_ID = "device_id"
    private const val KEY_DEVICE_TOKEN = "device_token"
    private const val KEY_LAST_MESSAGE = "last_message"
    private const val KEY_LAST_CONTACT = "last_contact"
    private const val KEY_LAST_STATUS = "last_status"
    private const val KEY_LAST_TIME = "last_time"

    fun deviceId(context: Context): String {
        val p = context.getSharedPreferences(PREF, Context.MODE_PRIVATE)
        val existing = p.getString(KEY_DEVICE_ID, null)
        if (!existing.isNullOrBlank()) return existing
        val created = "edwin-" + UUID.randomUUID().toString()
        p.edit().putString(KEY_DEVICE_ID, created).apply()
        return created
    }

    fun saveDeviceToken(context: Context, token: String) {
        context.getSharedPreferences(PREF, Context.MODE_PRIVATE)
            .edit()
            .putString(KEY_DEVICE_TOKEN, token)
            .apply()
    }

    fun deviceToken(context: Context): String =
        context.getSharedPreferences(PREF, Context.MODE_PRIVATE)
            .getString(KEY_DEVICE_TOKEN, "") ?: ""

    fun isPaired(context: Context): Boolean = deviceToken(context).isNotBlank()

    fun saveObservation(context: Context, contact: String, message: String, status: String) {
        context.getSharedPreferences(PREF, Context.MODE_PRIVATE).edit()
            .putString(KEY_LAST_CONTACT, contact)
            .putString(KEY_LAST_MESSAGE, message)
            .putString(KEY_LAST_STATUS, status)
            .putLong(KEY_LAST_TIME, System.currentTimeMillis())
            .apply()
    }

    data class Snapshot(
        val contact: String,
        val message: String,
        val status: String,
        val time: Long
    )

    fun snapshot(context: Context): Snapshot {
        val p = context.getSharedPreferences(PREF, Context.MODE_PRIVATE)
        return Snapshot(
            p.getString(KEY_LAST_CONTACT, "") ?: "",
            p.getString(KEY_LAST_MESSAGE, "") ?: "",
            p.getString(KEY_LAST_STATUS, "No event yet") ?: "No event yet",
            p.getLong(KEY_LAST_TIME, 0L)
        )
    }
}
