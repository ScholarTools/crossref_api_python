# -*- coding: utf-8 -*-
"""
API documentation
https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md
"""

"""
7/30/2016
Status:
1) Lots of end points are not implemented
2) Filter is not implemented
3) Queries on works not implemented
4) Works should probably be refactored
    - own class
    - retrieve new options and filter from the class
5) Works models are not completely implemented
6) Clean up work response model, why are we cleaning dict keys?????


/funders/{funder_id}	returns metadata for specified funder and its suborganizations
/prefixes/{owner_prefix}	returns metadata for the DOI owner prefix
/members/{member_id}	returns metadata for a CrossRef member
/types/{type_id}	returns information about a metadata work type
/journals/{issn}	returns information about a journal with the given ISSN
"""

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

VERSION = '0.7'


import sys
import re

PY2 = int(sys.version[0]) == 2


#3rd party
#------------------------
import requests


#Local Imports
#------------------------
from . import errors
from . import models
from . import utils
from .utils import get_truncated_display_string as td

try:
    from . import user_config
except:
    raise Exception("User Config is required for running the codes")
    
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
    https://github.com/CrossRef/rest-api-doc#parameters
    
    Attributes
    ----------
    query :
        Uses DisMax queries
        TODO: Add documentation on how to use
        e.g.
            'renear+-ontologies' #renear but not ontologies
    rows : int
        Number of results per page
        #TODO might rename or alias
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
    
    BASE_URL = 'https://api.crossref.org/'
    
    """
    Attributes
    ----------
    session : requests.Session
    last_url :
    last_response :
    last_params :
    work_types
    
    """
    
    def __init__(self,debug=False):
        
        self.debug = debug
        self.session = requests.Session()
        self._work_types = None
     
    def _make_get_request(self,url,object_fh, params=None, response_params=None,is_list=False):
    
        if params is None:
            params = {}
        else:
            #????? - what are we doing here? - only including ones with values
            #Does requests do this for us?
            if PY2:
                params = dict((k, v) for k, v in params.iteritems() if v)
            else:
                params = dict((k, v) for k, v in params.items() if v)
     


        #Example          
        #GroovyBib/1.1 (https://example.org/GroovyBib/; mailto:GroovyBib@example.org) BasedOnFunkyLib/1.4.

        #It is unclear if we need to match this format
        #This is good enough for now
        #Eventually we might allow a user to describe their application
        #version, and url
        ua_str = 'st_crossref/%s (https://github.com/ScholarTools/crossref_api_python; mailto:%s)' % (VERSION,user_config.email)
        
        headers = {'user-agent': ua_str}
        
        r = self.session.get(url,params=params,headers=headers)      

        self.last_url = url
        self.last_response = r     
        self.last_params = params     
        
        if r.status_code == 404:
            #This typically happens when the DOI is invalid
            #TODO: Make this a named exception
            raise errors.RequestError(r.text)
        
        j = r.json()
        if j['status'] == 'failed':
            raise Exception(j['message'])
            
        temp = ResponseMessageInfo(j,is_list)
        object_json = temp.json
            
        """
        {'status': 'failed', 'message-type': 'validation-failure', 
        'message': [{'value': 'sample', 
        'message': 'This route does not support sample', 'type': 'parameter-not-allowed'}]}
        """     
        if response_params is None:
            return object_fh(object_json,self)
        else:
            return object_fh(object_json,self,response_params)
    
    def _make_search_request(self,url,object_fh,options,_filter):

        """
        Parameters
        ----------
        url :
        object_fh : Function handle to result object
        options : 
        _filter :
        TODO: We could also allow options to be a dict rather than forcing the object creation
        """
        
        #TODO: Consider renaming to _make_search_request
        
        if options is not None:
            qd = options.get_query_dict()
        else:
            qd = {}
               
        #TODO: We could make a post request instead, this might be preferable
        return self._make_get_request(url,object_fh,qd,is_list=True)
    
    def search_licenses(self,options=None,_filter=None):
        pass
    
    #---- Funders
    #===========================================================
    def funders(self,options=None,_filter=None):
        
        url = self.BASE_URL + 'funders'
        return self._make_search_request(url,models.FundersSearchResult,options,_filter)
        
    
    #---- Journals
    #===========================================================
    def journals(self,options=None,_filter=None):
        
        url = self.BASE_URL + 'journals'
        return self._make_search_request(url,models.JournalSearchResult,options,_filter)
    
    #---- Licenses 
    #===========================================================
    def licenses(self,options=None,_filter=None):
        
        url = self.BASE_URL + 'licenses'
        return self._make_search_request(url,models.LicenseSearchResult,options,_filter)    
        
    def search_works(self,options=None,_filter=None):
        """
        
        Parameters
        ----------
        options : QueryOptions
        _filter : Filter

        Returns
        -------
        crossref.models.WorkList

        Invalid options
        ---------------
        sample
        
        TODO: Do we get a 'next' link?
        TODO: Make sure the model methods show in the display ...
        """
        
        url = self.BASE_URL + 'works'
        return self._make_list_request(url,models.WorkList,options,_filter)
        
    def search_works_by_funder(self):
        pass
    
    def search_works_by_type(self):
        pass
    
    def search_works_by_owner(self):
        pass
    
    def search_works_by_member(self):
        pass
    
    def search_works_by_journal(self):
        pass
    
    def dois(self,options):
        pass

    def doi_info(self,doi,**kwargs):
        """
        
        Returns
        -------
        crossref.models.Work       
        
        If the DOI is not found the errors.InvalidDOI exception is raised.
        
        Example
        -------
        import crossref
        c = crossref.API()
        m = c.doi_meta('10.1109/TNSRE.2011.2163145')
        
        
        TODO : are there any valid kwargs? I don't think there are. This
        can probably be removed (oops, maybe version?)
        
        
        """
        
        doi = _clean_doi(doi)
        
        url = self.BASE_URL + 'works/' + doi
        
        try:
            return self._make_get_request(url,models.Work)
        except errors.RequestError:
            #TODO: Check for 404
            #last_response.status_code
            #TODO: Do this only if debugging is enabled
            if self.debug:
                #TODO: Also report code
                print("Error msg from server: " + self.last_response.text)
            raise errors.InvalidDOI('Invalid DOI requested: ' + doi)
        
        #return self._make_get_request(url,models.Work,kwargs)
        
    def prefix_info(self,prefix_id):
        """
        Returns metadata for the DOI owner prefix
        
        Returns
        -------
        crossref.models.Prefix
        
        Implements
        ----------
        /prefixes/{owner_prefix}
        
        Example Data
        ------------
        <class 'crossref.models.Prefix'>:
            member: http://id.crossref.org/member/311
              name: Wiley-Blackwell
            prefix: http://id.crossref.org/prefix/10.1002
        """
        
        url = self.BASE_URL + 'prefixes/' + prefix_id
        
        return self._make_get_request(url,models.Prefix)
    
    def member_info(self,member_id):
        """
        
        Example Data
        ------------
        <class 'crossref.models.Member'>:
    last_status_check_time: 1522803773023
              primary_name: Wiley-Blackwell
                    counts: <dict> with 3 fields
                breakdowns: <dict> with 1 fields
                  prefixes: <list> len 33
                  coverage: <dict> with 18 fields
                    prefix: <list> len 33
                        id: 311
                    tokens: ['wiley', 'blackwell']
                     flags: <dict> with 20 fields
                  location: 111 River Street Hoboken NJ 07...
                     names: <list> len 33
        """
        
        url = self.BASE_URL + 'members/' + member_id
        return self._make_get_request(url,models.Member)
    
    def members(self):
        url = self.BASE_URL + 'members/'
        return self._make_get_request(url,models.MembersSearchResult)
    
    def work_types(self):
        if self._work_types is None:
            url = self.BASE_URL + 'types'
            self._work_types = self._make_list_request(url,models.TypesList,None,None)

        return self._work_types
    
    def work_type_info(self,type_id):
        """
        This doesn't seem to be all that useful, since it just returns
        the subset of work_types()
        
        Example
        -------
        api.work_type_info('journal')
        e.g. {'id': 'journal', 'label': 'Journal'}
        """
        url = self.BASE_URL + 'types/' + type_id
        return self._make_get_request(url,models.pass_through)

        
        
    
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
            
            #These weren't present with types-list 
            #Where is that documented?????
            self.query = self.json.get('query')
            self.items_per_page = self.json.get('items_per_page')
            self.facets = self.json.get('facets')
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

def _validate_config(user_config):
    
    #1) Validate email
    if hasattr(user_config,'email') and len(user_config.email) > 0:
        pass
    else:
        raise Exception("Invalid email, email required in user_config")

_validate_config(user_config)

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