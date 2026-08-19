import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# ============================================================
# AICTE INTERNSHIP PORTAL
# ============================================================

BASE_URL = "https://internship.aicte-india.org"

INTERNSHIP_URL = (
    "https://internship.aicte-india.org/"
    "internships.php?future=intern"
)


# ============================================================
# FETCH WEBSITE
# ============================================================

def fetch_page():

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/151.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(
        INTERNSHIP_URL,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    return response.text


# ============================================================
# HELPER FUNCTION
# ============================================================

def get_text(element, selector, default=""):

    found = element.select_one(selector)

    if found:

        return found.get_text(
            " ",
            strip=True
        )

    return default


# ============================================================
# SCRAPE AICTE
# ============================================================

def scrape_aicte():

    html = fetch_page()

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    internships = []


    # ========================================================
    # FIND INTERNSHIP CARDS
    # ========================================================

    cards = soup.select(
        ".internships-list .internship-item"
    )


    print(
        f"Found {len(cards)} internship cards on AICTE page."
    )


    # ========================================================
    # PROCESS EACH CARD
    # ========================================================

    for card in cards:

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        title = get_text(
            card,
            ".job-title"
        )


        # ----------------------------------------------------
        # Company
        # ----------------------------------------------------

        company = get_text(
            card,
            ".company-name"
        )


        # ----------------------------------------------------
        # Job attributes
        # ----------------------------------------------------

        attributes = card.select(
            ".job-attributes li"
        )


        internship_type = ""

        posted_date = ""

        location = ""


        for attribute in attributes:

            class_list = attribute.get(
                "class",
                []
            )

            value = attribute.get_text(
                " ",
                strip=True
            )


            if "wfh" in class_list:

                internship_type = value


            elif "posted-on" in class_list:

                posted_date = value


            elif "location" in class_list:

                location = value


        # ----------------------------------------------------
        # Start date
        # ----------------------------------------------------

        start_date = get_text(
            card,
            ".start-date span"
        )


        # ----------------------------------------------------
        # Duration
        # ----------------------------------------------------

        duration = get_text(
            card,
            ".duration span"
        )


        # ----------------------------------------------------
        # Stipend
        # ----------------------------------------------------

        stipend = get_text(
            card,
            ".stipend span"
        )


        # ----------------------------------------------------
        # Number of openings
        # ----------------------------------------------------

        openings = ""


        for item in card.select(
            ".job-supplement-attributes li"
        ):

            heading = item.select_one(
                "h6"
            )

            if heading:

                heading_text = heading.get_text(
                    " ",
                    strip=True
                ).lower()


                if "number of openings" in heading_text:

                    span = item.select_one(
                        "span"
                    )

                    if span:

                        openings = span.get_text(
                            " ",
                            strip=True
                        )

                    break


        # ----------------------------------------------------
        # Apply by
        # ----------------------------------------------------

        apply_by = get_text(
            card,
            ".apply-by span"
        )


        # ----------------------------------------------------
        # Details URL
        # ----------------------------------------------------

        details_link = card.select_one(
            ".btn-wrap a"
        )


        if details_link:

            href = details_link.get(
                "href",
                ""
            )

            details_url = urljoin(
                BASE_URL + "/",
                href
            )

        else:

            details_url = ""


        # ----------------------------------------------------
        # Skip invalid cards
        # ----------------------------------------------------

        if not title:

            continue


        # ----------------------------------------------------
        # Determine basic domain
        # ----------------------------------------------------

        domain = detect_domain(
            title
        )


        # ----------------------------------------------------
        # Create standardized record
        # ----------------------------------------------------

        internship = {

            "title": title,

            "company": company,

            "location": location,

            "domain": domain,

            "type": internship_type,

            "source": "AICTE",

            "salary": stipend,

            "duration": duration,

            "start_date": start_date,

            "posted_date": posted_date,

            "apply_by": apply_by,

            "openings": openings,

            "url": details_url

        }


        internships.append(
            internship
        )


    return internships


# ============================================================
# DOMAIN DETECTION
# ============================================================

def detect_domain(title):

    title_lower = title.lower()


    if any(
        word in title_lower
        for word in [
            "python",
            "django",
            "flask"
        ]
    ):

        return "Python"


    if any(
        word in title_lower
        for word in [
            "java",
            "spring boot",
            "spring"
        ]
    ):

        return "Java"


    if any(
        word in title_lower
        for word in [
            "react",
            "frontend",
            "front end",
            "web development",
            "web developer"
        ]
    ):

        return "Web Development"


    if any(
        word in title_lower
        for word in [
            "data science",
            "data analyst",
            "data analytics"
        ]
    ):

        return "Data Science"


    if any(
        word in title_lower
        for word in [
            "machine learning",
            "deep learning",
            "artificial intelligence",
            "generative ai",
            "agentic ai",
            "ai agent",
            "ai agents"
        ]
    ):

        return "AI / ML"


    if any(
        word in title_lower
        for word in [
            "cybersecurity",
            "cyber security",
            "information security"
        ]
    ):

        return "Cybersecurity"


    if any(
        word in title_lower
        for word in [
            "cloud",
            "aws",
            "azure",
            "google cloud"
        ]
    ):

        return "Cloud"


    if any(
        word in title_lower
        for word in [
            "devops",
            "dev ops"
        ]
    ):

        return "DevOps"


    if any(
        word in title_lower
        for word in [
            "android",
            "kotlin"
        ]
    ):

        return "Android"


    if any(
        word in title_lower
        for word in [
            "embedded",
            "arduino",
            "raspberry pi",
            "iot"
        ]
    ):

        return "Embedded Systems"


    if any(
        word in title_lower
        for word in [
            "ui/ux",
            "ui ux",
            "user interface",
            "user experience"
        ]
    ):

        return "UI / UX"


    if any(
        word in title_lower
        for word in [
            "marketing",
            "digital marketing"
        ]
    ):

        return "Digital Marketing"


    return "Other"


# ============================================================
# TEST SCRAPER
# ============================================================

if __name__ == "__main__":

    data = scrape_aicte()


    print(
        "\n=========================================="
    )

    print(
        f"TOTAL INTERNSHIPS FOUND: {len(data)}"
    )

    print(
        "==========================================\n"
    )


    for index, internship in enumerate(
        data[:10],
        start=1
    ):

        print(
            f"{index}. {internship['title']}"
        )

        print(
            f"   Company: {internship['company']}"
        )

        print(
            f"   Location: {internship['location']}"
        )

        print(
            f"   Domain: {internship['domain']}"
        )

        print(
            f"   Type: {internship['type']}"
        )

        print(
            f"   Stipend: {internship['salary']}"
        )

        print(
            f"   Duration: {internship['duration']}"
        )

        print(
            f"   Apply By: {internship['apply_by']}"
        )

        print(
            f"   URL: {internship['url']}"
        )

        print(
            "------------------------------------------"
        )