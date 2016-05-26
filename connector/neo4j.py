import configparser
from neo4j.v1 import GraphDatabase, basic_auth

config = configparser.ConfigParser()
config.read("config.ini")

# Connect to the database
driver = GraphDatabase.driver(
    "bolt://%s" % config['neo4j']['url'],
    auth=basic_auth(config['neo4j']['user'], config['neo4j']['password'])
)

# Send a cyper request to neo4j instance
def query_neo4j(request):
    session = driver.session()
    result = session.run(request)
    session.close()
    return result


def create_node(node):
    req = "CREATE"

