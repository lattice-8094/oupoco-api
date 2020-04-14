# -*- coding: utf-8 -*-

import generation_sonnets

def test_last_word():
    sentence = "Que dans l’oubli fermé par le cadre se fixe"
    assert generation_sonnets.__get_last_word__(sentence) == 'fixe'

def test_last_word_strong_punct():
    sentence = "Et les citrons amers où s’imprimaient tes dents ?"
    assert generation_sonnets.__get_last_word__(sentence) == 'dents'

def test_last_word_weak_punct():
    sentence = "Entrelaçant leurs corps impudiques et beaux,"
    assert generation_sonnets.__get_last_word__(sentence) == 'beaux'
