#!/usr/bin/env python3

import pandas as pd
import numpy as np
import collections
import sys
import os

class edgelist():
  def __init__(self, cormat, pmat, clim, plim):
      self.cormat = cormat
      self.pmat = pmat
      self.clim = clim
      self.plim = plim

  def filter_and_stack(self, df):
      """
      Function which takes a dataframe to solely select the upper triangle and stack them afterwards
      """
      # reshape adjancy matrix
      # https://stackoverflow.com/questions/48218455/how-to-create-an-edge-list-dataframe-from-a-adjacency-matrix-in-python
      #df = df.rename_axis('Source').reset_index().melt('Source', value_name='Weight', var_name='Target').query('Source != Target').reset_index(drop=True)
      
      # https://stackoverflow.com/questions/34417685/melt-the-upper-triangular-matrix-of-a-pandas-dataframe
      # select only upper triangle to reshape and stack df
      df_triu = df.where(np.triu(np.ones(df.shape)).astype(np.bool))
      
      # stack upper triangle and reset index
      df_fin = df_triu.stack().reset_index()

      # rename colum names to match required nomenclature
      df_fin.columns = ["source", "target", "weight"]
      
      # avoid self correlation (corr value == 1) -> (Source != Target)
      df_fin = df_fin[df_fin["source"] != df_fin["target"]]
      
      return(df_fin)

  def compare_order(self, df1, df2, name):
      """
      Function which evaluates the order of two columns of a dataframe(s) to make sure both
      columns have the same order.
      Returns TRUE if the order is the same.
      Returns FALSE if the order differs.
      """
      compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
      return(compare(df1[name].tolist(), df2[name].tolist()))

  # filter correlations by correlation and p-value
  def filter_relevant(self, df, pval, cval):
      """
      Function which filters the given dataframe by specified correlation
      and p-value threshold.
      """
      df = df[(df["weight"] > cval) | (df["weight"] < (cval * -1))]
      df = df[(df["pval"] < pval) & (df["pval"] != 0)]
      
      return(df)

  def summary_of_edges(self, from_edges):
      """
      Function to display a short summary about the resulting
      EDGE and NODE lists and their respective number
      """
      # Pandas shape function returns (?,?):
      # number of rows df.shape[0]
      # number of col = df.shape[1]

      print("\n## Summary")
      print("No. of edges = {}".format(from_edges.shape[0]))
      print("Range:")
      print("\tpval:\t{}..{}".format(from_edges["pval"].min(), from_edges["pval"].max()))
      print("\tweight:\t{}..{}".format(from_edges["weight"].min(), from_edges["weight"].max()))


  def edges(self):

      # import required files 
      corr = pd.read_table(self.cormat, sep = "\t", index_col = '#OTU ID')
      pval = pd.read_table(self.pmat, sep = "\t", index_col = '#OTU ID')

      
      # shape dataframe to required format -> edge_list
      corr_el = self.filter_and_stack(corr)
      pval_el = self.filter_and_stack(pval)

      # check if order of both dataframes have the same 'Source' and 'Target' order 
      # otherwise joining would be inadmissible
      source = self.compare_order(corr_el, pval_el, "source")
      target = self.compare_order(corr_el, pval_el, "target")

      if source and target:
          merged = pd.concat([corr_el, pval_el["weight"]], axis = 1, ignore_index = True)        
          merged.columns = ["source", "target", "weight", "pval"]
          
          # filter final frame by weight and p value
          finalFrame = self.filter_relevant(merged, float(self.plim), float(self.clim))        
          finalFrame["direction"] = np.where(finalFrame["weight"] < 0, "-1", "1")

      else:
          print("ERROR: Correlation and pvalue matrix do not have the same order")
          sys.exit(0)
      
      # save edge_list and node_list to file if frame is not 'None'
      if finalFrame is not None:           
          print("\n## Parameter")
          print("correlation threshold: {}".format(self.clim))
          print("p-value threshold: {}".format(self.plim))
          
          # show summary of edges
          self.summary_of_edges(finalFrame)
          return(finalFrame)
      else:
          print("ERROR: Something went wrong on building the edgelist.")
          sys.exit(0)




