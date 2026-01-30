import logging
from logging.handlers import RotatingFileHandler
import os

# Tạo thư mục logs nếu chưa tồn tại
log_dir = os.path.join(os.path.dirname(__file__), "../../logs")
os.makedirs(log_dir, exist_ok=True)

# Cấu hình logger
logger = logging.getLogger("autofill_ai")
logger.setLevel(logging.DEBUG)

# Handler cho file
file_handler = RotatingFileHandler(
    os.path.join(log_dir, "app.log"),
    maxBytes=10485760,  # 10MB
    backupCount=5
)
file_handler.setLevel(logging.DEBUG)

# Handler cho console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
