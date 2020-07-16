# corrnet
The provided scripts can be used to convert correlation and p-value matrices to an condensed edgelist. Following, the resulting edge list will be used to generate networks using the python package [NetworkX](https://networkx.github.io/). The edge list can be optional restricted to a given correlation treshold (-clim) and p-value threshold (-plim). Great tools for calculating correlation matrices, especially of microbiome communities are [SparCC](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1002687) and [FastSpar](https://academic.oup.com/bioinformatics/article/35/6/1064/5086389).

## Requirements
### Prerequisites
The additional python packages below are required:
- numpy
- pandas
- matplotlib
- networkx

Following input is required to run the script:
- correlation matrix -> tabular separated (.tsv) 
- p-value matrix -> tabular separated (.tsv)

Optional:
- correlation limit -> numerical value
- p-value limit -> numerical value 
- Prefix 

## Usage
### Parameter
    -cm     correlation matrix
    -pm     p-value matrix
    -clim   Threshold of correlation matrix (Default: 0.7)
    -plim   Threshold of p-value matrix (Default: 0.05)
    -out    Path for generated output
    -pre    Prefix used to name output folder and files (Default: corrnet)

### Run

```
python3 corrnet.py -cm correlation.tsv -pm pvalue.tsv --prefix firstproject 
```

## Output

- edgelist summary
- network summary
- network plot
- network degree distribution plot

