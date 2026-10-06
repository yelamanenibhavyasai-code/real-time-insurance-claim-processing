# Architecture

```text
Claim Generator
      |
      v
Kafka Producer
      |
      v
insurance-claims
      |
      v
Claim Processor
      |
      +--> Validation
      |
      +--> Risk Scoring
      |
      +--> Fraud Detection
      |
      +--> SQLite
      |
      +--> processed-claims
      |
      +--> fraud-alerts (suspicious claims)
      |
      v
Reports
```

## Why Kafka?

Kafka provides a durable, distributed event-streaming layer between claim generation and processing. It decouples producers from consumers, supports consumer groups and multiple partitions, and allows processing to continue independently from the producer.

## Components

- **Producer:** creates insurance claim events and sends JSON messages.
- **insurance-claims:** input event stream.
- **Consumer:** validates and enriches each claim.
- **Risk scoring:** assigns a 0–100 score.
- **Fraud detection:** applies transparent business rules.
- **processed-claims:** output event stream.
- **fraud-alerts:** suspicious-claim stream.
- **SQLite:** simple local storage for demonstrations.
- **Reports:** summarizes processed data.
