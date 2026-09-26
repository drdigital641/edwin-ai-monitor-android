# Edwin AI Monitor Android

Read-only Android Accessibility bridge for Edwin Garage.

- Watches WhatsApp Business only (`com.whatsapp.w4b`).
- Reads visible Accessibility text only.
- Does not click, type or send messages.
- No Base44 credential or pairing code is stored in this repository.
- Pairs the phone with Base44 at runtime and stores the issued device token only on the phone.

Base44 app ID: `6ab7b2596dc4c4ccbd5c279e`

## Build

The included GitHub Actions workflow builds the debug APK on push to `main`.

After a successful run:
1. Open Actions.
2. Open `Build Android APK`.
3. Download `Edwin-AI-Monitor-APK`.
4. Extract `app-debug.apk`.
5. Install it on the Samsung phone.
6. Pair with Base44.
7. Enable Edwin AI Monitor under Android Accessibility.
