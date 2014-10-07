__author__ = 'arenduchintala'


class SegmentState:
    def __init__(self, target, source, score):
        self.target = target
        self.source = source
        self.cov_target = [False] * len(target)
        self.cov_source = [False] * len(source)
        self.alignments = []
        self.score = score

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

    def disp_state(self):
        bt = [str(int(t)) for t in self.cov_target]
        bs = [str(int(s)) for s in self.cov_source]
        print self.score
        print ''.join(bt)
        print ''.join(bs)

    def state_key(self):
        return tuple(self.cov_source + self.cov_target)

    def add_alignment(self, span_matched):
        self.alignments.append(span_matched)

    def get_copy(self):
        new_state = SegmentState(self.target, self.source, self.score)
        new_state.cov_target = [t for t in self.cov_target]
        new_state.cov_source = [s for s in self.cov_source]
        new_state.alignments = [a for a in self.alignments]
        return new_state