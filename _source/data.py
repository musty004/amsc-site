"""Facts the site is built from. Change a fact here once and rebuild.

Everything below comes from the AMSC Website Requirements Master Brief
(2026/2027) unless the comment says otherwise.
"""

# ---------------------------------------------------------------- identity
ORG = "AFIT Muslim Students’ Community"
SHORT = "AMSC"
INSTITUTE = "Air Force Institute of Technology (AFIT), Kaduna"
TAGLINE_AR = "معًا في الدين والهدف"
TAGLINE_EN = "Together in Faith and Purpose"
CORE = "Building brotherhood and purpose through faith."
KEY = "Fostering academic excellence in Muslim students."
CAMPAIGN = "One Ummah. One Campus."
SESSION = "1448 AH / 2026–2027"

# The live address today. Change this one line when the site moves to its
# own domain; canonical links, the sitemap and share previews follow it.
SITE_URL = "https://afitmsc.com.ng"

# ---------------------------------------------------------------- channels
EMAIL = "Afitmssn@gmail.com"
IG = "https://www.instagram.com/afitmsc/"
IG_HANDLE = "@afitmsc"
IG_FRESHERS_POST = "https://www.instagram.com/p/DetrV2ljgpf/"
FB = "https://www.facebook.com/share/19dP61VwLX/"
# Registration (membership + WhatsApp Community). Students register here and
# an admin adds them to the WhatsApp Community. Embedded on join.html.
GFORM = "https://docs.google.com/forms/d/e/1FAIpQLSfekaScC6DzLTsi1cZsaLM3jOFMluLS_5ZwNnVV_VZbJC4g4A/viewform"
GFORM_EMBED = GFORM + "?embedded=true"
JOIN = "join.html#register"          # every "Join" button points here

# Formspree endpoints (forms are sent in the background; a full-page thank-you shows after)
FORMSPREE_CONTACT = "https://formspree.io/f/myeepzbb"   # contact form and volunteer form
FORMSPREE_ALUMNI = "https://formspree.io/f/xdeedkpz"    # AMAN alumni register
# Carried over from the previous version of the site (not in the 2026 brief).
WA_LINE = "https://wa.me/2349027597106"
WA_LINE_DISPLAY = "+234 902 759 7106"
# Substack: the publication does not exist yet. Leave this as None until the
# official URL is confirmed; the site shows "Coming soon" while it is None.
SUBSTACK = None

# Carried over from the previous version of the site.
DUES = "https://selar.com/u2vg771111"   # online card payment for dues and the welfare fund
# Semester dues by bank transfer, from the 2026/2027 "Semester Dues" flyer.
# The account belongs to the Financial Officer; update all three lines when it changes.
DUES_ACCOUNT_NUMBER = "2089476204"
DUES_ACCOUNT_NAME = "Abdullahi Abdulrahman"
DUES_BANK = "Kuda MFB"
DUES_AMOUNT = "&#8358;1,000 and above"
PQ = "https://drive.google.com/drive/folders/1fb8-RHPktAcA3E0Pl-qYUzApFLa60jUP"
ALBUM_MUSABAQAH = "https://photos.app.goo.gl/in1m5R4zdyLntKKWA"
# Freshers' Orientation 2025/1447 photo album
ALBUM_COMMUNITY = "https://photos.app.goo.gl/FcwfspCuvfw3PGTc8"
ALBUM_ORIENTATION_2025 = ALBUM_COMMUNITY
ASKBOX = "https://gdpd.xyz/amsc"


def wa(num, msg):
    """WhatsApp click-to-chat link for a Nigerian number like 08029320846."""
    from urllib.parse import quote
    return f"https://wa.me/234{num[1:]}?text={quote(msg)}"


def wa_text(msg):
    """WhatsApp click-to-chat link with a prefilled message."""
    from urllib.parse import quote
    return f"{WA_LINE}?text={quote(msg)}"


# ---------------------------------------------------------------- values
VALUES = [
    ("Faith", "Worship and sincerity come first, in every programme we run."),
    ("Unity", "One community across departments, levels and backgrounds."),
    ("Discipline", "Punctual, organised and dependable, as AFIT expects of us."),
    ("Excellence", "Doing every task well, from a tutorial to a Qur’an competition."),
    ("Service", "Looking after one another and leaving the campus better."),
    ("Growth", "Steady progress in deen, character and skill."),
    ("Academics", "Good grades are part of the trust placed in a student."),
]

