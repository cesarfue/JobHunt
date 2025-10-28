from typing import List, Optional

import requests
from src.config import API_URL
from src.models.job import Job, JobStatus
from src.repository.job_repository import JobRepository


class JobService:

    def __init__(self, repository: Optional[JobRepository] = None):
        self.repository = repository or JobRepository()
        self.api_url = API_URL

    def get_job(self, job_id: int) -> Optional[Job]:
        return self.repository.find_by_id(job_id)

    def get_all_jobs(self, include_discarded: bool = False) -> List[Job]:
        return self.repository.find_all(include_discarded)

    def get_pending_jobs(self, order: str = "DESC") -> List[Job]:
        return self.repository.find_pending_and_wip(order)

    def get_statistics(self) -> dict:
        counts = self.repository.count_by_status()
        return {
            "pending": counts.get("pending", 0),
            "wip": counts.get("wip", 0),
            "applied": counts.get("applied", 0),
            "discarded": counts.get("discarded", 0),
            "total": sum(counts.values()),
        }

    def add_job(self, job: Job) -> Job:
        return self.repository.save(job)

    def add_jobs_batch(self, jobs: List[Job]) -> List[Job]:
        return self.repository.save_many(jobs)

    def mark_as_pending(self, job_id: int) -> Optional[Job]:
        job = self.repository.find_by_id(job_id)
        if job:
            job.mark_pending()
            return self.repository.save(job)
        return None

    def mark_as_wip(self, job_id: int) -> Optional[Job]:
        job = self.repository.find_by_id(job_id)
        if job:
            job.mark_wip()
            return self.repository.save(job)
        return None

    def mark_as_applied(self, job_id: int) -> Optional[Job]:
        job = self.repository.find_by_id(job_id)
        if job:
            job.mark_applied()
            return self.repository.save(job)
        return None

    def mark_as_discarded(self, job_id: int) -> Optional[Job]:
        job = self.repository.find_by_id(job_id)
        if job:
            job.mark_discarded()
            return self.repository.save(job)
        return None

    def apply_to_job(self, job: Job) -> bool:
        print(f"\nApplying to {job.company} - {job.title}...")

        try:
            response = requests.post(
                self.api_url,
                json={
                    "url": job.url,
                    "description": job.description,
                    "company": job.company,
                },
                timeout=60,
            )

            if response.status_code == 200:
                job.mark_wip()
                self.repository.save(job)
                return True

            return False

        except requests.exceptions.RequestException as e:
            print(f"Error while sending {job.url}: {e}")
            return False
