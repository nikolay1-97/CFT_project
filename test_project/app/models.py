from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import Session
from app.config import DATABASE_URL, REDIS_HOST, REDIS_PORT, TESTING
import redis

metadata = MetaData()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def connect_db():
    session = Session(bind=engine.connect())
    return session

def get_redis_instance():
    redis_instance = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    return redis_instance


Employe_model = Table(
    'employe',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('permission_level', Integer),
    Column('username', String, unique=True),
    Column('hashed_password', String),
    Column('full_name', String),
    Column('age', Integer),
    Column('position', String)
)

Salary_model = Table(
    'salary',
    metadata,
    Column('id', Integer,  primary_key=True),
    Column('salary', Float),
    Column('employe_username', String, ForeignKey('employe.username')),
    Column('salary_increase_date', String)
)

if TESTING:
    metadata.create_all(engine)







