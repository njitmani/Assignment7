import argparse
import qrcode
from dotenv import load_dotenv
import logging.config
from pathlib import Path
import os
from datetime import datetime
import validators

load_dotenv()

DEFAULT_URL = "https://github.com/sid995/"
qr_dir_path = os.getenv("QR_OUTPUT_DIR", "./qr_codes")
log_dir_path = os.getenv("LOG_OUTPUT_DIR", "./logs")
fill_color = os.getenv("QR_FILL_COLOR", "black")
back_color = os.getenv("QR_BACK_COLOR", "white")

log_file_path = Path(log_dir_path) / "application.log"

log_file_path.parent.mkdir(parents=True, exist_ok=True)

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(log_file_path),  # Use the string path
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'default',
            'level': 'INFO',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'INFO',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file'],
    },
})


def is_valid_url(url):
    return validators.url(url)

def create_directory(path):
    path = Path(path)
    if not path.exists():
        path.mkdir(parents=True)
        logging.info(f"Created directory: {path}")
    else:
        logging.info(f"Directory {path} already exists")

def generate_qr_code(url, dir_path, fill_color, back_color):
    if not is_valid_url(url):
        logging.error(f"Invalid URL: {url}")
        return
        
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    create_directory(dir_path)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = Path(dir_path) / f"qr_code_{timestamp}.png"
    img.save(file_path)
    logging.info(f"QR code saved to {file_path}")

def main():
    parser = argparse.ArgumentParser(description='Generate a QR code from a URL.')
    parser.add_argument('--url', help='The URL to generate a QR code for', default=DEFAULT_URL)
    args = parser.parse_args()
    url = args.url
    generate_qr_code(url, qr_dir_path, fill_color, back_color)

if __name__ == "__main__":
    main()
    