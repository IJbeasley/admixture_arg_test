import tsinfer
import tskit as ts
import numpy as np

################# Argparse arguments ######################

import argparse
parser = argparse.ArgumentParser()

# Optional inputs
req_group = parser.add_argument_group(title='REQUIRED INPUT')

req_group.add_argument('-tree', '-t', 
                       help='Tree file', 
                       required=True
                       )
req_group.add_argument('-pop_assign', 
                       help = 'Text file assigning samples to populations',
                       required=True
                       )

args = parser.parse_args()


############### Loading in data ############ 

print("\n Load in tree + sample data")

tree = ts.load(args.tree)
# tree1 = ts.load("output/sampleData/chr_20_5EUR.samples.tree")
# tree2 = ts.load("output/sampleData/chr_20_5EUR_undef.samples.tree")

pop_assign = np.loadtxt(args.pop_assign, 
                              dtype='U10', 
                              delimiter=','
                              )
      
samples_id = np.unique(pop_assign[:, 0])


############## Genealogical Nearest Neighbours ################

print("\n Assesing genealogical nearest neighbours")

# tree.genealogical_nearest_neighbours(focal = ["HG00096"], 
#                                      sample_sets = ["HG00099", "HG00100", "HG00101"])
#
all_samples = range(0,len(tree.samples()))
#print(all_samples)

gnn_mat = np.empty((len(all_samples), len(all_samples)))

for sample_id in all_samples: 
  # make list of lists for samples to compare to: 
  #to_compare = [id for id in all_samples if id != sample_id]
  to_compare = [[id] for id in all_samples]
  
  gnn = tree.genealogical_nearest_neighbours(focal = [sample_id], 
                                             sample_sets = to_compare)
  
  gnn_mat[sample_id, :] = gnn
  #print(gnn)
  
print(gnn_mat)
np.savetxt("matrix.csv", gnn_mat, delimiter = ",")
############ Individuals #################

# idk about that 
# print("Individuals")
# print(tree.individuals())

# working
# print("samples")
# print(tree.samples())

########### KC distance ###############

#print(tree1.kc_distance(tree2))

############ Draw Tree ##########

# works
#tree.draw_svg(path = "figure.svg")

#tree1.simplify(['HG00100'])
