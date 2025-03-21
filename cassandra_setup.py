# make cassandra table
#=========================================
from cassandra.cluster import Cluster
import os
from dotenv import load_dotenv
load_dotenv()
CASSANDRA_KEYSPACE=os.getenv("CASSANDRA_KEYSPACE")
CASSANDRA_HOST=os.getenv("CASSANDRA_HOST")
CASSANDRA_TABLE=os.getenv("CASSANDRA_TABLE")

# connect cassandra
cluster = Cluster([CASSANDRA_HOST])
session = cluster.connect()

# make keyspace
CASSANDRA_KEYSPACE = CASSANDRA_KEYSPACE
session.execute(f"""
    CREATE KEYSPACE IF NOT EXISTS {CASSANDRA_KEYSPACE}
    WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}};
""")

# use keyspace
session.set_keyspace(CASSANDRA_KEYSPACE)

# make {CASSANDRA_TABLE} table for QUERY1
CASSANDRA_TABLE=CASSANDRA_TABLE
session.execute(f"""
    CREATE TABLE IF NOT EXISTS {CASSANDRA_TABLE} (
        id UUID PRIMARY KEY,
        timestamp TIMESTAMP,
        src_ip TEXT,
        dst_ip TEXT,
        direction INT,
        protocol TEXT,
        src_port INT,
        dst_port INT,
        length INT
    );
""")

# make traffic_by_ip table for QUERY2
session.execute(f"""
    CREATE TABLE IF NOT EXISTS traffic_by_ip (
        src_ip TEXT,
        timestamp TIMESTAMP,
        dst_ip TEXT,
        direction INT,
        protocol TEXT,
        src_port INT,
        dst_port INT,
        length INT,
        PRIMARY KEY (src_ip, timestamp)
    ) WITH CLUSTERING ORDER BY (timestamp DESC);
""")

# make traffic_counter table for QUERY3
session.execute(f"""
    CREATE TABLE IF NOT EXISTS traffic_counter (
        protocol TEXT PRIMARY KEY,
        count COUNTER
    );
""")

# make test_ttl table for QUERY4
session.execute(f"""
    CREATE TABLE IF NOT EXISTS test_ttl (
    id UUID PRIMARY KEY,
    message TEXT
    );
""")


print(f"Cassandra 테이블 {CASSANDRA_KEYSPACE}.{CASSANDRA_TABLE} 생성 완료.")