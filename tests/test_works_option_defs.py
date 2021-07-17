#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This should contain everything but filters. 
"""

import crossref as cr

api = cr.API()

def test_facet_options():
    
    
    LEAD_IN_TEXT = 'for this route are:'
    
    #        temp = api.works(facet='*:2')

    
    
    #TODO: Can we double facet????
    
    try:
        temp = api.works(facet='madeUp:*')
    except cr.errors.CrossrefAPIError:
        temp_str = api.last_error['message'][0]['message']
  
    
    #TODO: Can we make this a shared method ...
    
    current_values = cr.utils.get_valid_options(temp_str,LEAD_IN_TEXT)
    
    temp = cr.utils.load_filter_table('works_facet_options')
    
    ref_values = temp['Key']
    
    if len(ref_values) == len(current_values) and all(ref_values == current_values):
        pass
    
    
    wtf = cr.utils.OptionComparison(ref_values,current_values)
    
    pass
