package sg.edwingarage.readonlybridge

import android.content.BroadcastReceiver
import android.content.ContentProviderOperation
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.provider.ContactsContract
import android.widget.Toast

class ContactSaveReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action != "sg.edwingarage.readonlybridge.CREATE_CONTACT") return

        val phone = intent.getStringExtra("phone")?.trim().orEmpty()
        val carModel = intent.getStringExtra("car_model")?.trim().orEmpty()
        val suppliedWhatsappName = intent.getStringExtra("whatsapp_name")?.trim().orEmpty()
        val unsaved = intent.getStringExtra("unsaved")?.trim()?.lowercase() in setOf("true", "1", "yes")
        if (!unsaved || phone.isBlank() || carModel.isBlank()) return

        val whatsappName = if (suppliedWhatsappName.isNotBlank()) {
            suppliedWhatsappName
        } else {
            WhatsAppNotificationNameService.cachedName(context, phone)
        }
        if (whatsappName.isBlank()) {
            Base44Sender.sendContactSaveStatus(context, phone, "", carModel, "", "skipped", "no_whatsapp_name_or_fallback")
            return
        }

        if (context.checkSelfPermission(android.Manifest.permission.READ_CONTACTS) != PackageManager.PERMISSION_GRANTED ||
            context.checkSelfPermission(android.Manifest.permission.WRITE_CONTACTS) != PackageManager.PERMISSION_GRANTED) {
            Toast.makeText(context, "Grant Contacts permission in Edwin AI Monitor.", Toast.LENGTH_LONG).show()
            Base44Sender.sendContactSaveStatus(context, phone, "", carModel, whatsappName, "skipped", "contacts_permission_missing")
            return
        }

        if (contactExists(context, phone)) {
            Base44Sender.sendContactSaveStatus(context, phone, "", carModel, whatsappName, "skipped", "already_exists")
            return
        }

        val displayName = (clean(carModel) + " " + clean(whatsappName)).replace(Regex("\\s+"), " ").trim()
        if (displayName.isBlank()) {
            Base44Sender.sendContactSaveStatus(context, phone, "", carModel, whatsappName, "skipped", "empty_display_name")
            return
        }

        val ops = arrayListOf<ContentProviderOperation>()
        ops += ContentProviderOperation.newInsert(ContactsContract.RawContacts.CONTENT_URI)
            .withValue(ContactsContract.RawContacts.ACCOUNT_TYPE, null)
            .withValue(ContactsContract.RawContacts.ACCOUNT_NAME, null)
            .build()
        ops += ContentProviderOperation.newInsert(ContactsContract.Data.CONTENT_URI)
            .withValueBackReference(ContactsContract.Data.RAW_CONTACT_ID, 0)
            .withValue(ContactsContract.Data.MIMETYPE, ContactsContract.CommonDataKinds.StructuredName.CONTENT_ITEM_TYPE)
            .withValue(ContactsContract.CommonDataKinds.StructuredName.DISPLAY_NAME, displayName)
            .build()
        ops += ContentProviderOperation.newInsert(ContactsContract.Data.CONTENT_URI)
            .withValueBackReference(ContactsContract.Data.RAW_CONTACT_ID, 0)
            .withValue(ContactsContract.Data.MIMETYPE, ContactsContract.CommonDataKinds.Phone.CONTENT_ITEM_TYPE)
            .withValue(ContactsContract.CommonDataKinds.Phone.NUMBER, phone)
            .withValue(ContactsContract.CommonDataKinds.Phone.TYPE, ContactsContract.CommonDataKinds.Phone.TYPE_MOBILE)
            .build()

        runCatching { context.contentResolver.applyBatch(ContactsContract.AUTHORITY, ops) }
            .onSuccess {
                Toast.makeText(context, "Saved: $displayName", Toast.LENGTH_SHORT).show()
                Base44Sender.sendContactSaveStatus(
                    context, phone, displayName, carModel, whatsappName, "saved", "created"
                )
            }
            .onFailure {
                Toast.makeText(context, "Contact save failed.", Toast.LENGTH_SHORT).show()
                Base44Sender.sendContactSaveStatus(
                    context, phone, displayName, carModel, whatsappName, "failed", it.javaClass.simpleName
                )
            }
    }

    private fun contactExists(context: Context, phone: String): Boolean {
        val uri = Uri.withAppendedPath(ContactsContract.PhoneLookup.CONTENT_FILTER_URI, Uri.encode(phone))
        context.contentResolver.query(uri, arrayOf(ContactsContract.PhoneLookup._ID), null, null, null)?.use {
            return it.moveToFirst()
        }
        return false
    }

    private fun clean(value: String): String =
        value.replace(Regex("[\\n\\r\\t]"), " ")
            .replace(Regex("[^\\p{L}\\p{N} .&'()+/-]"), "")
            .replace(Regex("\\s+"), " ")
            .trim()
}
