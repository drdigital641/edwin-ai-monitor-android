# -*- coding: utf-8 -*-
"""SEO/AEO additions (2 Nov 2026): hub intros, extra paragraphs and FAQs for hub/thin pages.
Built ONLY from facts already on this site (services.py, locations.py, guides_*.py, README, llms.txt). No prices, no new claims."""


def T(en, zh):
    return {'en': en, 'zh': zh}


EXTRA = {
    'about-benjamin-poon/': {
        'more': [
            T("Families usually contact Benjamin because they want to understand their options before they need them, or because a loss has just happened and they need calm, plain guidance. He explains the options that suit the situation, shares current options and prices from the operator on request, and can arrange a visit to the venue so the family sees the place in person.",
              "家属联系 Benjamin，通常是想在需要之前先了解各种选择，或是刚刚经历丧亲、需要平和而清楚的指引。他会说明适合情况的选择，应要求向营运单位索取最新的选择和价格告知，也可以安排参观，让家人亲自到现场看看。"),
            T("This website is Benjamin's own. Its guides draw on Nirvana Memorial Garden's 2025 booklet and on official Singapore sources such as NEA, ICA and the Singapore Statutes Online, and each guide shows its updated date. You can read everything in English or in Simplified Chinese.",
              "本网站为 Benjamin 个人所有。指南内容参考富贵山庄 2025 年手册，以及 NEA、ICA 和新加坡法规网站等官方来源，每篇指南都标明更新日期。全站提供英文和简体中文两种语言。"),
        ],
        'faqs': [
            (T("Who is Benjamin Poon?", "潘国雄（Benjamin Poon）是谁？"),
             T("Benjamin Poon (潘国雄) is a Service Advisor and Life Managing Director in Singapore who represents Nirvana Singapore (富贵山庄). He helps families with columbarium niches, ancestral tablets, funeral arrangements and will planning.",
               "潘国雄（Benjamin Poon）是新加坡的生命经理师，代表富贵山庄（Nirvana Singapore），协助家庭了解福位、神主牌、殡葬安排与遗嘱规划。")),
            (T("Which languages does Benjamin speak?", "Benjamin 会说哪些语言？"),
             T("English and Mandarin, with fluent Cantonese and Hokkien. He also understands some Teochew.",
               "华语和英语，广东话、福建话流利，也略懂潮州话。")),
            (T("Is this the official website of Nirvana?", "这是富贵山庄的官方网站吗？"),
             T("No. This is Benjamin Poon's personal professional website. It is not the official website of Nirvana Singapore, Lin San Temple, Thian Leng Chong Toh Tong or Advance Planners.",
               "不是。这是潘国雄的个人专业网站，并非富贵山庄、灵山寺、天灵总道堂或 Advance Planners 的官方网站。")),
        ],
    },
    'services/': {
        'faqs': [
            (T("What does Benjamin Poon help with?", "潘国雄可以协助哪些事项？"),
             T("Four areas: columbarium niches, ancestral tablets, funeral services and will planning. For will planning he works with Advance Planners as a certified will planner.",
               "四个方面：福位 / 骨灰位、神主牌、殡葬服务和遗嘱规划。遗嘱规划方面，他以认证遗嘱规划师身份与 Advance Planners 合作。")),
            (T("Does this website show prices?", "网站上有列出价格吗？"),
             T("No. Prices depend on the arrangement, so none are published here. Benjamin shares current options and prices from the operator when you ask him on WhatsApp.",
               "没有。价格视安排而定，网站不公布价格。您通过 WhatsApp 询问时，Benjamin 会向营运单位索取最新的选择和价格告知。")),
            (T("Is the first conversation an obligation?", "第一次咨询需要承诺什么吗？"),
             T("No. A first conversation is simple and has no obligation. You do not need to share personal or medical details, and you can take the time you need to discuss with your family.",
               "不需要。第一次交谈很简单，也没有任何约束。不需要提供个人或健康方面的详情，您可以和家人慢慢商量。")),
        ],
    },
    'locations/': {
        'faqs': [
            (T("Which venues can Benjamin help with?", "Benjamin 协助哪些地点？"),
             T("Three venues: Nirvana Memorial Garden at 950 Old Choa Chu Kang Road, Lin San Temple (灵山寺) at 27 Lorong 12 Geylang, and Thian Leng Chong Toh Tong (天灵总道堂) at 472 Changi Road.",
               "三个地点：旧蔡厝港路 950 号的富贵山庄、芽笼 12 巷 27 号的灵山寺，以及樟宜路 472 号的天灵总道堂。")),
            (T("Can I visit a venue before deciding?", "决定之前可以先参观吗？"),
             T("Yes. If you wish, Benjamin can arrange a visit so the family can see the place in person before deciding.",
               "可以。如果您愿意，Benjamin 可以安排参观，让家人在决定之前亲自到现场看看。")),
            (T("Are these venue pages official?", "这些地点页面是官方页面吗？"),
             T("No. They are general information from Benjamin Poon's personal website. For official details, use each venue's own website or ask Benjamin to check for you.",
               "不是。这些是潘国雄个人网站提供的一般资讯。官方详情请参考各地点自己的网站，或请 Benjamin 为您查证。")),
        ],
    },
    'guides/': {
        'intro': [
            T("These guides answer the questions families ask most often when they plan a columbarium niche, an ancestral tablet, a funeral or a will in Singapore. They cover choosing between a niche and a tablet, private memorial parks compared with government columbaria, how Nirvana Memorial Garden's maintenance fee and trust fund work, festival visits, how to get to the venues, what to do when a loved one passes away, and the basics of will planning.",
              "这些指南解答家庭在新加坡规划福位、神主牌、殡葬或遗嘱时最常问的问题，内容包括福位与神主牌如何选择、私人纪念园与政府骨灰堂的比较、富贵山庄维护费与信托基金如何运作、节日探访、前往各地点的交通、亲人离世后该怎么办，以及遗嘱规划的基础知识。"),
            T("Benjamin Poon (潘国雄) writes them in plain language from Nirvana Memorial Garden's 2025 booklet and from official sources such as NEA, ICA and Singapore Statutes Online. Each guide shows who wrote it and when it was last updated. The guides give general information, not legal advice. Every guide is also available in Simplified Chinese.",
              "这些指南由潘国雄用浅白的语言撰写，参考富贵山庄 2025 年手册，以及 NEA、ICA 和新加坡法规网站等官方来源。每篇指南都标明作者和最近更新日期。内容属一般资讯，并非法律意见。每篇指南都有简体中文版本。"),
        ],
        'faqs': [
            (T("Who writes these guides?", "这些指南由谁撰写？"),
             T("Benjamin Poon (潘国雄), a Service Advisor and Life Managing Director who represents Nirvana Singapore. Each guide shows his name and the date it was last updated.",
               "由代表富贵山庄的生命经理师潘国雄撰写。每篇指南都标明他的名字和最近更新日期。")),
            (T("Are the guides legal advice?", "指南属于法律意见吗？"),
             T("No. They give general information. Questions that need legal advice, such as complex wills or estates, should go to a qualified lawyer.",
               "不是。指南提供一般资讯。需要法律意见的问题，例如复杂的遗嘱或遗产事宜，请咨询合格律师。")),
            (T("Are the guides available in Chinese?", "指南有中文版本吗？"),
             T("Yes. Every guide has a Simplified Chinese version under the 中文 link at the top of the page.",
               "有。每篇指南都有简体中文版本，点击页面顶部的「中文」链接即可。")),
        ],
    },
    'contact/': {
        'more': [
            T("The fastest way to reach Benjamin Poon is WhatsApp on +65 8932 9933. You can also call the same number or email benpoon.nirvana@gmail.com. He replies in English, Mandarin, Cantonese or Hokkien, and you do not need to share personal or medical details in your first message.",
              "联系潘国雄最快的方式是 WhatsApp +65 8932 9933。您也可以致电同一号码，或电邮 benpoon.nirvana@gmail.com。他可以用华语、英语、广东话或福建话回复，第一条讯息不需要提供个人或健康方面的详情。"),
        ],
        'faqs': [
            (T("What is the fastest way to contact Benjamin?", "联系 Benjamin 最快的方式是什么？"),
             T("WhatsApp on +65 8932 9933. Send a short message with the topic you have in mind and he will reply.",
               "WhatsApp +65 8932 9933。发一条简短讯息说明您想了解的主题，他会回复您。")),
            (T("Which languages can I use?", "可以使用哪些语言？"),
             T("English, Mandarin, Cantonese or Hokkien. He also understands some Teochew.", "华语、英语、广东话或福建话，他也略懂潮州话。")),
            (T("Do I need to share personal details first?", "需要先提供个人资料吗？"),
             T("No. You do not need to share personal or medical details to start. Tell him the topic and he will ask a few plain questions from there.",
               "不需要。开始时不必提供个人或健康方面的详情，只要说明主题，他会再问几个简单的问题。")),
        ],
    },
}
