from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from .database import get_db
from . import crud, schemas

app = FastAPI(
    title="Job Data API",
    version="1.0.0",
    description="API for querying and analyzing the jobdata SQL Server database"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Job Data API is running"}


# -----------------------------
# Jobs routes
# -----------------------------

@app.get("/jobs", response_model=List[schemas.JobOut])
def read_jobs(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return crud.get_jobs(db, skip=skip, limit=limit)


@app.get("/jobs/search", response_model=List[schemas.JobOut])
def search_jobs(
    title: Optional[str] = None,
    location: Optional[str] = None,
    country: Optional[str] = None,
    work_from_home: Optional[bool] = None,
    min_salary: Optional[float] = None,
    max_salary: Optional[float] = None,
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return crud.search_jobs(
        db=db,
        title=title,
        location=location,
        country=country,
        work_from_home=work_from_home,
        min_salary=min_salary,
        max_salary=max_salary,
        limit=limit,
    )


@app.get("/jobs/top-paying", response_model=List[schemas.JobOut])
def top_paying_jobs(
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return crud.get_top_paying_jobs(db, limit=limit)


# Keep /jobs/{job_id} AFTER the more specific /jobs/... routes
@app.get("/jobs/{job_id}", response_model=schemas.JobOut)
def read_job(job_id: int, db: Session = Depends(get_db)):
    job = crud.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


# -----------------------------
# Skills / analytics routes
# -----------------------------

@app.get("/skills/top-paying", response_model=List[schemas.SkillSalaryOut])
def top_paying_skills(
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return crud.get_top_paying_skills(db, limit=limit)


@app.get("/skills/most-demanded", response_model=List[schemas.SkillDemandOut])
def most_demanded_skills(
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return crud.get_most_demanded_skills(db, limit=limit)


@app.get("/analytics/top-skills-by-title", response_model=List[schemas.SkillDemandOut])
def top_skills_by_title(
    title: str,
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return crud.get_top_skills_by_title(db, title=title, limit=limit)


# -----------------------------
# Company routes
# -----------------------------

@app.get("/companies", response_model=List[schemas.CompanyOut])
def read_companies(
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    return crud.get_companies(db, limit=limit)


@app.get("/companies/{company_id}/jobs", response_model=List[schemas.JobOut])
def jobs_by_company(
    company_id: int,
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    return crud.get_jobs_by_company(db, company_id=company_id, limit=limit)