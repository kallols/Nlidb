import copy


class Node:

    outside = False
    index = 0
    info = None
    word = None
    posTag = None
    parent = None
    children = list()
    isInvalid = False

    def __init__(self, word, posTag, index = 0, info = None):
        self.index = index
        self.word = word
        self.posTag = posTag
        self.info = info

    def cloneNode(self, node):
        if node is None:
            return None

        copy = Node(node.index, node.word, node.posTag, node.info)

        for child in node.children:
            copyChild = Node.cloneNode(self, child)
            copyChild.parent = copy
            copy.children.append(copyChild)

        return copy

    def clone(self):
        return copy.deepcopy(self)

    def getInfo(self):
        return Node.info

    def setInfo(self, info):
        Node.info = info

    def getWord(self):
        return Node.word

    def setWord(self, word):
        Node.word = word

    def getPosTag(self):
        return Node.posTag

    def getChildren(self):
        return Node.children

    def setChild(self, child):
        Node.children.append(child)

    def getParent(self):
        return Node.parent

    def setParent(self, parent):
        Node.parent = parent

    def getOutside(self):
        return Node.outside

    def setOutside(self, outside):
        Node.outside = outside

    def removeChild(self, child):
        Node.children = [childeNode for childeNode in Node.children if childeNode != child]
        return

    def printNodeArray(self):
        nodes = Node.genNodesArray(self)
        for node in nodes:
            print ("type: " + node.getInfo().getType() + " value: " + nodes.getInfo().getValue())

    def genNodesArray(self):
        nodesList = list()
        stack = list()
        stack.insert(0, self)

        while len(stack) != 0:
            curr = stack.pop(-len(stack))
            nodesList.append(curr)
            currChildren = curr.getChildren()
            for i in range(len(currChildren)-1, -1, -1):
                stack.insert(0, currChildren[i])

        return nodesList

    def hashCode(self):
        prime = 31
        result = 17

        result = prime * result + Node.index
        result = prime * result + (0 if (Node.posTag is None) else Node.posTag.hashCode())
        result = prime * result + (0 if (Node.word is None) else Node.word.hashCode())
        result = prime * result + (0 if (Node.info is None) else Node.info.hashCode())

        if Node.children is not None:
            for child in Node.children:
                result = prime * result + child.hashCode()

        return result

    def equals(self, obj):
        if self == obj:
            return True
        if obj is None:
            return False
        if not (self.__class__ == obj.__class__):
            return False

        other = obj
        if not Node.index == other.index:
            return False

        if not Node.word == other.word:
            return False

        if not Node.posTag == other.posTag:
            return False

        if not Node.info == other.info:
            if (Node.info is None) or (other.info is None):
                return False
            if not Node.info == other.info:
                return False

        if Node.children != other.children:
            if (Node.children is None) or (other.children is None):
                return False
            if len(Node.children) != len(other.children):
                return False
            for i in range (0, len(Node.children)):
                if not Node.children[i] == other.children[i]:
                    return False
        return True

    def toString(self):
        s = "( %s ) %s"%(Node.index,Node.word)
        if not Node.info is None:
            s = s + "("+Node.info.getType()+":"+Node.info.getValue()+")"
        return s
