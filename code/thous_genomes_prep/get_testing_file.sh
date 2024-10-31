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
#$ -N thous_genomes

# How much RAM per slot
#$ -l mem_free=1G

#$ -l scratch=2G      # job requires up to 2 GiB of local /scratch space

# The maximum running time of the job in hours:mins:sec (converted to 10 minutes):
#$ -l h_rt=0:10:00

# Partition for the job (SGE equivalent is specifying the queue):
#$ -q short.q

module load CBI
module load htslib/1.21
module load bcftools/1.21

# wget ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000_genomes_project/release/20181203_biallelic_SNV/ALL.chr20.shapeit2_integrated_v1a.GRCh38.20181129.phased.vcf.gz.tbi

chr_num=20
save_filename=data/thus_genomes/thous_snv_bi_chr_$chr_num

echo "Get bcf file for5 european samples"
bcftools view $save_filename.bcf -s HG00096,HG00097,HG00099,HG00100,HG00101 -O b -o output/chr_20_5EUR.bcf

bcftools head output/chr_20_5EUR.bcf -n 5

