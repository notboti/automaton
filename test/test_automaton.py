# -*- coding: utf-8 -*-
# @author <lambda.coder@gmail.com>

from unittest import TestCase

from automaton.automaton import MutableAutomatonException
from automaton.automaton import MutableAutomaton
from automaton.automaton import MutableAutomatonWithDefaultSuccessor


class MutableAutomatonTestCase(TestCase):
    def test_construction(self):
        f = MutableAutomaton()
        self.assertEqual(f.get_letters(), [])
        s0 = f.get_initial_state()
        self.assertEqual(s0, 0)
        self.assertEqual(f.get_states(), [s0])
        self.assertEqual(f.get_final_states(), [])
        self.assertEqual(f.to_dict(), {'initial': s0, 'finals': set(), 'outputs': {}, 'transitions': {s0: {}}})

    def test_add_state(self):
        f = MutableAutomaton()
        s0 = f.get_initial_state()
        s1 = f.add_state()
        self.assertEqual(f.get_states(), [s0, s1])
        self.assertEqual(f.to_dict(), {'initial': s0, 'finals': set(), 'outputs': {}, 'transitions': {s0: {}, s1: {}}})
        s2 = f.add_state()
        self.assertEqual(f.get_states(), [s0, s1, s2])
        self.assertEqual(f.to_dict(),
                         {'initial': s0, 'finals': set(), 'outputs': {}, 'transitions': {s0: {}, s2: {}, s1: {}}})

    def test_add_transition_with_empty_word(self):
        f = MutableAutomaton()
        s0 = f.get_initial_state()
        self.assertRaises(MutableAutomatonException, f.add_transition, s0, '', s0)

    def test_add_transition(self):
        f = MutableAutomaton()
        s0 = f.get_initial_state()
        s1 = f.add_state()
        s2 = f.add_state()
        # s0 a s1
        f.add_transition(s0, 'a', s1)
        self.assertEqual(f.to_dict(), {'initial': s0, 'finals': set(), 'outputs': {},
                                       'transitions': {s0: {'a': s1}, s1: {}, s2: {}}})
        t = f.get_target(s0, 'a')
        self.assertEqual(t, s1)
        self.assertEqual(f.get_letters(), ['a'])
        # s0 b s2
        f.add_transition(s0, 'b', s2)
        self.assertEqual(f.to_dict(),
                         {'initial': s0, 'finals': set(), 'outputs': {},
                          'transitions': {s0: {'a': s1, 'b': s2}, s1: {}, s2: {}}})
        t = f.get_target(s0, 'b')
        self.assertEqual(t, s2)
        self.assertEqual(f.get_letters(), ['a', 'b'])
        # s1 a s0
        f.add_transition(s1, 'a', s0)
        self.assertEqual(f.to_dict(),
                         {'initial': s0, 'finals': set(), 'outputs': {},
                          'transitions': {s0: {'a': s1, 'b': s2}, s1: {'a': s0}, s2: {}}})
        t = f.get_target(s1, 'a')
        self.assertEqual(t, s0)
        # s0 a s2
        f.add_transition(s0, 'a', s2)
        self.assertEqual(f.to_dict(),
                         {'initial': s0, 'finals': set(), 'outputs': {},
                          'transitions': {s0: {'a': s2, 'b': s2}, s1: {'a': s0}, s2: {}}})
        t = f.get_target(s0, 'a')
        self.assertEqual(t, s2)

    def test_final_state(self):
        f = MutableAutomaton()
        s0 = f.get_initial_state()
        s1 = f.add_state()
        self.assertEqual(f.get_final_states(), [])
        f.set_final_state(s1)
        self.assertEqual(f.get_final_states(), [s1])
        self.assertEqual(f.to_dict(), {'initial': s0, 'finals': {s1}, 'outputs': {}, 'transitions': {s0: {}, s1: {}}})
        s2 = f.add_state()
        f.set_final_state(s2)
        self.assertEqual(f.get_final_states(), [s1, s2])
        self.assertEqual(f.to_dict(),
                         {'initial': s0, 'finals': {s1, s2}, 'outputs': {}, 'transitions': {s0: {}, s1: {}, s2: {}}})

    def test_is_final_state(self):
        f = MutableAutomaton()
        s0 = f.get_initial_state()
        self.assertFalse(f.is_final_state(s0))
        s1 = f.add_state()
        f.set_final_state(s1)
        self.assertFalse(f.is_final_state(s0))
        self.assertTrue(f.is_final_state(s1))
        f.set_final_state(s0)
        self.assertTrue(f.is_final_state(s0))

    def test_accept(self):
        # build some fsa
        f = MutableAutomaton()
        s0 = f.get_initial_state()
        s1 = f.add_state()
        f.add_transition(s0, 'a', s1).add_transition(s1, 'a', s0).set_final_state(s1)
        self.assertEqual(f.to_dict(),
                         {'initial': s0, 'finals': {s1}, 'outputs': {}, 'transitions': {s0: {'a': s1}, s1: {'a': s0}}})
        # test accept
        # empty word is not accepted
        self.assertFalse(f.accept(''))
        # a is accepted
        self.assertTrue(f.accept('a'))
        # aa is not accepted
        self.assertFalse(f.accept('aa'))
        # aaa is not accepted
        self.assertTrue(f.accept('aaa'))
        # b is not accepted
        self.assertFalse(f.accept('b'))

    def test_det_search_ab_babb_bb(self):
        # build some fsa
        f = MutableAutomaton()
        s0 = f.get_initial_state()
        s1 = f.add_state()
        s2 = f.add_state()
        s3 = f.add_state()
        s4 = f.add_state()
        s5 = f.add_state()
        s6 = f.add_state()
        s7 = f.add_state()
        f.add_transition(s0, 'a', s1).add_transition(s0, 'b', s3)
        f.add_transition(s1, 'a', s1).add_transition(s1, 'b', s2)
        f.add_transition(s2, 'a', s4).add_transition(s2, 'b', s7)
        f.add_transition(s3, 'a', s4).add_transition(s3, 'b', s7)
        f.add_transition(s4, 'a', s1).add_transition(s4, 'b', s5)
        f.add_transition(s5, 'a', s4).add_transition(s5, 'b', s6)
        f.add_transition(s6, 'a', s4).add_transition(s6, 'b', s7)
        f.add_transition(s7, 'a', s4).add_transition(s7, 'b', s7)
        f.set_final_state(s2).set_final_state(s5).set_final_state(s6).set_final_state(s7)
        f.add_output(s2, 'ab').add_output(s5, 'ab').add_output(s6, 'bb').add_output(s6, 'babb').add_output(s7, 'bb')
        self.assertEqual(f.to_dict(), {'initial': s0, 'finals': {s2, s5, s6, s7},
                                       'outputs': {s2: ['ab'], s5: ['ab'], s6: ['babb', 'bb'], s7: ['bb']},
                                       'transitions': {s0: {'a': s1, 'b': s3}, s1: {'a': s1, 'b': s2},
                                                       s2: {'a': s4, 'b': s7}, s3: {'a': s4, 'b': s7},
                                                       s4: {'a': s1, 'b': s5}, s5: {'a': s4, 'b': s6},
                                                       s6: {'a': s4, 'b': s7}, s7: {'a': s4, 'b': s7}}})
        self.assertEqual(f.get_letters(), ['a', 'b'])
        # test det_search simulation on babba
        self.assertEqual(f.get_target(s0, 'b'), s3)
        self.assertEqual(f.get_target(s3, 'a'), s4)
        self.assertEqual(f.get_target(s4, 'b'), s5)
        self.assertEqual(f.get_target(s5, 'b'), s6)
        self.assertEqual(f.get_target(s6, 'a'), s4)
        # test det_search
        outputs = f.search('babba')
        # babba
        # 01234
        self.assertEqual(outputs, [('ab', 1, 3), ('babb', 0, 4), ('bb', 2, 4)])
        for o in outputs:
            self.assertEqual('babba'[o[1]:o[2]], o[0])

    def test_det_search_ab_aa(self):
        f = MutableAutomaton()
        s0 = f.get_initial_state()
        s1 = f.add_state()
        s2 = f.add_state()
        s3 = f.add_state()
        f.add_transition(s0, 'a', s1)
        f.add_transition(s1, 'a', s2).add_transition(s1, 'b', s3)
        f.set_final_state(s2).set_final_state(s3)
        f.add_output(s2, 'aa').add_output(s3, 'ab')
        self.assertEqual(f.search('a ab aa'), [])

    def test_output_stuff(self):
        f = MutableAutomaton()
        s0 = f.get_initial_state()
        self.assertEqual(f.get_outputs(s0), set())
        self.assertEqual(f.to_dict(), {'initial': s0, 'finals': set(), 'outputs': {}, 'transitions': {s0: {}}})
        f.add_output(s0, 1)
        self.assertEqual(f.get_outputs(s0), {1})
        self.assertEqual(f.to_dict(), {'initial': s0, 'finals': set(), 'outputs': {s0: [1]}, 'transitions': {s0: {}}})
        f.add_output(s0, 2)
        self.assertEqual(f.get_outputs(s0), {1, 2})
        self.assertEqual(f.to_dict(),
                         {'initial': s0, 'finals': set(), 'outputs': {s0: [1, 2]}, 'transitions': {s0: {}}})
        f.add_output(s0, 1)
        self.assertEqual(f.get_outputs(s0), {1, 2})
        self.assertEqual(f.to_dict(),
                         {'initial': s0, 'finals': set(), 'outputs': {s0: [1, 2]}, 'transitions': {s0: {}}})

    def test_get_stats(self):
        # build some fsa
        f = MutableAutomaton()
        s0 = f.get_initial_state()
        s1 = f.add_state()
        s2 = f.add_state()
        s3 = f.add_state()
        s4 = f.add_state()
        s5 = f.add_state()
        s6 = f.add_state()
        s7 = f.add_state()
        f.add_transition(s0, 'a', s1).add_transition(s0, 'b', s3)
        f.add_transition(s1, 'a', s1).add_transition(s1, 'b', s2)
        f.add_transition(s2, 'a', s4).add_transition(s2, 'b', s7)
        f.add_transition(s3, 'a', s4).add_transition(s3, 'b', s7)
        f.add_transition(s4, 'a', s1).add_transition(s4, 'b', s5)
        f.add_transition(s5, 'a', s4).add_transition(s5, 'b', s6)
        f.add_transition(s6, 'a', s4).add_transition(s6, 'b', s7)
        f.add_transition(s7, 'a', s4).add_transition(s7, 'b', s7)
        f.set_final_state(s2).set_final_state(s5).set_final_state(s6).set_final_state(s7)
        f.add_output(s2, 'ab').add_output(s5, 'ab').add_output(s6, 'bb').add_output(s6, 'babb').add_output(s7, 'bb')
        self.assertEqual(f.to_dict(), {'initial': s0, 'finals': {s2, s5, s6, s7},
                                       'outputs': {s2: ['ab'], s5: ['ab'], s6: ['babb', 'bb'], s7: ['bb']},
                                       'transitions': {s0: {'a': s1, 'b': s3}, s1: {'a': s1, 'b': s2},
                                                       s2: {'a': s4, 'b': s7}, s3: {'a': s4, 'b': s7},
                                                       s4: {'a': s1, 'b': s5}, s5: {'a': s4, 'b': s6},
                                                       s6: {'a': s4, 'b': s7}, s7: {'a': s4, 'b': s7}}})
        # test get_stats
        self.assertEqual(f.get_stats(), {'numStates': 8, 'numFinalStates': 4, 'numTransitions': 16})

    def test_to_dot(self):
        f = MutableAutomaton()
        # initial state
        s0 = f.get_initial_state()
        expected_dot = """digraph automaton {
rankdir = LR;
label = "";
center = 1;
ranksep = "0.4";
nodesep = "0.25";
0 [label = "0", shape = circle, style = bold, fontsize = 14]
}"""
        self.assertEqual(f.to_dot().split('\n'), expected_dot.split('\n'))
        # add state
        s1 = f.add_state()
        expected_dot = """digraph automaton {
rankdir = LR;
label = "";
center = 1;
ranksep = "0.4";
nodesep = "0.25";
0 [label = "0", shape = circle, style = bold, fontsize = 14]
1 [label = "1", shape = circle, style = bold, fontsize = 14]
}"""
        self.assertEqual(f.to_dot().split('\n'), expected_dot.split('\n'))
        # add transition
        f.add_transition(s0, 'a', s1)
        expected_dot = """digraph automaton {
rankdir = LR;
label = "";
center = 1;
ranksep = "0.4";
nodesep = "0.25";
0 [label = "0", shape = circle, style = bold, fontsize = 14]
	0 -> 1 [label = "a", fontsize = 14];
1 [label = "1", shape = circle, style = bold, fontsize = 14]
}"""
        self.assertEqual(f.to_dot().split('\n'), expected_dot.split('\n'))
        # add final state
        f.set_final_state(s1)
        # check to_dot
        expected_dot = """digraph automaton {
rankdir = LR;
label = "";
center = 1;
ranksep = "0.4";
nodesep = "0.25";
0 [label = "0", shape = circle, style = bold, fontsize = 14]
	0 -> 1 [label = "a", fontsize = 14];
1 [label = "1", shape = doublecircle, style = bold, fontsize = 14]
}"""
        self.assertEqual(f.to_dot().split('\n'), expected_dot.split('\n'))


class MutableAutomatonDTestCase(TestCase):
    def test_matching(self):
        f = MutableAutomatonWithDefaultSuccessor()
        s0 = f.get_initial_state()
        s1 = f.add_state()
        s2 = f.add_state()
        s3 = f.add_state()
        f.add_transition(s0, 'a', s1)
        f.add_transition(s1, 'a', s2).add_transition(s1, 'b', s3)
        f.set_final_state(s2).set_final_state(s3)
        f.add_output(s2, 'aa').add_output(s3, 'ab')
        self.assertEqual(f.search('a ab aa'), [('ab', 2, 4), ('aa', 5, 7)])
