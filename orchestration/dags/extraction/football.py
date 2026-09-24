import logging
from datetime import timedelta

from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG, chain

logger = logging.getLogger(__name__)

with DAG(
    dag_id="football_api_daily_extraction",
    schedule=None,
    catchup=False,
    default_args={
        "depends_on_past": False,
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
        "execution_timeout": timedelta(minutes=10),
    },
    tags=["api-sports"],
) as dag:

    def check_api_sports_status() -> None:
        from airflow.sdk import Variable

        from client.sports import APISports

        client = APISports(
            base_url="v3.football.api-sports.io",
            api_key=Variable.get("FOOTBALL_API_KEY"),
        )

        data = client.get_from_api(client.build_request_url("status"))
        logger.info("API-Sports status: %s", data)

    check_status = PythonOperator(
        task_id="check_api_sports_status", python_callable=check_api_sports_status
    )

    chain(check_api_sports_status)
