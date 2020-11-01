from pathlib import Path
import sys
import redis

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEV = True

if DEV:
    from settings.dev_env import *

def redis_connect() -> redis.client.Redis:
    try:
        client = redis.Redis(
            host=Settings().dict()['redis_host'],
            port=Settings().dict()['redis_port'],
            db=Settings().dict()['redis_db'],
            socket_timeout=Settings().dict()['redis_time_out'],
        )
        ping = client.ping()
        if ping is True:
            return client
    except Exception as e:
        print(f"AuthenticationError {e}")
        sys.exit(1)



redis_client = redis_connect()