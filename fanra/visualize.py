import networkx as nx
import matplotlib.pyplot as plt
from numpy import greater
from fanra.models import Relation
from pyvis.network import Network


class Visualize:
    def show(self):
        relations = Relation.objects.all()
        graph = GraphVisualization()
        for relation in relations:
            graph.addEdge(relation.person1.name, relation.person2.name)

        graph.visualize()


class GraphVisualization:
    def __init__(self):

        # visual is a list which stores all
        # the set of edges that constitutes a
        # graph
        self.visual = []

    # addEdge function inputs the vertices of an
    # edge and appends it to the visual list
    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)

    # In visualize function G is an object of
    # class Graph given by networkx G.add_edges_from(visual)
    # creates a graph with a given list
    # nx.draw_networkx(G) - plots the graph
    # plt.show() - displays the graph
    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)

        nx.draw_networkx(G)
        nt = Network("500px", "500px")
        nt.from_nx(G)
        nt.show("nx.html")
