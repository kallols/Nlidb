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

    def hashCode(self):
        prime = 31
        result = 1
        result = prime * result + (0 if self.type is None else self.type.hashCode())
        result = prime * result + (0 if self.value is None else self.value.hashCode())
        return result

    def __eq__(self, other):
        if self == other:
            return True
        if other is None:
            return False
        if type(self) != type(other):
            return False

        if self.type is None:
            if other.type is not None:
                return  False
        elif self.type != other.type:
            return False
        if self.value is None:
            if other.value is not None:
                return False
        elif self.value != other.value:
            return False
        return True

    def ExactSameSchema(self, other):
        if self.type is None or \
            other.getType() is None or \
            self.value is None or \
            other.getValue() is None:
            return False

        if self.type == other.getType()  and self.value == other.getValue():
            return True

        return False

    def sameSchema(self, other):
        if self.type is None or other.getType() is None or self.value is None or other.getValue() is None:
            return False

        try:
            indexOfDot_Other = other.getValue().index('.')
        except ValueError:
            indexOfDot_Other = -1

        try :
            indexOfDot = self.value.index('.')
        except ValueError:
            indexOfDot = -1

        if indexOfDot_Other == -1:
            indexOfDot_Other = other.getValue().length()

        if indexOfDot == -1 :
            indexOfDot = self.value.length()

        if other.getValue()[0, indexOfDot_Other - 1] == self.value[0, indexOfDot - 1]:
            return True

        return False






