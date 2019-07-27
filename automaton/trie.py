# -*- coding: utf-8 -*-
# @author <lambda.coder@gmail.com>

from .automaton import MutableAutomaton


def build_trie(words, fst_factory=MutableAutomaton):
    automaton = fst_factory()
    for word in words:
        if len(word) != 0:
            state = automaton.get_initial_state()
            for letter in word:
                target = automaton.get_target(state, letter)
                if target is None:
                    target = automaton.add_state()
                    automaton.add_transition(state, letter, target)
                state = target
            automaton.set_final_state(state)
            automaton.add_output(state, word)
    return automaton
