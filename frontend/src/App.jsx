import { useState } from "react";
import ThreeBackground from "./ThreeBackground";
import "./App.css";

function App() {
  // ============================================================
  // STATES
  // ============================================================

  const [domain, setDomain] = useState("All Domains");
  const [workMode, setWorkMode] = useState("All");
  const [source, setSource] = useState("All Sources");

  const [internships, setInternships] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [count, setCount] = useState(0);

  // ============================================================
  // DOMAIN LIST
  // ============================================================

  const domains = [
    "All Domains",
    "Python",
    "Java",
    "Web Development",
    "React",
    "Data Science",
    "AI / ML",
    "Cybersecurity",
    "Cloud",
    "DevOps",
    "Android",
    "Embedded Systems",
    "UI / UX",
    "Digital Marketing",
    "Other",
  ];

  // ============================================================
  // WORK MODE LIST
  // ============================================================

  const workModes = [
    "All",
    "Remote",
    "On-site",
    "Hybrid",
  ];

  // ============================================================
  // SOURCE LIST
  // ============================================================

  const sources = [
    "All Sources",
    "AICTE",
    "StudentsIntern",
    "The Muse",
    "Remotive",
  ];

  // ============================================================
  // FIND INTERNSHIPS
  // ============================================================

  const findInternships = async () => {
    setLoading(true);
    setError("");
    setInternships([]);
    setCount(0);

    try {
      // --------------------------------------------------------
      // BUILD API PARAMETERS
      // --------------------------------------------------------

      const params = new URLSearchParams();

      // Domain
      if (domain !== "All Domains") {
        params.append("domain", domain);
      }

      // Work Mode
      if (workMode !== "All") {
        params.append("work_mode", workMode);
      }

      // --------------------------------------------------------
      // BUILD FINAL API URL
      // --------------------------------------------------------

      const baseUrl =
        "https://internhub-backend-dpo9.onrender.com/api/internships";

      const url = params.toString()
        ? `${baseUrl}?${params.toString()}`
        : baseUrl;

      console.log(
        "Fetching internships from:",
        url
      );

      // --------------------------------------------------------
      // API REQUEST
      // --------------------------------------------------------

      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(
          `Server returned ${response.status}`
        );
      }

      const result = await response.json();

      console.log(
        "API Response:",
        result
      );

      // --------------------------------------------------------
      // API ERROR
      // --------------------------------------------------------

      if (!result.success) {
        throw new Error(
          result.error ||
            "Unable to fetch internships"
        );
      }

      // --------------------------------------------------------
      // GET RESULTS
      // --------------------------------------------------------

      const results = Array.isArray(
        result.data
      )
        ? result.data
        : [];

      // --------------------------------------------------------
      // SOURCE FILTER
      // --------------------------------------------------------

      const filteredResults =
        source === "All Sources"
          ? results
          : results.filter(
              (internship) =>
                internship.source === source
            );

      // --------------------------------------------------------
      // SET RESULTS
      // --------------------------------------------------------

      setInternships(
        filteredResults
      );

      setCount(
        filteredResults.length
      );

    } catch (err) {
      console.error(
        "Internship fetch error:",
        err
      );

      setInternships([]);
      setCount(0);

      setError(
        "Unable to fetch internships. Please check whether the backend server is running."
      );

    } finally {
      setLoading(false);
    }
  };

  // ============================================================
  // CLEAR FILTERS
  // ============================================================

  const clearFilters = () => {
    setDomain("All Domains");
    setWorkMode("All");
    setSource("All Sources");

    setInternships([]);
    setCount(0);
    setError("");
  };

  // ============================================================
  // CHECK WHETHER FILTERS ARE ACTIVE
  // ============================================================

  const hasFilters =
    domain !== "All Domains" ||
    workMode !== "All" ||
    source !== "All Sources";

  // ============================================================
  // UI
  // ============================================================

  return (
    <div className="app">

      {/* ======================================================
          NAVBAR
      ====================================================== */}

      <nav className="navbar">

        <div className="logo">
          Intern<span>Hub</span>
        </div>

        <div className="nav-links">

          <a href="#home">
            Home
          </a>

          <a href="#internships">
            Internships
          </a>

          <a href="#about">
            About
          </a>

        </div>

      </nav>


      {/* ======================================================
          HERO
      ====================================================== */}

      <section
        className="hero"
        id="home"
      >

        <ThreeBackground />

        <div className="hero-content">

          {/* TAGLINE */}

          <p className="tagline">
            🚀 Your Internship Search Starts Here
          </p>


          {/* TITLE */}

          <h1>
            Find Your
            <span>
              Dream Internship
            </span>
          </h1>


          {/* DESCRIPTION */}

          <p className="description">
            Discover internships from multiple platforms
            in one place.
          </p>


          {/* ==================================================
              SEARCH AREA
          ================================================== */}

          <div className="search-box">

            {/* DOMAIN */}

            <select
              value={domain}
              onChange={(e) =>
                setDomain(e.target.value)
              }
            >

              {domains.map((item) => (
                <option
                  key={item}
                  value={item}
                >
                  {item}
                </option>
              ))}

            </select>


            {/* WORK MODE */}

            <select
              value={workMode}
              onChange={(e) =>
                setWorkMode(e.target.value)
              }
            >

              {workModes.map((mode) => (
                <option
                  key={mode}
                  value={mode}
                >
                  {mode}
                </option>
              ))}

            </select>


            {/* SOURCE */}

            <select
              value={source}
              onChange={(e) =>
                setSource(e.target.value)
              }
            >

              {sources.map((item) => (
                <option
                  key={item}
                  value={item}
                >
                  {item}
                </option>
              ))}

            </select>


            {/* FIND BUTTON */}

            <button
              onClick={findInternships}
              disabled={loading}
            >

              {loading
                ? "🔄 Searching..."
                : "🔍 Find Internships"}

            </button>


            {/* CLEAR BUTTON */}

            {hasFilters && (
              <button
                className="clear-btn"
                onClick={clearFilters}
                disabled={loading}
              >
                ✕ Clear
              </button>
            )}

          </div>

        </div>

      </section>


      {/* ======================================================
          RESULTS
      ====================================================== */}

      <section
        className="results"
        id="internships"
      >

        {/* ==================================================
            RESULTS HEADER
        ================================================== */}

        <div className="results-header">

          <div>

            <h2>
              Internship Opportunities
            </h2>

            <p>

              {count > 0
                ? `${count} internships found`
                : "Explore opportunities from multiple platforms"}

            </p>

          </div>


          {/* ==================================================
              ACTIVE FILTER INFO
          ================================================== */}

          {hasFilters && (
            <div className="active-filters">

              {domain !== "All Domains" && (
                <span>
                  🏷️ {domain}
                </span>
              )}

              {workMode !== "All" && (
                <span>
                  💻 {workMode}
                </span>
              )}

              {source !== "All Sources" && (
                <span>
                  🌐 {source}
                </span>
              )}

            </div>
          )}

        </div>


        {/* ==================================================
            RESULTS GRID
        ================================================== */}

        <div className="internship-grid">

          {/* ==================================================
              LOADING
          ================================================== */}

          {loading && (
            <p className="status-message">
              🔍 Searching for internships...
            </p>
          )}


          {/* ==================================================
              ERROR
          ================================================== */}

          {!loading && error && (
            <p className="status-message error">
              {error}
            </p>
          )}


          {/* ==================================================
              RESULTS
          ================================================== */}

          {!loading &&
            !error &&
            internships.length > 0 &&
            internships.map(
              (internship, index) => (

                <div
                  className="internship-card"
                  key={
                    internship.url ||
                    `${internship.title || "internship"}-${index}`
                  }
                >

                  {/* SOURCE */}

                  <div className="card-top">

                    <span className="source">
                      {internship.source ||
                        "InternHub"}
                    </span>

                  </div>


                  {/* TITLE */}

                  <h3>
                    {internship.title ||
                      "Internship Opportunity"}
                  </h3>


                  {/* COMPANY */}

                  <p className="company">
                    {internship.company ||
                      "Company not specified"}
                  </p>


                  {/* LOCATION + TYPE */}

                  <div className="details">

                    <span>
                      📍{" "}
                      {internship.location ||
                        "Location not specified"}
                    </span>

                    <span>
                      💼{" "}
                      {internship.type ||
                        "Internship"}
                    </span>

                  </div>


                  {/* SALARY + DOMAIN */}

                  <div className="details">

                    <span>
                      💰{" "}
                      {internship.salary ||
                        "Not specified"}
                    </span>

                    <span>
                      🏷️{" "}
                      {internship.domain ||
                        "Other"}
                    </span>

                  </div>


                  {/* DURATION + APPLY DATE */}

                  <div className="details">

                    {internship.duration && (
                      <span>
                        ⏱️{" "}
                        {internship.duration}
                      </span>
                    )}

                    {internship.apply_by && (
                      <span>
                        📅 Apply by:{" "}
                        {internship.apply_by}
                      </span>
                    )}

                  </div>


                  {/* POSTED DATE */}

                  {internship.posted_date && (
                    <div className="details">

                      <span>
                        🕒 Posted:{" "}
                        {internship.posted_date}
                      </span>

                    </div>
                  )}


                  {/* START DATE */}

                  {internship.start_date && (
                    <div className="details">

                      <span>
                        🚀 Start:{" "}
                        {internship.start_date}
                      </span>

                    </div>
                  )}


                  {/* OPENINGS */}

                  {internship.openings && (
                    <div className="details">

                      <span>
                        👥 Openings:{" "}
                        {internship.openings}
                      </span>

                    </div>
                  )}


                  {/* APPLY BUTTON */}

                  {internship.url && (
                    <a
                      href={internship.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="apply-btn"
                    >
                      Apply Now →
                    </a>
                  )}

                </div>

              )
            )}


          {/* ==================================================
              NO RESULTS AFTER FILTER
          ================================================== */}

          {!loading &&
            !error &&
            internships.length === 0 &&
            hasFilters && (

              <p className="status-message">

                {source !== "All Sources" ? (
                  <>
                    ❌ No internships available from{" "}
                    <strong>
                      {source}
                    </strong>{" "}
                    right now.

                    <br />

                    Try selecting another source
                    or choose{" "}
                    <strong>
                      All Sources
                    </strong>.
                  </>
                ) : (
                  <>
                    ❌ No internships found for
                    the selected filters.

                    <br />

                    Try changing the domain
                    or work mode.
                  </>
                )}

              </p>

            )}


          {/* ==================================================
              INITIAL STATE
          ================================================== */}

          {!loading &&
            !error &&
            internships.length === 0 &&
            !hasFilters && (

              <p className="status-message">

                Select a domain, work mode or source
                and click{" "}

                <strong>
                  "Find Internships"
                </strong>

                {" "}to search.

              </p>

            )}

        </div>

      </section>


      {/* ======================================================
          FOOTER
      ====================================================== */}

      <footer>

        <p>
          © 2026 InternHub —
          Internship Discovery Platform
        </p>

      </footer>

    </div>
  );
}

export default App;
