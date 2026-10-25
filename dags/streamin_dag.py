"""STREAMING: every minute, call an API and store the answer in raw.checkouts."""
import os
import random
from datetime import datetime

import requests
from airflow import DAG
from airflow.operators.python import PythonOperator

from db import get_conn


def pull_checkouts():
    # ONE simple call: the API returns 10 fake shopping carts
    url = f"https://dummyjson.com/carts?limit=10&skip={random.randint(0, 190)}"
    verify = os.environ.get("VERIFY_SSL", "true") == "true"   # see README if your network blocks HTTPS
    carts = requests.get(url, timeout=10, verify=verify).json()["carts"]

    now = datetime.utcnow()
    conn = get_conn()
    with conn, conn.cursor() as cur:
        for cart in carts:
            order_id = f"chk_{now:%Y%m%d%H%M%S}_{cart['id']}"
            store_id = cart["userId"] % 6 + 1                  # API user -> one of our 6 BIM stores
            for item in cart["products"]:
                product_id = (item["id"] - 1) % 25 + 1         # API product -> one of our 25 BIM products
                cur.execute(
                    "INSERT INTO raw.checkouts VALUES (%s, %s, %s, %s, %s)",
                    [order_id, store_id, now, product_id, item["quantity"]],
                )
    conn.close()
    print(f"{len(carts)} checkouts saved in raw.checkouts")


with DAG(
    dag_id="1_streaming",
    schedule="* * * * *",          # every minute
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["bim"],
) as dag:
    PythonOperator(task_id="pull_checkouts", python_callable=pull_checkouts)