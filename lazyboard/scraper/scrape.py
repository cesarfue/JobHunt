from db.db import init_db, insert_jobs
from jobspy import scrape_jobs
from scraper.score import retrieve_job_score


def run_scraper():
    init_db()
    print("Scraping new jobs...")

    jobs = scrape_jobs(
        site_name=["indeed", "linkedin"],
        search_term="développeur",
        location="Lyon, France",
        results_wanted=30,
        hours_old=24,
        country_indeed="France",
    )

    if jobs.empty:
        print("No jobs found.")
        return

    columns_to_keep = [
        col
        for col in ["title", "company", "job_type", "site", "location", "job_url"]
        if col in jobs.columns
    ]
    filtered_jobs = jobs[columns_to_keep]
    job_dicts = filtered_jobs.to_dict(orient="records")
    for job in job_dicts:
        job["score"] = retrieve_job_score(job["title"])
    job_dicts = [job for job in job_dicts if job["score"] > 0]
    insert_jobs(job_dicts)


if __name__ == "__main__":
    run_scraper()
