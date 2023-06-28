import os
from starlette.config import Config

TESTING = False

dir_path = os.path.dirname(os.path.realpath(__file__))
root_dir = dir_path[:-3]
config = Config(f'{root_dir}.env')
DB_NAME = config('DB_NAME', cast=str)

if TESTING:
    DATABASE_URL = "sqlite+pysqlite:///:memory:"
else:
    DATABASE_URL = f'sqlite:///{root_dir}' + config('DB_NAME', cast=str)

SECRET_KEY = config('SECRET_KEY', cast=str)
ALGORITHM = config('ALGORITHM', cast=str)
ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES', cast=str)
REDIS_HOST = config('REDIS_HOST', cast=str)
REDIS_PORT = config('REDIS_PORT', cast=str)