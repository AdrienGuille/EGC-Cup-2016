/Users/adrien/anaconda/bin/python /Users/adrien/GitHub/EGC-Cup-2016/adrien/egc.py

#EGC 2016 Cup

##Data

###Data provided by the organizers
Number of articles presented at the EGC conference: 1041
Number of articles without abstract: 145

###Cleaned up data
Number of articles per language detected from the abstract: Counter({'fr': 817, '': 145, 'en': 79})   
Number of articles for which both the language of the abstract and the authors' affiliations are available: 760  
Number of articles for which have a French asbtract and for which the authors' affiliations are available: 691  
Number of articles per year: Counter({'2010': 115, '2006': 103, '2008': 103, '2011': 100, '2007': 92, '2005': 90, '2014': 87, '2004': 82, '2009': 81, '2015': 67, '2012': 65, '2013': 56})   

#Topical structure of the EGC society

##Prepared corpus and topic model
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
institution_name	institution_id	nb_articles  
@orange-ftgroup.com	0	8  
@univ-paris13.fr	1	6  
@univ-orleans.fr	2	5  
@orange.com	3	4  
@inria.fr	4	4  
@u-cergy.fr	5	3  
@univ-lyon2.fr	6	3  
@ceremade.dauphine.fr	7	2  
@orange-ft.com	8	2  
@univ-nantes.fr	9	2  
@isg.rnu.tn	10	2  
@gfi.fr	11	1  
@irisa.fr	12	1  
@univ-bpclermont.fr	13	1  
@lirmm.fr	14	1  
@univ-lille1.fr	15	1  
@fst.rnu.tn	16	1  
@stochastik.rwth-aachen.de	17	1  
@insa-lyon.fr	18	1  
@inist.fr	19	1  
@uclouvain.be	20	1  
@univ-nc.nc	21	1  
@cin.ufpe.br	22	1  
@telecom-bretagne.eu	23	1  
@supelec.fr	24	1  
@univ-lr.fr	25	1  
@fundp.ac.be	26	1  
@cnam.fr	27	1  
@ensi.rnu.tn	28	1  
@riadi.rnu.tn	29	1  
@groupama.com	30	1  
@ensta-bretagne.fr	31	1  
@univ-reunion.fr	32	1  
@agroparistech.fr	33	1  
@loria.fr	34	1  
@uniroma1.it	35	1  
@stat.uga.edu	36	1  
@enit.rnu.tn	37	1  
@lifo.univ	38	1  
@chu-rennes.fr	39	1  
@univ-lorraine.fr	40	1  
@lip6.fr	41	1  
@lri.fr	42	1  
@utc.fr	43	1  
@univ-tours.fr	44	1  
@fep.up.pt	45	1  
@univ-paris1.fr	46	1  
@cs.umb.edu	47	1  
@univ-rennes1.fr	48	1  
@univ-metz.fr	49	1  
@math.u-bordeaux1.fr	50	1  
@sfr.fr	51	1  
@francetelecom.com	52	1  
labels: @orange-ftgroup.com,@univ-paris13.fr,@univ-orleans.fr,@orange.com,@inria.fr,@u-cergy.fr,@univ-lyon2.fr,@ceremade.dauphine.fr,@orange-ft.com,@univ-nantes.fr,@isg.rnu.tn,@gfi.fr,@irisa.fr,@univ-bpclermont.fr,@lirmm.fr,@univ-lille1.fr,@fst.rnu.tn,@stochastik.rwth-aachen.de,@insa-lyon.fr,@inist.fr,@uclouvain.be,@univ-nc.nc,@cin.ufpe.br,@telecom-bretagne.eu,@supelec.fr,@univ-lr.fr,@fundp.ac.be,@cnam.fr,@ensi.rnu.tn,@riadi.rnu.tn,@groupama.com,@ensta-bretagne.fr,@univ-reunion.fr,@agroparistech.fr,@loria.fr,@uniroma1.it,@stat.uga.edu,@enit.rnu.tn,@lifo.univ,@chu-rennes.fr,@univ-lorraine.fr,@lip6.fr,@lri.fr,@utc.fr,@univ-tours.fr,@fep.up.pt,@univ-paris1.fr,@cs.umb.edu,@univ-rennes1.fr,@univ-metz.fr,@math.u-bordeaux1.fr,@sfr.fr,@francetelecom.com  

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

