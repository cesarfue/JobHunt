from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class JobStatus(Enum):
    PENDING = "pending"
    WIP = "wip"
    APPLIED = "applied"
    DISCARDED = "discarded"


@dataclass
class Job:
    title: str
    company: str
    url: str
    site: str = ""
    location: str = ""
    job_type: str = ""
    description: str = ""
    score: float = 0.5
    status: JobStatus = JobStatus.PENDING
    date_added: Optional[datetime] = None
    id: Optional[int] = None

    def __post_init__(self):
        if isinstance(self.status, str):
            self.status = JobStatus(self.status.lower())

        if self.date_added is None:
            self.date_added = datetime.now()
        elif isinstance(self.date_added, str):
            self.date_added = datetime.fromisoformat(self.date_added)

    @property
    def is_pending(self) -> bool:
        return self.status == JobStatus.PENDING

    @property
    def is_wip(self) -> bool:
        return self.status == JobStatus.WIP

    @property
    def is_applied(self) -> bool:
        return self.status == JobStatus.APPLIED

    @property
    def is_discarded(self) -> bool:
        return self.status == JobStatus.DISCARDED

    def mark_wip(self):
        self.status = JobStatus.WIP

    def mark_applied(self):
        self.status = JobStatus.APPLIED

    def mark_discarded(self):
        self.status = JobStatus.DISCARDED

    def mark_pending(self):
        self.status = JobStatus.PENDING

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "url": self.url,
            "site": self.site,
            "location": self.location,
            "job_type": self.job_type,
            "description": self.description,
            "score": self.score,
            "status": self.status.value,
            "date_added": self.date_added.isoformat() if self.date_added else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Job":
        return cls(
            id=data.get("id"),
            title=data.get("title", ""),
            company=data.get("company", ""),
            url=data.get("url", ""),
            site=data.get("site", ""),
            location=data.get("location", ""),
            job_type=data.get("job_type", ""),
            description=data.get("description", ""),
            score=data.get("score", 0.5),
            status=data.get("status", "pending"),
            date_added=data.get("date_added"),
        )

    @classmethod
    def from_row(cls, row: tuple) -> "Job":
        if len(row) == 7:
            return cls(
                id=row[0],
                title=row[1],
                company=row[2],
                site=row[3],
                location=row[4],
                url="",
                date_added=row[5],
                status=row[6],
            )
        elif len(row) >= 5:
            return cls(
                id=row[0],
                title=row[1],
                company=row[2],
                site=row[3],
                location=row[4],
                url=row[5] if len(row) > 5 else "",
                status=row[6] if len(row) > 6 else "pending",
            )
        else:
            raise ValueError(f"Invalid row format: {row}")
