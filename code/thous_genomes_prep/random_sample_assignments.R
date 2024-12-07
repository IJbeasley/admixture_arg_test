

# Get YRI assignments

# bcftools query -l $samp_dir/chr_20_YRI.bcf > output/randomised_pop_assigns/chr_20_YRI.txt 

# Get GBR 

# bcftools query -l $samp_dir/chr_20_GBR.bcf > output/randomised_pop_assigns/chr_20_GBR.txt 

df = data.table::fread("output/randomised_pop_assigns/chr_20_GBR.txt",
                       header = F)

df2 = df |> 
  dplyr::mutate(pop = "GBR")

data.table::fwrite(file = "output/randomised_pop_assigns/chr_20_GBR_all_GBR.txt",
                   df2,
                   sep = ",",
                   col.names = F)

df2 = df |> 
  dplyr::mutate(pop = sample(c("GBR", "NR"), 
          size = nrow(df), 
          replace = T,
          prob = c(0.9, 0.1)))

data.table::fwrite(file = "output/randomised_pop_assigns/chr_20_GBR_0.1_NR.txt",
                   df2,
                   sep = ",",
                   col.names = F)


df2 = df |> 
  dplyr::mutate(pop = sample(c("GBR", "NR"), 
                             size = nrow(df), 
                             replace = T,
                             prob = c(0.75, 0.25)))

data.table::fwrite(file = "output/randomised_pop_assigns/chr_20_GBR_0.25_NR.txt",
                   df2,
                   sep = ",",
                   col.names = F)



df2 = df |> 
  dplyr::mutate(pop = sample(c("GBR", "NR"), 
                             size = nrow(df), 
                             replace = T,
                             prob = c(0.5, 0.5)))

data.table::fwrite(file = "output/randomised_pop_assigns/chr_20_GBR_0.5_NR.txt",
                   df2,
                   sep = ",",
                   col.names = F)
