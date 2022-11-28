import random
import networkx as nx
import networkit as nk
from typing import Union
from sna_samplers.sampler import Sampler


NKGraph = type(nk.graph.Graph())
NXGraph = nx.classes.graph.Graph

# node choosed based on degree
class ShortestPathModifiedSampler(Sampler):
    def __init__(self, number_of_nodes: int = 100, seed: int = 42):
        self.number_of_nodes = number_of_nodes
        self.seed = seed
        self.degrees = []
        self._set_seed()

    def _set_seed_set(self):
        self._nodes = set()

    def _sample_a_node(self, graph):
        return random.choice(range(self.backend.get_number_of_nodes(graph)))
    
    def _sample_a_node_highest(self,graph):
        self.highest_index += 1
        return self.degrees[self.highest_index]
    
    def _sample_a_node_lowest(self,graph):
        self.lowest_index -= 1
        return self.degrees[self.lowest_index]

    def _sample_a_pair(self, graph):
        source = self._sample_a_node_highest(graph)
        target = self._sample_a_node_highest(graph)
        return source, target

    def sample(self, graph: Union[NXGraph, NKGraph]) -> Union[NXGraph, NKGraph]:
        c = nx.clustering(graph) # clustering
        self.degrees = [node for (node, _) in sorted(graph.degree(), key=lambda x: c[x[0]], reverse=True)]
        self.highest_index = -1
        self.lowest_index = len(self.degrees)
        
        self._deploy_backend(graph)
        self._set_seed_set()
        while len(self._nodes) < self.number_of_nodes:
            source, target = self._sample_a_pair(graph)
            if source != target:
                path = self.backend.get_shortest_path(graph, source, target)
                for node in path:
                    self._nodes.add(node)
                    if len(self._nodes) >= self.number_of_nodes:
                        break

        new_graph = self.backend.get_subgraph(graph, self._nodes)
        return new_graph