# -*- coding: utf-8 -*-

import generation_sonnets

def test_cpt_position_2():
    id = "s-1-2-1"
    assert generation_sonnets.cpt_verse_position(id) == 5

def test_cpt_position_3():
    id = "s-1-3-2"
    assert generation_sonnets.cpt_verse_position(id) == 10
