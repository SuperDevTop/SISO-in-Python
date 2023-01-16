from graph import Graph, Path

def verifyULongerPath(I, S, H):
    ###########################################################################
    #
    # TODO HW2 - implement a polytime verifier that:
    #
    # - Only returns 'unsure' or 'correct'
    # - Only returns 'correct' if the given instance is a positive instance,
    #   the proposed solution is "yes" and the hint is a valid proof of that
    #   positive instance (i.e. a simple path that starts and ends at the right
    #   place and is sufficiently long.
    # - Runs in polynomial-time with respect to "I"
    #
    if S == 'no': 
        return 'unsure'
    # extract G,L from I, and convert to correct data types etc.
    splits = I.split(';')

    G = splits[0] #Graph
    startNode = splits[1]
    endNode = splits[2]
    L = splits[3]  # length

    G = Graph(G, weighted=False, directed=False); 
    L = int(L)
    
    hints = H.split(',')
    cycle = Path(hints)

    if len(hints) >= L and \
        G.isPath(cycle) and \
        cycle.start() == startNode and \
        cycle.end() == endNode:

        return 'correct'
    else:
        return 'unsure'
    ###########################################################################

    # raise NotImplementedError('implement me')

## TEST CASES #################################################################
##
## Do not modify anything below this line

import unittest

class TestVerify(unittest.TestCase):
    POSITIVE_CASES_WITH_VALID_HINTS = [
        ('v1,v2 v1,v4 v2,v3 v2,v5 v3,v4 v4,v5;v1;v3;2', 'v1,v2,v3'),
        ('v1,v2 v1,v4 v2,v3 v2,v5 v3,v4 v4,v5;v1;v3;2', 'v1,v4,v3'),
        ('v1,v2 v1,v4 v2,v3 v2,v5 v3,v4 v4,v5;v1;v3;2', 'v1,v2,v5,v4,v3'),
        ('v1,v2 v1,v4 v2,v3 v2,v5 v3,v4 v4,v5;v1;v3;3', 'v1,v2,v3'),
        ('v1,v2 v1,v4 v2,v3 v2,v5 v3,v4 v4,v5;v1;v3;3', 'v1,v4,v3'),
        ('v1,v2 v1,v4 v2,v3 v2,v5 v3,v4 v4,v5;v1;v3;3', 'v1,v2,v5,v4,v3'),
        ('v1,v2 v1,v4 v2,v3 v2,v5 v3,v4 v4,v5;v1;v3;4', 'v1,v2,v5,v4,v3'),
        ('v1,v2 v1,v4 v2,v3 v2,v5 v3,v4 v4,v5;v1;v3;5', 'v1,v2,v5,v4,v3'),
    ]

    def test_correct(self):
        for inp, path in self.POSITIVE_CASES_WITH_VALID_HINTS:
            self.assertEqual(verifyULongerPath(inp, 'yes', path), 'correct')

    def test_path_in_hint_has_wrong_start(self):
        # Hint is a valid path, but it does not start with the requested
        # starting node. There are other valid paths that start on that node,
        # but the hint is not one of them.
        inp = 'v1,v2 v1,v4 v2,v3 v2,v5 v3,v4 v4,v5;v1;v3;2'
        path = 'v5,v4,v3'
        self.assertEqual(verifyULongerPath(inp, 'yes', path), 'unsure')

    def test_path_in_hint_has_wrong_end(self):
        # Hint is a valid path, but it does not start with the requested
        # ending node. There are other valid paths that end on that node, but
        # the hint is not one of them.
        inp = 'v1,v2 v1,v4 v2,v3 v2,v5 v3,v4 v4,v5;v1;v3;2'
        path = 'v1,v4,v5'
        self.assertEqual(verifyULongerPath(inp, 'yes', path), 'unsure')

    def test_invalid_path_in_hint(self):
        # Hint is not a valid path. There are other valid paths of the right
        # length, but the hint is not one of them.
        inp = 'v1,v2 v1,v4 v2,v3 v2,v5 v3,v4 v4,v5;v1;v3;2'
        path = 'v1,v5,v3'
        self.assertEqual(verifyULongerPath(inp, 'yes', path), 'unsure')

    def test_path_too_short_in_hint(self):
        # Hint is a path that's too short, even though it's a valid path. There
        # are other valid paths that are sufficiently long, but the hint is not
        # one of them.
        inp = 'v1,v2 v1,v4 v2,v3 v2,v5 v3,v4 v4,v5;v1;v3;4'
        path = 'v1,v2,v3'
        self.assertEqual(verifyULongerPath(inp, 'yes', path), 'unsure')

    def test_path_has_repeated_nodes_in_hint(self):
        # Hint is a path with repeated nodes. There are simple paths that are
        # sufficiently long, but the hint is not one of them.
        inp = 'v1,v2 v1,v4 v2,v3 v2,v5 v3,v4 v4,v5;v1;v3;2'
        path = 'v1,v2,v1,v2,v3'
        self.assertEqual(verifyULongerPath(inp, 'yes', path), 'unsure')

    def test_hint_is_excessively_long(self):
        # Hint is a path that is excessively long. Guarding against such hints
        # is needed to ensure that the verifier runs in polynomial-time.
        #
        # Technically, the only way to have an excessively long hint is for the
        # hint to be invalid: either incorrectly formatted, or the path has
        # repeated nodes. Thus, some other checks will cover these cases, but
        # for the verifier to be a polytime verifier, it must guard against
        # these cases by checking the length explicitly.
        inp = 'v1,v2 v1,v4 v2,v3 v2,v5 v3,v4 v4,v5;v1;v3;2'
        path = 'v1,v2,v5,v4,v1,v2,v5,v4,v1,v2,v5,v4,v1,v2,v5,v4,v3'
        self.assertEqual(verifyULongerPath(inp, 'yes', path), 'unsure')

    def test_no_such_path_but_hint_says_there_is_one(self):
        # There is no path that's sufficiently long. The hint gives a path that
        # doesn't exist, and the proposed solution is "yes". Neither can be
        # correct, so the verifier must return "unsure".
        inp = 'v1,v2 v1,v4 v2,v3 v2,v5 v3,v4 v4,v5;v1;v3;5'
        path = 'v3,v2,v1,v5,v4'
        self.assertEqual(verifyULongerPath(inp, 'yes', path), 'unsure')

    def test_proposed_solution_is_no(self):
        # Hint is a valid path, but because the proposed solution is not "yes",
        # the verifier should ignore the hint and return "unsure".
        inp = 'v1,v2 v1,v4 v2,v3 v2,v5 v3,v4 v4,v5;v1;v3;2'
        path = 'v1,v2,v3'
        self.assertEqual(verifyULongerPath(inp, 'no', path), 'unsure')

if __name__ == '__main__':
    unittest.main()
