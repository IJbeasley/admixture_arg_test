import tsinfer

# Preparation steps for tsinfer:

# Check:
# phased data only 
# biallelic sites only

# Make: SampleData file 
# https://tskit.dev/tsinfer/docs/stable/api.html
# https://tskit.dev/tsinfer/docs/stable/file_formats.html#sec-file-formats-samples

# a. Define populations 

def process_chunk(chunk, output_path):
    """Process a chunk of VCF lines and write to SampleData."""
    sample_data = tsinfer.SampleData(path=output_path)
    for line in chunk:
        if line.startswith("#"):
            continue  # Skip header lines
        fields = line.strip().split("\t")
        position = int(fields[1])  # POS column
        alleles = [fields[3]] + fields[4].split(",")  # REF + ALT
        genotypes = [int(gt) for gt in fields[9].split(":")[0].split("|")]  # GT column
        sample_data.add_site(position=position, genotypes=genotypes, alleles=alleles)
    sample_data.finalise()
    
process_chunk

# b. Define samples 

sample_data = tsinfer.SampleData(path="mydata.samples")
sample_data.add_site(position=1234, genotypes=[0, 0, 1, 0], alleles=["G", "C"])
sample_data.add_site(position=5678, genotypes=[1, 1, 1, 0], alleles=["A", "T"])
sample_data.finalise()

with tsinfer.SampleData(path="mydata.samples") as sample_data:
    sample_data.add_site(1234, [0, 0, 1, 0], ["G", "C"])
    sample_data.add_site(5678, [1, 1, 1, 0], ["A", "T"])


#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT  HG00096
chr20   60114   .       T       C       .       PASS    AC=0;AN=2;DP=67920;AF=0;EAS_AF=0;EUR_AF=0;AFR_AF=0;AMR_AF=0;SAS_AF=0;VT=SNP;NS=2548      GT      0|0
chr20   60138   .       T       A       .       PASS    AC=0;AN=2;DP=69096;AF=0;EAS_AF=0;EUR_AF=0;AFR_AF=0;AMR_AF=0;SAS_AF=0;VT=SNP;NS=2548      GT      1|0
chr20   60149   .       C       T       .       PASS    AC=0;AN=2;DP=66846;AF=0;EAS_AF=0;EUR_AF=0;AFR_AF=0;AMR_AF=0.01;SAS_AF=0;VT=SNP;NS=2548   GT      0|1

60114 

# Check / compute: 
# Infer ancestral state
