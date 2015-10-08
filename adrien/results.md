/Users/adrien/anaconda/bin/python /Users/adrien/GitHub/EGC-Cup-2016/adrien/egc.py

#EGC 2016 Cup

#Topical structure of the EGC society

##Corpus and topic model
corpus size: 817  
vocabulary size: 1739  
Topic model: NMF  
number of topics: 15  

##Topics

###Most relevant words for each topic -> LaTeX table
topic 0 & réseau, social, communauté, détection, méthode, analyse, interaction, lien\\  
topic 1 & ontologie, alignement, sémantique, annotation, concept, domaine, owl, entre\\  
topic 2 & règle, association, extraction, mesure, base, extraire, confiance, indice\\  
topic 3 & séquence, temporel, événement, série, modèle, évènement, vidéo, spatio\\  
topic 4 & motif, séquentiel, extraction, contrainte, fréquent, extraire, découverte, donnée\\  
topic 5 & document, xml, annotation, recherche, information, structure, requête, mots\\  
topic 6 & utilisateur, web, information, site, système, page, sémantique, comportement\\  
topic 7 & connaissance, gestion, expert, agent, système, compétence, modélisation, métier\\  
topic 8 & variable, classification, superviser, méthode, non, classe, apprentissage, sélection\\  
topic 9 & image, afc, segmentation, recherche, région, objet, classification, satellite\\  
topic 10 & graphe, voisinage, représentation, interrogation, fouille, sous, visualisation, structure\\  
topic 11 & donnée, flux, base, requête, cube, fouille, visualisation, entrepôt\\  
topic 12 & algorithme, arbre, svm, ensemble, décision, nouveau, grand, résultat\\  
topic 13 & carte, topologique, auto, organisatrice, som, cognitif, probabiliste, contrainte\\  
topic 14 & texte, corpus, automatique, textuel, partir, méthode, opinion, clr\\  

###Overall frequency of each topic -> Pgfplot table
topic_id	overall_frequency  
0	0.036720  
1	0.068543  
2	0.067319  
3	0.057528  
4	0.055080  
5	0.051408  
6	0.104039  
7	0.067319  
8	0.088127  
9	0.036720  
10	0.045288  
11	0.138311  
12	0.074663  
13	0.039168  
14	0.069767  

##Fading topic: topic #2 (association rule mining)

###Frequency vs. year -> Pgfplot table
year	topic_frequency  
2004	0.103448  
2005	0.094595  
2006	0.118421  
2007	0.088889  
2008	0.043478  
2009	0.053571  
2010	0.051282  
2011	0.075758  
2012	0.080000  
2013	0.039216  
2014	0.012821  
2015	0.041667  

##Emerging topic: topic #0 (social network analysis and mining)

###Frequency vs. year -> Pgfplot table
year	topic_frequency  
2004	0.000000  
2005	0.013514  
2006	0.026316  
2007	0.022222  
2008	0.010870  
2009	0.035714  
2010	0.012821  
2011	0.030303  
2012	0.060000  
2013	0.117647  
2014	0.089744  
2015	0.062500  

##Mostly industrial topic: topic #8 (variable and model selection)

###Articles per institution -> Pgfplot table
institution	nb_articles  
@orange-ftgroup.com	8  
@univ-paris13.fr	6  
@univ-orleans.fr	5  
@orange.com	4  
@inria.fr	4  
@u-cergy.fr	3  
@univ-lyon2.fr	3  
@ceremade.dauphine.fr	2  
@orange-ft.com	2  
@univ-nantes.fr	2  
@isg.rnu.tn	2  
@gfi.fr	1  
@irisa.fr	1  
@univ-bpclermont.fr	1  
@lirmm.fr	1  
@univ-lille1.fr	1  
@fst.rnu.tn	1  
@stochastik.rwth-aachen.de	1  
@insa-lyon.fr	1  
@inist.fr	1  
@uclouvain.be	1  
@univ-nc.nc	1  
@cin.ufpe.br	1  
@telecom-bretagne.eu	1  
@supelec.fr	1  
@univ-lr.fr	1  
@fundp.ac.be	1  
@cnam.fr	1  
@ensi.rnu.tn	1  
@riadi.rnu.tn	1  
@groupama.com	1  
@ensta-bretagne.fr	1  
@univ-reunion.fr	1  
@agroparistech.fr	1  
@loria.fr	1  
@uniroma1.it	1  
@stat.uga.edu	1  
@enit.rnu.tn	1  
@lifo.univ	1  
@chu-rennes.fr	1  
@univ-lorraine.fr	1  
@lip6.fr	1  
@lri.fr	1  
@utc.fr	1  
@univ-tours.fr	1  
@fep.up.pt	1  
@univ-paris1.fr	1  
@cs.umb.edu	1  
@univ-rennes1.fr	1  
@univ-metz.fr	1  
@math.u-bordeaux1.fr	1  
@sfr.fr	1  
@francetelecom.com	1  

