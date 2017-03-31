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

    def __init__(self):
        self.startConnection()
        self.nodeMapper = NodeMapper()
        self.parser = NLParser()
        print "Controller initialized."
        pass

    def startConnection(self):
        """ Connect to MySQL database """
        try:
            self.conn = psycopg2.connect("dbname='dblp' user='postgres' host='localhost' password='Codechef'")
        except:
            print "I am unable to connect to the database"
        print "connected to database..."
        self.schema = SchemaGraph(self.conn)

    def startMappingNodes(self):
        if self.mappingNodes:
            return
        self.mappingNodes = True
        #
        # iter = parseTree.iterator();
        # if (!iter.hasNext()) {
        #     finishNodesMapping();
        #     return;
        # }
        # node = iter.next();
        # List < NodeInfo > choices = nodeMapper.getNodeInfoChoices(node, schema);
        # if (choices.size() == 1) {chooseNode(choices.get(0));}
        # else {setChoicesOnView(choices);}

    def processNaturalLanguage(self, input):
        if self.processing:
            print "\nCurrently processing a sentence!\n"
        else:
            self.processing = True
            self.parseTree = ParseTree(input, parser=self.parser)
            self.startMappingNodes()


    def closeConnection(self):
        try:
            conn.close()
        except Error as e:
            print(e)
        print("Database connection closed")