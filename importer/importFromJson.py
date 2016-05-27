import configparser
import json
import time
from datetime import datetime
from py2neo import *
from connector.neo4j import query_neo4j
from neo4j.v1 import ResultError

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
            user_node = Node('user')
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
                user_node['group_member'] = user_fields['Group_membership'] # not well struture to be relation
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
            # Language
            if user_fields['Language']:
                req = "MATCH (u:user { uid : %d })" % user_node['uid']
                req += "MERGE (l:language { name : '%s'})" % user_fields['Language']
                req += "CREATE UNIQUE (u)-[:SPEAK]->(l)"
                query_neo4j(req)
            # Role
            if user_fields['Roles']:
                for role in user_fields['Roles'].split(','):
                    req = "MATCH (u:user { uid : %d }) " % user_node['uid']
                    req += "MERGE (r:role { name : '%s'}) " %role
                    req += "CREATE UNIQUE (u)-[:HIS]->(r)"
                    query_neo4j(req)

            # TimeTree
            if user_fields['Created_date']:
                timestamp = int(time.mktime(datetime.strptime(user_fields['Created_date'], "%A, %B %d, %Y - %H:%M").timetuple())* 1000)
                req = "MATCH (u:user { uid : %d }) WITH u " % user_node['uid']
                req += "CALL ga.timetree.events.attach({node: u, time: %s, relationshipType: 'CREATED_ON'}) " % timestamp
                req += "YIELD node RETURN u"
                query_neo4j(req)

    def create_posts(self):
        query_neo4j("CREATE CONSTRAINT ON (p:post) ASSERT p.pid IS UNIQUE")
        print('Import posts')
        json_posts = json.load(open(config['importer']['json_posts_path']))
        for post_entry in json_posts['nodes']:
            post_node = Node('post')
            post_fields = post_entry['node']
            post_node['pid'] = int(post_fields['Nid'])
            if post_fields['title']:
                post_node['title'] = post_fields['title']
            if post_fields['Body']:
                post_node['body'] = post_fields['Body']
            if post_fields['Group']:
                post_node['group'] = post_fields['Group']
            self.neo4j_graph.merge(post_node)

            # Add relation
            # Type
            if post_fields['Type']:
                req = "MATCH (p:post { pid : %d })" % post_node['pid']
                req += "MERGE (pt:post_type { name : '%s'})" % post_fields['Type']
                req += "CREATE UNIQUE (p)-[:TYPE_IS]->(pt)"
                query_neo4j(req)

            # Type
            if post_fields['Group ID']:
                req = "MATCH (p:post { pid : %d })" % post_node['pid']
                req += "MERGE (n:group_id { gid : '%s'})" % post_fields['Group ID']
                req += "CREATE UNIQUE (p)-[:GROUP_IS]->(n)"
                query_neo4j(req)

            # Author
            if post_fields['Author uid']:
                result = query_neo4j("MATCH (u:user { uid : %s }) RETURN u" % post_fields['Author uid'])
                try :
                    record = result.single()
                    req = "MATCH (p:post { pid : %d })" % post_node['pid']
                    req = "MATCH (u:user { uid : %s })" % post_fields['Author uid']
                    req += "CREATE UNIQUE (u)-[:AUTHORSHIP]->(p)"
                    query_neo4j(req)
                except ResultError:
                    print("post pid : %d as no author uid : %s" % (post_node['pid'], post_fields['Author uid']))

            # TimeTree
            if post_fields['Post date']:
                timestamp = int(time.mktime(
                    datetime.strptime(post_fields['Post date'][:-13], "%a, %Y-%m-%d %H:%M").timetuple()) * 1000)
                req = "MATCH (p:post { pid : %d }) WITH p " % post_node['pid']
                req += "CALL ga.timetree.events.attach({node: p, time: %s, relationshipType: 'POST_ON'}) " % timestamp
                req += "YIELD node RETURN p"
                query_neo4j(req)




    def create_comments(self):
        query_neo4j("CREATE CONSTRAINT ON (c:comment) ASSERT c.cid IS UNIQUE")
        print('Import comments')