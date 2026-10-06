import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
CLAIM_TOPIC = os.getenv("CLAIM_TOPIC", "insurance-claims")
PROCESSED_TOPIC = os.getenv("PROCESSED_TOPIC", "processed-claims")
FRAUD_TOPIC = os.getenv("FRAUD_TOPIC", "fraud-alerts")
CONSUMER_GROUP = os.getenv("CONSUMER_GROUP", "insurance-claim-processor")
CLAIM_INTERVAL_SECONDS = float(os.getenv("CLAIM_INTERVAL_SECONDS", "2"))
