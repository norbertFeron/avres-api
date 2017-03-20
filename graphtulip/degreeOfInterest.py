import configparser
import time

from tulip import *
from math import sqrt

config = configparser.ConfigParser()
config.read("config.ini")

# todo : connect to neo4j
graph = tlp.loadGraph(config['importer']['doi_data'])

# ---------------------------------------------------
# return the API value for DOI computation
def makeAPIdiff(n, sigma, maxMetric, metric):
    deg = float(metric[n])
    degHere = deg / maxMetric

    degN = 0.0
    for nn in graph.getInOutNodes(n):
        if (metric[nn] > degN):
            degN = float(metric[nn])  # on peut faire intervenir El pour mitiger le rsultat
    degN = degN / maxMetric
    return max(degHere, (sigma * degN))

# ---------------------------------------------------
# initialize dicType
def initialisationDicCoverType(dic, allNodes, typeResource):
    for n in allNodes:
        tmpType = typeResource[n]
        if not (tmpType in dic):
            dic[tmpType] = 0

# list the number of types in a list of nodes
def fillDicCoverType(listn, dic, allNodes, typeResource):
    initialisationDicCoverType(dic, allNodes, typeResource)
    for n in listn:
        if (typeResource[n] != ''):
            typeTmp = typeResource[n]
            if (typeTmp in dic):
                dic[typeTmp] += 1.0
            else:
                dic[typeTmp] = 1.0

# ---------------------------------------------------
# return the value of the cover : 1 is good-covered, near 0 is garbage
def calculateCoverMetric(dic):
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
def initCoverMetric(n, dic, typeResource):
    if (typeResource[n] != ""):
        # initalValue = calculateCoverMetric(dic)
        dic[typeResource[n]] += 1
        newValue = calculateCoverMetric(dic)
        dic[typeResource[n]] -= 1
        return newValue  # - initialValue
    return 1

def personMetric(n, degree, degPersonMax):
    # print str(float(degree[n])/degPersonMax)
    return float(degree[n]) / degPersonMax

# a lot of parameters are here to match only with a particular node type. Pretty ugly, doesnt it ?
def selectUIAccordingNodeType(n, dic, typeResource, type_search, labelsNodeTlp, degree, degPersonMax):
    if (type_search[n] == "resource" or ("resource" in labelsNodeTlp[n])):
        return initCoverMetric(n, dic, typeResource)
    if (type_search[n] == "person" or ("person" in labelsNodeTlp[n])):
        return personMetric(n, degree, degPersonMax)
    if ("location" in labelsNodeTlp[n] or "organization" in labelsNodeTlp[n] or "collection" in labelsNodeTlp[n]):
        return 1
    return 0.5

# ---------------------------------------------------
# distance : 0, very close : near 1
def preComputeDistanceDOI(graph, listIsChosen, distanceToFocus, isChosen, viewLayout):
    # y
    distMax = 0.0
    lenList = float(len(listIsChosen))
    for n in graph.getNodes():
        distY = 0.0
        for y in listIsChosen:
            distTmp = sqrt((viewLayout[n][0] - viewLayout[y][0]) ** 2 + (viewLayout[n][1] - viewLayout[y][1]) ** 2)
            if (isChosen[y]):
                distY += distTmp
        distaceToFocusTmp = distY / lenList
        distanceToFocus[n] = distaceToFocusTmp
        if (distaceToFocusTmp > distMax):
            distMax = distaceToFocusTmp

    for n in graph.getNodes():
        distanceToFocus[n] = (1.0 - (distanceToFocus[n] / distMax))

# ---------------------------------------------------
def makeUIdiff(n, dic, typeResource):

    return 0

# ---------------------------------------------------
def makeDOI(n, sigma, maxMetric, dic, metric, typeResource, distanceToFocus, scoreDOI, type_search, labelsNodeTlp,
            degree, degPersonMax):
    API = makeAPIdiff(n, sigma, maxMetric, metric)
    # print "API : " + str(API)
    UI = selectUIAccordingNodeType(n, dic, typeResource, type_search, labelsNodeTlp, degree, degPersonMax)
    # print "UI : " + str(UI)
    DIST = distanceToFocus[n]
    # print "DIST : " + str(DIST)
    DOI = API + UI + DIST
    scoreDOI[n] = DOI

