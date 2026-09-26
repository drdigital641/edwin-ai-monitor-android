package sg.edwingarage.readonlybridge

import android.content.Context
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.util.concurrent.Executors

object PairingClient {
    private val executor = Executors.newSingleThreadExecutor()

    fun pair(
        context: Context,
        pairingCode: String,
        callback: (Boolean, String) -> Unit
    ) {
        val appContext = context.applicationContext
        executor.execute {
            var conn: HttpURLConnection? = null
            try {
                val deviceId = BridgeState.deviceId(appContext)
                val body = JSONObject().apply {
                    put("pairing_code", pairingCode.trim())
                    put("device_id", deviceId)
                    put("label", "Edwin Samsung")
                }.toString()

                conn = (URL(BridgeConfig.PAIR_URL).openConnection() as HttpURLConnection).apply {
                    requestMethod = "POST"
                    connectTimeout = 10000
                    readTimeout = 10000
                    doOutput = true
                    setRequestProperty("Content-Type", "application/json")
                }

                conn.outputStream.use { it.write(body.toByteArray(Charsets.UTF_8)) }
                val code = conn.responseCode
                val input = if (code in 200..299) conn.inputStream else conn.errorStream
                val response = input?.bufferedReader()?.use { it.readText() }.orEmpty()

                if (code in 200..299) {
                    val token = JSONObject(response).optString("device_token")
                    if (token.isNotBlank()) {
                        BridgeState.saveDeviceToken(appContext, token)
                        callback(true, "Paired successfully")
                    } else {
                        callback(false, "Pairing response missing token")
                    }
                } else {
                    callback(false, "Pairing failed (HTTP $code)")
                }
            } catch (e: Exception) {
                callback(false, "Pairing error: ${e.javaClass.simpleName}")
            } finally {
                conn?.disconnect()
            }
        }
    }
}