# ---------------------------------------------------------------- executive
# Nominee list for the 1448 AH / 2026-2027 session, exactly as supplied.
# Presentation-only clean-ups: "Ass." is written "Asst." and "Dawah" is
# written "Da'wah". Phone None = contact not provided.
# Fields: name, department, level, role, phone, portfolio
BROTHERS = [
    ("Abdulmannan Abdullahi", "Physics", "400L", "Ameer", "09059509377", "lead"),
    ("Ganiyu Mubarak Ademola", "Chemistry", "400L", "Naibul Ameer", "09078721068", "lead"),
    ("Haruna Muhammad Sufyan", "Automotive Engineering", "500L", "Gen Secretary I", "08085877295", "sec"),
    ("Omeiza AbdulMugni Sha’aban", "Electrical and Electronics Engineering", "400L", "Mudeer", "09112654472", "lead"),
    ("Musa Abdulrazaq", "Aerospace Engineering", "400L", "Asst. Gen Secretary I", "07015854245", "sec"),
    ("Sulaiman Abdullah", "Automotive Engineering", "400L", "Da’wah Coordinator", "08030523205", "dawah"),
    ("Abdullah Abubakar Muhydeen", "Electrical and Electronics Engineering", "300L", "Asst. Da’wah Coordinator", "09036842089", "dawah"),
    ("Adeniyi Habibrahman Adejare", "Mechatronics Engineering", "500L", "Chief Organizer I", "07034330833", "org"),
    ("Mukhtar Atiku", "Mechanical Engineering", "400L", "Asst. Chief Organizer", "09126045092", "org"),
    ("Ahmad Aminu", "Electrical and Electronics Engineering", "400L", "Public Relation Officer I", "09072657979", "media"),
    ("Abubakar Muhammad Girei", "Civil and Environmental Engineering", "500L", "Public Relation Officer II", "09042425865", "media"),
    ("Kodaolu Khaleel Akorede", "Aerospace Engineering", "500L", "Media Coordinator I", "08123449488", "media"),
    ("Muhammad Kamal", "Civil and Environmental Engineering", "400L", "Asst. Media Coordinator I", "08121692327", "media"),
    ("Khalid Olatunde Ladeji", "Mechatronics Engineering", "500L", "Academics Coordinator I", "07080369164", "acad"),
    ("Badirudeen Abdulsobur", "Telecommunications Engineering", "300L", "Asst. Academics Coordinator I", "08135806903", "acad"),
    ("Najmudeen Mushaffa", "Mechatronics Engineering", "300L", "Welfare Officer I", "08029320846", "welfare"),
    ("Abdullah Kabir", "Aerospace Engineering", "400L", "Asst. Welfare Officer I", "09072027179", "welfare"),
    ("Abdullahi Abdulrahman", "Automotive Engineering", "400L", "Financial Officer", "09031411139", "fin"),
    ("Ibrahim Bayo", "Accounting", "400L", "Asset Maintenance Officer", "08166115813", "fin"),
    ("Ahmad Abubakar Sadiq", "Mechanical Engineering", "300L", "Mosque Coordinator", "08039349790", "mosque"),
]

SISTERS = [
    ("Ibrahim Nusaibah", "Electrical and Electronics Engineering", "500L", "Ameerah", "08168625392", "lead"),
    ("Amirah Usman Modibbo", "Cyber Security", "400L", "Naibatul Ameerah", "07062010279", "lead"),
    ("Ummusalma Ibrahim Ashu", "International Relations", "300L", "Gen Secretary II", None, "sec"),
    ("Hafsat Bashir", "Accounting", "300L", "Financial Secretary II", "08115338340", "fin"),
    ("Fatimah Usman", "Civil and Environmental Engineering", "400L", "Da’wah Coordinator II", "08101101858", "dawah"),
    ("Aisha Aminu", "Business Administration", "300L", "Asst. Da’wah Coordinator II", "08170215006", "dawah"),
    ("Faridat Abdulgafar", "Chemistry", "400L", "Chief Organizer II", "08081203245", "org"),
    ("Marufah Abdulhakeem", "Computer Science", "200L", "Asst. Chief Organizer II", "07017943546", "org"),
    ("Ummul Khair Muhammad", "Accounting", "300L", "Public Relation Officer II", "09168961211", "media"),
    ("Falade Kareemah", "Accounting", "300L", "Asst. Public Relation Officer II", "07014984376", "media"),
    ("Kafayat Ajibola Olarinoye", "Mechanical Engineering", "400L", "Media Coordinator II", "09112899697", "media"),
    ("Sanni Rahmah", "Metallurgy and Materials Engineering", "300L", "Asst. Media Coordinator II", "08163364382", "media"),
    ("Zhara Eneze Abdul Rahman", "Civil and Environmental Engineering", "400L", "Academics Coordinator II", "08100940559", "acad"),
    ("Khadija Jibril", "Accounting", "300L", "Asst. Academics Coordinator", "07015163069", "acad"),
    ("Fatima Abubakar", "Electrical and Electronics Engineering", "500L", "Welfare Officer II", "08143404271", "welfare"),
    ("Aisha Yusuf", "Mechatronics Engineering", "300L", "Asst. Welfare Officer II", "09035561675", "welfare"),
]

