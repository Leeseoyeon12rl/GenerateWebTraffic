# 네트워크 트래픽을 실시간으로 캡처.
# + 패킷 크기, In/Out 방향 등을 포함한 CSV 저장.

from scapy.all import sniff, IP, TCP, UDP
import pandas as pd
import time
from datetime import datetime
import os
import uuid
import base64
from dotenv import load_dotenv
load_dotenv()
MY_IP = os.getenv("MY_IP")
CSV_FILE = os.getenv("CSV_FILE")

def process_packet(packet):
    if packet.haslayer(IP):
        id = str(uuid.uuid4()),
        timestamp = datetime.now().isoformat(),
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        length = len(packet)
        protocol = "TCP" if packet.haslayer(TCP) else "UDP" if packet.haslayer(UDP) else "Other"
        src_port = packet.sport if packet.haslayer(TCP) or packet.haslayer(UDP) else None
        dst_port = packet.dport if packet.haslayer(TCP) or packet.haslayer(UDP) else None
        direction = 512 if src_ip == MY_IP else -512

        df = pd.DataFrame([{
            "timestamp": timestamp, "src_ip": src_ip, "dst_ip": dst_ip, 
            "direction": direction, "protocol": protocol, 
            "src_port": src_port, "dst_port": dst_port, "length": length
        }])

        df.to_csv(CSV_FILE, mode="a", index=False, encoding="utf-8-sig", header=not os.path.exists(CSV_FILE))

sniff(filter="tcp or udp", prn=process_packet, store=0)
    