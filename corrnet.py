import corr2edge as cte
import edge2net as etn
import argparse
import os

def main():
  # handle command line arguments
  parser = argparse.ArgumentParser(description = "Program to transform correlation matrix to edgelists for further network creation")
  parser.add_argument("-cm", "--corrmat", help = "Path to correlation matrix")
  parser.add_argument("-pm", "--pmat", help = "Path to p value matrix")
  parser.add_argument("-clim", "--corrlimit", help = "correlation value threshold (Default: -0.7 | 0.7")
  parser.add_argument("-out", "--output", help = "Path for generated summaries and network statistics")
  parser.add_argument("-plim", "--plimit", help = "p-value threshold (Default: 0.05)")
  parser.add_argument("-pre", "--prefix", help = "Prefix to label specific run")
  args = parser.parse_args()


  if (args.corrmat and args.pmat):
      # check correlation limit and pvalue limit
      clim = args.corrlimit if args.corrlimit else 0.7
      plim = args.plimit if args.plimit else 0.05
      
      # create new edgelist object and pull edges
      data = cte.edgelist(args.corrmat, args.pmat, clim, plim) 
      edges = data.edges()

      # check if output path is provided
      output = args.output if args.output else os.getcwd()
      pref = args.prefix if args.prefix else "corrnet"
      
      # create network
      data_net = etn.net(edges)
      print("")
      print("## Network Summary")
      for element in data_net.summary():
          print(element)
      
      # save all files
      # create final output folder
      out_dir = os.path.join(output, pref)
      if os.path.isdir(out_dir):
          pass
      else:
          os.mkdir(out_dir)

      edges.to_csv("{}/edge_list_{}.tsv".format(out_dir, pref), index = None, sep = '\t', mode = 'w')
      network = data_net.plot_network()
      network.savefig(os.path.join(out_dir, "net.pdf"), bbox_inches = 'tight')
      
      degree_histogram = data_net.plot_degree_hist()
      degree_histogram.savefig(os.path.join(out_dir, "hist.pdf"), bbox_inches = 'tight')

      


if __name__ == "__main__":
  main()
