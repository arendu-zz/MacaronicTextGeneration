__author__ = 'arenduchintala'
"""
This script accepts a SegmentState object that is created by bisegmentation search.
The SegmentState has recursivly bisegmented a bitext
"""


def get_state(root_node):
    state_bt = ''
    S = [root_node]
    while len(S) > 0:
        current_node = S.pop()
        if current_node.display:
            state_bt += '1'
        else:
            state_bt += '0'
        for c in current_node.get_children():
            S.append(c)
    return state_bt


def push_ticks(root_node, push_node):
    S = [root_node]
    while len(S) > 0:
        current_node = S.pop()
        if str(current_node) == str(push_node) and len(current_node.get_children()) > 0:
            current_node.display = False
            for c in current_node.get_children():
                c.display = True
        for c in current_node.get_children():
            S.append(c)
    return root_node


def display_ticks(root_node):
    display_items = []
    S = [root_node]
    while len(S) > 0:
        current_node = S.pop()
        if current_node.display:
            display_items.append(current_node)
        for c in current_node.get_children():
            S.append(c)
    return display_items


global tree_stack, tree_stack_states, json
tree_stack = {}
tree_stack_states = []
json = []


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


def print_levels(segmentstate):
    lvl = 0
    d_prev = ()
    cond = True
    while cond:
        d1 = tuple(segmentstate.display_child_alignments(lvl))
        if d1 == d_prev:
            cond = False
        else:
            d_prev = d1
            t, f = zip(*d1)
            print ' | '.join(list(t))
            print ' | '.join(list(f)), '\n'
        lvl += 1


def get_json(segmentstate):
    json = []
    push_tree_stack(segmentstate)
    while len(tree_stack) > 0:
        current_root = pop_tree_stack()
        current_display_nodes = display_ticks(current_root)
        current_display_nodes.sort(key=lambda x: x.target_span[0])
        disp = [str(i) for i in current_display_nodes]
        # print ' '.join(disp)
        tar = [' '.join(i.target) for i in current_display_nodes]
        src = [' '.join(i.source) for i in current_display_nodes]

        for i in xrange(len(tar)):
            print (tar[i], src[i])

            children.append((tar[i], src[i]))

        for cdn in current_display_nodes:
            root_cpy = current_root.deepcopy()
            push_ticks(root_cpy, cdn)
            push_tree_stack(root_cpy)
    return json


def print_cuts(segmentstate):
    push_tree_stack(segmentstate)
    while len(tree_stack) > 0:
        current_root = pop_tree_stack()
        current_display_nodes = display_ticks(current_root)
        current_display_nodes.sort(key=lambda x: x.target_span[0])
        disp = [str(i) for i in current_display_nodes]
        # print ' '.join(disp)
        tar = [' '.join(i.target) for i in current_display_nodes]
        src = [' '.join(i.source) for i in current_display_nodes]
        for i in xrange(len(tar)):
            m = max(len(tar[i]), len(src[i]))
            tar[i] = tar[i].center(m)
            src[i] = src[i].center(m)
        print ' | '.join(tar)
        print ' | '.join(src), '\n'
        for cdn in current_display_nodes:
            root_cpy = current_root.deepcopy()
            push_ticks(root_cpy, cdn)
            push_tree_stack(root_cpy)
