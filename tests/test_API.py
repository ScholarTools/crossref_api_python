# -*- coding: utf-8 -*-
"""
Other links:
Main Documentation
    https://github.com/CrossRef/rest-api-doc
Demo with notes
    https://github.com/CrossRef/rest-api-doc/blob/master/demos/crossref-api-demo.ipynb
API format
    https://github.com/Crossref/rest-api-doc/blob/master/api_format.md

Other implementations:
    https://github.com/sckott/habanero
    https://github.com/fabiobatalha/crossrefapi    

    
Endpoint List
-----------------------
/funders - returns a list of all funders in the Funder Registry
/journals
/liceneses
/members
DONE /types - returns a list of valid work types
/works





-----------------------
/types/{type_id}

/works/{doi} 

"""

#TODO: Change these to endpoint alphabetical order

import crossref
from crossref import errors

api = crossref.API(debug=True)
#========================================



#---- /works
#========================================
options = crossref.QueryOptions()
options.sample = 10
temp = api.doi_list(options=options)

options = crossref.QueryOptions()
options.query = "bladder"
temp = api.doi_list(options=options)

#---- /members
#===========================================
temp = api.members()

#---- /types
#===========================================
temp = api.work_types()





#==========================================================
#---- ID tests
#==========================================================

#---- /member/{member_id}
#========================================
temp = api.member_info('311')

#---- /prefixes/{owner_prefix}
#==========================================
temp = api.prefix_info("10.1002")

#---- /types/{type_id}
#===========================================
temp = api.work_type_info('journal')

#---- /works/{doi}
#===========================================

#Invalid DOI testing
try:
    temp = api.doi_meta("10.3909/riu0653")
    assert False, "This shouldn't run because the DOI is invalid"
except errors.InvalidDOI:
    pass
    
#Valid DOI testing
temp = api.doi_meta("10.1002/nau.1930090206")
#TODO: some test, not sure what to have here ...



#/journals

temp = api.search_journals()