__author__ = 'arenduchintala'


class Node():
    def __init__(self, contents):
        self.display = False
        self.contents = contents
        self.children = []

    def __str__(self):
        return self.contents

    def deepcopy(self):
        n = Node(self.contents)
        n.display = self.display
        for c in self.children:
            n.children.append(c.deepcopy())
        return n


def get_state(root_node):
    state_bt = ''
    S = [root_node]
    while len(S) > 0:
        current_node = S.pop()
        if current_node.display:
            state_bt += '1'
        else:
            state_bt += '0'
        for c in current_node.children:
            S.append(c)
    return state_bt


def push_ticks(root_node, push_node):
    S = [root_node]
    while len(S) > 0:
        current_node = S.pop()
        if current_node.contents == push_node.contents and len(current_node.children) > 0:
            current_node.display = False
            for c in current_node.children:
                c.display = True
        for c in current_node.children:
            S.append(c)
    return root_node


def display_ticks(root_node):
    display_items = []
    S = [root_node]
    while len(S) > 0:
        current_node = S.pop()
        if current_node.display:
            display_items.append(current_node)
        for c in current_node.children:
            S.append(c)
    return display_items


global tree_stack, tree_stack_states
tree_stack = {}
tree_stack_states = []


def push_tree_stack(root_node):
    global tree_stack, tree_stack_states
    st = get_state(root_node)
    if st not in tree_stack_states:
        tree_stack[st] = root_node
        tree_stack_states.append(st)
    else:
        pass  # already seen this state


def pop_tree_stack():
    global tree_stack
    tsd = dict((get_state(rn).count('1'), get_state(rn)) for k, rn in tree_stack.items())
    top_sd = sorted(tsd)
    rt = tree_stack.pop(tsd[top_sd[0]])
    return rt


if __name__ == '__main__':
    # make tree
    n1 = Node('A-4')
    n2 = Node('B-3')
    n3 = Node('C-2')
    n4 = Node('D-1')
    n12 = Node('AB-34')
    n12.children = [n1, n2]
    n34 = Node('CD-12')
    n34.children = [n3, n4]
    n1234 = Node('ABCD-1234')
    n1234.children = [n12, n34]
    n1234.display = True

    # print get_state(n1234)
    # n1234 = push_ticks(n1234, n1234)
    # print get_state(n1234)

    push_tree_stack(n1234)

    while len(tree_stack) > 0:
        current_tree = pop_tree_stack()
        current_display_nodes = display_ticks(current_tree)
        disp = [str(i) for i in current_display_nodes]
        print ' '.join(sorted(disp))
        for cdn in current_display_nodes:
            root_cpy = current_tree.deepcopy()
            # print get_state(root_cpy)
            root_cpy = push_ticks(root_cpy, cdn)
            # print get_state(root_cpy)
            push_tree_stack(root_cpy)







    

