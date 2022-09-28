import random
import numpy as np
import networkx as nx
import networkit as nk
from typing import List, Tuple


NKGraph = type(nk.graph.Graph())
NXGraph = nx.classes.graph.Graph


class NetworKitBackEnd(object):
    
    def __init__(self):
        pass

    def get_number_of_nodes(self, graph: NKGraph) -> int:
        
        return graph.numberOfNodes()


    def get_number_of_edges(self, graph: NKGraph) -> int:
        
        return graph.numberOfEdges()


    def get_nodes(self, graph: NKGraph) -> List:
        
        return graph.nodes()


    def get_edges(self, graph: NKGraph) -> List[Tuple]:
        
        return graph.edges()


    def get_node_iterator(self, graph: NKGraph):
        
        return graph.iterNodes()


    def get_edge_iterator(self, graph: NKGraph):
        
        return graph.iterEdges()


    def get_degree(self, graph: NKGraph, node: int) -> int:
        
        return graph.degree(node)


    def get_subgraph(self, graph: NKGraph, nodes: List[int]) -> NKGraph:
        
        return graph.subgraphFromNodes(nodes)


    def get_neighbors(self, graph: NKGraph, node: int) -> List[int]:
        
        return graph.neighbors(node)


    def get_random_neighbor(self, graph: NKGraph, node: int) -> int:
        
        return graph.randomNeighbor(node)


    def get_shortest_path(self, graph: NKGraph, source: int, target: int) -> List[int]:
        
        return nk.distance.ReverseBFS(graph, source, True, False, target).run().getPath(target)


    def get_pagerank(self, graph: NKGraph, alpha: float) -> np.array:
        
        pagerank = nk.centrality.PageRank(graph, alpha)
        pagerank.run()
        pagerank = np.array(pagerank.scores())
        pagerank = pagerank / pagerank.sum()
        return pagerank

    def is_weighted(self, graph: NKGraph) -> bool:
        return graph.isWeighted()

    def get_edge_weight(self, graph: NKGraph, u: int, v: int) -> float:
        return graph.weight(u, v)

    def graph_from_edgelist(self, edges: List) -> NKGraph:
        
        new_graph = nk.graph.Graph(directed=False)
        for edge in edges:
            new_graph.addEdge(edge[0], edge[1], addMissing=True)
        return new_graph


    def _check_networkit_graph(self, graph: NKGraph):
        
        assert isinstance(graph, NKGraph), "This is not a NetworKit graph."


    def _check_connectivity(self, graph: NKGraph):
        
        connected = nk.components.ConnectedComponents(graph).run().numberOfComponents()
        assert connected == 1, "Graph is not connected."


    def _check_directedness(self, graph: NXGraph):
        
        directed = graph.isDirected()
        assert directed == False, "Graph is directed."


    def _check_indexing(self, graph: NKGraph):
        
        numeric_indices = [index for index in range(graph.numberOfNodes())]
        node_indices = sorted([node for node in graph.nodes()])
        assert numeric_indices == node_indices, "The node indexing is wrong."


    def check_graph(self, graph: NKGraph):
        
        self._check_networkit_graph(graph)
        self._check_directedness(graph)
        self._check_indexing(graph)


class NetworkXBackEnd(object):
    
    def __init__(self):
        pass


    def get_number_of_nodes(self, graph: NXGraph) -> int:
        
        return graph.number_of_nodes()


    def get_number_of_edges(self, graph: NXGraph) -> int:
        
        return graph.number_of_edges()


    def get_nodes(self, graph: NXGraph) -> List:
        
        return [node for node in graph.nodes()]


    def get_edges(self, graph: NXGraph) -> List[Tuple]:
        
        return [edge for edge in graph.edges()]


    def get_node_iterator(self, graph: NXGraph):
        
        return graph.nodes()


    def get_edge_iterator(self, graph: NXGraph):
        
        return graph.edges()


    def get_degree(self, graph: NXGraph, node: int) -> int:
        
        return graph.degree[node]


    def get_subgraph(self, graph: NXGraph, nodes: List[int]) -> NXGraph:
        
        return graph.subgraph(nodes)


    def get_neighbors(self, graph: NXGraph, node: int) -> List[int]:
        
        return [node for node in graph.neighbors(node)]


    def get_random_neighbor(self, graph: NXGraph, node: int) -> int:
        
        neighbors = self.get_neighbors(graph, node)
        return random.choice(neighbors)


    def get_shortest_path(self, graph: NXGraph, source: int, target: int) -> List[int]:
        
        return nx.shortest_path(graph, source, target)


    def get_pagerank(self, graph: NXGraph, alpha: float) -> np.array:
        
        pagerank = nx.pagerank_scipy(graph, alpha=alpha)
        pagerank = np.array([pagerank[node] for node in graph.nodes()])
        pagerank = pagerank / pagerank.sum()
        return pagerank

    def is_weighted(self, graph: NXGraph) -> bool:
        return nx.is_weighted(graph)

    def get_edge_weight(self, graph: NXGraph, u: int, v: int) -> float:
        return graph.get_edge_data(u, v)['weight']

    def graph_from_edgelist(self, edges: List) -> NXGraph:
        
        graph = nx.from_edgelist(edges)
        return graph


    def _check_networkx_graph(self, graph: NXGraph):
        
        assert isinstance(graph, NXGraph), "This is not a NetworkX graph."


    def _check_connectivity(self, graph: NXGraph):
        
        connected = nx.is_connected(graph)
        assert connected, "Graph is not connected."


    def _check_directedness(self, graph: NXGraph):
        
        directed = nx.is_directed(graph)
        assert directed == False, "Graph is directed."


    def _check_indexing(self, graph: NXGraph):
        
        numeric_indices = [index for index in range(graph.number_of_nodes())]
        node_indices = sorted([node for node in graph.nodes()])
        assert numeric_indices == node_indices, "The node indexing is wrong."


    def check_graph(self, graph: NXGraph):
        
        self._check_networkx_graph(graph)
        self._check_directedness(graph)
        self._check_indexing(graph)