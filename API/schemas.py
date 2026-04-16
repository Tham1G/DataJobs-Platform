from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class JobOut(BaseModel):
    job_id: Optional[int] = None
    company_id: Optional[int] = None
    company_name: Optional[str] = None

    job_title: Optional[str] = None
    job_title_short: Optional[str] = None
    job_location: Optional[str] = None
    job_country: Optional[str] = None

    job_schedule_type: Optional[str] = None
    job_work_from_home: Optional[bool] = None

    salary_year_avg: Optional[float] = None
    salary_hour_avg: Optional[float] = None
    salary_rate: Optional[str] = None

    job_posted_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class SkillSalaryOut(BaseModel):
    skill: str
    avg_salary: float
    job_count: int


class SkillDemandOut(BaseModel):
    skill: str
    demand_count: int


class CompanyOut(BaseModel):
    company_id: int
    name: Optional[str] = None
    link: Optional[str] = None
    link_google: Optional[str] = None
    thumbnail: Optional[str] = None

    class Config:
        from_attributes = True