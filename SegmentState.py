__author__ = 'arenduchintala'

import pdb


class SegmentState(object):
    def __init__(self, target_span, source_span, target, source):
        self.target_span = target_span
        self.source_span = source_span
        self.target = target
        self.source = source
        self._cov_target = [False] * len(target)
        self._cov_source = [False] * len(source)
        self.cov_ratio = 0.0
        self.state_source = '0' * len(source)
        self.state_target = '0' * len(target)
        self.alignments = []
        self._child_states = []
        self.display = False

    def get_children(self):
        return self._child_states

    def __str__(self):
        return str(self.target_span) + ' ' + ' '.join(self.target) + ' -> ' + str(
            self.source_span) + ' ' + ' '.join(self.source)

    @property
    def cov_source(self):
        return self._cov_source;

    @cov_source.setter
    def cov_source(self, val):
        self.state_source = ''.join(str(int(t)) for t in val)
        self._cov_source = val

    @property
    def cov_target(self):
        return self._cov_target;

    @cov_target.setter
    def cov_target(self, val):
        self.state_target = ''.join(str(int(t)) for t in val)
        self._cov_target = val

    def compare_state(self, segment_state):
        for i, t in enumerate(self.cov_target):
            if t != segment_state.cov_target[i]:
                return False
        for i, t in enumerate(self.cov_source):
            if t != segment_state.cov_source[i]:
                return False
        return True


    def coverage_score(self):
        count_false = self.cov_source.count(False)
        return count_false

    def probability_score(self):
        if len(self.alignments) > 0:
            count_score = -sum([a[2] for a in self.alignments]) / float(len(self.alignments))
        else:
            count_score = 0.0
        return count_score


    def get_score(self):
        # return self.probability_score()
        return self.coverage_ratio_score()

    def coverage_ratio_score(self):
        return self.probability_score() * self.cov_ratio

    def state_key(self):
        return self.state_target + ',' + self.state_source

    def add_alignment(self, target_span, source_span, alignment_score):
        self.alignments.append((target_span, source_span, alignment_score))

    def get_alignment_strings(self):
        alignment_strings = {}
        for a in self.alignments:
            (t_span, s_span, a_score) = a
            if s_span[0] is None and s_span[1] is None:
                alignment_strings[(t_span, s_span)] = (self.target[t_span[0]:t_span[1]], ["NULL"])
            else:
                alignment_strings[(t_span, s_span)] = (
                    self.target[t_span[0]:t_span[1]], self.source[s_span[0]:s_span[1]])
        return alignment_strings

    def display_alignment_strings(self):
        a_str = self.get_alignment_strings()
        t_spaced = []
        s_spaced = []
        for (t_span, s_span) in sorted(a_str):
            (t, s) = a_str[(t_span, s_span)]
            t_str = ' '.join(t)
            s_str = ' '.join(s)
            m = max(len(t_str), len(s_str)) + 1
            t_spaced.append(t_str.center(m))
            s_spaced.append(s_str.center(m))
        print self.get_score()
        print ' | '.join(t_spaced)
        print ' | '.join(s_spaced)
        pass

    def get_copy(self):
        new_state = SegmentState(self.target_span, self.source_span,
                                 self.target, self.source)
        new_state.cov_target = [t for t in self.cov_target]
        new_state.cov_source = [s for s in self.cov_source]
        new_state.alignments = [a for a in self.alignments]
        new_state.display = self.display
        return new_state

    def display_child_alignments(self, lvl):
        if lvl == 0:
            s = ' '.join(self.source)
            s = s.strip()
            t = ' '.join(self.target)
            t = t.strip()
            m = max(len(t), len(s))
            return [(t.center(m), s.center(m))]
        if len(self.get_children()) == 0:
            s = self.source[0]
            s = s.strip()
            t = self.target[0]
            t = t.strip()
            m = max(len(t), len(s))
            return [(t.center(m), s.center(m))]
        else:
            self.get_children().sort(key=lambda x: x.target_span[0])
            disp = []
            for c in self.get_children():
                disp += c.display_child_alignments(lvl - 1)
            return disp

    def get_state(self):
        state_bt = ''
        S = [self]
        while len(S) > 0:
            current_node = S.pop()
            if current_node.display:
                state_bt += '1'
            else:
                state_bt += '0'
            for c in current_node.get_children():
                S.append(c)
        return state_bt


    def add_to_children(self, segmentstate):
        # At this point we convert relative spans positions back to original span positions
        # by adding the span start point of the parent (self is the parent)
        if segmentstate.target_span[0] == None and segmentstate.target_span[1] == None:
            pass
        else:
            segmentstate.target_span = (segmentstate.target_span[0] + self.target_span[0],
                                        segmentstate.target_span[1] + self.target_span[0])
        if segmentstate.source_span[0] == None and segmentstate.source_span[1] == None:
            if len(segmentstate.source_span) == 3 and len(segmentstate.source) == 1:
                segmentstate.source[0] = segmentstate.source_span[2]
            else:
                pass  # pdb.set_trace()
        else:
            segmentstate.source_span = (segmentstate.source_span[0] + self.source_span[0],
                                        segmentstate.source_span[1] + self.source_span[0])
        self._child_states.append(segmentstate)

    def deepcopy(self):
        cpy = self.get_copy()
        for c in self._child_states:
            cpy._child_states.append(c.deepcopy())
        return cpy


    def get_recursive_rep(self):
        if not self.get_children():
            return ' '.join(self.source), ' '.join(self.target)
        else:
            c = []
            for child in self.get_children():
                c.append(child.get_recursive_rep())
            return [(' '.join(self.source), ' '.join(self.target)), c]

