
# Unimplemented features:
# - NPR: Would have to compute page ranks for all pages, very costly
# - LCC: Would have to compute edges of all neighbors, a bit costly, but doable if very needed

NETWORK_FEATURES = ['NIN', 'NOUT', 'NASSinin', 'NASSinout', 'NASSoutin', 'NASSoutout', 'NREP', 'NT']

def compute_network_features(graph_id, network_graph, neighbor_graph, num_translations):

    ft = {}

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
    ft['NT'] = num_translations

    return ft
