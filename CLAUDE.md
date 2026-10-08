# Edwin's website architecture (permanent rules)

Owner: Edwin, who owns the Bluehost cPanel account `sgmodde1`.

## The five websites (all on `sgmodde1`)

| Bridge key | Domain                 | Name                 |
|------------|------------------------|----------------------|
| `sggarage` | sggarage.com           | SG Garage            |
| `cleanic`  | cleanicdetailing.com   | Cleanic Detailing    |
| `alicia`   | aliciaongproperty.com  | Alicia Ong Property  |
| `danny`    | dannychuafinancial.com | Danny Chua Financial |
| `sofacare` | sofacaresg.com         | SofaCare SG          |

## How every website change is made

Claude → Base44 → Bluehost Bridge → Bluehost server (`sgmodde1`) → live website.

- Use the **bluehost-bridge** connector (`https://blue-bridge-pilot.base44.app/api/mcp`)
  to list, read, edit, write and restore site files. Changes go live straight away.
- The bridge is the Base44 app **Bluehost Bridge** (app id `6ac6d47b4ec84148578914c7`).
  Change the bridge itself through the Base44 connector.
- Every write is backed up first and logged (`BridgeLog`). Use the restore tool to roll back.
- The bridge blocks secrets (`wp-config.php`, `.env`, keys), `.htaccess` and server-side
  code (`.php` etc.). Don't try to work around this; tell Edwin when a change needs one of those.
- If the bluehost-bridge connector isn't loaded in a session, say so. Don't switch to
  another way of changing the live sites.
