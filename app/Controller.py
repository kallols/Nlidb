import psycopg2
from model.SchemaGraph import SchemaGraph
from model.NodeMapper import NodeMapper
from model.ParseTree import ParseTree
from model.NLParser import NLParser


class Controller:
    conn = None
    nodeMapper = None
    parser = None
    schema = None
    processing = False
    parseTree = None
    mappingNodes = False
    node = None
    view = None
    selectingTree = False
    treeChoices = []
    query = ""
    iter = None

    def __init__(self, userView):
        self.startConnection()
        self.nodeMapper = NodeMapper()
        self.parser = NLParser()
        self.view = userView
        print "Controller initialized."

    def startConnection(self):
        """ Connect to MySQL database """
        try:
            self.conn = psycopg2.connect("dbname='dblp' user='postgres' host='localhost' password='Codechef'")
        except:
            print "I am unable to connect to the database"
        print "connected to database..."
        self.schema = SchemaGraph(self.conn)

    def closeConnection(self):
        try:
            self.conn.close()
        except:
            pass


        print("Database connection closed")

    def setChoicesOnView(self, choices): #TODO
        sb = []
        sb.append("Mapping nodes: \n")
        sb.append(self.parseTree.getSentence())
        self.view.setDisplay(''.join(sb))
        sb = []
        sb.append("Currently on: ")
        sb.append(self.node.getWord())
        self.view.appendDisplay( ''.join(sb))
        #view.setChoices(FXCollections.observableArrayList(choices)); TODO doubt here
        self.view.setChoices(choices)

    def finishNodesMapping(self):
        print "in Finish Node Mapping...\n"
#        self.view.setDisplay("Nodes mapped.\n" + self.parseTree.getSentence())
        self.mappingNodes = False
        self.view.removeChoiceBoxButton()
        self.processAfterNodesMapping()
        print "Finish Node Mapping Done!...\n"

    def startMappingNodes(self): #TODO
        print "in Start Mapping Nodes...\n"
        self.view.showNodesChoice()

        if self.mappingNodes:
            return
        self.mappingNodes = True

        self.iter = self.parseTree.iterator(self.parseTree.root)
        if not (self.iter.hasNext()) :
            self.finishNodesMapping()
            return

        self.node = self.iter.getNext()
        choices = self.nodeMapper.getNodeInfoChoices(self.node, self.schema)
        if len(choices) == 1:
            self.chooseNode(choices[0])
        else:
            print "Choices ::"
            print choices
            self.setChoicesOnView(choices)
        print "Start Mapping Nodes Done!...\n"

    def chooseNode(self, info):
        print "in Choose Node...\n"
        if not self.mappingNodes:
            return

        self.node.setInfo(info)

        if not(self.iter.hasNext()) :
            self.finishNodesMapping();
            return

        self.node = self.iter.getNext()
        choices = self.nodeMapper.getNodeInfoChoices(self.node, self.schema)
        if len(choices) == 1:
            self.chooseNode(choices[0])
        else:
            self.setChoicesOnView(choices)
        print "Choose Node Done!...\n"

    def startTreeSelection(self):
        if self.selectingTree:
            return
        self.view.showTreesChoice()
        self.selectingTree = True
        self.treeChoices = self.parseTree.getAdjustedTrees()

    def showTree(self, index):
        self.view.setDisplay(self.treeChoices[0])

    def chooseTree(self, index):
        self.parseTree = self.treeChoices[index]
        self.finishTreeSelection()

    def finishTreeSelection(self):
        self.selectingTree = False
        self.view.removeTreesChoices()
        self.processAfterTreeSelection()

    def processAfterTreeSelection(self):
        print "The tree before implicit nodes insertion: %s\n"%self.parseTree
        self.parseTree.insertImplicitNodes()
        print "Going to do translation for tree: %s\n"%self.parseTree
        self.query = self.parseTree.translateToSQL(self.schema)
        self.view.setDisplay(self.query.toString())
        self.processing = False

    def processAfterNodesMapping(self):
        print "Going to remove meaningless nodes for tree: "
        print self.parseTree
        for n in self.parseTree.nodes:
            print n.getWord()
            print [word.getWord() for word in n.getChildren()]
        self.parseTree.removeMeaningLessNodes()
        print "###"
        self.parseTree.mergeLNQN()
        print "After mergeLNQn"
        self.startTreeSelection()
        print "After startTreeSelection..."

    def processNaturalLanguage(self, input):
        if self.processing:
            print "\nCurrently processing a sentence!\n"
        else:
            self.processing = True
            self.parseTree = ParseTree(input, parser=self.parser)
            self.startMappingNodes()

