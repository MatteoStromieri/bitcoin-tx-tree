import networkx as nx
import transaction
import matplotlib.pyplot as plt
import matplotlib


def add_edges(graph, node, parent=None):
    if isinstance(node.root, transaction.SegWitTx):
        color = 'red'
    else:
        color = 'blue'
    if node.root.isCoinbase():
        linewidth = 5
    else:
        linewidth = 1
    graph.add_node(node, label = node.root.id, color = color, linewidth = linewidth)
    if parent is not None:
        graph.add_edge(node, parent)
    for child in node.children:
        add_edges(graph, child, node)

def build_nx_tree(tree_root):
    graph = nx.DiGraph()
    add_edges(graph, tree_root)
    return graph

def visualize_tree(nx_tree):
    pos = nx.drawing.nx_agraph.graphviz_layout(nx_tree, prog='dot')
    pos = {node: (x, -y) for node, (x, y) in pos.items()}
    labels = nx.get_node_attributes(nx_tree, 'label')
    colors = nx.get_node_attributes(nx_tree, 'color')
    border_thicknesses = nx.get_node_attributes(nx_tree, 'linewidth')

    colors = [colors[node] for node in nx_tree.nodes()]
    border_thicknesses = [border_thicknesses[node] for node in nx_tree.nodes()]

    nx.draw(nx_tree, pos, with_labels=True, labels=labels, linewidths=border_thicknesses, node_size=5000, node_color=colors, edgecolors='black',  font_size=10)
    plt.show()

if __name__=="__main__":
    matplotlib.use('TkAgg')
    g = nx.bull_graph()
    visualize_tree(g)