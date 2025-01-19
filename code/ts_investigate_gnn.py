import tsinfer
import tskit as ts
import numpy as np
import sys 

################# Argparse arguments ######################

import argparse
parser = argparse.ArgumentParser(description="Use tskit GNN to investigate a single tree")

# Optional inputs
req_group = parser.add_argument_group(title='REQUIRED INPUT')

req_group.add_argument('-tree', '-t', 
                       help='Tree file', 
                       required=True
                       )
req_group.add_argument('-pop_assign', 
                       help = 'Text file assigning samples to populations'
                       'if not provided, then comparisions are made between individuals',
                       default='undefined',
                       required=False
                       )
req_group.add_argument('-out_matrix', '-o', 
                       help = 'GNN output matrix (saved as csv)',
                       required=True
                       )

args = parser.parse_args()


############### Loading in data ############ 

print("\n Load in tree + sample data")

tree = ts.load(args.tree)

# print("Number of populations")
# print(tree.num_populations)
# 
# print("Number of nodes")
# print(tree.num_nodes)
# 
# print("Number of samples")
# print(tree.num_samples)

# number of num_indivs
num_indivs = int(tree.num_samples / 2)


if args.pop_assign =='undefined': 
  
   indiv_ids = range(num_indivs)
   
   pop_assign = np.column_stack((indiv_ids, indiv_ids))
   # print(pop_assign)
   # sys.exit()

# pop_assign is a 2d-array
# rows are individuals, 
# columns are 1000 genomes sample IDs & population label
   
else:
   pop_assign = np.loadtxt(args.pop_assign, 
                          dtype='U10', 
                          delimiter=','
                          )
                          
# duplicate each row so that each row refers to a chromosome    
# rather than an individual 
pop_assign = np.repeat(pop_assign, repeats=2, axis=0)      

# make a sample (chromosome) id column in pop_assign array 
# to make it compatible with tskit

# Generate a column of row numbers
row_numbers = np.arange(pop_assign.shape[0]).reshape(-1, 1)
# Add the row numbers as a new column to pop_assign
pop_assign = np.hstack((pop_assign, row_numbers.astype(int)))
# Make sure sample id is an integer
pop_assign[:, 2] = pop_assign[:, 2].astype(int)


############## Genealogical Nearest Neighbours ################

print("\n Assesing genealogical nearest neighbours")

# items to iterate against: 

# array of indidividuals to iterate against
all_individs = np.unique(pop_assign[:,0])

# population labels to iterate against
all_populations = np.unique(pop_assign[:, 1])

gnn_mat = np.empty((len(all_individs), len(np.unique(all_populations)))
                   )

# make gnn for each individual: 
for individ_id in all_individs: 
  
  # get sample ids (focal nodes) 
  
  focal_set = pop_assign[pop_assign[:, 0] == individ_id]
  # get the chrom
  focal_set = [int(individ_id) for individ_id in focal_set[:, 2]]
  print(focal_set)
  
  # get samples to compare to 
  # each item in list is a list corresponding to all samples in this population
  
  compare_set = pop_assign
  #compare_set = pop_assign[pop_assign[:, 0] != sample_id]
  
  grouped_samples = {pop: [] for pop in np.unique(all_populations)}
  
  # then form a list of lists 
  for thous_sample_id, population_id, tskit_id in compare_set:
      grouped_samples[population_id].append(int(tskit_id))
  
  # Step 3: Convert to a list of lists
  list_of_compare_samples = list(grouped_samples.values())
  #print(list_of_compare_samples)
  
  gnn = tree.genealogical_nearest_neighbours(focal = focal_set, 
                                             sample_sets = list_of_compare_samples)
  
  # take the average gnn per individual                                           
  gnn = np.mean(gnn, axis = 0 )                                          
  
  gnn_mat[individ_id, :] = gnn 
  

################## saving gnn ######################

print("\n Saving GNN matrix as " + args.out_matrix)


np.savetxt(args.out_matrix, 
           gnn_mat, 
           delimiter = ",")


