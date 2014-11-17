__author__ = "Bailey Parker"


from json import dumps
from collections import OrderedDict


def tree_to_json(tree, pretty=False):
	"""Convert a macaronic translated string tree into a consumable, recursive JSON format.

	Arguments:
	tree -- The tree to convert
	pretty -- if true returns nicely formatted JSON else compact JSON (default: False)

	Expectations:
	tree -- The tree is expected to be well-formed (ie. no circular references) and follow
			the following general pattern:
				Each node in the tree can be EITHER a tuple where the first element is the
				target text and the second is the source text OR each node in the tree can
				be a list where the first element is the aforementioned tuple and the
				second is a list of child nodes. By using a tuple to represent a node
				(instead of a list), you are implicitly declaring that the node has no
				children. Additionally, all tuples MUST contain 2 elements. For words that
				either fall out or are added as a product of translation, substitute an
				empty string in place of the omision of either the source or target
	"""
	
	return dumps(_tree_to_dict(tree), indent=4 if pretty else None)

def _tree_to_dict(tree):
	if isinstance(tree, tuple):
		tree = tree, []
	
	(target, source), children = tree

	return OrderedDict([
		('target', target),
		('source', source),
		('children', [_tree_to_dict(subtree) for subtree in children]),
	])
