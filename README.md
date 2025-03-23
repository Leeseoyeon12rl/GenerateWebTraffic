# GenerateWebTraffic
## 📡 Real-Time Network Traffic Capture & Analysis

This project sets up a complete pipeline for real-time https network traffic analysis. It generates web traffic using Selenium, captures packets using Scapy, streams the data via Apache Kafka, and stores it in Apache Cassandra. The system demonstrates key features such as counters, TTL-based expiration, and partitioned queries in Cassandra.

## 📁 Project Structure
```
.
├── .env                       # Environment variables
├── docker-compose.yml        # Kafka + Zookeeper + Cassandra setup
├── main.py                   # Launches all scripts in parallel
├── cassandra_setup.py        # Initializes Cassandra keyspace and tables
├── selenium_maketraffic.py   # Generates web traffic using Selenium
├── scapy_capturetraffic.py   # Captures packets and logs to CSV
├── kafka_producer.py         # Streams packets to Kafka
├── kafka_consumer.py         # Consumes from Kafka and stores to Cassandra
├── nw_traffic_log.csv        # Captured network log file
├── QUERY.md                  # Example queries for Cassandra
```

## ⚙️ Requirements

1. Install Docker

Install Docker Desktop or Docker CLI:

```
https://www.docker.com/
```

2. Set up .env

Update the .env file according to your environment:
```

CSV_FILE="nw_traffic_log.csv"
MY_IP=localhost  # Or your actual IP address
KAFKA_BROKER=localhost:9092
CASSANDRA_HOST=localhost
CASSANDRA_KEYSPACE=nw_traffic_data
CASSANDRA_TABLE=network_traffic
TRAFFIC_DURATION=15
WEBSITES=https://www.google.com,https://www.wikipedia.org,...
```

 MY_IP is used to determine the direction of captured traffic. You can use localhost or your actual IP.

## 🚀 How to Run

1. Start the Docker environment
```
docker-compose up -d
```

This will spin up the following containers:

```
cassandra_network_traffic

kafka_network_traffic

zookeeper_network_traffic
```

To verify:

```
docker ps
```

2. Run the pipeline

```
python main.py
```

This script will launch the following in parallel:

```
cassandra_setup.py: Initializes tables

selenium_maketraffic.py: Generates HTTP traffic

scapy_capturetraffic.py: Captures local packets

kafka_producer.py: Sends data to Kafka

kafka_consumer.py: Inserts data into Cassandra
```

It will run for the duration set in TRAFFIC_DURATION.

## 🔍 Example Queries (See QUERY.md)

  1. View traffic loaded after the particular time

  2. Query traffic from a specific IP address

  3. Count TCP/UDP packets using Cassandra counters

  4. Observe TTL behavior and compaction in Cassandra

## ✅ Tech Stack

Apache Kafka + Zooeeper: Streaming message queue

Apache Cassandra: Distributed NoSQL database

Scapy: Packet capturing

Selenium: Web automation

Python Multiprocessing: Parallel task execution

## 💡 Potential Extensions

Integrate with a real-time dashboard (e.g., Grafana or Streamlit)

Anomaly detection on network data

Simulate various traffic scenarios using TOR

Deploy on Kubernetes for scalability




