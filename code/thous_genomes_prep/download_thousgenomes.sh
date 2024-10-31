#!/bin/bash

module load CBI
module load htslib/1.21
module load bcftools/1.21

chromosomes=(20)
data_dir=data/thous_genomes
out_dir=output/thous_genomes_bcf

for chr_num in "${chromosomes[@]}"; do

    save_filename=thous_snv_bi_chr_$chr_num



    echo "Downloading data for chromosome $chr_num"
    
    url=ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000_genomes_project/release/20181203_biallelic_SNV/ALL.chr$chr_num.shapeit2_integrated_v1a.GRCh38.20181129.phased.vcf.gz
 
    wget -nc -O  $data_dir/$save_filename.vcf.gz $url
    
    
    
    echo "Saving files as bcfs .. "
    
    if [ ! -f $data_dir/$save_filename.vcf ]; then
       
       gunzip -k $data_dir/$save_filename.vcf.gz
       
    fi
    
    #gunzip -k $data_dir/$save_filename.vcf.gz
    
    bcftools view $data_dir/$save_filename.vcf -O b -o $out_dir/$save_filename.bcf
    
    
    echo "Removing temporary vcf"
    
    rm $data_dir/$save_filename.vcf 
    
done
