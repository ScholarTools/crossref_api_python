# -*- coding: utf-8 -*-
"""
"""
#Std Lib Imports
#--------------------------
#import itertools
from collections import defaultdict
#from datetime import datetime

#Local imports
#--------------------------
from . import utils
display_class = utils.display_class
td = utils.get_truncated_display_string
cld = utils.get_list_class_display
pv = utils.property_values_to_string

#keys are based on ids


#----- Generic 
def pass_through(data,api):
    return data

#https://stackoverflow.com/questions/16380575/python-decorating-property-setter-with-list

class ExtendedList(list):

    #This class dynamically creates a class instance when accessing a
    #member of the list
    
    #This needs to be defined as a function handle for the sub class
    item_class = None
    
    def __init__(self, data, api):
        self.api = api
        self.data = data

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, index):
        #Convery index to class
        #[Member(utils.clean_dict_keys(x),api) for x in self.json]
        return self.item_class(self.data[index],self.api)
    


class ResponseObject(object):
    
    #I made this a property so that the user could change this processing
    #if they wanted. For example, this would allow the user to return authors
    #as just the raw json (from a document) rather than creating a list of 
    #Persons
    #
    #Object fields must have function handles that accept self and the field name
    object_fields = {}
    
    renamed_fields = {}
    
    other_fields_for_display = []
        
    def __init__(self,json):
        self.json = json
        
    def __getattr__(self, name):
        
        #TODO: At some point I think we had optional field support and this
        #has since been removed - right now we only allow:
        #1) keys from json
        #2) keys in renamed_fields
        if name in json.keys():
            pass
        elif name in self.renamed_fields:
            #What this acomplishes is that it let's us ask for
            #my_cool_variable which then internally accesses my_variable
            name = self.renamed_fields[name]
        else:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))
        
        value = self.json.get(name)
        
        if value is None:
           return None
        elif name in self.object_fields:
            #Here we return the value after passing it to a method
            #fh => function handle
            #
            #Only the value is explicitly passed in
            #Any other information needs to be explicitly bound
            #to the method
            method_fh = self.object_fields[name]
            return method_fh(self,name)
        else:
            return value
        
    @classmethod
    def __dir__(cls):
        d = set(list(dir(cls)) + cls.fields())
        d.remove('fields')
        d.remove('object_fields')

        return sorted(d)

    def fields(self):
        """
        This should be overloaded by the subclass.
        """
        return list(self.json.keys()) + self.other_fields_for_display
    
    def __repr__(self):
        temp = []
        for key in self.json.keys():
            #TODO: This doesn't support non_json fields and it doesn't respect
            #any object transformation that might occur
            disp_str = _short_string(self.json[key])
            temp.extend([key,disp_str])
        for key in self.other_fields_for_display:
            value = self.__dict__[key]
            temp.extend([key,value])
        return display_class(self,temp)
    
def _short_string(value):
    MAX_LENGTH = 30 #default was a bit long for td
    disp_string = str(value)
    if len(disp_string) < MAX_LENGTH:
        return disp_string
    
    if type(value) is dict:
        return '<dict> with %d fields' % len(value.keys())
    elif type(value) is list:
        #TODO: If length 1 just print the truncated list
        return '<list> len %d' % len(value)
    else:
        s = str(value)
        return td(s,max_length=MAX_LENGTH)  

class TypesList(ResponseObject):
    
    """
    A list of the various types that are supported by CrossRef
    e.g. journal, book, book-chapter, etc.
    
    
    /types
    """
    
    def __init__(self,json,api):
        super(TypesList, self).__init__(json)    
        #self.objs = [Type(x,api) for x in self.json]
        self.raw = json
        self.ids = [x['id'] for x in self.json]
        self.labels = [x['label'] for x in self.json]
        #Not sure how to make this more useful to the end user (if at all)
        
    def __repr__(self):
        pv = ['raw',td(self.raw),
                'ids',td(self.ids),
              'labels',td(self.labels)]

        return utils.property_values_to_string(pv)      

