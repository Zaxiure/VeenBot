import os
from discordbot import newBot
from py_dotenv import read_dotenv
import mysql.connector

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
read_dotenv(dotenv_path)

mydb = mysql.connector.connect(
  host=os.getenv('DB_HOST'),
  user=os.getenv('DB_USER'),
  passwd=os.getenv('DB_PASSWORD'),
  database=os.getenv('DB_DATABASE')
)

connection = mydb.cursor()
newBot(os.getenv('DISCORD_TOKEN'), connection, mydb, os.getenv('ACTIVATION_CHANNEL'), os.getenv('DOMAIN'))
