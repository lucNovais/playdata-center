import logging
from datetime import timedelta

from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG

logger = logging.getLogger(__name__)


def give_welcome_message() -> None:
    logger.info("Hello, world!")


def give_goodbye_message() -> None:
    logger.info("Until next time!")


with DAG(
    dag_id="test_dag",
    default_args={
        "depends_on_past": False,
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
        "execution_timeout": timedelta(minutes=10),
    },
) as dag:
    first_task = PythonOperator(
        task_id="give_welcome_message",
        python_callable=give_welcome_message,
    )

    second_task = PythonOperator(
        task_id="give_goodbye_message",
        python_callable=give_goodbye_message,
    )

    first_task >> second_task
