package sg.edwingarage.readonlybridge

import android.content.Context
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.time.Instant
import java.time.temporal.ChronoUnit
import java.util.concurrent.Executors

object Base44Sender {
    private val executor = Executors.newSingleThreadExecutor()
    fun sendOutgoing(context: Context, contactTitle: String, messageText: String,
        observedAtMs: Long, messageTime: String, detectedVia: String) {
        val app = context.applicationContext
        val contact = contactTitle.trim()
        val message = messageText.trim()
        if (!MonitorRules.validContact(contact) || !MonitorRules.usable(message)) return
        if (detectedVia !in setOf("accessibility_send_click", "accessibility_historical_right_bubble")) return
        val instant = try { Instant.parse(messageTime) } catch (_: Exception) { return }
        if (observedAtMs <= 0 || instant.toEpochMilli() <= 0 ||
            instant.isAfter(Instant.ofEpochMilli(observedAtMs)) || instant != instant.truncatedTo(ChronoUnit.MINUTES)) return
        val canonicalTime = instant.toString()
        val token = BridgeState.deviceToken(app)
        if (token.isBlank()) {
            BridgeState.saveObservation(app, contact, message, "Not paired with Base44")
            return
        }
        val deviceId = BridgeState.deviceId(app)
        val hash = MonitorRules.identity(contact, message, canonicalTime)
        if (!BridgeState.reserve(app, hash)) return
        val body = JSONObject().apply {
            put("event_id", "acc-$hash")
            put("source", "edwin_android_monitor_v2")
            put("package_name", BridgeConfig.WHATSAPP_BUSINESS_PACKAGE)
            put("contact_title", contact)
            put("message_text", message)
            put("observed_at_ms", observedAtMs)
            put("message_time", canonicalTime)
            put("whatsapp_time", canonicalTime)
            put("device_id", deviceId)
            put("direction", "outgoing")
            put("payload_hash", hash)
            put("meta", JSONObject().apply {
                put("reader_version", "2.0-manual-only")
                put("read_only", true)
                put("author", "human")
                put("detected_via", detectedVia)
                put("message_time", canonicalTime)
                put("whatsapp_time", canonicalTime)
                put("timestamp_confidence", if (detectedVia == "accessibility_send_click") "send_click" else "same_bubble_with_date")
            })
        }.toString()
        try {
            executor.execute {
                var conn: HttpURLConnection? = null
                try {
                    BridgeState.saveObservation(app, contact, message, "Manual message; uploading…")
                    conn = (URL(BridgeConfig.RECEIVER_URL).openConnection() as HttpURLConnection).apply {
                        requestMethod = "POST"
                        instanceFollowRedirects = false
                        connectTimeout = 10000
                        readTimeout = 10000
                        doOutput = true
                        setRequestProperty("Content-Type", "application/json")
                        setRequestProperty("X-Device-Id", deviceId)
                        setRequestProperty("X-Device-Token", token)
                    }
                    conn.outputStream.use { it.write(body.toByteArray(Charsets.UTF_8)) }
                    val code = conn.responseCode
                    val status = when {
                        code in 200..299 -> {
                            val saved = BridgeState.acknowledge(app, hash)
                            if (saved) "Uploaded to Base44 ($code)" else "Uploaded; dedupe persistence failed"
                        }
                        code == 401 -> "Pairing expired/invalid — pair again"
                        else -> "Base44 HTTP $code; may retry when observed again"
                    }
                    BridgeState.saveObservation(app, contact, message, status)
                } catch (e: Exception) {
                    BridgeState.saveObservation(app, contact, message, "Upload error: ${e.javaClass.simpleName}; may retry")
                } finally {
                    conn?.disconnect()
                    // Removes only the transient reservation. Successful identities remain committed.
                    BridgeState.release(app, hash)
                }
            }
        } catch (_: Exception) {
            BridgeState.release(app, hash)
        }
    }
}
