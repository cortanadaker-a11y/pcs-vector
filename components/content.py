"""Shared marketing and product copy for PCS Vector."""

from services.installation_data import SUPPORTED_INSTALLATIONS

INSTALLATION_COUNT = len(SUPPORTED_INSTALLATIONS)

HERO = {
    "kicker": "Your PCS. Your family. One clear plan.",
    "headline": "Stop guessing your PCS — get a plan your whole family can follow",
    "subheadline": (
        "PCS Vector turns your real inputs into a personalized strategic plan: where to live, "
        "how to protect spouse income, which schools work, and what to tackle in the first "
        "30 days — written like advice from a senior NCO who's done this move."
    ),
    "outcome_line": (
        "Built for E-5 through W-3 families · 6–8 minute intake · Plan in your inbox tonight"
    ),
}

AUDIENCE_STRIP = (
    "For Soldiers and families juggling spouse careers, school zones, BAH math, and a hard report date — "
    "not another generic checklist."
)

TRUST_SIGNALS = {
    "banner": "Built For Soldiers; By Soldiers",
    "badges": [
        "By Soldiers, for families",
        "22 CONUS installations",
        "Secure Stripe checkout",
        "PDF emailed to you",
        "Minutes, not weeks of research",
    ],
}

MOTIVATION_RALLY = {
    "headline": "You already carry the mission. Your family shouldn't carry the chaos.",
    "body": (
        "Every PCS asks the same hard questions — and they all hit at once. "
        "Where do we live? Can my spouse work? Are the kids in the right schools? "
        "Do we have the cash to bridge the gap? PCS Vector answers them in one plan "
        "you and your spouse can execute together."
    ),
    "punch": "This isn't more research. It's the plan you wish you had last PCS.",
}

MOTIVATION_CLOSE = {
    "headline": "Your next PCS doesn't have to feel like another deployment for your family.",
    "body": (
        "Six to eight minutes of inputs. One clear strategic plan. "
        "Share it with your spouse tonight and start making decisions tomorrow."
    ),
}

CTA = {
    "primary": "Build My Family's PCS Plan",
    "hero": "Build My Family's PCS Plan →",
    "mid": "I'm Ready — Build My Plan →",
    "caption": "One-time payment · 6–8 minute form · Plan in your inbox minutes later",
    "form_pay_reassurance": (
        "You'll review everything on the next screen, then pay once through Stripe. "
        "No subscription. Your report generates immediately after payment."
    ),
}

PAIN_POINTS = [
    {
        "title": "The lease you sign in week one",
        "desc": "Wrong school zone or a commute that kills spouse interviews can cost thousands before you course-correct.",
    },
    {
        "title": "The income gap nobody budgets for",
        "desc": "Spouse licensure, childcare waitlists, and deposit timing stack up fast — generic checklists never connect them to your actual timeline.",
    },
    {
        "title": "The timeline that won't wait",
        "desc": "Report date, hiring windows, and school registration deadlines don't care that you're still in Facebook research mode.",
    },
]

OUTCOME_BENEFITS = [
    {
        "title": "Lead the move — don't chase it",
        "desc": (
            "Get a firm recommendation, ranked backups, and the one dependency that "
            "breaks the plan if you ignore it. No more decision paralysis."
        ),
        "icon": "→",
    },
    {
        "title": "Move as a family unit",
        "desc": (
            "Spouse career, school zoning, and childcare land in one PDF you can "
            "hand your partner and say: this is our plan."
        ),
        "icon": "→",
    },
    {
        "title": "Know the dollars and the deadlines",
        "desc": (
            "2026 BAH math, DITY/PPM estimates, cash-flow pressure, and installation-specific "
            "gotchas — the stuff that actually moves your bottom line."
        ),
        "icon": "→",
    },
]

DIY_VS_VECTOR = [
    {"label": "Facebook groups & Reddit threads", "diy": "Hours of conflicting opinions", "vector": "One synthesized plan for your family"},
    {"label": "Generic PCS checklists", "diy": "Tasks without dependencies", "vector": "Decision gates and timed action phases"},
    {"label": "Housing sites alone", "diy": "Rent vs BAH once", "vector": "6-month surplus, utilities, and school-zone tradeoffs"},
    {"label": "Spouse job boards", "diy": "Apply and hope", "vector": "Licensure timeline, fast-tracks, and military spouse leverage"},
]

