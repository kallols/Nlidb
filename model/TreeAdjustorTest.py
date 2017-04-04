class TreeAdjustorTest:
    def numberOfInvalidNodesTest(self):
        T = ParseTree()
        nodes = [Node(index=-1, word="DEFAULT", posTag="DEFAULT") for i in range(0,9)]

        nodes[0] = Node(index=0, word="ROOT", posTag="--")
        nodes[0].info = NodeInfo(type="ROOT",value="ROOT")
        nodes[1] = Node(index=1, word="return", posTag="--")
        nodes[1].info = NodeInfo(type="SN",value="ROOT")
        nodes[2] = Node(index=2, word="author", posTag="--")
        nodes[2].info = NodeInfo(type="NN",value="ROOT")
        nodes[3] = Node(index=3, word="paper", posTag="--")
        nodes[3].info = NodeInfo(type="NN",value="ROOT")
        nodes[4] = Node(index=4, word="more", posTag="--")
        nodes[4].info = NodeInfo(type="ON",value="ROOT")
        nodes[5] = Node(index=5, word="Bob", posTag="--")
        nodes[5].info = NodeInfo(type="VN",value="ROOT")
        nodes[6] = Node(index=6, word="VLDB", posTag="--")
        nodes[6].info = NodeInfo(type="NN",value="ROOT")
        nodes[7] = Node(index=7, word="after", posTag="--")
        nodes[7].info = NodeInfo(type="ON",value="ROOT")
        nodes[8] = Node(index=8, word="2000", posTag="--")
        nodes[8].info = NodeInfo(type="VN",value="ROOT")

        T.root = nodes[0];
        nodes[0].children.append(nodes[1]);
        nodes[1].parent = nodes[0];
        nodes[1].children.append(nodes[2]);
        nodes[2].parent = nodes[1];
        nodes[2].children.append(nodes[3]);
        nodes[3].parent = nodes[2];
        nodes[2].children.append(nodes[5]);
        nodes[5].parent = nodes[2];
        nodes[2].children.append(nodes[7]);
        nodes[7].parent = nodes[2];
        nodes[3].children.append(nodes[4]);
        nodes[4].parent = nodes[3];
        nodes[5].children.append(nodes[6]);
        nodes[6].parent = nodes[5];
        nodes[7].children.append(nodes[8]);
        nodes[8].parent = nodes[7];

        print "===========test for Running SyntacticEvaluator.numberOfInvalidNodes==========="
        print "Number of Invalid nodes: "+SyntacticEvaluator.numberOfInvalidNodes(T)
        print "Invalid nodes: "

        for i in range(1,len(nodes)):
            if nodes[i].isInvalid:
                print nodes[i]

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
        print T
        print "Number of possible trees for choice:"
        result = TreeAdjustor.getAdjustedTrees(T)
        print len(result)
        sorted(result,cmp=)
        print "The three trees with highest scores look like:"
        for i in range(0,5):
            print result[i]


obj = TreeAdjustorTest()
obj.getAdjustedTreesTest()



