"""Shared marketing and product copy for PCS Vector."""

from services.installation_data import SUPPORTED_INSTALLATIONS

INSTALLATION_COUNT = len(SUPPORTED_INSTALLATIONS)

HERO = {
    "kicker": "Decision-grade PCS planning for Army families",
    "headline": "Make the PCS decisions that protect your family — before they get expensive",
    "subheadline": (
        "PCS Vector turns your family's situation into a clear strategic plan — "
        "housing, schools, spouse career, finances, and a sequenced 30-day action path — "
        "so you make better decisions faster, with less stress and fewer costly mistakes."
    ),
    "outcome_line": (
        "Save hours of research · Reduce move-day panic · Protect spouse income and school stability"
    ),
}

TRUST_SIGNALS = {
    "banner": "Built by a serving Army officer · Independent planning tool · Not affiliated with DoD",
    "badges": [
        "Serving Army officer–built",
        "Trusted by military families",
        "Secure Stripe checkout",
        "PDF emailed automatically",
        f"{INSTALLATION_COUNT} CONUS installations",
    ],
}

PAIN_POINTS = [
    {
        "title": "The lease you sign in week one",
        "desc": "Wrong school zone or a commute that kills spouse interviews can cost thousands before you course-correct.",
    },
    {
        "title": "The income gap nobody budgets for",
        "desc": "Spouse licensure, childcare waitlists, and deposit timing stack up fast — generic checklists don't sequence them.",
    },
    {
        "title": "The timeline that won't wait",
        "desc": "Report date, hiring windows, and school registration deadlines don't care that you're still in Facebook research mode.",
    },
]

OUTCOME_BENEFITS = [
    {
        "title": "Decisions, not data dumps",
        "desc": (
            "Get a senior-NCO-style strategic plan with clear recommendations, ranked alternatives, "
            "and the one risk that collapses everything if you ignore it."
        ),
        "icon": "◎",
    },
    {
        "title": "Family stability first",
        "desc": (
            "Spouse career paths, school zoning, and childcare sequencing are woven together — "
            "because those threads actually determine whether your PCS works."
        ),
        "icon": "◎",
    },
    {
        "title": "Real math, real timelines",
        "desc": (
            "2026 BAH figures, DITY/PPM estimates, cash-flow pressure, and installation-specific "
            "gotchas — not blog-post generalities."
        ),
        "icon": "◎",
    },
]

DIY_VS_VECTOR = [
    {"label": "Facebook groups & Reddit threads", "diy": "Hours of conflicting opinions", "vector": "One synthesized plan for your family"},
    {"label": "Generic PCS checklists", "diy": "Tasks without dependencies", "vector": "Decision gates and sequenced actions"},
    {"label": "Housing sites alone", "diy": "Rent vs BAH once", "vector": "6-month surplus, utilities, and school-zone tradeoffs"},
    {"label": "Spouse job boards", "diy": "Apply and hope", "vector": "Licensure timeline, fast-tracks, and military spouse leverage"},
]

WHY_25 = {
    "headline": "Why $25 beats another week of research",
    "intro": (
        "A PCS touches your housing budget, spouse's career, children's schools, and cash flow "
        "for the next 2–3 years. One wrong lease, missed hiring window, or unbudgeted income gap "
        "typically costs far more than this report."
    ),
    "points": [
        {
            "title": "Time you'll actually get back",
            "desc": "Families spend 10–20+ hours piecing together housing, schools, and spouse leads. PCS Vector delivers a decision-ready plan in minutes after a 6–8 minute form.",
        },
        {
            "title": "Mistakes you'll likely avoid",
            "desc": "Off-post leases in the wrong district, DITY choices that don't match family complexity, and spouse income gaps without a cash cushion — the report calls these out explicitly.",
        },
        {
            "title": "Peace of mind before boxes ship",
            "desc": "Walk into your PCS with a spouse-readable plan, commander brief line, and ranked next steps — not a browser full of half-answered tabs.",
        },
    ],
    "roi_line": (
        "Most families report the plan pays for itself if it prevents one housing mistake "
        "or shaves even a week off spouse unemployment."
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
        "desc": "Phased Soldier and Spouse tasks with decision gates — parallel execution, not a generic checklist.",
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
    "“Lock off-post in Hope Mills before arrival — $644 BAH surplus with Cumberland County school access.”",
    "“Run partial DITY: $2,179 net on 7,000 lbs — lower risk than full truck with kids and pets.”",
    "“Spouse: substitute pool + lateral-entry in parallel — 4-week licensure delay costs $3,600.”",
    "“If childcare isn't locked by day 21, the entire employment timeline slips — submit DD 2606 day one.”",
]

TESTIMONIAL = {
    "quote": (
        "We had orders to Bragg and no idea where to start with schools and spouse employment. "
        "This wasn't another checklist — it told us what to decide first and what would go wrong "
        "if we waited. My husband and I finally had the same plan."
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
        "not a generic checklist. You get clear recommendations, risk analysis, and sequenced next steps "
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