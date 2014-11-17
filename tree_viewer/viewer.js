(function(window, document, undefined) {

	document.addEventListener('DOMContentLoaded', function() {

		var svg = document.getElementsByTagName('svg')[0];

		window.scrollTo(0, 0);

		// Convert JSON to HTML structure
		var tree = window.JSON.parse(document.getElementsByTagName('script')[0].innerText);
		
		document.body.appendChild(makeTree(tree));

		// Draw connections
		var nodes = document.getElementsByClassName('node');

		for(var i = 0, length = nodes.length; i < length; i++) {

			var parent = getParent(nodes[i]);

			if(parent !== null) {

				var nodeRect = nodes[i].getBoundingClientRect(),
					parentRect = parent.getBoundingClientRect();

				var x1 = nodeRect.left + nodes[i].offsetWidth / 2,
					y1 = nodeRect.top + 1,

					x2 = parentRect.left + parent.offsetWidth / 2,
					y2 = parentRect.bottom - 1;

				drawLine(svg, x1, y1, x2, y2);
			}
		}

	}, false);

	function makeTree(tree) {

		var group = document.createElement('div');
		group.className = 'group';

		var node = document.createElement('div');
		node.className = 'node';
		node.innerHTML = '<span class="source">' + (tree.source === '' ? '""' : tree.source) + '</span><br><span class="target">' + (tree.target === '' ? '""' : tree.target) + '</span>';

		group.appendChild(node);

		if(tree.children.length > 0) {

			var children = document.createElement('div');
			children.className = 'children';

			for(var i = 0, length = tree.children.length; i < length; i++) {

				children.appendChild(makeTree(tree.children[i]));
			}

			group.appendChild(children);
		}

		return group;
	}

	function getParent(node) {

		var possibleParent = node.parentNode.parentNode.parentNode.firstElementChild;

		if('classList' in possibleParent && possibleParent.classList.contains('node')) {

			return possibleParent;
		}

		return null;
	}

	function drawLine(svg, x1, y1, x2, y2) {

		var line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
		line.setAttribute('x1', x1);
		line.setAttribute('y1', y1);
		line.setAttribute('x2', x2);
		line.setAttribute('y2', y2);
		line.setAttribute('stroke', 'black');
		line.setAttribute('stroke-width', '3');

		svg.appendChild(line);
	}

})(window, window.document);
