# theecuclinicsg.com (2 Nov 2026)
| site | fix | status |
|---|---|---|
| theecuclinicsg.com | /articles/ hub: intro + 3 FAQs + FAQPage | done, live (edit_file, backup 20261102-090100-7ae13b), source branch claude/ecu-night-2-nov (2769f7643) + build.py edit, commit a23828180 |
| | 404.html: added links to ABS pump repair and Articles | done live (backup 20261102-090102-1eb6c8); not mirrored in build.py (live 404 differs from build) |
| | /services/ hub | skipped: the site has no /services/ index page (services are a section on home + 9 pages); creating a new page was out of scope |
| | Sync excludes | no whole-site sync run; ecu.js, icons and the live-only article files were never touched |
| | Thin articles, sitemap/llms | skipped |

## Continuation (2 Nov 2026, second helper)
| item | status |
|---|---|
| Organization JSON-LD | AutoRepair @id #business, logo icon-512, sameAs = [Facebook TheECUclinicSG]. The GBP is known only by place id (reviews URLs), not a profile URL, so not added: "sameAs: Facebook only". No change. |
| Articles byline | all 27 live articles had "By The ECU Clinic - <date>"; label now "Last updated <date>" on all 27 (edit_file, live, 3 live-only files edited in place, no sync) + build.py. |
| Thin / no-FAQ articles | NOT expanded. 13 of 27 have no FAQ/FAQPage. Thin (<500 words): hybrid-battery-replacement-signs 333, toyota-voxy-noah-sienta-abs-pump 326, mercedes-steering-lock-elv-failure 352, mercedes-esp-control-unit-fault-n30-4 398, mercedes-7g-tronic-722-9-tcu-problems 408, honda-yaw-rate 417, mercedes-active-brake-assist 427, bmw-cas-elv-fault-codes 431, honda-vsa-solenoid 462, honda-radar-p2583 483. 10 thin left; 14 already 726-1056 words. |
| llms.txt | added "Last updated 2 November 2026." live + build.py. Sitemap already true (articles/ 2026-11-02, services untouched per memory). |
| 404 | live has ABS pump repair + Articles links (previous helper); now mirrored in build.py not_found(). |
| Repo | a9dfbea9c |

## Continuation 2 (2 Nov 2026, third helper)
| item | status |
|---|---|
| 10 thin articles | DONE for all 10 (these were also the ones lacking a visible FAQ): honda-yaw-rate, bmw-cas-elv-fault-codes, honda-vsa-solenoid, mercedes-esp-n30-4, honda-radar-p2583, mercedes-active-brake-assist, mercedes-steering-lock-elv-failure, hybrid-battery-replacement-signs, toyota-voxy-noah-sienta-abs-pump, mercedes-7g-tronic-722-9. Each has a "Short answer" direct answer (40-60 words), 4 FAQs (visible details = FAQPage JSON-LD, parsed OK) and extra sections from facts already in the article/memory only (6-month repair warranty, hybrid battery 1 year/100,000 km, hours, pick-up and delivery, ELV emulator sold). Body text grew from 147-310 words to about 520-650 words; shortest are hybrid-battery-replacement-signs and toyota-voxy (about 530). 700 was not reached on every page without padding. |
| Live | 9 via per-folder sync_from_github (commit fb097455f), backups 20261102-092517-fa0613, -092521-028cd6, -092526-97841a, -092530-5ee6c6, -092533-39ab26, -092537-b40eac, -092541-ec302d, -092546-0631c4, -092551-39f8ab. Live-only mercedes-7g-tronic-722-9: edited in place with invoke_edit_file (backup 20261102-092604-728579; it already had 2 FAQs + the Booster "Repair or replace" section, kept; added direct answer, 3 sections, 2 more FAQs + JSON-LD). Live sitemap: 10 article lastmods -> 2026-11-02 (backup 20261102-092616-dcf70e). ecu.js, icons and abs-warning-light-causes were not touched. |
| Mirrored | pages.py (incl. the 7g live-only text, so a later build keeps it, and updated_iso 2026-11-02 for the 10). Only the 9 article files were taken from the build into site/; the rest of repo site/ left as is. |
| Not done | Brief said 13 articles lack a FAQ; repo/live check found 10 without a visible FAQ (abs-warning-light-causes has FAQPage JSON-LD but pages.py has no faq field; left alone, Booster live-only). The other 3 of the 13 could not be identified. |
| Live probe (run 41418868108) | https://theecuclinicsg.com/articles/ 200, /no-such-page-xyz-123/ 404; http, www and https-www variants 301 -> https://theecuclinicsg.com/ (single hop). Preview header: /preview/ecu-clinic/ HTTP/2 200, x-robots-tag: noindex, nofollow. |
