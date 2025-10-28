from jobspy import scrape_jobs
from src.config import (
    SCRAPE_HOURS_OLD,
    SCRAPE_LOCATION,
    SCRAPE_RESULTS,
    SCRAPE_SITES,
    SCRAPE_TERM,
)
from src.models.job import Job
from src.services.job_service import JobService
from src.services.score_service import retrieve_job_score


def run_scraper(job_service: JobService):
    print("Scraping new jobs...")

    jobs_df = scrape_jobs(
        site_name=SCRAPE_SITES,
        search_term=SCRAPE_TERM,
        location=SCRAPE_LOCATION,
        results_wanted=SCRAPE_RESULTS,
        hours_old=SCRAPE_HOURS_OLD,
        country_indeed="France",
    )

    if jobs_df.empty:
        print("No jobs found.")
        return

    jobs_to_add = []
    for _, row in jobs_df.iterrows():
        score = retrieve_job_score(row.get("title", ""), row.get("description", ""))

        if score == 0:
            continue

        job = Job(
            title=row.get("title", ""),
            company=row.get("company", ""),
            location=row.get("location", ""),
            site=row.get("site", ""),
            url=row.get("job_url", ""),
            job_type=row.get("job_type", ""),
            description=row.get("description", ""),
            score=score,
        )
        jobs_to_add.append(job)

    saved = job_service.add_jobs_batch(jobs_to_add)
    print(f"Added {len(saved)} new jobs to database")
