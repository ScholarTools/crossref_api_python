# -*- coding: utf-8 -*-
"""
Next Goals
-----------------------
- cursor
- next
- support field queries
- add on ability to change print length
- x-rate limits


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

    
"""

#TODO: Change these to endpoint alphabetical order

import crossref
from crossref import errors
from crossref import search_keys as sk

api = crossref.API(debug=True)


#========================================

#---- /funders
#===========================================
temp = api.funders()

temp = api.funders(query='National Cancer Institute')

#TODO: This doesn't work, can't sample 
#temp = api.funders(n_random=10)

#---- /journals
#===========================================
temp = api.journals()

#TODO: This shouldn't make it to the request stage but should fail locally
#temp = api.journals('1433-3023')

#---- /licenses
#===========================================
temp = api.licenses()

temp = api.licenses(query='creative')

#---- /members
#===========================================
temp = api.members()

temp = api.members(query='Elsevier')

#TODO: Search filter testing

#---- /types
#===========================================
temp = api.work_types()

#---- /works
#========================================
temp = api.works()

temp = api.works(select='ISSN,DOI')

temp = api.works(filter='type:book-section')

temp = api.works(filter='has-references:1')

temp = api.works(filter='has-funder:t')

temp = api.works(filter='funder:100000054')

temp = api.works(n_random=10,query='sacral neuromodulation')

temp1 = api.works(n_per_page=10,select='DOI')

temp2 = api.works(n_per_page=10,select='DOI',offset=5)

temp = api.works(facet='issn:100',query='sacral neuromodulation')

temp = api.works(filter='issn:1873-5584')

temp = api.works(query='urinary urgency',cursor='*')

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

#---- /funders/{funder_id}
#==========================================
temp = api.funder_info('501100000165')

#---- /journals/{journal_id}
#==========================================
temp = api.journal_info('1433-3023')

#Resource not found
temp = api.journal_info('1873-5584')

#---- /members/{member_id}
#==========================================
temp = api.member_info('311')

#---- /prefixes/{owner_prefix}
#==========================================
temp = api.prefix_info("10.1002")

temp = api.prefix_info("10.1016")

#---- /types/{type_id}
#===========================================
#This is pretty useless since getting everything
#is so small
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

#Invalid DOI with cleaning
temp = api.doi_info('j.apsusc.2018.04.237')

temp = api.doi_info('10.1016/j.apsusc.2018.04.237')
