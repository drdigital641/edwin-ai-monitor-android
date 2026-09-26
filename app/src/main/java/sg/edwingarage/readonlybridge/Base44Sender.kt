package sg.edwingarage.readonlybridge

import android.content.Context
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.security.MessageDigest
import java.util.concurrent.Executors

object Base44Sender {
    private val executor = Executors.newSingleThreadExecutor()

    fun sendOutgoing(
        context: Context,
        contactTitle: String,
        messageText: String,
        observedAtMs: Long
    ) {
        val appContext = context.applicationContext
        val normalized = messageText.trim()
        if (normalized.isBlank()) return

        val deviceId = BridgeState.deviceId(appContext)
        val token = BridgeState.deviceToken(appContext)
        if (token.isBlank()) {
            BridgeState.saveObservation(appContext, contactTitle, normalized, "Not paired with Base44")
            return
        }

        val hashInput = "$deviceId|$contactTitle|$normalized|$observedAtMs"
        val payloadHash = sha256(hashInput)
        val eventId = "acc-" + payloadHash.take(32)

        executor.execute {
            var conn: HttpURLConnection? = null
            try {
                val body = JSONObject().apply {
                    put("event_id", eventId)
                    put("source", "android_accessibility")
                    put("package_name", BridgeConfig.WHATSAPP_BUSINESS_PACKAGE)
                    put("contact_title", contactTitle)
                    put("message_text", normalized)
                    put("observed_at_ms", observedAtMs)
                    put("device_id", deviceId)
                    put("direction", "outgoing")
                    put("payload_hash", payloadHash)
                    put("meta", JSONObject().apply {
                        put("reader_version", "1.1")
                        put("read_only", true)
                        put("detection", "right_side_accessibility_text")
                    })
                }.toString()

                conn = (URL(BridgeConfig.RECEIVER_URL).openConnection() as HttpURLConnection).apply {
                    requestMethod = "POST"
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
                    code in 200..299 -> "Uploaded to Base44 ($code)"
                    code == 401 -> "Pairing expired/invalid — pair again"
                    else -> "Base44 HTTP $code"
                }
                BridgeState.saveObservation(appContext, contactTitle, normalized, status)
            } catch (e: Exception) {
                BridgeState.saveObservation(
                    appContext,
                    contactTitle,
                    normalized,
                    "Upload error: ${e.javaClass.simpleName}"
                )
            } finally {
                conn?.disconnect()
            }
        }
    }

    private fun sha256(value: String): String {
        val bytes = MessageDigest.getInstance("SHA-256")
            .digest(value.toByteArray(Charsets.UTF_8))
        return bytes.joinToString("") { "%02x".format(it) }
    }
}