#class Type(ResponseObject):
#    """
#    Created from TypesList
#    
#    
#    Attributes
#    ----------
#    label
#    id 
#    """
#    def __init__(self,json,api):
#        super(Type, self).__init__(json)    
#
#    def _null(self):
#        self.label = None
#        self.id = None
#
#    @classmethod
#    def fields(cls):
#        return _l2d([
#        'label', None, 
#        'id',None])
#        
#    def __repr__(self,pv_only=False):
#        pv = ['label',self.label,
#                'id',self.id]
#        return utils.property_values_to_string(pv)
  
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

#---- Works

class Work(ResponseObject):
    
    """
    Documentation!
    https://github.com/Crossref/rest-api-doc/blob/master/api_format.md#work
    
    
    Relevant Endpoints
    ------------------
    /works/{doi}
    
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
        #The api isn't used yet but is meant to allow further calls
        #in the methods
        self.api = api
        super(Work, self).__init__(json)
        
    def get_prefix_info(self):
        pass        
    
        
#----  Prefix
#=================================================

class PrefixList(ResponseObject):

    def __init__(self,json,api):
        super(PrefixList, self).__init__(json)
        self.docs = [Prefix(utils.clean_dict_keys(x),api) for x in self.json]

    def __repr__(self):
        pv = ['docs',cld(self.docs)]

        return utils.property_values_to_string(pv)  

class Prefix(ResponseObject):
    
    """
    Relevant Endpoints
    ------------------
    /prefixes/{owner_prefix}
    
    """

    def __init__(self,json,api):
        super(Prefix, self).__init__(json)
        
    def get_member_info(self):
        #TODO: Implement this
        pass

#---- Members
#==========================================
class MembersSearchResult(ResponseObject):
    
    other_fields_for_display = ['api','citems']
    
    def __init__(self,json,api):
        self.api = api
        super(MembersSearchResult, self).__init__(json)
        self.citems = MembersList(json['items'],api)
        
    

        
        
        #self.api = api
        #super(MemberList, self).__init__(json)
        #self.docs = [Member(utils.clean_dict_keys(x),api) for x in self.json]

    
    #def item_as_class(self,index):
    #    return Member(self.json['items'][index],self.api)
    
    #TODO: Can we add converted documents
    #=> Let's just show the methods
    
    #TODO: 
    #- iterable
    #- Next X
    
    """
    #def __repr__(self):
    #    pv = ['docs',cld(self.docs)]
    #
    #    return utils.property_values_to_string(pv) 
    """
        
class Member(ResponseObject):
    
    """
    Documentation??? - I can't find it
    https://github.com/Crossref/rest-api-doc/blob/master/api_format.md#work


    Relevant Endpoints
    ------------------
    /members/{member_id}
    
    Example Data
    ------------
        <class 'crossref.models.Member'>:
    last_status_check_time: 1522803773023
              primary_name: Wiley-Blackwell
                    counts: <dict> with 3 fields
                breakdowns: <dict> with 1 fields
                        => # of dois by year
                  prefixes: <list> len 33
                  coverage: <dict> with 18 fields
                        => % of tasks that have been completed
                            e.g. 'references-current' : 0.729
                    prefix: <list> len 33
                        id: 311
                    tokens: ['wiley', 'blackwell']
                     flags: <dict> with 20 fields
                        => indicates deposit behavior
                  location: 111 River Street Hoboken NJ 07...
                     names: <list> len 33
                        => contains list of journals?
    
    """

    def __init__(self,json,api):
        super(Member, self).__init__(json)       
        
        #Any other methods
        #=> get prefix info
 
class MembersList(ExtendedList):
    
    item_class = Member
    
    def __init__(self,json,api):
        super(MembersList, self).__init__(json,api)       

#----  Work Types
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
