# -*- coding: utf-8 -*-
"""
"""

from collections import defaultdict
from datetime import datetime

from . import utils
td = utils.get_truncated_display_string
cld = utils.get_list_class_display

#keys are based on ids


class ResponseObject(object):
    
    #I made this a property so that the user could change this processing
    #if they wanted. For example, this would allow the user to return authors
    #as just the raw json (from a document) rather than creating a list of 
    #Persons
    object_fields = {}
    
    renamed_fields = {}
    
    def __init__(self,json):
        self.json = json
        
    def __getattr__(self, name):
        
        #This check allows an optional field to be returned as None
        #even if it isn't in the current json definition
        #
        #This however still keeps in place errors like if you ask for:
        #document.yeear <= instead of year
        
        #TODO: I did some quick copy_paste, this may need to change ...

        #TODO: new_name is a poor variable name, it really represents
        #the name of the entry in the json dict
        d = self.fields()

        if name in d:
            new_name = name
        elif name in self.renamed_fields:
            new_name = name #Do we want to do object lookup on the new name?
            name = self.renamed_fields[name]
        else:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))
        
        if name in d:
            fh = d[name]
            if fh is None:
                value = self.json.get(new_name)
            else:
                #We will let the function handle work with the input name
                value = fh(self,name)
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
        self.all_ids = [x['id'] for x in self.json]
        
    def __repr__(self):
        pv = ['docs',cld(self.docs),
              'all_ids',td(self.all_ids)]

        return utils.property_values_to_string(pv)      

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
  
class JournalList(ResponseObject):
    
    def __init__(self,json,api):
        super(JournalList, self).__init__(json)
        
        self.api = api
        self.journals = [Journal(x,api) for x in self.json]
        

class Journal(ResponseObject):

    """
    Attributes
    ----------
    breakdowns :
        Ex. {'dois-by-issued-year': [[2014, 24], [2015, 20], [2016, 7]]}
        
    counts :
        Ex. {'backfile-dois': 12, 'total-dois': 51, 'current-dois': 39}
    coverage :
        Ex. {'update-policies-backfile': 0.0, 'funders-current': 0.0, 'award-numbers-current': 0.0, 'orcids-current': 0.0 ...
    flags:
        Ex. {'deposits-award-numbers-current': False, 'deposits-award-numbers-backfile': False, ...
        
    """
    
    
    def __init__(self,json,api):
        super(Journal, self).__init__(json)


    @classmethod
    def fields(cls):
        #TODO: this is not done, will also need to split by type
        return _l2d([
        'breakdowns', None, 
        'last_status_check_time',None,
        'counts', None, 
        'ISSN', None,
        'publisher',None,
        'coverage',None,
        'title',None,
        'flags',None])
        
    def __repr__(self):
        pv = ['breakdowns',td(self.breakdowns),
                'last_status_check_time',self.last_status_check_time,
                'counts',td(self.counts),
                'ISSN',self.ISSN,
                'publisher',self.publisher,
                'coverage',td(self.coverage),
                'title',self.title,
                'flags',td(self.flags)]

        return utils.property_values_to_string(pv)        
        #'all_titles',lambda x,y: _get_alternate_field(x,'title'), #This is an example, we might not really use it



      
class WorkList(ResponseObject):
    
    """
    Attributes
    ----------
    docs : [Work]    
    """
    
    
    def __init__(self,json,api):
        super(WorkList, self).__init__(json)
        
        self.api = api  
        self.docs = [_create_work(utils.clean_dict_keys(x),api) for x in self.json]
        
        types = [x['type'] for x in self.json]
        
        docs_by_type = defaultdict(list)

        for x in self.json:
            cur_type = x['type']
            docs_by_type[cur_type].append(x)

        type_fields = {}

        for key in docs_by_type:
            docs = docs_by_type[key]
            all_keys_list = [set(x.keys()) for x in docs]
            all_unique_fields = sorted(set.union(*all_keys_list))
            type_fields[key] = all_unique_fields
        
        self.docs_by_type = docs_by_type
        self.type_fields = type_fields
        self.unique_types = set(types)        
        
    def __repr__(self):
        pv = [
            'api',cld(self.api),
             'docs',cld(self.docs),
            'unique_types',self.unique_types]

        return utils.property_values_to_string(pv)        

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
        self.api = api
        super(Work, self).__init__(json)
        
    def get_prefix_info(self):
        pass        
    
        


