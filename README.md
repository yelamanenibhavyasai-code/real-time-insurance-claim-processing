# Real-Time Insurance Claim Processing using Apache Kafka

A beginner-friendly real-time data engineering project that simulates insurance claims, streams them through Apache Kafka, validates and risk-scores them, detects suspicious claims, stores results in SQLite, and produces a report.

## Business Problem

Insurance companies receive many claims and need to process them quickly. A streaming architecture can separate claim submission from downstream processing and allow suspicious claims to be routed for review.

## Architecture

```text
Insurance Claim Generator
        |
        v
Kafka Producer
        |
        v
insurance-claims
        |
        v
Claim Processor
  |       |       |
  v       v       v
Validation Risk   Fraud
          Score   Detection
        |
        +--> processed-claims
        |
        +--> fraud-alerts
        |
        v
      SQLite
        |
        v
      Report
```

## Technology Stack

- Python 3.11+
- Apache Kafka
- Docker Compose
- kafka-python
- SQLite
- pytest
- JSON

## Project Structure

```text
real-time-insurance-claim-processing/
├── README.md
├── requirements.txt
├── docker-compose.yml
├── .env.example
├── .gitignore
├── producer/
├── consumer/
├── database/
├── reports/
├── models/
├── config/
├── scripts/
├── tests/
├── data/
└── docs/
```

## Kafka Topics

1. `insurance-claims` - incoming claims
2. `processed-claims` - processed/enriched claims
3. `fraud-alerts` - suspicious claims

## Fraud Detection Rules

- Claim amount over ₹100,000 increases risk strongly.
- Five or more previous claims increases risk.
- An incident within 30 days of policy start increases risk.
- Very high amounts receive an additional risk signal.
- Invalid/missing data results in rejection.

Risk levels:

- LOW
- MEDIUM
- HIGH
- FRAUD_SUSPECTED
- REJECTED

## Prerequisites

Install:

- Python 3.11+
- Docker Desktop

Check:

```bash
python --version
docker --version
docker compose version
```

## Installation

### 1. Extract and enter the project

```bash
cd real-time-insurance-claim-processing
```

### 2. Create virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/WSL:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create environment file

Windows:

```bash
copy .env.example .env
```

Linux/WSL:

```bash
cp .env.example .env
```

### 5. Start Kafka

```bash
docker compose up -d
```

Check:

```bash
docker ps
```

### 6. Create Kafka topics

```bash
python scripts/create_topics.py
```

## Run the Project

Open three terminals.

### Terminal 1 - Consumer

```bash
python consumer/claim_processor.py
```

### Terminal 2 - Producer

For 50 claims:

```bash
python producer/claim_producer.py --count 50 --interval 1
```

For continuous generation:

```bash
python producer/claim_producer.py
```

Press Ctrl+C to stop continuous mode.

### Terminal 3 - Report

```bash
python reports/claim_report.py
```

## Testing

```bash
pytest -q
```

## Demo Flow

1. Start Docker Kafka.
2. Create topics.
3. Start the consumer.
4. Start the producer.
5. Watch claims move through Kafka.
6. Show risk scores and fraud alerts in the consumer terminal.
7. Run the report.
8. Explain that Kafka decouples claim generation from processing.

## Stop Kafka

```bash
docker compose down
```

To also remove the Kafka volume:

```bash
docker compose down -v
```

## Important

The SQLite database is created automatically at:

```text
database/claims.db
```

It is intentionally ignored by Git because it is generated runtime data.
