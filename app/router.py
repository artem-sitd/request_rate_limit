import ipaddress
from . import app, r
from flask import request, jsonify, Blueprint
from .functions import get_client_ip, increment_request_count, is_rate_limited
from .config import env

all_routes = Blueprint("all_routes", __name__)


# Этот обработчик проверяет, превышен ли лимит запросов, и возвращает ошибку 429, если лимит превышен.
# В противном случае он увеличивает счетчик запросов и возвращает статический контент.
@app.route('/', methods=["GET"])
def index():
    client_ip = get_client_ip()
    if is_rate_limited(client_ip):
        return jsonify({"error": "Too Many Requests"}), 429

    increment_request_count(client_ip)
    return "Static content"


# Этот обработчик принимает префикс подсети и сбрасывает лимиты запросов и блокировки для этой подсети.
@app.route('/reset', methods=['POST'])
def reset():
    prefix = request.json.get('prefix')
    if prefix:
        subnet = str(ipaddress.ip_network(f"{prefix}/{env.SUBNET_MASK}", strict=False).network_address)
        r.delete(f"rate_limit:{subnet}")
        r.delete(f"blocked:{subnet}")
        return jsonify({"message": "Reset successful"}), 200
    return jsonify({"error": "Invalid prefix"}), 400