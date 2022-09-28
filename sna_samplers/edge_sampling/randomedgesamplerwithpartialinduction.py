import random
import networkx as nx
import networkit as nk
from typing import Union
from sna_samplers import Sampler


NKGraph = type(nk.graph.Graph())
NXGraph = nx.classes.graph.Graph


class RandomEdgeSamplerWithPartialInduction(Sampler):
    

    def __init__(self, p: float = 0.5, seed: int = 42):
        self.p = p
        self.seed = seed
        self._set_seed()

    def _create_initial_set(self, graph):
        
        self._nodes = set()
        self._edges = set()
        self._edge_stream = self.backend.get_edges(graph)
        random.shuffle(self._edge_stream)

    def _insert_edge(self, edge):
        
        self._edges.add((edge[0], edge[1]))
        self._edges.add((edge[1], edge[0]))

    def _insert_nodes(self, edge):
        
        self._nodes.add(edge[0])
        self._nodes.add(edge[1])

    def _sample_edges(self):
        
        for edge in self._edge_stream:
            if edge[0] in self._nodes and edge[1] in self._nodes:
                self._insert_edge(edge)
            else:
                p = random.uniform(0, 1)
                if p < self.p:
                    self._insert_nodes(edge)
                    self._insert_edge(edge)
        self._edges = [edge for edge in self._edges]

    def sample(self, graph: Union[NXGraph, NKGraph]) -> Union[NXGraph, NKGraph]:
        
        self._deploy_backend(graph)
        self._create_initial_set(graph)
        self._sample_edges()
        new_graph = self.backend.graph_from_edgelist(self._edges)
        return new_graph
