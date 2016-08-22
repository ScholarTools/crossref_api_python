# -*- coding: utf-8 -*-
"""
These methods are specific to working with DOIs and are not part of the standard
API or may expose a part of the API in a different in useful way.


DOI notes:
----------
1) DOIs are not case sensitive



"""

import requests

from .errors import InvalidDOI, UnhandledHTTPResonseFailure

# TODO: How do we want to support session state? Pass it in and make
# a generic shared method


def is_valid(doi):
    try:
        get_doi_link(doi)
        return True
    except InvalidDOI:
        return False


def follow_doi(doi):
    # TODO: I've seen this fail when the page includes a javascript redirect
    # call get_doi_link then follow the call allowing redirects until it stops
    pass


def get_doi_link(doi):
    
    """
    This was created to handle returning the link that the doi points to without
    retrieving the page content
    """    
    
    #TODO: Optionally take in session and use make_request function
    
    cleaned_doi = clean_doi(doi,_format='http')
    r = requests.get(cleaned_doi,allow_redirects=False)
    if r.status_code != 303:
        if r.status_code == 404:
            raise InvalidDOI('Invalid DOI: %s' % cleaned_doi)
        else:
            print('Status code: %s' % r.status_code)
            raise UnhandledHTTPResonseFailure('Unexpected response when resolving doi: %s' % cleaned_doi)
        
    
    doi_link = r.headers['Location']
    
    # Often times this link is to a local server which then gets the item:
    #
    # e.g.
    # http://dx.doi.org/10.1002/nau.1930090206  points to (303)
    # http://doi.wiley.com/10.1002/nau.1930090206 points to (302)
    # http://onlinelibrary.wiley.com/resolve/doi?DOI=10.1002/nau.1930090206
    
    return doi_link

def clean_doi(doi,_format='value'):
    """
    TODO: Support different return formats:
        
    Parameters
    ----------
    _format
        - 'value' : e.g. 10.1002/nau.1930090206
        - 'doi'   : e.g. doi:10.1002/nau.1930090206
        - 'http'  : http://dx.doi.org/10.1002/nau.1930090206
        - 'https' : https://dx.doi.org/10.1002/nau.1930090206
    value : e
    """
    
    if doi.startswith('10.'):
        #TODO: do other registries exist? 100.?
        value = doi
    else:
        lower_doi = doi.lower()
        if lower_doi.startswith('doi:'):
            #TODO: Do we ever get doi: followed by a space ?
            value = doi[4:]
        elif lower_doi.startswith('http://dx.doi.org/'):
            value = doi[18:]
        elif lower_doi.startswith('https://dx.doi.org/'):
            value = doi[19:]
        else:
            raise Exception('Form of DOI is unrecognized, value = %s' % doi)
        
    if _format == 'value':
        return value
    elif _format == 'doi':
        return 'doi:' + value
    elif _format == 'http':
        return 'http://dx.doi.org/' + value
    elif _format == 'http':
        return 'http://dx.doi.org/' + value    
    else:
        raise Exception('Unhandled format for DOI cleaning')


# This could be shared by anything above that may or may not have a session
# passed in
def _make_request():
    pass
