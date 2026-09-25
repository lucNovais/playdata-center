import importlib
from typing import Any

from airflow.providers.standard.operators.python import PythonOperator


def _run_job(job: str, params: dict[str, Any]) -> None:
    module_path, class_name = job.split("::")

    job_cls = getattr(importlib.import_module(module_path), class_name)
    job_cls(**params).run()


def python_job(task_id: str, job: str, **params: Any) -> PythonOperator:
    return PythonOperator(
        task_id=task_id,
        python_callable=_run_job,
        op_kwargs={
            "job": job,
            "params": params,
        },
    )
