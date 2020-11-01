from pydantic import BaseSettings


class Settings(BaseSettings):
    redis_host = 'localhost'
    redis_port = 6379
    redis_db = 0
    redis_time_out = 1

    URL_Q = 'pepe'

    class Config:
        case_sensitive = True


settings_as_dict = Settings().dict()
