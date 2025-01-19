#!/bin/bash

#$ -S /bin/bash     # run job as a Bash shell [IMPORTANT]
#$ -cwd             # run job in the current working directory

# Use this email address:
#$ -M isobel.beasley@ucsf.edu

# Send yourself an email when the job:
# aborts abnormally (fails), begins, and ends successfully
#$ -m abe

# Multithreaded (SMP) job: must run on one node 
#$ -pe smp 1

# The name of the job:
#$ -N test_tsinfer

# How much RAM per slot
#$ -l mem_free=10G

#$ -l scratch=2G      # job requires up to 2 GiB of local /scratch space

# The maximum running time of the job in hours:mins:sec (converted to 10 minutes):
#$ -l h_rt=0:25:00

# Partition for the job (SGE equivalent is specifying the queue):

# Check that the script is launched with qsub
if [ "x$JOB_ID" == "x" ]; then
   echo "You need to submit your job to the queuing system with qsub"
   exit 1
fi

module load CBI miniforge3/24.7.1-0
conda activate admixture_arg_test_v3

#conda create --name admixture_arg_test_v3 python=3.12
#conda install bioconda:cyvcf2=0.31.1 
#conda install conda-forge::tsinfer=0.3.3


python3 code/ts_investigate_gnn.py  \
-tree "output/sampleData/chr_20_GBR_all_GBR.samples.tree" \
-out_matrix "all_GBR_samples_undef.csv" 


python3 code/ts_investigate_gnn.py  \
-tree "output/sampleData/chr_20_GBR_0.5_NR.samples.tree" \
-out_matrix "GBR_0.5_NR.samples_undef.csv" 

python3 code/ts_investigate_gnn.py  \
-tree "output/sampleData/chr_20_GBR_0.25_NR.samples.tree" \
-out_matrix "GBR_0.25_NR.samples_undef.csv" 

python3 code/ts_investigate_gnn.py  \
-tree "output/sampleData/chr_20_GBR_0.1_NR.samples.tree" \
-out_matrix "GBR_0.1_NR.samples_undef.csv" 

#\
#-pop_assign "output/randomised_pop_assigns/chr_20_GBR_0.1_NR.txt"

python3 code/ts_investigate_gnn.py \
-tree "output/sampleData/chr_20_5EUR.samples.tree"
#-pop_assign "output/test_pop_assign.txt"
# 
# python3 code/ts_infer.py \
#         -v "output/thous_genomes_samp/chr_20_GBR.bcf" \
#         -o "output/sampleData/chr_20_GBR_all_GBR.samples" \
#         -pop_assign   "output/randomised_pop_assigns/chr_20_GBR_all_GBR.txt"
# 
# 
# python3 code/ts_infer.py \
#         -v "output/thous_genomes_samp/chr_20_GBR.bcf" \
#         -o "output/sampleData/chr_20_GBR_0.1_NR.samples" \
#         -pop_assign   "output/randomised_pop_assigns/chr_20_GBR_0.1_NR.txt"
#         
# python3 code/ts_infer.py \
#         -v "output/thous_genomes_samp/chr_20_GBR.bcf" \
#         -o "output/sampleData/chr_20_GBR_0.25_NR.samples" \
#         -pop_assign   "output/randomised_pop_assigns/chr_20_GBR_0.25_NR.txt"
# 
#         
# python3 code/ts_infer.py \
#         -v "output/thous_genomes_samp/chr_20_GBR.bcf" \
#         -o "output/sampleData/chr_20_GBR_0.5_NR.samples" \
#         -pop_assign   "output/randomised_pop_assigns/chr_20_GBR_0.5_NR.txt"
        
######################

python3 code/ts_investigate_gnn.py \
        -tree "output/sampleData/chr_20_GBR_all_GBR.samples.tree" \
        -pop_assign "output/randomised_pop_assigns/chr_20_GBR_0.1_NR.txt" \
        -out_matrix "GGBR_0.1_matrix.csv"


code/ts_investigate_gnn.py \
        -tree "output/sampleData/chr_20_GBR_0.1_NR.samples.tree" \
         -pop_assign "output/randomised_pop_assigns/chr_20_GBR_0.1_NR.txt"

python3 code/ts_investigate.py \
        -tree "output/sampleData/chr_20_GBR_all_GBR.samples.tree" \
        -tree2 "output/sampleData/chr_20_GBR_0.1_NR.samples.tree" \
        -pop_assign "output/randomised_pop_assigns/chr_20_GBR_0.1_NR.txt"
         
# python3 code/ts_investigate.py \
#         -t "output/sampleData/chr_20_5EUR.samples.tree" \
#         -pop_assign "output/test_pop_assign.txt"     
     