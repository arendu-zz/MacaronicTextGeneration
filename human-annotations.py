__author__ = 'arenduchintala'
"""
Takes in a tree text file as input. e.g. output/bottom-up-tree.out.pruned.1.txt
"""
import codecs, pdb

if __name__ == '__main__':
    txt_trees = codecs.open('outputs/bottom-up-tree.out.pruned.10.txt', 'r', 'utf-8').read().rstrip().split('\n\n')
    for a_tree in txt_trees:
        tree_lines = a_tree.split('\n')[1:]
        print 'full english:', tree_lines[0]
        print 'middle cut  :', tree_lines[len(tree_lines) / 2]
        print 'full german :', tree_lines[len(tree_lines) - 1]
        print ''


