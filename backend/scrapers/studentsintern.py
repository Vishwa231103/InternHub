import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://studentsintern.com/"
SOURCE_NAME = "StudentsIntern"


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    )
}


# ============================================================
# DOMAIN DETECTION
# ============================================================

def detect_domain(title, skills=""):

    title_text = title.lower().strip()
    skills_text = skills.lower().strip()

    text = f"{title_text} {skills_text}"

    # React
    if "react" in text:
        return "React"

    # Python
    if (
        "python" in title_text
        or "django" in title_text
        or "flask" in title_text
        or "fastapi" in title_text
        or "python" in skills_text
    ):
        return "Python"

    # AI / ML
    if any(keyword in text for keyword in [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "generative ai",
        "ai/ml",
        "tensorflow",
        "pytorch"
    ]):
        return "AI / ML"

    # Cybersecurity
    if any(keyword in text for keyword in [
        "cyber security",
        "cybersecurity",
        "ethical hacking",
        "penetration testing",
        "network security"
    ]):
        return "Cybersecurity"

    # Android
    if any(keyword in text for keyword in [
        "android",
        "kotlin"
    ]):
        return "Android"

    # UI / UX
    if any(keyword in text for keyword in [
        "ui/ux",
        "ui ux",
        "ux design",
        "ui design",
        "figma"
    ]):
        return "UI / UX"

    # Digital Marketing
    if any(keyword in text for keyword in [
        "digital marketing",
        "seo",
        "social media",
        "content marketing"
    ]):
        return "Digital Marketing"

    # DevOps
    if any(keyword in text for keyword in [
        "devops",
        "docker",
        "kubernetes",
        "jenkins",
        "ci/cd"
    ]):
        return "DevOps"

    # Cloud
    if any(keyword in text for keyword in [
        "cloud",
        "aws",
        "azure",
        "google cloud",
        "gcp"
    ]):
        return "Cloud"

    # Web Development
    if any(keyword in text for keyword in [
        "web development",
        "web developer",
        "frontend",
        "front end",
        "backend",
        "back end",
        "full stack",
        "html",
        "css",
        "javascript"
    ]):
        return "Web Development"

    # Java
    # IMPORTANT:
    # Do not use simply "java" in text
    # because JavaScript contains "java".

    if (
        "java developer" in title_text
        or "java /" in title_text
        or "java internship" in title_text
        or "spring boot" in text
        or "spring framework" in text
    ):
        return "Java"

    # Data Science
    if any(keyword in text for keyword in [
        "data science",
        "data scientist",
        "data analyst",
        "analytics",
        "pandas",
        "numpy"
    ]):
        return "Data Science"

    # Embedded Systems
    if any(keyword in text for keyword in [
        "embedded",
        "arduino",
        "raspberry pi",
        "embedded systems",
        "iot"
    ]):
        return "Embedded Systems"

    return "Other"


# ============================================================
# COMPANY EXTRACTION
# ============================================================

def extract_company(card, title):

    lines = [
        line.strip()
        for line in card.get_text(
            "\n",
            strip=True
        ).splitlines()
        if line.strip()
    ]

    ignored = {
        title.lower(),
        "onsite",
        "remote",
        "hybrid",
        "why apply?",
        "verified & approved company",
        "apply in one click",
        "instant status updates",
        "view & apply →",
        "apply now →"
    }

    locations = {
        "hyderabad",
        "bangalore",
        "bengaluru",
        "chennai",
        "mumbai",
        "delhi",
        "pune",
        "thanjavur",
        "coimbatore",
        "kolkata",
        "noida",
        "gurgaon",
        "gurugram"
    }

    # Actual StudentsIntern card order is generally:
    #
    # Title
    # Work Mode
    # Company
    # Location
    # Skills
    #
    # So first suitable line after title/work-mode
    # is normally the company.

    title_found = False

    for line in lines:

        lower = line.lower().strip()

        if lower == title.lower():
            title_found = True
            continue

        if not title_found:
            continue

        if lower in ignored:
            continue

        if lower in locations:
            continue

        # Skip obvious skill names
        if lower in {
            "python",
            "java",
            "mysql",
            "sql",
            "html",
            "css",
            "javascript",
            "react",
            "git",
            "github",
            "figma",
            "django",
            "spring boot"
        }:
            continue

        if len(line) <= 80:
            return line

    return ""


# ============================================================
# LOCATION EXTRACTION
# ============================================================

