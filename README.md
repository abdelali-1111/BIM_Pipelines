BIM Pipelines — Data Ingestion & Processing Architecture

A complete end-to-end data orchestration pipeline built with Apache Airflow, PostgreSQL, and Adminer, fully containerized using Docker Compose.

📌 Project Overview

This project manages a robust data pipeline architecture divided into 4 major stages:

1_streaming: Real-time continuous data ingestion (handling checkout events).

2_batch: Scheduled daily batch data ingestion (@daily) for static references (stores, products, promotions).

3_staging: Monitors upstream tasks, cleanses raw data, and executes staging SQL transformation scripts.

4_marts: Automatically triggered upon successful staging execution to build analytical Data Marts for downstream business intelligence.

🏗️ Platform Architecture

Data Flow Breakdown:

Ingestion: Dual-path ingestion supporting both batch CSV feeds and streaming API payloads.

Orchestration: Apache Airflow coordinates DAG dependencies, ensures data completeness, and executes SQL transformations in order.

Storage & Management: Data is consolidated into PostgreSQL (bim database) and managed via Adminer on port 8085.

🛠️ Tech Stack

Orchestrator: Apache Airflow 2.9.3 (Standalone Mode)

Database: PostgreSQL 15

Database Management UI: Adminer

Containerization: Docker & Docker Compose

Languages & Frameworks: Python, SQL

## 🏗️ Platform Architecture

![Platform Architecture](assets/architecture.png)

## 🖼️ Interface Screenshots

![Airflow DAGs View](assets/airflow_dags.png)

Apache Airflow Dashboard

🚀 Getting Started

Prerequisites

Docker Desktop installed and running on your machine.

Installation Steps

Clone the repository:

git clone https://github.com/abdelali-1111/BIM_Pipelines.git
cd BIM_Pipelines


Start services with Docker Compose:

docker compose up -d


Access Web Interfaces:
Apache Airflow UI

URL: http://localhost:8083

Username: admin

Password: Retrieve the auto-generated password by running:

docker compose exec airflow cat /opt/airflow/standalone_admin_password.txt


Note: You should see 1_streaming and 2_batch running. 3_staging and 4_marts are ready for your data pipeline tasks.

Adminer UI (Database Management)

URL: http://localhost:8086

System: PostgreSQL

Server: postgres

Username: bim

Password: bim

Database: bim


## 🗂️ Project Structure

```text
BIM_Pipelines/
├── dags/                  # Airflow DAG definitions
│   ├── 1_streaming_dag.py
│   ├── 2_batch_dag.py
│   ├── 3_staging_dag.py
│   └── 4_marts_dag.py
├── sql/                   # SQL transformation scripts
│   ├── staging/           # Staging cleanup & normalization scripts
│   └── mart/              # Analytical data mart aggregation scripts
├── assets/                # Documentation assets (screenshots & architecture diagram)
│   ├── airflow_dags.png
│   └── architecture.png
├── docker-compose.yml     # Multi-container service definitions
├── .gitignore             # Git exclusion rules
└── README.md              # Project documentation