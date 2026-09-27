package sg.edwingarage.readonlybridge

import android.content.Context
import org.json.JSONObject
import java.util.UUID

object BridgeState {
    private const val PREF = "bridge_state"
    private var ledger: DedupeLedger? = null

    fun deviceId(context: Context): String {
        val p = context.getSharedPreferences(PREF, Context.MODE_PRIVATE)
        val existing = p.getString("device_id", null)
        if (!existing.isNullOrBlank()) return existing
        val created = "edwin-" + UUID.randomUUID().toString()
        p.edit().putString("device_id", created).apply()
        return created
    }
    fun saveDeviceToken(context: Context, token: String) {
        context.getSharedPreferences(PREF, Context.MODE_PRIVATE).edit().putString("device_token", token).apply()
    }
    fun deviceToken(context: Context): String =
        context.getSharedPreferences(PREF, Context.MODE_PRIVATE).getString("device_token", "") ?: ""
    fun isPaired(context: Context) = deviceToken(context).isNotBlank()

    private fun dedupe(context: Context): DedupeLedger {
        ledger?.let { return it }
        val saved = LinkedHashMap<String, Long>()
        try {
            val data = JSONObject(context.getSharedPreferences(PREF, Context.MODE_PRIVATE).getString("dedupe_v2", "{}") ?: "{}")
            data.keys().forEach { key -> saved[key] = data.optLong(key) }
        } catch (_: Exception) { }
        return DedupeLedger(saved).also { ledger = it }
    }
    @Synchronized
    fun reserve(context: Context, key: String) = dedupe(context).reserve(key, System.currentTimeMillis())

    /** Called only after a successful HTTP response, never when an observation is queued. */
    @Synchronized
    fun acknowledge(context: Context, key: String): Boolean {
        val data = dedupe(context).acknowledge(key, System.currentTimeMillis())
        return context.getSharedPreferences(PREF, Context.MODE_PRIVATE).edit()
            .putString("dedupe_v2", JSONObject(data).toString()).commit()
    }
    @Synchronized
    fun release(context: Context, key: String) { dedupe(context).release(key) }

    fun saveObservation(context: Context, contact: String, message: String, status: String) {
        context.getSharedPreferences(PREF, Context.MODE_PRIVATE).edit()
            .putString("last_contact", contact).putString("last_message", message)
            .putString("last_status", status).putLong("last_time", System.currentTimeMillis()).apply()
    }
    data class Snapshot(val contact: String, val message: String, val status: String, val time: Long)
    fun snapshot(context: Context): Snapshot {
        val p = context.getSharedPreferences(PREF, Context.MODE_PRIVATE)
        return Snapshot(p.getString("last_contact", "") ?: "", p.getString("last_message", "") ?: "",
            p.getString("last_status", "No event yet") ?: "No event yet", p.getLong("last_time", 0L))
    }
}

/** In-flight reservations are transient; only acknowledged identities survive process restarts. */
internal class DedupeLedger(saved: Map<String, Long> = emptyMap()) {
    private val committed = LinkedHashMap(saved)
    private val inFlight = HashSet<String>()
    private val retention = 30L * 24 * 60 * 60 * 1000
    private fun prune(now: Long) {
        committed.entries.removeAll { now - it.value >= retention }
        if (committed.size > 5000) {
            committed.entries.sortedBy { it.value }.take(committed.size - 5000).forEach { committed.remove(it.key) }
        }
    }
    fun reserve(key: String, now: Long): Boolean {
        prune(now)
        if (key in committed || key in inFlight || inFlight.size >= 128) return false
        return inFlight.add(key)
    }
    fun acknowledge(key: String, now: Long): Map<String, Long> {
        if (inFlight.remove(key)) committed[key] = now
        prune(now)
        return committed.toMap()
    }
    fun release(key: String) { inFlight.remove(key) }
}