###Titles of the articles related to topic #8 and involving Orange
0	Sélection d'une méthode de classification multi-label pour un système interactif  
1	Un Critère d'évaluation pour la construction de variables à base d'itemsets pour l'apprentissage supervisé multi-tables  
2	Vers une Automatisation de la Construction de Variables pour la Classification Supervisée  
3	Clustering hiérarchique non paramétrique de données fonctionnelles  
4	Prétraitement Supervisé des Variables Numériques pour la Fouille de Données Multi-Tables  
5	Sélection Bayésienne de Modèles avec Prior Dépendant des Données  
6	Optimisation directe des poids de modèles dans un prédicteur Bayésien naïf moyenné  
7	Sélection des variables informatives pour l'apprentissage supervisé multi-tables  
8	Classification supervisée pour de grands nombres de classes à prédire : une approche par co-partitionnement des variables explicatives et à expliquer  
9	Exploration des corrélations dans un classifieur Application au placement d'offres commerciales  
10	Une méthode de classification supervisée sans paramètre pour l'apprentissage sur les grandes bases de données  
11	Une approche non paramétrique Bayésienne pour l'estimation de densité conditionnelle sur les rangs  

##Highly collaborative topic: topic #4 (pattern mining)

###Normalized size of the largest component in the collaboration network per topic -> Pgfplot table
topic_id	normalized_size  
0	0.108108  
1	0.081633  
2	0.129310  
3	0.067308  
4	0.744186  
5	0.115385  
6	0.144860  
7	0.140625  
8	0.085938  
9	0.113924  
10	0.083333  
11	0.083665  
12	0.091603  
13	0.392857  
14	0.161538  

###Z-score(Normalized size of the largest component in the collaboration network per topic) -> Pgfplot table
topic_id	z_score  
0	-0.359524  
1	-0.514272  
2	-0.235598  
3	-0.598001  
4	3.358325  
5	-0.316993  
6	-0.144712  
7	-0.169464  
8	-0.489110  
9	-0.325530  
10	-0.504331  
11	-0.502391  
12	-0.455995  
13	1.304822  
14	-0.047226  

#Collaborative structure of the EGC society

##Evolution of the density of the collaboration network
year	year_density	cumulative_density  
2004	0.016438	0.016438  
2005	0.012310	0.008806  
2006	0.013780	0.006939  
2007	0.011000	0.005411  
2008	0.011432	0.004477  
2009	0.017381	0.004087  
2010	0.012873	0.003571  
2011	0.015368	0.003349  
2012	0.019571	0.003205  
2013	0.019554	0.003006  
2014	0.013099	0.002782  
2015	0.018892	0.002628  

##Evolution of the average clustering coefficient of the collaboration network
year	year_clust_coeff	cumulative_clust_coeff  
2004	0.751924	0.751924  
2005	0.683988	0.704545  
2006	0.656927	0.687971  
2007	0.698964	0.678432  
2008	0.711735	0.678143  
2009	0.752582	0.679420  
2010	0.777737	0.684606  
2011	0.792193	0.681818  
2012	0.804520	0.683244  
2013	0.826731	0.688406  
2014	0.821196	0.693921  
2015	0.822952	0.695448  

Process finished with exit code 0
