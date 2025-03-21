# Kafka란?
# 여러 개의 데이터 생산자(Producer)와 소비자(Consumer)가 데이터를 주고받는 메시지 큐 시스템.
# 실시간으로 데이터가 Kafka Topic에 쌓이면 여러 개의 Consumer가 데이터를 처리할 수 있음.

# 네트워크 패킷 데이터를 Kafka에 스트리밍.
# Cassandra Consumer를 만들어 실시간으로 DB에 저장 가능.
#==================================================================================
# Kafka Producer: 네트워크 트래픽 데이터를 Kafka로 보내기

from kafka import KafkaProducer
from cassandra.cluster import Cluster
import json
from scapy.all import sniff, IP, TCP, UDP
import os
import time
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

MY_IP = os.getenv("MY_IP")
KAFKA_BROKER = os.getenv("KAFKA_BROKER")
CASSANDRA_TABLE=os.getenv("CASSANDRA_TABLE")


producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def process_packet(packet):
    if packet.haslayer(IP):
        timestamp = datetime.now().isoformat()
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        length = len(packet)
        protocol = "TCP" if packet.haslayer(TCP) else "UDP" if packet.haslayer(UDP) else "Other"
        src_port = packet[TCP].sport if packet.haslayer(TCP) else (packet[UDP].sport if packet.haslayer(UDP) else None)
        dst_port = packet[TCP].dport if packet.haslayer(TCP) else (packet[UDP].dport if packet.haslayer(UDP) else None)
        direction = 512 if src_ip == MY_IP else -512

        data = {"timestamp": timestamp, "src_ip": src_ip, "dst_ip": dst_ip, "direction": direction, "protocol": protocol, "src_port": src_port, "dst_port": dst_port, "length": length}
        
        producer.send(CASSANDRA_TABLE, json.dumps(data).encode('utf-8'))

sniff(filter="tcp or udp", prn=process_packet, store=0)
