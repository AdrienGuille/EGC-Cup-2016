/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 *   @author Adrien GUILLE, ERIC Lab, University of Lyon 2
 *   @email adrien.guille@univ-lyon2.fr
 */
public class Main {
    
    public static void main(String[] args) throws Exception {
        GraphVisualization first6conferences = new GraphVisualization("/Users/adrien/GitHub/EGC-Cup-2016/output/topic models/lda_fr_2004-2009.txt");
        GraphVisualization last6conferences = new GraphVisualization("/Users/adrien/GitHub/EGC-Cup-2016/output/topic models/lda_fr_2010-2015.txt");
    }
}
