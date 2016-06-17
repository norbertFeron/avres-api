from tulip import *
from py2neo import *
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


# todo create a unique Createtlp to avoid code duplication
class CreateUserTlp(object):
    def __init__(self):
        super(CreateUserTlp, self).__init__()
        print('Initializing')

        self.neo4j_graph = Graph(host=config['neo4j']['url'], user=config['neo4j']['user'], password=config['neo4j']['password'])
        self.tulip_graph = tlp.newGraph()
        self.tulip_graph.setName('opencare')
        # todo pass in parameters labels and colors
        self.labels = ["title", "subject", "name"]
        self.colors = {"uid": tlp.Color(0, 0, 255), "pid": tlp.Color(0, 255, 0), "cid": tlp.Color(255, 0, 0)}

    # -----------------------------------------------------------
    # the updateVisualization(centerViews = True) function can be called
    # during script execution to update the opened views

    # the pauseScript() function can be called to pause the script execution.
    # To resume the script execution, you will have to click on the "Run script " button.

    # the runGraphScript(scriptFile, graph) function can be called to launch another edited script on a tlp.Graph object.
    # The scriptFile parameter defines the script name to call (in the form [a-zA-Z0-9_]+.py)

    # the main(graph) function must be defined
    # to run the script on the current graph
    # -----------------------------------------------------------

    # Can be used with nodes or edges
    def managePropertiesEntity(self, entTlp, entN4J, entProperties):
        # print 'WIP'
        for i in entN4J.properties:
            tmpValue = str(entN4J.properties[i])
            if i in self.labels:
                word = tmpValue.split(' ')
                if len(word) > 3:
                    tmpValue = "%s %s %s ..." % (word[0], word[1], word[2])
                entProperties["viewLabel"] = self.tulip_graph.getStringProperty("viewLabel")
                entProperties["viewLabel"][entTlp] = tmpValue
            if i in self.colors.keys():
                entProperties["viewColor"] = self.tulip_graph.getColorProperty("viewColor")
                entProperties["viewColor"][entTlp] = self.colors.get(i)
            if i in entProperties:
                entProperties[i][entTlp] = tmpValue
            else:
                # print type(tmpValue)
                entProperties[i] = self.tulip_graph.getStringProperty(i)
                # print 'i = ' + i
                # print 'has key ? ' + str(i in entProperties)
                entProperties[i][entTlp] = tmpValue

    def manageLabelsNode(self, labelsNode, nodeTlp, nodeN4J):
        # print "WIP"
        tmpArrayString = []
        for s in nodeN4J.properties:
            tmpArrayString.append(s)
        labelsNode[nodeTlp] = tmpArrayString


    # def manageLabelEdge(labelEdge,edgeTlp,edgeN4J):
    # 	labelEdge[edgeTlp] = edgeN4J.type

    # def testTransmmission(graph,node):
    # 	testNul = self.tulip_graph.getIntegerProperty("testNul")
    # 	strNul = "testNul"
    # 	exec(strNul)[node] = 1

    def create(self):
        # Entities properties
        tmpIDNode = self.tulip_graph.getIntegerProperty("tmpIDNode")
        tmpIDEdge = self.tulip_graph.getIntegerProperty("tmpIDEdge")
        labelsNodeTlp = self.tulip_graph.getStringVectorProperty("labelsNodeTlp")
        labelEdgeTlp = self.tulip_graph.getStringProperty("labelEdgeTlp")
        nodeProperties = {}
        edgeProperties = {}
        indexNodes = {}

        # Prepare node request
        nodes_req = "MATCH (n:user) "
        nodes_req += "RETURN ID(n),n"

        # Prepare edge comments request
        comment_edges_req = "MATCH (n1:user)-[:AUTHORSHIP]->(c:comment)-[:COMMENTS]->(p:post)<-[:AUTHORSHIP]-(n2:user) "
        comment_edges_req += "RETURN ID(n1),ID(n2),ID(c),ID(p)"

        # Prepare edge response request
        resp_edges_req = "MATCH (n1:user)-[:AUTHORSHIP]->(c:comment)-[:COMMENTS]->(c2:comment)<-[:AUTHORSHIP]-(n2:user) "
        resp_edges_req += "RETURN ID(n1),ID(n2)"

        # Get the users
        print("Read Users")
        result = self.neo4j_graph.run(nodes_req)
        for qr in result:
            n = self.tulip_graph.addNode()
            self.managePropertiesEntity(n, qr[1], nodeProperties)
            self.manageLabelsNode(labelsNodeTlp, n, qr[1])
            tmpIDNode[n] = qr[0]
            # keep the reference for edges creation
            indexNodes[qr[0]] = n

        # Get the comments edges
        print("Read Edges")
        result = self.neo4j_graph.run(comment_edges_req)
        for qr in result:
            if qr[0] in indexNodes and qr[1] in indexNodes:
                e = self.tulip_graph.addEdge(indexNodes[qr[0]], indexNodes[qr[1]])
                # self.managePropertiesEntity(e, qr[4], edgeProperties)
                # manageLabelEdge(labelEdgeTlp,e,qr[3])
                edgeProperties["viewLabel"] = self.tulip_graph.getStringProperty("viewLabel")
                edgeProperties["viewLabel"][e] = "COMMENTS"
                labelEdgeTlp[e] = "COMMENTS"

        # Get the resp edges
        print("Read Edges")
        result = self.neo4j_graph.run(resp_edges_req)
        for qr in result:
            if qr[0] in indexNodes and qr[1] in indexNodes:
                e = self.tulip_graph.addEdge(indexNodes[qr[0]], indexNodes[qr[1]])
                # self.managePropertiesEntity(e, qr[4], edgeProperties)
                # manageLabelEdge(labelEdgeTlp,e,qr[3])
                edgeProperties["viewLabel"] = self.tulip_graph.getStringProperty("viewLabel")
                edgeProperties["viewLabel"][e] = "REPLY"
                labelEdgeTlp[e] = "REPLY"

        print("Export")
        tlp.saveGraph(self.tulip_graph, "%s%s.tlp" % (config['exporter']['tlp_path'], "usersToUsers"))


