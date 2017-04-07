from Queue import PriorityQueue
from SyntacticEvaluator import SyntacticEvaluator

class TreeAdjustor:
    MAX_EDIT = 5

    def __init__(self):
        pass
    
    @staticmethod
    def find(tree, targetNode):
        if tree is None:
            raise Exception
        for node in tree:
            if node.equals(targetNode):
                return node
        return None

    @staticmethod
    def swap( parent, child):
        childInfo = child.info
        childWord = child.word
        childPosTag = child.posTag
        child.info = parent.info
        child.word = parent.word
        child.posTag = parent.posTag
        parent.info = childInfo
        parent.word = childWord
        parent.posTag = childPosTag

    @staticmethod
    def makeSibling( target, child):
        children = target.getChildren()
        target.children = list()
        for anyChild in children:
            if not (anyChild == child):
                target.getChildren().append(anyChild)

        target.parent.children.append(child)
        child.parent = target.parent

    @staticmethod
    def makeChild( target, sibling):
        siblings = target.parent.children
        target.parent.children = list()
        for anySibling in siblings:
            if not (anySibling == sibling):
                target.parent.children.append(anySibling)

        target.children.append(sibling)
        sibling.parent = target

    @staticmethod
    def adjust(tree, target=None):
        from ParseTree import ParseTree
        if target is not None:
            adjusted = set()
            if target.parent is None:
                return adjusted

            for child in target.getChildren():
                tempTree = ParseTree(node=tree.root)
                # print "\n\nTempTree:"
                TreeAdjustor.swap(TreeAdjustor.find(tempTree, target), TreeAdjustor.find(tempTree, child))
                adjusted.add(tempTree)
                print "adjusted Size: %d" % (len(adjusted))
                print "%s:%d" % (tempTree.getSentence(), tempTree.getScore())
            for child in target.getChildren():
                tempTree = ParseTree(node=tree.root)
                TreeAdjustor.makeSibling(TreeAdjustor.find(tempTree, target), TreeAdjustor.find(tempTree, child))
                adjusted.add(tempTree)
                print "adjusted Size: %d" % (len(adjusted))
                print "%s:%d"%(tempTree.getSentence(), tempTree.getScore())

            for sibling in target.parent.getChildren():
                if (sibling == target):
                    continue
                tempTree = ParseTree(node=tree.root)
                TreeAdjustor.makeChild(TreeAdjustor.find(tempTree, target), TreeAdjustor.find(tempTree, sibling))
                adjusted.add(tempTree);

                print "adjusted Size: %d" % (len(adjusted))
                print "%s:%d" % (tempTree.getSentence(), tempTree.getScore())

            if (len(target.getChildren()) >= 2):
                children = target.getChildren()
                for i in range(1, len(children)):
                    tempTree = ParseTree(node=tree.root)
                    TreeAdjustor.swap(TreeAdjustor.find(tempTree, children[0]),
                              TreeAdjustor.find(tempTree, children[i]));
                    adjusted.add(tempTree);
                    print "adjusted Size: %d" % (len(adjusted))
                    print "%s:%d"%(tempTree.getSentence(), tempTree.getScore())
            # print "adjusted Size: %d" % (len(adjusted))
            # print "Adjusted Trees: "
            # for tr in adjusted:
            #      print tr.getSentence()

            print "------------------------------------------"
            print "------------------------------------------"
            return adjusted
        elif target is None:
            treeList = set()
            for node in tree:
                print "Node: "
                print node

                temp = TreeAdjustor.adjust(tree, node)
                for t in temp:
                    treeList.add(t)
            print "treeList Size: %d"%(len(treeList))
            return list(treeList)

    @staticmethod
    def getAdjustedTrees( tree):
        results = list()
        ctr = 10
        queue = PriorityQueue()
        #TODO :check if p queue is working properly
        H = dict()
        queue.put(tree)
        results.append(tree);
        H[tree.__hash__()] = tree
        tree.setEdit(0);

        #TODO addON is wrong
        treeWithON = tree.addON()

        # print "aaaa"
        # print treeWithON


        queue.put(treeWithON);
        results.append(treeWithON);
        H[treeWithON.__hash__()]  = treeWithON
        treeWithON.setEdit(0)


        while not queue.empty() and ctr>0:
            debug_size = queue._qsize()
            print "queue size = %d" %(debug_size)
            print "Queue tree: "
            tempList =[]

            for i in range(0, queue._qsize()):
                tr = queue.get()
                tempList.append(tr)
                print tr.getSentence()

            for tr in tempList:
                queue.put(tr)

            # if ctr == 10:
            #     oriTree = queue.get()
            #     # secTree = queue.get()
            #     queue.put(oriTree)
            #     # oriTree =secTree
            # else:
            oriTree = queue.get()
            ctr = ctr - 1
            if (oriTree.getEdit() >= TreeAdjustor.MAX_EDIT):
                continue

            treeList = TreeAdjustor.adjust(oriTree)

            numInvalidNodes = SyntacticEvaluator().numberOfInvalidNodes(oriTree)

            for i in range(0,len(treeList)):
                currentTree = treeList[i]
                hashValue = currentTree.__hash__()
                if not(H.has_key(hashValue) ):
                    H[hashValue] =  currentTree
                    currentTree.setEdit(oriTree.getEdit() + 1);
                    if SyntacticEvaluator().numberOfInvalidNodes(currentTree) <= numInvalidNodes:
                        queue.put(currentTree);
                        results.append(currentTree);


        return results





