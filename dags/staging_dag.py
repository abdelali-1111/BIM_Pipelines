"""STAGING: wait for streaming + batch, then raw -> staging. Then starts the marts DAG."""
from datetime import datetime

from airflow import DAG
from airflow.models import DagRun
from airflow.models.baseoperator import cross_downstream
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sensors.python import PythonSensor

from db import run_sql_file


def has_succeeded(dag_id):
    """True once the given DAG has at least one successful run."""
    return len(DagRun.find(dag_id=dag_id, state="success")) > 0


with DAG(
    dag_id="3_staging",
    schedule="*/2 * * * *",        # every 2 minutes
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["bim"],
) as dag:
    waits = [
        PythonSensor(
            task_id=f"wait_{name}",
            python_callable=has_succeeded,
            op_args=[dag_id],
            mode="reschedule",
            poke_interval=10,
            timeout=90,
            soft_fail=True,        # nothing to stage yet -> skip this run, try again in 2 min
        )
        for name, dag_id in [("streaming", "1_streaming"), ("batch", "2_batch")]
    ]

    staging_tasks = [
        PythonOperator(task_id=f"stg_{name}", python_callable=run_sql_file, op_args=[f"staging/{name}.sql"])
        for name in ["stores", "products", "promotions", "checkouts"]
    ]

    start_marts = TriggerDagRunOperator(task_id="start_marts", trigger_dag_id="4_marts")

    cross_downstream(waits, staging_tasks)   # every wait -> every staging task
    staging_tasks >> start_marts