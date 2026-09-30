package sg.edwingarage.readonlybridge

import android.app.Activity
import android.content.ComponentName
import android.content.Intent
import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.provider.Settings
import android.text.InputType
import android.text.TextUtils
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import java.text.DateFormat
import java.util.Date

class MainActivity : Activity() {

    private lateinit var serviceStatus: TextView
    private lateinit var pairingStatus: TextView
    private lateinit var pairingCode: EditText
    private lateinit var lastStatus: TextView
    private lateinit var contactsStatus: TextView

    private val refresh = object : Runnable {
        override fun run() {
            refreshUi()
            lastStatus.postDelayed(this, 1000)
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val pad = (20 * resources.displayMetrics.density).toInt()
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(pad, pad, pad, pad)
        }

        root.addView(TextView(this).apply {
            text = "Edwin AI Monitor"
            textSize = 24f
        })

        root.addView(TextView(this).apply {
            text = "Read-only WhatsApp Business Accessibility bridge. It does not click, type or send messages."
            textSize = 15f
            setPadding(0, pad / 2, 0, pad)
        })

        pairingStatus = TextView(this).apply { textSize = 16f }
        root.addView(pairingStatus)

        pairingCode = EditText(this).apply {
            hint = "8-digit pairing code"
            inputType = InputType.TYPE_CLASS_NUMBER
            maxLines = 1
        }
        root.addView(
            pairingCode,
            ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            )
        )

        root.addView(Button(this).apply {
            text = "Pair with Base44"
            setOnClickListener {
                val code = pairingCode.text.toString().trim()
                if (code.isBlank()) {
                    pairingStatus.text = "Enter the pairing code first."
                } else {
                    pairingStatus.text = "Pairing…"
                    PairingClient.pair(this@MainActivity, code) { ok, message ->
                        runOnUiThread {
                            pairingStatus.text =
                                if (ok) "Base44 pairing: CONNECTED ✅" else message
                            if (ok) pairingCode.setText("")
                        }
                    }
                }
            }
        })

        serviceStatus = TextView(this).apply {
            textSize = 16f
            setPadding(0, pad, 0, 0)
        }
        root.addView(serviceStatus)

        root.addView(Button(this).apply {
            text = "Open Accessibility Settings"
            setOnClickListener {
                startActivity(Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS))
            }
        })

        contactsStatus = TextView(this).apply {
            textSize = 16f
            setPadding(0, pad, 0, 0)
        }
        root.addView(contactsStatus)

        root.addView(Button(this).apply {
            text = "Grant Contacts Permission"
            setOnClickListener {
                requestPermissions(
                    arrayOf(Manifest.permission.READ_CONTACTS, Manifest.permission.WRITE_CONTACTS),
                    1001
                )
            }
        })

        root.addView(Button(this).apply {
            text = "Open Notification Access"
            setOnClickListener {
                startActivity(Intent(Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS))
            }
        })

        root.addView(TextView(this).apply {
            text = "\nHow to use:\n1. Pair with Base44 once.\n2. Enable Edwin AI Monitor in Accessibility.\n3. Open WhatsApp Business normally.\n4. The app observes visible outgoing text only and sends the observation to Base44.\n"
            textSize = 14f
        })

        lastStatus = TextView(this).apply { textSize = 14f }
        root.addView(lastStatus)

        root.addView(TextView(this).apply {
            text = "\nBase44 receiver:\n${BridgeConfig.RECEIVER_URL}"
            textSize = 11f
        })

        setContentView(ScrollView(this).apply { addView(root) })
    }

    override fun onResume() {
        super.onResume()
        lastStatus.removeCallbacks(refresh)
        lastStatus.post(refresh)
    }

    override fun onPause() {
        lastStatus.removeCallbacks(refresh)
        super.onPause()
    }

    private fun refreshUi() {
        pairingStatus.text = if (BridgeState.isPaired(this)) {
            "Base44 pairing: CONNECTED ✅"
        } else {
            "Base44 pairing: NOT PAIRED"
        }

        serviceStatus.text = if (isAccessibilityServiceEnabled()) {
            "Accessibility reader: ENABLED ✅\n"
        } else {
            "Accessibility reader: DISABLED\n"
        }

        contactsStatus.text =
            if (checkSelfPermission(Manifest.permission.READ_CONTACTS) == PackageManager.PERMISSION_GRANTED &&
                checkSelfPermission(Manifest.permission.WRITE_CONTACTS) == PackageManager.PERMISSION_GRANTED) {
                "Contacts auto-save permission: ENABLED ✅"
            } else {
                "Contacts auto-save permission: NOT GRANTED"
            }

        val s = BridgeState.snapshot(this)
        val time = if (s.time > 0) {
            DateFormat.getDateTimeInstance().format(Date(s.time))
        } else {
            "—"
        }

        lastStatus.text = buildString {
            append("Last observation\n")
            append("Contact: ").append(if (s.contact.isBlank()) "—" else s.contact).append('\n')
            append("Message: ").append(if (s.message.isBlank()) "—" else s.message).append('\n')
            append("Status: ").append(s.status).append('\n')
            append("Time: ").append(time)
        }
    }

    private fun isAccessibilityServiceEnabled(): Boolean {
        val expected =
            ComponentName(this, WhatsAppReadService::class.java).flattenToString()
        val enabled = Settings.Secure.getString(
            contentResolver,
            Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES
        ) ?: return false

        val splitter = TextUtils.SimpleStringSplitter(':')
        splitter.setString(enabled)
        return splitter.any { it.equals(expected, ignoreCase = true) }
    }
}
