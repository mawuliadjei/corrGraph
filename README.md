# corrGraph
A python module built using graph theory to analyse how attributes/features in a dataset correlate with each other

## Project Goal

The goal of this project is to provide a comprehensive tool for analyzing the correlation between different attributes or features within a dataset using graph theory. By leveraging the capabilities of graph theory, this module aims to offer insightful visualizations and metrics that can help in understanding the relationships and dependencies among various features.

### Features

- **Graph Construction**: Build graphs where nodes represent features and edges represent the correlation between them.
- **Correlation Metrics**: Calculate various correlation metrics to quantify the strength and direction of relationships.
- **Visualization**: Generate visual representations of the correlation graph to easily identify clusters and key relationships.
- **Usability**: Simple and intuitive API for integrating with other data analysis workflows.

### Usage

Refer to the `corrGraph_usages` file for detailed examples and use cases demonstrating how to utilize the module effectively.

### Installation

To install the module, run:
```bash
pip install corrGraph
```

### Getting Started

Here's a quick example to get you started:
```python
from corrGraph import CorrGraph

# Load your dataset
data = pd.read_csv('some_data.csv')

# Initialize the CorrGraph object with a pandas correlation matrix
cg = CorrGraph(data.corr())

# Build the correlation graph
cg.get_graph()

# Visualize the graph
cg.visualize_graph()
```