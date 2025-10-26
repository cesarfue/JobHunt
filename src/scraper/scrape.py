from jobspy import scrape_jobs

from db.db import init_db, insert_jobs


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

    if not job_dicts:
        print("No valid jobs to insert (all missing URLs).")
        return

    insert_jobs(job_dicts)
    print(f"Inserted {len(job_dicts)} jobs (duplicates ignored).")


if __name__ == "__main__":
    run_scraper()
