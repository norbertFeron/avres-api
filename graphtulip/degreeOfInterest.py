import time

from tulip import *
from math import sqrt


class ComputeDoi(object):
    def __init__(self, graph):
        self.graph = graph
    # ---------------------------------------------------
    # return the API value for DOI computation
    def makeAPIdiff(self, n, sigma, maxMetric, metric):
        deg = float(metric[n])
        degHere = deg / maxMetric

        degN = 0.0
        for nn in self.graph.getInOutNodes(n):
            if (metric[nn] > degN):
                degN = float(metric[nn])  # on peut faire intervenir El pour mitiger le rsultat
        degN = degN / maxMetric
        return max(degHere, (sigma * degN))

    # ---------------------------------------------------
    # initialize dicType
    def initialisationDicCoverType(self, dic, allNodes, typeResource):
        for n in allNodes:
            tmpType = typeResource[n]
            if not (tmpType in dic):
                dic[tmpType] = 0

    # list the number of types in a list of nodes
    def fillDicCoverType(self, listn, dic, allNodes, typeResource):
        self.initialisationDicCoverType(dic, allNodes, typeResource)
        for n in listn:
            if (typeResource[n] != ''):
                typeTmp = typeResource[n]
                if (typeTmp in dic):
                    dic[typeTmp] += 1.0
                else:
                    dic[typeTmp] = 1.0

    # ---------------------------------------------------
    # return the value of the cover : 1 is good-covered, near 0 is garbage
    def calculateCoverMetric(self, dic):
        maxVal = 0.0
        actualVal = 0.0
        for val in dic.values():
            if (val > maxVal):
                maxVal = val
        for val in dic.values():
            tmp = (maxVal - val)
            actualVal += (tmp ** 2.0)
        return 1 - (actualVal / (len(dic) * (maxVal ** 2)))

    # return the value <nop>of variation</nop> of cover if this node goes in selected nodes
    def initCoverMetric(self, n, dic, typeResource):
        if (typeResource[n] != ""):
            # initalValue = calculateCoverMetric(dic)
            dic[typeResource[n]] += 1
            newValue = self.calculateCoverMetric(dic)
            dic[typeResource[n]] -= 1
            return newValue  # - initialValue
        return 1

    def personMetric(self, n, degree, degPersonMax):
        # print str(float(degree[n])/degPersonMax)
        return float(degree[n]) / degPersonMax

    # a lot of parameters are here to match only with a particular node type. Pretty ugly, doesnt it ?
    def selectUIAccordingNodeType(self, n, dic, typeResource, type_search, labelsNodeTlp, degree, degPersonMax):
        if (type_search[n] == "resource" or ("resource" in labelsNodeTlp[n])):
            return self.initCoverMetric(n, dic, typeResource)
        if (type_search[n] == "person" or ("person" in labelsNodeTlp[n])):
            return self.personMetric(n, degree, degPersonMax)
        if ("location" in labelsNodeTlp[n] or "organization" in labelsNodeTlp[n] or "collection" in labelsNodeTlp[n]):
            return 1
        return 0.5

    # ---------------------------------------------------
    # distance : 0, very close : near 1
    def preComputeDistanceDOI(self, listIsChosen, distanceToFocus, isChosen, viewLayout):
        # y
        distMax = 0.0
        lenList = float(len(listIsChosen))
        for n in self.graph.getNodes():
            distY = 0.0
            for y in listIsChosen:
                distTmp = sqrt((viewLayout[n][0] - viewLayout[y][0]) ** 2 + (viewLayout[n][1] - viewLayout[y][1]) ** 2)
                if (isChosen[y]):
                    distY += distTmp
            distaceToFocusTmp = distY / lenList
            distanceToFocus[n] = distaceToFocusTmp
            if (distaceToFocusTmp > distMax):
                distMax = distaceToFocusTmp

        for n in self.graph.getNodes():
            distanceToFocus[n] = (1.0 - (distanceToFocus[n] / distMax))

    # ---------------------------------------------------
    def makeUIdiff(self, n, dic, typeResource):

        return 0

    # ---------------------------------------------------
    def makeDOI(self, n, sigma, maxMetric, dic, metric, typeResource, distanceToFocus, scoreDOI, type_search, labelsNodeTlp,
                degree, degPersonMax):
        API = self.makeAPIdiff(n, sigma, maxMetric, metric)
        # print "API : " + str(API)
        UI = self.selectUIAccordingNodeType(n, dic, typeResource, type_search, labelsNodeTlp, degree, degPersonMax)
        # print "UI : " + str(UI)
        DIST = distanceToFocus[n]
        # print "DIST : " + str(DIST)
        DOI = API + UI + DIST
        scoreDOI[n] = DOI

    # print "DOI : " + str(DOI)
    # print scoreDOI[n]
    # ---------------------------------------------------
    def fonctionPrint(self, maxMetric):
        print(maxMetric)



    # ---------------------------------------------------
    def create(self, selection, sizeMaxDOIGraph, subName):

        degree = self.graph.getIntegerProperty("degree")
        labelsNodeTlp = self.graph.getStringVectorProperty("labelsNodeTlp")

        metric = self.graph.getDoubleProperty("metric")

        typeResource = self.graph.getStringProperty("typeResource")

        type_search = self.graph.getStringProperty("type_search")
        viewColor = self.graph.getColorProperty("viewColor")
        viewLayout = self.graph.getLayoutProperty("viewLayout")
        viewSelection = self.graph.getBooleanProperty("viewSelection")

        isCandidate = self.graph.getBooleanProperty("isCandidate")
        isChosen = self.graph.getBooleanProperty("isChosen")
        distanceToFocus = self.graph.getDoubleProperty("distanceToFocus")
        scoreDOI = self.graph.getDoubleProperty("scoreDOI")
        originalId = self.graph.getIntegerProperty("originalId")

        dicType = {}
        initialFocusNode = None
        listIsChosen = []
        candidateStack = []
        listNodesSubGraph = []

        # precomputed with an other script python
        degMax = 5794.0
        # precomputed with an other script python
        degPersonMax = 3401

        # sizeMaxDOIGraph = 120
        # How to select the focus node
        chooseFocusWith = "selection"  # id, doi, selection
        # According to chooseFocusWith, the value permitting the selection of a new focus node
        idFocusNode = ""  # "f72838f2-9915-4ca1-8be7-e822ac0cc5a2" #4603 #"f72838f2-9915-4ca1-8be7-e822ac0cc5a2"

        # Are you ready ?!
        start = time.time()

        ##########Init##########
        # select the focus node
        print("Mode : " + chooseFocusWith.upper())
        for n in self.graph.getNodes():
            originalId[n] = n.id
            if n.id in selection:
                isChosen[n] = True
                listIsChosen.append(n)
                # viewColor[n] = tlp.Color(20, 20, 255)
                # viewSize[n] = tlp.Size(2, 2, 1)
            # reset isCandidate
            isCandidate[n] = False

        print("Nodes currently chosen : " + str(listIsChosen) + ".")

        # determinate dicType
        self.fillDicCoverType(listIsChosen, dicType, self.graph.getNodes(), typeResource)

        # compute distance between focus node and others node in the self.graph
        if (listIsChosen):
            self.preComputeDistanceDOI(listIsChosen, distanceToFocus, isChosen, viewLayout)
        else:
            print("you need to select one or several nodes")

        ##########Compute DOI##########
        for n in self.graph.getNodes():
            self.makeDOI(n, 0.8, degMax, dicType, metric, typeResource, distanceToFocus, scoreDOI, type_search,
                    labelsNodeTlp, degree, degPersonMax)

        ##########New Subself.graph##########
        # Creation of the new subself.graph
        for n in listIsChosen:
            listNodesSubGraph.append(n)
            viewSelection[n] = True
            isCandidate[n] = True
            for nn in self.graph.getInOutNodes(n):
                if (isCandidate[nn] == False):
                    candidateStack.append(nn)
                    isCandidate[nn] = True
        # candidateStack = list(set(candidateStack))

        cmpt = 0.0
        while ((len(candidateStack) != 0) and (cmpt < sizeMaxDOIGraph)):
            nodeWithDOImax = candidateStack[0];
            for n in candidateStack:
                if (scoreDOI[n] > scoreDOI[nodeWithDOImax]):
                    nodeWithDOImax = n
            for nn in self.graph.getInOutNodes(nodeWithDOImax):
                if (isCandidate[nn] == False):
                    candidateStack.append(nn)
                    isCandidate[nn] = True
            listNodesSubGraph.append(nodeWithDOImax)
            candidateStack.remove(nodeWithDOImax)
            cmpt += 1
            print("--- " + str(int((cmpt / sizeMaxDOIGraph) * 100)) + "% ---")


        # Done
        end = time.time()
        print("Time(s) : " + str(end - start))
        return self.graph.inducedSubGraph(listNodesSubGraph, self.graph, subName)
