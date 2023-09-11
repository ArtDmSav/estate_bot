import configparser
from pathlib import Path

dir_path = Path.cwd()
path = Path(dir_path, 'config', 'config.ini')
config = configparser.ConfigParser()
config.read(path)

BOT_TOKEN = config['Telegram']['bot_token']
BOT_USERNAME = config['Telegram']['bot_username']
USERNAME = config['Telegram']['username']
API_ID = config['Telegram']['api_id']
API_HASH = config['Telegram']['api_hash']
