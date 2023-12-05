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
				f = plt.figure(figsize=(10,10))

				#set layout to circular layout
				layout = nx.circular_layout(self.edgelist)
				
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
				return(f"Positive: {positive}\t Negative: {negative}")
		
		def summary(self):
				'''
				Print summary information of network
				'''
				return([self.relation_info(), self.get_density_value()])