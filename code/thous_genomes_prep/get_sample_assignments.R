

df<- data.table::fread("data/thous_genomes/sample_assign/igsr-gbr.tsv.tsv") 

df = df |> 
     dplyr::select("Sample name")


data.table::fwrite(file = "output/thous_genomes/sample_assign/igsr-gbr.tsv",
                   df,
                   col.names = F,
                   sep = "\t")


df<- data.table::fread("data/thous_genomes/sample_assign/igsr-yri.tsv.tsv") 

df = df |> 
  dplyr::select("Sample name")


data.table::fwrite(file = "output/thous_genomes/sample_assign/igsr-yri.tsv",
                   df,
                   col.names = F,
                   sep = "\t")
