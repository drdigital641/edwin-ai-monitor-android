# Edwin AI Monitor v2.1 — final review notes

This repository is the APK source for Edwin Garage's read-only WhatsApp Business monitor.

## Integration contract

- WhatsApp package: `com.whatsapp.w4b`
- Base44 monitor app: `6ab7b2596dc4c4ccbd5c279e`
- Pair endpoint: `/functions/pair-device`
- Raw outgoing endpoint: `/functions/receive-outgoing`
- Reader version emitted by this build: `2.1-exact-bubble-time`

## Timestamp safety rule

`observed_at_ms` is scanner observation time only. It must never be represented as the WhatsApp sent time.

A normalized WhatsApp timestamp is allowed only when all of these hold:

1. Edwin tapped Send recently.
2. The same contact is still open.
3. The rendered right-side bubble text matches the remembered outgoing draft after whitespace normalization.
4. Exactly one clock can be read from that smallest bubble/container.
5. The clock parses to a plausible WhatsApp time.

Only then does the APK emit:

- `timestamp_confidence = exact_same_bubble`
- `timestamp_provenance = exact_same_bubble_clock`
- `direction_confidence = right_side_exact_bubble`

Historical/right-side sensor observations may still be uploaded for diagnostics, but their timestamp provenance is explicitly untrusted and Base44 must fail closed.

## Known bad evidence that must stay filtered

Do not treat accessibility chrome as Edwin text, including reaction labels, delivery/read labels, photo/gallery controls, media-count labels, voice-message descriptions, colour/editor controls, dashboard labels, profile labels, and other WhatsApp UI controls.

AI-tagged bubbles containing `-Replied by AI` are not manual Edwin messages.

## Clean reinstall behavior

A clean Android reinstall generates a new local device id and has no prior device token. Pair again in the app. The Base44 pairing backend is configured to retire older enabled monitor-device tokens after a successful new-device pairing.

## Review acceptance checks

1. Project compiles with Java 17 / Android 35 workflow.
2. No send-click/device time is copied into `whatsapp_time`.
3. No observation time fallback exists for authoritative sent time.
4. Same-bubble trust is only granted to a recent exact draft/contact match.
5. Raw evidence remains auditable even when normalized timestamp is rejected.
6. Network failure releases the dedupe reservation; successful upload acknowledges it.
7. Accessibility service remains scoped to WhatsApp Business and does not click/type/send messages.
8. Pairing and receiver URLs continue to target monitor app `6ab7b2596dc4c4ccbd5c279e`.
