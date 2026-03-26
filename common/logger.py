import os
from loguru import logger
from config.config import LOG_DIR, BASE_DIR

os.makedirs(LOG_DIR, exist_ok=True)

logger.add(
    os.path.join(LOG_DIR, "web_auto_{time:YYYY-MM-DD}.log"),
    encoding="utf-8",
    rotation="00:00",
    retention="7 days",
    level="INFO"
)

log = logger