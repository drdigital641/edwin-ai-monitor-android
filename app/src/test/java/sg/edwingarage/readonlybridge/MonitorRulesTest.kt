package sg.edwingarage.readonlybridge

import org.junit.Assert.*
import org.junit.Test
import java.time.Instant

class MonitorRulesTest {
    private val now = Instant.parse("2026-09-27T04:00:00Z").toEpochMilli()
    private fun bubble(text: String = "Your car is ready", x: Int = 450, extras: List<ReadNode> = emptyList()) =
        ReadNode("bubble", box = Box(x, 400, x + 500, 500), children = listOf(
            ReadNode("message_text", text, box = Box(x + 15, 420, x + 420, 460)),
            ReadNode("date", "11:30 am", box = Box(x + 350, 460, x + 480, 485))
        ) + extras)
    private fun chat(b: ReadNode = bubble(), date: String? = "Today", title: String = "Customer Tan",
        extra: List<ReadNode> = emptyList()): ReadNode =
        ReadNode("root", box = Box(0, 0, 1000, 2000), children = listOf(
            ReadNode("conversation_name", title, box = Box(150, 50, 650, 120)),
            ReadNode("entry", "", box = Box(80, 1800, 800, 1900), editable = true), b
        ) + (date?.let { listOf(ReadNode("date_header", it, box = Box(400, 200, 600, 240))) } ?: emptyList()) + extra)

    @Test fun acceptsSameBubbleAndSingaporeDate() {
        assertEquals(listOf(ManualMessage("Your car is ready", "2026-09-27T03:30:00Z")),
            MonitorRules.historical(chat(), now, false))
    }
    @Test fun rejectsHomeSearchAndMissingContact() {
        for (title in listOf("", "Home", "Search…", "New chat", "WhatsApp Business", "Page 2 of 5"))
            assertTrue(MonitorRules.historical(chat(title = title), now, false).isEmpty())
        assertNull(MonitorRules.contact(chat().copy(children = chat().children.filter { it.id != "entry" })))
        assertNull(MonitorRules.contact(chat(extra = listOf(
            ReadNode("search_src_text", "car", box = Box(0, 100, 1000, 200), editable = true)))))
    }
    @Test fun ignoresCustomerAndAi() {
        assertTrue(MonitorRules.historical(chat(bubble(x = 50)), now, false).isEmpty())
        assertTrue(MonitorRules.historical(chat(bubble("Ready -Replied by AI")), now, false).isEmpty())
        val marker = ReadNode("status", description = "-Replied by AI", box = Box(800, 490, 900, 500))
        assertTrue(MonitorRules.historical(chat(bubble(extras = listOf(marker))), now, false).isEmpty())
    }
    @Test fun rejectsMissingDateUnboundClockAndMultipleClocks() {
        assertTrue(MonitorRules.historical(chat(date = null), now, false).isEmpty())
        val noTime = bubble().copy(children = bubble().children.filter { it.id == "message_text" })
        assertTrue(MonitorRules.historical(chat(noTime, extra = listOf(
            ReadNode("date", "11:30 am", box = Box(850, 550, 950, 580)))), now, false).isEmpty())
        val sameClock = ReadNode("timestamp", "11:30 am", box = Box(850, 485, 950, 500))
        assertTrue(MonitorRules.historical(chat(bubble(extras = listOf(sameClock))), now, false).isEmpty())
        val secondMessage = ReadNode("message_text", "Another message", box = Box(460, 490, 800, 500))
        assertTrue(MonitorRules.historical(chat(bubble(extras = listOf(secondMessage))), now, false).isEmpty())
    }
    @Test fun rejectsDateTextInsideMessageAsAnchor() {
        val c = chat(date = null, extra = listOf(ReadNode("message_text", "Today", box = Box(400, 200, 600, 240))))
        assertTrue(MonitorRules.historical(c, now, false).isEmpty())
    }
    @Test fun strictDatesClocksAndWeekdays() {
        assertEquals("2026-09-26T15:59:00Z", MonitorRules.resolveTime("Yesterday", "11:59 pm", now, false))
        assertEquals("2026-09-25T03:30:00Z", MonitorRules.resolveTime("Friday", "11:30 am", now, false))
        assertEquals("2026-09-26T03:30:00Z", MonitorRules.resolveTime("26 September 2026", "11:30", now, true))
        assertEquals("2026-09-26T03:30:00Z", MonitorRules.resolveTime("26/09/2026", "11:30", now, true))
        for (date in listOf("03/04/2026", "31 February 2026", "31/02/2026", "26 Sep", "Sunday", "26/09/26"))
            assertNull(MonitorRules.resolveTime(date, "11:30 am", now, false))
        for (time in listOf("13:30 pm", "12:60 pm", "24:00", "11:30", "12:01 pm"))
            assertNull(MonitorRules.resolveTime("Today", time, now, false))
    }
    @Test fun singaporeMidnightAndAmPm() {
        val midnight = Instant.parse("2026-09-26T16:01:00Z").toEpochMilli()
        assertEquals("2026-09-26T16:00:00Z", MonitorRules.resolveTime("Today", "12:00 am", midnight, false))
        assertEquals("2026-09-26T15:59:00Z", MonitorRules.resolveTime("Yesterday", "11:59 pm", midnight, false))
    }
    @Test fun identityUsesAuthoritativeTimeAndNormalizedText() {
        val a = MonitorRules.identity(" Tan ", "Car  ready", "2026-09-27T03:30:00Z")
        assertEquals(a, MonitorRules.identity("tan", "car\nready", "2026-09-27T03:30:00Z"))
        assertNotEquals(a, MonitorRules.identity("tan", "car ready", "2026-09-27T03:31:00Z"))
        assertNotEquals(MonitorRules.identity("a|b", "c", "t"), MonitorRules.identity("a", "b|c", "t"))
    }
    @Test fun retriesFailuresAndSuppressesInflightAndSuccessfulRescans() {
        val ledger = DedupeLedger()
        assertTrue(ledger.reserve("a", now))
        assertFalse(ledger.reserve("a", now))
        ledger.release("a")
        assertTrue(ledger.reserve("a", now))
        val saved = ledger.acknowledge("a", now)
        ledger.release("a")
        assertFalse(ledger.reserve("a", now + 1))
        val restarted = DedupeLedger(saved)
        assertFalse(restarted.reserve("a", now + 1))
        assertTrue(restarted.reserve("a", now + 30L * 24 * 60 * 60 * 1000))
    }
    @Test fun boundedRetentionAndUnacknowledgedRestart() {
        val ledger = DedupeLedger()
        var saved: Map<String, Long> = emptyMap()
        for (i in 0..5000) {
            assertTrue(ledger.reserve("k$i", now + i))
            saved = ledger.acknowledge("k$i", now + i)
        }
        assertEquals(5000, saved.size)
        assertFalse(saved.containsKey("k0"))
        assertTrue(ledger.reserve("pending", now + 6000))
        assertTrue(DedupeLedger(saved).reserve("pending", now + 6000))
    }
}
