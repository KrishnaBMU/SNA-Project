import random
import numpy as np
import networkx as nx
import networkit as nk
from typing import Union, List
from sna_samplers.sampler import Sampler

NKGraph = type(nk.graph.Graph())
NXGraph = nx.classes.graph.Graph


class PageRankBasedSampler(Sampler):
    

    def __init__(self, number_of_nodes: int = 100, seed: int = 42, alpha: float = 0.85):
        self.number_of_nodes = number_of_nodes
        self.seed = seed
        self.alpha = alpha
        self._set_seed()

    def _create_initial_node_set(self, graph) -> List[int]:
        
        nodes = [node for node in range(self.backend.get_number_of_nodes(graph))]
        page_rank = self.backend.get_pagerank(graph, self.alpha)
        page_rank_sum = np.sum(page_rank)
        probabilities = page_rank / page_rank_sum
        sampled_nodes = np.random.choice(
            nodes, size=self.number_of_nodes, replace=False, p=probabilities
        )
        return sampled_nodes

    def sample(self, graph: Union[NXGraph, NKGraph]) -> Union[NXGraph, NKGraph]:
        
        self._deploy_backend(graph)
        self._check_number_of_nodes(graph)
        sampled_nodes = self._create_initial_node_set(graph)
        new_graph = self.backend.get_subgraph(graph, sampled_nodes)
        return new_graph
