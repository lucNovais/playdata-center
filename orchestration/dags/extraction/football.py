from datetime import timedelta

from airflow.sdk import DAG
from common.operators import python_job

with DAG(
    dag_id="football_api_daily_extraction",
    schedule=None,
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
        "execution_timeout": timedelta(minutes=10),
    },
) as dag:
    api_to_raw = python_job(
        task_id="api_to_raw",
        job="playdata.jobs.extraction.football::FootballAPIToRaw",
        api_key="{{ var.value.FOOTBALL_API_KEY }}",
        base_url="v3.football.api-sports.io",
        endpoint="status",
    )
