import argparse
import itertools
import sys
import unittest

from BayesNet import Net


#!/usr/bin/env python3
class TestBayesNet(unittest.TestCase):
    def setUp(self):
        self.net_alarm = Net('alarm.bn')
        self.net_ex2 = Net('ex2.bn')

    def test_parse(self):
        # func(self)
        # self.assert...(self, value)
        pass

    def test_normalize0(self):
        inputs = [[0.00059224, 0.0014919]]
        outputs = [(0.284165171, 0.715834828)]
        for i1, i2 in enumerate(inputs):
            res = self.net_alarm.normalize(i2)
            self.assertAlmostEqual(res[0], outputs[i1][0])
            self.assertAlmostEqual(res[1], outputs[i1][1])

    def test_toposort0(self):
        res = self.net_alarm.toposort()
        self.assertEqual(res, ['B', 'E', 'A', 'J', 'M'])

    def test_toposort1(self):
        res = self.net_ex2.toposort()
        self.assertEqual(res, ['A', 'B', 'C', 'D', 'E'])

    def test_querygiven_alarm(self):
        cases = [
            (('B', {'B': False}), .999),
            (('B', {'B': True}), .001),
            (('A', {'A': True, 'B': True, 'E': False}), .94),
            (('A', {'A': False, 'B': False, 'E': True}), .71),
            (('A', {'A': False, 'B': False, 'E': False}), .999),
            (('M', {'M': False, 'A': False}), .99)
        ]
        for i, o in cases:
            self.assertAlmostEqual(self.net_alarm.querygiven(*i), o)

    def test_querygiven_ex2(self):
        cases = [
            (('A', {'A': False}), 0.7),
            (('B', {'B': True}), 0.6),
            (('E', {'C': True, 'E': False}), 0.3),
            (('D', {'B': False, 'A': True, 'D': False}), 0.2),
            (('D', {'B': False, 'A': True, 'D': True}), 0.8),
            (('C', {'C': True, 'A': True}), 0.8),
            (('C', {'C': False, 'A': False}), 0.6)
        ]
        for i, o in cases:
            self.assertAlmostEqual(self.net_ex2.querygiven(*i), o)

    def test_genpermutations(self):
        cases = [0, 1, 2, 5]
        for c in cases:
            res = self.net_alarm.genpermutations(c)
            for r in res:
                self.assertEqual(len(r), c)
            self.assertEqual(len(set(res)), len(res))

    def test_makefactor0(self):
        i = ('D', {'D': ['D', 'A']}, {'B': True})
        o = (['A', 'D'], {(True, True): 0.7, (True, False): 0.30000000000000004,
            (False, True): 0.1, (False, False): 0.9})
        self.assertEqual(self.net_ex2.makefactor(*i), o)

    def test_pointwise0(self):
        i1 = (['C', 'E'], {(False, False): 0.8, (False, True): 0.2, (True, True): 0.7, (True, False): 0.3})
        i2 = (['A', 'C'], {(True, True): 0.8, (True, False): 0.2, (False, True): 0.4, (False, False): 0.6})
        o = (['A', 'C', 'E'], {(False, True, True): 0.27999999999999997,
            (False, False, False): 0.48, (True, True, False): 0.24,
            (True, False, False): 0.16000000000000003, (False, True, False): 0.12,
            (False, False, True): 0.12, (True, True, True): 0.5599999999999999,
            (True, False, True): 0.04000000000000001})
        self.assertEqual(self.net_ex2.pointwise('C', i1, i2), o)

    def test_sumout0(self):
        self.assertEqual(self.net_ex2.sumout('D', [(['A', 'D'], {(True, True): 0.7,
            (True, False): 0.3, (False, True): 0.1, (False, False): 0.9})]),
        [(['A'], {(False,): 1.0, (True,): 1.0})])

    def test_alarm_ask1(self):
        inputs = [
            ('B', {'J': False, 'M': True}),
            ('A', {'B': True, 'E': False, 'J': True, 'M': True}),
            ('M', {'B': False, 'E': False}),
            ('E', {'B': True}),
            ('E', {'A': True, 'M': False})
        ]
        outputs = [
            (0.9931, 0.0069),
            (0.0001, 0.9999),
            (0.9893, 0.0107),
            (0.9980, 0.0020),
            (0.7690, 0.2310)
        ]
        for i, i1 in enumerate(inputs):
            res = self.net_alarm.enum_ask(*i1)
            self.assertEqual(round(res[0] - outputs[i][0], 3), 0)
            self.assertEqual(round(res[1] - outputs[i][1], 3), 0)
            res = self.net_alarm.elim_ask(*i1)
            self.assertEqual(round(res[0] - outputs[i][0], 3), 0)
            self.assertEqual(round(res[1] - outputs[i][1], 3), 0)

