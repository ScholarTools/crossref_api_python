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
The works component can be appended to other resources.

resource	description
/works/{doi}	returns information about the specified CrossRef DOI
/funders/{funder_id}/works	returns list of works associated with the specified funder_id
/types/{type_id}/works	returns list of works of type type
/prefixes/{owner_prefix}/works	returns list of works associated with specified owner_prefix
/members/{member_id}/works	returns list of works associated with a CrossRef member (deposited by a CrossRef member)
/journals/{issn}/works	returns a list of works in the given journal
"""


import requests
from . import models
from . import utils
from .utils import get_truncated_display_string as td

import sys
import re

PY2 = int(sys.version[0]) == 2


class Filter(object):
    """
    filter={filter_name}:{value}	filter results by specific fields
    """
    pass

"""
has-funder		metadata which includes one or more funder entry
funder	{funder_id}	metadata which include the {funder_id} in FundRef data
prefix	{owner_prefix}	metadata belonging to a DOI owner prefix {owner_prefix} (e.g. 10.1016 )
member	{member_id}	metadata belonging to a CrossRef member
from-index-date	{date}	metadata indexed since (inclusive) {date}
until-index-date	{date}	metadata indexed before (inclusive) {date}
from-deposit-date	{date}	metadata last (re)deposited since (inclusive) {date}
until-deposit-date	{date}	metadata last (re)deposited before (inclusive) {date}
from-update-date	{date}	Metadata updated since (inclusive) {date}. Currently the same as from-deposit-date.
until-update-date	{date}	Metadata updated before (inclusive) {date}. Currently the same as until-deposit-date.
from-created-date	{date}	metadata first deposited since (inclusive) {date}
until-created-date	{date}	metadata first deposited before (inclusive) {date}
from-pub-date	{date}	metadata where published date is since (inclusive) {date}
until-pub-date	{date}	metadata where published date is before (inclusive) {date}
has-license		metadata that includes any <license_ref> elements.
license.url	{url}	metadata where <license_ref> value equals {url}
license.version	{string}	metadata where the <license_ref>'s applies_to attribute is {string}
license.delay	{integer}	metadata where difference between publication date and the <license_ref>'s start_date attribute is <= {integer} (in days)
has-full-text		metadata that includes any full text <resource> elements.
full-text.version	{string}	metadata where <resource> element's content_version attribute is {string}.
full-text.type	{mime_type}	metadata where <resource> element's content_type attribute is {mime_type} (e.g. application/pdf).
public-references		metadata where publishers allow references to be distributed publically. [^*]
has-references		metadata for works that have a list of references
has-archive		metadata which include name of archive partner
archive	{string}	metadata which where value of archive partner is {string}
has-orcid		metadata which includes one or more ORCIDs
orcid	{orcid}	metadata where <orcid> element's value = {orcid}
issn	{issn}	metadata where record has an ISSN = {issn}. Format is xxxx-xxxx.
type	{type}	metadata records whose type = {type}. Type must be an ID value from the list of types returned by the /types resource
directory	{directory}	metadata records whose article or serial are mentioned in the given {directory}. Currently the only supported value is doaj.
doi	{doi}	metadata describing the DOI {doi}
updates	{doi}	metadata for records that represent editorial updates to the DOI {doi}
is-update		metadata for records that represent editorial updates
has-update-policy		metadata for records that include a link to an editorial update policy
container-title		metadata for records with a publication title exactly with an exact match
publisher-name		metadata for records with an exact matching publisher name
category-name		metadata for records with an exact matching category label
type-name		metadata for records with an exacty matching type label
award.number	{award_number}	metadata for records with a matching award nunber. Optionally combine with award.funder
award.funder	{funder doi or id}	metadata for records with an award with matching funder. Optionally combine with award.number
assertion-group		metadata for records with an assertion in a particular group
assertion		metadata for records with a particular named assertion
affiliation		metadata for records with at least one contributor with the given affiliation
has-affiliation		metadata for records that have any affiliation information
alternative-id		metadata for records with the given alternative ID, which may be a publisher-specific ID, or any other identifier a publisher may have provided
article-number		metadata for records with a given article number
"""


class QueryOptions(object):
    """
    
    Attributes
    ----------
    query :
        Uses DisMax queries
        TODO: Add documentation on how to use
        e.g.
            'renear+-ontologies' #renear but not ontologies
    rows :
    offset :
    sample :
        If specified, this return N random results. This can be useful 
        for testing.
    sort :
        - score
        - relevance
        - updated
        - deposited
        - indexed
        - published
    order :
        - asc - ascending order
        - desc - descending order
    facet : 
        "Facet counts can be retrieved by enabling faceting; facet=t (or 1, 
        true). Facet counts give counts per field value for an entire result 
        set" => I'm not sure what this means
    """
    
    
    """
    We use setattr so that only user specified query parameters are passed
    in a query, rather than having defaults for each parameter that are then
    passed to the query each time.
    """

    fields = ['query','rows','offset','sample','sort','order','facet']

    def __init__(self):
        self.__dict__['query_params'] = {}

    def _null(self):
        self.query = None
        self.rows = None
        self.offset = None
        self.sample = None
        self.sort = None
        self.order = None
        self.facet = None
        
    def get_query_dict(self):
        return self.query_params

    def __getattr__(self,name):
        if name in self.fields:
            #TODO: Does .get work? or does it call this
            #recursively?????
            if name in self.query_params:
                return self.query_params[name]
            else:
                return None
        else:
            raise AttributeError

        
    def __setattr__(self,name,value):
        if name in self.fields:
            self.query_params[name] = value
        else:
            raise Exception('Unable to set attribute: %s'%name)
    
    def __repr__(self): 
        pv = ['query',self.query,
            'rows',self.rows,
            'offset',self.offset,
            'sample',self.sample,
            'sort',self.sort,
            'order',self.order,
            'facet',self.facet]

        return utils.property_values_to_string(pv)


"""
query	limited DisMax query terms

