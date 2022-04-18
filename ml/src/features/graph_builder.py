import time


edge_file = 'ml/wikidumps/enwiki-2021-edges.csv'
node_file = 'ml/wikidumps/enwiki-2021-nodes.csv'
csv_sep = '_'

def update_params(nf, ef, sep):
    global node_file, edge_file, csv_sep
    node_file = nf
    edge_file = ef
    csv_sep = sep

def build_graph(titles):
    if len(titles) == 0:
        return {}, {}, {}

    start_time = time.time()
    main_graph = {}

    print("Building network graph...")
    with open(node_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('id'): # first line
                continue

            [id, title] = line.strip().split(csv_sep)
            if title in titles:
                main_graph[id] = { 'title': title, 'out': [], 'in': [], 'num_reciprocal_edges': 0 }
                
    with open(edge_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('source'): # first line
                continue

            [source, target] = line.strip().split(csv_sep) # should we ignore if source == target?

            if source in main_graph:
                main_graph[source]['out'].append(target)

            if target in main_graph:
                main_graph[target]['in'].append(source)

    all_neighbors = set()

    # for every graph element, remove duplicate neighbors, also join all neighbors to set
    for id in main_graph:
        unique_in = set(main_graph[id]['in'])
        unique_out = set(main_graph[id]['out'])
        main_graph[id]['in'] = list(unique_in)
        main_graph[id]['out'] = list(unique_out)
        all_neighbors = all_neighbors.union(unique_in).union(unique_out)

    # Now make the graph with neighbors ( we only need in/out degree )
    neighbor_graph = {}
    for neighbor in all_neighbors:
        neighbor_graph[neighbor] = { 'in_degree': 0, 'out_degree': 0 }

    with open(edge_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('source'): # first line
                continue

            [source, target] = line.strip().split(csv_sep)
            if source in neighbor_graph:
                neighbor_graph[source]['out_degree'] += 1

                # Check if reversed edge already existed in the graph. If there's a reciprocal, 
                #   both edges will already be present in the main graph, so we just need to do the check once.
                if target in main_graph and source in main_graph[target]['out']:
                    main_graph[target]['num_reciprocal_edges'] += 1

            if target in neighbor_graph:
                neighbor_graph[target]['in_degree'] += 1

    # make map from title to id
    graph_ids = {}
    for id in main_graph:
        graph_ids[main_graph[id]['title']] = id

    print(f'Completely built article graph ({len(main_graph)}/{len(titles)} titles found). Time elapsed: {time.time() - start_time:.2f} seconds.')

    return main_graph, neighbor_graph, graph_ids

        
import unittest

class TestBuilder(unittest.TestCase):
    
    def test_graphbuilder(self):
        update_params('ml/test/graphbuilder/nodes1.csv', 'ml/test/graphbuilder/edges1.csv', ',')
        
        graph, neighbors, graph_ids = build_graph(["A"])

        self.assertEqual(graph_ids['A'], '1')
        self.assertEqual(graph['1']['title'], 'A')
        self.assertEqual(set(graph['1']['out']), set(['3','2','5']))
        self.assertEqual(set(graph['1']['in']), set(['4','2']))
        self.assertEqual(graph['1']['num_reciprocal_edges'], 1)

        self.assertEqual(neighbors['5']['in_degree'], 2)

        graph, _, graph_ids = build_graph(["A", "B", "C", "D", "E"])

        self.assertEqual(graph['1']['num_reciprocal_edges'], 1)
        self.assertEqual(graph['2']['num_reciprocal_edges'], 1)
        self.assertEqual(graph['3']['num_reciprocal_edges'], 0)
        self.assertEqual(graph['4']['num_reciprocal_edges'], 1)
        self.assertEqual(graph['5']['num_reciprocal_edges'], 1)

        return

if __name__ == '__main__':
    unittest.main()