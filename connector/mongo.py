import configparser
from pymongo import MongoClient

config = configparser.ConfigParser()
config.read("config.ini")

# Connect to the database
client = MongoClient('mongodb://%s:%s/' % (config['mongo']['host'], config['mongo']['port']))
db = client[config['mongo']['db']]
