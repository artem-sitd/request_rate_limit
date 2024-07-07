from app import app
from app.router import all_routes

if __name__ == "__main__":
    app.register_blueprint(all_routes)
    app.run(host="0.0.0.0", port=5000)
