
# Unimplemented features:
# - NPR: Would have to compute page ranks for all pages, very costly
# - LCC: Would have to compute edges of all neighbors, a bit costly, but doable if very needed

def compute_network_features(title, num_translations, graph_info = None):
    # Network features are costly to compute in real time because we need to build the graph
    # So if we want to use the network features, pass the graph_info to the function

    ft = {}

    if graph_info is None:
        return ft

    ft['NT'] = num_translations


    network_graph, neighbor_graph, graph_ids = graph_info
    graph_id = graph_ids[title]

    node = network_graph[graph_id]
    neighbors = list(set(node['in'] + node['out']))

    neighbor_avg_in = sum(neighbor_graph[n]['in_degree'] for n in neighbors) / len(neighbors) if len(neighbors) > 0 else 0
    neighbor_avg_out = sum(neighbor_graph[n]['out_degree'] for n in neighbors) / len(neighbors) if len(neighbors) > 0 else 0
    
    ft['NIN'] = len(node['in']) # In-degree
    ft['NOUT'] = len(node['out']) # Out-degree

    ft['NASSinin'] = ft['NIN'] / neighbor_avg_in if neighbor_avg_in > 0 else 0 # Assortativity in-in
    ft['NASSinout'] = ft['NIN'] / neighbor_avg_out if neighbor_avg_out > 0 else 0 # Assortativity in-out
    ft['NASSoutin'] = ft['NOUT'] / neighbor_avg_in if neighbor_avg_in > 0 else 0 # Assortativity out-in
    ft['NASSoutout'] = ft['NOUT'] / neighbor_avg_out if neighbor_avg_out > 0 else 0 # Assortativity out-out

    num_edges = len(node['in']) + len(node['out']) - node['num_reciprocal_edges']
    ft['NREP'] = node['num_reciprocal_edges'] / num_edges if num_edges > 0 else 0 # Reciprocity

    return ft
