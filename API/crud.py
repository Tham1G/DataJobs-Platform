from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from . import models


def to_job_out(job: models.JobPostingFact):
    return {
        "job_id": job.job_id,
        "company_id": job.company_id,
        "company_name": job.company.name if job.company else None,
        "job_title": job.job_title,
        "job_title_short": job.job_title_short,
        "job_location": job.job_location,
        "job_country": job.job_country,
        "job_schedule_type": job.job_schedule_type,
        "job_work_from_home": job.job_work_from_home,
        "salary_year_avg": float(job.salary_year_avg) if job.salary_year_avg is not None else None,
        "salary_hour_avg": float(job.salary_hour_avg) if job.salary_hour_avg is not None else None,
        "salary_rate": job.salary_rate,
        "job_posted_date": job.job_posted_date,
    }


def get_jobs(db: Session, skip: int = 0, limit: int = 20):
    jobs = (
        db.query(models.JobPostingFact)
        .options(joinedload(models.JobPostingFact.company))
        .order_by(models.JobPostingFact.job_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [to_job_out(job) for job in jobs]


def get_job_by_id(db: Session, job_id: int):
    job = (
        db.query(models.JobPostingFact)
        .options(joinedload(models.JobPostingFact.company))
        .filter(models.JobPostingFact.job_id == job_id)
        .first()
    )
    if not job:
        return None
    return to_job_out(job)


def search_jobs(
    db: Session,
    title: str | None = None,
    location: str | None = None,
    country: str | None = None,
    work_from_home: bool | None = None,
    min_salary: float | None = None,
    max_salary: float | None = None,
    limit: int = 20
):
    query = (
        db.query(models.JobPostingFact)
        .options(joinedload(models.JobPostingFact.company))
    )

    if title:
        query = query.filter(models.JobPostingFact.job_title.ilike(f"%{title}%"))

    if location:
        query = query.filter(models.JobPostingFact.job_location.ilike(f"%{location}%"))

    if country:
        query = query.filter(models.JobPostingFact.job_country.ilike(f"%{country}%"))

    if work_from_home is not None:
        query = query.filter(models.JobPostingFact.job_work_from_home == work_from_home)

    if min_salary is not None:
        query = query.filter(models.JobPostingFact.salary_year_avg >= min_salary)

    if max_salary is not None:
        query = query.filter(models.JobPostingFact.salary_year_avg <= max_salary)

    jobs = (
        query
        .order_by(models.JobPostingFact.job_id)
        .limit(limit)
        .all()
    )
    return [to_job_out(job) for job in jobs]


def get_top_paying_jobs(db: Session, limit: int = 10):
    jobs = (
        db.query(models.JobPostingFact)
        .options(joinedload(models.JobPostingFact.company))
        .filter(models.JobPostingFact.salary_year_avg.isnot(None))
        .order_by(desc(models.JobPostingFact.salary_year_avg), models.JobPostingFact.job_id)
        .limit(limit)
        .all()
    )
    return [to_job_out(job) for job in jobs]


def get_top_paying_skills(db: Session, limit: int = 10):
    rows = (
        db.query(
            models.SkillsDim.skills.label("skill"),
            func.avg(models.JobPostingFact.salary_year_avg).label("avg_salary"),
            func.count(models.JobPostingFact.job_id).label("job_count")
        )
        .join(models.SkillsJobDim, models.SkillsDim.skill_id == models.SkillsJobDim.skill_id)
        .join(models.JobPostingFact, models.SkillsJobDim.job_id == models.JobPostingFact.job_id)
        .filter(models.JobPostingFact.salary_year_avg.isnot(None))
        .group_by(models.SkillsDim.skills)
        .order_by(desc(func.avg(models.JobPostingFact.salary_year_avg)), models.SkillsDim.skills)
        .limit(limit)
        .all()
    )

    return [
        {
            "skill": row.skill,
            "avg_salary": float(row.avg_salary),
            "job_count": row.job_count,
        }
        for row in rows
    ]


def get_most_demanded_skills(db: Session, limit: int = 10):
    rows = (
        db.query(
            models.SkillsDim.skills.label("skill"),
            func.count(models.SkillsJobDim.job_id).label("demand_count")
        )
        .join(models.SkillsJobDim, models.SkillsDim.skill_id == models.SkillsJobDim.skill_id)
        .group_by(models.SkillsDim.skills)
        .order_by(desc(func.count(models.SkillsJobDim.job_id)), models.SkillsDim.skills)
        .limit(limit)
        .all()
    )

    return [
        {
            "skill": row.skill,
            "demand_count": row.demand_count,
        }
        for row in rows
    ]


def get_jobs_by_company(db: Session, company_id: int, limit: int = 50):
    jobs = (
        db.query(models.JobPostingFact)
        .options(joinedload(models.JobPostingFact.company))
        .filter(models.JobPostingFact.company_id == company_id)
        .order_by(models.JobPostingFact.job_id)
        .limit(limit)
        .all()
    )
    return [to_job_out(job) for job in jobs]


def get_companies(db: Session, limit: int = 50):
    return (
        db.query(models.CompanyDim)
        .order_by(models.CompanyDim.company_id)
        .limit(limit)
        .all()
    )


def get_top_skills_by_title(db: Session, title: str, limit: int = 20):
    rows = (
        db.query(
            models.SkillsDim.skills.label("skill"),
            func.count(models.SkillsJobDim.job_id).label("demand_count")
        )
        .join(models.SkillsJobDim, models.SkillsDim.skill_id == models.SkillsJobDim.skill_id)
        .join(models.JobPostingFact, models.SkillsJobDim.job_id == models.JobPostingFact.job_id)
        .filter(models.JobPostingFact.job_title.ilike(f"%{title}%"))
        .group_by(models.SkillsDim.skills)
        .order_by(desc(func.count(models.SkillsJobDim.job_id)), models.SkillsDim.skills)
        .limit(limit)
        .all()
    )

    return [
        {
            "skill": row.skill,
            "demand_count": row.demand_count,
        }
        for row in rows
    ]