class PrefixList(ResponseObject):

    def __init__(self,json,api):
        super(Work, self).__init__(json)
        self.docs = [Prefix(utils.clean_dict_keys(x),api) for x in self.json]

    def __repr__(self):
        pv = ['docs',cld(self.docs)]

        return utils.property_values_to_string(pv)  

class Prefix(ResponseObject):

    def __init__(self,json,api):
        super(Work, self).__init__(json)
        

#------------------------------------------------------------------------
class BookSection(Work):
    
    def __init__(self,json,api):
        super(BookSection, self).__init__(json,api)    

class Monograph(Work):
    
    def __init__(self,json,api):
        super(Monograph, self).__init__(json,api)     

class Report(Work):
    
    def __init__(self,json,api):
        super(Report, self).__init__(json,api)  
        
class BookTrack(Work):
    
    def __init__(self,json,api):
        super(BookTrack, self).__init__(json,api)  

class JournalArticle(Work):
    
    def __init__(self,json,api):
        super(JournalArticle, self).__init__(json,api)  

class BookPart(Work):
    
    def __init__(self,json,api):
        super(BookPart, self).__init__(json,api)  

class Other(Work):
    
    def __init__(self,json,api):
        super(Other, self).__init__(json,api)  

class Book(Work):
    
    def __init__(self,json,api):
        super(Book, self).__init__(json,api)  

class JournalVolume(Work):
    
    def __init__(self,json,api):
        super(JournalVolume, self).__init__(json,api)  
        
class BookSet(Work):
    
    def __init__(self,json,api):
        super(BookSet, self).__init__(json,api)  
        
class ReferencyEntry(Work):
    
    def __init__(self,json,api):
        super(ReferencyEntry, self).__init__(json,api)  
        
class ProceedingsArticle(Work):
    
    def __init__(self,json,api):
        super(ProceedingsArticle, self).__init__(json,api)  

class UnhandledWork(Work):

    def __init__(self,json,api):
        super(UnhandledWork, self).__init__(json,api)   
    
    def _null(self):
        #This will change, need to expand work by types
        self.DOI = None
        self.ISSN = None
        self.URL = None
    
    @classmethod
    def fields(cls):
        #TODO: this is not done, will also need to split by type
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
        'title', _list_to_element,
        'all_titles',lambda x,y: _get_alternate_field(x,'title'), #This is an example, we might not really use it
        'type', None,
        'update_policy',None,
        'volume', None])
                
    def __repr__(self):
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

        return utils.property_values_to_string(pv)

#List is based on id, not label
type_objects = {
    'book-section':BookSection,
    'monograph':Monograph,
    'report':Report,
    'book-track':BookTrack,
    'journal-article':JournalArticle,
    'book-part':BookPart,
    'other':Other}

def _create_work(json,api):
    
    work_type = json['type']
    if work_type in type_objects:
        fh = type_objects[work_type]
        return fh(json,api)
    else:
        return UnhandledWork(json,api)        
            
def _l2d(input_list):
    #property-value pairs to dictionary
    keys = input_list[::2]
    values = input_list[1::2]
    return {k:v for k,v in zip(keys,values)}
    
def _list_to_element(self,name):
    """
    This is useful in cases in which we get a list which usually only has 1 element
    """
    value = self.json.get(name)
    if value is None:
        return None
    else:
        return value[0]
    
def _get_alternate_field(self,alternate_name):
    return self.json.get(alternate_name)
