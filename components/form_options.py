"""Dropdown and option lists for the PCS input form."""

from services.installation_data import SUPPORTED_INSTALLATIONS

RANK_PAY_GRADES = [
    "E-1",
    "E-2",
    "E-3",
    "E-4",
    "E-5",
    "E-6",
    "E-7",
    "E-8",
    "E-9",
    "W-1",
    "W-2",
    "W-3",
    "W-4",
    "W-5",
    "O-1",
    "O-2",
    "O-3",
    "O-4",
    "O-5",
    "O-6",
    "O-7+",
    "Other",
]

PAY_GRADE_TO_RANK: dict[str, str] = {
    "E-1": "Private",
    "E-2": "Private",
    "E-3": "Private First Class",
    "E-4": "Specialist",
    "E-5": "Sergeant",
    "E-6": "Staff Sergeant",
    "E-7": "Sergeant First Class",
    "E-8": "Master Sergeant",
    "E-9": "Sergeant Major",
    "W-1": "Warrant Officer 1",
    "W-2": "Chief Warrant Officer 2",
    "W-3": "Chief Warrant Officer 3",
    "W-4": "Chief Warrant Officer 4",
    "W-5": "Chief Warrant Officer 5",
    "O-1": "Second Lieutenant",
    "O-2": "First Lieutenant",
    "O-3": "Captain",
    "O-4": "Major",
    "O-5": "Lieutenant Colonel",
    "O-6": "Colonel",
    "O-7+": "General Officer",
}


def rank_for_pay_grade(pay_grade: str) -> str:
    """Return the standard rank title for a pay grade."""
    return PAY_GRADE_TO_RANK.get(pay_grade, "")

CURRENT_INSTALLATIONS = [*SUPPORTED_INSTALLATIONS, "Other installation"]

GAINING_INSTALLATIONS = [*SUPPORTED_INSTALLATIONS, "Other CONUS installation"]

MOVE_WINDOWS = [
    "Within 30 days",
    "1–3 months",
    "3–6 months",
    "6+ months",
    "Orders not firm yet",
]

MOVE_FLEXIBILITY = [
    "Fixed — must align with reporting date",
    "Somewhat flexible (±2 weeks)",
    "Very flexible — open to best timing",
]

SPOUSE_CAREER_FIELDS = [
    "K-12 education / teaching",
    "Healthcare / nursing",
    "Remote / work-from-home professional",
    "Federal / government civilian",
    "Retail / hospitality / service",
    "Trades / skilled labor",
    "Not currently working — seeking employment",
    "Student / continuing education",
    "Other field",
]

HOUSING_PREFERENCES = [
    "On-post — prefer government housing",
    "Off-post — prefer renting/buying locally",
    "Open to either — best overall fit",
]

BUDGET_MODES = [
    "Optimize for best value",
    "Set a monthly budget cap",
]

BUDGET_PRESETS = [
    "Under $1,200/mo",
    "$1,200 – $1,600/mo",
    "$1,600 – $2,000/mo",
    "$2,000+/mo",
    "Custom amount",
]

HOUSING_MUST_HAVES = [
    "4+ bedrooms",
    "Fenced yard",
    "Garage / covered parking",
    "Short commute (under 20 min)",
    "Strong internet / remote-work ready",
    "Pet-friendly",
    "Newer construction",
]

CHILD_AGE_RANGES = [
    "Infant (0–2)",
    "Preschool (3–5)",
    "Elementary (6–10)",
    "Middle school (11–13)",
    "High school (14–18)",
]

PRIORITY_CHOICES = [
    "Spouse career / quick employment",
    "Minimizing total costs",
    "Fastest possible resettlement",
    "School quality",
]

# Legacy mapping for summaries
PRIORITY_LABELS = {
    "spouse_career": "Spouse career / quick employment",
    "minimize_costs": "Minimizing total costs",
    "fast_resettlement": "Fastest possible resettlement",
    "school_quality": "School quality",
}

DITY_OPTIONS = [
    "Yes — I want to explore a DITY/PPM move",
    "Maybe — run the numbers for me",
    "No — prefer a full government move",
]

PET_OPTIONS = ["No pets", "Yes — we have pets"]

PET_TYPES = [
    "Dog (under 50 lb)",
    "Dog (50 lb or more)",
    "Cat(s)",
    "Other pet",
]

VEHICLE_COUNTS = ["0", "1", "2", "3+"]

CONCERN_FLAGS = [
    "Child has IEP / special education needs",
    "EFMP / medical care coordination",
    "Dual-military household",
    "Professional licensure transfer",
    "Winter weather / heating costs",
    "Gate traffic / commute sensitivity",
    "Need childcare immediately on arrival",
]