###Order of the collaboration network and size of the largest component per topic -> Pgfplot table
topic_id	network_order	largest_cc_size	average_cc_size  
0	74	8	3.363636  
1	147	12	4.083333  
2	116	15	3.314286  
3	104	7	3.354839  
4	86	64	9.555556  
5	104	12	3.354839  
6	214	31	3.689655  
7	128	18	3.555556  
8	128	11	3.657143  
9	79	9	3.950000  
10	96	8	3.096774  
11	251	21	4.114754  
12	131	12	3.638889  
13	56	22	4.666667  
14	130	21	4.193548  

###Normalized size of the largest component in the collaboration network per topic -> Pgfplot table
topic_id	normalized_size	cc_density  
0	0.108108	0.642857  
1	0.081633	0.424242  
2	0.129310	0.266667  
3	0.067308	0.571429  
4	0.744186	0.078869  
5	0.115385	0.393939  
6	0.144860	0.144086  
7	0.140625	0.261438  
8	0.085938	0.345455  
9	0.113924	0.416667  
10	0.083333	0.642857  
11	0.083665	0.209524  
12	0.091603	0.303030  
13	0.392857	0.181818  
14	0.161538	0.204762  

Mean largest c.c. size: 18.066667, mean normalized size: 0.169618, mean largest c.c. density: 0.339176

