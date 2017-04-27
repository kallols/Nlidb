from Queue import PriorityQueue
from SyntacticEvaluator import SyntacticEvaluator
from time import gmtime, strftime
from datetime import datetime

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
                # print "adjusted Size: %d" % (len(adjusted))
                # print "add adj %s:%d %d" % (tempTree.getSentence(), tempTree.getScore(), tempTree.__hash__())
                tempTree.time = str(datetime.now())

            for child in target.getChildren():
                tempTree = ParseTree(node=tree.root)
                TreeAdjustor.makeSibling(TreeAdjustor.find(tempTree, target), TreeAdjustor.find(tempTree, child))
                adjusted.add(tempTree)
                # print "adjusted Size: %d" % (len(adjusted))
                # print "add adj %s:%d %d" % (tempTree.getSentence(), tempTree.getScore(), tempTree.__hash__())
                tempTree.time =str(datetime.now())

            for sibling in target.parent.getChildren():
                if (sibling == target):
                    continue
                tempTree = ParseTree(node=tree.root)
                TreeAdjustor.makeChild(TreeAdjustor.find(tempTree, target), TreeAdjustor.find(tempTree, sibling))
                adjusted.add(tempTree);
                # print "adjusted Size: %d" % (len(adjusted))
                # print "add adj %s:%d %d" % (tempTree.getSentence(), tempTree.getScore(),tempTree.__hash__())
                tempTree.time = str(datetime.now())

            if (len(target.getChildren()) >= 2):
                children = target.getChildren()
                for i in range(1, len(children)):
                    tempTree = ParseTree(node=tree.root)
                    TreeAdjustor.swap(TreeAdjustor.find(tempTree, children[0]),
                              TreeAdjustor.find(tempTree, children[i]));
                    # print "add adj %s:%d %d" % (tempTree.getSentence(), tempTree.getScore(), tempTree.__hash__())
                    adjusted.add(tempTree);
                    tempTree.time = str(datetime.now())

            # print "adjusted Size: %d" % (len(adjusted))

            # for t in adjusted:
            #     print "adjusted tree : %s %d %s %d"%(t.getSentence(), t.getScore(), t.time, t.__hash__())
            # #return adjusted
            # for i in range(0, len(m)):
            #     for j in range(i+1, len(m)):
            #         if(m[i].time > m[j].time):
            #             temp = m[i]
            #             # m[i] =m[j]
            #             # m[j] = temp

            # for t in m:
            #     print "adjusted tree : %s %d %s"%(t.getSentence(), t.getScore(), t.time)

            # return adjusted
            m = list(adjusted)
            return m
        elif target is None:
            treeList = set()
            # print ("adjusting Tree: %s " % tree.getSentence())
            for node in tree:
                # print "Node: "
                # print node
                # print ("Node: %s " % node.getWord())
                temp = TreeAdjustor.adjust(tree, node)
                for t in temp:
                    # print "\n\n"
                    # print "Adding to List %s:%d (%d)" % (t.getSentence(), t.getScore(), t.__hash__())
                    treeList.add(t)
                    # t.time = str(datetime.now())
                    #
                    # for tr in treeList:
                    #     print "Tree List %s:%d (%d)" % (tr.getSentence(), tr.getScore(), tr.__hash__())
                # print "treeList Size: %d" % (len(treeList))
                m =list(treeList)
                # l =sorted(m, cmp =TreeAdjustor.timeStampCompare)
                for i in range(0, len(m)):
                    for j in range(i+1, len(m)):
                        if(m[i].time > m[j].time):
                            temp = m[i]
                            m[i] =m[j]
                            m[j] = temp
                # for t in m:
                #     # t.time =None
                #         print "Tree List %s:%d (%s) %d" % (t.getSentence(), t.getScore(), t.time, t.__hash__())

            return m

    @staticmethod
    def timeStampCompare(tree1, tree2):
        return tree1.time < tree2.time

    @staticmethod
    def getAdjustedTrees( tree):
        results = list()
        treeHashSet = set()
        ctr = 20
        queue = PriorityQueue()
        #TODO :check if p queue is working properly
        H = dict()
        queue.put(tree)
        # if tree not in treeHashSet:
        #     treeHashSet.add(tree)

        results.append(tree);
        H[tree.__hash__()] = tree
        tree.setEdit(0);


        #TODO addON is wrong
        treeWithON = tree.addON()

        queue.put(treeWithON);
        # if treeWithON not in treeHashSet:
        #     treeHashSet.add(treeWithON)

        results.append(treeWithON);
        H[treeWithON.__hash__()]  = treeWithON
        treeWithON.setEdit(0)

        while not queue.empty() :
            ctr -= 1
            scoreList = []
            editList = []
            debug_size = queue._qsize()
            # print "\nqueue size = %d\n" %(debug_size)
            # print "Queue tree: "
            tempList =[]

            # for i in range(0, queue._qsize()):
            #     tr = queue.get()
            #     #print tr.getSentence()
            #     # print "%s --> %d"%(tr.getSentence(), tr.getScore())
            #     scoreList.append(tr.getScore())
            #     editList.append(tr.getEdit())
            #     tempList.append(tr)
            #
            # print "scoreList: "
            # print scoreList
            # print "editList: "
            # print editList
            # for tr in tempList:
            #     queue.put(tr)

            # if ctr == 10:
            #     oriTree = queue.get()
            #     # secTree = queue.get()
            #     queue.put(oriTree)
            #     # oriTree =secTree
            # else:
            oriTree = queue.get()

            # print "Currently Adjusting tree: %s:%d" % (oriTree.getSentence(), oriTree.getScore())
            # print
            if (oriTree.getEdit() >= TreeAdjustor.MAX_EDIT):
                continue

            treeList = TreeAdjustor.adjust(oriTree)
            # print "treeAdjuster :219 "
            numInvalidNodes = SyntacticEvaluator().numberOfInvalidNodes(oriTree)

            for i in range(0,len(treeList)):
                currentTree = treeList[i]

                hashValue = currentTree.__hash__()
                if not( H.has_key(hashValue) ):
                    H[hashValue] =  currentTree
                    currentTree.setEdit(oriTree.getEdit() + 1);
                    # print "treeAdjuster :229 "
                    if SyntacticEvaluator().numberOfInvalidNodes(currentTree) <= numInvalidNodes:
                        queue.put(currentTree)
                        results.append(currentTree)
        # for tr in results:
        #     print "Result: %s %d" % (tr.getSentence(), tr.getScore())
        return results
