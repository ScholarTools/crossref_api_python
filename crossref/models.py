# -*- coding: utf-8 -*-
"""
"""
#Std Lib Imports
#--------------------------
#import itertools
from collections import defaultdict
#from datetime import datetime
import sys
import re

PY2 = int(sys.version[0]) == 2

#Local imports
#--------------------------
from . import utils
display_class = utils.display_class
td = utils.get_truncated_display_string
cld = utils.get_list_class_display
pv = utils.property_values_to_string

#keys are based on ids

if PY2:
    import __builtin__ as builtins
else:
    import builtins



#----- Generic 
def pass_through(data,api):
    return data

#https://stackoverflow.com/questions/16380575/python-decorating-property-setter-with-list

class ExtendedList(list):

    #This class dynamically creates a class instance when accessing a
    #member of the list
    
    #This needs to be defined as a function handle by the sub class
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
    
    def __repr__(self):
       #return '%s: %d elements%s\n' % (type(self),len(self.data),type(self.item_class))
       return '%d element list of type %s' %(len(self.data),self.item_class)


#=> issn-type
#=> last-status-check-time

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
        """
        Parameters
        ----------
        json : dict
        """
        self.json = json
        
    def get(self,key,default=None):
        if key in self.json.keys():
            return self.json[key]
        else:
            return default
        
    def __getitem__(self, key):
        return self.json[key]    
        
    def __getattr__(self, name):
        
        #TODO: At some point I think we had optional field support and this
        #has since been removed - right now we only allow:
        #1) keys from json
        #2) keys in renamed_fields
        if name in self.json.keys():
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
        
    def __dir__(self):
        #Note that fields() needs an instance :/
        #
        #d  = super(ResponseObject, self).__dir__()
        #d = set(list(dir(super(ResponseObject, self))) + self.fields())
        #d = set(list(builtins.dir(self)) + self.fields())
        d = dir(type(self)) + list(self.__dict__.keys()) + self.fields()
        #import pdb
        #pdb.set_trace()
        #d.remove('fields')
        #d.remove('object_fields')

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
            disp_str = _short_string(value)
            temp.extend([key,disp_str])
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

#---- Types
#============================================
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
  
#---- Funders
#=============================================
class FundersSearchResult(ResponseObject):
    
    other_fields_for_display = ['api','citems']
    
    def __init__(self,json,api):  
        self.api = api
        temp = {'items':json}
        super(FundersSearchResult, self).__init__(temp)
        
        #This class returns only the items as a list (json)
        #rather than as a dict with meta data and the results
        self.citems = FundersList(json,api)  
        
class Funder(ResponseObject):

    """
        
    """
    
    def __init__(self,json,api):
        super(Funder, self).__init__(json)



class FundersList(ExtendedList):
    
    item_class = Funder
    
    def __init__(self,json,api):
        super(FundersList, self).__init__(json,api)      


        
#---- Journals
#=============================================
class JournalSearchResult(ResponseObject):
    
    other_fields_for_display = ['api','citems']
    
    def __init__(self,json,api):
        self.api = api
        temp = {'items':json}
        super(JournalSearchResult, self).__init__(temp)
        
        #This class returns only the items as a list (json)
        #rather than as a dict with meta data and the results
        self.citems = JournalsList(json,api)        

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
        
    #TODO: Support getting works from this journal ...

class JournalsList(ExtendedList):
    
    item_class = Journal
    
    def __init__(self,json,api):
        super(JournalsList, self).__init__(json,api)       

  

#---- Licenses
#===========================================================
class LicenseSearchResult(ResponseObject):
    
    other_fields_for_display = ['api','citems']
    
    def __init__(self,json,api):
        self.api = api
        temp = {'items':json}
        super(LicenseSearchResult, self).__init__(temp)
        
        #This class returns only the items as a list (json)
        #rather than as a dict with meta data and the results
        self.citems = LicensesList(json,api)    

class License(ResponseObject):

    """
    Examples
    --------
    <class 'crossref.models.Journal'>:
           URL: http://academic.oup.com/journals/pages/about_us/legal/notices
    work-count: 2882
    """
    
    
    def __init__(self,json,api):
        super(License, self).__init__(json)

class LicensesList(ExtendedList):
    
    item_class = License
    
    def __init__(self,json,api):
        super(LicensesList, self).__init__(json,api)  
      

#---- Members
#==========================================
class MembersSearchResult(ResponseObject):
    
    other_fields_for_display = ['api','citems']
    
    def __init__(self,json,api):
        self.api = api
        super(MembersSearchResult, self).__init__(json)
        self.citems = MembersList(json['items'],api)
        
       
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


#---- Works
#===========================================================
class WorksSearchResult(ResponseObject):
    
    """
    Attributes
    ----------
      
    """
    
    other_fields_for_display = ['api','citems']
    
    
    def __init__(self,json,api):
        self.api = api
        temp = {'items':json}
        super(WorksSearchResult, self).__init__(temp)
               
        self.citems = FundersList(json,api)  

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
    
class JournalArticle(Work):
    pass

class WorksList(ExtendedList):
    item_class = Funder
    
    def __init__(self,json,api):
        super(WorksList, self).__init__(json,api)     
    
        
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
