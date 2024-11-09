import tsinfer
import tskit as ts


################# Argparse arguments ######################

import argparse
parser = argparse.ArgumentParser()


############### Loading in data ############ 

tree1 = ts.load("output/sampleData/chr_20_5EUR.samples.tree")
tree2 = ts.load("output/sampleData/chr_20_5EUR_undef.samples.tree")

print(tree1.individuals())

#print(tree1.kc_distance(tree2))

tree1.draw_svg(path = "figure.svg")

#tree1.simplify(['HG00100'])