WHY_25 = {
    "headline": "Why $25 beats another week of spinning your wheels",
    "intro": (
        "A PCS shapes your housing budget, spouse's career, kids' schools, and cash flow "
        "for 2–3 years. One wrong lease or missed hiring window costs more than this report — "
        "and the stress tax on your family is the part you can't invoice."
    ),
    "points": [
        {
            "title": "Reclaim your evenings",
            "desc": "Stop losing 10–20 hours to tabs, threads, and half-answers. Answer a focused form and get a plan built for your family in minutes.",
        },
        {
            "title": "Avoid the expensive defaults",
            "desc": "Wrong school district, bad DITY choice, spouse income gap without a cushion — the report names these before you sign anything.",
        },
        {
            "title": "Show up ready",
            "desc": "Walk into your PCS with a spouse-readable plan, commander brief line, and ranked next steps — not anxiety and open browser tabs.",
        },
    ],
    "roi_line": (
        "If this plan prevents one housing mistake or gets your spouse earning one week sooner, "
        "it paid for itself many times over."
    ),
}

REPORT_SECTIONS = [
    {
        "num": 1,
        "title": "Executive Summary & Recommended Strategy",
        "desc": "Primary recommendation, ranked alternatives, and the single dependency that breaks the plan.",
    },
    {
        "num": 2,
        "title": "Spouse Career & Childcare Plan",
        "desc": "Licensure timelines, fast-track paths, military spouse programs, and childcare bottlenecks.",
    },
    {
        "num": 3,
        "title": "Housing Strategy & Cost Tradeoffs",
        "desc": "On-post vs off-post table with BAH surplus math and negotiation leverage.",
    },
    {
        "num": 4,
        "title": "Financial Opportunities & DITY/PPM",
        "desc": "Clear move math, recommended mode, and 30-day cash-flow pressure.",
    },
    {
        "num": 5,
        "title": "First 30 Days Action Plan",
        "desc": "Phased Soldier and Spouse tasks with clear decision gates — not a generic checklist.",
    },
    {
        "num": 6,
        "title": "Schools, Pets & Logistics",
        "desc": "Enrollment deadlines, zoning traps, and walk-away red flags before you sign a lease.",
    },
    {
        "num": 7,
        "title": "Timeline & Key Decisions",
        "desc": "Hard triggers, risk scenarios, and a ready-to-use commander conversation line.",
    },
    {
        "num": 8,
        "title": "Prioritized Next Steps",
        "desc": "6–8 time-bound actions ranked by impact — start this week.",
    },
]

HOW_IT_WORKS_STEPS = [
    {"num": "1", "title": "Tell us your PCS", "desc": "6–8 min form · family, priorities, installations"},
    {"num": "2", "title": "Secure checkout", "desc": "One-time $25 · Stripe · no subscription"},
    {"num": "3", "title": "Get your plan", "desc": "Personalized 8-section strategic report"},
    {"num": "4", "title": "Execute together", "desc": "PDF emailed · share with your spouse"},
]

REPORT_HIGHLIGHTS = [
    "“I'd lock off-post in Hope Mills before you arrive — $644 BAH surplus and Cumberland County school access.”",
    "“Run partial DITY here: about $2,179 net on 7,000 lbs — less risk than a full truck with kids and pets.”",
    "“Your spouse should hit the substitute pool while lateral-entry clears — a four-week licensure delay costs $3,600.”",
    "“If childcare isn't locked by day 21, the employment timeline slips — get DD 2606 in day one.”",
]

SPOUSE_SHARE_TEASE = (
    "Every report ends with a spouse-share line you can forward as-is — "
    "so you're both working the same plan, not re-explaining it at the kitchen table."
)