PORTFOLIOS = [
    ("lead", "Leadership",
     "Sets the direction for the session, represents AMSC to the Institute and "
     "coordinates the work of every portfolio. The Ameer and Ameerah lead the "
     "brothers’ and sisters’ wings."),
    ("sec", "Secretariat",
     "Records and minutes, correspondence, the membership register and letters "
     "of attestation for scholarship applications."),
    ("dawah", "Da’wah",
     "Islamiyyah classes, reminders, lectures, Da’wah Week and the anonymous "
     "question-and-answer sessions."),
    ("org", "Organising",
     "Planning and logistics for programmes and events: venues, set-up, "
     "registration and the order of the day."),
    ("media", "Public relations and media",
     "Announcements, flyers, photography and video, the social channels and "
     "this website."),
    ("acad", "Academics",
     "Weekend tutorials, the past question bank, scholarship notices and "
     "support through exam season."),
    ("welfare", "Welfare",
     "Confidential support for members, visits to the sick, and help for new "
     "students as they settle in."),
    ("fin", "Finance and assets",
     "Dues, donations, receipts and accounts, and the care of the community’s "
     "property."),
    ("mosque", "Mosque",
     "Coordinating AMSC’s activities at the mosque."),
]


def tel(num):
    return "+234" + num[1:]


def pretty_phone(num):
    return f"{num[:4]} {num[4:7]} {num[7:]}"


def initials(name):
    parts = [p for p in name.replace("’", "").split() if p[0].isalpha()]
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) > 1 else parts[0][:2].upper()


def wing_of(p):
    return "Brothers" if p in BROTHERS else "Sisters"


def holder(role_startswith, wing="b"):
    """Find an executive by the start of their role, for cross-page references."""
    for p in (BROTHERS if wing == "b" else SISTERS):
        if p[3].lower().startswith(role_startswith.lower()):
            return p
    raise KeyError(role_startswith)


# ---------------------------------------------------------------- freshers
# Part 14 of the brief.
FRESHER_PREP = [
    "Exactly 4 photocopies of every required document",
    "White-background passport photographs",
    "Primary school certificate",
    "LGA identification letter",
]
FRESHER_PAYMENT = [
    ("Pay the acceptance fee first", "Pay it before you pay the school fees."),
    ("Print every online payment receipt", "Keep the printed copies together with your documents."),
    ("Get the receipts verified and stamped", "Take them to the Bursary Unit for physical verification and stamping before you go any further."),
]
FRESHER_ROUTE = [
    ("Bursary Unit", "Have your online payment receipts physically verified and stamped."),
    ("Academic Branch", "Submit your 4 complete sets of required documents."),
    ("Departmental Officer", "Complete your registration with your department."),
]


def officer_wa(role, wing):
    p = holder(role, wing)
    return wa(p[4], "Assalamu alaykum, I got your contact from the AMSC website. I would like to speak with the welfare officer.")


def mudeer_wa():
    p = holder("Mudeer", "b")
    return wa(p[4], "Assalamu alaykum, I would like access to the Islamiyyah class notes.")


# ---------------------------------------------------------------- prayer locations
JUMUAH_PLACE = "Nigerian Air Force Base Central Mosque, beside the NAF Hospital"
EID_PLACE = "Air Force Primary School"

# ---------------------------------------------------------------- Amanah Desk (lost and found)
AMANAH_NUMBER = "08166115813"
AMANAH_DISPLAY = "+234 816 611 5813"
AMANAH_WA = wa(AMANAH_NUMBER, "Assalamu alaykum, I am contacting the Amanah Desk from the AMSC website.")

# ---------------------------------------------------------------- PDFNest partnership
PDFNEST_URL = "https://pdfnest.vercel.app"
PDFNEST_WA = wa("07030586690", "Assalamu alaykum, I am an AFIT student from the AMSC website. Please help me get access to the PDFNest WhatsApp group.")

# ---------------------------------------------------------------- Islamiyyah
# From the AFIT Islaamiyyah Committee's 2026/2027 Programme Portfolio and the
# "Islamiyyah classes are back" flyer.
ISLAMIYYAH_VENUE = "AFIT Mosque"
ISLAMIYYAH_DAYS = "Saturdays and Sundays"
ISLAMIYYAH_HOURS = "9:00am to 12:30pm"
# (day: 0 = Sunday … 6 = Saturday, start, end, session, who)
ISLAMIYYAH_TIMETABLE = [
    (6, "09:00", "11:00", "Musaffa, Tajweed and Hifz", "Grouped by Qur’an level"),
    (6, "11:00", "12:30", "Arabic Language", "Grouped by Arabic level"),
    (0, "09:00", "11:00", "Musaffa, Tajweed and Hifz", "Grouped by Qur’an level"),
    (0, "11:00", "12:30", "Islamic Book Studies", "All students together"),
]
ARABIC_TEXT = ("دروس اللغة العربية", "Durus al-Lughah al-Arabiyyah")
# (Arabic title, transliteration, subject, what it covers)
ISLAMIYYAH_BOOKS = [
    ("نواقض الإسلام", "Nawaqid al-Islam", "Aqeedah and Tawheed", "the foundations of Islamic belief and Tawheed"),
    ("كتاب الأخضري", "Kitab al-Akhdari", "Fiqh", "foundational jurisprudence and practical worship"),
    ("خلاصة نور اليقين", "Khulasat Nur al-Yaqeen", "Seerah", "the life, character and teachings of the Prophet ﷺ"),
]
PORTAL = "portal.html"


def portal_help_wa():
    p = holder("Mudeer", "b")
    return wa(p[4], "Assalamu alaykum, I need help with the AMSC Islamiyyah Student Portal.")
