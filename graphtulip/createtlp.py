from tulip import *
from py2neo import *
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


class CreateTlp(object):
    def __init__(self):
        super(CreateTlp, self).__init__()
        print('Initializing')

        self.neo4j_graph = Graph(host=config['neo4j']['url'], user=config['neo4j']['user'], password=config['neo4j']['password'])
        self.tulip_graph = tlp.newGraph()
        self.tulip_graph.setName('opencare')

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
            if (i in entProperties):
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
        # View properties
        viewBorderColor = self.tulip_graph.getColorProperty("viewBorderColor")
        viewBorderWidth = self.tulip_graph.getDoubleProperty("viewBorderWidth")
        viewColor = self.tulip_graph.getColorProperty("viewColor")
        viewFont = self.tulip_graph.getStringProperty("viewFont")
        viewFontAwesomeIcon = self.tulip_graph.getStringProperty("viewFontAwesomeIcon")
        viewFontSize = self.tulip_graph.getIntegerProperty("viewFontSize")
        viewLabel = self.tulip_graph.getStringProperty("viewLabel")
        viewLabelBorderColor = self.tulip_graph.getColorProperty("viewLabelBorderColor")
        viewLabelBorderWidth = self.tulip_graph.getDoubleProperty("viewLabelBorderWidth")
        viewLabelColor = self.tulip_graph.getColorProperty("viewLabelColor")
        viewLabelPosition = self.tulip_graph.getIntegerProperty("viewLabelPosition")
        viewLayout = self.tulip_graph.getLayoutProperty("viewLayout")
        viewMetaGraph = self.tulip_graph.getGraphProperty("viewMetaGraph")
        viewMetric = self.tulip_graph.getDoubleProperty("viewMetric")
        viewRotation = self.tulip_graph.getDoubleProperty("viewRotation")
        viewSelection = self.tulip_graph.getBooleanProperty("viewSelection")
        viewShape = self.tulip_graph.getIntegerProperty("viewShape")
        viewSize = self.tulip_graph.getSizeProperty("viewSize")
        viewSrcAnchorShape = self.tulip_graph.getIntegerProperty("viewSrcAnchorShape")
        viewSrcAnchorSize = self.tulip_graph.getSizeProperty("viewSrcAnchorSize")
        viewTexture = self.tulip_graph.getStringProperty("viewTexture")
        viewTgtAnchorShape = self.tulip_graph.getIntegerProperty("viewTgtAnchorShape")
        viewTgtAnchorSize = self.tulip_graph.getSizeProperty("viewTgtAnchorSize")

        # Entities properties
        tmpIDNode = self.tulip_graph.getIntegerProperty("tmpIDNode")
        tmpIDEdge = self.tulip_graph.getIntegerProperty("tmpIDEdge")
        labelsNodeTlp = self.tulip_graph.getStringVectorProperty("labelsNodeTlp")
        labelEdgeTlp = self.tulip_graph.getStringProperty("labelEdgeTlp")
        nodeProperties = {}
        edgeProperties = {}
        indexNodes = {}

        # Get the nodes of Neo4J
        print("Read Nodes")
        for qr in self.neo4j_graph.run("MATCH (n) RETURN ID(n),n"):
            n = self.tulip_graph.addNode()
            self.managePropertiesEntity(n, qr[1], nodeProperties)
            self.manageLabelsNode(labelsNodeTlp, n, qr[1])
            tmpIDNode[n] = qr[0]
            # keep the reference for edges creation
            indexNodes[qr[0]] = n

        # Get the edges of Neo4J
        print("Read Edges")
        for qr in self.neo4j_graph.run("MATCH (n1)-[e]->(n2) RETURN ID(e),ID(n1),ID(n2),e"):
            # for n in self.tulip_graph.getNodes():
            # 	if(tmpIDNode[n]==qr[1]):
            # 		tmpNode1 = n
            # 	if(tmpIDNode[n]==qr[2]):
            # 		tmpNode2 = n
            # e = self.tulip_graph.addEdge(tmpNode1,tmpNode2)
            e = self.tulip_graph.addEdge(indexNodes[qr[1]], indexNodes[qr[2]])
            self.managePropertiesEntity(e, qr[3], edgeProperties)
            # manageLabelEdge(labelEdgeTlp,e,qr[3])
            labelEdgeTlp[e] = qr[3].type()
            tmpIDEdge[e] = qr[0]

        print("Apply LayoutAlgorithm")
        self.tulip_graph.applyLayoutAlgorithm("FM^3 (OGDF)")
        print("Export")
        filename = "complete"
        tlp.saveGraph(self.tulip_graph, "%s%s.tlp" % (config['exporter']['tlp_path'], filename))
        tlp.exportGraph("SIGMA JSON Export", self.tulip_graph, "%s%s.json" % (config['exporter']['json_path'], filename))


