from model.NodeInfo import NodeInfo
from model.WordSimilarity import WordSimilarity
from operator import attrgetter


class NodeMapper:

    map = None
    wordSimilarity = None

    def __init__(self):
        self.wordSimilarity = WordSimilarity()
        self.map = dict()

        self.map["return"] = NodeInfo("SN", "SELECT") # Select Node

        self.map["equals"]= NodeInfo("ON", "=") # Operator Node
        self.map["less"] = NodeInfo("ON", "<")
        self.map["greater"] = NodeInfo("ON", ">")
        self.map["not"] = NodeInfo("ON", "!=")
        self.map["before"] = NodeInfo("ON", "<")
        self.map["after"] = NodeInfo("ON", ">")
        self.map["more"] = NodeInfo("ON", ">")
        self.map["older"] = NodeInfo("ON", ">")
        self.map["newer"] = NodeInfo("ON", "<")

        self.map["fn"] = NodeInfo("FN", "AVG") # Function Node
        self.map["average"] = NodeInfo("FN", "AVG")
        self.map["most"] = NodeInfo("FN", "MAX")
        self.map["total"] = NodeInfo("FN", "SUM")
        self.map["number"] = NodeInfo("FN", "COUNT")

        self.map["all"] = NodeInfo("QN", "ALL") # Quantifier Node
        self.map["any"] = NodeInfo("QN", "ANY")
        self.map["each"] = NodeInfo("QN", "EACH")

        self.map["and"] = NodeInfo("LN", "AND") # Logic Node
        self.map["or"] = NodeInfo("LN", "OR")

    def reverseScoreComparator(self, a, b):
        if a.score < b.score:
            return 1
        elif a.score > b.score:
            return -1
        else:
            return 0

    def getNodeInfoChoices(self , node, schema):
        result = list() #final output

        if node.getWord() == "ROOT":
            result.append(NodeInfo("ROOT", "ROOT"))
            return result

        valueNodes = list()
        word = node.getWord().lower()

        if word in self.map:
            result.append( self.map[word] )
            return result

        for tableName in schema.getTableNames():
            result.append(NodeInfo("NN", tableName, self.wordSimilarity.getSimilarity(word, tableName)))

            for colName in schema.getColumns(tableName):
                result.append(NodeInfo("NN", tableName + "." + colName, self.wordSimilarity.getSimilarity(word, colName)))

                for value in schema.getValues(tableName, colName):
                    if (word is None) or (value is None):
                        print "Comparing %s and %s"%(word, value)
                        print "In table %s column %s"%(tableName, colName)

                    valueNodes.append(NodeInfo("VN", tableName+"."+colName, self.wordSimilarity.getSimilarity(word, value)))

        result.extend(valueNodes)
        result.append(NodeInfo("UNKNOWN", "meaningless", 1.0))
        list1 = sorted(result, cmp = self.reverseScoreComparator, reverse=True)
        return sorted(result, cmp = self.reverseScoreComparator, reverse=True)