import unittest
import pandas as pd
import networkx as nx
from corrGraph.corrGraph import CorrGraph

class TestCorrGraph(unittest.TestCase):

    def setUp(self):
        # Create a sample correlation matrix
        data = {
            'A': [1.0, 0.8, 0.7],
            'B': [0.8, 1.0, 0.4],
            'C': [0.7, 0.4, 1.0]
        }
        self.corr_matrix = pd.DataFrame(data, index=['A', 'B', 'C'])
        self.corr_graph = CorrGraph(self.corr_matrix, threshold=0.5)

    def test_graph_creation(self):
        graph = self.corr_graph.get_graph()
        self.assertIsInstance(graph, nx.Graph)
        self.assertEqual(len(graph.nodes), 3)
        self.assertEqual(len(graph.edges), 2)

    def test_update_node_weights(self):
        weights = {'A': 1.5, 'B': -0.5, 'C': 2.0}
        self.corr_graph.update_node_weights(weights)
        graph = self.corr_graph.get_graph()
        self.assertEqual(graph.nodes['A']['weight'], 1.5)
        self.assertEqual(graph.nodes['B']['weight'], -0.5)
        self.assertEqual(graph.nodes['C']['weight'], 2.0)

    def test_update_node_weights_invalid_node(self):
        weights = {'D': 1.5}
        with self.assertRaises(ValueError):
            self.corr_graph.update_node_weights(weights)

    def test_update_node_weights_invalid_weight(self):
        weights = {'A': 'invalid'}
        with self.assertRaises(TypeError):
            self.corr_graph.update_node_weights(weights)

    def test_visualize_graph_with_plotly(self):
        try:
            self.corr_graph.visualize_graph_with_plotly()
        except Exception as e:
            self.fail(f"visualize_graph_with_plotly() raised {e.__class__.__name__} unexpectedly!")

    def test_visualize_graph_with_pyvis(self):
        try:
            self.corr_graph.visualize_graph_with_pyvis(use_as_notebook=False)
        except Exception as e:
            self.fail(f"visualize_graph_with_pyvis() raised {e.__class__.__name__} unexpectedly!")

if __name__ == '__main__':
    unittest.main()