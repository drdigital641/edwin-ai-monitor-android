# Cheap translation step (Rule 6): content_en.json -> content_{LANG}.json

Input: /tmp/claude-0/sh/src/content_en.json (English, final). Output: /tmp/claude-0/sh/src/content_{LANG}.json with EXACTLY the same JSON structure and keys (same list lengths, same order). Translate every string VALUE. Never change keys.
- LANG=ms: Bahasa Malaysia (Malaysian Malay, NOT Indonesian: use "kereta", "bengkel", "servis", "telefon", "percuma" style Malaysian words; "anda"). 
- LANG=zh: Simplified Chinese (简体中文), natural Malaysian Chinese usage (e.g. 士古来 for Skudai, 新山 for Johor Bahru, 柔佛 for Johor).

Keep exactly as written (do not translate): brand and model names (BMW, Mercedes-Benz, Porsche, Volkswagen, VW, MINI, Mini Cooper S, Peugeot 308, Toyota Alphard, Vios NCP150, Camry ACV30, Altis, Lexus GS300 (GRS190), Honda CR-V, Honda Shuttle 2015, Honda Civic, Nissan Navara, Hyundai Sonata, Ford Raptor, Ford Focus, VW Golf, VW Beetle, VW Passat, B48, K114, Koyo, P2583, P0016, SCN, DCC, AIRMATIC, W205, C200, C250, Macan S, Cayenne, Panamera, X5/X6, ADAS, ECU, CVT, LCD, OEM, AhaPay, AutoSEO.my, Google, Facebook, WhatsApp), the business names "Sheng Heng Auto Service Centre" / "Sheng Heng" / "Sheng Heng Auto Service (M) Sdn Bhd", SSM numbers, addresses (17, Jalan Hang Lekir 12, Taman Industri Jaya, 81300 Skudai, Johor; all road names like Jalan Indah, AEON Bukit Indah, Lebuhraya Skudai), place names in Latin script (in zh you may add the common Chinese name in brackets once if well known, e.g. 士古来 (Skudai); otherwise keep the Malay name), phone numbers, numbers and km, "Make The Quality" (their slogan, keep English), "Mr. Yaw", and anything inside double quotes that is a customer's review quote (keep the English quote verbatim, you may add nothing).
- "credit": keep "Website by AutoSEO.my" EXACTLY (English) in all languages.
- "legal": keep exactly.
- "review_tags": keep exactly.
- "chips", "makes" style lists: translate service words, keep brand names.
- In titles: keep under 60 characters, and START the home and service titles with the keyword below. H1 must contain the keyword. Meta: one sentence with a WhatsApp CTA.
- No em dashes or en dashes; use commas/colons. No exclamation marks. Do not add facts, prices, promises or claims that are not in the English. Never write the words: terbaik, 最好, 最佳, jaminan, 保证, waranti, 保修, 授权, sah/authorised dealer, Korea/韩.
- WhatsApp prefills ("wa", "wa_home", ...) start "Hai Sheng Heng," (ms) / "你好 Sheng Heng，" (zh).

Keywords (title starts with it; H1 contains it):
| key | ms | zh |
| pages.home | bengkel kereta Skudai | 士古来修车厂 |
| continental-car-specialist-skudai | pakar kereta continental Skudai | 士古来 欧洲车维修 |
| adas-calibration-skudai | kalibrasi ADAS Johor (Skudai) | 新山 ADAS 校准 |
| ecu-repair-programming-skudai | baiki ECU Skudai | 士古来 ECU 维修 编程 |
| car-key-immobilizer-skudai | buat kunci kereta Skudai | 士古来 汽车钥匙 配置 |
| car-coding-instrument-cluster-skudai | coding kereta Skudai (baiki meter) | 新山 汽车仪表 维修 编码 |
| gearbox-overhaul-skudai | overhaul gearbox Skudai | 士古来 变速箱 大修 |
| car-diagnostic-skudai | diagnostik kereta Skudai | 士古来 电脑诊断 故障灯 |
| car-service-skudai | servis kereta Skudai | 士古来 汽车保养 |
Area pages: ms "Bengkel kereta berhampiran <area>", zh "<area中文或原名> 附近修车厂".

Write with python (json.dump(..., ensure_ascii=False, indent=1)). Then verify: a script that walks both JSONs and asserts identical key structure and list lengths; and grep the output for — – terbaik 最好 最佳 jaminan 保证 waranti 保修 授权 Korea 韩. Fix any hit. Work in chunks if the file is large (translate section by section: ui, home, img, services, areas, pages), but the final file must be complete. Reply only "done" plus anything you were unsure about.
