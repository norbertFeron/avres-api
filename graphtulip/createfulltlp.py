from tulip import *
import configparser
from py2neo import *

config = configparser.ConfigParser()
config.read("config.ini")


class CreateFullTlp(object):
    def __init__(self):
        super(CreateFullTlp, self).__init__()
        print('Initializing')
        self.neo4j_graph = Graph(host=config['neo4j']['url'], user=config['neo4j']['user'], password=config['neo4j']['password'])
        self.tulip_graph = tlp.newGraph()

    def create(self):
        '''
        Builds a tulip version of the whole database
        '''

        self.tulip_graph.setName('opencare')
        shape = self.tulip_graph.getIntegerProperty('viewShape')
        color = self.tulip_graph.getColorProperty('viewColor')
        size = self.tulip_graph.getSizeProperty('viewSize')
        label = self.tulip_graph.getStringProperty('viewLabel')
        # uid for users / nid for content nodes / cid for comments
        uid = self.tulip_graph.getIntegerProperty('uid')
        pid = self.tulip_graph.getIntegerProperty('pid')
        cid = self.tulip_graph.getIntegerProperty('cid')
        name = self.tulip_graph.getStringProperty('name')
        element_type = self.tulip_graph.getStringProperty('node_type')
        body = self.tulip_graph.getStringProperty('body')
        title = self.tulip_graph.getStringProperty('title')

        print("Read Users")
        for user in self.neo4j_graph.find('user'):
            n = self.tulip_graph.addNode()
            element_type[n] = 'user'
            shape[n] = tlp.NodeShape.GlowSphere
            color[n] = tlp.Color.Tan
            size[n] = tlp.Size(1, 1, 1)
            uid[n] = user['uid']
            name[n] = user['name']
            label[n] = user['name']

        print("Read Posts")
        for post in self.neo4j_graph.find('post'):
            n = self.tulip_graph.addNode()
            element_type[n] = 'post'
            shape[n] = tlp.NodeShape.RoundedBox
            color[n] = tlp.Color.Lilac
            size[n] = tlp.Size(1, 2, 1)
            pid[n] = post['pid']
            title[n] = post['title']
            word = post['title'].split(' ')
            if len(word) > 3:
                label[n] = "%s %s %s ..." % (word[0], word[1], word[2])
            else:
                label[n] = post['title']

        print("Read Comments")
        for comment in self.neo4j_graph.find('comment'):
            n = self.tulip_graph.addNode()
            element_type[n] = 'comment'
            shape[n] = tlp.NodeShape.RoundedBox
            color[n] = tlp.Color.ElectricBlue
            size[n] = tlp.Size(1, 2, 1)
            cid[n] = comment['cid']
            if comment['subject']:
                title[n] = comment['subject']
                word = comment['subject'].split(' ')
                if len(word) > 3:
                    label[n] = "%s %s %s ..." % (word[0], word[1], word[2])
                else:
                    label[n] = comment['subject']

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
                e = self.tulip_graph.addEdge(tulip_source, tulip_target)
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
                e = self.tulip_graph.addEdge(tulip_source, tulip_target)
            else:
                print("ERROR source or target is not define")
            element_type[e] = 'COMMENTS'

        print("Apply LayoutAlgorithm")
        self.tulip_graph.applyLayoutAlgorithm("FM^3 (OGDF)")
        print("Export")
        filename = "complete"
        tlp.saveGraph(self.tulip_graph, "%s%s.tlp" % (config['exporter']['tlp_path'], filename))
        tlp.exportGraph("SIGMA JSON Export", self.tulip_graph, "%s%s.json" % (config['exporter']['json_path'], filename))

    @staticmethod
    def find_node_by_id(wanted_id, graph, type_id):
        for node in graph.getNodes():
            if type_id.getNodeValue(node) == wanted_id:
                return node
        print("ERROR cannot finding node %s " % wanted_id)
        return None
