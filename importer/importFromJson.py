import configparser
import json
import time
from datetime import datetime
from py2neo import *
from connector.neo4j import query_neo4j

config = configparser.ConfigParser()
config.read("config.ini")

class ImportFromJson(object):
    def __init__(self):
        super(ImportFromJson, self).__init__()
        print('Initializing')
        self.neo4j_graph = Graph(host=config['neo4j']['url'], user=config['neo4j']['user'], password=config['neo4j']['password'])
        # self.neo4j_graph.delete_all() # todo remove
        # todo ask neo4j for is data version aka last_uid last_pid last_cid


    def create_users(self):
        query_neo4j("CREATE CONSTRAINT ON (n:user) ASSERT n.uid IS UNIQUE")
        query_neo4j("CREATE CONSTRAINT ON (l:language) ASSERT l.name IS UNIQUE")
        query_neo4j("CREATE CONSTRAINT ON (r:role) ASSERT r.name IS UNIQUE")
        print('Import users')
        json_users = json.load(open(config['importer']['json_users_path']))
        for user_entry in json_users['nodes']:
            user_node = Node(u'user')
            user_fields = user_entry['node']
            user_node['uid'] = int(user_fields['Uid'])
            if user_fields['name']:
                user_node['name'] = user_fields['name']
            if user_fields['Bio']:
                user_node['biography'] = user_fields['Bio']
            if user_fields['based_in']:
                user_node['based'] = user_fields['based_in']
            if user_fields['Website_URL']:
                user_node['website_url'] = user_fields['Website_URL']
            if user_fields['Active']:
                user_node['active'] = user_fields['Active']
            if user_fields['Age_Group']:
                user_node['age'] = user_fields['Age_Group']
            if user_fields['Email']:
                user_node['email'] = user_fields['Email']
            if user_fields['Facebook_URL']:
                user_node['facebook'] = user_fields['Facebook_URL']
            if user_fields['First_Name']:
                user_node['first_name'] = user_fields['First_Name']
            if user_fields['Last_Name']:
                user_node['last_name'] = user_fields['Last_Name']
            if user_fields['Group_membership']:
                user_node['group_member'] = user_fields['Group_membership']
            if user_fields['How_did_you_hear_about_Edgeryders?']:
                user_node['hear_about_edgeryders'] = user_fields['How_did_you_hear_about_Edgeryders?']
            if user_fields['LinkedIn_URL']:
                user_node['linkedin'] = user_fields['LinkedIn_URL']
            if user_fields['Permission']:
                user_node['permission'] = user_fields['Permission']
            if user_fields['Twitter_URL']:
                user_node['twitter'] = user_fields['Twitter_URL']
            if user_fields['Real_name']:
                user_node['real_name'] = user_fields['Real_name']
            self.neo4j_graph.merge(user_node)

            # Add relation
            if user_fields['Language']:
                query_neo4j("MATCH (u:user { uid : %d }) MERGE (l:language { name : '%s'}) CREATE UNIQUE (u)-[:SPEAK]->(l)" % (user_node['uid'], user_fields['Language']))
            if user_fields['Roles']:
                for role in user_fields['Roles'].split(','):
                    query_neo4j("MATCH (u:user { uid : %d }) MERGE (r:role { name : '%s'}) CREATE UNIQUE (u)-[:HIS]->(r)" % (user_node['uid'], role))

            # TimeTree
            if user_fields['Created_date']:
                timestamp = time.mktime(datetime.strptime(user_fields['Created_date'], "%A, %B %d, %Y - %H:%M").timetuple())
                req = "MATCH (u:user { uid : %d }) WITH u " % user_node['uid']
                req += "CALL ga.timetree.events.attach({node: u, time: %s, relationshipType: 'created_on'}) YIELD node RETURN u" % int(timestamp * 1000)
                query_neo4j(req)

    def create_posts(self):
        query_neo4j("CREATE CONSTRAINT ON (p:post) ASSERT p.pid IS UNIQUE")
        print('Import posts')


    def create_comments(self):
        query_neo4j("CREATE CONSTRAINT ON (c:comment) ASSERT c.cid IS UNIQUE")
        print('Import comments')