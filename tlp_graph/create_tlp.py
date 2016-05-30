from tulip import *
import configparser
from tulipplugins import *
from py2neo import *

config = configparser.ConfigParser()
config.read("config.ini")


class create_tlp(object):
    def __init__(self):
        super(create_tlp, self).__init__()
        print('Initializing')
        self.neo4j_graph = Graph(host=config['neo4j']['url'], user=config['neo4j']['user'], password=config['neo4j']['password'])

    def create_full(self):
        '''
        Builds a tulip version of the whole database
        '''

        tulip_graph = tlp.newGraph()
        tulip_graph.setName('opencare')
        shape = tulip_graph.getIntegerProperty('viewShape')
        color = tulip_graph.getColorProperty('viewColor')
        size = tulip_graph.getSizeProperty('viewSize')
        label = tulip_graph.getStringProperty('viewLabel')
        # uid for users / nid for content nodes / cid for comments
        uid = tulip_graph.getIntegerProperty('uid')
        pid = tulip_graph.getIntegerProperty('pid')
        cid = tulip_graph.getIntegerProperty('cid')
        name = tulip_graph.getStringProperty('name')
        element_type = tulip_graph.getStringProperty('node_type')
        body = tulip_graph.getStringProperty('body')
        title = tulip_graph.getStringProperty('title')

        print("Read Users")
        for user in self.neo4j_graph.find('user'):
            n = tulip_graph.addNode()
            element_type[n] = 'user'
            shape[n] = tlp.NodeShape.GlowSphere
            color[n] = tlp.Color.Tan
            size[n] = tlp.Size(1, 1, 1)
            uid[n] = user['uid']
            name[n] = user['name']
            label[n] = user['name']

        print("Read Posts")
        for post in self.neo4j_graph.find('post'):
            n = tulip_graph.addNode()
            element_type[n] = 'post'
            shape[n] = tlp.NodeShape.RoundedBox
            color[n] = tlp.Color.Lilac
            size[n] = tlp.Size(1, 2, 1)
            pid[n] = post['pid']
            title[n] = post['title']
            label[n] = post['title']

        print("Read Comments")
        for comment in self.neo4j_graph.find('comment'):
            n = tulip_graph.addNode()
            element_type[n] = 'comment'
            shape[n] = tlp.NodeShape.RoundedBox
            color[n] = tlp.Color.ElectricBlue
            size[n] = tlp.Size(1, 2, 1)
            cid[n] = comment['cid']
            if comment['title']:
                title[n] = comment['title']
                label[n] = comment['title']

        print("Create AUTHORSHIP edges")
        for link in self.neo4j_graph.match(start_node=None, rel_type='AUTHORSHIP', end_node=None, bidirectional=False,
                                           limit=None):
            source = link.start_node()
            target = link.end_node()
            s_id = source['uid']
            tulip_source = self.find_node_by_id(s_id, tulip_graph, uid)
            if target['pid']:
                t_id = target['pid']
                tulip_target = self.find_node_by_id(t_id, tulip_graph, pid)
            if target['cid']:
                t_id = target['cid']
                tulip_target = self.find_node_by_id(t_id, tulip_graph, cid)
            if tulip_source and tulip_target:
                e = tulip_graph.addEdge(tulip_source, tulip_target)
            else:
                print("ERROR source or target is not define")
            element_type[e] = 'AUTHORSHIP'

        print("Create COMMENTS edges")
        for link in self.neo4j_graph.match(start_node=None, rel_type='COMMENTS', end_node=None, bidirectional=False,
                                           limit=None):
            source = link.start_node()
            target = link.end_node()
            s_id = source['cid']
            tulip_source = self.find_node_by_id(s_id, tulip_graph, cid)
            if target['pid']:
                t_id = target['pid']
                tulip_target = self.find_node_by_id(t_id, tulip_graph, pid)
            elif target['cid']:
                t_id = target['cid']
                tulip_target = self.find_node_by_id(t_id, tulip_graph, cid)
            if tulip_source and tulip_target:
                e = tulip_graph.addEdge(tulip_source, tulip_target)
            else:
                print("ERROR source or target is not define")
            element_type[e] = 'COMMENTS'

        print("Export the graph to %s" % config['exporter']['tlp_path'])
        tlp.saveGraph(tulip_graph, config['exporter']['tlp_path'])

    def find_node_by_id(self, id, graph, type):
        for node in graph.getNodes():
            if type.getNodeValue(node) == id:
                return node
        print("ERROR cannot finding node %s " % id)
        return None
