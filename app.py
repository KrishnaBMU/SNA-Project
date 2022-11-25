import networkx as nx
from sna_samplers import *
import matplotlib.pyplot as plt
from sna_samplers.exploration_sampling.shortest_path import ShortestPathSampler


def PlotDiffusionSampler(graph):
    sampler = DiffusionSampler()
    return sampler.sample(graph)

def PlotRandomEdgeSampler(graph):
    sampler = RandomEdgeSampler()
    return sampler.sample(graph)

def PlotRandomNodeSampler(graph):
    sampler = RandomNodeSampler()
    return sampler.sample(graph)

def PlotRandomWalkSampler(graph):
    sampler = RandomWalkSampler()
    return sampler.sample(graph)

def PlotShortestPathSampler(graph):
    sampler = ShortestPathSampler()
    return sampler.sample(graph)

# reader = GraphReader("wikipedia")
# graph = reader.get_graph()
graph = nx.newman_watts_strogatz_graph(1000, 20, 0.05)

# new_graph = PlotDiffusionSampler(graph)
# new_graph = PlotRandomEdgeSampler(graph)
# new_graph = PlotRandomNodeSampler(graph)
# new_graph = PlotRandomWalkSampler(graph)
new_graph = PlotShortestPathSampler(graph)

nx.draw(new_graph,with_labels=True)
plt.show()