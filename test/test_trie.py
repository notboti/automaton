# -*- coding: utf-8 -*-
# @author <lambda.coder@gmail.com>

from unittest import TestCase

from automaton.trie import build_trie


class BuildTrieTestCase(TestCase):
    def test_emptyword(self):
        words = ['']
        t = build_trie(words)
        self.assertEqual(t.to_dict(), {'initial': 0, 'finals': set(), 'outputs':{}, 'transitions': {0: {}}})
        self.assertFalse(t.accept(''))

    def test_a(self):
        words = ['a']
        t = build_trie(words)
        self.assertEqual(t.to_dict(),
                         {'initial': 0, 'finals':{1}, 'outputs': {1: ['a']}, 'transitions': {0: {'a': 1}, 1: {}}})
        self.assertFalse(t.accept(''))
        self.assertTrue(t.accept('a'))
        self.assertFalse(t.accept('aa'))

    def test_a_and_emptyword(self):
        words = ['a', '']
        t = build_trie(words)
        self.assertEqual(t.to_dict(),
                         {'initial': 0, 'finals': {1}, 'outputs': {1: ['a']}, 'transitions': {0: {'a': 1}, 1: {}}})

    def test_a_b(self):
        words = ['a', 'b']
        t = build_trie(words)
        self.assertEqual(t.to_dict(), {'initial': 0, 'finals': {1, 2}, 'outputs': {1: ['a'], 2: ['b']},
                                       'transitions': {0: {'a': 1, 'b': 2}, 1: {}, 2: {}}})
        self.assertFalse(t.accept(''))
        self.assertTrue(t.accept('a'))
        self.assertTrue(t.accept('b'))
        self.assertFalse(t.accept('aa'))
        self.assertFalse(t.accept('ab'))

    def test_aa_ab(self):
        words = ['aa', 'ab']
        t = build_trie(words)
        self.assertEqual(t.to_dict(), {'initial': 0, 'finals': {2, 3}, 'outputs': {2: ['aa'], 3: ['ab']},
                                       'transitions': {0: {'a': 1}, 1: {'a': 2, 'b': 3}, 2: {}, 3: {}}})
        self.assertFalse(t.accept(''))
        self.assertFalse(t.accept('a'))
        self.assertFalse(t.accept('b'))
        self.assertTrue(t.accept('aa'))
        self.assertTrue(t.accept('ab'))

    def test_a_aa_ab(self):
        words = ['a', 'aa', 'ab']
        t = build_trie(words)
        self.assertEqual(t.to_dict(), {'initial': 0, 'finals': {1, 2, 3}, 'outputs': {1: ['a'], 2: ['aa'], 3: ['ab']},
                                       'transitions': {0: {'a': 1}, 1: {'a': 2, 'b': 3}, 2: {}, 3: {}}})
        self.assertFalse(t.accept(''))
        self.assertTrue(t.accept('a'))
        self.assertFalse(t.accept('b'))
        self.assertTrue(t.accept('aa'))
        self.assertTrue(t.accept('ab'))
