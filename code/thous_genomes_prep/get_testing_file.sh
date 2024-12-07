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

chr_num=20
data_dir=data/thous_genomes
out_dir=output/thous_genomes_bcf
samp_dir=output/thous_genomes_samp

save_filename=thous_snv_bi_chr_$chr_num

# echo "Get bcf file for 5 european samples"
# bcftools view $out_dir/$save_filename.bcf -s HG00096,HG00097,HG00099,HG00100,HG00101 -O b -o $samp_dir/chr_20_5EUR.bcf
# 
# echo "Remove variants fixed in this sample"
# bcftools  view $samp_dir/chr_20_5EUR.bcf -e 'AC==0 || AC==AN' -O b -o $samp_dir/chr_20_5EUR.bcf
# 
# bcftools head $samp_dir/chr_20_5EUR.bcf -n 5
# #bcftools view -H $out_dir/$save_filename.bcf | wc -l
# bcftools view -H $samp_dir/chr_20_5EUR.bcf | wc -l 

echo "Get bcf file for GBR samples"
bcftools view $out_dir/$save_filename.bcf -S output/thous_genomes/sample_assign/igsr-gbr.tsv -O b -o $samp_dir/chr_20_GBR.bcf --force-samples

echo "Remove variants fixed in this sample"
bcftools  view $samp_dir/chr_20_GBR.bcf -e 'AC==0 || AC==AN' -O b -o $samp_dir/chr_20_GBR.bcf

bcftools head $samp_dir/chr_20_GBR.bcf -n 5
#bcftools view -H $out_dir/$save_filename.bcf | wc -l
bcftools view -H $samp_dir/chr_20_GBR.bcf| wc -l 



echo "Get bcf file for GBR samples"
bcftools view $out_dir/$save_filename.bcf -S output/thous_genomes/sample_assign/igsr-yri.tsv -O b -o $samp_dir/chr_20_YRI.bcf --force-samples

echo "Remove variants fixed in this sample"
bcftools  view $samp_dir/chr_20_YRI.bcf -e 'AC==0 || AC==AN' -O b -o $samp_dir/chr_20_YRI.bcf

bcftools head $samp_dir/chr_20_YRI.bcf -n 5
#bcftools view -H $out_dir/$save_filename.bcf | wc -l
bcftools view -H $samp_dir/chr_20_YRI.bcf| wc -l 
