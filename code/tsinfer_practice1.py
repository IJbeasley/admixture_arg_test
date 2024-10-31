import cyvcf2
import tsinfer
import time as time


# Input argument
import argparse
parser = argparse.ArgumentParser()

# Required
req_group = parser.add_argument_group(title='REQUIRED INPUT')
req_group.add_argument('-vcf', '-v', help='VCF/BCF file', required=True)
req_group.add_argument('-out', '-o', help='Output sampleData file', required=True)

args = parser.parse_args()

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def add_diploid_sites(vcf, samples):
    """
    Read the sites in the vcf and add them to the samples object, reordering the
    alleles to put the ancestral allele first, if it is available.
    """
    # You may want to change the following line, e.g. here we allow * (a spanning
    # deletion) to be a valid allele state
    allele_chars = set("ATGCatgc*")
    pos = 0
    for variant in vcf:  # Loop over variants, each assumed at a unique site
        if pos == variant.POS:
            print(f"Duplicate entries at position {pos}, ignoring all but the first")
            continue
        else:
            pos = variant.POS
        if any([not phased for _, _, phased in variant.genotypes]):
            raise ValueError("Unphased genotypes for variant at position", pos)
        alleles = [variant.REF.upper()] + [v.upper() for v in variant.ALT]
        ancestral = variant.INFO.get("AA", ".")  # "." means unknown
        # some VCFs (e.g. from 1000G) have many values in the AA field: take the 1st
        ancestral = ancestral.split("|")[0].upper()
        if ancestral == "." or ancestral == "":
            # use the reference as ancestral, if unknown (NB: you may not want this)
            ancestral = variant.REF.upper()
        # Ancestral state must be first in the allele list.
        ordered_alleles = [ancestral] + list(set(alleles) - {ancestral})
        # Check we have ATCG alleles
        for a in ordered_alleles:
            if len(set(a) - allele_chars) > 0:
                print(f"Ignoring site at pos {pos}: allele {a} not in {allele_chars}")
                continue
        allele_index = {
            old_index: ordered_alleles.index(a) for old_index, a in enumerate(alleles)
        }
        # Map original allele indexes to their indexes in the new alleles list.
        genotypes = [
            allele_index[old_index]
            for row in variant.genotypes
            for old_index in row[0:2]
        ]
        samples.add_site(pos, genotypes=genotypes, alleles=ordered_alleles)


def chromosome_length(vcf):
    assert len(vcf.seqlens) == 1
    return vcf.seqlens[0]


start_time = time.perf_counter()

#in_filename = "output/thous_genomes_samp/chr_20_5EUR.bcf"
#out_filename="output/sampleData/chr_20_5EUR.samples"

vcf = cyvcf2.VCF(args.vcf)

with tsinfer.SampleData(
    path=args.out
) as samples:
    add_diploid_sites(vcf, samples)


end_time = time.perf_counter()
print(f"\n Making the SampleData file took {end_time - start_time:.4f} seconds")

print(
    "\n Sample file created for {} samples ".format(samples.num_samples)
    + "({} individuals) ".format(samples.num_individuals)
    + "with {} variable sites.".format(samples.num_sites),
    flush=True,
)


# Do the inference

start_time = time.perf_counter()

ts = tsinfer.infer(samples)
print(
    "Inferred tree sequence: {} trees over {} Mb ({} edges)".format(
        ts.num_trees, ts.sequence_length / 1e6, ts.num_edges
    )
)

end_time = time.perf_counter()
print(f"\n Infering the ARG took {end_time - start_time:.4f} seconds")

print("\n Done!")
