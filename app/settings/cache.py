from redis import Redis

try:
    redisClient = Redis.from_url("redis://localhost:6379")
    print("Connected to redis...")
except Exception as e:
    print(f"Error connecting to redis: {e}")
