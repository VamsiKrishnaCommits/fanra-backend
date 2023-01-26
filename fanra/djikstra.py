from collections import defaultdict
import sys
import functools
from queue import Queue

from fanra.models import Relation

import pickle
import os



def find_shortest_relation_with_person(start_person, end_person):
    # Create a graph represented as a dictionary
    graph = build_graph()
    # Initialize the queue and visited set
    q = Queue()
    visited = set()
    q.put((start_person, []))
    visited.add(start_person)

    while not q.empty():
        current_person, path = q.get()
        if current_person == end_person:
            return [(start_person, None)] + path + [(end_person, None)]
        for neighbor, relation in graph[current_person]:
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = path + [(current_person, relation)]
                q.put((neighbor, new_path))

    return None


@functools.lru_cache()
def build_graph(force:bool = False):
    '''
    To be called with force set to True when you have relations and persons added 
    to the database and generate new graph altogether. Usually done by sshing into
    the pod.

    It defaults to reading from the file and returning a dictionary

    Make sure the file is always updated before pushing it to the production
    '''
    if not force :
        return read_graph_from_disk('graph.pickle')

    graph = defaultdict(list)
    relations = Relation.objects.all()
    for relation in relations:
        graph[relation.person1].append((relation.person2, relation.relation))
    write_graph_to_disk('graph.pickle', graph)
    return graph

def write_graph_to_disk(file_name , graph):

    with open(file_name, "wb") as f:
        pickle.dump(graph, f)

def read_graph_from_disk(file_name):

    with open(file_name, "rb") as f:
        graph = pickle.load(f)
    return graph