###Authors (with a least 5 papers) sorted by skweness of their topic repartition -> TSV
author	std	skewness	kurtosis  
Amedeo Napoli	0.348709	0.093028	-1.587365  
Edwin Diday	0.379736	0.498372	-1.510524  
Christine Largeron	0.262402	0.575817	-0.566045  
Christel Vrain	0.302996	0.588731	-0.987870  
Cécile Favre	0.312223	0.714372	-0.746362  
Mohand-Said Hacid	0.341517	0.800266	-0.915905  
Cherif Chiraz Latiri	0.361467	0.942323	-0.816333  
Gilles Venturini	0.305251	0.992668	-0.299284  
Florent Masseglia	0.309910	1.081338	-0.189203  
Guillaume Cleuziou	0.293518	1.121840	0.207203  
Ollivier Haemmerlé	0.312266	1.131042	-0.102580  
Germain Forestier	0.309480	1.131686	-0.137313  
Hakim Hacid	0.288101	1.133764	0.428896  
Jérôme Azé	0.270158	1.154402	0.317952  
Julien Blanchard	0.369300	1.160363	-0.450676  
Yahya Slimani	0.324590	1.180387	-0.120467  
Sadok Ben Yahia	0.298966	1.190191	0.289812  
Pascale Kuntz	0.299148	1.190238	0.324259  
Fadila Bentayeb	0.312210	1.238783	0.130772  
Mathias Géry	0.293849	1.257235	0.561451  
Rim Faiz	0.261578	1.329763	1.754023  
Djamel Abdelkader Zighed	0.281306	1.383428	1.053884  
Marie-Aude Aufaure	0.277782	1.412445	0.997142  
Stéphane Lallich	0.273058	1.416660	1.443289  
Fatiha Saïs	0.321357	1.429691	0.475204  
Sami Faiz	0.274394	1.477977	1.769687  
Khaoula Mahmoudi	0.274394	1.477977	1.769687  
Mohamed Ben Ahmed	0.297707	1.486959	0.997267  
Dominique Gay	0.289557	1.490681	1.100879  
Jean-François Boulicaut	0.254066	1.562670	2.020125  
Sabine Loudcher	0.308503	1.572964	1.136321  
Sandra Bringay	0.271121	1.599025	2.032850  
Patrick Gallinari	0.275063	1.633068	1.977201  
Guénaël Cabanes	0.297628	1.638019	1.340491  
Rose Dieng-Kuntz	0.287585	1.673526	1.724516  
Younès Bennani	0.304023	1.680164	1.412315  
Hanane Azzag	0.280996	1.712214	2.105403  
Fabrice Guillet	0.293525	1.716361	1.651973  
Henri Briand	0.266331	1.736625	2.191328  
Julien Velcin	0.265658	1.783239	2.605607  
Pascal Poncelet	0.263434	1.788868	2.353224  
Romain Guigourès	0.321787	1.796424	1.703961  
Frédéric Flouvat	0.270514	1.869026	2.774570  
Yves Lechevallier	0.261352	1.869553	2.842734  
Omar Boussaid	0.256705	1.876288	2.859134  
Gérard Dray	0.284709	1.905362	2.305639  
Maguelonne Teisseire	0.256594	1.909753	2.928608  
Gérard Govaert	0.256013	1.925675	3.343185  
Nazha Selmaoui-Folcher	0.268277	1.930568	2.937986  
Philippe Lenca	0.300537	1.943622	2.180116  
Dominique Laurent	0.293344	1.966346	2.409850  
Pierre-Emmanuel Jouve	0.318624	1.976803	2.171265  
Mathieu Roche	0.245675	1.998333	3.932901  
Yves Kodratoff	0.270304	2.006124	2.914940  
Mohamed Nadif	0.261879	2.018205	3.530936  
Nicole Vincent	0.275141	2.041534	2.857279  
Thierry Urruty	0.247333	2.044858	3.875466  
Gilbert Ritschard	0.267503	2.091149	3.412433  
Fabrice Clérot	0.254610	2.112678	4.172735  
Alain Simac-Lejeune	0.297708	2.113298	2.688075  
Mustapha Lebbah	0.278414	2.155057	3.414529  
Jean-Emile Symphor	0.268139	2.203362	3.845699  
Pierre Gançarski	0.251569	2.208785	4.346480  
Anne Laurent	0.256985	2.279574	4.330994  
Carine Hue	0.272273	2.327008	4.184155  
Vincent Lemaire	0.252780	2.391660	5.131095  
Engelbert Mephu Nguifo	0.230092	2.486604	5.871174  
Stéphane Loiseau	0.267399	2.498323	5.033458  
Sylvie Desprès	0.261945	2.500624	5.216727  
Chedy Raïssi	0.261593	2.529620	5.324439  
Marc Plantevit	0.245682	2.580567	6.057870  
Marc Boullé	0.241910	2.612480	6.320859  
François Poulet	0.260848	2.673131	6.010567  
Nguyen-Khang Pham	0.262856	2.676094	5.873895  
Fabrice Rossi	0.244566	2.721934	6.795102  
Thierry Despeyroux	0.243831	2.737551	6.803263  
David Genest	0.254439	2.750114	6.473101  
Juliette Dibie-Barthélemy	0.246055	2.898004	7.426477  
Régis Gras	0.242491	3.040661	8.105704  
Arnaud Soulet	0.242402	3.217414	8.902052  
Alexis Gabadinho	0.242224	3.251082	9.043522  
Matthias Studer	0.242224	3.251082	9.043522  
Nicolas S. Müller	0.242224	3.251082	9.043522  
Sylvie Guillaume	0.240687	3.265493	9.106045  
Patrice Buche	0.239918	3.299401	9.296406  
Annie Morin	0.242196	3.361720	9.584701  
Bruno Crémilleux	0.244629	3.415982	9.816101  
Georges Hébrail	0.245017	3.418853	9.827302  
Thanh-Nghi Do	0.247947	3.431130	9.876119  

###Global collaboration graph
order: 1307, largest connected component: 605  

Process finished with exit code 0
