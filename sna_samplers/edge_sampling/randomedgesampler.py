import random
import networkx as nx
import networkit as nk
from typing import Union, List
from sna_samplers.sampler import Sampler

NKGraph = type(nk.graph.Graph())
NXGraph = nx.classes.graph.Graph


class RandomEdgeSampler(Sampler):
    def __init__(self, number_of_edges: int = 100, seed: int = 42):
        self.number_of_edges = number_of_edges
        self.seed = seed
        self._set_seed()

    def _create_initial_edge_set(self, graph):
        
        edges = self.backend.get_edges(graph)
        self._sampled_edges = random.sample(edges, self.number_of_edges)

    def sample(self, graph: Union[NXGraph, NKGraph]) -> Union[NXGraph, NKGraph]:
        self._deploy_backend(graph)
        self._check_number_of_edges(graph)
        self._create_initial_edge_set(graph)
        new_graph = self.backend.graph_from_edgelist(self._sampled_edges)
        return new_graph
