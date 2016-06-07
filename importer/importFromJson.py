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
    def __init__(self, erase=False):
        super(ImportFromJson, self).__init__()
        print('Initializing')
        self.neo4j_graph = Graph(host=config['neo4j']['url'], user=config['neo4j']['user'], password=config['neo4j']['password'])
        if erase:
            self.neo4j_graph.delete_all()
        # else:
            # todo ask neo4j for is data version (last_uid last_pid last_cid)
        self.unavailable_users_id = []
        self.unavailable_posts_id = []
        self.unavailable_comments_id = []

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
                # user_node['email'] = user_fields['Email']
                user_node['email'] = "nomail@nomail.com"
            if user_fields['Facebook_URL']:
                user_node['facebook'] = user_fields['Facebook_URL']
            if user_fields['First_Name']:
                user_node['first_name'] = user_fields['First_Name']
            if user_fields['Last_Name']:
                user_node['last_name'] = user_fields['Last_Name']
            if user_fields['Group_membership']:
                user_node['group_member'] = user_fields['Group_membership'] # not well structure to be relation
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
                req = "MATCH (u:user { uid : %d }) " % user_node['uid']
                req += "MERGE (l:language { name : '%s'}) " % user_fields['Language']
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
                req += " MERGE (n:group_id { gid : '%s'})" % post_fields['Group ID']
                req += " CREATE UNIQUE (p)-[:GROUP_IS]->(n)"
                query_neo4j(req)

            # Author
            if post_fields['Author uid']:
                try :
                    req = "MATCH (p:post { pid : %d })" % post_node['pid']
                    req += " MATCH (u:user { uid : %s })" % post_fields['Author uid']
                    req += " CREATE UNIQUE (u)-[:AUTHORSHIP]->(p) RETURN u"
                    query_neo4j(req).single()
                except ResultError:
                    print("WARNING : post pid : %d as no author uid : %s" % (post_node['pid'], post_fields['Author uid']))
                    query_neo4j("MATCH (p:post {pid : %s}) DETACH DELETE p" % post_node['pid'])
                    self.unavailable_users_id.append(post_fields['Author uid'])

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
        json_comments = json.load(open(config['importer']['json_comments_path']))
        for comment_entry in json_comments['nodes']:
            comment_node = Node('comment')
            comment_fields = comment_entry['node']
            comment_node['cid'] = int(comment_fields['ID'])
            if comment_fields['subject']:
                comment_node['subject'] = comment_fields['subject']
            if comment_fields['Comment']:
                comment_node['comment'] = comment_fields['Comment']
            self.neo4j_graph.merge(comment_node)

            # Add relation
            # Language
            if comment_fields['Language']: # todo repare
                req = "MATCH (c:comment { cid : %d })" % comment_node['cid']
                req += " MERGE (l:language { name : '%s'})" % comment_fields['Language']
                req += " CREATE UNIQUE (u)-[:WRITE_IN]->(l)"
                query_neo4j(req)

            # ParentAuthor
            if comment_fields['Author uid']:
                result = query_neo4j("MATCH (u:user { uid : %s }) RETURN u" % comment_fields['Author uid'])
                try:
                    req = "MATCH (c:comment { cid : %d }) " % comment_node['cid']
                    req += "MATCH (u:user { uid : %s }) " % comment_fields['Author uid']
                    req += "CREATE UNIQUE (u)-[:AUTHORSHIP]->(c) RETURN u"
                    query_neo4j(req).single()
                except ResultError:
                    print("WARNING : comment cid : %d as no author uid : %s" % (comment_node['cid'], comment_fields['Author uid']))
                    query_neo4j("MATCH (c:comment {cid : %s}) DETACH DELETE c" % comment_node['cid'])
                    if comment_fields['Author uid'] not in self.unavailable_users_id:
                        self.unavailable_users_id.append(comment_fields['Author uid'])
            # ParentPost
            if comment_fields['Nid']:
                try:
                    req = "MATCH (c:comment { cid : %d }) " % comment_node['cid']
                    req += "MATCH (p:post { pid : %s }) " % comment_fields['Nid'].replace(",", "")
                    req += "CREATE UNIQUE (c)-[:COMMENTS]->(p) RETURN p"
                    query_neo4j(req).single()
                except ResultError:
                    print("WARNING : comment cid : %d as no post parent pid : %s" % (comment_node['cid'], comment_fields['Nid'].replace(",", "")))
                    query_neo4j("MATCH (c:comment {cid : %s}) DETACH DELETE c" % comment_node['cid'])
                    if comment_fields['Nid'] not in self.unavailable_posts_id:
                        self.unavailable_posts_id.append(comment_fields['Nid'])

            # TimeTree
            if comment_fields['Post date']:
                timestamp = int(time.mktime(datetime.strptime(comment_fields['Post date'], "%A, %B %d, %Y - %H:%M").timetuple()) * 1000)
                req = "MATCH (c:comment { cid : %d }) WITH c " % comment_node['cid']
                req += "CALL ga.timetree.events.attach({node: c, time: %s, relationshipType: 'POST_ON'}) " % timestamp
                req += "YIELD node RETURN c"
                query_neo4j(req)

        # ParentComment
        for comment_entry in json_comments['nodes']:
            comment_node = Node('comment')
            comment_fields = comment_entry['node']
            comment_node['cid'] = int(comment_fields['ID'])
            if comment_fields['Parent CID'] and comment_fields['Parent CID'] != 0:
                try:
                    req = "MATCH (c:comment { cid : %d }) " % comment_node['cid']
                    req += "MATCH (parent:comment { cid : %d }) " % int(comment_fields['Parent CID'])
                    req += "CREATE UNIQUE (c)-[:COMMENTS]->(parent) RETURN parent"
                    query_neo4j(req).single()
                except ResultError:
                    print("WARNING : comment cid : %d as no comment parent pid : %s" % (comment_node['cid'], comment_fields['Parent CID']))
                    query_neo4j("MATCH (c:comment {cid : %s}) DETACH DELETE c" % comment_node['cid'])
                    if comment_fields['Parent CID'] not in self.unavailable_comments_id:
                        self.unavailable_comments_id.append(comment_fields['Parent CID'])

    def end_import(self):
        response = "\n Unavailable users :"
        response += str(self.unavailable_users_id)
        response += "\n Unavailable posts :"
        response += str(self.unavailable_posts_id)
        response += "\n Unavailable comments :"
        response += str(self.unavailable_comments_id)
        print(response)
        return response

