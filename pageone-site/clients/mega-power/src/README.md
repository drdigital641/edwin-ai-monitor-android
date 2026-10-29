# Mega Power website mockup (preview)

Client: Mega Power Engineering & Trading (megapower.com.sg). Brief: drdigital641/edwin-ai-context `handoffs/2026-10-29-mega-power-website-mockup.md`.
Built 29 Oct 2026. Preview: https://pageonesingapore.com/preview/mega-power/ (hidden from Google by the parent `preview/.htaccess` header; pages carry no noindex).
Live megapower.com.sg was NOT touched.

## Build
`python3 build.py OUT_DIR` (sources here: build.py, mp.css, mp.js, staff.js, staff.css, assets/). Repo copy: edwin-ai-monitor-android `pageone-site/clients/mega-power/` (site/ + src/), branch `claude/project-thread-vxgyxh`. Upload = Bridge `sync_from_github` site=pageone, base_path=preview/mega-power, source_path=pageone-site/clients/mega-power/site.

## Facts used (public pages read 29 Oct 2026, nothing else)
- Name: Mega Power Engineering & Trading. Since 1989. Workshops and garages across Singapore; passenger, commercial, excavators, trucks.
- Main line +65 6842 3389, enquiry@megapower.com.sg.
- Branches (contact page): Ang Mo Kio 5025 AMK Ind Park 2 #01-55/57 S569528 (6482 3389), Toh Guan 21 Toh Guan Rd East #01-33 S608609 (6766 3389), Kaki Bukit 13 Kaki Bukit Rd 4 #01-27 S417807 (6385 3389), Soon Lee 5 Soon Lee St #01-26 S627607 (6252 3389). Contact page map points to 39 Genting Road (not a listed branch): ask owner.
- 13 public listings with attributes copied verbatim (country, refrigerant, oil, OEM no.). Old site shows "In stock" on all; mockup hides stock (needs owner approval).
- Product photos and logo are hotlinked from megapower.com.sg (container can't download them); placeholders show if the old site blocks them. Porsche photo file is named "comp_sample" (check).
- Not used: YUKI brand, "leading supplier" claim, brand logos (no distributor claims), Pte Ltd name.

## How the demo works
- Search: client-side, data.js + staff changes in localStorage (`mp_*_v1`). Exact ref / match / possible labels; unknown chassis codes (W210) fail instead of guessing.
- Leads, RFQ list, staff products, audit log all live in the viewer's browser only. No email/WhatsApp sent.
- Product/category URLs = old Magento URLs. htaccess.txt holds the go-live 301s for other old paths.
- chat.js = mascot + assistant (rule-based intents, catalogue search via window.MP, leads tagged CHAT_*; sessionStorage mp_chat/mp_bub). Not a live AI.
- wa.js = tracking/wa-tap-counter.js v2 with site 'mega-power' (inactive on pageonesingapore.com; no wa.me links until a WhatsApp number is confirmed; needs a Controller Client row at go-live).

## Open (owner)
See staff dashboard > Settings & approvals (12 items from the brief) + Magento admin access for the full export.
