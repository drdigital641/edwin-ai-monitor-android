package sg.edwingarage.readonlybridge
import android.accessibilityservice.AccessibilityService
import android.graphics.Rect
import android.os.SystemClock
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo
import java.time.Instant
import java.time.LocalTime
import java.time.ZoneId
import java.time.temporal.ChronoUnit

class WhatsAppReadService : AccessibilityService() {
 private var lastFingerprint=""; private var lastSentElapsed=0L
 private val clock=Regex("""\b(\d{1,2}):(\d{2})(?:\s*([ap]m))?\b""",RegexOption.IGNORE_CASE)
 private val zone=ZoneId.of("Asia/Singapore")
 override fun onAccessibilityEvent(event:AccessibilityEvent?){
  if(event==null||event.packageName?.toString()!=BridgeConfig.WHATSAPP_BUSINESS_PACKAGE)return
  if(event.eventType!=AccessibilityEvent.TYPE_WINDOW_CONTENT_CHANGED&&event.eventType!=AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED&&event.eventType!=AccessibilityEvent.TYPE_VIEW_SCROLLED)return
  val root=rootInActiveWindow?:return; val screen=Rect(); root.getBoundsInScreen(screen); if(screen.width()<=0||screen.height()<=0)return
  val nodes=mutableListOf<TextNode>(); collectText(root,nodes); val contact=inferContact(nodes,screen)
  val outgoing=inferLatestOutgoing(nodes,screen)?:return; val text=outgoing.text.trim(); if(text.isBlank()||isUiChrome(text))return
  val observed=System.currentTimeMillis()
  val whatsappClock=inferSameBubbleClock(outgoing,nodes,screen)?:return
  val messageTime=resolveTodayClock(whatsappClock,observed)?:return
  val fingerprint=contact+"|"+text+"|"+messageTime+"|"+outgoing.bounds.left+"|"+outgoing.bounds.top
  val elapsed=SystemClock.elapsedRealtime(); if(fingerprint==lastFingerprint&&elapsed-lastSentElapsed<30000)return
  lastFingerprint=fingerprint; lastSentElapsed=elapsed
  BridgeState.saveObservation(this,contact,text,"Observed with WhatsApp time; uploading…")
  Base44Sender.sendOutgoing(this,contact,text,observed,messageTime)
 }
 override fun onInterrupt()=Unit
 private data class TextNode(val text:String,val bounds:Rect)
 private fun collectText(node:AccessibilityNodeInfo?,out:MutableList<TextNode>){
  if(node==null)return; val r=Rect(); node.getBoundsInScreen(r)
  val text=node.text?.toString()?.trim().orEmpty(); if(text.isNotBlank()&&r.width()>0&&r.height()>0)out+=TextNode(text,Rect(r))
  val desc=node.contentDescription?.toString()?.trim().orEmpty(); if(desc.isNotBlank()&&desc!=text&&r.width()>0&&r.height()>0)out+=TextNode(desc,Rect(r))
  for(i in 0 until node.childCount)collectText(node.getChild(i),out)
 }
 private fun inferContact(nodes:List<TextNode>,screen:Rect):String{
  val top=screen.top+(screen.height()*0.22).toInt()
  return nodes.asSequence().filter{it.bounds.top in screen.top until top}.filter{it.bounds.centerX()>screen.left+screen.width()*0.18}.filter{it.bounds.centerX()<screen.left+screen.width()*0.82}.map{it.text}.filter{it.length in 2..100}.filterNot{isUiChrome(it)}.firstOrNull()?:""
 }
 private fun inferLatestOutgoing(nodes:List<TextNode>,screen:Rect):TextNode?{
  val minY=screen.top+(screen.height()*0.18).toInt(); val maxY=screen.bottom-(screen.height()*0.10).toInt(); val right=screen.left+(screen.width()*0.52).toInt()
  return nodes.asSequence().filter{it.bounds.centerX()>=right}.filter{it.bounds.top>=minY&&it.bounds.bottom<=maxY}.filter{it.text.length in 1..5000}.filterNot{isUiChrome(it.text)}.filterNot{clock.containsMatchIn(it.text)&&it.text.length<=20}.maxByOrNull{it.bounds.bottom}
 }
 private fun inferSameBubbleClock(message:TextNode,nodes:List<TextNode>,screen:Rect):String?{
  val slack=(screen.height()*0.025).toInt().coerceAtLeast(24)
  val candidates=nodes.asSequence().filter{it!==message}.flatMap{n->clock.findAll(n.text).map{m->Pair(n,m.value)}}.filter{(n,_)->
   n.bounds.centerX()>=screen.left+screen.width()*0.52&&n.bounds.left>=message.bounds.left-screen.width()*0.08&&n.bounds.top>=message.bounds.top-slack&&n.bounds.bottom<=message.bounds.bottom+slack*2&&n.bounds.right>=message.bounds.right-screen.width()*0.20
  }.map{it.second.trim()}.distinct().toList()
  return candidates.singleOrNull()
 }
 private fun resolveTodayClock(value:String,observedAt:Long):String?{
  val m=clock.find(value)?:return null; var hour=m.groupValues[1].toIntOrNull()?:return null; val minute=m.groupValues[2].toIntOrNull()?:return null; val ap=m.groupValues[3].lowercase()
  if(minute !in 0..59)return null
  if(ap.isNotEmpty()){if(hour !in 1..12)return null; hour=hour%12+if(ap=="pm")12 else 0}else if(hour !in 0..23)return null
  val observed=Instant.ofEpochMilli(observedAt).atZone(zone); val instant=observed.toLocalDate().atTime(LocalTime.of(hour,minute)).atZone(zone).toInstant()
  if(instant.isAfter(Instant.ofEpochMilli(observedAt).plus(1,ChronoUnit.MINUTES)))return null
  return instant.truncatedTo(ChronoUnit.MINUTES).toString()
 }
 private fun isUiChrome(text:String):Boolean{
  val t=text.trim().lowercase(); if(t.isBlank())return true
  if(t.matches(Regex("""\d{1,2}:\d{2}(\s?[ap]m)?"""))||t.matches(Regex("""\d{1,2}/\d{1,2}/\d{2,4}""")))return true
  return t in setOf("whatsapp business","message","type a message","search","video call","voice call","more options","back","camera","attach","emoji","voice message")
 }
}
