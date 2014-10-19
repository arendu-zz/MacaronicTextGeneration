__author__ = 'arenduchintala'


class SegmentState:
    def __init__(self, target_span, source_span, target, source):
        self.target_span = target_span
        self.source_span = source_span
        self.target = target
        self.source = source
        self.cov_target = [False] * len(target)
        self.cov_source = [False] * len(source)
        self.alignments = []
        self.child_states = []

    def __str__(self):
        return str(self.target_span) + ' ' + ' '.join(self.target) + ' ---> ' + str(
            self.source_span) + ' ' + ' '.join(self.source)

    def update_cov_target(self, uct):
        self.cov_target = [i | j for i, j in zip(uct, self.cov_target)]

    def update_cov_source(self, ucs):
        self.cov_source = [i | j for i, j in zip(ucs, self.cov_source)]

    def compare_state(self, segment_state):
        for i, t in enumerate(self.cov_target):
            if t != segment_state.cov_target[i]:
                return False
        for i, t in enumerate(self.cov_source):
            if t != segment_state.cov_source[i]:
                return False
        return True

    def coverage_score(self):
        return self.cov_source.count(False)

    def get_score(self):
        return self.coverage_score(), len(self.alignments)

    def state_key(self):
        bt = ''.join(str(int(t)) for t in self.cov_target)
        bs = ''.join(str(int(s)) for s in self.cov_source)
        return bt + ',' + bs

    def add_alignment(self, target_span, source_span):
        self.alignments.append((target_span, source_span))

    def get_alignment_strings(self):
        alignment_strings = {}
        for a in self.alignments:
            (t_span, s_span) = a
            if s_span[0] is None and s_span[1] is None:
                alignment_strings[(t_span, s_span)] = (self.target[t_span[0]:t_span[1]], ["NULL"])
            else:
                alignment_strings[(t_span, s_span)] = (
                    self.target[t_span[0]:t_span[1]], self.source[s_span[0]:s_span[1]])
        return alignment_strings

    def get_copy(self):
        new_state = SegmentState(self.target_span, self.source_span, self.target, self.source)
        new_state.cov_target = [t for t in self.cov_target]
        new_state.cov_source = [s for s in self.cov_source]
        new_state.alignments = [a for a in self.alignments]
        return new_state