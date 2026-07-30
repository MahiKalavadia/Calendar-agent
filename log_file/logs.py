import logging, os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_formatter = logging.Formatter('%(asctime)s - %(name)s%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p')

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

log_filename = f"app_{datetime.today().strftime('%Y-%m-%d')}.log"
file_handler = logging.FileHandler(
    os.path.join(LOG_DIR, log_filename),
    encoding="utf-8"
)

file_handler.setFormatter(log_formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[console_handler, file_handler]
)

logging.getLogger("watchfiles").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)