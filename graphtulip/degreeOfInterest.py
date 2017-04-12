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
        print
        maxMetric



    # ---------------------------------------------------
    def create(self, selection, sizeMaxDOIGraph, subName):

        AllAnnotated = self.graph.getStringProperty("AllAnnotated")
        ColorSpectrum = self.graph.getStringProperty("ColorSpectrum")
        about = self.graph.getStringProperty("about")
        abstract_de = self.graph.getStringProperty("abstract_de")
        abstract_en = self.graph.getStringProperty("abstract_en")
        abstract_fr = self.graph.getStringProperty("abstract_fr")
        alchemyapi_reconciliated = self.graph.getStringProperty("alchemyapi_reconciliated")
        animetrics_annotated = self.graph.getStringProperty("animetrics_annotated")
        answered_by = self.graph.getStringProperty("answered_by")
        batch = self.graph.getStringProperty("batch")
        birth_date = self.graph.getStringProperty("birth_date")
        birth_place = self.graph.getStringProperty("birth_place")
        birth_time = self.graph.getStringProperty("birth_time")
        caption = self.graph.getStringProperty("caption")
        caption_cs = self.graph.getStringProperty("caption_cs")
        caption_da = self.graph.getStringProperty("caption_da")
        caption_de = self.graph.getStringProperty("caption_de")
        caption_el = self.graph.getStringProperty("caption_el")
        caption_en = self.graph.getStringProperty("caption_en")
        caption_es = self.graph.getStringProperty("caption_es")
        caption_fr = self.graph.getStringProperty("caption_fr")
        caption_gl = self.graph.getStringProperty("caption_gl")
        caption_hr = self.graph.getStringProperty("caption_hr")
        caption_hu = self.graph.getStringProperty("caption_hu")
        caption_it = self.graph.getStringProperty("caption_it")
        caption_la = self.graph.getStringProperty("caption_la")
        caption_lt = self.graph.getStringProperty("caption_lt")
        caption_lu = self.graph.getStringProperty("caption_lu")
        caption_lv = self.graph.getStringProperty("caption_lv")
        caption_nl = self.graph.getStringProperty("caption_nl")
        caption_pt = self.graph.getStringProperty("caption_pt")
        caption_search = self.graph.getStringProperty("caption_search")
        caption_sl = self.graph.getStringProperty("caption_sl")
        caption_sv = self.graph.getStringProperty("caption_sv")
        cdiff = self.graph.getStringProperty("cdiff")
        celebrity = self.graph.getStringProperty("celebrity")
        cloned = self.graph.getStringProperty("cloned")
        colorized = self.graph.getStringProperty("colorized")
        content = self.graph.getStringProperty("content")
        copyright_ = self.graph.getStringProperty("copyright")
        country = self.graph.getStringProperty("country")
        created_by = self.graph.getStringProperty("created_by")
        creation_date = self.graph.getStringProperty("creation_date")
        creation_time = self.graph.getStringProperty("creation_time")
        cs_url = self.graph.getStringProperty("cs_url")
        da_url = self.graph.getStringProperty("da_url")
        date = self.graph.getStringProperty("date")
        date_languages = self.graph.getStringProperty("date_languages")
        de_url = self.graph.getStringProperty("de_url")
        death_date = self.graph.getStringProperty("death_date")
        death_place = self.graph.getStringProperty("death_place")
        death_time = self.graph.getStringProperty("death_time")
        degree = self.graph.getIntegerProperty("degree")
        description = self.graph.getStringProperty("description")
        df = self.graph.getStringProperty("df")
        discovered = self.graph.getStringProperty("discovered")
        doi = self.graph.getStringProperty("doi")
        downvote = self.graph.getStringProperty("downvote")
        ecmd = self.graph.getStringProperty("ecmd")
        el_url = self.graph.getStringProperty("el_url")
        email = self.graph.getStringProperty("email")
        en_url = self.graph.getStringProperty("en_url")
        end_date = self.graph.getStringProperty("end_date")
        end_month = self.graph.getStringProperty("end_month")
        end_time = self.graph.getStringProperty("end_time")
        ent_time = self.graph.getStringProperty("ent_time")
        es_url = self.graph.getStringProperty("es_url")
        favourited = self.graph.getStringProperty("favourited")
        fi_url = self.graph.getStringProperty("fi_url")
        first = self.graph.getStringProperty("first")
        first_name = self.graph.getStringProperty("first_name")
        firstname = self.graph.getStringProperty("firstname")
        fr_url = self.graph.getStringProperty("fr_url")
        frequency = self.graph.getStringProperty("frequency")
        full_search = self.graph.getStringProperty("full_search")
        gender = self.graph.getStringProperty("gender")
        geocode_bounds_ne_lat = self.graph.getStringProperty("geocode_bounds_ne_lat")
        geocode_bounds_ne_lng = self.graph.getStringProperty("geocode_bounds_ne_lng")
        geocode_bounds_sw_lat = self.graph.getStringProperty("geocode_bounds_sw_lat")
        geocode_bounds_sw_lng = self.graph.getStringProperty("geocode_bounds_sw_lng")
        geocode_countryId = self.graph.getStringProperty("geocode_countryId")
        geocode_countryName = self.graph.getStringProperty("geocode_countryName")
        geocode_formatted_address = self.graph.getStringProperty("geocode_formatted_address")
        geocode_id = self.graph.getStringProperty("geocode_id")
        geocode_lat = self.graph.getStringProperty("geocode_lat")
        geocode_lng = self.graph.getStringProperty("geocode_lng")
        geocode_query = self.graph.getStringProperty("geocode_query")
        geocode_toponymName = self.graph.getStringProperty("geocode_toponymName")
        geocoding_annotated = self.graph.getStringProperty("geocoding_annotated")
        geocoding_country = self.graph.getStringProperty("geocoding_country")
        geocoding_fcl = self.graph.getStringProperty("geocoding_fcl")
        geocoding_id = self.graph.getStringProperty("geocoding_id")
        geoname_country = self.graph.getStringProperty("geoname_country")
        geoname_fcl = self.graph.getStringProperty("geoname_fcl")
        geoname_id = self.graph.getStringProperty("geoname_id")
        geonames_annotated = self.graph.getStringProperty("geonames_annotated")
        geonames_countryCode = self.graph.getStringProperty("geonames_countryCode")
        geonames_countryId = self.graph.getStringProperty("geonames_countryId")
        geonames_countryName = self.graph.getStringProperty("geonames_countryName")
        geonames_id = self.graph.getStringProperty("geonames_id")
        geonames_lat = self.graph.getStringProperty("geonames_lat")
        geonames_lng = self.graph.getStringProperty("geonames_lng")
        geonames_query = self.graph.getStringProperty("geonames_query")
        geonames_toponymName = self.graph.getStringProperty("geonames_toponymName")
        height = self.graph.getStringProperty("height")
        intersections = self.graph.getStringProperty("intersections")
        ipr_ca = self.graph.getStringProperty("ipr_ca")
        ipr_cs = self.graph.getStringProperty("ipr_cs")
        ipr_da = self.graph.getStringProperty("ipr_da")
        ipr_de = self.graph.getStringProperty("ipr_de")
        ipr_el = self.graph.getStringProperty("ipr_el")
        ipr_en = self.graph.getStringProperty("ipr_en")
        ipr_es = self.graph.getStringProperty("ipr_es")
        ipr_et = self.graph.getStringProperty("ipr_et")
        ipr_fi = self.graph.getStringProperty("ipr_fi")
        ipr_fr = self.graph.getStringProperty("ipr_fr")
        ipr_ga = self.graph.getStringProperty("ipr_ga")
        ipr_gl = self.graph.getStringProperty("ipr_gl")
        ipr_hu = self.graph.getStringProperty("ipr_hu")
        ipr_it = self.graph.getStringProperty("ipr_it")
        ipr_lt = self.graph.getStringProperty("ipr_lt")
        ipr_lu = self.graph.getStringProperty("ipr_lu")
        ipr_lv = self.graph.getStringProperty("ipr_lv")
        ipr_mt = self.graph.getStringProperty("ipr_mt")
        ipr_nl = self.graph.getStringProperty("ipr_nl")
        ipr_no = self.graph.getStringProperty("ipr_no")
        ipr_pl = self.graph.getStringProperty("ipr_pl")
        ipr_pt = self.graph.getStringProperty("ipr_pt")
        ipr_ru = self.graph.getStringProperty("ipr_ru")
        ipr_sk = self.graph.getStringProperty("ipr_sk")
        ipr_sl = self.graph.getStringProperty("ipr_sl")
        ipr_sv = self.graph.getStringProperty("ipr_sv")
        is_uncertain = self.graph.getStringProperty("is_uncertain")
        it_url = self.graph.getStringProperty("it_url")
        jaccard = self.graph.getStringProperty("jaccard")
        labelEdgeTlp = self.graph.getStringProperty("labelEdgeTlp")
        labelsNodeTlp = self.graph.getStringVectorProperty("labelsNodeTlp")
        language = self.graph.getStringProperty("language")
        languages = self.graph.getStringProperty("languages")
        last_modification_date = self.graph.getStringProperty("last_modification_date")
        last_modification_time = self.graph.getStringProperty("last_modification_time")
        last_name = self.graph.getStringProperty("last_name")
        lat = self.graph.getStringProperty("lat")
        links_viaf = self.graph.getStringProperty("links_viaf")
        links_wiki = self.graph.getStringProperty("links_wiki")
        links_worldcat = self.graph.getStringProperty("links_worldcat")
        links_yago = self.graph.getStringProperty("links_yago")
        lng = self.graph.getStringProperty("lng")
        lu_url = self.graph.getStringProperty("lu_url")
        merged_with = self.graph.getStringProperty("merged_with")

        metric = self.graph.getDoubleProperty("metric")

        mimetype = self.graph.getStringProperty("mimetype")
        mt_url = self.graph.getStringProperty("mt_url")
        name = self.graph.getStringProperty("name")
        name_en = self.graph.getStringProperty("name_en")
        name_search = self.graph.getStringProperty("name_search")
        nl_url = self.graph.getStringProperty("nl_url")
        no_url = self.graph.getStringProperty("no_url")
        overlapping = self.graph.getStringProperty("overlapping")
        password = self.graph.getStringProperty("password")
        persons = self.graph.getStringProperty("persons")
        picture = self.graph.getStringProperty("picture")
        picture_source = self.graph.getStringProperty("picture_source")
        pl_url = self.graph.getStringProperty("pl_url")
        place = self.graph.getStringProperty("place")
        pt_url = self.graph.getStringProperty("pt_url")
        reference = self.graph.getStringProperty("reference")
        refersTo = self.graph.getStringProperty("refersTo")
        rekognition_annotated = self.graph.getStringProperty("rekognition_annotated")
        resource = self.graph.getStringProperty("resource")
        ru_url = self.graph.getStringProperty("ru_url")
        salt = self.graph.getStringProperty("salt")
        score = self.graph.getStringProperty("score")
        service = self.graph.getStringProperty("service")
        services = self.graph.getStringProperty("services")
        slug = self.graph.getStringProperty("slug")
        solution = self.graph.getStringProperty("solution")
        sort_index = self.graph.getStringProperty("sort_index")
        source = self.graph.getStringProperty("source")
        source_en = self.graph.getStringProperty("source_en")
        specificity = self.graph.getStringProperty("specificity")
        stakeholders = self.graph.getStringProperty("stakeholders")
        start_date = self.graph.getStringProperty("start_date")
        start_month = self.graph.getStringProperty("start_month")
        start_time = self.graph.getStringProperty("start_time")
        status = self.graph.getStringProperty("status")
        strategy = self.graph.getStringProperty("strategy")
        sv_url = self.graph.getStringProperty("sv_url")
        tags = self.graph.getStringProperty("tags")
        tdf = self.graph.getStringProperty("tdf")
        textrazor_annotated = self.graph.getStringProperty("textrazor_annotated")
        textrazor_reconciliated = self.graph.getStringProperty("textrazor_reconciliated")
        tf = self.graph.getStringProperty("tf")
        tfidf = self.graph.getStringProperty("tfidf")
        thumbnail = self.graph.getStringProperty("thumbnail")
        title = self.graph.getStringProperty("title")
        title_ar = self.graph.getStringProperty("title_ar")
        title_ca = self.graph.getStringProperty("title_ca")
        title_cs = self.graph.getStringProperty("title_cs")
        title_da = self.graph.getStringProperty("title_da")
        title_de = self.graph.getStringProperty("title_de")
        title_el = self.graph.getStringProperty("title_el")
        title_en = self.graph.getStringProperty("title_en")
        title_es = self.graph.getStringProperty("title_es")
        title_et = self.graph.getStringProperty("title_et")
        title_fi = self.graph.getStringProperty("title_fi")
        title_fr = self.graph.getStringProperty("title_fr")
        title_gl = self.graph.getStringProperty("title_gl")
        title_hr = self.graph.getStringProperty("title_hr")
        title_hu = self.graph.getStringProperty("title_hu")
        title_it = self.graph.getStringProperty("title_it")
        title_lt = self.graph.getStringProperty("title_lt")
        title_lu = self.graph.getStringProperty("title_lu")
        title_lv = self.graph.getStringProperty("title_lv")
        title_mt = self.graph.getStringProperty("title_mt")
        title_nl = self.graph.getStringProperty("title_nl")
        title_no = self.graph.getStringProperty("title_no")
        title_pl = self.graph.getStringProperty("title_pl")
        title_pt = self.graph.getStringProperty("title_pt")
        title_ru = self.graph.getStringProperty("title_ru")
        title_search = self.graph.getStringProperty("title_search")
        title_sk = self.graph.getStringProperty("title_sk")
        title_sl = self.graph.getStringProperty("title_sl")
        title_sv = self.graph.getStringProperty("title_sv")
        tmpIDEdge = self.graph.getIntegerProperty("tmpIDEdge")
        tmpIDNode = self.graph.getIntegerProperty("tmpIDNode")
        trustworthiness = self.graph.getStringProperty("trustworthiness")
        type_ = self.graph.getStringProperty("type")

        typeResource = self.graph.getStringProperty("typeResource")

        type_search = self.graph.getStringProperty("type_search")
        union = self.graph.getStringProperty("union")
        unknowns = self.graph.getStringProperty("unknowns")
        upvote = self.graph.getStringProperty("upvote")
        uri = self.graph.getStringProperty("uri")
        url = self.graph.getStringProperty("url")
        url_cs = self.graph.getStringProperty("url_cs")
        url_da = self.graph.getStringProperty("url_da")
        url_de = self.graph.getStringProperty("url_de")
        url_el = self.graph.getStringProperty("url_el")
        url_en = self.graph.getStringProperty("url_en")
        url_es = self.graph.getStringProperty("url_es")
        url_fi = self.graph.getStringProperty("url_fi")
        url_fr = self.graph.getStringProperty("url_fr")
        url_it = self.graph.getStringProperty("url_it")
        url_lu = self.graph.getStringProperty("url_lu")
        url_mt = self.graph.getStringProperty("url_mt")
        url_nl = self.graph.getStringProperty("url_nl")
        url_no = self.graph.getStringProperty("url_no")
        url_pl = self.graph.getStringProperty("url_pl")
        url_pt = self.graph.getStringProperty("url_pt")
        url_ru = self.graph.getStringProperty("url_ru")
        url_sv = self.graph.getStringProperty("url_sv")
        username = self.graph.getStringProperty("username")
        viewBorderColor = self.graph.getColorProperty("viewBorderColor")
        viewBorderWidth = self.graph.getDoubleProperty("viewBorderWidth")
        viewColor = self.graph.getColorProperty("viewColor")
        viewFont = self.graph.getStringProperty("viewFont")
        viewFontAwesomeIcon = self.graph.getStringProperty("viewFontAwesomeIcon")
        viewFontSize = self.graph.getIntegerProperty("viewFontSize")
        viewLabel = self.graph.getStringProperty("viewLabel")
        viewLabelBorderColor = self.graph.getColorProperty("viewLabelBorderColor")
        viewLabelBorderWidth = self.graph.getDoubleProperty("viewLabelBorderWidth")
        viewLabelColor = self.graph.getColorProperty("viewLabelColor")
        viewLabelPosition = self.graph.getIntegerProperty("viewLabelPosition")
        viewLayout = self.graph.getLayoutProperty("viewLayout")
        viewMetric = self.graph.getDoubleProperty("viewMetric")
        viewRotation = self.graph.getDoubleProperty("viewRotation")
        viewSelection = self.graph.getBooleanProperty("viewSelection")
        viewShape = self.graph.getIntegerProperty("viewShape")
        viewSize = self.graph.getSizeProperty("viewSize")
        viewSrcAnchorShape = self.graph.getIntegerProperty("viewSrcAnchorShape")
        viewSrcAnchorSize = self.graph.getSizeProperty("viewSrcAnchorSize")
        viewTexture = self.graph.getStringProperty("viewTexture")
        viewTgtAnchorShape = self.graph.getIntegerProperty("viewTgtAnchorShape")
        viewTgtAnchorSize = self.graph.getSizeProperty("viewTgtAnchorSize")
        width = self.graph.getStringProperty("width")
        yago_annotated = self.graph.getStringProperty("yago_annotated")
        yaml = self.graph.getStringProperty("yaml")

        isCandidate = self.graph.getBooleanProperty("isCandidate")
        isChosen = self.graph.getBooleanProperty("isChosen")
        distanceToFocus = self.graph.getDoubleProperty("distanceToFocus")
        distanceMax = self.graph.getDoubleProperty("distanceMax")
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
            if str(n.id) in selection:
                isChosen[n] = True
                listIsChosen.append(n)
                viewColor[n] = tlp.Color(20, 20, 255)
                viewSize[n] = tlp.Size(2, 2, 1)
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
