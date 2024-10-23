
# Preparation steps for tsinfer:

# Check:
# phased data only 
# biallelic sites only

# Check / compute: 
# Infer ancestral state


# Make: SampleData file 
# https://tskit.dev/tsinfer/docs/stable/api.html
# https://tskit.dev/tsinfer/docs/stable/file_formats.html#sec-file-formats-samples

sample_data = tsinfer.SampleData(path="mydata.samples")
sample_data.add_site(position=1234, genotypes=[0, 0, 1, 0], alleles=["G", "C"])
sample_data.add_site(position=5678, genotypes=[1, 1, 1, 0], alleles=["A", "T"])
sample_data.finalise()

with tsinfer.SampleData(path="mydata.samples") as sample_data:
    sample_data.add_site(1234, [0, 0, 1, 0], ["G", "C"])
    sample_data.add_site(5678, [1, 1, 1, 0], ["A", "T"])
