
mat = read.csv("matrix.csv", header = F)
mat = as.matrix(mat)

library(ggplot2)
library(viridis)
library(reshape2)

plot =    ComplexHeatmap::Heatmap(mat = mat)
