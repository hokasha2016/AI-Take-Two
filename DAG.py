import sys as sys
import argparse

from collections import defaultdict


class NodeD():
    def __init__(self, bool):
        self.nodeDic = {
            "name": 0,
            "boolean": bool,
            "next": []
        }

    def setNext(self, newpos):
        self.nodeDic["next"].append(newpos)
        # print("added new dest: "+str(newpos)+" -- to node: "+str(self.nodeDic["name"]))
        # print(self.nodeDic["next"])
        # print(self.nodeDic)

    def setPos(self, position):
        self.nodeDic["name"] = position
        # print("added node: "+str(position))


class Graph():
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [None] * self.V

    def addEdge(self, src, dest, bool):
        exists = False
        checNode = False
        node = NodeD(bool)
        for node1 in self.graph:
            if node1 and node1.nodeDic["name"] == src:
                exists = True
                # print(str(src) +" : Does exist")
            # else:
            # print(str(src) + " : Does NOT exist")
        if exists:
            node = self.graph[src]
            # print(str(src) +": EXISTS")
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
            if node3 and node3.nodeDic["name"] == dest:
                checNode = True
        if not checNode:
            temp = NodeD(False)
            temp.nodeDic["name"] = dest
            self.graph[dest] = temp

    def delEdge(self, src, dest):
        # search for src in graph
        for node in self.graph:
            if node.nodeDic["name"] == src:
                Node = node
                break

        # remove dest from node list
        Node.nodeDic["next"].remove(dest)


    def isCyclicUtil(self, v, visited, recStack):

        # Mark current node as visited and
        # adds to recursion stack
        visited[v] = True
        recStack[v] = True

        # Recur for all neighbours
        # if any neighbour is visited and in
        # recStack then graph is cyclic

        if not self.graph[v]:
            return False

        for neighbour in self.graph[v].nodeDic["next"]:
            if not self.graph[v].nodeDic["next"]:
                return False
            else:
                if not visited[neighbour]:
                    if self.isCyclicUtil(neighbour, visited, recStack):
                        return True
                elif recStack[neighbour]:
                    return True

        # The node needs to be popped from
        # recursion stack before function ends
        recStack[v] = False
        return False

    # Returns true if graph is cyclic else false
    def isCyclic(self):
        visited = [False] * self.V
        recStack = [False] * self.V
        for node in range(self.V):
            if not visited[node]:
                if self.isCyclicUtil(node, visited, recStack):
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

def main():
    parser = argparse.ArgumentParser(description='Process args')
    parser.add_argument('--userinput', '-u', type=int,
                        help='0 or empty for defualt graph, 1 or greater for user input')

    args = parser.parse_args()

    if args.userinput and int(args.userinput) > 0:
        # if user wants manual input
        val = input("Enter number of verticies in the graph: ")
        g = Graph(int(val))
        print("To stop adding edges to the graph, enter 0 for src and 0 for dest")

        while True:
            # this while loop asks for src, dest and bool, then inputs it as an adge
            src = int(input("Enter src vertex: "))
            dest = int(input("Enter dest vertex: "))
            boolean = bool(input("Enter boolean for src vertex: "))

            if str(src) == str(0) and str(dest) == str(0):
                # break the while loop if user wants to stop
                break
            g.addEdge(src, dest, boolean)

            if g.isCyclic() == 1:
                # if user graph is cyclic from most recent edge, removed most recent edge
                print("That edge makes the graph cyclic! This edge will be removed.")
                g.delEdge(src, dest)
                
        g.print_graph()

    else:
        # default graph
        g = Graph(5)
        g.addEdge(0, 1, False)
        g.addEdge(0, 4, False)
        g.addEdge(1, 2, True)
        g.addEdge(1, 3, False)
        g.addEdge(1, 4, True)
        g.addEdge(2, 3, False)
        g.addEdge(3, 4, True)

        ####above is no cycle
        # g.addEdge(0, 2, False)
        # g.addEdge(2, 0, True)
        #######including this is a cycle

        if g.isCyclic() == 1:
            print("Graph has a cycle")
        else:
            print("Graph has no cycle")

        g.print_graph()

    # Driver program to the above graph class


# number of nodes, nodes as Boolean variables, arcs, and probability tables on nodes
# (prior probability on source nodes, conditional probabilities on other nodes).


if __name__ == "__main__":
    main()
