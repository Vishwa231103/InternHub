import time

from scrapers.aicte import scrape_aicte
from scrapers.remotive import scrape_remotive
from scrapers.studentsintern import scrape_studentsintern
from scrapers.themuse import scrape_themuse

# ============================================================
# SIMPLE IN-MEMORY CACHE
# ============================================================

CACHE = {
    "data": [],
    "timestamp": 0
}

CACHE_DURATION = 15 * 60


# ============================================================
# NORMALIZE AICTE DATA
# ============================================================

def normalize_aicte(internships):

    normalized = []

    for internship in internships:

        normalized.append({

            "title": internship.get(
                "title",
                "Internship Opportunity"
            ),

            "company": internship.get(
                "company",
                "Not Specified"
            ),

            "location": internship.get(
                "location",
                "Not Specified"
            ),

            "domain": internship.get(
                "domain",
                "Other"
            ),

            "type": internship.get(
                "type",
                "Internship"
            ),

            "source": internship.get(
                "source",
                "AICTE"
            ),

            "salary": internship.get(
                "salary",
                "Not Specified"
            ),

            "duration": internship.get(
                "duration",
                "Not Specified"
            ),

            "start_date": internship.get(
                "start_date",
                ""
            ),

            "posted_date": internship.get(
                "posted_date",
                ""
            ),

            "apply_by": internship.get(
                "apply_by",
                ""
            ),

            "openings": internship.get(
                "openings",
                ""
            ),

            "url": internship.get(
                "url",
                ""
            )

        })

    return normalized


# ============================================================
# NORMALIZE REMOTIVE DATA
# ============================================================

def normalize_remotive(jobs):

    normalized = []

    for job in jobs:

        normalized.append({

            "title": job.get(
                "title",
                "Internship Opportunity"
            ),

            "company": job.get(
                "company",
                "Not Specified"
            ),

            "location": job.get(
                "location",
                "Not Specified"
            ),

            "domain": job.get(
                "domain",
                "Other"
            ),

            "type": job.get(
                "type",
                "Remote"
            ),

            "source": job.get(
                "source",
                "Remotive"
            ),

            "salary": job.get(
                "salary",
                "Not Specified"
            ),

            "duration": job.get(
                "duration",
                ""
            ),

            "start_date": job.get(
                "start_date",
                ""
            ),

            "posted_date": job.get(
                "posted_date",
                ""
            ),

            "apply_by": job.get(
                "apply_by",
                ""
            ),

            "openings": job.get(
                "openings",
                ""
            ),

            "url": job.get(
                "url",
                ""
            )

        })

    return normalized


# ============================================================
# NORMALIZE STUDENTSINTERN DATA
# ============================================================

def normalize_studentsintern(internships):

    normalized = []

    for internship in internships:

        normalized.append({

            "title": internship.get(
                "title",
                "Internship Opportunity"
            ),

            "company": internship.get(
                "company",
                "Not Specified"
            ),

            "location": internship.get(
                "location",
                "Not Specified"
            ),

            "domain": internship.get(
                "domain",
                "Other"
            ),

            "type": internship.get(
                "type",
                "Internship"
            ),

            "source": internship.get(
                "source",
                "StudentsIntern"
            ),

            "salary": internship.get(
                "salary",
                "Not Specified"
            ),

            "duration": internship.get(
                "duration",
                ""
            ),

            "start_date": internship.get(
                "start_date",
                ""
            ),

            "posted_date": internship.get(
                "posted_date",
                ""
            ),

            "apply_by": internship.get(
                "apply_by",
                ""
            ),

            "openings": internship.get(
                "openings",
                ""
            ),

            "url": internship.get(
                "url",
                ""
            )

        })

    return normalized


# ============================================================
# INTERNSHIP RELEVANCE CHECK
# ============================================================

