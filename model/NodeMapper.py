from model.NodeInfo import NodeInfo
from model.WordSimilarity import WordSimilarity


class NodeMapper:

    map = None
    wordSimilarity = None

    def __init__(self):
        self.wordSimilarity = WordSimilarity()
        map = dict()

        map["return"] = NodeInfo("SN", "SELECT") # Select Node

        map["equals"]= NodeInfo("ON", "=") # Operator Node
        map["less"] = NodeInfo("ON", "<")
        map["greater"] = NodeInfo("ON", ">")
        map["not"] = NodeInfo("ON", "!=")
        map["before"] = NodeInfo("ON", "<")
        map["after"] = NodeInfo("ON", ">")
        map["more"] = NodeInfo("ON", ">")
        map["older"] = NodeInfo("ON", ">")
        map["newer"] = NodeInfo("ON", "<")

        map["fn"] = NodeInfo("FN", "AVG") # Function Node
        map["average"] = NodeInfo("FN", "AVG")
        map["most"] = NodeInfo("FN", "MAX")
        map["total"] = NodeInfo("FN", "SUM")
        map["number"] = NodeInfo("FN", "COUNT")

        map["all"] = NodeInfo("QN", "ALL") # Quantifier Node
        map["any"] = NodeInfo("QN", "ANY")
        map["each"] = NodeInfo("QN", "EACH")

        map["and"] = NodeInfo("LN", "AND") # Logic Node
        map["or"] = NodeInfo("LN", "OR")

    def getNodeInfoChoices(self , node, schema):
        result = list() #final output

        if node.getWord() == "ROOT":
            result.append(NodeInfo("ROOT", "ROOT"))
            return result

        valueNodes = list()
        word = node.getWord().lower()

        if word in NodeMapper.map:
            result.append( map[word] )
            return result

        for tableName in schema.getTableNames():
            result.append(NodeInfo("NN", tableName, WordSimilarity.getSimilarity(word, tableName)))

            for colName in schema.getColumns(tableName):
                result.append(NodeInfo("NN", tableName + "." + colName, WordSimilarity.getSimilarity(word, colName)))

                for value in schema.getValues(tableName, colName):
                    if (word is None) or (value is None):
                        print "Comparing %s and %s"%(word, value)
                        print "In table %s column %s"%(tableName, colName)

                    valueNodes.append(NodeInfo("VN", tableName+"."+colName, WordSimilarity.getSimilarity(word, value)))

        result.append(valueNodes) #doubt : result.addAll() vs result.append()
        result.append(NodeInfo("UNKNOWN", "meaningless", 1.0))
        return sorted(result, cmp = NodeInfo.reverseScoreComparator())