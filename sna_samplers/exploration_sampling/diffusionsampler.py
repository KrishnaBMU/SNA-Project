import random
import networkx as nx
import networkit as nk
from typing import Union
from sna_samplers.sampler import Sampler


NKGraph = type(nk.graph.Graph())
NXGraph = nx.classes.graph.Graph


class DiffusionSampler(Sampler):
    

    def __init__(self, number_of_nodes: int = 100, seed: int = 42):
        self.number_of_nodes = number_of_nodes
        self.seed = seed
        self._set_seed()

    def _create_initial_node_set(self, graph, start_node):
        
        self._sampled_edges = []
        if start_node is not None:
            if start_node >= 0 and start_node < self.backend.get_number_of_nodes(graph):
                self._sampled_nodes = set([start_node])
            else:
                raise ValueError("Starting node index is out of range.")
        else:
            node = random.choice(range(self.backend.get_number_of_nodes(graph)))
            self._sampled_nodes = set([node])

    def _do_a_step(self, graph):
        
        source_node = random.sample(self._sampled_nodes, 1)[0]
        neighbor = self.backend.get_random_neighbor(graph, source_node)
        if neighbor not in self._sampled_nodes:
            self._sampled_nodes.add(neighbor)
            self._sampled_edges.append([source_node, neighbor])
            self._sampled_edges.append([neighbor, source_node])

    def sample(
        self, graph: Union[NXGraph, NKGraph], start_node: int = None
    ) -> Union[NXGraph, NKGraph]:
        
        self._deploy_backend(graph)
        self._check_number_of_nodes(graph)
        self._create_initial_node_set(graph, start_node)
        while len(self._sampled_nodes) < self.number_of_nodes:
            self._do_a_step(graph)
        new_graph = self.backend.get_subgraph(graph, list(self._sampled_nodes))
        return new_graph
