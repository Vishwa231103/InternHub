from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.aggregator import get_internships


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="InternHub API",
    description="Internship aggregation API",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://intern-hub-ashen.vercel.app",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "InternHub Backend is running!"
    }


# ============================================================
# INTERNSHIPS API
# ============================================================

@app.get("/api/internships")
def internships_api(

    domain: str = "All Domains",

    search: str = "",

    location: str = "",

    work_mode: str = "All"

):

    print("\n==========================================")
    print("INTERNSHIP API REQUEST")
    print("==========================================")

    print("Domain    :", domain)
    print("Search    :", search)
    print("Location  :", location)
    print("Work Mode :", work_mode)

    print("==========================================\n")


    try:

        internships = get_internships(

            domain=domain,

            search=search,

            location=location,

            work_mode=work_mode

        )


        print(
            f"Returning {len(internships)} internships."
        )


        return {

            "success": True,

            "count": len(
                internships
            ),

            "filters": {

                "domain": domain,

                "search": search,

                "location": location,

                "work_mode": work_mode

            },

            "data": internships

        }


    except Exception as error:

        print(
            "Aggregator error:",
            error
        )


        return {

            "success": False,

            "count": 0,

            "filters": {

                "domain": domain,

                "search": search,

                "location": location,

                "work_mode": work_mode

            },

            "data": [],

            "error":
                "Unable to fetch internships"

        }
