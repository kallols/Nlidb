from ParseTree import ParseTree
from Node import Node
from NodeInfo import NodeInfo
from TreeAdjustor import TreeAdjustor



class TreeAdjustorTest:


    def __init__(self):
        return

    def getAdjustedTreesTest(self):



        T = ParseTree()
        nodes = [Node(index=-1, word="DEFAULT", posTag="DEFAULT") for i in range(0, 8)]

        nodes[0] = Node(index=0, word="ROOT", posTag="--")
        nodes[0].info = NodeInfo(type="ROOT", value="ROOT")
        nodes[1] = Node(index=1, word="return", posTag="--")
        nodes[1].info = NodeInfo(type="SN", value="SELECT")
        nodes[2] = Node(index=2, word="conference", posTag="--")
        nodes[2].info = NodeInfo(type="NN", value="Author")
        nodes[3] = Node(index=3, word="area", posTag="--")
        nodes[3].info = NodeInfo(type="NN", value="Title")
        nodes[4] = Node(index=4, word="papers", posTag="--")
        nodes[4].info = NodeInfo(type="NN", value="Author")
        nodes[5] = Node(index=5, word="citations", posTag="--")
        nodes[5].info = NodeInfo(type="NN", value="Journal")
        nodes[6] = Node(index=6, word="most", posTag="--")
        nodes[6].info = NodeInfo(type="FN", value=">")
        nodes[7] = Node(index=7, word="total", posTag="--")
        nodes[7].info = NodeInfo(type="FN", value="Year")

        T.root = nodes[0];
        nodes[0].children.append(nodes[1]);
        nodes[1].parent = nodes[0];
        nodes[1].children.append(nodes[2]);
        nodes[2].parent = nodes[1];
        nodes[2].children.append(nodes[3]);
        nodes[3].parent = nodes[2];
        nodes[2].children.append(nodes[4]);
        nodes[4].parent = nodes[2];
        nodes[4].children.append(nodes[5]);
        nodes[5].parent = nodes[4];
        nodes[5].children.append(nodes[6]);
        nodes[6].parent = nodes[5];
        nodes[5].children.append(nodes[7]);
        nodes[7].parent = nodes[5];

        print "===========test for Running getAdjustedTrees() in TreeAdjustor==========="
        print "The original tree:"
        print T.toString()
        print "Number of possible trees for choice:"

        obj = TreeAdjustor()
        result = TreeAdjustor.getAdjustedTrees(T)
        print len(result)
        sorted(result,cmp=cmpp)
        print "The three trees with highest scores look like:"
        for i in range(0,5):
           print result[i]

def cmpp(a,b):
    if a.getScore() < b.getScore():
        return 1
    elif a.getScore() > b.getScore():
        return -1
    else:
        return 0

obj = TreeAdjustorTest()
obj.getAdjustedTreesTest()



