
mat = read.csv("matrix.csv", header = F)

library(ggplot2)
library(viridis)
library(reshape2)

XTidy = melt(mat, value.name="val", varnames = c("x", "y") )

ggplot(XTidy, aes( x, y ) ) + 
  geom_tile( aes( fill = val ) ) + 
  geom_text( aes( label = val ) ) + 
  scale_fill_viridis(name = "GNN", option = "D")
