"""BATCH: load the 3 CSV files into the raw schema."""
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from db import get_conn


def load_csv(table):
    conn = get_conn()
    with conn, conn.cursor() as cur, open(f"/opt/airflow/data/{table}.csv", encoding="utf-8") as f:
        columns = f.readline().strip()   # first line = column names
        f.seek(0)
        cur.execute(f"TRUNCATE raw.{table}")   # reload from scratch = safe to re-run
        cur.copy_expert(f"COPY raw.{table} ({columns}) FROM STDIN WITH CSV HEADER", f)
    conn.close()
    print(f"raw.{table} loaded")


with DAG(
    dag_id="2_batch",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["bim"],
) as dag:
    for table in ["stores", "products", "promotions"]:
        PythonOperator(task_id=f"load_{table}", python_callable=load_csv, op_args=[table])