from datetime import timedelta

from airflow.sdk import DAG
from common.operators import python_job
from extraction.football.constants import SUPPORT_YAML_PATH
from extraction.utils import read_yaml_file

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
    support_data: dict = read_yaml_file(path=SUPPORT_YAML_PATH)

    api_version: str = support_data["api_version"]
    api_url: str = support_data["api_url"]
    endpoints: list[str] = list(support_data["support_endpoints"].keys())

    api_to_raw = python_job(
        task_id="api_to_raw",
        job="playdata.jobs.extraction.api_football_support::APIFootballSupport",
        api_key="{{ var.value.FOOTBALL_API_KEY }}",
        api_version=api_version,
        base_url=f"{api_version}.{api_url}/",
        endpoints=endpoints,
    )
