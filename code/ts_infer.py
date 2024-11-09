import cyvcf2
import tsinfer
import time as time
import numpy as np

import warnings
warnings.simplefilter(action='ignore', 
                      category=FutureWarning
                      )


################# Argparse arguments ######################

import argparse
parser = argparse.ArgumentParser()

# Required inputs 
req_group = parser.add_argument_group(title='REQUIRED INPUT')
req_group.add_argument('-vcf', '-v', 
                       help='VCF/BCF file', 
                       required=True
                       )
req_group.add_argument('-out', '-o', 
                       help='Output sampleData file', 
                       required=True
                       )

# Optional inputs
inp_group = parser.add_argument_group(title='OPTIONAL INPUT')
inp_group.add_argument('-pop_assign', 
                       help = 'Text file assigning samples to populations'
                       'Otherwise, all samples are assumed to be from the same population',
                       default='undefined',
                       required=False
                       )
inp_group.add_argument('-n_cpus', '-n', 
                       help = "Number of avaliable CPUs", 
                       required=False
                       )

args = parser.parse_args()


########## Functions ################## 

def add_diploid_populations(pop_assign, samplesData): 
    """
    Read in the population assignments, and set these up with the 
    """

    if pop_assign == "undefined":
      
      samplesData.add_population(metadata={"name": pop_assign})

    else:
      
      pop_assign = np.loadtxt(pop_assign, 
                              dtype='U10', 
                              delimiter=','
                              )
      
      all_populations = np.unique(pop_assign[:, 1])

      for population in all_populations:
        
        samplesData.add_population(metadata={"name": population})
         
       

def add_diploid_individuals(pop_assign, vcf, samplesData):
    """
    Read in the samples from the vcf, and add them to the samples object
    """
    
    if pop_assign == "undefined":
      
       for individual in vcf.samples:
         
            samplesData.add_individual(ploidy = 2, 
                                   population = 0, 
                                   metadata={"name": individual}
                                   )
    
    else:
      
      pop_assign = np.loadtxt(pop_assign, 
                              dtype='U10', 
                              delimiter=','
                              )
          
      # getting mapping between sample id and population id                            
      all_populations = np.unique(pop_assign[:, 1])
      population_to_num = {pop: i for i, pop in enumerate(all_populations)}
      
      for individual_num in range(pop_assign.shape[0]):
        
          individual_pop = pop_assign[individual_num, 1]
           
          samplesData.add_individual(ploidy = 2, 
                                     population = population_to_num.get(individual_pop),
                                     metadata = {"name": individual_pop}
                                     )

    

def add_diploid_sites(vcf, samplesData):
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
        samplesData.add_site(pos, genotypes=genotypes, alleles=ordered_alleles)


# def chromosome_length(vcf):
#     assert len(vcf.seqlens) == 1
#     return vcf.seqlens[0]

######### Build sampleData file: #############

start_time = time.perf_counter()
vcf = cyvcf2.VCF(args.vcf)

#samples = vcf.samplesData

# Set up population assignments for sampleData file: 
pop_assign = args.pop_assign

with tsinfer.SampleData(
    path=args.out
) as samplesData:
    add_diploid_populations(pop_assign, samplesData)
    add_diploid_individuals(pop_assign, vcf, samplesData)
    add_diploid_sites(vcf, samplesData)

print(
    "\n \n Sample file created for {} samples: ".format(samplesData.num_samples)
    + "\n {} populations".format(samplesData.num_populations)
#    + "{})".samplesData.populations_metadata_schema
    + "\n {} individuals ".format(samplesData.num_individuals)
    + "\n {} variable sites.".format(samplesData.num_sites),
    flush=True,
)

end_time = time.perf_counter()
print(f"\n Making the SampleData file took {end_time - start_time:.4f} seconds")


############## Infering the ARG #######################


# Do the inference
start_time = time.perf_counter()

ts = tsinfer.infer(samplesData)
print(
    "\n \n Inferred tree sequence: {} trees over {} Mb ({} edges)".format(
        ts.num_trees, ts.sequence_length / 1e6, ts.num_edges
    )
)

ts.dump(args.out + ".tree")

end_time = time.perf_counter()
print(f"\n Infering the ARG took {end_time - start_time:.4f} seconds")

print("\n Done!")
