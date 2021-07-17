#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

import crossref as cr

api = cr.API()

def test_facets():
    
    temp = api.works(facet='published:20')
    
def test_filters():
    pass

def n_rows():
    
    temp = api.works(n_rows=100)

    pass

def n_random():
    pass

def offset():
    pass

def query():
    pass

def cursor():
    pass

def select():
    pass
