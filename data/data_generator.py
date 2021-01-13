#/usr/bin/env python3

import pandas as pd
import numpy as np

no_otus = 100
no_samples = 50

sample_names =["sample" + str(x) for x in range(1,no_samples + 1)]  
row_names = ["org" + str(x) for x in range(1,no_otus + 1)] 
col_names = row_names

# OTU table
otu = pd.DataFrame(np.random.randint(0,10000,size = (no_otus, no_samples)), index = row_names,  columns = sample_names)
otu.to_csv('otu_table.tsv', header=True, index=True, sep = "\t")

# correlation values
corr_val = pd.DataFrame(np.random.uniform(-1,1, size = (no_otus, no_otus)), index = row_names, columns = col_names)
corr_val.to_csv('random_correlation.tsv', header=True, index=True, sep = "\t")

# p values
p_val = pd.DataFrame(np.random.uniform(0,0.08, size = (no_otus, no_otus)), index = row_names,  columns = col_names)
p_val.to_csv('random_p_value.tsv', header=True, index=True, sep = "\t")
