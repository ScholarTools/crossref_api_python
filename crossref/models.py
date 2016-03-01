# -*- coding: utf-8 -*-
"""
"""

from datetime import datetime

from . import utils
td = utils.get_truncated_display_string
cld = utils.get_list_class_display


class ResponseObject(object):
    
    #I made this a property so that the user could change this processing
    #if they wanted. For example, this would allow the user to return authors
    #as just the raw json (from a document) rather than creating a list of 
    #Persons
    object_fields = {}    
    
    def __init__(self,json):
        self.json = json
        
    def __getattr__(self, name):
        
        #This check allows an optional field to be returned as None
        #even if it isn't in the current json definition
        #
        #This however still keeps in place errors like if you ask for:
        #document.yeear <= instead of year
        d = self.fields()
        if name in d:
            #TODO: Build in evaluation of methods
            value = self.json.get(name)
            return value
        else:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))

    @classmethod
    def __dir__(cls):
        d = set(dir(cls) + cls.fields().keys())
        d.remove('fields')
        d.remove('object_fields')

        return sorted(d)

    @classmethod
    def fields(cls):
        """
        This should be overloaded by the subclass.
        """
        return []

class TypesList(ResponseObject):
    
    def __init__(self,json,api):
        super(TypesList, self).__init__(json)    
        self.docs = [Type(x,api) for x in self.json]

class Type(ResponseObject):
    """
    Attributes
    ----------
    label
    id 
    """
    def __init__(self,json,api):
        super(Type, self).__init__(json)    

    def _null(self):
        self.label = None
        self.id = None

    @classmethod
    def fields(cls):
        return _l2d([
        'label', None, 
        'id',None])
        
    def __repr__(self,pv_only=False):
        pv = ['label',self.label,
                'id',self.id]
        return utils.property_values_to_string(pv)
        
class WorkList(ResponseObject):
    
    """
    Attributes
    ----------
    docs : [Work]    
    """
    
    
    def __init__(self,json,api):
        super(WorkList, self).__init__(json)
        
        self.api = api  
        self.docs = [Work(utils.clean_dict_keys(x),api) for x in self.json]
        
        #TODO: We might want to break up by type
        all_keys_list = [set(x.keys()) for x in self.json]
        all_unique_keys = sorted(set.union(*all_keys_list))
        all_types = [x.get('type') for x in self.json]
        #import pdb
        #pdb.set_trace()
        #self.all_keys = set([])

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
        known types include: TODO: Update with output of types-list
        #and add a test for inclusion and exclusion
        - book-chapter
        - component
        - dataset
        - dissertation
        - journal-article
        - journal-issue
        - monograph
        - proceedings-article
    page :
    subject : list
        TODO: Where are these coming from? Are these keywords? How are these
        decideed upon?
    score :
        Any values other than 1?
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
        
    def _null(self):
        """
        TODO: Ask on SO about this, is there an alternative approach?
        It does expose tab completion in Spyder ...
        """
        self.DOI = None
        self.ISSN = None
        self.URL = None
    
    @classmethod
    def fields(cls):
        #TODO: Let's insert transforming functions here
        return _l2d([
        'DOI', None, 
        'ISBN',None,
        'ISSN', None, 
        'URL', None,
        'alternative_id',None,
        'archive',None,
        'article_number',None,
        'assertion',None,
        'author', None,
        'container_title', None,
        'created', None,  
        'deposited', None,
        'editor',None,
        'funder',None,
        'indexed', None,
        'issue', None,
        'issued', None,
        'link',None,
        'member', None,
        'page', None,
        'prefix', None, 
        'published_online',None,
        'published_print', None,
        'publisher', None,
        'reference_count', None,
        'score', None,
        'source', None,  
        'subject', None, 
        'subtitle', None, 
        'title', None, 
        'type', None,
        'update_policy',None,
        'volume', None])
                
    def __repr__(self,pv_only=False):
        pv = ['ISSN',self.ISSN,
                'title',self.title,
                'URL',self.URL,
                'subtitle',self.subtitle,
                'container_title',self.container_title,
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
            
def _l2d(input_list):
    #property-value pairs to dictionary
    keys = input_list[::2]
    values = input_list[1::2]
    return {k:v for k,v in zip(keys,values)}
    
