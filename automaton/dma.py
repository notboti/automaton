# -*- coding: utf-8 -*-
# @author <lambda.coder@gmail.com>


from .automaton import MutableAutomatonWithDefaultSuccessor
from .trie import build_trie


def get_letters(words):
    return set(letter for word in words for letter in word)


def build_dma_complete(words, letters=None):
    """
    build a complete Dictionary Matching Automaton ( aka DMA )
    the transition matrix of the automaton is complete
    :param words:
    :param letters:
    :return: DMA automaton computed by Aho-Corasick algorithm

    see https://en.wikipedia.org/wiki/Aho–Corasick_algorithm
    """
    automaton = build_trie(words)
    initial = automaton.get_initial_state()
    queue = []
    if letters is None:
        letters = get_letters(words)
    for letter in letters:
        target = automaton.get_target(initial, letter)
        if target is None:
            automaton.add_transition(initial, letter, initial)
        else:
            queue.append((target, initial))
    while len(queue) != 0:
        p, r = queue.pop(0)
        if automaton.is_final_state(r):
            automaton.set_final_state(p)
            automaton.add_outputs(p, automaton.get_outputs(r))
        for letter in letters:
            q = automaton.get_target(p, letter)
            s = automaton.get_target(r, letter)
            if q is None:
                automaton.add_transition(p, letter, s)
            else:
                queue.append((q, s))
    return automaton


def build_dma_default(words, letters=None):
    """
    build a Dictionary Matching Automaton ( aka DMA )
    :param words:
    :param letters:
    :return: DMA automaton computed by Aho-Corasick algorithm

    see https://en.wikipedia.org/wiki/Aho–Corasick_algorithm
    """
    automaton = build_trie(words, fst_factory=MutableAutomatonWithDefaultSuccessor)
    initial = automaton.get_initial_state()
    queue = []
    if letters is None:
        letters = get_letters(words)
    for letter in letters:
        target = automaton.get_target(initial, letter)
        if target is not None:
            queue.append((target, initial))
    while len(queue) != 0:
        p, r = queue.pop(0)
        if automaton.is_final_state(r):
            automaton.set_final_state(p)
            automaton.add_outputs(p, automaton.get_outputs(r))
        for letter in letters:
            q = automaton.get_target(p, letter)
            s = automaton.get_target_by_default(r, letter)
            if q is None:
                if s != initial:
                    automaton.add_transition(p, letter, s)
            else:
                queue.append((q, s))
    return automaton
