import networkx as nx
from typing import Dict
import pandas as pd
from pyvis.network import Network
import plotly.graph_objects as go

class Config:
    """
    Configuration class for setting default parameters for the correlation graph visualization.
    """
    AXIS_CONFIG = dict(showline=False, zeroline=False, showgrid=False, showticklabels=False, title='')
    LAYOUT_CONFIG = dict(
        title='<br>Correlation Graph',
        titlefont_size=16,
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        annotations=[dict(
            text="Visualization of the correlation graph",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.005, y=-0.002)],
        xaxis=AXIS_CONFIG,
        yaxis=AXIS_CONFIG,
        width=800,
        height=800
    )
    DEFAULT_NODE_SIZE = 10
    DEFAULT_EDGE_WIDTH = 0.01
    NODE_SIZE_SCALE = 20
    EDGE_WIDTH_SCALE = 1
    NEGATIVE_COLOR = 'orange'
    POSITIVE_COLOR = 'blue'
    FIGURE_SIZE = '800px'

class CorrGraph:
    """
    Class for creating and visualizing a correlation graph from a correlation matrix.
    """
    def __init__(self, corr_matrix: pd.DataFrame, threshold: float = 0.5, use_correlations_as_weights: bool = True) -> None:
        """
        Initialize the CorrGraph object.

        :param corr_matrix: A pandas DataFrame representing the correlation matrix.
        :param threshold: A float value to determine the minimum correlation value to consider an edge.
        :param use_correlations_as_weights: A boolean to decide if correlations should be used as edge weights.
        """
        self.corr_matrix: pd.DataFrame = corr_matrix
        self.threshold: float = threshold
        self.use_correlations_as_weights: bool = use_correlations_as_weights
        self.graph: nx.Graph = nx.Graph()
        self._create_graph()

    def _create_graph(self) -> None:
        """
        Create a graph from the correlation matrix based on the threshold and weight settings.
        """
        features = self.corr_matrix.columns
        num_features = len(features)
        for i in range(num_features):
            self.graph.add_node(features[i])
            for j in range(i + 1, num_features):
                if abs(self.corr_matrix.iloc[i, j]) >= self.threshold:
                    weight = self.corr_matrix.iloc[i, j]
                    self.graph.add_edge(features[i], features[j], weight=weight)

    def get_graph(self) -> nx.Graph:
        """
        Get the created graph.

        :return: A networkx Graph object representing the correlation graph.
        """
        return self.graph

    def update_node_weights(self, weights: Dict[str, float]) -> None:
        """
        Update the weights of the nodes in the graph.

        :param weights: A dictionary where keys are node names and values are the weights to be assigned.
        :raises ValueError: If a node is not found in the graph.
        :raises TypeError: If a weight is not numeric.
        """
        for node, weight in weights.items():
            if node not in self.graph:
                raise ValueError(f"Feature '{node}' not found in the graph.")
            if not isinstance(weight, (int, float)):
                raise TypeError(f"Weight for feature '{node}' must be numeric.")
            self.graph.nodes[node]['weight'] = weight

    def visualize_graph_with_plotly(self, node_weight_is_size: bool = True, edge_weight_is_size: bool = True) -> None:
        """
        Visualize the graph using Plotly.

        :param node_weight_is_size: A boolean to decide if node weights should determine node sizes.
        :param edge_weight_is_size: A boolean to decide if edge weights should determine edge widths.
        """
        pos = nx.spring_layout(self.graph)
        fig = go.Figure(layout=Config.LAYOUT_CONFIG)

        for edge in self.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x = [x0, x1, None]
            edge_y = [y0, y1, None]
            edge_width = self.graph.edges[edge].get('weight', Config.DEFAULT_EDGE_WIDTH) * Config.EDGE_WIDTH_SCALE if edge_weight_is_size else Config.DEFAULT_EDGE_WIDTH

            fig.add_trace(
                go.Scatter(
                    x=edge_x, y=edge_y,
                    line=dict(width=edge_width, color='#888'),
                    hoverinfo='none',
                    mode='lines',
                    text=f'{edge_width if edge_weight_is_size else "none"}',
                )
            )

        for node in self.graph.nodes():
            x, y = pos[node]
            node_text = f'{node}<br>Weight: {self.graph.nodes[node].get("weight", "N/A")}'
            node_size = abs(self.graph.nodes[node].get('weight', Config.DEFAULT_NODE_SIZE)) * Config.NODE_SIZE_SCALE if node_weight_is_size else Config.DEFAULT_NODE_SIZE
            node_color = Config.NEGATIVE_COLOR if self.graph.nodes[node].get('weight', 0) < 0 else Config.POSITIVE_COLOR

            fig.add_trace(
                go.Scatter(
                    x=[x],
                    y=[y],
                    mode='markers',
                    text=node_text,
                    textposition="top center",
                    hoverinfo='text',
                    marker=dict(
                        size=node_size,
                        color=node_color,
                        line_width=2)
                )
            )

        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode='markers',
                marker=dict(
                    size=Config.DEFAULT_NODE_SIZE,
                    color=Config.NEGATIVE_COLOR,
                ),
                legendgroup='Negative Weight',
                showlegend=True,
                name='Negative Weight'
            )
        )

        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode='markers',
                marker=dict(
                    size=Config.DEFAULT_NODE_SIZE,
                    color=Config.POSITIVE_COLOR,
                ),
                legendgroup='Positive Weight',
                showlegend=True,
                name='Positive Weight'
            )
        )

        fig.show()

    def visualize_graph_with_pyvis(self, node_weight_is_size: bool = True, edge_weight_is_size: bool = True, use_as_notebook = True) -> None:
        """
        Visualize the graph using PyVis.

        :param node_weight_is_size: A boolean to decide if node weights should determine node sizes.
        :param edge_weight_is_size: A boolean to decide if edge weights should determine edge widths.
        :param use_as_notebook: A boolean to decide if the visualization should be displayed in a Jupyter notebook.
        """
        net = Network(height=Config.FIGURE_SIZE, width=Config.FIGURE_SIZE, notebook=use_as_notebook)

        for node in self.graph.nodes():
            node_size = abs(self.graph.nodes[node].get('weight', Config.DEFAULT_NODE_SIZE)) * Config.NODE_SIZE_SCALE if node_weight_is_size else Config.DEFAULT_NODE_SIZE
            node_color = Config.NEGATIVE_COLOR if self.graph.nodes[node].get('weight', 0) < 0 else Config.POSITIVE_COLOR
            node_title = f'{node}\nWeight: {self.graph.nodes[node].get("weight", "N/A")}'
            net.add_node(node, label=node, size=node_size, color=node_color, title=node_title)

        for edge in self.graph.edges():
            edge_weight = self.graph.edges[edge].get('weight', Config.DEFAULT_EDGE_WIDTH)
            edge_width = edge_weight * Config.EDGE_WIDTH_SCALE if edge_weight_is_size else Config.DEFAULT_EDGE_WIDTH
            edge_title = f'Weight: {edge_weight}'
            
            if edge_weight < 0:
                edge_color = 'red'
            else:
                edge_color = 'green'
            # Determine edge color based on weight            
            if edge_weight_is_size:
                net.add_edge(edge[0], edge[1], value=edge_width, title=edge_title, color=edge_color)
            else:
                net.add_edge(edge[0], edge[1], title=edge_title, color=edge_color)

        net.show('correlation_graph.html')
