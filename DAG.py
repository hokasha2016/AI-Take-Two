import sys as sys
import argparse

from collections import defaultdict


####NODE OBJECT###
class NodeD:
    def __init__(self, Boolie):  # Makes node dictionary object
        self.nodeDic = {
            "nodePos": 0,
            "booleanState": Boolie,
            "destNode": [],
            "Probability Value": 0
        }

    # node dictionary Setter's
    def setNext(self, newPos):  # adds new destination node for current node
        self.nodeDic["destNode"].append(newPos)

    def setPos(self, position):  # sets/modifies nodePos of node
        self.nodeDic["nodePos"] = position

    def setBool(self, Boolie):  # sets/modifies boolean value of node
        self.nodeDic["booleanState"] = Boolie
    
    def setProbValue(self,v): # sets/modifies Probability Value
        self.nodeDic["Probability Value"] = v


class Graph:

    def __init__(self, vertices):  # initalizes graph which is an empty list size of number of verticies
        self.V = vertices
        self.graph = [None] * self.V

    def addEdge(self, src, dest, boolie):  # stores/ generates new node edge into the graph
        exists = False
        checNode = False
        node = NodeD(boolie)  # makes empty node
        # Flips flag for finding previously existing node
        for node1 in self.graph:
            if node1 and node1.nodeDic["nodePos"]==src:
                exists = True

        # if node already exists, modify
        if exists:
            # adds the new dest node to list of destNode nodes,
            # and sets boolean Value based on input
            node = self.graph[src]
            node.setNext(dest)
            node.setBool(boolie)
        else:
            # makes new Node and stores new Info
            node.setPos(src)
            node.setNext(dest)
            node.setBool(boolie)
            node.next = self.graph[src]
            self.graph[src] = node
            node.next = self.graph[dest]
            self.graph[dest] = node

        # Checks to see if destination node exists, flips "checNode" flag
        for node3 in self.graph:
            if node3 and node3.nodeDic["nodePos"]==dest:
                checNode = True
        # If dest node doesnt exist, make False empty node with nodePos of dest node
        if not checNode:
            temp = NodeD(False)
            temp.nodeDic["nodePos"] = dest
            self.graph[dest] = temp

    def delEdge(self, src, dest):
        # search for src in graph
        for node2 in self.graph:
            if node2 and node2.nodeDic["nodePos"]==src:
                Node = node2
                break
        # remove dest from node list
        try:
            Node.nodeDic["destNode"].remove(dest)
        except Node:
            print("ERROR: unable to remove edge, Vertex not found")

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

        for neighbour in self.graph[v].nodeDic["destNode"]:
            if not self.graph[v].nodeDic["destNode"]:
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
        # Prints graph based on number of vertices and their stored information
        for i in self.graph:
            if i:
                print("Adjacency list of vertex {}\n".format(i.nodeDic["nodePos"]), end="")
                temp = i.nodeDic
                print(temp)
                print(" \n")
            else:
                print("ERROR: Unable to print, Vertex position does not exist!")


    def levelDepthUtil(self, v, count, depth_count):
        for neighbour in self.graph[v].nodeDic["destNode"]:
            count += 1
            if count > depth_count:
                depth_count = count
            depth_count = self.levelDepthUtil(neighbour, count, depth_count)
        return depth_count

    def levelDepth(self):
        try:
            if self.isCyclic()==0:
                depth_count = 0
                depth_count = self.levelDepthUtil(0, 0, depth_count)
                print("Lowest depth is: " + str(depth_count))
            else:
                print("Graph is cyclic! Depth can be infinite!")
        except:
            print("ERROR: no depth found")

    # Driver program to the above graph class

    # number of nodes, nodes as Boolean variables, arcs, and probability tables on nodes
    # (prior probability on source nodes, conditional probabilities on other nodes).

    # checks and returns boolean values
    def boolCheck(self, a):
        if a.capitalize()=="T":
            return True
        elif a.capitalize()=="F":
            return False


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
        count = 0
        while True:
            # this while loop asks for src, dest and bool, then inputs it as an edge
            print("Vertex " + str(count) + ": ")
            src = int(input("Enter source vertex: "))
            dest = int(input("Enter destination vertex: "))
            boolIn = str(input("Enter boolean value for this vertex: "))
            boolState = g.boolCheck(boolIn)
            if src==0 and dest==0:
                break
            else:
                g.addEdge(src, dest, boolState)

            if g.isCyclic()==1:
                # if user graph is cyclic from most recent edge, removed most recent edge
                print("That edge makes the graph cyclic! This edge will be removed.")
                g.delEdge(src, dest)

            count += 1
            print(" ")

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

        if g.isCyclic()==1:
            print("Graph has a cycle")
        else:
            print("Graph has no cycle")


    g.print_graph()
    g.levelDepth()

# Driver program to the above graph class
if __name__=="__main__":
    main()
