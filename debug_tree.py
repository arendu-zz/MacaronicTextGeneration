__author__ = "Bailey Parker"

from tree_to_json import tree_to_json

with open('tree_viewer/viewer.inlined.html', 'r') as f:
	viewer_template = f.read()

def debug_tree(tree, filename=None):
	"""Create a visual representation of a macaronic tree (useful for debugging).

	Arguments:
	tree -- The tree to convert
	filename -- The filename to save the viewer html file as (default: The source text at tree's root)
	"""

	name = tree[0][1]

	if not filename:
		filename = '{}.html'.format(name.rstrip('.').strip())

	with open(filename, 'w') as f:
		f.write(viewer_template.replace('{name}', name).replace('{tree}', tree_to_json(tree)))
