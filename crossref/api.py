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
from . import search_values as sv
from . import errors
from . import models
from . import utils
from .utils import get_truncated_display_string as td
display_class = utils.display_class

try:
    from . import user_config
except:
    raise Exception("User Config is required for running the API")
    
        
#/works filters
#https://github.com/CrossRef/rest-api-doc#filter-names




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
    
    
    search_values = {}
    
    #https://github.com/CrossRef/rest-api-doc#parameters
    """
    search_options = {
            'filter':'test',
            'n_rows':'max # of results to return per request',
            'n_random':'Return this # of random values',
            'offset':'Return starting at a given position, max=10k',
            'query':'Search terms, TODO: provide link to examples',
            'sort_by':'A field by which to sort the results, see search_options.sort',
            'order':'How to order the results, either "asc" (ascending) or "desc" (descending)',
            'facet':'test',
            'cursor':'test',
            'select':'Fields '}
    """
    
    search_keys = ['cursor',
         'facet',
         'filter',
         'n_rows',
         'n_random',
         'offset',
         'order',
         'query',
         'select',
         'sort_by']
    
    #search_examples = {}
    

    
    
    def __init__(self,debug=False):
        
        self.debug = debug
        self.session = requests.Session()
        self._work_types = None
        self.last_error = None
     
 
    def get_search_descriptions(key_name):
        pass
    
    def get_search_examples(key_name):
        pass
    
    @staticmethod
    def get_search_options(key_name):
        if key_name is 'cursor':
            pass
        elif key_name is 'facet':
            pass
        elif key_name is 'filter':
            pass
        elif key_name is 'n_rows':
            return None
        elif key_name is 'n_random':
            return None
        elif key_name is 'offset':
            return None
        elif key_name is 'order':
            return sv.order
        elif key_name is 'query':
            return None
        elif key_name is 'select':
            print('select')
        elif key_name is 'sort_by':
            return sv.sort
            pass
            
        
    def _make_get_request(self,url,object_fh,params=None,return_type=None):
    
        if params is None:
            params = {}
        #else:
        #    #????? - what are we doing here? - only including ones with values
        #    #Does requests do this for us?
        #    if PY2:
        #        params = dict((k, v) for k, v in params.iteritems() if v)
        #    else:
        #       params = dict((k, v) for k, v in params.items() if v)
     


        #Example          
        #GroovyBib/1.1 (https://example.org/GroovyBib/; mailto:GroovyBib@example.org) BasedOnFunkyLib/1.4.

        #It is unclear if we need to match this format
        #This is good enough for now
        #Eventually we might allow a user to describe their application
        #version, and url
        ua_str = 'st_crossref/%s (https://github.com/ScholarTools/crossref_api_python; mailto:%s)' % (VERSION,user_config.email)
        
        headers = {'user-agent': ua_str}
        
        r1 = requests.Request('GET',url,params=params,headers=headers)
        prepped = r1.prepare()
        r = self.session.send(prepped)
        
        #r = self.session.get(url,params=params,headers=headers)      

        self.last_prepped = prepped
        self.last_url = url
        self.last_response = r     
        self.last_params = params     
        
        if r.status_code == 404:
            #This typically happens when the DOI is invalid
            #TODO: Make this a named exception
            raise errors.RequestError(r.text)
        
        json_data = r.json()
        if json_data['status'] == 'failed':
            self.last_error = json_data
            raise errors.CrossrefError(json_data['message'])
            
        #temp = ResponseMessageInfo(j,is_list)
        #object_json = temp.json
            
        """
        {'status': 'failed', 'message-type': 'validation-failure', 
        'message': [{'value': 'sample', 
        'message': 'This route does not support sample', 'type': 'parameter-not-allowed'}]}
        """     
        
        #TODO: return_type
        if return_type is 'json':
            return json_data
        else:
            return object_fh(json_data,self)
    
    def _options_to_dict(self,filter=None,n_rows=None,n_random=None,
                     offset=None,query=None,sort_by=None,order=None,
                     facet=None,cursor=None,select=None):
        #https://github.com/CrossRef/rest-api-doc#parameters
        
        #I'm not thrilled about order ...
        #
        params = {
                'cursor':cursor,
                'facet':facet,
                'filter':filter,
                'offset':offset,
                'order':order,
                'query':query,
                'rows':n_rows,
                'select':select,
                'sample':n_random,
                'sort':sort_by}
        
        #TODO: We have some more processing to do here
        #=> filter processsing
        #=> select
        
        """
        DONE query	query terms
        DONE filter={filter_name}:{value}	filter results by specific fields
        DONE rows={#}	results per per page
        DONE offset={#} (mak 10k)	result offset (user cursor for larger /works result sets)
        DONE sample={#} (max 100)	return random N results
        DONE sort={#}	sort results by a certain field
        DONE order={#}	set the sort order to asc or desc
        DONE facet={#}	enable facet information in responses
        DONE cursor={#}	deep page through /works result sets
        
        """
                
        return params
            
    def funders(self,filter=None,n_rows=None,
                     offset=None,query=None,sort_by=None,order=None,
                     facet=None,cursor=None,return_type=None):
        
        """
        n_random not supported
        select not supported
        """
        
        params = self._options_to_dict(filter=filter,n_rows=n_rows,
             n_random=None,offset=offset,query=query,
             sort_by=sort_by,order=order,facet=facet,cursor=cursor,
             select=None)
                
        url = self.BASE_URL + 'funders'
        return self._make_get_request(url,models.FundersSearchResult,params,return_type)
    
    def journals(self,filter=None,n_rows=None,n_random=None,
                     offset=None,query=None,sort_by=None,order=None,
                     facet=None,cursor=None,return_type=None):
        
        params = self._options_to_dict(filter=filter,n_rows=n_rows,
             n_random=n_random,offset=offset,query=query,
             sort_by=sort_by,order=order,facet=facet,cursor=cursor,
             select=None)
        
        url = self.BASE_URL + 'journals'
        return self._make_get_request(url,models.JournalSearchResult,params,return_type)
    
    def licenses(self,filter=None,n_rows=None,n_random=None,
                     offset=None,query=None,sort_by=None,order=None,
                     facet=None,cursor=None,select=None,return_type=None):
        
        """
        
        ??? - This seems to return all licenses
        
        Example Data
        ------------
        .URL
        .work-count
        """
        
        params = self._options_to_dict(filter=filter,n_rows=n_rows,
             n_random=n_random,offset=offset,query=query,
             sort_by=sort_by,order=order,facet=facet,cursor=cursor,
             select=None)
        
        url = self.BASE_URL + 'licenses'
        #return self._make_search_request(url,models.LicenseSearchResult,options,_filter)
        return self._make_get_request(url,models.LicenseSearchResult,params,return_type)    
    
    def members(self,filter=None,n_rows=None,n_random=None,
                     offset=None,query=None,sort_by=None,order=None,
                     facet=None,cursor=None,select=None,return_type=None):
        
        
        params = self._options_to_dict(filter=filter,n_rows=n_rows,
             n_random=n_random,offset=offset,query=query,
             sort_by=sort_by,order=order,facet=facet,cursor=cursor,
             select=select)
        
        url = self.BASE_URL + 'members/'
        return self._make_get_request(url,models.MembersSearchResult,params,return_type)
    
    def works(self,filter=None,n_rows=None,n_random=None,
                     offset=None,query=None,sort_by=None,order=None,
                     facet=None,cursor=None,select=None,return_type=None):
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
        
        params = self._options_to_dict(filter=filter,n_rows=n_rows,
             n_random=n_random,offset=offset,query=query,
             sort_by=sort_by,order=order,facet=facet,cursor=cursor,
             select=select)
        
        url = self.BASE_URL + 'works'
        #return self._make_search_request(url,models.WorksSearchResult,options,_filter)
        return self._make_get_request(url,models.WorksSearchResult,params,return_type)

    def work_types(self):
        """
        
        """
        
        if self._work_types is None:
            url = self.BASE_URL + 'types'
            self._work_types = self._make_get_request(url,models.TypesList,None,None)

        return self._work_types
    
    def doi_info(self,doi):
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
        
        """
        
        doi = _clean_doi(doi)
        
        url = self.BASE_URL + 'works/' + doi
        
        try:
            return self._make_get_request(url,models.work_single)
        except errors.RequestError:
            #TODO: Check for 404
            #last_response.status_code
            #TODO: Do this only if debugging is enabled
            if self.debug:
                #TODO: Also report code
                print("Error msg from server: " + self.last_response.text)
            raise errors.InvalidDOI('Invalid DOI requested: ' + doi)
        
        #return self._make_get_request(url,models.Work,kwargs)
        
    def funder_info(self,funder_id):
        """
        
        Example Data
        ------------

        """
        
        url = self.BASE_URL + 'funders/' + funder_id
        return self._make_get_request(url,models.funder_single)

    def journal_info(self,journal_id):
        """
        
        Example Data
        ------------

        """
        
        url = self.BASE_URL + 'journals/' + journal_id
        return self._make_get_request(url,models.journal_single)
    
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
        return self._make_get_request(url,models.member_single)
    

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
        
        return self._make_get_request(url,models.prefix_single)    

    
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