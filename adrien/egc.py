# coding: utf-8
import utils
import networkx as nx
from scipy import stats
import numpy as np

__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

print'\n#EGC 2016 Cup : results'

print'\n##Overview of the data'

# Load the topic model : NMF (k=15)
topic_model = utils.load_topic_model('nmf_15topics_egc.pickle')
print 'corpus size: %i' % topic_model.corpus.size
print 'vocabulary size: %i' % len(topic_model.corpus.vocabulary)
print 'number of topics: %i' % topic_model.nb_topics

print '\n###Most relevant words for each topic -> LaTeX table'
for topic_id in range(topic_model.nb_topics):
    word_list = []
    for weighted_word in topic_model.top_words(topic_id, 8):
        word_list.append(weighted_word[0])
    print 'topic %i & %s\\\\  ' % (topic_id, ', '.join(word_list))

print '\n###Overall frequency of each topic -> Pgfplot table'
frequency = topic_model.topics_frequency()
for topic_id in range(topic_model.nb_topics):
    print '%i\t%f  ' % (topic_id, frequency[topic_id])

topic_associations = topic_model.documents_per_topic()

print '\n##Fading topic: topic #2 (association rule mining)'

print '\n###Frequency vs. year -> Pgfplot table'
for i in range(2004, 2016):
    print '%i\t%f  ' % (i, topic_model.topic_frequency(2, date=i))

print '\n##Emerging topic: topic #0 (social network analysis and mining)'

print '\n###Frequency vs. year -> Pgfplot table'
for i in range(2004, 2016):
    print '%i\t%f  ' % (i, topic_model.topic_frequency(0, date=i))

print '\n##Mostly industrial topic: topic #8 (variable and model selection)'

print '\n###Articles per institution -> Pgfplot table'
for institution, nb_articles in topic_model.affiliation_repartition(8):
    print '%s\t%i  ' % (institution, nb_articles)

print '\n###Titles of the articles related to topic #8 and involving Orange'
for doc_id in topic_associations[8]:
    affiliations = topic_model.corpus.affiliations(doc_id)
    if '@orange.com' in affiliations or '@orange-ftgroup.com' in affiliations or '@orange.com' in affiliations:
        print topic_model.corpus.short_content(doc_id), '  '

print '\n##Highly collaborative topic: topic #4 (pattern mining)'

normalized_sizes = []
print '\n###Normalized size of the largest component in the collaboration network per topic -> Pgfplot table'
for topic_id in range(topic_model.nb_topics):
    graph = topic_model.corpus.collaboration_network(topic_associations[topic_id], nx_format=True)
    graph_order = len(nx.nodes(graph))
    connected_components = sorted(nx.connected_component_subgraphs(graph), key=len, reverse=True)
    largest_connected_component = connected_components[0]
    largest_connected_component_norm_size = float(len(nx.nodes(largest_connected_component)))/float(graph_order)
    normalized_sizes.append(largest_connected_component_norm_size)
    print '%i\t%f  ' % (topic_id, largest_connected_component_norm_size)

# Remove the normalized size of the largest connected component for topic 4
normalized_size_topic4 = normalized_sizes.pop(4)

print '\nAre these values drawn from a normal distribution (Shapiro-Wilk)? W=%f, p-value=%f  ' % stats.shapiro(normalized_sizes)

# Fit a normal distribution to these values
mu, std = stats.norm.fit(normalized_sizes)
s = np.random.normal(mu, std)
