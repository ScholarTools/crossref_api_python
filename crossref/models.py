# -*- coding: utf-8 -*-
"""
"""

from datetime import datetime

from .utils import get_truncated_display_string as td
from .utils import get_list_class_display as cld

from . import utils

class ResponseObject(object):
    
    #I made this a property so that the user could change this processing
    #if they wanted. For example, this would allow the user to return authors
    #as just the raw json (from a document) rather than creating a list of 
    #Persons
    object_fields = {}    
    
    def __init__(self,json):
        #TODO: Parse out wrapper
        self.message_type = json['message-type']
        self.message_version = json['message-version']
        self.status = json['status'] #ok
        d = json['message']
        self.json = { x.replace(':', ''): d[x] for x in d.keys() }

    def __getattr__(self, name):
        
        #This check allows an optional field to be returned as None
        #even if it isn't in the current json definition
        #
        #This however still keeps in place errors like if you ask for:
        #document.yeear <= instead of year
        if name in self.fields():
            value = self.json.get(name)
            if value is None:
                return None
            elif name in self.object_fields:
                method_fh = self.object_fields[name]
                return method_fh(value)
            else:
                return value
        else:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))

    @classmethod
    def __dir__(cls):
        d = set(dir(cls) + cls.fields())
        d.remove('fields')
        d.remove('object_fields')

        return sorted(d)

    @classmethod
    def fields(cls):
        """
        This should be overloaded by the subclass.
        """
        return []
        
class WorkList(ResponseObject):
    
    def __init__(self,json,m):
        pass

class Work(ResponseObject):
    
    """
    Attributes
    ----------
    ISSN: list
        In my first example I saw 2 (print and online?)
    title: list
        Why is this a list?
    URL: string
    subtitle : ?
    container-title: None
    prefix : 
        ex. http://id.crossref.org/prefix/10.1109
    type : string
        journal-article
    page :
    subject : list
    score :
    member :
    created :
        ex. {'date-parts': [[2011, 8, 31]], 'timestamp': 1314805584000, 'date-time': '2011-08-31T15:46:24Z'}
    volume :
    published_print :
    indexed :
    
    """
    
    """
    TODO:
    ------
    - might remove title and subtitle list
    - for multiple ISSN, might split to print and online
    - do I want to do anything with the times?
    - is subject always singular?

    """    
    
    def __init__(self,json,api):
        super(Work, self).__init__(json)
        import pdb
        pdb.set_trace()
        
    def _null(self):
        """
        TODO: Ask on SO about this, is there an alternative approach?
        It does expose tab completion in Spyder ...
        """
        self.ISSN = None
    
    @classmethod
    def fields(cls):
        return ['ISSN', 'title', 'URL', 'subtitle', 'container_title', 'prefix', 
        'type', 'page', 'subject', 'score', 'member', 'created', 'volume', 
        'published_print', 'indexed', 'deposited', 'issue', 'issued', 
        'publisher', 'source', 'author', 'reference_count', 'DOI']
                
    def __repr__(self,pv_only=False):
        #TODO: Set this up like it looks in Mendeley
        pv = ['ISSN',self.ISSN,
                'title',self.title,
                'URL',self.URL,
                'subtitle',self.subtitle,
                'container-title',self.container_title,
                'prefix',self.prefix,
                'type',self.type,
                'page',self.page,
                'subject',self.subject,
                'score',self.score,
                'member',self.member,
                'created',self.created,
                'volume',self.volume,
                'published_print',self.published_print,
                'indexed',self.indexed]
        if pv_only:
            return pv
        else:
            return utils.property_values_to_string(pv)