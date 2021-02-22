import sys as sys

from collections import defaultdict

class NodeD():

    def __init__(self, pos,bool):
        self.nodeDic={
            "name":pos,
            "boolean":bool,
            "next":0
        }
    def setNext(self, newpos):
        self.nodeDic["next"]=newpos
        print(self.nodeDic["next"])
        print(self.nodeDic)


class Graph():
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [None]*self.V

    #def
    def addEdge(self, src, dest, bool):
        node = NodeD(dest,bool)
        node.next = self.graph[src]
        self.graph[src] = node

        # Adding the source node to the destination as
        # it is the undirected graph
        node = NodeD(src,bool)
        node.next = self.graph[dest]
        self.graph[dest] = node
        node.setNext(dest)

    def isCyclicUtil(self, v, visited, recStack):

        # Mark current node as visited and
        # adds to recursion stack
        visited[v] = True
        recStack[v] = True

        # Recur for all neighbours
        # if any neighbour is visited and in
        # recStack then graph is cyclic
        hood = []
        for node in self.graph:
            if node.nodeDic["name"] == v:
                hood.append(node.nodeDic["next"])

        for neighbour in hood:
            if visited[neighbour]==False:
                if self.isCyclicUtil(neighbour, visited, recStack)==True:
                    return True
            elif recStack[neighbour]==True:
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
        for i in range(self.V):
            print("Adjacency list of vertex {}\n head".format(i), end="")
            temp = self.graph[i]
            print(temp)
            print(" \n")


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
    g.addEdge(0, 2, False)
    g.addEdge(2, 0, True)
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

