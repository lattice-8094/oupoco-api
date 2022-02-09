# -*- coding: utf-8 -*-

import generation_sonnets

def test_date_authors():
    """
    checks that uncompatible constraints returns None
    """
    authors=['Charles Baudelaire']
    dates=['1800-1830']
    assert generation_sonnets.generate(authors=authors, dates=dates) == None

def test_date_authors_2():
    """
    checks if 'Alfred de Musset' is in interval 1800-1830
    """
    authors=['Alfred de Musset']
    assert '1800-1830' in generation_sonnets.get_dates(authors)