

{
  library(ggplot2)
  library(viridis)
  library(reshape2)
  library(circlize)
  library(ComplexHeatmap)
}

{
#mat = read.csv("matrix.csv", header = F)
mat = read.csv("all_GBR_samples_undef.csv", header = F)
mat = read.csv("GBR_0.5_NR.samples_undef.csv", header = F)
mat = read.csv("GBR_0.25_NR.samples_undef.csv", header = F)
mat = read.csv("GBR_0.1_NR.samples_undef.csv", header = F)
mat = as.matrix(mat)
}



{
# col_fun = colorRamp2(seq(from = 0, to = 1, length.out = 10),
#                      viridis::magma(n = 10),
#                      space = "RGB")

  
  col_fun = colorRamp2(seq(from = 0, to = max(mat), length.out = 10),
                       viridis::magma(n = 10),
                       space = "RGB")
  

plot =    ComplexHeatmap::Heatmap(mat = mat,
                                  col = col_fun,
                                  show_column_names = F,
                                  cluster_columns = T,
                                  cluster_rows = T,
                                  name = "GNN  ",
                                  heatmap_legend_param = list(
                                    direction = "horizontal",
                                    title_position = "leftcenter",
                                    title_gp = gpar(fontsize = 46),  # Title font size
                                    labels_gp = gpar(fontsize = 36), # Label font size
                                    legend_height = unit(7, "cm"),   # Height of the legend (optional)
                                    legend_width = unit(10, "cm")     # Width of the legend (optional)
                                  )
                                  )


ComplexHeatmap::draw(
  plot, 
  heatmap_legend_side = "bottom"
)
}