if __name__ == '__main__':
    unittest.main()























"""
DAG2.py
Made by: Alexander Esenwein & Hussein Okasha
Email: aesenwein2018@my.fit.edu & hokasha2016@my.fit.edu
"""

####NODE OBJECT###
class NodeD:
    def __init__(self, Boolie):  # Makes node dictionary object
        self.nodeDic = {
            "nodePos": 0,
            "booleanState": Boolie,
            "destNode": [],
            "Probability Value": []
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

    def delEdge(self, src, dest): #Delete-edge function
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

    # Prints graph based on number of vertices and their stored information
    def print_graph(self):
        for i in self.graph:
            if i:
                print("Information for vertex {}:\n".format(i.nodeDic["nodePos"]), end="")
                temp = i.nodeDic
                print("Node: "+str(temp["nodePos"])+", Boolean Value: "+str(temp["booleanState"])
                      +", Destination:"+str(temp["destNode"]))
                print(" \n")
            else:
                print("ERROR: Unable to print, Vertex position does not exist!")
        self.printProbability()

    # recursive function used by levelDepth
    def levelDepthUtil(self, v, count, depth_count):
        for neighbour in self.graph[v].nodeDic["destNode"]:
            count += 1
            if count > depth_count:
                depth_count = count
            depth_count = self.levelDepthUtil(neighbour, count, depth_count)
        return depth_count

    # finds maximum depth of the graph
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

    # checks and returns boolean values
    def boolCheck(self, a):
        if a.capitalize()=="T":
            return True
        elif a.capitalize()=="F":
            return False
        else:
            return None

    # finds all parent nodes of vertex v
    def findParents(self, v):
        parents = []
        for node in self.graph:
            if v.nodeDic["nodePos"] in node.nodeDic["destNode"]:
                parents.append(node.nodeDic["nodePos"])
        return parents

    def probability(self):
        print("Now cycling through all nodes to get probability input for each node.")
        for node in self.graph:
            val = []
            parents = self.findParents(node)
            if not parents:
                # if node is root
                check = float(input("Input probability value for root node: "))
                val.append(check)
                node.setProbValue(val)
            else:
                #if node is a child
                print("Parent nodes in probability table for node "
                      + str(node.nodeDic["nodePos"]) + ":")
                for x in parents:
                    sys.stdout.write(str(x) + "\t")
                print('')
                #prints T/F table to input probability value of each node
                table = list(itertools.product([True, False], repeat=len(parents)))
                for x in table:
                    for y in x:
                        if y == False:
                            sys.stdout.write('F\t')
                        else:
                            sys.stdout.write('T\t')
                    val.append(input(""))
                node.setProbValue(val)

    def printProbability(self): #display probability results
        for node in self.graph:
            parents = self.findParents(node)
            if not parents:
                # if node is root
                print("Probability value for root node: "+str(node.nodeDic["Probability Value"][0]))
            else:
                # if node is a child
                print("Parent nodes in probability table for node "
                      + str(node.nodeDic["nodePos"]) + ":")
                for x in parents:
                    sys.stdout.write(str(x) + "\t")
                print('')
                table = list(itertools.product([True, False], repeat=len(parents)))
                counter=0
                # prints T/F table to input probability value of each node
                for x in table:
                    for y in x:
                        if y == False:
                            sys.stdout.write('F\t')
                        else:
                            sys.stdout.write('T\t')
                    #prints value at certain probability, neatly displayed the same way it was stored
                    print(node.nodeDic["Probability Value"][counter])
                    counter+=1

# main function that calls everything
def main():
    parser = argparse.ArgumentParser(description='Process args')
    parser.add_argument('--userinput', '-u', type=int,
        help='0 or empty for default graph, 1 or greater for user input')
    args = parser.parse_args()

    if args.userinput and int(args.userinput) > 0:
        if int(args.userinput) == 1:
            # if user wants manual input:
            # number of nodes, nodes as Boolean variables, arcs, and probability tables on nodes
            # (prior probability on source nodes, conditional probabilities on other nodes).
            val = int(input("Enter number of verticies in the graph: "))
            g = Graph(val)
            print("To stop adding edges to the graph, enter 0 for src and 0 for dest")
            while True:
                # this while loop asks for src, dest and bool, then inputs it as an edge
                invalidIN = False #flag for invalid dest and src values
                try:
                    src = int(input("Enter source vertex: "))
                except:
                    invalidIN = True #if src input is a letter

                try:
                    dest = int(input("Enter destination vertex: "))
                except:
                    invalidIN = True #if dest input is a letter
                #Bool values
                boolIn = str(input("Enter boolean value for this vertex: "))
                boolState = g.boolCheck(boolIn) #returns boolstate , True of False based on input. None if invalid
                # input
                if src==0 and dest==0: #exits input loop
                    break
                elif src >= val or dest >= val:
                    #check incase input value for src and dest more than number of verticies
                    #initally put
                    print("ERROR: Vertex value not within number of vertices. please try again")
                elif invalidIN: #check for lifted flag of invalid src and dest inputs
                    print("ERROR: Source and destination values are only digits. please try again")
                elif boolState == None: #check for flag of invalid boolean input
                    print("ERROR: Boolean value invalid. please try again")
                else:#if passed all checks, adds edge to the graph
                    g.addEdge(src, dest, boolState)

                if g.isCyclic()==1:
                    # if user graph is cyclic from most recent edge, removed most recent edge
                    print("That edge makes the graph cyclic! This edge will be removed.")
                    g.delEdge(src, dest)

                print(" ")
            g.probability()

        else:
            # user wants to skip adding edges
            g = Graph(5)
            g.addEdge(0, 1, False)
            g.addEdge(0, 4, False)
            g.addEdge(1, 2, True)
            g.addEdge(1, 3, False)
            g.addEdge(1, 4, True)
            g.addEdge(2, 3, False)
            g.addEdge(3, 4, True)

        if int(args.userinput) == 2:
            g.probability()
            # get probability input from user

    if not args.userinput or int(args.userinput) == 0:
        # default graph
        g = Graph(5)
        g.addEdge(0, 1, False)
        g.addEdge(0, 4, False)
        g.addEdge(1, 2, True)
        g.addEdge(1, 3, False)
        g.addEdge(1, 4, True)
        g.addEdge(2, 3, False)
        g.addEdge(3, 4, True)
        g.graph[0].setProbValue([0.95])
        g.graph[1].setProbValue([0.25, 0.36])
        g.graph[2].setProbValue([0.15, 0.28])
        g.graph[3].setProbValue([0.12, 0.87, 0.126, 0.96])
        g.graph[4].setProbValue([0.13, 0.45, 0.67, 0.36, 0.754, 0.12, 0.28, 0.39])

        ####above is no cycle
        # g.addEdge(0, 2, False)
        # g.addEdge(2, 0, True)
        #######including this is a cycle

        if g.isCyclic() == 1:
            print("Graph has a cycle")
        else:
            print("Graph has no cycle")

    g.levelDepth()
    print(" ")
    print("Printing Graph Data")
    g.print_graph()

# Driver program to the above graph class
if __name__=="__main__":
    main()
