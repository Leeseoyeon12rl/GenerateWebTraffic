## 사용할 쿼리들 목록
----------------------------------------------

1. 최근 10초간의 네트워크 트래픽 보기
특징: 실시간 데이터 쓰기(using 2 terminal) + 타임베이스 기반 조회(filter by timestamp)

SELECT toTimestamp(now()) FROM system.local;
SELECT * FROM network_traffic WHERE timestamp >  '2025-03-22T03:06:05.334363' ALLOW FILTERING;
// timestamp에서 정수(밀리초)를 빼는 계산 -> Cassandra는 타입 간 연산에 대한 정의가 없으므로 쿼리 외부에서 계산해서 넣어야 함.



2. 특정 IP에서 발생한 모든 트래픽 조회
특징: 검색 쿼리에 맞춘 별도 테이블(traffic_by_ip)을 cassandra_setup.py에서 만들어 사용. -> IP 기준 파티셔닝

SELECT * FROM traffic_by_ip WHERE src_ip = '192.168.0.64'; # 파티션 기준으로 테이블을 미리 만들어뒀으므로 ALLOW FILTERING 없어도 됨.



3. TCP 프로토콜별로 발생한 트래픽 통계
특징: 카운터 활용(프로토콜별 트래픽 수) -> counter table을 cassandra_setup.py에서 만들어 사용. kafka_consumer.py에서 카운터 업데이트

SELECT * FROM traffic_counter;



4. TTL이 지난 후 Tombstone이 생기는 걸 확인하고 COmpaction이 실행된 후 실제로 row가 삭제되는 것 확인.

SELECT * FROM test_ttl;
// Tombstone 확인 가능.

DESCRIBE TABLE test_ttl;
// gc_grace_seconds = 864000이 보일 것임.

ALTER TABLE test_ttl WITH gc_grace_seconds = 0;

docker exec -it cassandra_network_traffic nodetool flush
docker exec -it cassandra_network_traffic nodetool compact nw_traffic_data test_ttl

SELECT * FROM test_ttl;
// Tombstone 모두 삭제된 것 확인 가능.

SELECT id, TTL(message) FROM test_ttl;
// Cassandra에서 TTL이 적용된 row가 전부 만료되어 실제로 삭제되었고, Tombstone도 compact 이후 완전히 제거됨.