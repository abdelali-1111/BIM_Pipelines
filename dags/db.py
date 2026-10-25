"""Tiny helpers shared by the 4 DAGs."""
import os

import psycopg2


def get_conn():
    return psycopg2.connect(
        host=os.environ["PG_HOST"],
        dbname=os.environ["PG_DB"],
        user=os.environ["PG_USER"],
        password=os.environ["PG_PASSWORD"],
    )


def run_sql_file(path):
    """Run one .sql file from the sql/ folder."""
    with open(f"/opt/airflow/sql/{path}", encoding="utf-8") as f:
        sql = f.read()
    conn = get_conn()
    with conn, conn.cursor() as cur:   # "with conn" = commit at the end
        cur.execute(sql)
    conn.close()