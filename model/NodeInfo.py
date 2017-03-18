class NodeInfo:

    type = None
    value = None
    score = 1.0

    def __init__(self,type,value,score=1.0):
        NodeInfo.type = type
        NodeInfo.value = value
        NodeInfo.score = score
        pass

    def getType(self):
        return self.type

    def getScore(self):
        return self.score

    def getValue(self):
        return self.value

    def reverseScoreComparator(self,a,b):
        if a.score < b.score:
            return 1
        elif a.score > b.score:
            return -1
        else:
            return 0

    def H






