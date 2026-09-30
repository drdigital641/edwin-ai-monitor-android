package sg.edwingarage.readonlybridge

object BridgeConfig {
    const val WHATSAPP_BUSINESS_PACKAGE = "com.whatsapp.w4b"
    const val BASE44_ROOT =
        "https://base44.app/api/apps/6ab7b2596dc4c4ccbd5c279e/functions"
    const val PAIR_URL = "$BASE44_ROOT/pair-device"
    const val RECEIVER_URL = "$BASE44_ROOT/receive-outgoing"
    const val CONTACT_SAVE_STATUS_URL = "$BASE44_ROOT/contact-save-status"
}
