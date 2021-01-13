org <- 10
sample <- 50

# otu table
otu <- matrix(sample.int(500, org * sample, replace = TRUE), org, sample)
rownames(otu) <- paste0("org", seq(1,org,1))
colnames(otu) <- paste0("sample", seq(1,sample,1))
write.table(otu, "C:/Users/Markus/Desktop/otu_table.tsv", quote = FALSE, sep = "\t")

# p value
p_val <- matrix(runif(org, min = 0, max = 0.07), org, org)
rownames(p_val) <- paste0("org", seq(1,org,1))
colnames(p_val) <- paste0("org", seq(1,org,1))
write.table(p_val, "C:/Users/Markus/Desktop/random_p_value.tsv", quote = FALSE, sep = "\t")

# corr value
corr_val <- matrix(runif(org, min = -1, max = 1), org, org)
rownames(corr_val) <- paste0("org", seq(1,org,1))
colnames(corr_val) <- paste0("org", seq(1,org,1))
write.table(corr_val, "C:/Users/Markus/Desktop/random_correlation.tsv", quote = FALSE, sep = "\t", col.names = TRUE)