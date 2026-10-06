import time
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, NoBrokersAvailable
from config.kafka_config import (
    KAFKA_BOOTSTRAP_SERVERS, CLAIM_TOPIC, PROCESSED_TOPIC, FRAUD_TOPIC
)

TOPICS = [CLAIM_TOPIC, PROCESSED_TOPIC, FRAUD_TOPIC]

for attempt in range(10):
    try:
        admin = KafkaAdminClient(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            client_id="insurance-topic-admin"
        )
        existing = admin.list_topics()
        new_topics = [
            NewTopic(name=t, num_partitions=3, replication_factor=1)
            for t in TOPICS if t not in existing
        ]
        if new_topics:
            try:
                admin.create_topics(new_topics=new_topics)
            except TopicAlreadyExistsError:
                pass
        print("Kafka topics ready:", ", ".join(TOPICS))
        admin.close()
        break
    except NoBrokersAvailable:
        print("Kafka not ready yet; retrying...")
        time.sleep(3)
else:
    raise SystemExit("Could not connect to Kafka.")
