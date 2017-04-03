from nltk.tree import ParentedTree
from nltk.tree import Tree

from Node import Node
from model import TreeAdjustor
from model.NodeInfo import NodeInfo
from model.SQLTranslator import SQLTranslator
from model.SyntacticEvaluator import SyntacticEvaluator


class ParseTree:
    edit = None
    root = None
    nodes = list()

    # TODO: This is created for the priority q . check if its working
    def __lt__(t1, t2):
        return - t1.getScore() + t2.getScore()

    def __init__(self, text=None, parser=None, node=None, other=None):

        def traverseTree(tree):
            print("tree:", tree.label())
            parInd = self.findNodeInd(tree.label())
            # print parInd
            # print tree.get_children()
            for subtree in tree:
                if type(subtree) == Tree:
                    childInd = self.findNodeInd(subtree.label())
                    self.nodes[parInd].setChild(self.nodes[childInd])
                    traverseTree(subtree)
                else:
                    childInd = self.findNodeInd(subtree.encode('ascii', 'ignore'))
                    self.nodes[parInd].setChild(self.nodes[childInd])
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

            traverseTree(gs_graph)
            print "...................."
            # self.nodes[1].setChild(self.nodes[3])
            for n in self.nodes:
                print n.getWord()
                print [word.getWord() for word in n.getChildren()]

    def findNodeInd(self, word):
        ind = 0
        for i in self.nodes:
            if i.getWord() == word:
                return ind
            ind += 1
        return None

    def size(self):
        return len(self.root.getNodesArray())

    def getEdit(self):
        return self.edit

    def setEdit(self, edit):
        self.edit = edit

    def removeMeaningLessNodes2(self, curr):
        if curr is None:
            return
        currChildren = curr.getChildren()

        for child in currChildren:
            self.removeMeaningLessNodes(child)

        if curr != curr.equals(self.root) and curr.getInfo().getType().equals("UNKNOWN"):
            curr.parent.getChildren().remove(curr)
            for child in curr.getChildren():
                curr.parent.getChildren().add(child)
                child.parent = curr.parent

    def removeMeaningLessNodes(self):
        if self.root.getChildren()[0].getInfo is None:
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
            if (childrenOfRoot.get(i).getInfo().getType().equals("SN")):
                IndexOfSN = i;

        # start from the name node

        SN = childrenOfRoot[IndexOfSN]
        SN_children = SN.getChildren()
        IndexOfSN_NN = 0

        for i in range(0, len(SN_children)):

            if (SN_children.get(i).getInfo().getType().equals("NN")):
                IndexOfSN_NN = i;
                break

        # add them to left subtree of all branches

        copy = None
        indexOfAppendedNode = None
        SN_NN = SN_children[IndexOfSN_NN]

        for i in range(0, len(childrenOfRoot)):

            if i != IndexOfSN:

                nodes_SN_NN = childrenOfRoot.get(i).genNodesArray()
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

                                    if (nodes[j].getInfo().getType().equals("FN")):
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

                            nodes_new = childrenOfRoot.get(i).genNodesArray();
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

                    nodes_final_temp = childrenOfRoot.get(i).genNodesArray();
                    indexOfLeftFN_Tail = -1;

                    for j in range(indexOfLeftCoreNode, -1, -1):

                        if (nodes_final_temp[j].getInfo().getType().equals("FN")):
                            indexOfLeftFN_Tail = j;
                            break;

                    if (indexOfLeftFN_Tail != -1):

                        for k in range(1, indexOfLeftFN_Tail + 1):

                            nodes_final = childrenOfRoot.get(i).genNodesArray();
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

            if (nodes[i].getInfo().getType().equals("NN")):
                return i

        return -1

    def nameNodeToBeAppended(self, nodes):

        for i in range(self.endOfLeftBranch(nodes), 0, -1):

            if (nodes[i].getInfo().getType().equals("NN")):
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

            if (nodes[i].getInfo().getType().equals("NN")):
                return i

        return -1;

    def mergeLNQN(self):
        nodes = self.root.genNodesArray();
        for i in range(0, self.size()):
            if (nodes[i].getInfo().getType().equals("LN") or nodes[i].getInfo().getType().equals("QN")):
                word = "(" + nodes[i].getWord() + ")";
                parentWord = nodes[i].getParent().getWord() + word;
                nodes[i].getParent().setWord(parentWord);
                self.removeNode(nodes[i]);

        tree = ParseTree(self.root);
        return tree

    def removeNode(self, curNode):
        curNode.getParent().getChildren().remove(curNode);
        for child in curNode.getChildren():
            child.setParent(curNode.getParent());
            curNode.getParent().setChild(child);

    def addON(self):
        root = self.root.clone();
        on = Node(0, "equals", "postag");
        on.info = NodeInfo("ON", "=");
        root.setChild(on);
        on.setParent(root);
        tree = ParseTree(root);
        return tree

    def compare(self, t1, t2):
        if (t1.getScore() != t2.getScore()):
            return - t1.getScore() + t2.getScore()
        else:
            return t1.getEdit() - t2.getEdit();

    def getAdjustedTrees(self):
        result = TreeAdjustor.getAdjustedTrees(self)
        sorted(result, cmp=self.compare())
        return result.subList(0, 4)

    def translateToSQL(self, schema):

        translator = SQLTranslator(self.root, schema)
        return translator.getResult()

    def hashCode(self):
        prime = 31
        result = 17
        result = prime * result + (0 if self.root is None else  self.root.hashCode())
        return result;

    def equals(self, obj):
        if (self == obj):
            return True;
        if (obj is None):
            return False;
        if (self.__class__ != obj.__class):
            return False

        if (self.root is None):
            if (obj.root is not None):
                return False
        elif (not self.root.equals(obj.root)):
            return False;
        return True;

    #### TODO : public class ParseTreeIterator implements Iterator<Node>

    def getScore(self):
        return - SyntacticEvaluator.numberOfInvalidNodes(self);

    def iterator(self):
        return self.ParseTreeIterator()

    class ParseTreeIterator:
        stack = list()

        def __init__(self):
            self.stack.insert(0,ParseTree.root)

        def hasNext(self):
            if len(self.stack) == 0:
                return False
            return True

        def getNext(self):
            curr = self.stack.pop(0)
            children = curr.getChildren()
            for i in range(children.size(),-1.-1):
                self.stack.insert(0,children[i])
            return curr



#
# a = NLParser()
# ParseTree(text="Return the number of authors who published theory papers before 1980 .", parser=a)
