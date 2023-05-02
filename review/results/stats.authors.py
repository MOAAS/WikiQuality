
import networkx as nx
import matplotlib.pyplot as plt
from csvs.loader import inclusion_but_with_more as papers
import random
import helpers.plot_saver as plotsaver


# create a graph
G = nx.Graph()

# add nodes
for paper in papers:
    authors = paper['Authors'].split('; ')
    for author in authors:
        G.add_node(author)

# add edges
for paper in papers:
    authors = paper['Authors'].split('; ')
    for author1 in authors:
        for author2 in authors:
            if author1 != author2:
                G.add_edge(author1, author2)

components = nx.connected_components(G)

# create a new graph with only the big components (more than 4 nodes)
components = [c for c in components if len(c) > 8]
G = G.subgraph([node for component in components for node in component])


# draw the graph, each connected component is a different color
pos = nx.spring_layout(G, k=0.7, iterations=100)
plt.figure(figsize=(9, 9))


for i, component in enumerate(components):
    node_color = '#%06X' % random.randint(0, 0xFFFFFF)
    nx.draw_networkx_nodes(G, pos, nodelist=component, node_size=25, node_color=node_color)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(component), width=1, alpha=0.5, edge_color=node_color)

# a little bit above the node (pos is a dict with: { key: [x, y]})
nx.draw_networkx_labels(G, {key: [x, y + 0.02] for key, [x, y] in pos.items()}, font_size=5)

plt.gca().spines['bottom'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plotsaver.show_and_save(plt, 'results/charts/coauthorship.pdf', size=(9, 9))




# print some stats
print('Number of nodes: ' + str(G.number_of_nodes()))
print('Number of edges: ' + str(G.number_of_edges()))
print('Number of connected components: ' + str(nx.number_connected_components(G)))