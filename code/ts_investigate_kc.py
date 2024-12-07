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
req_group.add_argument('-tree2', '-s', 
                       help='Tree file'#, 
                      # required=True
                       )
req_group.add_argument('-pop_assign', 
                       help = 'Text file assigning samples to populations',
                       required=True
                       )

args = parser.parse_args()


############### Loading in data ############ 

print("\n Load in tree + sample data")

tree = ts.load(args.tree)
tree2 = ts.load(args.tree2)

########### KC distance ###############

import tskit

# Check if the tree has multiple roots
def ensure_single_root(tree):
    if tree.num_roots > 1:
        print(f"Tree has {tree.num_roots} roots. Adding a new root.")
        tables = tree.tree_sequence.dump_tables()
        
        # Add a new root node
        new_root = tables.nodes.add_row(time=tree.max_root_time + 1)
        for root in tree.roots:
            tables.edges.add_row(parent=new_root, child=root, left=0.0, right=tree.sequence_length)
        
        # Sort and simplify the tables
        tables.sort()
        single_root_ts = tables.tree_sequence()
        return single_root_ts.first()
    return tree

# Ensure both trees have single roots
tree1 = ensure_single_root(tree)
tree2 = ensure_single_root(tree2)

# Compute KC distance
kc_dist = tree1.kc_distance(other=tree2)
print(f"KC distance: {kc_dist}")

#print(tree2.kc_distance(other = tree))

############ Draw Tree ##########

# works
#tree.draw_svg(path = "figure.svg")

#tree1.simplify(['HG00100'])
