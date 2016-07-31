# -*- coding: utf-8 -*-
"""

"""

import crossref

api = crossref.API()

#/works
options = crossref.QueryOptions()
options.sample = 10
temp = api.doi_list(options=options)

options = crossref.QueryOptions()
options.query = "bladder"
temp = api.doi_list(options=options)

#/works/{doi}

#Doesn't exist
temp = api.doi_meta("10.3909/riu0653")

temp = api.doi_meta("10.1002/nau.1930090206")

#/types

temp = api.work_types

#/journals

temp = api.search_journals()