import cyvcf2
import tsinfer


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


# URL for the VCF
#url = "https://github.com/tskit-dev/tsinfer/raw/main/docs/_static/P_dom_chr24_phased.vcf.gz"
filename = "ALL.chr21.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.vcf.gz"

#vcf = cyvcf2.VCF(url)
vcf = cyvcf2.VCF(filename)
with tsinfer.SampleData(
    path="ALL.chr21.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.samples", sequence_length=46709983
) as samples:
    add_diploid_sites(vcf, samples)

print(
    "Sample file created for {} samples ".format(samples.num_samples)
    + "({} individuals) ".format(samples.num_individuals)
    + "with {} variable sites.".format(samples.num_sites),
    flush=True,
)

# Do the inference
ts = tsinfer.infer(samples)
print(
    "Inferred tree sequence: {} trees over {} Mb ({} edges)".format(
        ts.num_trees, ts.sequence_length / 1e6, ts.num_edges
    )
)