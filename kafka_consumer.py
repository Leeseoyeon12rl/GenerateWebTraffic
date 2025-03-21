# Kafka Consumer: Kafka에서 데이터를 받아 Cassandra에 저장.

from kafka import KafkaConsumer
from cassandra.cluster import Cluster
from datetime import datetime
import json
import uuid
import os
from dotenv import load_dotenv
load_dotenv()

KAFKA_BROKER = os.getenv("KAFKA_BROKER")
CASSANDRA_HOST = os.getenv("CASSANDRA_HOST")
CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE")
CASSANDRA_TABLE = os.getenv("CASSANDRA_TABLE")


# Kafka Consumer 설정
consumer = KafkaConsumer(
    CASSANDRA_TABLE,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset='earliest',
    group_id='traffic-group'
)

# Cassandra 연결
cluster = Cluster([CASSANDRA_HOST])
session = cluster.connect(CASSANDRA_KEYSPACE)


for message in consumer:
    data = message.value

    raw_ts = data["timestamp"]
    if isinstance(raw_ts, str):
        timestamp = datetime.fromisoformat(raw_ts)
    elif isinstance(raw_ts, (float, int)):
        timestamp = datetime.fromtimestamp(raw_ts)
    else:
        raise TypeError(f"지원되지 않는 timestamp 형식: {type(raw_ts)}")

    # Cassandra에 데이터 저장 - table: network_traffic
    session.execute(
        """
        INSERT INTO network_traffic (id, timestamp, src_ip, dst_ip, direction, protocol, src_port, dst_port, length)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            uuid.uuid4(), timestamp, data["src_ip"], data["dst_ip"],
            data["direction"], data["protocol"], data["src_port"],
            data["dst_port"], data["length"]
        )
    )

    # insert to table: traffic_by_ip
    session.execute(
        """
        INSERT INTO traffic_by_ip (src_ip, timestamp, dst_ip, direction, protocol, src_port, dst_port, length)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            data["src_ip"], timestamp, data["dst_ip"],
            data["direction"], data["protocol"],
            data["src_port"], data["dst_port"], data["length"]
        )
    )

    # counter update - table: traffic_counter
    session.execute("UPDATE traffic_counter SET count = count + 1 WHERE protocol = %s", (data["protocol"],))

    # insert tombstone - table: test_ttl
    session.execute("INSERT INTO test_ttl (id, message) VALUES (%s, %s) USING TTL 10", (uuid.uuid4(), "This will expire.")) # 이 시점부터 10초 후 row가 만료됨.

    print(f"Cassandra 저장 완료: {data}")