# print "DOI : " + str(DOI)
# print scoreDOI[n]
# ---------------------------------------------------
def fonctionPrint(maxMetric):
    print
    maxMetric


# ---------------------------------------------------
def create(private_gid, selection):

    AllAnnotated = graph.getStringProperty("AllAnnotated")
    ColorSpectrum = graph.getStringProperty("ColorSpectrum")
    about = graph.getStringProperty("about")
    abstract_de = graph.getStringProperty("abstract_de")
    abstract_en = graph.getStringProperty("abstract_en")
    abstract_fr = graph.getStringProperty("abstract_fr")
    alchemyapi_reconciliated = graph.getStringProperty("alchemyapi_reconciliated")
    animetrics_annotated = graph.getStringProperty("animetrics_annotated")
    answered_by = graph.getStringProperty("answered_by")
    batch = graph.getStringProperty("batch")
    birth_date = graph.getStringProperty("birth_date")
    birth_place = graph.getStringProperty("birth_place")
    birth_time = graph.getStringProperty("birth_time")
    caption = graph.getStringProperty("caption")
    caption_cs = graph.getStringProperty("caption_cs")
    caption_da = graph.getStringProperty("caption_da")
    caption_de = graph.getStringProperty("caption_de")
    caption_el = graph.getStringProperty("caption_el")
    caption_en = graph.getStringProperty("caption_en")
    caption_es = graph.getStringProperty("caption_es")
    caption_fr = graph.getStringProperty("caption_fr")
    caption_gl = graph.getStringProperty("caption_gl")
    caption_hr = graph.getStringProperty("caption_hr")
    caption_hu = graph.getStringProperty("caption_hu")
    caption_it = graph.getStringProperty("caption_it")
    caption_la = graph.getStringProperty("caption_la")
    caption_lt = graph.getStringProperty("caption_lt")
    caption_lu = graph.getStringProperty("caption_lu")
    caption_lv = graph.getStringProperty("caption_lv")
    caption_nl = graph.getStringProperty("caption_nl")
    caption_pt = graph.getStringProperty("caption_pt")
    caption_search = graph.getStringProperty("caption_search")
    caption_sl = graph.getStringProperty("caption_sl")
    caption_sv = graph.getStringProperty("caption_sv")
    cdiff = graph.getStringProperty("cdiff")
    celebrity = graph.getStringProperty("celebrity")
    cloned = graph.getStringProperty("cloned")
    colorized = graph.getStringProperty("colorized")
    content = graph.getStringProperty("content")
    copyright_ = graph.getStringProperty("copyright")
    country = graph.getStringProperty("country")
    created_by = graph.getStringProperty("created_by")
    creation_date = graph.getStringProperty("creation_date")
    creation_time = graph.getStringProperty("creation_time")
    cs_url = graph.getStringProperty("cs_url")
    da_url = graph.getStringProperty("da_url")
    date = graph.getStringProperty("date")
    date_languages = graph.getStringProperty("date_languages")
    de_url = graph.getStringProperty("de_url")
    death_date = graph.getStringProperty("death_date")
    death_place = graph.getStringProperty("death_place")
    death_time = graph.getStringProperty("death_time")
    degree = graph.getIntegerProperty("degree")
    description = graph.getStringProperty("description")
    df = graph.getStringProperty("df")
    discovered = graph.getStringProperty("discovered")
    doi = graph.getStringProperty("doi")
    downvote = graph.getStringProperty("downvote")
    ecmd = graph.getStringProperty("ecmd")
    el_url = graph.getStringProperty("el_url")
    email = graph.getStringProperty("email")
    en_url = graph.getStringProperty("en_url")
    end_date = graph.getStringProperty("end_date")
    end_month = graph.getStringProperty("end_month")
    end_time = graph.getStringProperty("end_time")
    ent_time = graph.getStringProperty("ent_time")
    es_url = graph.getStringProperty("es_url")
    favourited = graph.getStringProperty("favourited")
    fi_url = graph.getStringProperty("fi_url")
    first = graph.getStringProperty("first")
    first_name = graph.getStringProperty("first_name")
    firstname = graph.getStringProperty("firstname")
    fr_url = graph.getStringProperty("fr_url")
    frequency = graph.getStringProperty("frequency")
    full_search = graph.getStringProperty("full_search")
    gender = graph.getStringProperty("gender")
    geocode_bounds_ne_lat = graph.getStringProperty("geocode_bounds_ne_lat")
    geocode_bounds_ne_lng = graph.getStringProperty("geocode_bounds_ne_lng")
    geocode_bounds_sw_lat = graph.getStringProperty("geocode_bounds_sw_lat")
    geocode_bounds_sw_lng = graph.getStringProperty("geocode_bounds_sw_lng")
    geocode_countryId = graph.getStringProperty("geocode_countryId")
    geocode_countryName = graph.getStringProperty("geocode_countryName")
    geocode_formatted_address = graph.getStringProperty("geocode_formatted_address")
    geocode_id = graph.getStringProperty("geocode_id")
    geocode_lat = graph.getStringProperty("geocode_lat")
    geocode_lng = graph.getStringProperty("geocode_lng")
    geocode_query = graph.getStringProperty("geocode_query")
    geocode_toponymName = graph.getStringProperty("geocode_toponymName")
    geocoding_annotated = graph.getStringProperty("geocoding_annotated")
    geocoding_country = graph.getStringProperty("geocoding_country")
    geocoding_fcl = graph.getStringProperty("geocoding_fcl")
    geocoding_id = graph.getStringProperty("geocoding_id")
    geoname_country = graph.getStringProperty("geoname_country")
    geoname_fcl = graph.getStringProperty("geoname_fcl")
    geoname_id = graph.getStringProperty("geoname_id")
    geonames_annotated = graph.getStringProperty("geonames_annotated")
    geonames_countryCode = graph.getStringProperty("geonames_countryCode")
    geonames_countryId = graph.getStringProperty("geonames_countryId")
    geonames_countryName = graph.getStringProperty("geonames_countryName")
    geonames_id = graph.getStringProperty("geonames_id")
    geonames_lat = graph.getStringProperty("geonames_lat")
    geonames_lng = graph.getStringProperty("geonames_lng")
    geonames_query = graph.getStringProperty("geonames_query")
    geonames_toponymName = graph.getStringProperty("geonames_toponymName")
    height = graph.getStringProperty("height")
    intersections = graph.getStringProperty("intersections")
    ipr_ca = graph.getStringProperty("ipr_ca")
    ipr_cs = graph.getStringProperty("ipr_cs")
    ipr_da = graph.getStringProperty("ipr_da")
    ipr_de = graph.getStringProperty("ipr_de")
    ipr_el = graph.getStringProperty("ipr_el")
    ipr_en = graph.getStringProperty("ipr_en")
    ipr_es = graph.getStringProperty("ipr_es")
    ipr_et = graph.getStringProperty("ipr_et")
    ipr_fi = graph.getStringProperty("ipr_fi")
    ipr_fr = graph.getStringProperty("ipr_fr")
    ipr_ga = graph.getStringProperty("ipr_ga")
    ipr_gl = graph.getStringProperty("ipr_gl")
    ipr_hu = graph.getStringProperty("ipr_hu")
    ipr_it = graph.getStringProperty("ipr_it")
    ipr_lt = graph.getStringProperty("ipr_lt")
    ipr_lu = graph.getStringProperty("ipr_lu")
    ipr_lv = graph.getStringProperty("ipr_lv")
    ipr_mt = graph.getStringProperty("ipr_mt")
    ipr_nl = graph.getStringProperty("ipr_nl")
    ipr_no = graph.getStringProperty("ipr_no")
    ipr_pl = graph.getStringProperty("ipr_pl")
    ipr_pt = graph.getStringProperty("ipr_pt")
    ipr_ru = graph.getStringProperty("ipr_ru")
    ipr_sk = graph.getStringProperty("ipr_sk")
    ipr_sl = graph.getStringProperty("ipr_sl")
    ipr_sv = graph.getStringProperty("ipr_sv")
    is_uncertain = graph.getStringProperty("is_uncertain")
    it_url = graph.getStringProperty("it_url")
    jaccard = graph.getStringProperty("jaccard")
    labelEdgeTlp = graph.getStringProperty("labelEdgeTlp")
    labelsNodeTlp = graph.getStringVectorProperty("labelsNodeTlp")
    language = graph.getStringProperty("language")
    languages = graph.getStringProperty("languages")
    last_modification_date = graph.getStringProperty("last_modification_date")
    last_modification_time = graph.getStringProperty("last_modification_time")
    last_name = graph.getStringProperty("last_name")
    lat = graph.getStringProperty("lat")
    links_viaf = graph.getStringProperty("links_viaf")
    links_wiki = graph.getStringProperty("links_wiki")
    links_worldcat = graph.getStringProperty("links_worldcat")
    links_yago = graph.getStringProperty("links_yago")
    lng = graph.getStringProperty("lng")
    lu_url = graph.getStringProperty("lu_url")
    merged_with = graph.getStringProperty("merged_with")

    metric = graph.getDoubleProperty("metric")

    mimetype = graph.getStringProperty("mimetype")
    mt_url = graph.getStringProperty("mt_url")
    name = graph.getStringProperty("name")
    name_en = graph.getStringProperty("name_en")
    name_search = graph.getStringProperty("name_search")
    nl_url = graph.getStringProperty("nl_url")
    no_url = graph.getStringProperty("no_url")
    overlapping = graph.getStringProperty("overlapping")
    password = graph.getStringProperty("password")
    persons = graph.getStringProperty("persons")
    picture = graph.getStringProperty("picture")
    picture_source = graph.getStringProperty("picture_source")
    pl_url = graph.getStringProperty("pl_url")
    place = graph.getStringProperty("place")
    pt_url = graph.getStringProperty("pt_url")
    reference = graph.getStringProperty("reference")
    refersTo = graph.getStringProperty("refersTo")
    rekognition_annotated = graph.getStringProperty("rekognition_annotated")
    resource = graph.getStringProperty("resource")
    ru_url = graph.getStringProperty("ru_url")
    salt = graph.getStringProperty("salt")
    score = graph.getStringProperty("score")
    service = graph.getStringProperty("service")
    services = graph.getStringProperty("services")
    slug = graph.getStringProperty("slug")
    solution = graph.getStringProperty("solution")
    sort_index = graph.getStringProperty("sort_index")
    source = graph.getStringProperty("source")
    source_en = graph.getStringProperty("source_en")
    specificity = graph.getStringProperty("specificity")
    stakeholders = graph.getStringProperty("stakeholders")
    start_date = graph.getStringProperty("start_date")
    start_month = graph.getStringProperty("start_month")
    start_time = graph.getStringProperty("start_time")
    status = graph.getStringProperty("status")
    strategy = graph.getStringProperty("strategy")
    sv_url = graph.getStringProperty("sv_url")
    tags = graph.getStringProperty("tags")
    tdf = graph.getStringProperty("tdf")
    textrazor_annotated = graph.getStringProperty("textrazor_annotated")
    textrazor_reconciliated = graph.getStringProperty("textrazor_reconciliated")
    tf = graph.getStringProperty("tf")
    tfidf = graph.getStringProperty("tfidf")
    thumbnail = graph.getStringProperty("thumbnail")
    title = graph.getStringProperty("title")
    title_ar = graph.getStringProperty("title_ar")
    title_ca = graph.getStringProperty("title_ca")
    title_cs = graph.getStringProperty("title_cs")
    title_da = graph.getStringProperty("title_da")
    title_de = graph.getStringProperty("title_de")
    title_el = graph.getStringProperty("title_el")
    title_en = graph.getStringProperty("title_en")
    title_es = graph.getStringProperty("title_es")
    title_et = graph.getStringProperty("title_et")
    title_fi = graph.getStringProperty("title_fi")
    title_fr = graph.getStringProperty("title_fr")
    title_gl = graph.getStringProperty("title_gl")
    title_hr = graph.getStringProperty("title_hr")
    title_hu = graph.getStringProperty("title_hu")
    title_it = graph.getStringProperty("title_it")
    title_lt = graph.getStringProperty("title_lt")
    title_lu = graph.getStringProperty("title_lu")
    title_lv = graph.getStringProperty("title_lv")
    title_mt = graph.getStringProperty("title_mt")
    title_nl = graph.getStringProperty("title_nl")
    title_no = graph.getStringProperty("title_no")
    title_pl = graph.getStringProperty("title_pl")
    title_pt = graph.getStringProperty("title_pt")
    title_ru = graph.getStringProperty("title_ru")
    title_search = graph.getStringProperty("title_search")
    title_sk = graph.getStringProperty("title_sk")
    title_sl = graph.getStringProperty("title_sl")
    title_sv = graph.getStringProperty("title_sv")
    tmpIDEdge = graph.getIntegerProperty("tmpIDEdge")
    tmpIDNode = graph.getIntegerProperty("tmpIDNode")
    trustworthiness = graph.getStringProperty("trustworthiness")
    type_ = graph.getStringProperty("type")

    typeResource = graph.getStringProperty("typeResource")

    type_search = graph.getStringProperty("type_search")
    union = graph.getStringProperty("union")
    unknowns = graph.getStringProperty("unknowns")
    upvote = graph.getStringProperty("upvote")
    uri = graph.getStringProperty("uri")
    url = graph.getStringProperty("url")
    url_cs = graph.getStringProperty("url_cs")
    url_da = graph.getStringProperty("url_da")
    url_de = graph.getStringProperty("url_de")
    url_el = graph.getStringProperty("url_el")
    url_en = graph.getStringProperty("url_en")
    url_es = graph.getStringProperty("url_es")
    url_fi = graph.getStringProperty("url_fi")
    url_fr = graph.getStringProperty("url_fr")
    url_it = graph.getStringProperty("url_it")
    url_lu = graph.getStringProperty("url_lu")
    url_mt = graph.getStringProperty("url_mt")
    url_nl = graph.getStringProperty("url_nl")
    url_no = graph.getStringProperty("url_no")
    url_pl = graph.getStringProperty("url_pl")
    url_pt = graph.getStringProperty("url_pt")
    url_ru = graph.getStringProperty("url_ru")
    url_sv = graph.getStringProperty("url_sv")
    username = graph.getStringProperty("username")
    viewBorderColor = graph.getColorProperty("viewBorderColor")
    viewBorderWidth = graph.getDoubleProperty("viewBorderWidth")
    viewColor = graph.getColorProperty("viewColor")
    viewFont = graph.getStringProperty("viewFont")
    viewFontAwesomeIcon = graph.getStringProperty("viewFontAwesomeIcon")
    viewFontSize = graph.getIntegerProperty("viewFontSize")
    viewLabel = graph.getStringProperty("viewLabel")
    viewLabelBorderColor = graph.getColorProperty("viewLabelBorderColor")
    viewLabelBorderWidth = graph.getDoubleProperty("viewLabelBorderWidth")
    viewLabelColor = graph.getColorProperty("viewLabelColor")
    viewLabelPosition = graph.getIntegerProperty("viewLabelPosition")
    viewLayout = graph.getLayoutProperty("viewLayout")
    viewMetric = graph.getDoubleProperty("viewMetric")
    viewRotation = graph.getDoubleProperty("viewRotation")
    viewSelection = graph.getBooleanProperty("viewSelection")
    viewShape = graph.getIntegerProperty("viewShape")
    viewSize = graph.getSizeProperty("viewSize")
    viewSrcAnchorShape = graph.getIntegerProperty("viewSrcAnchorShape")
    viewSrcAnchorSize = graph.getSizeProperty("viewSrcAnchorSize")
    viewTexture = graph.getStringProperty("viewTexture")
    viewTgtAnchorShape = graph.getIntegerProperty("viewTgtAnchorShape")
    viewTgtAnchorSize = graph.getSizeProperty("viewTgtAnchorSize")
    width = graph.getStringProperty("width")
    yago_annotated = graph.getStringProperty("yago_annotated")
    yaml = graph.getStringProperty("yaml")

    isCandidate = graph.getBooleanProperty("isCandidate")
    isChosen = graph.getBooleanProperty("isChosen")
    distanceToFocus = graph.getDoubleProperty("distanceToFocus")
    distanceMax = graph.getDoubleProperty("distanceMax")
    scoreDOI = graph.getDoubleProperty("scoreDOI")

    dicType = {}
    initialFocusNode = None
    listIsChosen = []
    candidateStack = []
    listNodesSubGraph = []

    # precomputed with an other script python
    degMax = 5794.0
    # precomputed with an other script python
    degPersonMax = 3401

    sizeMaxDOIGraph = 120
    # How to select the focus node
    chooseFocusWith = "selection"  # id, doi, selection
    # According to chooseFocusWith, the value permitting the selection of a new focus node
    idFocusNode = ""  # "f72838f2-9915-4ca1-8be7-e822ac0cc5a2" #4603 #"f72838f2-9915-4ca1-8be7-e822ac0cc5a2"

    # Are you ready ?!
    start = time.time()

    ##########Init##########
    # select the focus node
    print("Mode : " + chooseFocusWith.upper())
    for n in graph.getNodes():
        if str(n.id) in list(selection.values()):
            isChosen[n] = True
            listIsChosen.append(n)
            viewColor[n] = tlp.Color(20, 20, 255)
            viewSize[n] = tlp.Size(2, 2, 1)
        # reset isCandidate
        isCandidate[n] = False

    print("Nodes currently chosen : " + str(listIsChosen) + ".")

    # determinate dicType
    fillDicCoverType(listIsChosen, dicType, graph.getNodes(), typeResource)

    # compute distance between focus node and others node in the graph
    if (listIsChosen):
        preComputeDistanceDOI(graph, listIsChosen, distanceToFocus, isChosen, viewLayout)
    else:
        print("you need to select one or several nodes")

    ##########Compute DOI##########
    for n in graph.getNodes():
        makeDOI(n, 0.8, degMax, dicType, metric, typeResource, distanceToFocus, scoreDOI, type_search,
                labelsNodeTlp, degree, degPersonMax)

    ##########New Subgraph##########
    # Creation of the new subgraph
    for n in listIsChosen:
        listNodesSubGraph.append(n)
        viewSelection[n] = True
        isCandidate[n] = True
        for nn in graph.getInOutNodes(n):
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
        for nn in graph.getInOutNodes(nodeWithDOImax):
            if (isCandidate[nn] == False):
                candidateStack.append(nn)
                isCandidate[nn] = True
        listNodesSubGraph.append(nodeWithDOImax)
        candidateStack.remove(nodeWithDOImax)
        cmpt += 1
        print("--- " + str(int((cmpt / sizeMaxDOIGraph) * 100)) + "% ---")

    context_subgraph = tlp.Graph.inducedSubGraph(graph, listNodesSubGraph)

    # Done
    end = time.time()
    print("Time(s) : " + str(end - start))
    params = tlp.getDefaultPluginParameters('TLPB Export', graph)
    tlp.exportGraph('TLPB Export', context_subgraph, "%s%s.tlpb" % (config['exporter']['tlp_path'], private_gid), params)
