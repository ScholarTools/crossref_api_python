# -*- coding: utf-8 -*-
"""
API documentation
https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md
"""

"""
/works	returns a list of all works (journal articles, conference proceedings, books, components, etc), 20 per page
/funders	returns a list of all funders in the FundRef Registry
/members	returns a list of all CrossRef members (mostly publishers)
/types	returns a list of valid work types
/licenses	return a list of licenses applied to works in CrossRef metadata
/journals	return a list of journals in the CrossRef database

/works/{doi}	returns metadata for the specified CrossRef DOI.
/funders/{funder_id}	returns metadata for specified funder and its suborganizations
/prefixes/{owner_prefix}	returns metadata for the DOI owner prefix
/members/{member_id}	returns metadata for a CrossRef member
/types/{type_id}	returns information about a metadata work type
/journals/{issn}	returns information about a journal with the given ISSN
"""

#TODO: Expose common aspects via def

"""
query	limited DisMax query terms
filter={filter_name}:{value}	filter results by specific fields
rows={#}	results per per page
offset={#}	result offset
sample={#}	return random N results
sort={#}	sort results by a certain field
order={#}	set the sort order to asc or desc
facet=t	enable facet information in responses

"""


import requests
from . import models

import sys
import re

PY2 = int(sys.version[0]) == 2

class API(object):
    
    BASE_URL = 'http://api.crossref.org/'    
    
    def __init__(self):
        
        self.session = requests.Session()
     
    def _make_get_request(self,url,object_fh, params, response_params=None):
    
        if params is None:
            params = {}
        else:
            if PY2:
                params = dict((k, v) for k, v in params.iteritems() if v)
            else:
                params = dict((k, v) for k, v in params.items() if v)
     
        r = self.session.get(url,params=params)      
        
        self.last_url = url
        self.last_response = r     
        self.last_params = params     
     
        if response_params is None:
            return object_fh(r.json(),self)
        else:
            return object_fh(r.json(),self,response_params)
     
    def doi_list(self):
        pass
        
    def doi_meta(self,doi,**kwargs):
        """
        
        Example
        -------
        from crossref import api
        c = api.API()
        m = c.doi_meta('10.1109/TNSRE.2011.2163145')
        
        """
        doi = _clean_doi(doi)
        
        url = self.BASE_URL + 'works/' + doi
        
        self._make_get_request(url,models.Work,kwargs)


def _clean_doi(input_doi):

    """
    This code was borrowed from:
    https://github.com/Impactstory/total-impact-core/
    """

    """
    Forms
    -----
    http://dx.doi.org/10.
    doi:
    10.
    """

    
    #Hopefully we don't need to worry about this for now ...
    #input_doi = remove_nonprinting_characters(input_doi)
    input_doi = input_doi.lower()
    if input_doi.startswith("http"):
        match = re.match("^https*://(dx\.)*doi.org/(10\..+)", input_doi)
        doi = match.group(2)
    elif "doi.org" in input_doi:
        match = re.match("^(dx\.)*doi.org/(10\..+)", input_doi)
        doi = match.group(2)
    elif input_doi.startswith("doi:"):
        match = re.match("^doi:(10\..+)", input_doi)
        doi = match.group(1)
    elif input_doi.startswith("10."):
        doi = input_doi
    elif "10." in input_doi:
        match = re.match(".*(10\.\d+.+)", input_doi, re.DOTALL)
        doi = match.group(1)
    else:
        raise Exception('Unable to clean DOI: %s'%input_doi)

    return doi