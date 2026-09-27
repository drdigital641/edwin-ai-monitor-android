package sg.edwingarage.readonlybridge

import android.content.Context
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.security.MessageDigest
import java.time.Instant
import java.util.concurrent.Executors

object Base44Sender {
    private val executor = Executors.newSingleThreadExecutor()

    fun sendOutgoing(
        context: Context,
        contactTitle: String,
        messageText: String,
        observedAtMs: Long,
        candidateMessageTime: String?,
        detectedVia: String,
        trustedSameBubble: Boolean
    ) {
        val app = context.applicationContext
        val contact = contactTitle.trim()
        val message = messageText.trim()
        if (!MonitorRules.validContact(contact) || !MonitorRules.usable(message)) return
        if (observedAtMs <= 0L) return

        val candidateCanonical = candidateMessageTime?.let {
            try { Instant.parse(it).toString() } catch (_: Exception) { null }
        }
        val authoritative = if (trustedSameBubble) candidateCanonical else null

        val deviceId = BridgeState.deviceId(app)
        val token = BridgeState.deviceToken(app)
        if (token.isBlank()) {
            BridgeState.saveObservation(app, contact, message, "Not paired with Base44")
            return
        }

        val identity = contact.lowercase() + "|" +
            message.replace(Regex("\\s+"), " ").trim().lowercase() + "|" +
            (if (trustedSameBubble) "trusted" else "untrusted") + "|" +
            (candidateCanonical ?: "no-time")
        val hash = sha256(identity)
        if (!BridgeState.reserve(app, hash)) return

        val meta = JSONObject().apply {
            put("reader_version", "2.2-v2-core-exact-bubble")
            put("read_only", true)
            put("author", "human")
            put("detected_via", detectedVia)
            if (candidateCanonical != null) put("candidate_message_time", candidateCanonical)
            if (authoritative != null) {
                put("message_time", authoritative)
                put("whatsapp_time", authoritative)
                put("timestamp_confidence", "exact_same_bubble")
                put("timestamp_provenance", "exact_same_bubble_clock")
                put("direction_confidence", "right_side_exact_bubble")
            } else {
                put("timestamp_confidence", "historical_candidate_untrusted")
                put("timestamp_provenance", "untrusted_historical_clock")
                put("direction_confidence", "right_side_id_verified_candidate")
            }
        }

        val body = JSONObject().apply {
            put("event_id", "acc-" + hash.take(32))
            put("source", "android_accessibility")
            put("package_name", BridgeConfig.WHATSAPP_BUSINESS_PACKAGE)
            put("contact_title", contact)
            put("message_text", message)
            put("observed_at_ms", observedAtMs)
            if (authoritative != null) {
                put("message_time", authoritative)
                put("whatsapp_time", authoritative)
            }
            put("device_id", deviceId)
            put("direction", "outgoing")
            put("payload_hash", hash)
            put("meta", meta)
        }.toString()

        try {
            executor.execute {
                var conn: HttpURLConnection? = null
                try {
                    BridgeState.saveObservation(app, contact, message, "Manual message; uploading…")
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
                        BridgeState.saveObservation(app, contact, message, "Uploaded to Base44 ($code)")
                    } else {
                        BridgeState.release(app, hash)
                        val status = if (code == 401) "Pairing expired/invalid — pair again" else "Base44 HTTP $code"
                        BridgeState.saveObservation(app, contact, message, status)
                    }
                } catch (err: Exception) {
                    BridgeState.release(app, hash)
                    BridgeState.saveObservation(app, contact, message, "Upload error: " + err.javaClass.simpleName)
                } finally {
                    conn?.disconnect()
                }
            }
        } catch (_: Exception) {
            BridgeState.release(app, hash)
        }
    }

    private fun sha256(value: String) =
        MessageDigest.getInstance("SHA-256")
            .digest(value.toByteArray(Charsets.UTF_8))
            .joinToString("") { "%02x".format(it) }
}
