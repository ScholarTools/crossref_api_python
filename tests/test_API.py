# -*- coding: utf-8 -*-
"""
Next Goals
-----------------------
- reimplement query options
- support journal type breakout on return type

Other Links
-----------------------
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
DONE    /funders - returns a list of all funders in the Funder Registry
DONE    /journals
DONE    /liceneses - returns a list of all Crossref members (mostly publishers)
DONE    /members - returns a list of all Crossref members (mostly publishers)
DONE    /types - returns a list of valid work types

#Still to do!
/works




Secondary Endpoint List
-----------------------
/member
/types/{type_id}

/works/{doi} 

"""

#TODO: Change these to endpoint alphabetical order

import crossref
from crossref import errors
from crossref.api import QueryOptions

api = crossref.API(debug=True)


#========================================

#---- /funders
#===========================================
temp = api.funders()

options = QueryOptions()
options.query = 'National Cancer Institute'
temp = api.funders(options=options)

#---- /journals
#===========================================
temp = api.journals()

#---- /licenses
#===========================================
temp = api.licenses()

#---- /members
#===========================================
temp = api.members()

#TODO: Search filter testing

#---- /types
#===========================================
temp = api.work_types()

#---- /works
#========================================
temp = api.works()

temp = api.works(_filter='type:book-section')

temp = api.works(_filter='has-references:1')

temp = api.works(_filter='has-funder:t')

temp = api.works(_filter='funder:100000054')

#yyyy
#yyyy-MM
#yyyy-MM-dd
temp = api.works(_filter='from-created-date:2018-01-15')


#options = crossref.QueryOptions()
#options.sample = 10
#temp = api.dois(options=options)

#options = crossref.QueryOptions()
#options.query = "bladder"
#temp = api.doi_list(options=options)









#==========================================================
#---- ID tests
#==========================================================

#---- /member/{member_id}
#========================================
temp = api.member_info('311')

#---- /prefixes/{owner_prefix}
#==========================================
temp = api.prefix_info("10.1002")

temp = api.prefix_info("10.1016")



#---- /types/{type_id}
#===========================================
temp = api.work_type_info('journal')

#---- /works/{doi}
#===========================================

#Invalid DOI testing
try:
    temp = api.doi_info("10.3909/riu0653")
    assert False, "This shouldn't run because the DOI is invalid"
except errors.InvalidDOI:
    pass
    
#Valid DOI testing
temp = api.doi_info("10.1002/nau.1930090206")
#TODO: some test, not sure what to have here ...

#Valid DOI - no 'reference' key
temp = api.doi_info("10.1016/j.fbr.2012.01.001")



#/journals

temp = api.search_journals()