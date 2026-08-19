import requests


# ============================================================
# CONFIG
# ============================================================

BASE_URL = "https://www.themuse.com/api/public/jobs"

SOURCE_NAME = "The Muse"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    )
}


# ============================================================
# CATEGORY TEXT EXTRACTION
# ============================================================

def extract_category_text(categories):

    values = []

    if not categories:
        return ""

    for category in categories:

        if isinstance(category, dict):

            name = category.get(
                "name",
                ""
            )

            if name:
                values.append(
                    str(name)
                )

        elif isinstance(category, str):

            values.append(
                category
            )

    return " ".join(values)


# ============================================================
# DOMAIN DETECTION
# ============================================================

def detect_domain(title, categories):

    text = title.lower()

    category_text = extract_category_text(
        categories
    ).lower()

    combined = f"{text} {category_text}"

    # React
    if "react" in combined:
        return "React"

    # Python
    if any(keyword in combined for keyword in [
        "python",
        "django",
        "flask",
        "fastapi"
    ]):
        return "Python"

    # AI / ML
    if any(keyword in combined for keyword in [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "generative ai",
        "ai engineer",
        "machine learning engineer"
    ]):
        return "AI / ML"

    # Cybersecurity
    if any(keyword in combined for keyword in [
        "cybersecurity",
        "cyber security",
        "information security",
        "security engineer",
        "ethical hacking"
    ]):
        return "Cybersecurity"

    # Cloud
    if any(keyword in combined for keyword in [
        "cloud",
        "aws",
        "azure",
        "google cloud",
        "gcp"
    ]):
        return "Cloud"

    # DevOps
    if any(keyword in combined for keyword in [
        "devops",
        "docker",
        "kubernetes",
        "jenkins"
    ]):
        return "DevOps"

    # Android
    if any(keyword in combined for keyword in [
        "android",
        "kotlin"
    ]):
        return "Android"

    # Data Science
    if any(keyword in combined for keyword in [
        "data science",
        "data scientist",
        "data analyst",
        "data analytics"
    ]):
        return "Data Science"

    # Web Development
    if any(keyword in combined for keyword in [
        "web developer",
        "web development",
        "frontend",
        "front end",
        "backend",
        "back end",
        "full stack",
        "javascript",
        "html",
        "css"
    ]):
        return "Web Development"

    # Java
    if any(keyword in combined for keyword in [
        "java developer",
        "java engineer",
        "spring boot",
        "spring framework"
    ]):
        return "Java"

    # UI / UX
    if any(keyword in combined for keyword in [
        "ui/ux",
        "ui ux",
        "ux design",
        "ui design",
        "product design",
        "figma"
    ]):
        return "UI / UX"

    # Digital Marketing
    if any(keyword in combined for keyword in [
        "digital marketing",
        "seo",
        "social media marketing",
        "content marketing"
    ]):
        return "Digital Marketing"

    # Embedded
    if any(keyword in combined for keyword in [
        "embedded",
        "embedded systems",
        "firmware",
        "iot",
        "arduino",
        "raspberry pi"
    ]):
        return "Embedded Systems"

    return "Other"


# ============================================================
# LOCATION EXTRACTION
# ============================================================

def extract_location(locations):

    if not locations:
        return "Not Specified"

    location_names = []

    for location in locations:

        if isinstance(location, dict):

            name = location.get(
                "name",
                ""
            )

            if name:
                location_names.append(
                    str(name)
                )

        elif isinstance(location, str):

            location_names.append(
                location
            )

    if not location_names:
        return "Not Specified"

    return ", ".join(
        location_names
    )


# ============================================================
# SCRAPE THE MUSE
# ============================================================

def scrape_themuse():

    internships = []

    try:

        print(
            "Fetching The Muse..."
        )

        all_jobs = []

        # ----------------------------------------------------
        # Fetch first 3 pages
        # ----------------------------------------------------

        for page in range(0, 3):

            params = {
                "page": page,
                "level": "Internship"
            }

            response = requests.get(
                BASE_URL,
                params=params,
                headers=HEADERS,
                timeout=30
            )

            print(
                f"The Muse page {page}: "
                f"{response.status_code}"
            )

            response.raise_for_status()

            data = response.json()

            jobs = data.get(
                "results",
                []
            )

            if not jobs:
                break

            all_jobs.extend(
                jobs
            )

        print(
            f"The Muse returned "
            f"{len(all_jobs)} internship jobs."
        )

        # ----------------------------------------------------
        # Convert jobs
        # ----------------------------------------------------

        for job in all_jobs:

            title = job.get(
                "name",
                ""
            )

            if not isinstance(title, str):
                continue

            title = title.strip()

            if not title:
                continue

            # ------------------------------------------------
            # Company
            # ------------------------------------------------

            company_data = job.get(
                "company",
                {}
            )

            if isinstance(
                company_data,
                dict
            ):

                company = company_data.get(
                    "name",
                    "Not Specified"
                )

            else:

                company = str(
                    company_data
                )

            # ------------------------------------------------
            # Location
            # ------------------------------------------------

            locations = job.get(
                "locations",
                []
            )

            location = extract_location(
                locations
            )

            # ------------------------------------------------
            # Categories
            # ------------------------------------------------

            categories = job.get(
                "categories",
                []
            )

            domain = detect_domain(
                title,
                categories
            )

            # ------------------------------------------------
            # Posted Date
            # ------------------------------------------------

            publication_date = job.get(
                "publication_date",
                ""
            )

            # ------------------------------------------------
            # URL
            # ------------------------------------------------

            refs = job.get(
                "refs",
                {}
            )

            if isinstance(refs, dict):

                landing_page = refs.get(
                    "landing_page",
                    ""
                )

            else:

                landing_page = ""

            # ------------------------------------------------
            # Final Internship Object
            # ------------------------------------------------

            internship = {

                "title": title,

                "company": company,

                "location": location,

                "domain": domain,

                "type": "Internship",

                "source": SOURCE_NAME,

                "salary": "Not Specified",

                "duration": "",

                "start_date": "",

                "posted_date": publication_date,

                "apply_by": "",

                "openings": "",

                "url": landing_page

            }

            internships.append(
                internship
            )

        print(
            f"The Muse: "
            f"{len(internships)} internship records"
        )

        return internships

    except Exception as error:

        print(
            "The Muse scraper error:",
            error
        )

        return []


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    data = scrape_themuse()

    print(
        "\n# Total internships:",
        len(data)
    )

    for index, internship in enumerate(
        data[:20],
        start=1
    ):

        print(
            f"\n{index}. "
            f"{internship['title']}"
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