import random
import networkx as nx
import networkit as nk
from typing import Union
from sna_samplers.sampler import Sampler

NKGraph = type(nk.graph.Graph())
NXGraph = nx.classes.graph.Graph


class RandomWalkWithJumpSampler(Sampler):
    

    def __init__(self, number_of_nodes: int = 100, seed: int = 42, p: float = 0.1):
        self.number_of_nodes = number_of_nodes
        self.seed = seed
        self.p = p
        self._set_seed()

    def _create_initial_node_set(self, graph, start_node):
        
        if start_node is not None:
            if start_node >= 0 and start_node < self.backend.get_number_of_nodes(graph):
                self._current_node = start_node
                self._sampled_nodes = set([self._current_node])
            else:
                raise ValueError("Starting node index is out of range.")
        else:
            self._current_node = random.choice(
                range(self.backend.get_number_of_nodes(graph))
            )
            self._sampled_nodes = set([self._current_node])

    def _do_a_step(self, graph):
        
        score = random.uniform(0, 1)
        if score < self.p:
            self._current_node = random.choice(
                range(self.backend.get_number_of_nodes(graph))
            )
        else:
            self._current_node = self.backend.get_random_neighbor(
                graph, self._current_node
            )
        self._sampled_nodes.add(self._current_node)

    def sample(
        self, graph: Union[NXGraph, NKGraph], start_node: int = None
    ) -> Union[NXGraph, NKGraph]:
        
        self._deploy_backend(graph)
        self._check_number_of_nodes(graph)
        self._create_initial_node_set(graph, start_node)
        while len(self._sampled_nodes) < self.number_of_nodes:
            self._do_a_step(graph)
        new_graph = self.backend.get_subgraph(graph, self._sampled_nodes)
        return new_graph
