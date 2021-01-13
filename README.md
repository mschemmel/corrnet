![GitHub](https://img.shields.io/github/license/mschemmel/corrnet)
<img src="https://img.shields.io/badge/python-3.4--3.9-9cf.svg?style=flat">
[![BuildStatus](https://travis-ci.org/mschemmel/corrnet.svg?branch=master)](https://travis-ci.org/mschemmel/corrnet)

# corrnet
The provided scripts can be used to convert correlation and p-value matrices to an condensed edgelist. Following, the resulting edge list will be used to generate networks using the python package [NetworkX](https://networkx.github.io/). The edge list can be optional restricted to a given correlation treshold (-clim) and p-value threshold (-plim). Great tools for calculating correlation matrices (identifying co-occurence patterns), especially of microbiome communities are [SparCC](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1002687) and [FastSpar](https://academic.oup.com/bioinformatics/article/35/6/1064/5086389). Created networks are only a basic representation, advanced representations require adjustments of the code. The 'data' folder contains artificially generated correlation and p-value matrices for testing purposes.   

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
| Argument | Type |
| --- | --- |
| clim | numeric |
| plim | numeric |
| prefix | character |


## Usage
### Parameter
    -cm     correlation matrix
    -pm     p-value matrix
    -clim   Threshold of correlation matrix (Default: 0.7)
    -plim   Threshold of p-value matrix (Default: 0.05)
    -out    Path for generated output. If not provided, current working directory is used.
    -pre    Prefix used to name output folder and files (Default: corrnet)

### Run

```
python3 corrnet.py -cm random_correlation.tsv -pm random_p_pvalue.tsv --prefix firstproject 
```

## Output
- edgelist (columns: source, target, weight, pval, direction, color)
- network plot
- network degree distribution plot

