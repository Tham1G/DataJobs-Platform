from sqlalchemy import inspect, MetaData
from .database import engine

REQUIRED_SCHEMA = {
    "company_dim": {"company_id", "name"},
    "skills_dim": {"skill_id", "skills"},
    "job_postings_fact": {
        "job_id",
        "company_id",
        "job_title",
        "job_title_short",
        "job_location",
        "job_schedule_type",
        "salary_year_avg",
        "job_posted_date",
    },
    "skills_job_dim": {"job_id", "skill_id"},
}


def validate_schema():
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    missing_tables = [table for table in REQUIRED_SCHEMA if table not in existing_tables]
    if missing_tables:
        raise RuntimeError(
            f"Missing required tables: {', '.join(missing_tables)}"
        )

    for table_name, required_columns in REQUIRED_SCHEMA.items():
        actual_columns = {
            col["name"] for col in inspector.get_columns(table_name)
        }
        missing_columns = required_columns - actual_columns
        if missing_columns:
            raise RuntimeError(
                f"Table '{table_name}' is missing required columns: "
                f"{', '.join(sorted(missing_columns))}"
            )


def reflect_tables():
    metadata = MetaData()
    metadata.reflect(
        bind=engine,
        only=[
            "company_dim",
            "skills_dim",
            "job_postings_fact",
            "skills_job_dim"
        ]
    )
    return metadata.tables