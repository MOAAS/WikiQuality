import it.unimi.dsi.webgraph.ImmutableGraph;
import it.unimi.dsi.webgraph.BVGraph;
import it.unimi.dsi.webgraph.LazyIntIterator;
import it.unimi.dsi.webgraph.NodeIterator;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;



public class GraphParser {
    private static ImmutableGraph load() {
        try {
            BVGraph graph =  BVGraph.loadOffline("src/main/resources/enwiki-2022");
            System.out.println("Loaded graph with " + graph.numNodes() + " nodes and " + graph.numArcs() + " arcs.");
            return graph;
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
    private static Map<Integer, String> loadTitles() {
        Map<Integer, String> ids = new HashMap<>();
        int currentId = 0;
        try (BufferedReader br = new BufferedReader(new FileReader("src/main/resources/enwiki-2022.ids"))) {
            String line;
            while ((line = br.readLine()) != null) {
                ids.put(currentId, line);
                currentId++;
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        System.out.println("Loaded " + currentId + " ids.");

        return ids;
    }

    public static void main(String[] args) throws IOException {
        ImmutableGraph graph = load();
        Map<Integer, String> titles = loadTitles();

        NodeIterator nodeIterator = graph.nodeIterator();

        int count = 0;
        int numNeighbors = 0;

        String separator = "|";

        try (
            FileWriter nodes = new FileWriter("src/main/resources/enwiki-2022-nodes.csv");
            FileWriter edges = new FileWriter("src/main/resources/enwiki-2022-edges.csv")
        ) {
            nodes.write("id" + separator + "title\n");
            edges.write("source" + separator + "target\n");
            while (nodeIterator.hasNext()) {
                int node = nodeIterator.nextInt();

                String title = titles.get(node); //.replaceAll("\\\\", "%5C"); // replace backslashes with %5C

                nodes.write(node + separator + title + "\n");

                LazyIntIterator neighbors = nodeIterator.successors();

                int neighbor = 0;
                while ((neighbor = neighbors.nextInt()) != -1) {
                    edges.write(node + separator + neighbor + "\n");
                    numNeighbors++;
                }

                count++;
            }
        }

        System.out.printf("Neighbors: %d\n",  numNeighbors);
        System.out.printf("Count: %d\n", count);
    }
}
