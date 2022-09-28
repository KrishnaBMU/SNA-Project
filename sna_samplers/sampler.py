import random
import numpy as np
import networkx as nx
import networkit as nk
from typing import Union
from sna_samplers.backend import NetworKitBackEnd
from sna_samplers.backend import NetworkXBackEnd


NKGraph = type(nk.graph.Graph())
NXGraph = nx.classes.graph.Graph


class Sampler(object):
    

    def __init__(self):
        
        pass

    def sample(self):
        
        pass

    def _set_seed(self):
        
        random.seed(self.seed)
        np.random.seed(self.seed)

    def _deploy_backend(self, graph: Union[NKGraph, NXGraph]):
        
        if isinstance(graph, NKGraph):
            self.backend = NetworKitBackEnd()
            self.backend.check_graph(graph)
        elif isinstance(graph, NXGraph):
            self.backend = NetworkXBackEnd()
            self.backend.check_graph(graph)
        else:
            raise ValueError("Not a NetworKit or NetworkX graph.")

    def _check_networkx_graph(self, graph):
        
        assert isinstance(
            graph, nx.classes.graph.Graph
        ), "This is not a NetworkX graph."

    def _check_directedness(self, graph):
        
        directed = nx.is_directed(graph)
        assert directed == False, "Graph is directed."

    def _check_indexing(self, graph):
        
        numeric_indices = [index for index in range(graph.number_of_nodes())]
        node_indices = sorted([node for node in graph.nodes()])
        assert numeric_indices == node_indices, "The node indexing is wrong."

    def _check_graph(self, graph: nx.classes.graph.Graph):
        
        self._check_networkx_graph(graph)
        self._check_directedness(graph)
        self._check_indexing(graph)

    def _check_number_of_nodes(self, graph):
        
        if self.number_of_nodes > self.backend.get_number_of_nodes(graph):
            raise ValueError(
                "The number of nodes is too large. Please see requirements."
            )

    def _check_number_of_edges(self, graph):
        
        if self.number_of_edges > self.backend.get_number_of_edges(graph):
            raise ValueError(
                "The number of edges is too large. Please see requirements."
            )
