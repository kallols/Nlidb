
class SyntacticEvaluator:
    numOfInvalid = 0
    def __init__(self):
        self.numOfInvalid =0

    def checkROOT(self, node):
        numOfInvalid = 0
        children = node.getChildren()
        sizeOfChildren = len(children)

        if (sizeOfChildren == 0):
            numOfInvalid += 1
            node.isInvalid = True
        elif(sizeOfChildren == 1 and not children[0].getInfo().getType().equals("SN")):
            numOfInvalid += 1
            node.isInvalid = True
        elif (sizeOfChildren > 1):
            if (not children[0].getInfo().getType().equals("SN")):
                numOfInvalid += 1
                node.isInvalid = True
            else:
                for j in range(1, sizeOfChildren):
                    if (not children.get(j).getInfo().getType().equals("ON")):
                        numOfInvalid += 1
                        node.isInvalid = True

        return numOfInvalid


    def checkSN(self, node):
        numOfInvalid = 0
        children = node.getChildren()
        sizeOfChildren = children.size()

        if (sizeOfChildren != 1):
            numOfInvalid += 1;
            node.isInvalid = True;
        else:
            childType = children[0].getInfo().getType()
            if (not(childType.equals("NN") or childType.equals("FN"))):
                numOfInvalid += 1;
                node.isInvalid = True;

        return numOfInvalid


    def checkON(self, node):
        numOfInvalid = 0
        parentType = node.getParent().getInfo().getType()
        children = node.getChildren()
        sizeOfChildren = children.size()

        if (parentType.equals("ROOT")):
            if (sizeOfChildren != 2):
                numOfInvalid += 1;
                node.isInvalid = True;
            else:
                for j in range(0,sizeOfChildren):
                    childType = children[j].getInfo().getType()
                    if (j == 0):
                        if (not(childType.equals("NN") or childType.equals("FN"))):
                            numOfInvalid += 1;
                            node.isInvalid = True;
                            break
                    elif j == 1:
                        if (childType.equals("ON")):
                            numOfInvalid += 1;
                            node.isInvalid = True;
                            break
        elif (parentType.equals("NN")):
            if (sizeOfChildren != 1):
                numOfInvalid += 1;
                node.isInvalid = True;
            elif (not children[0].getInfo().getType().equals("VN")):
                numOfInvalid += 1;
                node.isInvalid = True

        return numOfInvalid

    def checkNN(self, node):
        numOfInvalid = 0
        parentType = node.getParent().getInfo().getType()
        children = node.getChildren()
        sizeOfChildren = children.size()

        if (parentType.equals("NN")):
            if (sizeOfChildren != 0):
                numOfInvalid += 1;
                node.isInvalid = True
        elif (parentType.equals("SN") or parentType.equals("FN") or parentType.equals("ON")):
            if (sizeOfChildren != 0):
                for j in range(0,sizeOfChildren):
                    childType = children.get(j).getInfo().getType()
                    if (not(childType.equals("NN") or childType.equals("VN") or childType.equals("ON"))):
                        numOfInvalid += 1;
                        node.isInvalid = True
                        break

        return numOfInvalid


    def checkVN(self, node):
        numOfInvalid = 0
        children = node.getChildren();
        sizeOfChildren = children.size();
        if (sizeOfChildren != 0):
            numOfInvalid += 1;
            node.isInvalid = True

        return numOfInvalid


    def checkFN(self, node):
        numOfInvalid = 0
        parentType = node.getParent().getInfo().getType()
        children = node.getChildren()
        sizeOfChildren = children.size()
        if (sizeOfChildren == 0):
            if (not parentType.equals("ON")):
                numOfInvalid += 1;
                node.isInvalid = True;
        elif (sizeOfChildren == 1):
            childType = children.get(0).getInfo().getType()
            if (not(parentType.equals("ON") or parentType.equals("SN"))):
                numOfInvalid += 1;
                node.isInvalid = True
            elif (not childType.equals("NN")):
                numOfInvalid += 1;
                node.isInvalid = True
            else:
                numOfInvalid += 1;
                node.isInvalid = True
            return numOfInvalid

    def numberOfInvalidNodes (self, T):
        numOfInvalid = 0
        for curNode in T:
            curType = curNode.getInfo().getType()
            if (curType.equals("ROOT")):
                numOfInvalid = numOfInvalid + self.checkROOT(curNode)
            if (curType.equals("SN")):
                numOfInvalid = numOfInvalid + self.checkSN(curNode)
            elif (curType.equals("ON")):
                numOfInvalid = numOfInvalid + self.checkON(curNode)
            elif (curType.equals("NN")):
                numOfInvalid = numOfInvalid + self.checkNN(curNode)
            elif (curType.equals("VN")):
                numOfInvalid = numOfInvalid + self.checkVN(curNode)
            elif (curType.equals("FN")):
                numOfInvalid = numOfInvalid + self.checkFN(curNode)


        return numOfInvalid


