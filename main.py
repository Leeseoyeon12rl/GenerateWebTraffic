# terminal 실행 순서
# 0. Docker 켜고 docker ps로 컨테이너 확인
# 1. Docker로 Kafka + Cassandra 실행
# docker-compose up -d
# 2. main.py 실행
# python main.py

# 종료: terminal kill...(손 볼 필요 있음)

from multiprocessing import Process # all scripts run simultaneously
import time
import subprocess
import logging
import os
from dotenv import load_dotenv
from cassandra.cluster import Cluster, NoHostAvailable
from kafka import KafkaAdminClient
load_dotenv()

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "localhost")
TRAFFIC_DURATION = int(os.getenv("TRAFFIC_DURATION"))


# scripts to run
scripts = [
    "cassandra_setup.py",
    "selenium_maketraffic.py",
    "scapy_capturetraffic.py",
    "kafka_producer.py",
    "kafka_consumer.py"
]

def run_script(script_name):
    subprocess.run(["python", script_name])

def wait_for_cassandra(host, max_retries=10, delay=5): # Cassandra가 연결이 좀 느림. Cassandra가 준비되기 전에 실행되는 문제 해결.
    for i in range(max_retries):
        try:
            logging.info(f"[Cassandra] 연결 시도 {i+1}/{max_retries}")
            cluster = Cluster([host])
            session = cluster.connect()
            logging.info("[Cassandra] 연결 성공")
            return True
        except NoHostAvailable:
            logging.warning("[Cassandra] 아직 연결할 수 없습니다. 재시도 중...")
            time.sleep(delay)
    logging.error("[Cassandra] 연결 실패. Cassandra가 실행 중인지 확인하세요.")
    return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("네트워크 트래픽 캡처 및 처리 시작")

    # Cassandra 준비 확인
    if not wait_for_cassandra(CASSANDRA_HOST):
        exit(1)

    # run process by multiprocessing
    processes = [Process(target=run_script, args=(script,)) for script in scripts]

    for process in processes:
        process.start()

    time.sleep(TRAFFIC_DURATION)

    for process in processes:
        process.kill()

    logging.info("모든 프로세스 종료 완료")

