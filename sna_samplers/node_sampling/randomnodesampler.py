import random
import networkx as nx
import networkit as nk
from typing import Union, List
from sna_samplers.sampler import Sampler


NKGraph = type(nk.graph.Graph())
NXGraph = nx.classes.graph.Graph


class RandomNodeSampler(Sampler):
    

    def __init__(self, number_of_nodes: int = 100, seed: int = 42):
        self.number_of_nodes = number_of_nodes
        self.seed = seed
        self._set_seed()

    def _create_initial_node_set(self, graph) -> List[int]:
        
        nodes = self.backend.get_nodes(graph)
        sampled_nodes = random.sample(nodes, self.number_of_nodes)
        return sampled_nodes

    def sample(self, graph: Union[NXGraph, NKGraph]) -> Union[NXGraph, NKGraph]:
        
        self._deploy_backend(graph)
        self._check_number_of_nodes(graph)
        sampled_nodes = self._create_initial_node_set(graph)
        new_graph = self.backend.get_subgraph(graph, sampled_nodes)
        return new_graph
