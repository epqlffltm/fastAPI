import redis

def test_redis_connection():
    # 레디스 서버와 연결
    redis_client = redis.Redis(host="127.0.0.1", port=6379, db=0, encoding="utf-8", decode_responses=True)
    print("")
    # 연결 성공 여부 확인
    print("레디스 연결 상태:", redis_client.ping())

    print(redis_client.set("key","value"))
    print(redis_client.get("key"))