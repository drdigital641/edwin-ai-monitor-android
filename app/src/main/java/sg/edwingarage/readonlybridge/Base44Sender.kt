package sg.edwingarage.readonlybridge

import android.content.Context
import android.graphics.Rect
import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.security.MessageDigest
import java.time.Instant
import java.util.concurrent.Executors

/**
 * Uploads raw sensor evidence to the Base44 monitor app.
 *
 * Critical timestamp rule:
 * - observedAtMs is scanner observation time only.
 * - messageTime/whatsapp_time is sent only when trustedSameBubble=true.
 * - Base44 remains the normalization boundary and preserves raw evidence separately.
 */
object Base44Sender {
    private val executor = Executors.newSingleThreadExecutor()

    fun sendOutgoing(
        context: Context,
        contactTitle: String,
        messageText: String,
        observedAtMs: Long,
        messageTime: String?,
        trigger: String,
        selectedBounds: Rect,
        nearbyCandidates: JSONArray,
        trustedSameBubble: Boolean
    ) {
        val app = context.applicationContext
        val message = messageText.trim()
        if (message.isBlank()) return

        val canonical = if (trustedSameBubble) {
            messageTime?.let {
                try { Instant.parse(it).toString() } catch (_: Exception) { null }
            }
        } else null

        val deviceId = BridgeState.deviceId(app)
        val token = BridgeState.deviceToken(app)
        if (token.isBlank()) {
            BridgeState.saveObservation(app, contactTitle, message, "Not paired with Base44")
            return
        }

        val identityTime = canonical ?: "untrusted"
        val identity = deviceId + "|" + contactTitle.trim().lowercase() + "|" +
            message.replace(Regex("\\s+"), " ").trim().lowercase() + "|" +
            identityTime + "|" + selectedBounds.left + "|" + selectedBounds.top
        val hash = sha256(identity)
        val eventId = "acc-" + hash.take(32)

        if (!BridgeState.reserve(app, hash)) return

        executor.execute {
            var conn: HttpURLConnection? = null
            try {
                val meta = JSONObject().apply {
                    put("reader_version", "2.1-exact-bubble-time")
                    put("read_only", true)
                    put("detection", "right_side_accessibility_text")
                    put("capture_trigger", trigger)
                    put(
                        "selected_bounds",
                        selectedBounds.left.toString() + "," + selectedBounds.top + "," +
                            selectedBounds.right + "," + selectedBounds.bottom
                    )
                    put("nearby_right_candidates", nearbyCandidates)
                    put("author", "human")
                    if (canonical != null) {
                        put("message_time", canonical)
                        put("whatsapp_time", canonical)
                        put("timestamp_confidence", "exact_same_bubble")
                        put("timestamp_provenance", "exact_same_bubble_clock")
                        put("direction_confidence", "right_side_exact_bubble")
                    } else {
                        put("timestamp_confidence", "historical_same_container_untrusted")
                        put("timestamp_provenance", "untrusted_historical_clock")
                        put("direction_confidence", "right_side_historical_candidate")
                    }
                }

                val body = JSONObject().apply {
                    put("event_id", eventId)
                    put("source", "android_accessibility")
                    put("package_name", BridgeConfig.WHATSAPP_BUSINESS_PACKAGE)
                    put("contact_title", contactTitle)
                    put("message_text", message)
                    put("observed_at_ms", observedAtMs)
                    if (canonical != null) {
                        put("message_time", canonical)
                        put("whatsapp_time", canonical)
                    }
                    put("device_id", deviceId)
                    put("direction", "outgoing")
                    put("payload_hash", hash)
                    put("meta", meta)
                }.toString()

                conn = (URL(BridgeConfig.RECEIVER_URL).openConnection() as HttpURLConnection).apply {
                    requestMethod = "POST"
                    connectTimeout = 10_000
                    readTimeout = 10_000
                    doOutput = true
                    setRequestProperty("Content-Type", "application/json")
                    setRequestProperty("X-Device-Id", deviceId)
                    setRequestProperty("X-Device-Token", token)
                }
                conn.outputStream.use { it.write(body.toByteArray(Charsets.UTF_8)) }
                val code = conn.responseCode
                if (code in 200..299) {
                    BridgeState.acknowledge(app, hash)
                    BridgeState.saveObservation(app, contactTitle, message, "Uploaded to Base44 ($code)")
                } else {
                    BridgeState.release(app, hash)
                    val status = if (code == 401) "Pairing expired/invalid — pair again" else "Base44 HTTP $code"
                    BridgeState.saveObservation(app, contactTitle, message, status)
                }
            } catch (e: Exception) {
                BridgeState.release(app, hash)
                BridgeState.saveObservation(app, contactTitle, message, "Upload error: " + e.javaClass.simpleName)
            } finally {
                conn?.disconnect()
            }
        }
    }

    private fun sha256(value: String) =
        MessageDigest.getInstance("SHA-256")
            .digest(value.toByteArray(Charsets.UTF_8))
            .joinToString("") { "%02x".format(it) }
}
