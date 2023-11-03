import configparser
import sentry_sdk
from pathlib import Path

# Absolut path
dir_path = Path.cwd()
path = Path(dir_path, 'config', 'config.ini')
config = configparser.ConfigParser()
config.read(path)

# Constants
BOT_TOKEN = config['Telegram']['bot_token']
BOT_USERNAME = config['Telegram']['bot_username']
USERNAME = config['Telegram']['username']
API_ID = config['Telegram']['api_id']
API_HASH = config['Telegram']['api_hash']
DEL_MSG_AFTER_DAY = 30
ACTIVE = 1
INACTIVE = 0

# Sentry
# sentry_sdk.init(
#     dsn="https://76c87c124566bc8a80985c0f5fdcc933@o4505862236078080.ingest.sentry.io/4505879335927808",
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production.
#     traces_sample_rate=1.0,
#     # Set profiles_sample_rate to 1.0 to profile 100%
#     # of sampled transactions.
#     # We recommend adjusting this value in production.
#     profiles_sample_rate=1.0,
# )
