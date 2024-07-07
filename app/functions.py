from flask import request
import ipaddress
import time
from . import r
from .config import env

"""
subnet переменная парсит адрес подсети (исключая номер устройства). Маска подсети берется из env (24)
"""


# Получаем ip. Либо из заголовка, либо с request
def get_client_ip():
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.remote_addr
    return ip


# Эта функция проверяет, превышено ли количество запросов из подсети.
# Если лимит превышен, подсеть блокируется на заданное время.
def is_rate_limited(ip):
    subnet = str(ipaddress.ip_network(f"{ip}/{env.SUBNET_MASK}", strict=False).network_address)
    key = f"rate_limit:{subnet}"
    current_time = int(time.time())

    # Check if the subnet is blocked
    blocked_until = r.get(f"blocked:{subnet}")
    if blocked_until and current_time < int(blocked_until):
        return True

    # Get request count
    count = r.get(key)
    if count and int(count) >= env.RATE_LIMIT:
        # Block for BLOCK_TIME seconds
        r.setex(f"blocked:{subnet}", env.BLOCK_TIME, current_time + env.BLOCK_TIME)
        return True

    return False


# Эта функция увеличивает счетчик запросов для подсети и устанавливает время жизни ключа в Redis.
def increment_request_count(ip):
    subnet = str(ipaddress.ip_network(f"{ip}/{env.SUBNET_MASK}", strict=False).network_address)
    key = f"rate_limit:{subnet}"

    # Increment request count
    r.incr(key)
    r.expire(key, env.TIME_WINDOW)
