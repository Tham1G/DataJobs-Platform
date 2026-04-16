from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class CompanyDim(Base):
    __tablename__ = "company_dim"

    company_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    link = Column(String, nullable=True)
    link_google = Column(String, nullable=True)
    thumbnail = Column(String, nullable=True)

    jobs = relationship("JobPostingFact", back_populates="company")


class JobPostingFact(Base):
    __tablename__ = "job_postings_fact"

    job_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("company_dim.company_id"), nullable=True)

    job_title_short = Column(String, nullable=True)
    job_title = Column(String, nullable=True)
    job_location = Column(String, nullable=True)
    job_via = Column(String, nullable=True)
    job_schedule_type = Column(String, nullable=True)
    job_work_from_home = Column(Boolean, nullable=True)
    search_location = Column(String, nullable=True)
    job_posted_date = Column(DateTime, nullable=True)
    job_no_degree_mention = Column(Boolean, nullable=True)
    job_health_insurance = Column(Boolean, nullable=True)
    job_country = Column(String, nullable=True)
    salary_rate = Column(String, nullable=True)
    salary_year_avg = Column(Float, nullable=True)
    salary_hour_avg = Column(Float, nullable=True)

    company = relationship("CompanyDim", back_populates="jobs")
    skill_links = relationship("SkillsJobDim", back_populates="job")


class SkillsDim(Base):
    __tablename__ = "skills_dim"

    skill_id = Column(Integer, primary_key=True, index=True)
    skills = Column(String, nullable=True)
    type = Column(String, nullable=True)

    job_links = relationship("SkillsJobDim", back_populates="skill")


class SkillsJobDim(Base):
    __tablename__ = "skills_job_dim"

    skill_id = Column(Integer, ForeignKey("skills_dim.skill_id"), primary_key=True)
    job_id = Column(Integer, ForeignKey("job_postings_fact.job_id"), primary_key=True)

    skill = relationship("SkillsDim", back_populates="job_links")
    job = relationship("JobPostingFact", back_populates="skill_links")