import argparse
import json
import random
import time
import logging
from datetime import date, datetime, timedelta

from kafka import KafkaProducer
from kafka.errors import KafkaError

from config.kafka_config import (
    KAFKA_BOOTSTRAP_SERVERS, CLAIM_TOPIC, CLAIM_INTERVAL_SECONDS
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger("claim-producer")

NAMES = [
    "Rahul Sharma", "Priya Reddy", "Arjun Kumar", "Sneha Rao",
    "Ananya Singh", "Vikram Patel", "Neha Gupta", "Kiran Das"
]
LOCATIONS = ["Hyderabad", "Bengaluru", "Chennai", "Mumbai", "Delhi", "Pune"]
POLICIES = ["Health", "Auto", "Home", "Travel", "Life"]
CLAIM_TYPES = {
    "Health": ["Hospitalization", "Surgery", "Medical Treatment"],
    "Auto": ["Accident", "Vehicle Damage", "Theft"],
    "Home": ["Fire Damage", "Water Damage", "Property Damage"],
    "Travel": ["Trip Cancellation", "Lost Baggage", "Medical Emergency"],
    "Life": ["Accidental Death", "Critical Illness"]
}

def random_date(start: date, end: date) -> date:
    days = (end - start).days
    return start + timedelta(days=random.randint(0, max(days, 0)))

def generate_claim(index: int) -> dict:
    today = date.today()
    policy_type = random.choice(POLICIES)
    policy_start = random_date(today - timedelta(days=1000), today - timedelta(days=15))
    incident = random_date(policy_start, today)
    submission = incident + timedelta(days=random.randint(0, 5))
    amount = round(random.uniform(5000, 180000), 2)

    # Deliberately create some suspicious records for a visible demo.
    if index % 10 == 0:
        amount = random.choice([125000, 175000, 250000])
    previous = random.randint(0, 7)

    return {
        "claim_id": f"CLM{10000 + index}",
        "policy_id": f"POL{50000 + index}",
        "customer_id": f"CUS{10000 + index}",
        "customer_name": random.choice(NAMES),
        "policy_type": policy_type,
        "claim_type": random.choice(CLAIM_TYPES[policy_type]),
        "claim_amount": amount,
        "incident_date": incident.isoformat(),
        "submission_date": submission.isoformat(),
        "location": random.choice(LOCATIONS),
        "description": "Insurance claim submitted for " + policy_type.lower() + " incident",
        "customer_age": random.randint(21, 75),
        "policy_start_date": policy_start.isoformat(),
        "previous_claims": previous,
        "timestamp": datetime.now().isoformat(timespec="seconds")
    }

def create_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        retries=5
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=0,
                        help="Number of claims to send. 0 means continuous mode.")
    parser.add_argument("--interval", type=float, default=CLAIM_INTERVAL_SECONDS)
    args = parser.parse_args()

    try:
        producer = create_producer()
        index = 1
        log.info("Sending claims to '%s'...", CLAIM_TOPIC)
        while args.count == 0 or index <= args.count:
            claim = generate_claim(index)
            producer.send(CLAIM_TOPIC, value=claim)
            producer.flush()
            log.info(
                "CLAIM SENT: %s | Type: %s | Amount: ₹%s",
                claim["claim_id"], claim["claim_type"],
                f"{claim['claim_amount']:,.2f}"
            )
            index += 1
            if args.count == 0 or index <= args.count:
                time.sleep(args.interval)
    except KeyboardInterrupt:
        log.info("Producer stopped.")
    except KafkaError as exc:
        log.error("Kafka error: %s", exc)
    finally:
        try:
            producer.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
