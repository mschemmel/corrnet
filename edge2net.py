# based on several tutorials
# amongst other: 
# http://jonathansoma.com/lede/algorithms-2017/classes/networks/networkx-graphs-from-source-target-dataframe/

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import collections
import numpy as np
import os
     
class net():
    def __init__(self, data):
        self.data = data
        # import edge list
        # transform edge list (data frame) to edge list (networkx)
        self.df = data
        self.df["color"] = np.where(self.df['direction'] == 1, '#E3CD81FF', '#9E1030FF')
        self.edgelist = nx.from_pandas_edgelist(self.df, source = 'source', target = 'target')
    
    def nodes_and_edges(self):
        return(nx.number_of_nodes(self.edgelist), nx.number_of_edges(self.edgelist))
    
    def plot_network(self, pltTitle = "Default"):
        # set figure size
        f = plt.figure(figsize=(10, 10))

        #set layout to circular layout
        layout = nx.circular_layout(self.edgelist)

        # Go through every zotu -> how many connections?
        # calculate circle size according to number of connections
        zotus = list(self.df.source.unique())
        zotu_size = [self.edgelist.degree(zotu) * 10 for zotu in zotus]

        # draw all nodes based on previously determined properties
        nx.draw_networkx_nodes(self.edgelist, 
                               layout, 
                               nodelist = zotus, 
                               node_size = zotu_size,
                               node_color = '#89ABE3FF')

        # draw all edges based on previously determined properties
        nx.draw_networkx_edges(self.edgelist, layout, width = 1, edge_color = self.df["color"])
        
        # set some plot specific elements
        plt.axis('off')
        plt.title(pltTitle)

        # return the network plot
        return(f)
        
    def get_density_value(self):
        # https://en.wikipedia.org/wiki/Degree_distribution
        # Density: The proportion of direct ties in a network relative to the total number possible.
        return("Density: {}".format(nx.density(self.edgelist)))
    
    def get_degree_values(self, sort = True):
        degrees = list(nx.degree(self.edgelist))
        if sort : degrees.sort(key = lambda x:x[1])
        return(degrees)
    
    def get_network_info(self):
        return(nx.info(self.edgelist))

    def relation_info(self):
        positive = len(self.df[self.df["direction"] == 1])
        negative = len(self.df[self.df["direction"] == -1])
        return "Positive: {}\t Negative: {}".format(positive, negative)
    
    def summary(self):
        return([self.get_network_info(), self.relation_info(), self.get_density_value()])
    
    def plot_degree_hist(self):
        # set subplot properties
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8,3))
        fig.suptitle('Degree distribution')
        
        degree_freq = nx.degree_histogram(self.edgelist)
        degrees = range(len(degree_freq))
        
        m = 3
        ax1.loglog(degrees[m:], degree_freq[m:], color = "#89ABE3FF")  
        ax1.set_xlabel('Degree')
        ax1.set_ylabel('Frequency')
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)

        # https://networkx.github.io/documentation/stable/auto_examples/drawing/plot_degree_histogram.html
        degree_sequence = sorted([d for n, d in self.edgelist.degree()], reverse = True)  # degree sequence
        degreeCount = collections.Counter(degree_sequence)
        deg, cnt = zip(*degreeCount.items())

        ax2.bar(deg, cnt, width=0.80, color='#89ABE3FF')
        ax2.set_ylabel('Count')
        ax2.set_xlabel('Degree')
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)   
        
        return(fig)