REPORT_PREVIEW = {
    "headline": "Preview your report before you pay",
    "subhead": (
        "Every plan follows this eight-section structure — written for your family, "
        "your installation, and your priorities. Here's what the finished product looks like."
    ),
    "sample_meta": "Sample · E-5 family · Fort Riley → Fort Campbell · minimizing total costs",
    "blur_note": "Your report uses your actual BAH, zip codes, spouse career field, and move window.",
    "visible_sections": [
        {
            "num": "1",
            "title": "Executive Summary & Recommended Strategy",
            "lines": [
                "Marcus, I'd lock off-post in Clarksville (37042) before you report — "
                "it hits your school-quality priority and keeps you under the $2,200 monthly cap.",
                "Hopkinsville is the backup if inventory tightens; on-post DODEA if zoning slips.",
                "The biggest risk is signing without written school-zone confirmation — "
                "miss that and you could be rezoning mid-year at your own expense.",
            ],
        },
        {
            "num": "3",
            "title": "Housing Strategy & Cost Tradeoffs",
            "lines": [],
            "table": [
                {"label": "On-post", "value": "$0 (BAH absorbed)", "note": "Shortest commute"},
                {"label": "Clarksville low", "value": "+$708/mo surplus", "note": "Verify zoning first"},
                {"label": "Clarksville high", "value": "+$308/mo surplus", "note": "Faster summer turnover"},
            ],
        },
        {
            "num": "5",
            "title": "First 30 Days Action Plan",
            "lines": [
                "Days 1–5 · Gate: If school zoning letters are requested by day 5 — "
                "otherwise you risk signing a lease that blocks enrollment.",
                "Days 6–15 · Gate: If lease includes written school-zone confirmation by day 15 — "
                "otherwise shift to on-post backup.",
            ],
        },
    ],
    "blurred_sections": [
        {"num": "2", "title": "Spouse Career & Childcare Plan"},
        {"num": "4", "title": "Financial Opportunities & DITY/PPM"},
        {"num": "6", "title": "Schools, Pets & Logistics Notes"},
        {"num": "7", "title": "Timeline & Key Decisions"},
        {"num": "8", "title": "Prioritized Next Steps"},
    ],
}

REPORT_GENERATION_STEPS = [
    {"id": "inputs", "label": "Reviewing your move details and priorities"},
    {"id": "housing", "label": "Analyzing housing, BAH, and local neighborhoods"},
    {"id": "spouse", "label": "Building spouse career and childcare recommendations"},
    {"id": "finance", "label": "Running cash-flow and DITY/PPM math"},
    {"id": "timeline", "label": "Drafting your 30-day action plan and decision gates"},
    {"id": "finalize", "label": "Polishing your executive summary and next steps"},
]

TESTIMONIAL = {
    "quote": (
        "We had orders to Bragg and no idea where to start. This wasn't another checklist — "
        "it told us what to decide first and what would go wrong if we waited. "
        "For the first time, my husband and I were on the same page before the movers showed up."
    ),
    "attribution": "Army spouse · E-6 family · Fort Bragg PCS",
}

PRICING_INCLUDES = [
    "Full 8-section personalized strategic plan",
    f"Local depth across {INSTALLATION_COUNT} major CONUS Army installations",
    "2026 BAH-aware housing and DITY math",
    "Professional PDF emailed automatically",
    "Generated in minutes after payment",
]

FAQ_ITEMS = [
    {
        "q": "What do I get for $25?",
        "a": "A personalized 8-section PCS strategic plan written in a direct, senior-advisor tone — "
        "not a generic checklist. You get clear recommendations, risk analysis, and time-bound next steps "
        "based on your family's inputs. View it in the app and receive a professional PDF by email. "
        "One report per purchase.",
    },
    {
        "q": "How is this different from free PCS resources?",
        "a": "Free groups and checklists give fragments — housing tips here, school rumors there. "
        "PCS Vector synthesizes your priorities, installation data, BAH math, and family situation into "
        "one decision-grade plan with dependencies, timelines, and explicit tradeoffs.",
    },
    {
        "q": "How long does the form take?",
        "a": "Most families finish in 6–8 minutes across three short sections. Your answers stay saved "
        "if you need a break before checkout.",
    },
    {
        "q": "When is my report generated?",
        "a": "Immediately after successful Stripe payment. You'll see a confirmation screen, then your "
        "report builds automatically — usually under a minute.",
    },
    {
        "q": "How do I get my PDF?",
        "a": "Enter your email in step 1. After payment, the PDF is **automatically emailed** to that "
        "address. You can also download it on the report page. Save your order reference (PCS-XXXXXXXX) "
        "and use **Retrieve Report** if you lose your tab.",
    },
    {
        "q": "Is my data stored or shared?",
        "a": "Form answers are used to generate your report and are not sold. Payment is processed "
        "securely by Stripe — we never see your card number.",
    },
    {
        "q": "Which installations are supported?",
        "a": f"PCS Vector includes tailored data for **{INSTALLATION_COUNT} major CONUS Army installations** "
        "(Fort Bragg, Fort Hood, Fort Bliss, Fort Campbell, JBLM, and more). Other CONUS locations receive "
        "strong general PCS guidance with BAH and move math where available.",
    },
    {
        "q": "Can I get a refund?",
        "a": "If something goes wrong with your report, contact support through the email on your "
        "Stripe receipt. We're committed to making it right.",
    },
]