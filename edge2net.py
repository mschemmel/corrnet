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
				self.df["color"] = np.where(self.df['direction'] == "1", '#2A9D8F', '#E76F51')
				self.edgelist = nx.from_pandas_edgelist(self.df, source = 'source', target = 'target')				
			

		def nodes_and_edges(self):
				'''
				Return number of nodes and number of edges of network
				'''
				return(nx.number_of_nodes(self.edgelist), nx.number_of_edges(self.edgelist))
		
		def plot_network(self, pltTitle = "Default"):
				'''
				Plot network with previously prepared edge list and export as .pdf file.
				Further, export histogram of network connections
				'''
				# set figure size
				f = plt.figure(figsize=(10, 10))

				#set layout to circular layout
				#layout = nx.circular_layout(self.edgelist)
				layout = nx.spring_layout(self.edgelist, k=0.15,iterations=20)
				#layout = nx.kamada_kawai_layout(self.edgelist)
				#layout = nx.shell_layout(self.edgelist)
				
				# Go through every zotu -> how many connections?
				# calculate circle size according to number of connections
				zotus = list(self.df.source.unique())
				zotu_size = [self.edgelist.degree(zotu) * 5 for zotu in zotus]
				
				# draw all nodes based on previously determined properties
				nx.draw_networkx_nodes(self.edgelist, 
															 layout,
															 nodelist = zotus, 
															 node_size = zotu_size,
															 #node_size = 7, 
															 node_color = '#89ABE3FF')

				# draw all edges based on previously determined properties
				nx.draw_networkx_edges(self.edgelist, layout, width = 1, edge_color = self.df["color"])
				
				# set some plot specific elements
				plt.axis('off')
				plt.title(pltTitle)

				# return the network plot
				return(f)
				
		def get_density_value(self):
				'''
				Return density value of network
				'''
				# https://en.wikipedia.org/wiki/Degree_distribution
				# Density: The proportion of direct ties in a network relative to the total number possible.
				return(f"Density: {round(nx.density(self.edgelist), 3)}")
		
		def get_degree_values(self, sort = True):
				'''
				Get degree values of network
				'''
				degrees = list(nx.degree(self.edgelist))
				if sort : degrees.sort(key = lambda x:x[1])
				return(degrees)
		
		def relation_info(self):
				'''
				Get and return number of positive and negative edges
				'''
				positive = len(self.df[self.df["direction"] == "1"])
				negative = len(self.df[self.df["direction"] == "-1"])

				# test if number of edges are equal before reporting informations about relations
				if ((positive + negative) == nx.number_of_edges(self.edgelist)):
					return(f"Positive: {positive}\t Negative: {negative}")
				else:
					return("ERROR: Number of edges differ.")
		
		def summary(self):
				'''
				Print summary information of network
				'''
				return([self.relation_info(), self.get_density_value()])
		
		def plot_degree_hist(self):
				'''
				Build degree histogram of edge list
				'''
				# set subplot properties
				fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8,3))
				fig.suptitle('Degree distribution and relation')
				
				degree_freq = nx.degree_histogram(self.edgelist)
				degrees = range(len(degree_freq))
				
				m = 3
				ax1.loglog(degrees[m:], degree_freq[m:], color = "#89ABE3FF")  
				ax1.set_xlabel('Degree')
				ax1.set_ylabel('Frequency')
				ax1.spines["top"].set_visible(False)
				ax1.spines["right"].set_visible(False)

				# https://networkx.github.io/documentation/stable/auto_examples/drawing/plot_degree_histogram.html
				degree_sequence = sorted([d for n, d in self.edgelist.degree()], reverse = True)	# degree sequence
				degreeCount = collections.Counter(degree_sequence)
				deg, cnt = zip(*degreeCount.items())

				ax2.bar(deg, cnt, width=0.80, color='#89ABE3FF')
				ax2.set_ylabel('Count')
				ax2.set_xlabel('Degree')
				ax2.spines["top"].set_visible(False)
				ax2.spines["right"].set_visible(False)	 
				
				# get number of positive and negative relations (same as function -> relation.info())
				positive = len(self.df[self.df["direction"] == "1"])
				negative = len(self.df[self.df["direction"] == "-1"])
				
				ax3.bar(["Pos", "Neg"], [positive,negative], width=0.80, color='#89ABE3FF')
				ax3.set_ylabel('Count')
				ax3.set_xlabel('Relation')
				ax3.spines["top"].set_visible(False)
				ax3.spines["right"].set_visible(False)	 
				
				return(fig)