def is_internship_relevant(job):

    text = " ".join([

        job.get(
            "title",
            ""
        ),

        job.get(
            "type",
            ""
        ),

        job.get(
            "duration",
            ""
        )

    ]).lower()


    internship_keywords = [

        "intern",

        "internship",

        "trainee",

        "student",

        "apprentice",

        "graduate intern",

        "summer intern"

    ]


    return any(

        keyword in text

        for keyword in internship_keywords

    )


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def remove_duplicates(internships):

    unique_internships = []

    seen = set()


    for internship in internships:

        title = internship.get(
            "title",
            ""
        ).strip().lower()


        company = internship.get(
            "company",
            ""
        ).strip().lower()


        location = internship.get(
            "location",
            ""
        ).strip().lower()


        url = internship.get(
            "url",
            ""
        ).strip().lower()


        # ----------------------------------------------------
        # Prefer URL when available
        # ----------------------------------------------------

        if url:

            unique_key = (
                "url",
                url
            )

        else:

            unique_key = (
                "details",
                title,
                company,
                location
            )


        if unique_key in seen:

            continue


        seen.add(
            unique_key
        )


        unique_internships.append(
            internship
        )


    return unique_internships


# ============================================================
# GET ALL INTERNSHIPS
# ============================================================

def get_all_internships():

    current_time = time.time()


    # ========================================================
    # RETURN CACHE IF STILL VALID
    # ========================================================

    if (

        CACHE["data"]

        and

        current_time - CACHE["timestamp"]
        < CACHE_DURATION

    ):

        print(
            "Using cached internship data."
        )

        return CACHE["data"]


    print(
        "Fetching fresh internship data..."
    )


    all_internships = []


    # ========================================================
    # AICTE
    # ========================================================

    try:

        aicte_data = scrape_aicte()


        aicte_data = normalize_aicte(
            aicte_data
        )


        all_internships.extend(
            aicte_data
        )


        print(
            f"AICTE: "
            f"{len(aicte_data)} records"
        )


    except Exception as error:

        print(
            "AICTE scraper error:",
            error
        )


    # ========================================================
    # REMOTIVE
    # ========================================================

    try:

        remotive_data = scrape_remotive()


        remotive_data = normalize_remotive(
            remotive_data
        )


        remotive_internships = [

            job

            for job in remotive_data

            if is_internship_relevant(
                job
            )

        ]


        all_internships.extend(
            remotive_internships
        )


        print(
            f"Remotive: "
            f"{len(remotive_internships)} "
            f"internship-relevant records"
        )


    except Exception as error:

        print(
            "Remotive scraper error:",
            error
        )


    # ========================================================
    # STUDENTSINTERN
    # ========================================================

    try:

        studentsintern_data = scrape_studentsintern()


        studentsintern_data = normalize_studentsintern(
            studentsintern_data
        )


        all_internships.extend(
            studentsintern_data
        )


        print(
            f"StudentsIntern: "
            f"{len(studentsintern_data)} records"
        )


    except Exception as error:

        print(
            "StudentsIntern scraper error:",
            error
        )


    # ========================================================
    # THE MUSE
    # ========================================================

    try:

        themuse_data = scrape_themuse()


        all_internships.extend(
            themuse_data
        )


        print(
            f"The Muse: "
            f"{len(themuse_data)} records"
        )


    except Exception as error:

        print(
            "The Muse scraper error:",
            error
        )


    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    all_internships = remove_duplicates(
        all_internships
    )


    # ========================================================
    # UPDATE CACHE
    # ========================================================

    CACHE["data"] = all_internships

    CACHE["timestamp"] = time.time()


    print(
        f"Cached "
        f"{len(all_internships)} "
        f"internships."
    )


    return all_internships


    # ========================================================
    # SAVE TO CACHE
    # ========================================================

    CACHE["data"] = all_internships

    CACHE["timestamp"] = current_time


    print(
        f"Cached "
        f"{len(all_internships)} "
        f"internships."
    )


    return all_internships


# ============================================================
# FILTER BY DOMAIN
# ============================================================

def filter_by_domain(
    internships,
    domain
):

    if (
        not domain
        or domain == "All Domains"
    ):

        return internships


    domain = domain.strip().lower()


    filtered = [

        internship

        for internship in internships

        if internship.get(
            "domain",
            ""
        ).strip().lower() == domain

    ]


    return filtered


# ============================================================
# FILTER BY SEARCH TEXT
# ============================================================

