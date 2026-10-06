import json
import logging
from datetime import datetime
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError

from config.kafka_config import (
    KAFKA_BOOTSTRAP_SERVERS, CLAIM_TOPIC, PROCESSED_TOPIC,
    FRAUD_TOPIC, CONSUMER_GROUP
)
from database.database import initialize_database, insert_claim, insert_fraud_alert
from models.claim import validate_claim

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
log = logging.getLogger("claim-processor")

from models.risk import calculate_risk_score, classify_claim

def process_claim(claim: dict) -> dict:
    valid, errors = validate_claim(claim)
    processed_at = datetime.now().isoformat(timespec="seconds")

    if not valid:
        result = {
            **claim,
            "risk_score": 100,
            "risk_level": "REJECTED",
            "status": "REJECTED",
            "reasons": errors,
            "processed_timestamp": processed_at
        }
        return result

    score, reasons = calculate_risk_score(claim)
    risk_level, status = classify_claim(score, True)

    return {
        **claim,
        "risk_score": score,
        "risk_level": risk_level,
        "status": status,
        "reasons": reasons,
        "processed_timestamp": processed_at
    }

def create_clients():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        retries=5
    )
    consumer = KafkaConsumer(
        CLAIM_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=CONSUMER_GROUP,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda value: json.loads(value.decode("utf-8"))
    )
    return producer, consumer

def main():
    initialize_database()
    try:
        producer, consumer = create_clients()
        log.info("Listening for claims on topic '%s'...", CLAIM_TOPIC)

        for message in consumer:
            claim = message.value
            claim_id = claim.get("claim_id", "UNKNOWN")
            log.info("CLAIM RECEIVED: %s", claim_id)

            try:
                result = process_claim(claim)
                insert_claim(result)

                producer.send(PROCESSED_TOPIC, value=result)

                amount = float(result.get("claim_amount", 0))
                log.info(
                    "Claim Amount: ₹%s | Risk Score: %s | Risk Level: %s | Status: %s",
                    f"{amount:,.2f}", result["risk_score"],
                    result["risk_level"], result["status"]
                )

                if result["risk_level"] == "FRAUD_SUSPECTED":
                    reason = "; ".join(result.get("reasons", []))
                    alert = {
                        "claim_id": claim_id,
                        "reason": reason,
                        "risk_score": result["risk_score"],
                        "created_timestamp": result["processed_timestamp"]
                    }
                    producer.send(FRAUD_TOPIC, value=alert)
                    insert_fraud_alert(
                        claim_id, reason, result["risk_score"],
                        result["processed_timestamp"]
                    )
                    log.warning("FRAUD ALERT: %s", reason)

                producer.flush()
                log.info("Published to %s", PROCESSED_TOPIC)
            except Exception as exc:
                log.exception("Failed to process claim %s: %s", claim_id, exc)

    except KeyboardInterrupt:
        log.info("Consumer stopped.")
    except KafkaError as exc:
        log.error("Kafka error: %s", exc)
    finally:
        try:
            consumer.close()
            producer.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