def extract_location(card):

    text = card.get_text(
        " ",
        strip=True
    ).lower()

    locations = [
        "Hyderabad",
        "Bangalore",
        "Bengaluru",
        "Chennai",
        "Mumbai",
        "Delhi",
        "Pune",
        "Thanjavur",
        "Coimbatore",
        "Kolkata",
        "Noida",
        "Gurgaon",
        "Gurugram",
        "India"
    ]

    for location in locations:

        if location.lower() in text:
            return location

    return ""


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_skills(card):

    text = card.get_text(
        " ",
        strip=True
    ).lower()

    skills = [
        "python",
        "java",
        "react",
        "javascript",
        "html",
        "css",
        "sql",
        "mysql",
        "figma",
        "machine learning",
        "artificial intelligence",
        "tensorflow",
        "pandas",
        "django",
        "spring boot",
        "kotlin",
        "android",
        "git",
        "github",
        "aws",
        "docker"
    ]

    found = []

    for skill in skills:

        # Prevent Java from matching JavaScript
        if skill == "java":

            if "java" in text and "javascript" not in text:
                found.append(skill)

        elif skill in text:

            found.append(skill)

    return ", ".join(found)


# ============================================================
# SCRAPE STUDENTSINTERN
# ============================================================

def scrape_studentsintern():

    internships = []

    try:

        print("Fetching StudentsIntern...")

        response = requests.get(
            BASE_URL,
            headers=HEADERS,
            timeout=30
        )

        response.raise_for_status()

        print(
            f"StudentsIntern status: "
            f"{response.status_code}"
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # IMPORTANT:
        # Actual internship cards are:
        #
        # <div class="int-card">

        cards = soup.select(
            "div.int-card"
        )

        print(
            f"Found {len(cards)} internship cards "
            f"on StudentsIntern page."
        )

        seen_urls = set()

        for card in cards:

            # ------------------------------------------------
            # TITLE
            # ------------------------------------------------

            title_element = card.select_one(
                ".int-title"
            )

            if not title_element:
                continue

            title = title_element.get_text(
                " ",
                strip=True
            )

            if not title:
                continue

            # ------------------------------------------------
            # APPLY LINK
            # ------------------------------------------------

            apply_url = ""

            links = card.find_all(
                "a",
                href=True
            )

            for link in links:

                href = link.get(
                    "href",
                    ""
                ).strip()

                link_text = link.get_text(
                    " ",
                    strip=True
                ).lower()

                if (
                    "apply" in link_text
                    or "view" in link_text
                ):
                    apply_url = href
                    break

            if not apply_url and links:

                apply_url = links[0].get(
                    "href",
                    ""
                ).strip()

            if not apply_url:
                continue

            url = urljoin(
                BASE_URL,
                apply_url
            )

            # ------------------------------------------------
            # DUPLICATES
            # ------------------------------------------------

            if url in seen_urls:
                continue

            seen_urls.add(url)

            # ------------------------------------------------
            # WORK MODE
            # ------------------------------------------------

            card_text = card.get_text(
                " ",
                strip=True
            )

            lower_text = card_text.lower()

            if "remote" in lower_text:
                work_mode = "Remote"

            elif "hybrid" in lower_text:
                work_mode = "Hybrid"

            elif "onsite" in lower_text:
                work_mode = "Onsite"

            else:
                work_mode = "Internship"

            # ------------------------------------------------
            # COMPANY
            # ------------------------------------------------

            company = extract_company(
                card,
                title
            )

            # ------------------------------------------------
            # LOCATION
            # ------------------------------------------------

            location = extract_location(
                card
            )

            # ------------------------------------------------
            # SKILLS
            # ------------------------------------------------

            skills = extract_skills(
                card
            )

            # ------------------------------------------------
            # DOMAIN
            # ------------------------------------------------

            domain = detect_domain(
                title,
                skills
            )

            # ------------------------------------------------
            # FINAL RECORD
            # ------------------------------------------------

            internship = {

                "title": title,

                "company": company,

                "location": location,

                "domain": domain,

                "type": "Internship",

                "source": SOURCE_NAME,

                "salary": "Not specified",

                "duration": "",

                "start_date": "",

                "posted_date": "",

                "apply_by": "",

                "openings": "",

                "url": url

            }

            internships.append(
                internship
            )

        print(
            f"StudentsIntern: "
            f"{len(internships)} internship records"
        )

        return internships

    except Exception as error:

        print(
            "StudentsIntern scraper error:",
            error
        )

        return []


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    data = scrape_studentsintern()

    print(
        "\n# Total internships:",
        len(data)
    )

    for index, internship in enumerate(
        data[:20],
        start=1
    ):

        print(
            f"\n{index}. {internship['title']}"
        )

        print(
            "   Company:",
            internship["company"]
        )

        print(
            "   Location:",
            internship["location"]
        )

        print(
            "   Domain:",
            internship["domain"]
        )

        print(
            "   Type:",
            internship["type"]
        )

        print(
            "   Source:",
            internship["source"]
        )

        print(
            "   URL:",
            internship["url"]
        )

        print("\n---")