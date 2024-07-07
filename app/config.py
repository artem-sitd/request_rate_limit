from pathlib import Path
from dotenv import load_dotenv
import os

env_file = (
    Path(__file__).parent.parent / ".env.docker"
    if os.getenv("USE_DOCKER")
    else Path(__file__).parent.parent / ".env"
)
load_dotenv(dotenv_path=env_file)


class Env_:
    RATE_LIMIT = int(os.getenv("RATE_LIMIT"))
    TIME_WINDOW = int(os.getenv("TIME_WINDOW"))  # 1 minute
    BLOCK_TIME = int(os.getenv("BLOCK_TIME"))  # 2 minutes
    SUBNET_MASK = int(os.getenv("SUBNET_MASK"))  # /24 subnet
    redis_host = os.getenv("redis_host")


env = Env_()
