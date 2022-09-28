import networkx as nx
import networkit as nk
from typing import Union, List
from sna_samplers.edge_sampling import RandomEdgeSampler


NKGraph = type(nk.graph.Graph())
NXGraph = nx.classes.graph.Graph


class RandomEdgeSamplerWithInduction(RandomEdgeSampler):
    

    def __init__(self, number_of_edges: int = 100, seed: int = 42):
        self.number_of_edges = number_of_edges
        self.seed = seed
        self._set_seed()

    def _induce_graph(self, graph) -> Union[NXGraph, NKGraph]:
        
        nodes = set([node for edge in self._sampled_edges for node in edge])
        new_graph = self.backend.get_subgraph(graph, nodes)
        return new_graph

    def sample(self, graph: Union[NXGraph, NKGraph]) -> Union[NXGraph, NKGraph]:
        
        self._deploy_backend(graph)
        self._check_number_of_edges(graph)
        self._create_initial_edge_set(graph)
        new_graph = self._induce_graph(graph)
        return new_graph
