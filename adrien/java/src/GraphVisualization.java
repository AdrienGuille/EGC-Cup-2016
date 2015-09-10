
import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import org.apache.commons.io.FileUtils;
import static org.graphstream.algorithm.Toolkit.averageClusteringCoefficient;
import static org.graphstream.algorithm.Toolkit.degreeDistribution;
import org.graphstream.graph.Graph;
import org.graphstream.graph.Node;
import org.graphstream.graph.implementations.DefaultGraph;

/**
 *
 *   @author Adrien GUILLE, ERIC Lab, University of Lyon 2
 *   @email adrien.guille@univ-lyon2.fr
 */
public class GraphVisualization {
    Graph graph;
    
    public GraphVisualization(String source) throws IOException, InterruptedException{
        graph = new DefaultGraph("");
        graph.addAttribute("ui.quality");
        graph.addAttribute("ui.antialias");
        String css = ""
            + "graph { fill-mode: plain; fill-color : #f4f4f4;}"
            + "edge  { fill-mode: plain; fill-color: rgba(0,0,0,85); size:0.25px; z-index: 1;}" 
            + "node  { fill-mode: dyn-plain; fill-color: burlywood,cadetblue,chocolate,cornflowerblue,cornsilk,crimson,brown,aqua,aquamarine,black,blueviolet,chartreuse,dodgerblue,forestgreen,darkseagreen; size-mode: dyn-size; size: 3px ;z-index : 2; stroke-mode: plain;}"
            + "node:clicked   { fill-color: black;}";
        graph.addAttribute("ui.stylesheet", css);
        List<String> lines = FileUtils.readLines(new File(source));
        List<List<String>> topics = new LinkedList<>();
        HashSet<String> vocabulary = new HashSet<>();
        graph.display();
        for(int t = 0; t < lines.size(); t++){
            String line = lines.get(t);
            String[] desc = line.split(" ");
            List<String> words = new LinkedList();
            for(int i = 0; i <= desc.length-2; i = i+2){
                String word = desc[i];
                words.add(word);
                vocabulary.add(word);
                double probability = Double.parseDouble(desc[i+1]);
                if(graph.getNode(word) == null){
                    graph.addNode(word);
                    graph.getNode(word).addAttribute("ui.label", word);
                    graph.getNode(word).addAttribute("ui.color", (double)t/15);
                }
            }
            topics.add(words);
            String word0 = words.get(0);
            for(int j = 1; j < desc.length/2; j++){
                String word1 = words.get(j);
                if(graph.getEdge(word0+"-"+word1)==null && graph.getEdge(word1+"-"+word0)==null){
                    graph.addEdge(word0+"-"+word1, word0, word1);
                    //Thread.sleep((long) (50));
                }
            }
            org.graphstream.algorithm.BetweennessCentrality bcb = new org.graphstream.algorithm.BetweennessCentrality();
            bcb.init(graph);
            bcb.compute();
            for(Node node : graph){
                double bc = node.getAttribute("Cb");
                node.setAttribute("ui.size", 10*Math.log(bc));
            }
        }
        System.out.println("degree distribution: "+Arrays.toString(degreeDistribution(graph))); 
        System.out.println("max degree: "+(degreeDistribution(graph).length-1));
        System.out.println("order: "+graph.getNodeCount());
        System.out.println("average clustering coefficient: "+averageClusteringCoefficient(graph));
    }
}
