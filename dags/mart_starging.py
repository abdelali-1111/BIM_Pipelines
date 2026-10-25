"""MARTS: staging -> mart (business tables). Started by the staging DAG, no schedule of its own."""
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from db import run_sql_file


def sql_task(name):
    return PythonOperator(task_id=name, python_callable=run_sql_file, op_args=[f"mart/{name}.sql"])


with DAG(
    dag_id="4_marts",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["bim"],
) as dag:
    sales = sql_task("sales")
    sales >> [sql_task("revenue_by_store"), sql_task("top_products")]