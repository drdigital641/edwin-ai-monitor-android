package sg.edwingarage.readonlybridge
import android.content.Context
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.security.MessageDigest
import java.time.Instant
import java.util.concurrent.Executors

object Base44Sender {
 private val executor=Executors.newSingleThreadExecutor()
 fun sendOutgoing(context:Context,contactTitle:String,messageText:String,observedAtMs:Long,messageTime:String){
  val app=context.applicationContext; val message=messageText.trim(); if(message.isBlank())return
  val canonical=try{Instant.parse(messageTime).toString()}catch(_:Exception){return}
  val deviceId=BridgeState.deviceId(app); val token=BridgeState.deviceToken(app)
  if(token.isBlank()){BridgeState.saveObservation(app,contactTitle,message,"Not paired with Base44");return}
  val hash=sha256(deviceId+"|"+contactTitle+"|"+message+"|"+canonical); val eventId="acc-"+hash.take(32)
  executor.execute{
   var conn:HttpURLConnection?=null
   try{
    val body=JSONObject().apply{
     put("event_id",eventId);put("source","android_accessibility");put("package_name",BridgeConfig.WHATSAPP_BUSINESS_PACKAGE)
     put("contact_title",contactTitle);put("message_text",message);put("observed_at_ms",observedAtMs)
     put("message_time",canonical);put("whatsapp_time",canonical);put("device_id",deviceId);put("direction","outgoing");put("payload_hash",hash)
     put("meta",JSONObject().apply{put("reader_version","1.2-same-bubble-time");put("read_only",true);put("detection","right_side_accessibility_text");put("message_time",canonical);put("whatsapp_time",canonical);put("timestamp_confidence","same_visible_right_bubble")})
    }.toString()
    conn=(URL(BridgeConfig.RECEIVER_URL).openConnection() as HttpURLConnection).apply{requestMethod="POST";connectTimeout=10000;readTimeout=10000;doOutput=true;setRequestProperty("Content-Type","application/json");setRequestProperty("X-Device-Id",deviceId);setRequestProperty("X-Device-Token",token)}
    conn.outputStream.use{it.write(body.toByteArray(Charsets.UTF_8))}; val code=conn.responseCode
    val status=if(code in 200..299)"Uploaded to Base44 ("+code+")" else if(code==401)"Pairing expired/invalid — pair again" else "Base44 HTTP "+code
    BridgeState.saveObservation(app,contactTitle,message,status)
   }catch(e:Exception){BridgeState.saveObservation(app,contactTitle,message,"Upload error: "+e.javaClass.simpleName)}finally{conn?.disconnect()}
  }
 }
 private fun sha256(value:String)=MessageDigest.getInstance("SHA-256").digest(value.toByteArray(Charsets.UTF_8)).joinToString(""){"%02x".format(it)}
}
