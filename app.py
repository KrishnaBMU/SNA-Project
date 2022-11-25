import networkx as nx
from sna_samplers import *
import matplotlib.pyplot as plt
from scipy import stats

# metrics
def RelativeError(graph, new_graph):
    acc = nx.average_clustering(graph)
    accn = nx.average_clustering(new_graph)
    return abs(acc-accn)/acc

def RootMeanSquare(graph, new_graph):
    cc = nx.clustering(graph)
    ccn = nx.clustering(new_graph)
    temp = 0
    for n in ccn.keys():
        temp += (cc[n] - ccn[n])**2
    temp = (temp/len(ccn))**(1/2)
    return temp

def KSTest(graph, new_graph):
    dd = nx.degree(graph)
    ddn = nx.degree(new_graph)
    ddl, ddln= [],[]
    for i in dd:
        ddl.append(i[1])
    for i in ddn:
        ddln.append(i[1])
    size = max(max(dd,key=lambda x:x[1]),max(dd,key=lambda x:x[1]))[1]
    temp = [0 for i in range(size+1)]
    tempn = [0 for i in range(size+1)]
    for i in range(size+1):
        temp[i] = ddl.count(i)
    for i in range(size+1):
        tempn[i] = ddln.count(i)
    return stats.kstest(temp,tempn).statistic


def print_stats(graph, new_graph):
    print("RE: ", RelativeError(graph,new_graph))
    print("RMS: ", RootMeanSquare(graph,new_graph))
    print("KSTest: ", KSTest(graph,new_graph))


def PlotDiffusionSampler(graph):
    sampler = DiffusionSampler()
    new_graph = sampler.sample(graph)
    print_stats(graph, new_graph)
    return new_graph

def PlotRandomEdgeSampler(graph):
    sampler = RandomEdgeSampler()
    new_graph = sampler.sample(graph)
    print_stats(graph, new_graph)
    return new_graph

def PlotRandomNodeSampler(graph):
    sampler = RandomNodeSampler()
    new_graph = sampler.sample(graph)
    print_stats(graph, new_graph)
    return new_graph

def PlotRandomWalkSampler(graph):
    sampler = RandomWalkSampler()
    new_graph = sampler.sample(graph)
    print_stats(graph, new_graph)
    return new_graph

def PlotShortestPathSampler(graph):
    sampler = ShortestPathSampler()
    new_graph = sampler.sample(graph)
    print_stats(graph, new_graph)
    return new_graph

def PlotShortestPathModifiedSampler(graph):
    sampler = ShortestPathModifiedSampler()
    new_graph = sampler.sample(graph)
    print_stats(graph, new_graph)
    return new_graph

# reader = GraphReader("wikipedia")
# graph = reader.get_graph()
graph = nx.newman_watts_strogatz_graph(1000, 20, 0.05)

# new_graph = PlotDiffusionSampler(graph)
# new_graph = PlotRandomEdgeSampler(graph)
# new_graph = PlotRandomNodeSampler(graph)
# new_graph = PlotRandomWalkSampler(graph)
# new_graph = PlotShortestPathSampler(graph)
new_graph = PlotShortestPathModifiedSampler(graph)

# nx.draw(new_graph,with_labels=True)
# plt.show()