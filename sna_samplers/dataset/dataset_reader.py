import io
import os
import numpy as np
import pandas as pd
import networkx as nx
from six.moves import urllib


class GraphReader(object):
    def __init__(self, dataset: str = "wikipedia"):
        self.dataset = dataset + "_edges.csv"
        self.base_path = (
            "./dataset"
        )

    def _pandas_reader(self, path):
        tab = pd.read_csv(
            path, encoding="utf8", sep=",", dtype={"switch": np.int32}
        )
        return tab

    def _dataset_reader(self):
        path = os.path.join(self.base_path, self.dataset)
        data = self._pandas_reader(path)
        return data

    def get_graph(self) -> nx.classes.graph.Graph:
        data = self._dataset_reader()
        graph = nx.convert_matrix.from_pandas_edgelist(data, "id_1", "id_2")
        return graph
