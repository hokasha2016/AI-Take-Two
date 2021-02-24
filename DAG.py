import sys as sys

from collections import defaultdict

class NodeD():
    def __init__(self, bool):

        self.nodeDic={
            "name":0,
            "boolean":bool,
            "next":[]
        }
    def setNext(self, newpos):
        self.nodeDic["next"].append(newpos)
        #print("added new dest: "+str(newpos)+" -- to node: "+str(self.nodeDic["name"]))
       # print(self.nodeDic["next"])
       # print(self.nodeDic)
    def setPos(self, position):
        self.nodeDic["name"]=position
        #print("added node: "+str(position))

class Graph():
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [None]*self.V

    #def
    def addEdge(self, src, dest, bool):
        exists=False
        checNode=False
        node = NodeD(bool)
        for node1 in self.graph:
            if node1 and node1.nodeDic["name"]==src:
                exists=True
                #print(str(src) +" : Does exist")
            #else:
                #print(str(src) + " : Does NOT exist")
        if exists==True:
            node=self.graph[src]
            #print(str(src) +": EXISTS")
            node.setNext(dest)
        else:
           # print(str(src) + ": doesn't exist")
            node.setPos(src)
            node.next = self.graph[src]
            self.graph[src] = node
            node.next = self.graph[dest]
            self.graph[dest] = node
            node.setNext(dest)
        for node3 in self.graph:
            if node3 and node3.nodeDic["name"]==dest:
                checNode=True
        if checNode==False:
            temp = NodeD(False)
            temp.nodeDic["name"] = dest
            self.graph[dest] = temp

    def isCyclicUtil(self, v, visited, recStack):

        # Mark current node as visited and
        # adds to recursion stack
        visited[v] = True
        recStack[v] = True

        # Recur for all neighbours
        # if any neighbour is visited and in
        # recStack then graph is cyclic

        for neighbour in self.graph[v].nodeDic["next"]:
            if not self.graph[v].nodeDic["next"]:
                return False
            else:
                if not visited[neighbour]:
                    if self.isCyclicUtil(neighbour, visited, recStack):
                        return True
                elif recStack[neighbour]:
                    return True

        # The node needs to be poped from
        # recursion stack before function ends
        recStack[v] = False
        return False

    # Returns true if graph is cyclic else false
    def isCyclic(self):
        visited = [False] * self.V
        recStack = [False] * self.V
        for node in range(self.V):
            if visited[node]==False:
                    if self.isCyclicUtil(node, visited, recStack)==True:
                        return True
        return False

    def print_graph(self):
        for i in self.graph:
            print("Adjacency list of vertex {}\n head".format(i.nodeDic["name"]), end="")
            temp = i.nodeDic
            print(temp)
            print(" \n")

   # def levelDepth(self,count,):


                # Driver program to the above graph class

        # number of nodes, nodes as Boolean variables, arcs, and probability tables on nodes
        # (prior probability on source nodes, conditional probabilities on other nodes).

def main(n):

    g = Graph(n)
    g.addEdge(0, 1, False)
    g.addEdge(0, 4, False)
    g.addEdge(1, 2, True)
    g.addEdge(1, 3, False)
    g.addEdge(1, 4, True)
    g.addEdge(2, 3, False)
    g.addEdge(3, 4, True)
    ####above is no cycle
    #g.addEdge(0, 2, False)
    #g.addEdge(2, 0, True)
    #######including this is a cycle

    if g.isCyclic() == 1:
        print("Graph has a cycle")
    else:
        print("Graph has no cycle")

    g.print_graph()


        # Driver program to the above graph class
#number of nodes, nodes as Boolean variables, arcs, and probability tables on nodes
# (prior probability on source nodes, conditional probabilities on other nodes).


if __name__ == "__main__":
    main(5)

