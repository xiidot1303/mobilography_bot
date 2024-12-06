import os
from dotenv import load_dotenv

load_dotenv(os.path.join(".env"))

PORT = int(os.environ.get("PORT"))
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DEBUG")
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",")
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS").split(",")

# Postgres db informations
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

# Telegram bot
BOT_API_TOKEN = os.environ.get("BOT_API_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
WEBAPP_URL = os.environ.get("WEBAPP_URL")
CHANNEL_JOIN_LINK = os.environ.get("CHANNEL_JOIN_LINK")

WEBSITE_URL = os.environ.get("WEBSITE_URL")
OFFER_URL = os.environ.get("OFFER_URL")

# Cryptocloud
CRYPTOCLOUD_API_KEY = os.environ.get("CRYPTOCLOUD_API_KEY")
CRYPTOCLOUD_SHOP_ID = os.environ.get("CRYPTOCLOUD_SHOP_ID")
CRYPTOCLOUD_SECRET_KEY = os.environ.get("CRYPTOCLOUD_SECRET_KEY")


PAYMENT_PROVIDERS = {
    "global": {
        "name": "Visa/Mastercard",
        "token": os.environ.get("GLOBAL_PAYMENT_TOKEN"),
        "currency": "UZS"
    },
    "yoomoney": {
        "name": "ЮKassa",
        "token": os.environ.get("YOOMONEY_TOKEN"),
        "currency": "RUB"
    },
    "click": {
        "name": "Click",
        "token": os.environ.get("CLICK_TOKEN"),
        "currency": "UZS"
    },
    "stars": {
        "name": "Telegram stars",
        "token": "",
        "currency": "XTR"
    },
    "cryptocloud": {
        "name": "CryptoCloud",
        "currency": "USD"
    }
}
