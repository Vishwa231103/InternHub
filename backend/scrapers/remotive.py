import requests


# ============================================================
# REMOTIVE API
# ============================================================

API_URL = "https://remotive.com/api/remote-jobs"


# ============================================================
# FETCH REMOTIVE JOBS
# ============================================================

def fetch_remotive_jobs():

    response = requests.get(
        API_URL,
        timeout=20
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# DOMAIN DETECTION
# ============================================================

def detect_domain(title, category=""):

    text = (
        f"{title} {category}"
    ).lower()


    if any(
        word in text
        for word in [
            "python",
            "django",
            "flask"
        ]
    ):

        return "Python"


    if any(
        word in text
        for word in [
            "java",
            "spring"
        ]
    ):

        return "Java"


    if any(
        word in text
        for word in [
            "react",
            "frontend",
            "front-end",
            "web developer",
            "web development"
        ]
    ):

        return "Web Development"


    if any(
        word in text
        for word in [
            "data science",
            "data analyst",
            "data analytics"
        ]
    ):

        return "Data Science"


    if any(
        word in text
        for word in [
            "machine learning",
            "deep learning",
            "artificial intelligence",
            "generative ai",
            "ai engineer"
        ]
    ):

        return "AI / ML"


    if any(
        word in text
        for word in [
            "cybersecurity",
            "cyber security",
            "information security"
        ]
    ):

        return "Cybersecurity"


    if any(
        word in text
        for word in [
            "cloud",
            "aws",
            "azure",
            "google cloud"
        ]
    ):

        return "Cloud"


    if any(
        word in text
        for word in [
            "devops",
            "dev ops"
        ]
    ):

        return "DevOps"


    if any(
        word in text
        for word in [
            "android",
            "kotlin"
        ]
    ):

        return "Android"


    if any(
        word in text
        for word in [
            "embedded",
            "iot",
            "arduino",
            "raspberry pi"
        ]
    ):

        return "Embedded Systems"


    if any(
        word in text
        for word in [
            "ui/ux",
            "ui ux",
            "user experience",
            "user interface"
        ]
    ):

        return "UI / UX"


    if any(
        word in text
        for word in [
            "marketing",
            "digital marketing"
        ]
    ):

        return "Digital Marketing"


    return "Other"


# ============================================================
# SCRAPE / FETCH REMOTIVE DATA
# ============================================================

def scrape_remotive():

    data = fetch_remotive_jobs()

    jobs = data.get(
        "jobs",
        []
    )


    internships = []


    for job in jobs:

        title = job.get(
            "title",
            ""
        ).strip()


        company = job.get(
            "company_name",
            ""
        ).strip()


        location = job.get(
            "candidate_required_location",
            ""
        ).strip()


        category = job.get(
            "category",
            ""
        ).strip()


        description = job.get(
            "description",
            ""
        )


        url = job.get(
            "url",
            ""
        )


        publication_date = job.get(
            "publication_date",
            ""
        )


        salary = job.get(
            "salary",
            ""
        )


        job_type = job.get(
            "job_type",
            ""
        )


        if not title:

            continue


        domain = detect_domain(
            title,
            category
        )


        internship = {

            "title": title,

            "company": company,

            "location": location,

            "domain": domain,

            "type": job_type or "Remote Job",

            "source": "Remotive",

            "salary": salary or "Not specified",

            "duration": "",

            "start_date": "",

            "posted_date": publication_date,

            "apply_by": "",

            "openings": "",

            "url": url

        }


        internships.append(
            internship
        )


    return internships


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    data = scrape_remotive()


    print(
        "\n=========================================="
    )

    print(
        "REMOTIVE JOBS"
    )

    print(
        "=========================================="
    )

    print(
        f"Total jobs: {len(data)}"
    )

    print(
        "==========================================\n"
    )


    for index, job in enumerate(
        data[:10],
        start=1
    ):

        print(
            f"{index}. {job['title']}"
        )

        print(
            f"   Company: {job['company']}"
        )

        print(
            f"   Location: {job['location']}"
        )

        print(
            f"   Domain: {job['domain']}"
        )

        print(
            f"   Source: {job['source']}"
        )

        print(
            f"   URL: {job['url']}"
        )

        print(
            "------------------------------------------"
        )