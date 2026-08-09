"""Installation-specific reference data for PCS Vector report templates.

Uses traditional installation names only (Fort Bragg, Fort Hood, Fort Benning, etc.).
New official names (Fort Liberty, Fort Cavazos, Fort Moore, etc.) are accepted as aliases
and resolve to the traditional keys in INSTALLATION_DATA.

BAH figures in _RICH_PROFILES are planning fallbacks when bah_2026.json has no entry.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

Priority = Literal["High", "Medium", "Low"]

# ---------------------------------------------------------------------------
# Canonical installation registry (traditional names)
# Keys use "Fort Name, ST" or "Joint Base ..., ST" format.
# ---------------------------------------------------------------------------

INSTALLATION_DATA: dict[str, dict[str, Any]] = {
    "Aberdeen Proving Ground, MD": {
        "state": "MD",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "RDECOM and test community. Baltimore metro 40 min south; spouse jobs in federal labs and healthcare.",
        "major_areas": [
            "Aberdeen",
            "Bel Air",
            "Edgewood",
            "Havre de Grace",
        ],
        "school_districts": [
            "Harford County Public Schools",
        ],
        "commute_notes": "I-95 and MD-22 peak with APG gates; Bel Air popular for schools.",
    },
    "Camp Casey, South Korea": {
        "state": "ROK",
        "priority": "Medium",
        "theater": "OCONUS",
        "notes": "2ID corridor north of Seoul. Unaccompanied tours common; command sponsorship limited. Use OHA not CONUS BAH.",
        "major_areas": [
            "Dongducheon",
            "Uijeongbu",
            "On-post housing (limited)",
        ],
        "school_districts": [
            "DODEA Korea (verify assignment eligibility)",
        ],
        "commute_notes": "Traffic toward Seoul heavy on weekends; winter cold; SOF-focused operational tempo nearby.",
    },
    "Camp Humphreys, South Korea": {
        "state": "ROK",
        "priority": "High",
        "theater": "OCONUS",
        "notes": "Primary USAG Korea hub. Command-sponsored families common. OHA/COL allowances apply; DODEA schools on/near post.",
        "major_areas": [
            "Pyeongtaek",
            "Anjeong-ri",
            "On-post family housing",
        ],
        "school_districts": [
            "DODEA Camp Humphreys schools",
        ],
        "commute_notes": "Large post footprint; gate wait times spike with school runs; high-speed rail access to Seoul.",
    },
    "Camp Zama, Japan": {
        "state": "Japan",
        "priority": "Medium",
        "theater": "OCONUS",
        "notes": "USAG Japan HQ. Tokyo metro access; OHA housing market competitive. Japanese vehicle rules and tolls matter.",
        "major_areas": [
            "Zama",
            "Sagamihara",
            "Machida (Tokyo side)",
        ],
        "school_districts": [
            "DODEA Japan schools (Camp Zama area)",
        ],
        "commute_notes": "Rail-centric lifestyle; parking limited off-post; typhoon season Jun–Oct.",
    },
    "Carlisle Barracks, PA": {
        "state": "PA",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "Army War College. Officer/senior NCO heavy PCS; short academic tours common; Harrisburg 30 min east.",
        "major_areas": [
            "Carlisle",
            "Mechanicsburg",
            "Camp Hill",
            "Harrisburg west shore",
        ],
        "school_districts": [
            "Carlisle Area School District",
            "Cumberland Valley SD",
        ],
        "commute_notes": "I-81 and PA-641; on-post historic housing limited; off-post inventory tight before academic year.",
    },
    "Detroit Arsenal, MI": {
        "state": "MI",
        "priority": "Low",
        "theater": "CONUS",
        "notes": "TACOM and acquisition community. Metro Detroit; winters and auto industry cycle affect rentals.",
        "major_areas": [
            "Warren",
            "Sterling Heights",
            "Troy",
            "Detroit suburbs north",
        ],
        "school_districts": [
            "Warren Consolidated Schools",
            "Utica Community Schools",
        ],
        "commute_notes": "I-696 and Mound Rd; snow delays Nov–Mar; spouse jobs strong in healthcare and tech.",
    },
    "Dugway Proving Ground, UT": {
        "state": "UT",
        "priority": "Low",
        "theater": "CONUS",
        "notes": "Isolated test range. Most live on-post or long commute from Tooele/Salt Lake valley.",
        "major_areas": [
            "On-post housing (primary)",
            "Tooele",
            "Grantsville",
        ],
        "school_districts": [
            "Tooele County School District",
            "On-post school options (verify)",
        ],
        "commute_notes": "Long desert drives; limited off-post inventory; winter mountain passes.",
    },
    "Fort Belvoir, VA": {
        "state": "VA",
        "priority": "High",
        "theater": "CONUS",
        "notes": "NCR post — intel, logistics, and agency footprint. High DC-metro BAH; Fairfax/Prince William housing expensive; traffic drives every lease decision.",
        "major_areas": [
            "Lorton",
            "Springfield",
            "Woodbridge",
            "Alexandria (south / Franconia)",
            "Mount Vernon area",
        ],
        "school_districts": [
            "Fairfax County Public Schools",
            "Prince William County Schools",
        ],
        "commute_notes": "I-95 and Fairfax County Pkwy choke daily; south Fairfax / Lorton often best for Belvoir gates vs reverse commute from DC.",
    },
    "Fort Benning, GA": {
        "state": "GA",
        "priority": "High",
        "theater": "CONUS",
        "notes": "High volume; Maneuver Center of Excellence. Heavy training tempo; spouse jobs cluster in Columbus and Phenix City.",
        "major_areas": [
            "Columbus, GA",
            "Phenix City, AL",
            "Midland / Upatoi corridor",
        ],
        "school_districts": [
            "Muscogee County Schools (GA)",
            "Russell County Schools (AL — Phenix City)",
        ],
        "commute_notes": "US-280 and Victory Drive peak with basic training graduations; AL leases require GA school zoning check.",
    },
    "Fort Bliss, TX": {
        "state": "TX",
        "priority": "High",
        "theater": "CONUS",
        "notes": "High volume; 1st Armored Division and WBAMC. Desert market favors off-post BAH surplus; verify unit gate (main vs east).",
        "major_areas": [
            "Northeast El Paso",
            "Horizon City",
            "West El Paso",
            "Sunland Park (NM)",
        ],
        "school_districts": [
            "El Paso ISD",
            "Socorro ISD",
            "Ysleta ISD",
        ],
        "commute_notes": "US-54 and Loop 375 choke at rush; monsoon season (Jul–Sep) can add 15–20 min unpredictably.",
    },
    "Fort Bragg, NC": {
        "state": "NC",
        "priority": "High",
        "theater": "CONUS",
        "notes": "Very high PCS volume; 82nd Airborne and SF corridor. Spouse employment and school zoning drive most family decisions.",
        "major_areas": [
            "Hope Mills",
            "Spring Lake",
            "Fayetteville (north side)",
            "Raeford",
        ],
        "school_districts": [
            "Cumberland County Schools",
            "Harnett County Schools (verify zoning)",
        ],
        "commute_notes": "All-American Fwy and Bragg Blvd peak 0630–0800; pre-apply rentals from losing station in summer PCS.",
    },
    "Fort Buchanan, PR": {
        "state": "PR",
        "priority": "Low",
        "theater": "OCONUS",
        "notes": "USAR / reserve hub in San Juan area. Tropical climate; hurricane season; OHA/local housing rules differ from CONUS BAH.",
        "major_areas": [
            "Guaynabo",
            "Bayamón",
            "San Juan metro",
        ],
        "school_districts": [
            "Puerto Rico Department of Education (verify bilingual options)",
            "DODEA if available",
        ],
        "commute_notes": "PR-22 congestion; hurricane prep required Jun–Nov.",
    },
    "Fort Campbell, KY": {
        "state": "KY/TN",
        "priority": "High",
        "theater": "CONUS",
        "notes": "High volume; 101st Airborne. Straddles KY/TN line — school district and state tax differ by side of post.",
        "major_areas": [
            "Clarksville, TN",
            "Oak Grove, KY",
            "Hopkinsville, KY",
            "Fort Campbell North housing",
        ],
        "school_districts": [
            "Clarksville-Montgomery County Schools (TN)",
            "Christian County Schools (KY)",
            "Fort Campbell Schools (on-post DODEA)",
        ],
        "commute_notes": "Madam Walker / Fort Campbell Blvd rush peaks with division cycles; TN side has more inventory, KY side quieter.",
    },
    "Fort Carson, CO": {
        "state": "CO",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "Medium-high volume; 4th Infantry Division. Elevation and wildfire smoke affect health; Colorado Springs market competitive.",
        "major_areas": [
            "Colorado Springs (south / Security-Widefield)",
            "Fountain",
            "Pueblo West",
        ],
        "school_districts": [
            "Fountain-Fort Carson School District 8",
            "Harrison School District 2",
            "Widefield School District 3",
        ],
        "commute_notes": "I-25 and Academy Blvd rush; verify gate (Main vs Gate 20) against unit location on post.",
    },
    "Fort Detrick, MD": {
        "state": "MD",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "Medical and biodefense. Frederick metro growing; DC/Baltimore reachable for dual-income spouses.",
        "major_areas": [
            "Frederick",
            "Walkersville",
            "Urbana",
            "Middletown",
        ],
        "school_districts": [
            "Frederick County Public Schools",
        ],
        "commute_notes": "US-15 and I-70; Frederick has strong school options and competitive rents.",
    },
    "Fort Drum, NY": {
        "state": "NY",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "Medium volume; 10th Mountain Division. Winter weather and heating costs are primary off-post risk factors.",
        "major_areas": [
            "Evans Mills",
            "Carthage",
            "Watertown",
            "Le Ray",
        ],
        "school_districts": [
            "Indian River Central School District",
            "Watertown City School District",
        ],
        "commute_notes": "Route 11 lake-effect closures Oct–Apr; build 30-min winter commute buffer.",
    },
    "Fort Gordon, GA": {
        "state": "GA",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "Medium-high volume; cyber and signal school hub. Augusta metro growing; Columbia County schools are top draw.",
        "major_areas": [
            "Evans",
            "Grovetown",
            "Martinez",
            "West Augusta",
        ],
        "school_districts": [
            "Columbia County Schools",
            "Richmond County Schools",
        ],
        "commute_notes": "Gordon Hwy and Gate 1 peak 0630–0730; Evans adds 15–20 min but better school ratings.",
    },
    "Fort Greely, AK": {
        "state": "AK",
        "priority": "Low",
        "theater": "CONUS",
        "notes": "Missile defense site. Very small community; extreme cold; most families on-post. COLA and PPM rules apply.",
        "major_areas": [
            "Delta Junction",
            "On-post housing",
        ],
        "school_districts": [
            "Delta/Greely School District",
        ],
        "commute_notes": "Isolated highway corridor; winter logistics dominate PCS planning.",
    },
    "Fort Hamilton, NY": {
        "state": "NY",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "NYC harbor post. Tiny footprint; most live off-post in Brooklyn/Staten Island; high cost of living.",
        "major_areas": [
            "Bay Ridge Brooklyn",
            "Staten Island",
            "Dyker Heights",
        ],
        "school_districts": [
            "NYC DOE (district varies by address)",
            "Nearby private/parochial options",
        ],
        "commute_notes": "Belt Pkwy and Verrazzano Bridge traffic; mass transit often better than driving.",
    },
    "Fort Hood, TX": {
        "state": "TX",
        "priority": "High",
        "theater": "CONUS",
        "notes": "Very high volume; III Armored Corps. Competitive Central Texas rental market; summer AC costs matter off-post.",
        "major_areas": [
            "Killeen",
            "Harker Heights",
            "Copperas Cove",
            "Nolanville",
        ],
        "school_districts": [
            "Killeen ISD",
            "Copperas Cove ISD",
        ],
        "commute_notes": "US-190 and Trimmier Rd gates back up at peak; Copperas Cove offers strong BAH surplus with longer drive.",
    },
    "Fort Huachuca, AZ": {
        "state": "AZ",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "Medium volume; intelligence and unmanned systems school. Sierra Vista market small; Tucson 70 min for spouse jobs.",
        "major_areas": [
            "Sierra Vista",
            "Huachuca City",
            "Hereford",
        ],
        "school_districts": [
            "Sierra Vista Unified School District",
            "Fry Elementary area (verify zoning)",
        ],
        "commute_notes": "Buffalo Soldier Gate and AZ-90; monsoon flooding on low crossings; remote spouse may need Tucson commute.",
    },
    "Fort Irwin, CA": {
        "state": "CA",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "Medium volume; National Training Center. Isolated desert post — most families live on-post or in Barstow; spouse jobs limited.",
        "major_areas": [
            "Barstow",
            "On-post housing (primary)",
            "Victorville (long commute)",
        ],
        "school_districts": [
            "Silver Valley Unified (on-post / Barstow area)",
            "Barstow Unified (off-post)",
        ],
        "commute_notes": "I-15 NTC gate run is 35+ min from Barstow; heat and wind drive high AC and vehicle wear.",
    },
    "Fort Jackson, SC": {
        "state": "SC",
        "priority": "High",
        "theater": "CONUS",
        "notes": "High volume; TRADOC initial entry training. Constant PCS churn; Columbia metro offers spouse job depth.",
        "major_areas": [
            "Columbia (northeast / Forest Acres)",
            "Elgin",
            "Blythewood",
            "Lexington",
        ],
        "school_districts": [
            "Richland School District Two",
            "Lexington County School District One",
        ],
        "commute_notes": "I-77 and Forest Drive congestion; Blythewood popular for schools, verify gate-to-barracks commute for sponsors.",
    },
    "Fort Knox, KY": {
        "state": "KY",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "Medium volume; Human Resources Command and cadet command. Radcliff/Elizabethtown corridor; Louisville 40 min north.",
        "major_areas": [
            "Radcliff",
            "Elizabethtown",
            "Vine Grove",
            "Louisville (south end)",
        ],
        "school_districts": [
            "Hardin County Schools",
            "Elizabethtown Independent",
        ],
        "commute_notes": "US-31W Dixie Highway peak with Fort Knox gate; Radcliff closest but school ratings vary by neighborhood.",
    },
    "Fort Leavenworth, KS": {
        "state": "KS",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "Medium-high volume; CGSC and staff college. Officer-heavy; on-post housing culture strong; KC metro 40 min north.",
        "major_areas": [
            "Leavenworth",
            "Lansing",
            "Basehor",
            "Platte City, MO",
        ],
        "school_districts": [
            "Leavenworth USD 453",
            "Lansing USD 469",
        ],
        "commute_notes": "Historic post with tight housing market; US-73 bridge traffic spikes with school calendar.",
    },
    "Fort Lee, VA": {
        "state": "VA",
        "priority": "High",
        "theater": "CONUS",
        "notes": "Sustainment and logistics school (also known as Fort Gregg-Adams). Petersburg/Colonial Heights market; Richmond 30 min north.",
        "major_areas": [
            "Petersburg",
            "Colonial Heights",
            "Prince George",
            "Chester",
        ],
        "school_districts": [
            "Prince George County Schools",
            "Chesterfield County Schools",
            "Colonial Heights City",
        ],
        "commute_notes": "I-95 and Temple Ave peak with training cycles; Chesterfield for schools, closer towns for short commute.",
    },
    "Fort Leonard Wood, MO": {
        "state": "MO",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "Medium volume; Maneuver Support Center. Training post with steady churn; Waynesville and St. Robert are hub towns.",
        "major_areas": [
            "Waynesville",
            "St. Robert",
            "Lebanon",
        ],
        "school_districts": [
            "Waynesville R-VI School District",
            "Laquey R-V School District",
        ],
        "commute_notes": "I-44 and MO-17 gate rush with basic training cycles; St. Robert has most retail and spouse service jobs.",
    },
    "Fort McCoy, WI": {
        "state": "WI",
        "priority": "Low",
        "theater": "CONUS",
        "notes": "Lower volume; training and mobilization platform. Many PCS are short tours; Sparta and Tomah are primary off-post towns.",
        "major_areas": [
            "Sparta",
            "Tomah",
            "On-post quarters (limited)",
        ],
        "school_districts": [
            "Sparta Area School District",
            "Tomah Area School District",
        ],
        "commute_notes": "Rural I-90 corridor; winter road maintenance good but black ice common Nov–Mar.",
    },
    "Fort Meade, MD": {
        "state": "MD",
        "priority": "High",
        "theater": "CONUS",
        "notes": "Cyber and intel corridor (NSA adjacent). Anne Arundel / Howard County; high demand housing near cyber employers.",
        "major_areas": [
            "Odenton",
            "Severn",
            "Columbia",
            "Laurel",
        ],
        "school_districts": [
            "Anne Arundel County Public Schools",
            "Howard County Public Schools",
        ],
        "commute_notes": "MD-32 and BW Parkway; Odenton walkable to MARC for DC spouses.",
    },
    "Fort Myer, VA": {
        "state": "VA",
        "priority": "High",
        "theater": "CONUS",
        "notes": "Joint Base Myer–Henderson Hall (Fort Myer + Henderson Hall + Fort McNair). Ceremonial and NCR mission; Pentagon support population. Arlington housing scarce and expensive; many live in Alexandria, Arlington, or DC metro.",
        "major_areas": [
            "Arlington",
            "Alexandria",
            "Falls Church",
            "Pentagon City / Crystal City",
            "On-post quarters (very limited)",
        ],
        "school_districts": [
            "Arlington Public Schools",
            "Alexandria City Public Schools",
            "Fairfax County Public Schools",
        ],
        "commute_notes": "I-395 and GW Parkway peak daily; Metro (Blue/Yellow) is a primary housing filter for Pentagon and Myer duty.",
    },
    "Pentagon / National Capital Region, VA": {
        "state": "VA",
        "priority": "High",
        "theater": "CONUS",
        "notes": "Pentagon and NCR Army duty (often admin/joint). Same Washington DC metro BAH MHA as Fort Myer / Belvoir. Housing strategy mirrors Fort Myer — Metro access and VA vs MD tax/schools tradeoffs.",
        "major_areas": [
            "Arlington / Pentagon City",
            "Alexandria",
            "Falls Church",
            "Springfield / Franconia",
            "Bethesda / Silver Spring (MD side)",
        ],
        "school_districts": [
            "Arlington Public Schools",
            "Alexandria City Public Schools",
            "Fairfax County Public Schools",
            "Montgomery County Public Schools (MD)",
        ],
        "commute_notes": "I-395, 14th St Bridge, and Metro Blue/Yellow define commute; reverse-commute from south Alexandria often better than DC proper.",
    },
    "Fort Polk, LA": {
        "state": "LA",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "Medium volume; JRTC. Rural market; Leesville and DeRidder are main off-post options with limited spouse employment.",
        "major_areas": [
            "Leesville",
            "DeRidder",
            "New Llano",
        ],
        "school_districts": [
            "Vernon Parish School District",
            "Beauregard Parish (DeRidder)",
        ],
        "commute_notes": "US-171 and LA-28; hurricane season Jun–Nov; limited rental inventory spikes before rotation cycles.",
    },
    "Fort Riley, KS": {
        "state": "KS",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "Medium-high volume; 1st Infantry Division. Manhattan (K-State) offers spouse jobs; tornado season awareness.",
        "major_areas": [
            "Junction City",
            "Manhattan",
            "Ogden",
        ],
        "school_districts": [
            "Geary County Schools (USD 475)",
            "Manhattan-Ogden USD 383",
        ],
        "commute_notes": "Fort Riley Blvd and I-70 interchange peak with division deployments; Manhattan commute 20–30 min.",
    },
    "Fort Rucker, AL": {
        "state": "AL",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "Medium volume; Army aviation center. Enterprise and Daleville dominate off-post; spouse jobs in healthcare and schools.",
        "major_areas": [
            "Enterprise",
            "Daleville",
            "Ozark",
        ],
        "school_districts": [
            "Enterprise City Schools",
            "Dale County Schools",
        ],
        "commute_notes": "US-231 and Rucker Blvd; low cost of living but limited inventory near gates.",
    },
    "Fort Sam Houston, TX": {
        "state": "TX",
        "priority": "High",
        "theater": "CONUS",
        "notes": "JBSA medical and command hub (AMEDD). San Antonio metro; BAMC and military medicine dominate spouse healthcare jobs.",
        "major_areas": [
            "San Antonio (northeast)",
            "Schertz",
            "Universal City",
            "Converse",
        ],
        "school_districts": [
            "North East ISD",
            "Schertz-Cibolo-Universal City ISD",
            "Judson ISD",
        ],
        "commute_notes": "I-35 and Loop 1604; verify JBSA gate (Sam Houston vs Randolph) against duty location.",
    },
    "Fort Shafter, HI": {
        "state": "HI",
        "priority": "Medium",
        "theater": "OCONUS",
        "notes": "USARPAC HQ. Honolulu cost of living high; OHA applies. Concurrent travel and household goods rules differ from CONUS.",
        "major_areas": [
            "Honolulu",
            "Aiea",
            "Salt Lake",
            "Moanalua",
        ],
        "school_districts": [
            "Hawaii DOE (complex area by address)",
            "DODEA if eligible",
        ],
        "commute_notes": "H-1 congestion daily; on-post housing waitlists long; vehicle shipping timelines critical.",
    },
    "Fort Sill, OK": {
        "state": "OK",
        "priority": "High",
        "theater": "CONUS",
        "notes": "High volume; Fires Center of Excellence. Lawton market is affordable; wind and hail affect insurance off-post.",
        "major_areas": [
            "Lawton",
            "Cache",
            "Medicine Park",
        ],
        "school_districts": [
            "Lawton Public Schools",
            "Cache Public Schools",
        ],
        "commute_notes": "Sheridan Road and Fort Sill Blvd are main arteries; shorter commutes than most CONUS posts.",
    },
    "Fort Stewart, GA": {
        "state": "GA",
        "priority": "High",
        "theater": "CONUS",
        "notes": "High volume; 3rd Infantry Division. Coastal Georgia humidity and hurricane season affect utilities and insurance.",
        "major_areas": [
            "Hinesville",
            "Richmond Hill",
            "Pooler",
            "Savannah suburbs (west)",
        ],
        "school_districts": [
            "Liberty County Schools",
            "Bryan County Schools",
        ],
        "commute_notes": "GA-119 and US-84 gate corridors; Richmond Hill popular for schools but adds 20–25 min.",
    },
    "Fort Wainwright, AK": {
        "state": "AK",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "Special case — Alaska PCS. COLA and PPM weight restrictions apply; extreme cold, darkness, and limited road network off-post.",
        "major_areas": [
            "Fairbanks (north and west)",
            "North Pole",
            "On-post housing (high demand)",
        ],
        "school_districts": [
            "Fairbanks North Star Borough School District",
        ],
        "commute_notes": "Winter plug-in block heaters required; -40°F days cancel school and delay in-processing; PPM often ships via Seattle.",
    },
    "Hunter Army Airfield, GA": {
        "state": "GA",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "Aviation support to Fort Stewart. Savannah metro; often paired with Stewart PCS planning.",
        "major_areas": [
            "Savannah",
            "Pooler",
            "Richmond Hill",
            "Hinesville (if dual with Stewart)",
        ],
        "school_districts": [
            "Savannah-Chatham County Schools",
            "Bryan County Schools",
        ],
        "commute_notes": "I-95 and Dean Forest Rd; hurricane season insurance check for coastal rentals.",
    },
    "Joint Base Elmendorf-Richardson, AK": {
        "state": "AK",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "Joint Army/Air Force. Anchorage metro; COLA and extreme winter logistics; dual-service spouse employment possible.",
        "major_areas": [
            "Anchorage (northeast / Eagle River)",
            "JBER on-post",
            "Wasilla (longer commute)",
        ],
        "school_districts": [
            "Anchorage School District",
            "Mat-Su Borough (if living north)",
        ],
        "commute_notes": "Glenn Hwy winter conditions; block heaters; limited daylight in winter affects school and morale planning.",
    },
    "Joint Base Langley-Eustis, VA": {
        "state": "VA",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "Army (Eustis) and Air Force (Langley). Hampton Roads; TRA/DOC training footprint on Eustis side.",
        "major_areas": [
            "Newport News",
            "Hampton",
            "Yorktown",
            "Williamsburg (north)",
        ],
        "school_districts": [
            "Newport News Public Schools",
            "York County Schools",
            "Hampton City Schools",
        ],
        "commute_notes": "I-64 tunnel/bridge congestion; verify Eustis vs Langley gate for daily commute.",
    },
    "Joint Base Lewis-McChord, WA": {
        "state": "WA",
        "priority": "High",
        "theater": "CONUS",
        "notes": "High volume; I Corps and 62nd AW. Rain, traffic, and tight Pierce County rental market define PCS planning.",
        "major_areas": [
            "Lakewood",
            "DuPont",
            "Puyallup",
            "Yelm",
        ],
        "school_districts": [
            "Clover Park School District",
            "Steilacoom Historical School District",
            "Yelm Community Schools",
        ],
        "commute_notes": "I-5 and SR-507 choke points; DuPont walkable to Madigan but inventory turns fast in summer.",
    },
    "Joint Base San Antonio, TX": {
        "state": "TX",
        "priority": "High",
        "theater": "CONUS",
        "notes": "Multi-installation JBSA (Sam Houston, Randolph, Lackland). Confirm duty location before housing search.",
        "major_areas": [
            "San Antonio",
            "Schertz",
            "Universal City",
            "Live Oak",
        ],
        "school_districts": [
            "North East ISD",
            "Northside ISD",
            "Schertz-Cibolo-Universal City ISD",
        ],
        "commute_notes": "I-35 / Loop 1604; housing that works for Sam Houston may be wrong for Randolph.",
    },
    "Picatinny Arsenal, NJ": {
        "state": "NJ",
        "priority": "Low",
        "theater": "CONUS",
        "notes": "Armaments R&D. Morris/Sussex County; high NJ cost of living; NYC/North Jersey dual-career common.",
        "major_areas": [
            "Rockaway",
            "Dover",
            "Sparta",
            "Morristown area",
        ],
        "school_districts": [
            "Local Morris/Sussex district by town (verify zoning)",
        ],
        "commute_notes": "I-80 congestion; winter storms; limited on-post family housing.",
    },
    "Presidio of Monterey, CA": {
        "state": "CA",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "DLI / language training. Monterey Bay high rent; short training tours common; California vehicle rules apply.",
        "major_areas": [
            "Monterey",
            "Seaside",
            "Marina",
            "Pacific Grove",
        ],
        "school_districts": [
            "Monterey Peninsula Unified",
            "Pacific Grove Unified",
        ],
        "commute_notes": "Fog and tourist traffic; inventory tight year-round; many live in Seaside/Marina for value.",
    },
    "Redstone Arsenal, AL": {
        "state": "AL",
        "priority": "High",
        "theater": "CONUS",
        "notes": "Missile / aviation / Space Command footprint. Huntsville tech boom; strong spouse STEM and federal jobs.",
        "major_areas": [
            "Huntsville",
            "Madison",
            "Hampton Cove",
            "Owens Cross Roads",
        ],
        "school_districts": [
            "Huntsville City Schools",
            "Madison City Schools",
            "Madison County Schools",
        ],
        "commute_notes": "I-565 and Martin Rd; Madison schools highly sought; summer heat utilities moderate.",
    },
    "Rock Island Arsenal, IL": {
        "state": "IL",
        "priority": "Low",
        "theater": "CONUS",
        "notes": "Island arsenal / JOC footprint. Quad Cities metro (IL/IA); low cost relative to coasts.",
        "major_areas": [
            "Rock Island",
            "Moline",
            "Davenport, IA",
            "Bettendorf, IA",
        ],
        "school_districts": [
            "Rock Island-Milan SD",
            "Moline-Coal Valley",
            "Davenport CSD (IA)",
        ],
        "commute_notes": "Bridges to Iowa peak at rush; winter river valley ice; dual-state tax considerations if living in IA.",
    },
    "Schofield Barracks, HI": {
        "state": "HI",
        "priority": "High",
        "theater": "OCONUS",
        "notes": "25th ID. Central Oahu; OHA housing market competitive. Concurrent with Fort Shafter for some families.",
        "major_areas": [
            "Wahiawa",
            "Mililani",
            "Waipahu",
            "On-post housing",
        ],
        "school_districts": [
            "Hawaii DOE (Leilehua / Mililani complexes)",
            "DODEA if eligible",
        ],
        "commute_notes": "H-2 congestion; on-post waitlists long; vehicle shipping and temporary lodging critical.",
    },
    "US Military Academy West Point, NY": {
        "state": "NY",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "USMA. Faculty and staff PCS; Hudson Valley high cost; NYC 50+ mi south.",
        "major_areas": [
            "Highland Falls",
            "Cornwall",
            "Newburgh",
            "On-post quarters",
        ],
        "school_districts": [
            "Highland Falls-Fort Montgomery CSD",
            "Cornwall CSD",
        ],
        "commute_notes": "US-9W and Bear Mountain Bridge traffic; limited inventory near gates.",
    },
    "USAG Bavaria, Germany": {
        "state": "Germany",
        "priority": "High",
        "theater": "OCONUS",
        "notes": "Grafenwoehr / Vilseck / Hohenfels training hub. OHA; German housing contracts; DODEA schools; POV shipping long-lead.",
        "major_areas": [
            "Vilseck",
            "Grafenwoehr",
            "Amberg",
            "Sulzbach-Rosenberg",
        ],
        "school_districts": [
            "DODEA Bavaria schools",
        ],
        "commute_notes": "Training area traffic; winter alpine weather on routes; German rental deposits (Kaution) require cash planning.",
    },
    "USAG Italy, Italy": {
        "state": "Italy",
        "priority": "Medium",
        "theater": "OCONUS",
        "notes": "Vicenza (SETAF / 173rd) and Camp Darby. OHA; Italian leases; DODEA Vicenza. Mediterranean climate.",
        "major_areas": [
            "Vicenza",
            "Caserma Ederle area",
            "Livingston / nearby comuni",
        ],
        "school_districts": [
            "DODEA Vicenza schools",
        ],
        "commute_notes": "City center parking limited; A4 autostrada traffic; temporary lodging before lease common.",
    },
    "USAG Rheinland-Pfalz, Germany": {
        "state": "Germany",
        "priority": "High",
        "theater": "OCONUS",
        "notes": "Kaiserslautern / Baumholder / Landstuhl medical. Large Army community; OHA; strong DODEA footprint.",
        "major_areas": [
            "Kaiserslautern",
            "Landstuhl",
            "Baumholder",
            "Ramstein-adjacent towns",
        ],
        "school_districts": [
            "DODEA Kaiserslautern / Baumholder schools",
        ],
        "commute_notes": "Autobahn A6; German lease norms; medical appointments at LRMC drive some housing choices.",
    },
    "USAG Wiesbaden, Germany": {
        "state": "Germany",
        "priority": "Medium",
        "theater": "OCONUS",
        "notes": "USAREUR-AF HQ. Wiesbaden city housing competitive; OHA; Frankfurt airport access for TDY families.",
        "major_areas": [
            "Wiesbaden",
            "Mainz-Kastel",
            "Taunusstein",
        ],
        "school_districts": [
            "DODEA Wiesbaden schools",
        ],
        "commute_notes": "City parking and tram access matter; A66 congestion; higher OHA neighborhoods fill fast in summer.",
    },
    "White Sands Missile Range, NM": {
        "state": "NM",
        "priority": "Low",
        "theater": "CONUS",
        "notes": "Test range. Las Cruces is primary off-post city; El Paso 45–60 min for some services.",
        "major_areas": [
            "Las Cruces",
            "On-post housing",
            "Organ / east mesa",
        ],
        "school_districts": [
            "Las Cruces Public Schools",
        ],
        "commute_notes": "US-70 gate run; desert heat; limited local spouse employment outside Las Cruces.",
    },
    "Yuma Proving Ground, AZ": {
        "state": "AZ",
        "priority": "Low",
        "theater": "CONUS",
        "notes": "Desert test center. Yuma metro; extreme summer heat; many short TDY/PCS mixes.",
        "major_areas": [
            "Yuma",
            "Fortuna Foothills",
            "On-post housing",
        ],
        "school_districts": [
            "Yuma Elementary / Yuma Union High School Districts (verify)",
        ],
        "commute_notes": "US-95 heat and dust; AC utility spikes May–Sep; inventory limited near gates.",
    },
    "Fort McNair, DC": {
        "state": "DC",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "Part of Joint Base Myer–Henderson Hall (NCR). National Defense University footprint. Same DC metro BAH as Fort Myer; tiny post footprint.",
        "major_areas": ["Southwest DC", "Capitol Hill", "Arlington", "Alexandria"],
        "school_districts": ["DC Public Schools", "Arlington Public Schools", "Alexandria City Public Schools"],
        "commute_notes": "South Capitol St and I-395; limited parking; Metro access critical.",
    },
    "Joint Base McGuire-Dix-Lakehurst, NJ": {
        "state": "NJ",
        "priority": "Medium",
        "theater": "CONUS",
        "notes": "Joint Army/Air Force/Navy. Fort Dix Army side. Central NJ; Philadelphia 40 min; high NJ housing costs relative to BAH in some grades.",
        "major_areas": ["Wrightstown", "Pemberton", "Mount Holly", "Trenton suburbs"],
        "school_districts": ["Local Burlington County districts (verify by town)"],
        "commute_notes": "NJ Turnpike and I-295; verify Dix vs McGuire gate for daily duty.",
    },
    "Fort Walker, VA": {
        "state": "VA",
        "priority": "Low",
        "theater": "CONUS",
        "notes": "Training installation (formerly Fort A.P. Hill). Rural Caroline County; many short training-related moves; limited off-post inventory.",
        "major_areas": ["Bowling Green", "Fredericksburg (north)", "On-post lodging/quarters"],
        "school_districts": ["Caroline County Public Schools"],
        "commute_notes": "US-301 corridor; limited spouse employment locally — Fredericksburg for services.",
    },
    "Fort Barfoot, VA": {
        "state": "VA",
        "priority": "Low",
        "theater": "CONUS",
        "notes": "Training post (formerly Fort Pickett). Blackstone/Nottoway area; Guard/Reserve and training PCS patterns.",
        "major_areas": ["Blackstone", "Crewe", "Farmville (services)"],
        "school_districts": ["Nottoway County Public Schools"],
        "commute_notes": "Rural US-460; sparse rentals; plan ahead for school-year moves.",
    },
    "Fort Hunter Liggett, CA": {
        "state": "CA",
        "priority": "Low",
        "theater": "CONUS",
        "notes": "Reserve training center. Isolated Monterey County; limited family infrastructure; many unaccompanied/short tours.",
        "major_areas": ["King City", "Paso Robles (long)", "On-post quarters"],
        "school_districts": ["Local Monterey County districts (verify)"],
        "commute_notes": "Remote; long drives for medical/shopping; CA vehicle/registration rules apply.",
    },
    "Tobyhanna Army Depot, PA": {
        "state": "PA",
        "priority": "Low",
        "theater": "CONUS",
        "notes": "Electronics maintenance depot. Poconos region; Scranton/Wilkes-Barre within range for spouse jobs.",
        "major_areas": ["Tobyhanna", "Mount Pocono", "Stroudsburg", "Scranton area"],
        "school_districts": ["Pocono Mountain SD", "Local Monroe County districts"],
        "commute_notes": "I-380 winter conditions; tourist traffic in summer.",
    },
    "Anniston Army Depot, AL": {
        "state": "AL",
        "priority": "Low",
        "theater": "CONUS",
        "notes": "Vehicle/weapon systems depot. Anniston/Oxford metro; Birmingham ~1 hour.",
        "major_areas": ["Anniston", "Oxford", "Jacksonville, AL"],
        "school_districts": ["Anniston City Schools", "Oxford City Schools"],
        "commute_notes": "I-20 corridor; low cost of living; limited on-post family housing.",
    },
    "Fort Gillem, GA": {
        "state": "GA",
        "priority": "Low",
        "theater": "CONUS",
        "notes": "Atlanta area logistics/enclave footprint. Most personnel live in south metro Atlanta; confirm current mission/tenant unit.",
        "major_areas": ["Forest Park", "Morrow", "Jonesboro", "Atlanta south side"],
        "school_districts": ["Clayton County Public Schools", "Henry County Schools"],
        "commute_notes": "I-75 / I-285 congestion; Atlanta traffic dominates PCS housing choice.",
    },
    "Natick Soldier Systems Center, MA": {
        "state": "MA",
        "priority": "Low",
        "theater": "CONUS",
        "notes": "R&D / soldier systems. Boston metro west; high COL; many civilian-heavy workforce with small military PCS volume.",
        "major_areas": ["Natick", "Framingham", "Wellesley", "Boston west suburbs"],
        "school_districts": ["Natick Public Schools", "Framingham Public Schools"],
        "commute_notes": "Mass Pike (I-90) and Route 9; winter storms; expensive rentals.",
    },
    "Camp Atterbury, IN": {
        "state": "IN",
        "priority": "Low",
        "theater": "CONUS",
        "notes": "Training / mobilization platform. Edinburgh/Franklin area; Indianapolis ~40 min north.",
        "major_areas": ["Edinburgh", "Franklin", "Columbus, IN", "Greenwood"],
        "school_districts": ["Local Johnson/Bartholomew County districts"],
        "commute_notes": "US-31 corridor; rural market; many short training-related moves.",
    },
    "Sierra Army Depot, CA": {
        "state": "CA",
        "priority": "Low",
        "theater": "CONUS",
        "notes": "Isolated high-desert depot (Herlong). Very limited off-post options; Reno ~1 hour; family infrastructure sparse.",
        "major_areas": ["Herlong", "Susanville", "Reno, NV (long)"],
        "school_districts": ["Local Lassen County districts"],
        "commute_notes": "Remote; extreme weather swings; plan for long supply runs.",
    },
    "Fort Story, VA": {
        "state": "VA",
        "priority": "Low",
        "theater": "CONUS",
        "notes": "Joint Expeditionary Base Little Creek–Fort Story (Army/Navy). Virginia Beach / Norfolk market.",
        "major_areas": ["Virginia Beach", "Norfolk", "Chesapeake"],
        "school_districts": ["Virginia Beach City Public Schools", "Norfolk Public Schools"],
        "commute_notes": "Shore Dr and I-264; tourist season traffic; coastal flood insurance check.",
    },
}

SUPPORTED_INSTALLATIONS: list[str] = sorted(INSTALLATION_DATA.keys())

# New official names → traditional keys (never expose new names in user-facing copy).
INSTALLATION_ALIASES: dict[str, str] = {
    "Pentagon": "Pentagon / National Capital Region, VA",
    "The Pentagon": "Pentagon / National Capital Region, VA",
    "Pentagon, VA": "Pentagon / National Capital Region, VA",
    "Pentagon / National Capital Region": "Pentagon / National Capital Region, VA",
    "Fort McNair": "Fort McNair, DC",
    "Fort McNair, VA": "Fort McNair, DC",
    "Fort A.P. Hill": "Fort Walker, VA",
    "Fort A.P. Hill, VA": "Fort Walker, VA",
    "Fort AP Hill": "Fort Walker, VA",
    "Fort Pickett": "Fort Barfoot, VA",
    "Fort Pickett, VA": "Fort Barfoot, VA",
    "JB MDL": "Joint Base McGuire-Dix-Lakehurst, NJ",
    "Fort Dix": "Joint Base McGuire-Dix-Lakehurst, NJ",
    "Fort Dix, NJ": "Joint Base McGuire-Dix-Lakehurst, NJ",
    "Aberdeen Proving Ground": "Aberdeen Proving Ground, MD",
    "Baumholder": "USAG Rheinland-Pfalz, Germany",
    "Camp Casey": "Camp Casey, South Korea",
    "Camp Humphreys": "Camp Humphreys, South Korea",
    "Camp Zama": "Camp Zama, Japan",
    "Carlisle Barracks": "Carlisle Barracks, PA",
    "Detroit Arsenal": "Detroit Arsenal, MI",
    "Dugway Proving Ground": "Dugway Proving Ground, UT",
    "Fort Belvoir": "Fort Belvoir, VA",
    "Fort Belvoir / NCR": "Fort Belvoir, VA",
    "Fort Benning": "Fort Benning, GA",
    "Fort Bliss": "Fort Bliss, TX",
    "Fort Bragg": "Fort Bragg, NC",
    "Fort Buchanan": "Fort Buchanan, PR",
    "Fort Campbell": "Fort Campbell, KY",
    "Fort Carson": "Fort Carson, CO",
    "Fort Cavazos": "Fort Hood, TX",
    "Fort Cavazos, TX": "Fort Hood, TX",
    "Fort Detrick": "Fort Detrick, MD",
    "Fort Drum": "Fort Drum, NY",
    "Fort Eisenhower": "Fort Gordon, GA",
    "Fort Eisenhower, GA": "Fort Gordon, GA",
    "Fort Gordon": "Fort Gordon, GA",
    "Fort Greely": "Fort Greely, AK",
    "Fort Gregg-Adams": "Fort Lee, VA",
    "Fort Gregg-Adams, VA": "Fort Lee, VA",
    "Fort Hamilton": "Fort Hamilton, NY",
    "Fort Hood": "Fort Hood, TX",
    "Fort Huachuca": "Fort Huachuca, AZ",
    "Fort Irwin": "Fort Irwin, CA",
    "Fort Jackson": "Fort Jackson, SC",
    "Fort Johnson": "Fort Polk, LA",
    "Fort Johnson, LA": "Fort Polk, LA",
    "Fort Knox": "Fort Knox, KY",
    "Fort Leavenworth": "Fort Leavenworth, KS",
    "Fort Lee": "Fort Lee, VA",
    "Fort Leonard Wood": "Fort Leonard Wood, MO",
    "Fort Liberty": "Fort Bragg, NC",
    "Fort Liberty, NC": "Fort Bragg, NC",
    "Fort McCoy": "Fort McCoy, WI",
    "Fort Meade": "Fort Meade, MD",
    "Fort Moore": "Fort Benning, GA",
    "Fort Moore, GA": "Fort Benning, GA",
    "Fort Myer": "Fort Myer, VA",
    "Fort Novosel": "Fort Rucker, AL",
    "Fort Novosel, AL": "Fort Rucker, AL",
    "Fort Polk": "Fort Polk, LA",
    "Fort Riley": "Fort Riley, KS",
    "Fort Rucker": "Fort Rucker, AL",
    "Fort Sam": "Fort Sam Houston, TX",
    "Fort Sam Houston": "Fort Sam Houston, TX",
    "Fort Shafter": "Fort Shafter, HI",
    "Fort Sill": "Fort Sill, OK",
    "Fort Stewart": "Fort Stewart, GA",
    "Fort Wainwright": "Fort Wainwright, AK",
    "Grafenwoehr": "USAG Bavaria, Germany",
    "Humphreys": "Camp Humphreys, South Korea",
    "Hunter Army Airfield": "Hunter Army Airfield, GA",
    "JB Myer-Henderson Hall": "Fort Myer, VA",
    "JBER": "Joint Base Elmendorf-Richardson, AK",
    "JBLM": "Joint Base Lewis-McChord, WA",
    "JBSA": "Joint Base San Antonio, TX",
    "JBSA Fort Sam Houston": "Fort Sam Houston, TX",
    "Joint Base Elmendorf-Richardson": "Joint Base Elmendorf-Richardson, AK",
    "Joint Base Langley-Eustis": "Joint Base Langley-Eustis, VA",
    "Joint Base Lewis-McChord": "Joint Base Lewis-McChord, WA",
    "Joint Base Myer-Henderson Hall": "Fort Myer, VA",
    "Joint Base Myer-Henderson Hall, VA": "Fort Myer, VA",
    "Joint Base San Antonio": "Joint Base San Antonio, TX",
    "Kaiserslautern": "USAG Rheinland-Pfalz, Germany",
    "Myer-Henderson Hall": "Fort Myer, VA",
    "Pentagon area": "Fort Myer, VA",
    "Picatinny Arsenal": "Picatinny Arsenal, NJ",
    "Presidio of Monterey": "Presidio of Monterey, CA",
    "Redstone Arsenal": "Redstone Arsenal, AL",
    "Rock Island Arsenal": "Rock Island Arsenal, IL",
    "Schofield Barracks": "Schofield Barracks, HI",
    "US Military Academy West Point": "US Military Academy West Point, NY",
    "USAG Bavaria": "USAG Bavaria, Germany",
    "USAG Humphreys": "Camp Humphreys, South Korea",
    "USAG Italy": "USAG Italy, Italy",
    "USAG Rheinland-Pfalz": "USAG Rheinland-Pfalz, Germany",
    "USAG Wiesbaden": "USAG Wiesbaden, Germany",
    "USMA": "US Military Academy West Point, NY",
    "Vicenza": "USAG Italy, Italy",
    "Vilseck": "USAG Bavaria, Germany",
    "West Point": "US Military Academy West Point, NY",
    "West Point, NY": "US Military Academy West Point, NY",
    "White Sands Missile Range": "White Sands Missile Range, NM",
    "Yuma Proving Ground": "Yuma Proving Ground, AZ",
}


def _canonical_installation_name(name: str) -> str | None:
    """Resolve aliases and return the traditional INSTALLATION_DATA key, or None."""
    cleaned = (name or "").strip()
    if not cleaned:
        return None
    if cleaned in INSTALLATION_DATA:
        return cleaned
    if cleaned in INSTALLATION_ALIASES:
        return INSTALLATION_ALIASES[cleaned]
    # Try appending state from data if user passed short name with comma state.
    for key in INSTALLATION_DATA:
        short = key.rsplit(", ", 1)[0]
        if cleaned.lower() == short.lower():
            return key
    return None


def get_installation_data(name: str) -> dict[str, Any] | None:
    """Return installation metadata dict for a traditional or aliased name."""
    canonical = _canonical_installation_name(name)
    if canonical is None:
        return None
    return INSTALLATION_DATA.get(canonical)


# ---------------------------------------------------------------------------
# Rich profiles for report generation (detailed housing/BAH/childcare fields)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class HousingMarket:
    on_post_pros: tuple[str, ...]
    on_post_cons: tuple[str, ...]
    off_post_areas: tuple[str, ...]
    avg_3br_rent_range: tuple[int, int]
    utility_note: str


@dataclass(frozen=True)
class InstallationProfile:
    key: str
    display_name: str
    short_name: str
    city: str
    state: str
    zip_code: str
    latitude: float
    longitude: float
    nearby_zip_codes: tuple[str, ...]
    bah_rates: dict[str, int]
    housing: HousingMarket
    school_districts: tuple[str, ...]
    spouse_employment_notes: tuple[str, ...]
    childcare_notes: tuple[str, ...]
    spouse_programs: tuple[str, ...]
    vehicle_registration_note: str
    climate_note: str
    commute_hotspots: tuple[str, ...]
    priority: Priority = "Medium"
    notes: str = ""


# Planning BAH fallbacks (with dependents) when bah_2026.json has no entry.
_BAH_DEFAULT: dict[str, int] = {
    "E-1": 1500, "E-2": 1500, "E-3": 1500, "E-4": 1500,
    "E-5": 1650, "E-6": 1800, "E-7": 1950, "E-8": 2100, "E-9": 2200,
    "W-1": 1850, "W-2": 1950, "W-3": 2050, "W-4": 2150, "W-5": 2250,
    "O-1": 1700, "O-2": 1850, "O-3": 2100, "O-4": 2300, "O-5": 2500,
    "O-6": 2650, "O-7+": 2800, "Other": 1650,
}

_BAH_BRAGG: dict[str, int] = {
    "E-1": 1428, "E-2": 1428, "E-3": 1428, "E-4": 1506, "E-5": 1653,
    "E-6": 1716, "E-7": 1836, "E-8": 1896, "E-9": 1944,
    "W-1": 1716, "W-2": 1836, "W-3": 1920, "W-4": 2016, "W-5": 2088,
    "O-1": 1716, "O-2": 1836, "O-3": 2016, "O-4": 2184, "O-5": 2328,
    "O-6": 2496, "O-7+": 2688, "Other": 1653,
}

_BAH_HOOD: dict[str, int] = {
    "E-1": 1380, "E-2": 1380, "E-3": 1380, "E-4": 1458, "E-5": 1542,
    "E-6": 1602, "E-7": 1710, "E-8": 1770, "E-9": 1818,
    "W-1": 1602, "W-2": 1710, "W-3": 1794, "W-4": 1878, "W-5": 1950,
    "O-1": 1602, "O-2": 1710, "O-3": 1878, "O-4": 2034, "O-5": 2166,
    "O-6": 2322, "O-7+": 2502, "Other": 1542,
}

_BAH_DRUM: dict[str, int] = {
    "E-1": 1332, "E-2": 1332, "E-3": 1332, "E-4": 1404, "E-5": 1548,
    "E-6": 1608, "E-7": 1716, "E-8": 1776, "E-9": 1824,
    "W-1": 1608, "W-2": 1716, "W-3": 1800, "W-4": 1884, "W-5": 1956,
    "O-1": 1608, "O-2": 1716, "O-3": 1884, "O-4": 2040, "O-5": 2172,
    "O-6": 2328, "O-7+": 2508, "Other": 1548,
}

_BAH_GORDON: dict[str, int] = {
    "E-1": 1356, "E-2": 1356, "E-3": 1356, "E-4": 1428, "E-5": 1572,
    "E-6": 1632, "E-7": 1740, "E-8": 1800, "E-9": 1848,
    "W-1": 1632, "W-2": 1740, "W-3": 1824, "W-4": 1908, "W-5": 1980,
    "O-1": 1632, "O-2": 1740, "O-3": 1908, "O-4": 2064, "O-5": 2196,
    "O-6": 2352, "O-7+": 2532, "Other": 1572,
}

_BAH_BLISS: dict[str, int] = {
    "E-1": 1665, "E-2": 1665, "E-3": 1665, "E-4": 1665, "E-5": 1809,
    "E-6": 2148, "E-7": 2172, "E-8": 2187, "E-9": 2241,
    "W-1": 2169, "W-2": 2178, "W-3": 2205, "W-4": 2256, "W-5": 2334,
    "O-1": 1857, "O-2": 2145, "O-3": 2202, "O-4": 2352, "O-5": 2466,
    "O-6": 2484, "O-7+": 2496, "Other": 1809,
}

# Per-installation rent planning ranges (low, high) for 3BR off-post.
_RENT_BY_PRIORITY: dict[Priority, tuple[int, int]] = {
    "High": (1300, 1750),
    "Medium": (1200, 1650),
    "Low": (1000, 1400),
}

# Geo and extended report fields for installations with hand-tuned report data.
_RICH_PROFILE_EXTENSIONS: dict[str, dict[str, Any]] = {
    "Fort Bragg, NC": {
        "key": "bragg",
        "city": "Fayetteville",
        "zip_code": "28307",
        "latitude": 35.1410,
        "longitude": -79.0060,
        "nearby_zip_codes": ("28303", "28348", "28390", "28376"),
        "bah_rates": _BAH_BRAGG,
        "avg_3br_rent_range": (1450, 1850),
        "off_post_areas": (
            "Hope Mills (28348) & Spring Lake (28390) — strong BAH value, 15–25 min commute",
            "Fayetteville north side (28303) — more inventory, watch school zones",
            "Raeford (28376) — quieter, longer commute, often lower rent",
        ),
        "utility_note": "Plan $150–$250/mo for electric/water off-post in summer months.",
        "spouse_employment_notes": (
            "Cape Fear Valley Health, Cumberland County Schools, and retail along Skibo Rd hire steadily",
            "Remote work viable with good broadband in Hope Mills / Fayetteville suburbs",
            "NC teaching license reciprocity available — start licensure packet early (4–8 weeks typical)",
        ),
        "childcare_notes": (
            "Fort Bragg CDC waitlists: 30–90 days for school-age; infant/toddler slots often 60–120 days",
            "Family Child Care (FCC) homes in Hope Mills/Spring Lake often have 2–4 week openings",
            "Submit CDC request (DD Form 2606) same day orders drop; ask ACS for current wait times",
        ),
        "spouse_programs": (
            "MSEP and My Career Advancement Account (MyCAA) for licensure/certification costs",
            "Hiring Our Heroes fellowship and ACS spouse employment workshops at Soldier Support Center",
        ),
        "vehicle_registration_note": "NC DMV: register within 30 days of establishing residency; bring title, insurance, and military orders.",
        "climate_note": "Mild winters; summer humidity drives higher AC costs off-post.",
        "commute_hotspots": ("All-American Fwy", "Bragg Blvd", "Murchison Rd gate"),
    },
    "Fort Hood, TX": {
        "key": "hood",
        "city": "Killeen",
        "zip_code": "76544",
        "latitude": 31.1349,
        "longitude": -97.7756,
        "nearby_zip_codes": ("76541", "76548", "76522", "76542"),
        "bah_rates": _BAH_HOOD,
        "avg_3br_rent_range": (1250, 1650),
        "off_post_areas": (
            "Killeen east side (76541) — most inventory, verify school zones",
            "Harker Heights (76548) — family-friendly, 10–20 min to main gates",
            "Copperas Cove (76522) — quieter, strong BAH value, 15–25 min commute",
        ),
        "utility_note": "Plan $175–$275/mo for electric/water off-post in peak summer AC months.",
        "spouse_employment_notes": (
            "Carl R. Darnall Army Medical Center, Killeen ISD, and on-post NAF roles",
            "Retail and service hiring along Veterans Memorial Blvd and Market Heights",
            "Remote work viable with good broadband in Harker Heights / Copperas Cove (200+ Mbps common)",
        ),
        "childcare_notes": (
            "Fort Hood CDC waitlists: 45–90 days for infants; school-age often 30–60 days in summer PCS surge",
            "FCC providers in Harker Heights and Copperas Cove are the fastest backup",
            "Submit CDC paperwork at in-processing; priority categories apply for dual-military and deployed sponsors",
        ),
        "spouse_programs": (
            "ACS Employment Readiness Program and Fort Hood Spouse Employment Center",
            "MSEP partners include CRDAMC and Killeen ISD for expedited hiring",
        ),
        "vehicle_registration_note": "Texas: register within 30 days; no state income tax but property tax applies to vehicles in some counties.",
        "climate_note": "Hot summers drive higher AC costs off-post; mild winters rarely spike heating bills.",
        "commute_hotspots": ("US-190", "Trimmier Rd", "Clear Creek Rd gate"),
    },
    "Fort Bliss, TX": {
        "key": "bliss",
        "city": "El Paso",
        "zip_code": "79916",
        "latitude": 31.8130,
        "longitude": -106.4220,
        "nearby_zip_codes": ("79925", "79928", "79938", "79934"),
        "bah_rates": _BAH_BLISS,
        "avg_3br_rent_range": (1250, 1650),
        "off_post_areas": (
            "Northeast El Paso (79925) — 10–20 min to main gates, strong school options",
            "Horizon City / East El Paso (79928) — newer builds, fenced yards common",
            "West El Paso / Sunland Park corridor (79922) — verify commute to unit area",
        ),
        "utility_note": "Plan $120–$200/mo electric in summer; water is modest in desert climate.",
        "spouse_employment_notes": (
            "William Beaumont Army Medical Center and Fort Bliss NAF health roles hire steadily",
            "El Paso Children's Hospital and Las Palmas Del Sol hire nurses with TX endorsement",
            "Federal civilian roles at Bliss and border agencies post on USAJOBS year-round",
        ),
        "childcare_notes": (
            "Fort Bliss CDC waitlists: 30–90 days school-age; infant/toddler often 60–120 days",
            "FCC homes in Northeast El Paso and Horizon City often open in 2–4 weeks",
            "Submit DD Form 2606 before departure — summer PCS surge adds 30+ days if delayed",
        ),
        "spouse_programs": (
            "ACS Employment Readiness and Fort Bliss Spouse Employment Center",
            "MSEP partners include WBAMC and EPISD for expedited hiring",
            "MyCAA for spouse licensure and certification in healthcare/education fields",
        ),
        "vehicle_registration_note": "Texas: register within 30 days; no state income tax but vehicle property tax applies.",
        "climate_note": "Desert heat drives summer AC costs; monsoon season (Jul–Sep) can disrupt commutes.",
        "commute_hotspots": ("US-54", "Loop 375", "Cassidy Rd / Spur 601 gates"),
    },
    "Fort Drum, NY": {
        "key": "drum",
        "city": "Watertown",
        "zip_code": "13602",
        "latitude": 44.0520,
        "longitude": -75.7890,
        "nearby_zip_codes": ("13637", "13619", "13601", "13612"),
        "bah_rates": _BAH_DRUM,
        "avg_3br_rent_range": (1300, 1700),
        "off_post_areas": (
            "Evans Mills / Le Ray (13637) — shortest commute, moderate rents",
            "Carthage (13619) — family-friendly, 15–20 min to post",
            "Watertown (13601) — most inventory & services, verify commute tolerance",
        ),
        "utility_note": "Budget higher winter heating ($200–$350/mo peak) off-post.",
        "spouse_employment_notes": (
            "Samaritan Medical Center, Jefferson County schools, and on-post NAF roles",
            "NY nursing endorsement: 4–8 weeks typical; temporary permit possible in 2–3 weeks",
            "Remote work works well; winter travel for in-person roles needs planning",
        ),
        "childcare_notes": (
            "Fort Drum CDC infant/toddler waitlists routinely 3–6 months — submit DD 2606 immediately",
            "FCC homes in Evans Mills/Le Ray often have 2–4 week openings as parallel track",
            "Peak summer PCS surge can add 30+ days to any childcare slot",
        ),
        "spouse_programs": (
            "ACS Spouse Employment and Fort Drum Military Spouse Preference for on-post NAF roles",
            "MyCAA covers nursing CEU/certification costs where eligible",
        ),
        "vehicle_registration_note": "NY DMV: register within 30 days; emissions/safety inspection required.",
        "climate_note": "Lake-effect snow and heating costs are real budget factors.",
        "commute_hotspots": ("Route 11", "Route 26", "California Rd gate"),
    },
    "Fort Gordon, GA": {
        "key": "gordon",
        "city": "Augusta",
        "zip_code": "30905",
        "latitude": 33.4268,
        "longitude": -82.1460,
        "nearby_zip_codes": ("30907", "30809", "30909", "30813"),
        "bah_rates": _BAH_GORDON,
        "avg_3br_rent_range": (1350, 1750),
        "off_post_areas": (
            "Evans / Martinez (30809) — popular with military families, 15–20 min commute",
            "Grovetown (30813) — newer construction, verify gate drive time",
            "West Augusta (30907) — more inventory and services, watch school zones",
        ),
        "utility_note": "Plan $150–$225/mo for electric/water off-post in summer months.",
        "spouse_employment_notes": (
            "AU Health, Columbia County schools, and Augusta cyber/defense contractors hire steadily",
            "Remote work viable with strong broadband in Evans and Grovetown",
            "GA teaching/nursing license reciprocity available — start packet early (4–6 weeks typical)",
        ),
        "childcare_notes": (
            "Fort Gordon CDC waitlists: 30–75 days depending on age group; summer PCS surge tightens slots",
            "FCC providers in Evans/Martinez corridor are fastest backup for toddlers",
            "Submit CDC request at in-processing; dual-military families may qualify for priority",
        ),
        "spouse_programs": (
            "ACS Employment Readiness and Augusta cyber corridor MSEP hiring events",
            "MyCAA for spouse licensure and certification in healthcare/education fields",
        ),
        "vehicle_registration_note": "GA DMV: register within 30 days; TAVT applies to new residents registering vehicles.",
        "climate_note": "Hot, humid summers drive AC costs; mild winters with occasional ice on bridges.",
        "commute_hotspots": ("Gordon Hwy", "Jimmie Dyess Pkwy", "Gate 1 / Gate 3 corridors"),
    },
    "Fort Campbell, KY": {
        "key": "campbell",
        "city": "Clarksville",
        "zip_code": "42223",
        "latitude": 36.6530,
        "longitude": -87.4600,
        "nearby_zip_codes": ("37042", "37040", "42223", "42262"),
        "bah_rates": _BAH_DEFAULT,
        "avg_3br_rent_range": (1350, 1750),
        "off_post_areas": (
            "Clarksville, TN (37042) — most inventory, verify TN vs KY school zoning",
            "Oak Grove, KY (42223) — shorter commute, quieter neighborhoods",
            "Hopkinsville, KY (42240) — lower rent, 20–25 min to gates",
        ),
        "utility_note": "Plan $140–$220/mo electric; TN side inventory turns faster in summer PCS.",
        "spouse_employment_notes": (
            "Blanchfield Army Community Hospital, Clarksville-Montgomery County Schools, and trades contractors on TN side",
            "KY/TN licensure differs for trades and healthcare — verify state before applying",
            "Gate traffic on Madam Walker peaks with 101st cycles — factor spouse interview windows",
        ),
        "childcare_notes": (
            "Fort Campbell CDC waitlists: 30–90 days school-age; infant/toddler 60–120 days in summer surge",
            "FCC homes in Oak Grove and Clarksville often open in 2–4 weeks",
            "IEP transfers require district registrar meeting within 10 school days — book before lease signing",
        ),
        "spouse_programs": (
            "ACS Employment Readiness and Fort Campbell Spouse Employment Center",
            "MSEP at Blanchfield and Clarksville-Montgomery County Schools",
            "MyCAA for trades certification and licensure costs",
        ),
        "vehicle_registration_note": "TN or KY registration depending on residence — 30-day rule applies in both states.",
        "climate_note": "Mild winters; humid summers; KY/TN line affects school district and state tax.",
        "commute_hotspots": ("Madam Walker Blvd", "Fort Campbell Blvd", "Wilma Rudolph Blvd"),
    },
    "Fort Benning, GA": {
        "key": "benning",
        "city": "Columbus",
        "zip_code": "31905",
        "latitude": 32.3540,
        "longitude": -84.9680,
        "nearby_zip_codes": ("31909", "31907", "36867", "31820"),
        "bah_rates": _BAH_DEFAULT,
        "avg_3br_rent_range": (1250, 1650),
        "off_post_areas": (
            "Columbus north / Midland (31909) — strong Muscogee County schools, 15–20 min",
            "Phenix City, AL (36867) — verify GA school zoning before signing AL lease",
            "Upatoi / east Columbus (31820) — quieter, longer commute",
        ),
        "utility_note": "Plan $150–$240/mo electric in summer humidity; AL leases need GA school check.",
        "spouse_employment_notes": (
            "Muscogee County Schools, Piedmont Columbus Regional, and Fort Benning NAF roles",
            "Heavy training tempo — spouse interviews best scheduled after 0900 to avoid graduation traffic",
            "MyCAA strong for spouse continuing education while sponsor in MCoE pipeline",
        ),
        "childcare_notes": (
            "Fort Benning CDC waitlists: 45–90 days infants; school-age 30–60 days",
            "EFMP coordination must transfer before housing lock — delays narrow on-post options",
            "IEP continuity requires Muscogee County registrar packet within first 10 school days",
        ),
        "spouse_programs": (
            "ACS Employment Readiness and Fort Benning Spouse Employment Center",
            "MSEP at Piedmont and Muscogee County Schools",
        ),
        "vehicle_registration_note": "GA DMV: register within 30 days; AL residents working in GA still need school zoning clarity.",
        "climate_note": "Hot, humid summers; ice rare but training tempo drives gate delays year-round.",
        "commute_hotspots": ("US-280", "Victory Drive", "Interstate 185 gate corridors"),
    },
    "Fort Stewart, GA": {
        "key": "stewart",
        "city": "Hinesville",
        "zip_code": "31314",
        "latitude": 31.8690,
        "longitude": -81.6080,
        "nearby_zip_codes": ("31313", "31324", "31326", "31328"),
        "bah_rates": _BAH_DEFAULT,
        "avg_3br_rent_range": (1200, 1550),
        "off_post_areas": (
            "Hinesville (31313) — shortest commute, Liberty County schools",
            "Richmond Hill (31324) — stronger schools, 20–25 min, higher rent",
            "Pooler / west Savannah (31322) — more inventory, verify commute tolerance",
        ),
        "utility_note": "Plan $160–$260/mo electric in summer humidity; hurricane season affects insurance off-post.",
        "spouse_employment_notes": (
            "Liberty County Schools, Winn Army Community Hospital NAF, and Savannah retail corridor",
            "Retail and hospitality hire fast — part-time bridge roles common within 2–4 weeks",
        ),
        "childcare_notes": (
            "Fort Stewart CDC infant waitlists: 60–120 days — submit DD 2606 before departure",
            "FCC in Hinesville is fastest path for infant + preschool combo",
            "Hurricane season (Jun–Nov) can delay movers — build 5-day buffer into TLE plan",
        ),
        "spouse_programs": (
            "ACS Employment Readiness and Stewart Spouse Employment Center",
            "MSEP at Winn ACH and Liberty County Schools",
        ),
        "vehicle_registration_note": "GA DMV: register within 30 days; coastal county insurance rates vary.",
        "climate_note": "Coastal humidity and hurricane season affect utilities and insurance.",
        "commute_hotspots": ("GA-119", "US-84", "Gate 1 / Gate 2 corridors"),
    },
    "Fort Sill, OK": {
        "key": "sill",
        "city": "Lawton",
        "zip_code": "73503",
        "latitude": 34.6690,
        "longitude": -98.4010,
        "nearby_zip_codes": ("73505", "73507", "73527", "73501"),
        "bah_rates": _BAH_DEFAULT,
        "avg_3br_rent_range": (950, 1300),
        "off_post_areas": (
            "Lawton west (73505) — most inventory, Lawton Public Schools",
            "Cache (73527) — quieter, 10–15 min, verify tornado shelter disclosure",
            "Medicine Park (73557) — scenic, limited inventory, longer commute",
        ),
        "utility_note": "Plan $120–$200/mo electric; wind/hail affect off-post insurance — get shelter clause in lease.",
        "spouse_employment_notes": (
            "Lawton Public Schools, Comanche County Memorial Hospital, and on-post NAF retail",
            "Retail and service roles often hire within 2–4 weeks — good bridge for part-time income",
        ),
        "childcare_notes": (
            "Fort Sill CDC infant/toddler waitlists: 45–90 days; school-age faster in off-peak PCS",
            "FCC in Lawton west side often has 2–3 week openings",
            "Ask landlords about tornado shelter or interior safe room — especially with infants",
        ),
        "spouse_programs": (
            "ACS Employment Readiness and Fort Sill Spouse Employment Center",
            "MSEP at Comanche County Memorial and Lawton PSD",
        ),
        "vehicle_registration_note": "OK DMV: register within 30 days; lower cost of living but verify renter's insurance for hail.",
        "climate_note": "Tornado and hail season — verify shelter access and renter's insurance riders.",
        "commute_hotspots": ("Sheridan Road", "Fort Sill Blvd", "Quanah Rd gate"),
    },
    "Joint Base Lewis-McChord, WA": {
        "key": "jblm",
        "city": "Lakewood",
        "zip_code": "98433",
        "latitude": 47.1120,
        "longitude": -122.5860,
        "nearby_zip_codes": ("98439", "98327", "98374", "98597"),
        "bah_rates": _BAH_DEFAULT,
        "avg_3br_rent_range": (1850, 2400),
        "off_post_areas": (
            "DuPont (98327) — walkable to Madigan, inventory turns in days in summer",
            "Lakewood / Tillicum (98439) — more inventory, verify I-5 commute",
            "Yelm (98597) — lower rent, 25–35 min, Yelm Community Schools",
        ),
        "utility_note": "Plan $180–$280/mo electric; rain drives mold risk — inspect ventilation before signing.",
        "spouse_employment_notes": (
            "Madigan Army Medical Center, MultiCare, and Pierce County school districts",
            "WA nursing endorsement: 4–8 weeks; temp permit possible — start before departure",
            "Tight rental market — spouse job search should parallel housing, not follow it",
        ),
        "childcare_notes": (
            "JBLM CDC waitlists: 60–120 days infants; preschool 30–60 days in PCS surge",
            "FCC in DuPont and Lakewood often faster than CDC for preschoolers",
            "Rain and traffic compound commute — childcare near lease address reduces daily risk",
        ),
        "spouse_programs": (
            "ACS Employment Readiness and JBLM Spouse Employment Center",
            "MSEP at Madigan and Clover Park School District",
            "MyCAA for nursing CEU and certification",
        ),
        "vehicle_registration_note": "WA DOL: register within 30 days; no state income tax but rental market is competitive.",
        "climate_note": "Rain 8+ months — budget dehumidifier and mold prevention; winter dark affects morale.",
        "commute_hotspots": ("I-5", "SR-507", "DuPont gate / McChord Field gates"),
    },
    "Fort Belvoir, VA": {
        "key": "belvoir",
        "city": "Fort Belvoir",
        "zip_code": "22060",
        "latitude": 38.7189,
        "longitude": -77.1543,
        "nearby_zip_codes": ("22079", "22150", "22191", "22315"),
        "bah_rates": {
            "E-1": 3096, "E-2": 3096, "E-3": 3096, "E-4": 3096, "E-5": 3132,
            "E-6": 3759, "E-7": 3855, "E-8": 3957, "E-9": 4128,
            "W-1": 3780, "W-2": 3894, "W-3": 4023, "W-4": 4167, "W-5": 4350,
            "O-1": 3213, "O-2": 3753, "O-3": 4020, "O-4": 4410, "O-5": 4692,
            "O-6": 4731, "O-7+": 4770, "Other": 3132,
        },
        "avg_3br_rent_range": (2400, 3200),
        "off_post_areas": (
            "Lorton (22079) — strong value for Belvoir gates, Fairfax schools",
            "Springfield / Franconia (22150) — Metro access, higher rent",
            "Woodbridge (22191) — more inventory, Prince William schools, longer I-95 run",
        ),
        "utility_note": "Plan $180–$280/mo electric in summer; NCR rents often exclude utilities — read lease carefully.",
        "spouse_employment_notes": (
            "Inova, Fairfax County Public Schools, and federal contractors along the Beltway hire steadily",
            "DC/NoVA remote and hybrid roles common — verify broadband before signing",
            "VA teaching license and hospital credentialing: start packets before departure",
        ),
        "childcare_notes": (
            "Belvoir CDC waitlists often 60–120 days for infants; school-age shorter in off-peak months",
            "FCC and off-post centers in Lorton/Springfield fill with summer PCS surge",
            "Submit DD Form 2606 as soon as orders drop",
        ),
        "spouse_programs": (
            "ACS Employment Readiness at Fort Belvoir",
            "MSEP and MyCAA for licensure costs",
        ),
        "vehicle_registration_note": "VA DMV: register within 30 days of establishing residency; bring title, insurance, and orders.",
        "climate_note": "Humid summers drive AC costs; mild winters; I-95 traffic is the real daily cost.",
        "commute_hotspots": ("I-95", "Fairfax County Pkwy", "Telegraph Rd / Belvoir gates"),
    },
    "Fort Myer, VA": {
        "key": "myer",
        "city": "Arlington",
        "zip_code": "22211",
        "latitude": 38.8806,
        "longitude": -77.0806,
        "nearby_zip_codes": ("22202", "22301", "22204", "20024"),
        "bah_rates": {
            "E-1": 3096, "E-2": 3096, "E-3": 3096, "E-4": 3096, "E-5": 3132,
            "E-6": 3759, "E-7": 3855, "E-8": 3957, "E-9": 4128,
            "W-1": 3780, "W-2": 3894, "W-3": 4023, "W-4": 4167, "W-5": 4350,
            "O-1": 3213, "O-2": 3753, "O-3": 4020, "O-4": 4410, "O-5": 4692,
            "O-6": 4731, "O-7+": 4770, "Other": 3132,
        },
        "avg_3br_rent_range": (2800, 3800),
        "off_post_areas": (
            "Pentagon City / Crystal City (22202) — Metro to Myer/Pentagon, premium rent",
            "Alexandria (22301) — strong schools options, Metro Blue/Yellow",
            "Arlington neighborhoods — walk/transit tradeoffs, inventory tight",
        ),
        "utility_note": "High rent market; utilities often separate — budget $150–$250/mo off-post.",
        "spouse_employment_notes": (
            "Pentagon contractors, Arlington schools, and federal agencies dominate hiring",
            "Metro access multiplies spouse job options across DC/MD/VA",
            "Security clearance jobs common — allow onboarding time",
        ),
        "childcare_notes": (
            "On-post CDC limited; off-post Arlington/Alexandria waitlists are long",
            "Start childcare search before arrival; deposit competition is real",
            "Submit DD Form 2606 early; ask ACS for current NCR wait estimates",
        ),
        "spouse_programs": (
            "ACS at Joint Base Myer–Henderson Hall",
            "MSEP and federal spouse hiring paths across the NCR",
        ),
        "vehicle_registration_note": "VA or DC registration rules depend on residency; many choose VA for lower insurance — confirm with finance/legal.",
        "climate_note": "Humid summers; snow events rare but cripple I-395; Metro reliability varies by line.",
        "commute_hotspots": ("I-395", "GW Parkway", "Metro Blue/Yellow", "14th St Bridge"),
    },
    "Pentagon / National Capital Region, VA": {
        "key": "pentagon",
        "city": "Arlington",
        "zip_code": "22202",
        "latitude": 38.8719,
        "longitude": -77.0563,
        "nearby_zip_codes": ("22202", "22301", "22204", "20024"),
        "bah_rates": {
            "E-1": 3096, "E-2": 3096, "E-3": 3096, "E-4": 3096, "E-5": 3132,
            "E-6": 3759, "E-7": 3855, "E-8": 3957, "E-9": 4128,
            "W-1": 3780, "W-2": 3894, "W-3": 4023, "W-4": 4167, "W-5": 4350,
            "O-1": 3213, "O-2": 3753, "O-3": 4020, "O-4": 4410, "O-5": 4692,
            "O-6": 4731, "O-7+": 4770, "Other": 3132,
        },
        "avg_3br_rent_range": (2800, 3800),
        "off_post_areas": (
            "Pentagon City / Crystal City — shortest Metro hop to the building",
            "Alexandria — more family inventory than Arlington core",
            "Springfield / Franconia — lower rent, longer bridge commute",
        ),
        "utility_note": "NCR rents are high; confirm utilities, parking, and condo fees before signing.",
        "spouse_employment_notes": (
            "Federal and contractor hiring across DC/MD/VA — clearance timelines matter",
            "Metro-accessible leases expand dual-income options",
            "Same planning pattern as Fort Myer / JB Myer–Henderson Hall families",
        ),
        "childcare_notes": (
            "No large on-post CDC at the Pentagon itself — plan off-post or Myer-area care",
            "Arlington/Alexandria waitlists are competitive year-round",
            "Lock care before first duty day if both adults work",
        ),
        "spouse_programs": (
            "Use ACS at Joint Base Myer–Henderson Hall for NCR spouse employment support",
            "MSEP and federal spouse pathways across the National Capital Region",
        ),
        "vehicle_registration_note": "Confirm VA vs DC vs MD residency for registration and insurance before buying a long commute.",
        "climate_note": "Same NCR climate as Fort Myer; traffic and Metro reliability drive daily quality of life.",
        "commute_hotspots": ("I-395", "14th St Bridge", "Metro Pentagon station", "Route 27"),
    },
}

_ON_POST_PROS = (
    "No rent out-of-pocket when assigned — BAH absorbed by housing",
    "Short commute and maintenance handled on-post",
    "Utilities often included in government housing",
)
_ON_POST_CONS = (
    "Waitlists spike before summer PCS season",
    "Limited floor-plan and neighborhood choice",
    "Older housing stock in some areas",
)


def _build_profile(canonical_name: str) -> InstallationProfile:
    """Build an InstallationProfile from INSTALLATION_DATA plus optional rich extensions."""
    data = INSTALLATION_DATA[canonical_name]
    rich = _RICH_PROFILE_EXTENSIONS.get(canonical_name, {})
    short_name = canonical_name.rsplit(", ", 1)[0]
    state = data["state"].split("/")[0]  # KY/TN → KY for profile state field
    priority: Priority = data["priority"]
    rent = rich.get("avg_3br_rent_range", _RENT_BY_PRIORITY[priority])

    major_areas = data["major_areas"]
    off_post = rich.get(
        "off_post_areas",
        tuple(f"{area} — verify school zoning and gate commute" for area in major_areas),
    )

    return InstallationProfile(
        key=rich.get("key", short_name.lower().replace(" ", "-").replace("joint-base-", "jb-")),
        display_name=canonical_name,
        short_name=short_name,
        city=rich.get("city", major_areas[0] if major_areas else ""),
        state=state,
        zip_code=rich.get("zip_code", ""),
        latitude=rich.get("latitude", 0.0),
        longitude=rich.get("longitude", 0.0),
        nearby_zip_codes=rich.get("nearby_zip_codes", ()),
        bah_rates=rich.get("bah_rates", _BAH_DEFAULT),
        housing=HousingMarket(
            on_post_pros=_ON_POST_PROS,
            on_post_cons=_ON_POST_CONS,
            off_post_areas=off_post,
            avg_3br_rent_range=rent,
            utility_note=rich.get(
                "utility_note",
                "Estimate $150–$250/mo utilities off-post; climate drives variance.",
            ),
        ),
        school_districts=tuple(data["school_districts"]),
        spouse_employment_notes=rich.get(
            "spouse_employment_notes",
            (
                f"Check hospital systems, school districts, and employers near {major_areas[0]}",
                "ACS Employment Readiness and MSEP available on-post",
            ),
        ),
        childcare_notes=rich.get(
            "childcare_notes",
            (
                "Submit DD Form 2606 same day orders drop",
                "FCC homes are typically faster than CDC for school-age and infants",
                "Contact ACS for current CDC waitlist estimates",
            ),
        ),
        spouse_programs=rich.get(
            "spouse_programs",
            (
                "ACS Employment Readiness Program and MSEP at most installations",
                "MyCAA for eligible spouse licensure and certification costs",
            ),
        ),
        vehicle_registration_note=rich.get(
            "vehicle_registration_note",
            f"Register vehicles within 30 days of establishing residency in {state}.",
        ),
        climate_note=rich.get("climate_note", data["notes"]),
        commute_hotspots=rich.get(
            "commute_hotspots",
            (data["commute_notes"][:80] + "…" if len(data["commute_notes"]) > 80 else data["commute_notes"],),
        ),
        priority=priority,
        notes=data["notes"],
    )


INSTALLATIONS: dict[str, InstallationProfile] = {
    name: _build_profile(name) for name in INSTALLATION_DATA
}

DEFAULT_INSTALLATION = InstallationProfile(
    key="generic",
    display_name="Your gaining installation",
    short_name="gaining installation",
    city="",
    state="",
    zip_code="",
    latitude=0.0,
    longitude=0.0,
    nearby_zip_codes=(),
    bah_rates=_BAH_DEFAULT,
    housing=HousingMarket(
        on_post_pros=_ON_POST_PROS[:2],
        on_post_cons=_ON_POST_CONS[:2],
        off_post_areas=(
            "Start research within a 30-minute gate-to-door commute",
            "Compare 3-bedroom rent to BAH before signing",
        ),
        avg_3br_rent_range=(1400, 1800),
        utility_note="Estimate utilities separately — they often decide on-post vs off-post value.",
    ),
    school_districts=("Verify district boundaries before lease signing",),
    spouse_employment_notes=(
        "Check local hospital systems, school districts, and remote-work feasibility",
    ),
    childcare_notes=(
        "Contact installation ACS for current CDC waitlist estimates",
        "FCC homes are typically the fastest backup for infants and toddlers",
    ),
    spouse_programs=(
        "ACS Employment Readiness Program and MSEP at most installations",
        "MyCAA for eligible spouse licensure and certification costs",
    ),
    vehicle_registration_note="Register vehicles within 30 days of establishing residency in the new state.",
    climate_note="Local weather affects utility costs and commute reliability.",
    commute_hotspots=("Main gate corridors at peak duty hours",),
    priority="Medium",
    notes="Generic fallback — add this installation to INSTALLATION_DATA for tailored guidance.",
)


# Approximate CONUS driving distances for DITY/PPM planning (miles, one-way).
MOVE_ROUTE_MILES: dict[tuple[str, str], int] = {
    ("Fort Hood, TX", "Fort Bragg, NC"): 1180,
    ("Fort Bragg, NC", "Fort Hood, TX"): 1180,
    ("Fort Gordon, GA", "Fort Drum, NY"): 980,
    ("Fort Drum, NY", "Fort Gordon, GA"): 980,
    ("Fort Bragg, NC", "Fort Drum, NY"): 780,
    ("Fort Drum, NY", "Fort Bragg, NC"): 780,
    ("Fort Hood, TX", "Fort Drum, NY"): 1580,
    ("Fort Drum, NY", "Fort Hood, TX"): 1580,
    ("Fort Gordon, GA", "Fort Bragg, NC"): 320,
    ("Fort Bragg, NC", "Fort Gordon, GA"): 320,
    ("Fort Hood, TX", "Fort Gordon, GA"): 860,
    ("Fort Gordon, GA", "Fort Hood, TX"): 860,
    ("Fort Bragg, NC", "Fort Bliss, TX"): 1680,
    ("Fort Bliss, TX", "Fort Bragg, NC"): 1680,
    ("Fort Bragg, NC", "Fort Benning, GA"): 280,
    ("Fort Benning, GA", "Fort Bragg, NC"): 280,
    ("Fort Bragg, NC", "Fort Campbell, KY"): 520,
    ("Fort Campbell, KY", "Fort Bragg, NC"): 520,
    ("Fort Hood, TX", "Fort Bliss, TX"): 620,
    ("Fort Bliss, TX", "Fort Hood, TX"): 620,
    ("Joint Base Lewis-McChord, WA", "Fort Hood, TX"): 2100,
    ("Fort Hood, TX", "Joint Base Lewis-McChord, WA"): 2100,
    ("Fort Benning, GA", "Fort Campbell, KY"): 380,
    ("Fort Campbell, KY", "Fort Benning, GA"): 380,
    ("Fort Bliss, TX", "Joint Base Lewis-McChord, WA"): 1850,
    ("Joint Base Lewis-McChord, WA", "Fort Bliss, TX"): 1850,
    ("Fort Leavenworth, KS", "Fort Bragg, NC"): 1050,
    ("Fort Bragg, NC", "Fort Leavenworth, KS"): 1050,
    ("Fort Stewart, GA", "Fort Sill, OK"): 1150,
    ("Fort Sill, OK", "Fort Stewart, GA"): 1150,
    ("Fort Hood, TX", "Fort Benning, GA"): 880,
    ("Fort Benning, GA", "Fort Hood, TX"): 880,
}


def _coords_for_installation(label: str) -> tuple[float, float] | None:
    """Lat/lon for known posts (rich profiles + common-post overrides)."""
    canonical = _canonical_installation_name(label) or label
    if canonical in INSTALLATIONS:
        p = INSTALLATIONS[canonical]
        if p.latitude and p.longitude:
            return float(p.latitude), float(p.longitude)
    # Posts that appear on the form but lack a full rich profile
    overrides: dict[str, tuple[float, float]] = {
        "Fort Sam Houston, TX": (29.4577, -98.4396),
        "Joint Base San Antonio, TX": (29.4498, -98.5040),
        "Camp Atterbury, IN": (39.3517, -86.0300),
        "Dugway Proving Ground, UT": (40.1999, -112.9352),
        "Fort Knox, KY": (37.8915, -85.9747),
        "Fort Riley, KS": (39.0558, -96.7850),
        "Fort Carson, CO": (38.7375, -104.7886),
        "Fort Leavenworth, KS": (39.3456, -94.9186),
        "Fort Polk, LA": (31.0502, -93.2066),
        "Fort Irwin, CA": (35.2628, -116.6847),
        "Fort Huachuca, AZ": (31.5552, -110.3495),
        "Fort Wainwright, AK": (64.8378, -147.7164),
        "Redstone Arsenal, AL": (34.6842, -86.6539),
        "White Sands Missile Range, NM": (32.3865, -106.4880),
        "Aberdeen Proving Ground, MD": (39.4723, -76.1305),
        "Fort Meade, MD": (39.1043, -76.7430),
        "Fort Leonard Wood, MO": (37.7400, -92.1270),
        "Fort Jackson, SC": (34.0194, -80.8900),
        "Fort Eustis, VA": (37.1624, -76.5788),
        "Fort Lee, VA": (37.2350, -77.3328),
        "Camp Humphreys, South Korea": (36.9681, 127.0334),
        "Camp Casey, South Korea": (37.9219, 127.0547),
        "USAG Bavaria, Germany": (49.6986, 11.7744),
        "USAG Wiesbaden, Germany": (50.0497, 8.3256),
        "USAG Rheinland-Pfalz, Germany": (49.4369, 7.6000),
        "Camp Zama, Japan": (35.4900, 139.3950),
        "Schofield Barracks, HI": (21.4950, -158.0620),
        "Fort Shafter, HI": (21.3456, -157.8860),
        "Fort Buchanan, PR": (18.4135, -66.1220),
    }
    return overrides.get(canonical)


def _haversine_miles(lat1: float, lon1: float, lat2: float, lon2: float) -> int:
    """Great-circle distance in statute miles (planning estimate; TMO has road miles)."""
    import math

    r = 3958.8  # Earth radius miles
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    # Road miles ≈ 1.2× great-circle for CONUS planning
    return max(50, int(round(2 * r * math.asin(math.sqrt(a)) * 1.18)))


def build_move_context(current_label: str, gaining_label: str) -> dict:
    """Return move-distance context for DITY/TLE planning."""
    current = _canonical_installation_name(current_label) or current_label
    gaining = _canonical_installation_name(gaining_label) or gaining_label
    miles = MOVE_ROUTE_MILES.get((current, gaining)) or MOVE_ROUTE_MILES.get(
        (gaining, current)
    )
    distance_source = "known_route"
    if miles is None:
        c1, c2 = _coords_for_installation(current), _coords_for_installation(gaining)
        if c1 and c2:
            miles = _haversine_miles(c1[0], c1[1], c2[0], c2[1])
            distance_source = "estimated_from_coordinates"
    if miles is None:
        return {
            "origin": current_label,
            "destination": gaining_label,
            "approximate_miles_one_way": None,
            "distance_source": "unknown",
            "dity_planning_note": (
                "Verify distance with TMO; for CONUS moves over 500 miles, "
                "full or partial DITY often nets $1,500–5,000 after expenses."
            ),
        }
    driving_days = max(2, round(miles / 500))
    estimate_note = ""
    if distance_source == "estimated_from_coordinates":
        estimate_note = (
            " (planning estimate from post locations — confirm road miles with TMO)."
        )
    return {
        "origin": current_label,
        "destination": gaining_label,
        "approximate_miles_one_way": miles,
        "estimated_driving_days": driving_days,
        "distance_source": distance_source,
        "dity_planning_note": (
            f"~{miles:,} miles one-way ({driving_days} driving days){estimate_note} "
            "Use this distance for PPM/DITY planning; partial DITY often nets $1,200–3,000 "
            "and full DITY more when weight allowance is maximized — verify with TMO."
        ),
    }


def resolve_installation(gaining_label: str) -> InstallationProfile:
    """Return installation profile from form gaining-installation value."""
    canonical = _canonical_installation_name(gaining_label)
    if canonical and canonical in INSTALLATIONS:
        return INSTALLATIONS[canonical]
    return DEFAULT_INSTALLATION


def get_bah_estimate(pay_grade: str, profile: InstallationProfile) -> int:
    """Return monthly BAH with dependents (2026 DTMO rates when available)."""
    from services.bah_rates import get_bah_monthly

    live = get_bah_monthly(profile.display_name, pay_grade)
    if live is not None:
        return live
    return profile.bah_rates.get(pay_grade, profile.bah_rates.get("E-5", 1600))


def get_bah_reference(pay_grade: str, profile: InstallationProfile) -> dict:
    """Return BAH metadata including source and effective date."""
    from services.bah_rates import get_bah_rate

    ref = get_bah_rate(profile.display_name, pay_grade, with_dependents=True)
    if ref.get("found"):
        return ref
    amount = profile.bah_rates.get(pay_grade, profile.bah_rates.get("E-5", 1600))
    return {
        "monthly_usd": amount,
        "mha": profile.display_name,
        "effective_date": "planning-fallback",
        "source": "PCS Vector static fallback (update bah_2026.json)",
        "with_dependents": True,
        "found": True,
    }


def build_installation_context(profile: InstallationProfile, pay_grade: str) -> dict:
    """Serialize installation reference data for the Grok prompt."""
    from services.utility_costs import (
        format_utility_table_markdown,
        get_utility_costs_for_installation,
    )

    bah_ref = get_bah_reference(pay_grade, profile)
    bah = bah_ref["monthly_usd"]
    rent_low, rent_high = profile.housing.avg_3br_rent_range
    base_data = get_installation_data(profile.display_name) or {}
    theater = base_data.get("theater") or getattr(profile, "theater", None)
    is_oconus = theater == "OCONUS" or profile.state in (
        "HI",
        "AK",
        "South Korea",
        "Germany",
        "Japan",
        "Italy",
        "PR",
    )
    # State field may still be "TX" for CONUS; check notes for OCONUS installs
    name_l = profile.display_name.lower()
    if any(x in name_l for x in ("camp humphreys", "korea", "usag", "germany", "japan", "zama", "italy")):
        is_oconus = True
    utility_costs = get_utility_costs_for_installation(
        profile.display_name,
        climate_hint=profile.climate_note or profile.housing.utility_note,
        is_oconus=is_oconus,
    )
    return {
        "installation": profile.display_name,
        "short_name": profile.short_name,
        "priority": profile.priority,
        "installation_notes": profile.notes or base_data.get("notes", ""),
        "location": {
            "city": profile.city,
            "state": profile.state,
            "zip_code": profile.zip_code,
            "latitude": profile.latitude,
            "longitude": profile.longitude,
            "nearby_zip_codes": list(profile.nearby_zip_codes),
        },
        "major_areas": base_data.get("major_areas", []),
        "commute_notes": base_data.get("commute_notes", ""),
        "estimated_bah_with_dependents_usd": bah,
        "bah_reference": bah_ref,
        "typical_3br_rent_range_usd": {"low": rent_low, "high": rent_high},
        "bah_surplus_if_rent_at_low": bah - rent_low,
        "bah_gap_if_rent_at_high": bah - rent_high,
        "on_post_pros": list(profile.housing.on_post_pros),
        "on_post_cons": list(profile.housing.on_post_cons),
        "off_post_areas_to_research": list(profile.housing.off_post_areas),
        "utility_note": profile.housing.utility_note,
        "off_post_utility_costs": utility_costs,
        "off_post_utility_table_markdown": format_utility_table_markdown(utility_costs),
        "school_districts": list(profile.school_districts),
        "spouse_employment_leads": list(profile.spouse_employment_notes),
        "childcare_waitlist_notes": list(profile.childcare_notes),
        "military_spouse_programs": list(profile.spouse_programs),
        "vehicle_registration_note": profile.vehicle_registration_note,
        "climate_and_cost_note": profile.climate_note,
        "commute_hotspots": list(profile.commute_hotspots),
        "housing_table_guidance": {
            "on_post_out_of_pocket_rent_usd": 0,
            "on_post_note": "Assigned government housing — BAH is absorbed; no monthly rent payment.",
            "use_rent_low_for_surplus_calc": bah - rent_low,
            "use_rent_high_for_shortfall_calc": bah - rent_high,
        },
    }


# ---------------------------------------------------------------------------
# HOW TO ADD A NEW INSTALLATION
# ---------------------------------------------------------------------------
# 1. Add an entry to INSTALLATION_DATA using the traditional name as the key
#    (e.g. "Fort Example, ST"). Required fields: state, priority (High/Medium/Low),
#    notes, major_areas, school_districts, commute_notes.
#
# 2. If the Army has renamed the post, add the new official name to
#    INSTALLATION_ALIASES pointing to your traditional key — never use the new
#    name in user-facing copy.
#
# 3. (Optional) Add hand-tuned report fields to _RICH_PROFILE_EXTENSIONS for
#    bases that need zip codes, BAH fallbacks, spouse/childcare detail, or
#    commute hotspots beyond the generic template.
#
# 4. (Optional) Add 2026 BAH rates to data/bah_2026.json so get_bah_estimate()
#    pulls live DTMO figures instead of planning fallbacks.
#
# 5. (Optional) Add MOVE_ROUTE_MILES pairs for common PCS corridors involving
#    the new installation (both directions).
#
# 6. Form dropdowns read SUPPORTED_INSTALLATIONS automatically (alphabetical).
#
# INSTALLATIONS and SUPPORTED_INSTALLATIONS rebuild automatically from
# INSTALLATION_DATA — no separate list maintenance required.
# OCONUS posts should set theater="OCONUS" (OHA guidance; BAH calculator skips them).