def filter_by_search(
    internships,
    search
):

    if not search:

        return internships


    search = search.strip().lower()


    if not search:

        return internships


    filtered = []


    for internship in internships:

        # ----------------------------------------------------
        # IMPORTANT:
        # Do NOT include source here.
        #
        # Otherwise:
        # searching "AI"
        # could match "AICTE".
        # ----------------------------------------------------

        searchable_text = " ".join([

            internship.get(
                "title",
                ""
            ),

            internship.get(
                "company",
                ""
            ),

            internship.get(
                "domain",
                ""
            ),

            internship.get(
                "location",
                ""
            )

        ]).lower()


        if search in searchable_text:

            filtered.append(
                internship
            )


    return filtered


# ============================================================
# FILTER BY LOCATION
# ============================================================

def filter_by_location(
    internships,
    location
):

    if not location:

        return internships


    location = location.strip().lower()


    if not location:

        return internships


    filtered = []


    for internship in internships:

        internship_location = internship.get(
            "location",
            ""
        ).lower()


        if location in internship_location:

            filtered.append(
                internship
            )


    return filtered


# ============================================================
# FILTER BY WORK MODE
# ============================================================

def filter_by_work_mode(
    internships,
    work_mode
):

    if (
        not work_mode
        or work_mode == "All"
    ):

        return internships


    work_mode = work_mode.strip().lower()


    filtered = []


    for internship in internships:

        internship_type = internship.get(
            "type",
            ""
        ).lower()


        internship_location = internship.get(
            "location",
            ""
        ).lower()


        combined_text = (
            internship_type
            + " "
            + internship_location
        )


        # ----------------------------------------------------
        # Remote
        # ----------------------------------------------------

        if work_mode == "remote":

            if any(

                word in combined_text

                for word in [

                    "remote",
                    "virtual",
                    "work from home",
                    "wfh"

                ]

            ):

                filtered.append(
                    internship
                )


        # ----------------------------------------------------
        # On-site
        # ----------------------------------------------------

        elif work_mode == "on-site":

            if not any(

                word in combined_text

                for word in [

                    "remote",
                    "virtual",
                    "work from home",
                    "wfh"

                ]

            ):

                filtered.append(
                    internship
                )


        # ----------------------------------------------------
        # Hybrid
        # ----------------------------------------------------

        elif work_mode == "hybrid":

            if "hybrid" in combined_text:

                filtered.append(
                    internship
                )


    return filtered


# ============================================================
# FINAL FILTERING FUNCTION
# ============================================================

def get_internships(
    domain="All Domains",
    search="",
    location="",
    work_mode="All"
):

    # --------------------------------------------------------
    # Get all source data
    # --------------------------------------------------------

    internships = get_all_internships()


    # --------------------------------------------------------
    # Domain
    # --------------------------------------------------------

    internships = filter_by_domain(
        internships,
        domain
    )


    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    internships = filter_by_search(
        internships,
        search
    )


    # --------------------------------------------------------
    # Location
    # --------------------------------------------------------

    internships = filter_by_location(
        internships,
        location
    )


    # --------------------------------------------------------
    # Work Mode
    # --------------------------------------------------------

    internships = filter_by_work_mode(
        internships,
        work_mode
    )


    return internships


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    data = get_internships()


    print(
        "\n=========================================="
    )

    print(
        "INTERNHUB MULTI-SOURCE AGGREGATOR"
    )

    print(
        "=========================================="
    )

    print(
        f"Total internships: {len(data)}"
    )

    print(
        "==========================================\n"
    )


    for index, internship in enumerate(
        data[:15],
        start=1
    ):

        print(
            f"{index}. {internship['title']}"
        )

        print(
            f"   Company: "
            f"{internship['company']}"
        )

        print(
            f"   Location: "
            f"{internship['location']}"
        )

        print(
            f"   Domain: "
            f"{internship['domain']}"
        )

        print(
            f"   Source: "
            f"{internship['source']}"
        )

        print(
            f"   URL: "
            f"{internship['url']}"
        )

        print(
            "------------------------------------------"
        )