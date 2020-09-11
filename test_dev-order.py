# -*- coding: utf-8 -*-

import generation_sonnets

def test_cpt_position_2_1():
    id = "s-1-2-1"
    assert generation_sonnets.cpt_verse_position(id) == 5

def test_cpt_position_3_2():
    id = "s-1-3-2"
    assert generation_sonnets.cpt_verse_position(id) == 10

def test_cpt_position_4_3():
    id = "s-1-4-3"
    assert generation_sonnets.cpt_verse_position(id) == 14

def test_date_authors():
    """
    checks that uncompatible constraints returns None
    """
    authors=['Charles Baudelaire']
    dates=['1800-1830']
    assert generation_sonnets.generate(authors=authors, dates=dates) == None