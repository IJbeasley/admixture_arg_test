import tsinfer
import tskit as ts
import numpy as np
import sys 

################# Argparse arguments ######################

import argparse
parser = argparse.ArgumentParser(description="Use tskit to investigate a single tree")

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
req_group.add_argument('-out_matrix', '-o', 
                       help = 'GNN output matrix (saved as csv)',
                       required=True
                       )

args = parser.parse_args()


############### Loading in data ############ 

print("\n Load in tree + sample data")

tree = ts.load(args.tree)

print(type(tree))
print(tree.metadata)
print(tree.nodes_population)
print(len(tree.nodes_population))
print(tree.nodes_individual)

print("Number of populations")
print(tree.num_populations)

print("Number of nodes")
print(tree.num_nodes)

print("Number of samples")
print(tree.num_samples)

print(tree.samples)

# pop_assign is a 2d-array
# rows are individuals, 
# columns are 1000 genomes sample IDs & population label
pop_assign = np.loadtxt(args.pop_assign, 
                              dtype='U10', 
                              delimiter=','
                              )
                              
# duplicate each row so that each row refers to a chromosome                            
pop_assign = np.repeat(pop_assign, repeats=2, axis=0)      

# make a sample id column that is compatible with tskit

# Generate a column of row numbers
row_numbers = np.arange(pop_assign.shape[0]).reshape(-1, 1)
# Add the row numbers as a new column to pop_assign
pop_assign = np.hstack((pop_assign, row_numbers.astype(int)))

print(pop_assign[:5,])

# get the all the population labels - and turn them into numbers
all_populations = np.unique(pop_assign[:, 1])


tree.genealogical_nearest_neighbours(focal = [1,2], 
                                             sample_sets = [[3,4], [5]])

#sys.exit()

############## Genealogical Nearest Neighbours ################

print("\n Assesing genealogical nearest neighbours")

all_samples = np.unique(pop_assign[:,0])
#range(0,len(tree.samples()))


gnn_mat = np.empty((tree.num_samples, len(all_populations)))

                   
pop_assign[:, 2] = pop_assign[:, 2].astype(int)

for sample_id in all_samples: 
  # make list of lists for samples to compare to: 
  #to_compare = [id for id in all_samples if id != sample_id]
  focal_set = pop_assign[pop_assign[:, 0] == sample_id]
  print(sample_id)

  #print(focal_set)
  focal_set = [int(id) for id in focal_set[:, 2]]
  #focal_set = [[id] for id in focal_set[:, 2]]
  print(focal_set)
  
  grouped_samples = {pop: [] for pop in all_populations}
  compare_set = pop_assign[pop_assign[:, 0] != str(sample_id)]
  
  # then form a list of lists 
  for thous_sample_id, population_id, tskit_id in compare_set:
      grouped_samples[population_id].append(int(tskit_id))
      
  # Step 3: Convert to a list of lists
  list_of_compare_samples = list(grouped_samples.values())
  print("Not OK")
  
  gnn = tree.genealogical_nearest_neighbours(focal = focal_set, 
                                             sample_sets = list_of_compare_samples)
  
  print("OK")
  
  print(gnn.shape)
 
  gnn_mat[focal_set, :] = gnn
  
print(gnn_mat)

np.savetxt(args.out_matrix, 
           gnn_mat, 
           delimiter = ",")