rows={#}	results per per page
offset={#}	result offset
sample={#}	return random N results
sort={#}	sort results by a certain field

    score or relevance	  Sort by relevance score
    updated	Sort by date of most recent change to metadata. Currently the same as deposited.
    deposited	Sort by time of most recent deposit
    indexed	Sort by time of most recent index
    published	Sort by publication date

"""

class API(object):
    
    BASE_URL = 'http://api.crossref.org/'    
    
    def __init__(self):
        
        self.session = requests.Session()
     
    def _make_get_request(self,url,object_fh, params, response_params=None,is_list=False):
    
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
        
        j = r.json()
        if j['status'] == 'failed':
            raise Exception(j['message'])
            
        temp = ResponseMessageInfo(j,is_list)
        object_json = temp.json
        import pdb
        pdb.set_trace()
            
        """
        {'status': 'failed', 'message-type': 'validation-failure', 
        'message': [{'value': 'sample', 
        'message': 'This route does not support sample', 'type': 'parameter-not-allowed'}]}
        """     
        if response_params is None:
            return object_fh(object_json,self)
        else:
            return object_fh(object_json,self,response_params)
    
    def _make_list_request(self,url,object_fh,options,_filter):
        if options is not None:
            qd = options.get_query_dict()
        else:
            qd = {}
               
        return self._make_get_request(url,object_fh,qd,is_list=True)
    
    def doi_list(self,options=None,_filter=None):
        """
        Invalid options
        ---------------
        sample
        """
        
        url = self.BASE_URL + 'works'
        return self._make_list_request(url,models.WorkList,options,_filter)
        
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
        
        return self._make_get_request(url,models.Work,kwargs)
        
    def funders_list(self,options=None,_filter=None):

        #url = self.BASE_URL + 'works/'
        
        pass
    
class ResponseMessageInfo(object):

    """
    Attributes
    ----------
    
    
    """
    
    
    def __init__(self,json,is_list):            
        self.message_type = json['message-type']
        self.message_version = json['message-version']
        self.status = json['status'] #ok
        temp = json['message']
        self.json = utils.clean_dict_keys(temp)
        self.is_list = is_list
        if is_list:
            self.total_results = self.json['total_results']
            self.query = self.json['query']
            self.items_per_page = self.json['items_per_page']
            self.facets = self.json['facets']
            #This is a bit sloppy, the message actually contains all the
            #info above and items, which we'll then parse out in the main
            #class ...
            self.json = self.json['items']

    def __repr__(self):
        #TODO: Set this up like it looks in Mendeley
        pv = ['is_list',self.is_list,
              'message_type',self.message_type,
                'message_version',self.message_version,
                'status',self.status,
                'json',td(self.json)]
                
        if self.is_list:
            pv += ['total_results',self.total_results,
                'query',self.query,
                'items_per_page',self.items_per_page,
                'facets',self.facets]
        
        return utils.property_values_to_string(pv)

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