from kafka import KafkaProducer
import time

DATA_FILE = "/home/sunbeam/Desktop/Project/Customer_Churn_Prediction/data/data.json"
TOPIC = "music_events"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    linger_ms=40,                 # Small wait to build better batches
    batch_size=524288,            # 512 KB per partition
    buffer_memory=16777216,       # 16 MB total buffer
    compression_type="lz4",       # Fast + light compression
    acks=1,                       # Faster than acks='all'
    retries=3                     # Safety without slowing too much
)

print("Starting Kafka producer...\n")

start_time = time.time()
count = 0

with open(DATA_FILE, "rb") as f:
    for line in f:
        if not line.strip():
            continue

        producer.send(TOPIC, value=line)
        count += 1

        if count % 250000 == 0:
            elapsed = time.time() - start_time
            rate = count / elapsed
            print(f"Sent {count:,} records | {int(rate):,} records/sec")

producer.flush()
producer.close()
