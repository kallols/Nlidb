

class SQLQuery:

    blocks = list()
    map = dict()

    def __init__(self):
        self.map = dict()
        self.map["SELECT"] = list()
        self.map["FROM"] = list()
        self.map["WHERE"] = list()
        self.blocks = list()

    def get(self):
        return SQLQuery.toString()

    def addBlock(self, query):
        self.blocks.append(query)
        SQLQuery.add(self, "FROM", "BLOCK%d"%len(self.blocks))

    def add(self, key, value):
        temp = self.map[key]
        temp.append(value)
        self.map[key] = temp

    def toSBLine(self, SELECT):
        sb = []
        for val in SELECT:
            if len(sb) == 0:
                sb.append(val)
            else:
                sb.append(", ")
                sb.append(val)
            return ''.join(sb)

    def toSBLineCondition(self, WHERE):
        sb = []
        for val in WHERE:
            if len(sb) == 0:
                sb.append(val)
            else:
                sb.append(" AND ")
                sb.append(val)
        return ''.join(sb)

    def toString(self):
        if len(self.map["SELECT"]) == 0 or len(self.map["WHERE"]) == 0:
            return "Illegal Query"

        sb = list()
        for i in range(0, len(self.blocks), 1):
            sb.append("BLOCK%s:\n"%(i+1))
            sb.append("%s\n"%self.blocks[i])
            ''.join(sb)

        sb.append("SELECT ")
        sb.append("%s\n"%SQLQuery.toSBLine(self.map["SELECT"]))
        sb.append("FROM ")
        sb.append("%s\n" % SQLQuery.toSBLine(self.map["FROM"]))

        if len(self.map["WHERE"]) != 0:
            sb.append("WHERE ")
            sb.append("%s\n"%SQLQuery.toSBLineCondition(self.map["WHERE"]))

        sb.append(";\n")
        return ''.join(sb)


