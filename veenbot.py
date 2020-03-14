import os
from discordbot import newBot
from py_dotenv import read_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
read_dotenv(dotenv_path)

newBot(os.getenv('DISCORD_TOKEN'), os.getenv('ACTIVATION_CHANNEL'), os.getenv('DOMAIN'), os.getenv('API'))
