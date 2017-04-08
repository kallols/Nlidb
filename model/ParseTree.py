from nltk.tree import ParentedTree
from nltk.tree import Tree

from Node import Node
from model.TreeAdjustor import TreeAdjustor
from model.NodeInfo import NodeInfo
from model.SQLTranslator import SQLTranslator
from model.SyntacticEvaluator import SyntacticEvaluator


class ParseTree:
    edit = None
    root = None
    nodes = list()
    time = None
    # TODO: This is created for the priority q . check if its working
    def __lt__(self, t2):
        # print "!!"
        # print self.toString()
        a = self.getScore()
        b = t2.getScore()
        # if(self.getScore() != t2.getScore()):
        return  self.getScore() >  t2.getScore()
        # else:
        #     return self.time < t2.time

    def __init__(self, text=None, parser=None, node=None, other=None):


        #self.root =None
        #self.nodes = list()
        self.time = None
        def traverseTree(tree):
            print("tree:", tree.label())
            parInd = self.findNodeInd(tree.label())
            # print parInd
            # print tree.get_children()
            for subtree in tree:
                if type(subtree) == Tree:
                    childInd = self.findNodeInd(subtree.label())
                    self.nodes[parInd].setChild(self.nodes[childInd])
                    self.nodes[childInd].setParent(self.nodes[parInd])
                    traverseTree(subtree)
                else:
                    childInd = self.findNodeInd(subtree.encode('ascii', 'ignore'))
                    self.nodes[parInd].setChild(self.nodes[childInd])
                    self.nodes[childInd].setParent(self.nodes[parInd])
                    print type(subtree.encode('ascii', 'ignore'))

        if text is not None and parser is not None and node is None and other is None:
            tagged = parser.tagger.tag(text.split())
            print tagged
            gs_graph_iter = parser.parser.raw_parse(text)
            self.root = Node(index=0, word="ROOT", posTag="ROOT")

            self.nodes.append(self.root)

            for child in gs_graph_iter:
                gs_graph = child.tree()
                p_gs_graph = ParentedTree.convert(gs_graph)
                print p_gs_graph
                break

            gs_graph.pprint()

            ind = 0
            for word in text.split():
                # print tagged[ind][1]
                self.nodes.append(Node(index=ind + 1, word=word, posTag=tagged[ind][1]))
                ind += 1

            rootInd = self.findNodeInd("ROOT")
            retInd = self.findNodeInd("Return")
            self.nodes[rootInd].setChild(self.nodes[retInd])
            traverseTree(gs_graph)
            print "...................."
            # self.nodes[1].setChild(self.nodes[3])
            for n in self.nodes:
                print n.getWord()
                print [word.getWord() for word in n.getChildren()]
        elif (node is not None):
            self.root = node.clone()
        elif other is not None:
            ParseTree(node= other.root)


    def findNodeInd(self, word):
        ind = 0
        for i in self.nodes:
            if i.getWord() == word:
                return ind
            ind += 1
        return None

    def size(self):
        return len(self.root.genNodesArray())

    def getEdit(self):
        return self.edit

    def setEdit(self, edit):
        self.edit = edit

    def removeMeaninglessNodes2(self, curr):
        if curr is None:
            return
        currChildren = curr.getChildren()

        for child in currChildren:
            self.removeMeaninglessNodes2(child)

        if (not curr.equals(self.root)) and curr.getInfo().getType() == "UNKNOWN":
            curr.parent.getChildren().remove(curr)
            for child in curr.getChildren():
                curr.parent.getChildren().add(child)
                child.parent = curr.parent

    def removeMeaningLessNodes(self):
        childrenList = self.root.getChildren()
        if childrenList[0].getInfo is None:
            print "ERR! Node info not yet mapped!"
        self.removeMeaninglessNodes2(self.root)

    def insertImplicitNodes(self):
        childrenOfRoot = self.root.getChildren()

        if childrenOfRoot.size() <= 1:
            return

        # phase 1, add nodes under select to left subtree
        print "Phase 1, add nodes under select node to left subtree"

        IndexOfSN = 0
        for i in range(0, len(childrenOfRoot)):
            if (childrenOfRoot[i].getInfo().getType() == "SN"):
                IndexOfSN = i;

        # start from the name node

        SN = childrenOfRoot[IndexOfSN]
        SN_children = SN.getChildren()
        IndexOfSN_NN = 0

        for i in range(0, len(SN_children)):

            if (SN_children[i].getInfo().getType() == "NN"):
                IndexOfSN_NN = i;
                break

        # add them to left subtree of all branches

        copy = None
        indexOfAppendedNode = None
        SN_NN = SN_children[IndexOfSN_NN]

        for i in range(0, len(childrenOfRoot)):

            if i != IndexOfSN:

                nodes_SN_NN = childrenOfRoot[i].genNodesArray()
                indexOfAppendedNode = self.nameNodeToBeAppended(nodes_SN_NN)

                if indexOfAppendedNode != -1:
                    copy = SN_NN.clone()
                    copy.setOutside(True)

                    nodes_SN_NN[indexOfAppendedNode].setChild(copy)
                    copy.setParent(nodes_SN_NN[indexOfAppendedNode])

        # phase 2, compare left core node with right core node
        print "Phase 2, core node insertion"
        indexOfRightCoreNode = -1
        indexOfLeftCoreNode = -1

        for i in range(0, len(childrenOfRoot)):

            if (i != IndexOfSN):

                nodes = childrenOfRoot[i].genNodesArray()
                startOfRightBranch = self.endOfLeftBranch(nodes) + 1
                sizeOfRightTree = len(nodes[startOfRightBranch].getChildren()) + 1

                # if right tree only contains numbers, skip it

                if sizeOfRightTree != 1 or not self.isNumeric(nodes[startOfRightBranch].getWord()):

                    indexOfLeftCoreNode = self.coreNode(nodes, True);
                    indexOfRightCoreNode = self.coreNode(nodes, False);

                    # if left core node exists

                    if indexOfLeftCoreNode != -1:

                        doInsert = False;

                        # if right subtree neither have core node nor it only contains number
                        if indexOfRightCoreNode == -1:

                            # copy core node only

                            doInsert = True;
                        elif not nodes[indexOfRightCoreNode].getInfo().ExactSameSchema(
                                nodes[indexOfLeftCoreNode].getInfo()):
                            # if right core node & left core node are different schema
                            # copy core node only
                            doInsert = True;

                        if doInsert:

                            copy = nodes[indexOfLeftCoreNode].clone()
                            copy.children = list()
                            copy.setOutside(True)

                            insertAroundFN = False;

                            indexOfNewRightCN = self.IndexToInsertCN(nodes);

                            if (indexOfNewRightCN == -1):

                                for j in range(len(nodes) - 1, self.endOfLeftBranch(nodes), -1):

                                    if (nodes[j].getInfo().getType() == "FN"):
                                        indexOfNewRightCN = j + 1;
                                        insertAroundFN = True;
                                        break;

                            if (insertAroundFN):

                                # THIS ONLY HANDLES FN NODE HAS NO CHILD OR ONE NAME NODE CHILD

                                FN_children = nodes[indexOfNewRightCN - 1].getChildren();

                                for j in range(0, len(FN_children)):
                                    copy.setChild(FN_children.get(j));
                                    FN_children.get(j).setParent(copy);

                                copy.setParent(nodes[indexOfNewRightCN - 1]);
                                nodes[indexOfNewRightCN - 1].children = list()
                                nodes[indexOfNewRightCN - 1].setChild(copy)
                            else:

                                # if right subtree only contains VN, adjust index

                                if (indexOfNewRightCN == -1):
                                    indexOfNewRightCN = self.endOfLeftBranch(nodes) + 1;

                                copy.setChild(nodes[indexOfNewRightCN]);
                                copy.setParent(nodes[indexOfNewRightCN].getParent());
                                nodes[indexOfNewRightCN].getParent().removeChild(nodes[indexOfNewRightCN]);
                                nodes[indexOfNewRightCN].getParent().setChild(copy);
                                nodes[indexOfNewRightCN].setParent(copy);

                        # phase 3, map each NV under left core node to right core node

                        print "Phase 3, transfer constrain nodes from left to right"
                        NV_children_left = nodes[indexOfLeftCoreNode].getChildren()

                        for j in range(0, len(NV_children_left)):

                            nodes_new = childrenOfRoot[i].genNodesArray();
                            indexOfRightCoreNode = self.coreNode(nodes_new, False);
                            NV_children_right = nodes_new[indexOfRightCoreNode].getChildren();
                            found_NV = False;

                            curr_left = NV_children_left.get(j);
                            curr_left_type = curr_left.getInfo().getType();

                            for k in range(0, len(NV_children_right)):
                                # compare
                                curr_right = NV_children_right.get(k);

                                # strictly compare, exact match ON

                                if (curr_left_type.equals("ON")):

                                    if (curr_left.equals(curr_right)):
                                        found_NV = True;
                                        break
                                else:

                                    if (curr_left.getInfo().sameSchema(curr_right.getInfo())):
                                        found_NV = True;
                                        break;

                            if (not found_NV):
                                # insert

                                copy = curr_left.clone();
                                nodes_new[indexOfRightCoreNode].setChild(copy);
                                copy.setOutside(True);
                                copy.setParent(nodes_new[indexOfRightCoreNode]);

                    # phase 4, insert function node

                    print "Phase 4, insert missing function node"

                    nodes_final_temp = childrenOfRoot[i].genNodesArray();
                    indexOfLeftFN_Tail = -1;

                    for j in range(indexOfLeftCoreNode, -1, -1):

                        if (nodes_final_temp[j].getInfo().getType() == "FN"):
                            indexOfLeftFN_Tail = j;
                            break;

                    if (indexOfLeftFN_Tail != -1):

                        for k in range(1, indexOfLeftFN_Tail + 1):

                            nodes_final = childrenOfRoot[i].genNodesArray();
                            indexOfRightCoreNode = self.coreNode(nodes_final, False);

                            found_FN = False;

                            for j in range(self.endOfLeftBranch(nodes_final) + 1, indexOfRightCoreNode, -1):

                                if (nodes_final[j].getInfo().ExactSameSchema(nodes_final[k].getInfo())):
                                    found_FN = True;

                            if (not found_FN):
                                copy = nodes_final[k].clone();
                                copy.setOutside(True);
                                copy.children = list()
                                nodes[0].removeChild(nodes_final[self.endOfLeftBranch(nodes_final) + 1]);
                                nodes[0].setChild(copy);

                                copy.setParent(nodes[0]);
                                copy.setChild(nodes[self.endOfLeftBranch(nodes_final) + 1]);
                                nodes[self.endOfLeftBranch(nodes_final) + 1].setParent(copy);

    def IndexToInsertCN(self, nodes):
        for i in range(self.endOfLeftBranch(nodes) + 1, len(nodes)):

            if (nodes[i].getInfo().getType() == "NN"):
                return i

        return -1

    def nameNodeToBeAppended(self, nodes):

        for i in range(self.endOfLeftBranch(nodes), 0, -1):

            if (nodes[i].getInfo().getType() == "NN"):
                return i

        return -1

    def endOfLeftBranch(self, nodes):

        for i in range(2, len(nodes)):

            if (nodes[i].getParent().equals(nodes[0])):
                return i - 1;

        return -1

    def isNumeric(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def coreNode(self, nodes, left):
        startIndex = 1
        endIndex = self.endOfLeftBranch(nodes);

        if (not left):
            startIndex = self.endOfLeftBranch(nodes) + 1;
            endIndex = nodes.length - 1;

        for i in range(startIndex, endIndex):

            if (nodes[i].getInfo().getType() == "NN"):
                return i

        return -1;

    def mergeLNQN(self):
        nodes = self.root.genNodesArray();
        for i in range(0, self.size()):
            if (nodes[i].getInfo().getType() == "LN") or nodes[i].getInfo().getType() == "QN":
                word = "(" + nodes[i].getWord() + ")";
                parentWord = nodes[i].getParent().getWord() + word;
                nodes[i].getParent().setWord(parentWord);
                self.removeNode(nodes[i]);

        tree = ParseTree(node = self.root);
        return tree

    def removeNode(self, curNode):
        curNode.getParent().getChildren().remove(curNode);
        for child in curNode.getChildren():
            child.setParent(curNode.getParent());
            curNode.getParent().setChild(child);

    def addON(self):

        # print "www"
        # print self

        root = self.root.clone();

        on = Node(index=0, word="equals", posTag="postag");
        on.info = NodeInfo(type="ON", value="=")
        root.setChild(on);
        on.setParent(root);
        tree = ParseTree(node=root);

        # print "qqq"
        # print tree

        return tree

    def compare(self, t1, t2):
        if (t1.getScore() != t2.getScore()):
            return  t1.getScore() > t2.getScore()
        else:
            return t1.getEdit() < t2.getEdit()

    def getAdjustedTrees(self):
        result = TreeAdjustor.getAdjustedTrees(self)
        sorted(result, cmp=self.compare)
        return result[0:4]

    def translateToSQL(self, schema):

        translator = SQLTranslator(self.root, schema)
        return translator.getResult()

    def __hash__(self):
        prime = 31
        result = 17
        result = prime * result + (0 if self.root is None else (self.root).__hash__())
        return result

    def __eq__(self, obj):
        # if (self == obj):
        #     return True
        if (obj is None):
            return False;
        if (self.__class__ != obj.__class__):
            return False

        if (self.root is None):
            if (obj.root is not None):
                return False

        elif (not self.root.equals(obj.root)):
            return False;
        return True;


    def equals(self, obj):
        # if (self == obj):
        #     return True
        if (obj is None):
            return False;
        if (self.__class__ != obj.__class__):
            return False

        if (self.root is None):
            if (obj.root is not None):
                return False

        elif (not self.root.equals(obj.root)):
            return False;
        return True;

    #### TODO : public class ParseTreeIterator implements Iterator<Node>
    def nodeToString(self,curr):
        if curr is None :
            return ""
        s = curr.toString() + " -> "
        #print curr.getChildren()
        s += ''.join( [ child.toString()  for child in curr.getChildren()]) + "\n";
        for child in curr.getChildren():
            s += self.nodeToString(child)
        return s


    def getSentence(self):
        sb = []
        first = True;
        for node in self:
            if (first):
                sb.append(node.getWord());
                first = False;
            else:
                sb.append(" ")
                sb.append(node.getWord())
        return ''.join(sb)

    def toString(self):
        s ="Sentence: " + self.getSentence()+"\n"+self.nodeToString(self.root)
        return s

    def __str__(self):
        s = "Sentence: " + self.getSentence() + "\n" + self.nodeToString(self.root)
        return s


    def getScore(self):
        return - SyntacticEvaluator().numberOfInvalidNodes(self);

    def iterator(self, rootNode):
        return self.ParseTreeIterator(rootNode)

    def __iter__(self):
        #print 123
        self.stack = list()
        self.stack.insert(0, self.root)

        return self

    stack = list()

    def next(self):  # Python 3: def __next__(self)
       # print 4
        if len(self.stack) == 0:
            raise StopIteration
        else:
            curr = self.stack.pop(0)
           # print curr
            if(curr is None):
                print "Self: "
                print self
            children = curr.getChildren()
            #print children
            for i in range(len(children) - 1, -1, -1):
                self.stack.insert(0, children[i])
                if children[i] is None:
                    print "hahaha:"
                    print self
            return curr


    class ParseTreeIterator:
        stack = list()

        def __init__(self, rootNode):
            self.stack.insert(0, rootNode)

        def hasNext(self):
            if len(self.stack) == 0:
                return False
            return True

        def getNext(self):
            curr = self.stack.pop(0)
            children = curr.getChildren()
            for i in range(len(children)-1,-1,-1):
                self.stack.insert(0,children[i])
            return curr



#
# a = NLParser()
# ParseTree(text="Return the number of authors who published theory papers before 1980 .", parser=a)
