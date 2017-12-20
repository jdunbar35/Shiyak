# file: airportMap.py
# author: Jack Dunbar
# date: 11/19/2017
# Defines the class that is the graph of airports
# Also contains cost-minimizing function

import copy

class airportMap(object):
    def __init__(self):
        # Nested dictionary with airports mapped their connections mapped to the cost of those connections
        self.map = {}
        # Dictionary mapping airports to the pixel locations of those airports
        self.airportLocations = {}
        # Dictionary mapping airports in Northeast ot pixel locations
        self.northeastLocations = {}
        # Dictionary mapping airports to names and codes (used in webscraping)
        self.codes = {}
        # Minimum cost route between two airports
        self.minList = []

    def addAirport(self, airport):
        self.map[airport] = {}

    # Connections are assumed to be 2-way
    def addConnection(self, airport1, airport2, cost):
        self.map[airport1][airport2] = cost
        self.map[airport2][airport1] = cost

    # Implements Dijkstra's in order to minimize the cost of flying between airports
    # Returns a set of the airport path used and the total cost of flying that path
    def minCost(self, start, finish):
        visited = [start]
        cost = 0

        # All node weights are set to infinity to begin
        nodeWeights = {}
        for node in self.map:
            nodeWeights[node] = float('inf')
        nodeWeights[start] = 0

        # Alters nodeWeights as well as the visited list
        self.Dijkstras(start, finish, nodeWeights, visited)

        cost = nodeWeights[finish]

        return self.minList, cost

    # Recursive-backtracking solution for Dijkstras
    def Dijkstras(self, start, finish, nodeWeights, visited):
        # Go through all options from the start
        for airport in self.map[start]:
            visited.append(airport)
            if (self.evalPath(visited) < nodeWeights[airport]):
                nodeWeights[airport] = self.evalPath(visited)
                # Base case
                if (airport == finish):
                    self.minList = copy.copy(visited)
                else:
                    # Recursive case
                    self.Dijkstras(airport, finish, nodeWeights, visited)
            # Backtrack
            visited.pop()

    # Evaluates cost of a path
    def evalPath(self, path):
        cost = 0
        for node in range(1, len(path)):
            cost += self.map[path[node-1]][path[node]]
        return cost

# Test function for minimizing cost on an arbitrary map
def testDijkstras():
    print("Testing minCost()...", end = " ")
    airports = airportMap()
    airports.addAirport("a", (1, 1))
    airports.addAirport("b", (2, 2))
    airports.addAirport("c", (3, 3))
    airports.addAirport("d", (4, 4))
    airports.addAirport("e", (5, 5))
    airports.addAirport("f", (6, 6))
    airports.addAirport("g", (7, 7))
    airports.addConnection("a", "b", 1)
    airports.addConnection("b", "d", 3)
    airports.addConnection("b", "c", 5)
    airports.addConnection("b", "f", 11)
    airports.addConnection("d", "e", 4)
    airports.addConnection("c", "e", 8)
    airports.addConnection("c", "f", 5)
    airports.addConnection("e", "f", 12)
    airports.addConnection("f", "g", 1)
    assert(airports.minCost("a", "g") == ["a", "b", "c", "f", "g"], 12)
    print("Passed!")