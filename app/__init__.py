from flask import Flask
from redis import Redis
from .config import env

app = Flask(__name__)

r = Redis(host=env.redis_host, port=6379, db=0)
