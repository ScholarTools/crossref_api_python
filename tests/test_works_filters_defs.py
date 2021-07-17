#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_works_filters_defs
"""

import crossref as cr

api = cr.API()
#import requests
#from bs4 import BeautifulSoup

def works_filter_options():
    
    """
    Spreadsheet: works_filters.tsv
    """
        
    LEAD_IN_TEXT = 'Valid filters for this route are:'
    
    try:
        temp = api.works(filter='madeUpOption:value')
    except cr.errors.CrossrefAPIError:
        temp_str = api.last_error['message'][0]['message']
    
    current_values = cr.utils.get_valid_options(temp_str,LEAD_IN_TEXT)
    
    temp = cr.utils.load_filter_table('works_filters')
    
    known_values = sorted(list(temp['Key']))
    
    #TODO: comparison of values
    
    
def test_types():
    
    #TODO: This is actually directly testable
    pass

def test_relation_defs():
    
    """
    Spreadsheet: works_filters.tsv
    """
    
    LEAD_IN_TEXT = 'but must be one of:'
        
    try:
        temp = api.works(filter='relation.type:madeUpRelation')
    except cr.errors.CrossrefAPIError:
        temp_str = api.last_error['message'][0]['message']
    
    current_values = cr.utils.get_valid_options(temp_str,LEAD_IN_TEXT)
    
    
    #This was compiled from a previous run
    known_values = ['based-on-data',
                 'compiles',
                 'continues',
                 'documents',
                 'has-comment',
                 'has-derivation',
                 'has-expression',
                 'has-format',
                 'has-manifestation',
                 'has-manuscript',
                 'has-part',
                 'has-preprint',
                 'has-related-material',
                 'has-reply',
                 'has-review',
                 'has-translation',
                 'has-version',
                 'is-based-on',
                 'is-basis-for',
                 'is-comment-on',
                 'is-compiled-by',
                 'is-continued-by',
                 'is-data-basis-for',
                 'is-derived-from',
                 'is-documented-by',
                 'is-expression-of',
                 'is-identical-to',
                 'is-manifestation-of',
                 'is-manuscript-of',
                 'is-original-form-of',
                 'is-part-of',
                 'is-preprint-of',
                 'is-referenced-by',
                 'is-related-material',
                 'is-replaced-by',
                 'is-reply-to',
                 'is-required-by',
                 'is-review-of',
                 'is-same-as',
                 'is-supplement-to',
                 'is-supplemented-by',
                 'is-translation-of',
                 'is-varient-form-of',
                 'is-version-of',
                 'references',
                 'replaces',
                 'requires']
    #TODO: run a comparison
    