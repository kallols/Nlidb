
class SQLTranslator:
    query =None
    schema = None
    blockCounter = 1

    def __init__(self, root, schema, block):
        if not block:
            self.schema = schema
            self.query = SQLQuery()

            self.translateSClause(root.getChildren()[0])
            if (root.getChildren().size() >= 2):
                self.translateComplexCondition(root.getChildren()[1])

            if schema is not None:
                self.addJoinPath()
            else:
                self.schema = schema
                query = SQLQuery()
                self.translateGNP(root)

    def getResult(self):
        return self.query

    def isNumber(self, str):
        length = len(str)
        if (length == 0):
            return False
        i =0
        if (str.charAt(0) == '-'):
            if (length == 1):
                return False
            i =1
        for x in range(i,length):
            c = str[x]
            if (c < '0' or c > '9' and c != '.'):
                return False
        return  True

    def translateCondition(self, node):
        attribute = "ATTRIBUTE"
        compareSymbol = "="
        value = "VALUE"
        if (node.getInfo().getType().equals("VN")):
            attribute = node.getInfo().getValue();
            value = node.getWord();
        elif (node.getInfo().getType().equals("ON")):
            compareSymbol = node.getInfo().getValue();
            VN = node.getChildren().get(0);
            attribute = VN.getInfo().getValue();
            value = VN.getWord();
        if not(self.isNumber(value)):
            value = "\"" + value + "\""

        self.query.add("WHERE", attribute + " " + compareSymbol + " " + value)
        self.query.add("FROM", attribute.split("\\.")[0]);

    def translateNN(self, node,valueFN=None):
        if valueFN is None:
            self.translateNN(node, valueFN="")
        else:
            if not(node.getInfo().getType().equals("NN")):
                return
            if not(valueFN.equals("")):
                self.query.add("SELECT", valueFN + "(" + node.getInfo().getValue() + ")")
            else:
                self.query.add("SELECT", node.getInfo().getValue())
            self.query.add("FROM", node.getInfo().getValue().split("\\.")[0])

    def translateNP(self, node, valueFN=None):
        if valueFN is None:
            self.translateNP(node, valueFN="")
        else:
            self.translateNN(node, valueFN)
            for child in node.getChildren():
                if (child.getInfo().getType().equals("NN")):
                    self.translateNN(child)
                elif (child.getInfo().getType().equals("ON") or child.getInfo().getType().equals("VN")):
                    self.translateCondition(child)

    def translateGNP(self, node):
        if (node.getInfo().getType().equals("FN")):
            if (node.getChildren().isEmpty()):
                return
            self.translateNP(node.getChildren().get(0), node.getInfo().getValue())
        elif (node.getInfo().getType().equals("NN")):
            self.translateNP(node)

    def translateComplexCondition(self, node):
        if not(node.getInfo().getType().equals("ON")):
            return
        if (node.getChildren().size() != 2):
            return
        transLeft = SQLTranslator(node.getChildren().get(0), self.schema, block=True)
        transRight = SQLTranslator(node.getChildren().get(1), self.schema, block=True)
        self.query.addBlock(transLeft.getResult());
        self.query.addBlock(transRight.getResult());
        self.query.add("WHERE","BLOCK" + (self.blockCounter) + " " + node.getInfo().getValue() + " " + "BLOCK" + (self.blockCounter+1))
        self.blockCounter+=2

    def translateSClause(self, node):
        if not(node.getInfo().getType().equals("SN")):
            return
        self.translateGNP(node.getChildren().get(0))


    def addJoinKeys(self, table1, table2):
        joinKeys = self.schema.getJoinKeys(table1, table2)
        for joinKey in joinKeys:
            self.query.add("WHERE", table1 + "." + joinKey + " = " + table2 + "." + joinKey)

    def addJoinPath(self ,joinPath = None):
        if joinPath is None:
            fromTables = list(self.query.getCollection("FROM"))
            if (fromTables.size() <= 1):
                return
            for i in range(0, len(fromTables)-1):
                for j in range(i+1, len(fromTables)):
                    joinPath = self.schema.getJoinPath(fromTables.get(i), fromTables.get(j))
                    self.addJoinPath(joinPath)
        else:
            for i in range(0,len(joinPath)-1):
                self.addJoinKeys(joinPath.get(i), joinPath.get(i+1))





