from tulip import *
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


def load_doi():
    # todo get data from neo4j
    return tlp.loadGraph(config['importer']['doi_data_tlpb'])
