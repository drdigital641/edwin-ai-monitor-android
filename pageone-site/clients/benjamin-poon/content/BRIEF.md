# Content brief: Benjamin Poon (潘国雄) website, EN + Simplified Chinese

You write ONE Python content module for a static site generator. The lead (build.py) renders it. Read this whole brief first,
then the client spec at /mnt/project-files/benjamin-poon/HANDOVER-from-client.md (sections 2, 4, 5, 9, 10 matter most).

## Who he is (only these facts are confirmed)
- Benjamin Poon (潘国雄). Mobile/WhatsApp +65 8932 9933. Email benpoon.nirvana@gmail.com.
- Represents Nirvana Singapore (富貴山庄). nirvana.com.sg is the COMPANY's official site, not his. He is NOT the owner/operator of Nirvana or any temple.
- Title per his badge (22 Oct 2026): 生命经理师 Life Managing Director 2025, Service Advisor (NVG Authorised Agency). Earlier note: "life planning professional" (his exact English title is pending).
- Services he discusses: columbarium niches (福位 / 骨灰位), ancestral tablets (神主牌), funeral services (殡葬服务), will planning (遗嘱规划) as a Certified Will Planner with Advance Planners (exact credential wording PENDING).
- Award images (shown on the site by the lead) say: "APG / Advance Planners, Authorised Agency of 富貴 Nirvana"; APG Sep 2025 Award; APG October 2025 Sales Award awardee; APG May 2026 Sales Award awardee (May 2026 image names 富貴山莊生命紀念館 CCK and 靈山寺 LIN SAN TEMPLE). NEVER mention any dollar amount or "$50K"/"Elite Club".
- Joined around late 2025. Do not state years of experience, number of families served, ratings, testimonials.
- Three venues: Nirvana Memorial Garden 富贵山庄 (950 Old Choa Chu Kang Road, Singapore 699816); Lin San Temple 灵山寺 (27 Lorong 12 Geylang, Singapore 399004); Thian Leng Chong Toh Tong 天灵总道堂 (472 Changi Road, Singapore 419890; exact name/characters PENDING).

## Hard rules
1. Original wording. Never copy from nirvana.com.sg, linsan.sg or other sites. You may web-search/fetch to VERIFY a fact; record the URL in `SOURCES`.
2. No prices, packages, availability, tenure (freehold/leasehold/lease years), opening/viewing hours, promotions, refund policies, guarantees, "best/No.1/cheapest", scarcity or urgency. If useful to mention, say "Benjamin will share current options and prices from the operator" and add a PENDING item.
3. Public transport / directions only if you verified them on an official or clearly reliable source today (record it). Otherwise say "Benjamin can share directions and arrange a viewing".
4. Never imply this site is the official site of Nirvana, Lin San Temple, Thian Leng or Advance Planners. Link to official sites as "official website" when useful (absolute https URLs).
5. Tone: calm, respectful, plain, never alarmist; short paragraphs (2-3 sentences); readers include seniors. No medical or bereavement targeting. Will pages: general information only, not legal advice; complex cases go to a lawyer.
6. Chinese is natural Simplified Chinese as written in Singapore (福位、骨灰位、骨灰塔、神主牌、殡葬、遗嘱、预先规划、巴士/地铁), NOT a literal translation. Same meaning as the English, same facts.
7. Every unverified or client-dependent point goes in that item's `pending` list (bilingual) instead of being guessed.
8. Answer-first: `answer` is a 40-60 word direct answer to the page's main question (EN); ZH equivalent ~80-120 characters.
9. Titles: EN ≤ 60 chars, ZH ≤ 30 chars, main term first, end with "| Benjamin Poon" / "| 潘国雄" when it fits. Descriptions: EN ≤ 155 chars, ZH ≤ 78 chars. No "guaranteed".
10. Singapore official figures (law, procedures) only from official sources (sso.agc.gov.sg, mylegacy.life.gov.sg, ica.gov.sg, nea.gov.sg, publictrustee / mlaw.gov.sg), each with link in the text or SOURCES and checked date 22 Oct 2026.

## Python format (exact)
```python
# -*- coding: utf-8 -*-
def T(en, zh):
    return {'en': en, 'zh': zh}

ITEMS = [   # name the list as told in your task (SERVICES / LOCATIONS / GUIDES)
    {
        'slug': 'columbarium-niches',
        'card': T('Columbarium niches', '福位 / 骨灰位'),            # ≤ 4 words
        'card_text': T('One or two plain sentences for a card.', '...'),
        'title': T('...', '...'),
        'desc': T('...', '...'),
        'h1': T('...', '...'),
        'lede': T('One sentence under the H1.', '...'),
        'answer': T('40-60 word direct answer.', '...'),
        'sections': [
            {'h': T('Question-style heading', '...'),
             'p': [T('Paragraph. May contain <strong>bold</strong> and <a href="services/ancestral-tablets/">relative links</a>.', '...')],
             'list': [T('bullet', '...')],        # optional
             'ol': True,                           # optional: numbered list instead of bullets
             'table': {'head': [T('', ''), ...], 'rows': [[T('', ''), ...], ...]},   # optional, for comparisons
            },
        ],
        'faqs': [(T('Question?', '问题？'), T('Answer 1-3 sentences.', '回答。')), ...],   # 4-6, real search-style questions
        'wa': T('Hello Benjamin, I found your <page> page and would like to ...', '您好 Benjamin，我在您的网站<页面>看到…，想了解…'),
        'related': ['services/ancestral-tablets/', 'locations/lin-san-temple/', 'guides/<slug>/'],   # 2-4 internal paths
        'pending': [T('What must be confirmed by Benjamin', '需由 Benjamin 确认的事项')],
        'photo': None,
    },
]
SOURCES = [('https://...', 'what it verified', 'checked 22 Oct 2026')]
```
- Relative links inside text: paths WITHOUT leading slash and WITHOUT 'zh/' (the renderer prefixes the right language). Valid targets:
  `services/`, `services/columbarium-niches/`, `services/ancestral-tablets/`, `services/funeral-services/`, `services/will-planning/`,
  `locations/`, `locations/nirvana-memorial-garden/`, `locations/lin-san-temple/`, `locations/thian-leng-temple/`,
  `guides/`, guide slugs listed in your task, `about-benjamin-poon/`, `contact/`.
- No other HTML than <strong>, <a>, <em>. Escape nothing else; use plain apostrophes and quotes inside Python strings correctly.
- 4-7 sections per page, total ~700-1100 English words per page (guides ~800-1200). Equivalent Chinese.
- The file must import cleanly: run `python3 -I -c "import importlib.util,sys; s=importlib.util.spec_from_file_location('m','<yourfile>'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(len(m.<LIST>))"` and fix errors before finishing.

## Guide slugs (fixed list, for cross-links)
- guides/columbarium-niche-vs-ancestral-tablet/
- guides/questions-before-choosing-a-columbarium-niche/
- guides/arranging-a-columbarium-viewing/
- guides/pre-planning-vs-immediate-funeral-arrangements/
- guides/what-to-do-when-a-loved-one-passes-away-singapore/
- guides/will-planning-basics-singapore/
- guides/preparing-for-a-memorial-planning-consultation/
