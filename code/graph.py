
curNodeID = 0

class Node(object):
    def __init__(self,loc,connections=[]):
        self.x = loc[0]
        self.y = loc[1]
        self.edges = []
        global curNodeID
        self.id = curNodeID
        curNodeID += 1
        for e in connections:
            self.addEdge(e)
    
    def __repr__(self):
        return "x "+ str(self.x) + "; y " + str(self.y) + "; id " + str(self.id)
    
    def addEdge(self,n):
        self.edges.append(n) #represents an edge to a node
        n.edges.append(self)
    
    def removeEdge(self,n):
        self.edges.remove(n) #not sure remove is the right function
        n.edges.remove(self)

#First create a graph from all lines. Well, it ends up more as 

#all ends should be circled for nearby ends. Those should be averaged. Then, the distance from all lines to that end should be checked. If the middle of a line is less than 5mm, then break that line there and set it to end at the endpoint.

#The final stage should be checking for any intersections between lines that don't share no nodes as endpoints [to avoid this detecting a shared endpoint as an intersection]. These intersections should split each of those lines and create a node with 4 connections.

def generateGraph(lines):
    nodes = set()
    for l in lines:
        n1 = Node(l[0])
        n2 = Node(l[1],[n1])
        nodes.add(n1)
        nodes.add(n2)

    return nodes


def collectEnds(nodes):
    while True:
        pass


if __name__=='__main__':
    n1 = Node((10.5,3.2))
    n2 = Node((2,2),[n1])
    n3 = Node((1,1),[n1,n2])
    print n1.edges
    n3.removeEdge(n2)
    print n1.edges
    print n2.edges
    generateGraph([[(1,1),(3,3)]])

