# -*- coding: utf-8 -*-
# @author <lambda.coder@gmail.com>

from unittest import TestCase

from automaton.transition_matrix import MutableTransitionMatrix
from automaton.transition_matrix import MutableTransitionMatrixWithDefaultSuccessor


class MutableTransitionMatrixTestCase(TestCase):
    def test_add_state__has_state__get_states(self):
        tm = MutableTransitionMatrix(0)
        self.assertEqual(tm.get_num_states(), 1)
        self.assertTrue(tm.has_state(0))
        self.assertFalse(tm.has_state(1))
        # add state
        s1 = tm.add_state()
        # test
        self.assertEqual(tm.get_num_states(), 2)
        self.assertTrue(tm.has_state(0))
        self.assertTrue(tm.has_state(s1))
        self.assertTrue(tm.has_state(0))
        self.assertTrue(tm.has_state(1))
        # check states
        self.assertEqual(tm.get_states(), [0, 1])

    def test_add_transition(self):
        # initial state
        s0 = 0
        # init transition matrix
        tm = MutableTransitionMatrix(s0)
        self.assertEqual(tm.get_num_states(), 1)
        self.assertEqual(tm.get_num_transitions(), 0)
        # states
        s1 = tm.add_state()
        self.assertEqual(tm.get_num_states(), 2)
        # add s0 a s1
        tm.add_transition(s0, 'a', s1)
        self.assertEqual(tm.get_num_states(), 2)
        self.assertEqual(tm.get_num_transitions(), 1)
        self.assertEqual(tm.get_target(s0, 'a'), s1)
        # add s0 b s0
        tm.add_transition(s0, 'b', s0)
        self.assertEqual(tm.get_num_states(), 2)
        self.assertEqual(tm.get_num_transitions(), 2)
        self.assertEqual(tm.get_target(s0, 'a'), s1)
        self.assertEqual(tm.get_target(s0, 'b'), s0)
        # add s1 a s1
        tm.add_transition(s1, 'a', s1)
        self.assertEqual(tm.get_num_states(), 2)
        self.assertEqual(tm.get_num_transitions(), 3)
        self.assertEqual(tm.get_target(s0, 'a'), s1)
        self.assertEqual(tm.get_target(s0, 'b'), s0)
        self.assertEqual(tm.get_target(s1, 'a'), s1)
        # add s1 b s1
        tm.add_transition(s1, 'b', s1)
        self.assertEqual(tm.get_num_states(), 2)
        self.assertEqual(tm.get_num_transitions(), 4)
        self.assertEqual(tm.get_target(s0, 'a'), s1)
        self.assertEqual(tm.get_target(s0, 'b'), s0)
        self.assertEqual(tm.get_target(s1, 'a'), s1)
        self.assertEqual(tm.get_target(s1, 'b'), s1)

    def test_get_target_none(self):
        s0 = 0
        tm = MutableTransitionMatrix(s0)
        self.assertEqual(tm.get_target(s0, 'a'), None)


class MutableTransitionMatrixWithDefaultSuccessorTestCase(TestCase):
    def test_get_target(self):
        s0 = 0
        tm = MutableTransitionMatrixWithDefaultSuccessor(s0)
        self.assertEqual(tm.get_target(s0, 'a'), None)
        self.assertEqual(tm.get_target_by_default(s0, 'a'), s0)
        s1 = tm.add_state()
        tm.add_transition(s0, 'a', s1)
        self.assertEqual(tm.get_target(s0, 'a'), s1)
        self.assertEqual(tm.get_target_by_default(s0, 'a'), s1)
        self.assertEqual(tm.get_target(s0, 'b'), None)
        self.assertEqual(tm.get_target_by_default(s0, 'b'), s0)
