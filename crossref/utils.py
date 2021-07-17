# -*- coding: utf-8 -*-
"""
#TODO: break out display utils to another module

This could probably be made private since the user doesn't really need
to call it

from crossref import utils
"""

import os.path as path

#I'm not thrilled about including this. It might change.
import pandas


def test_options(fcn,params,lead_in_text,ref_table):
    pass

class OptionComparison():
    
    def __init__(self,local_ref_values,server_new_values):
        """
        Parameters
        ----------
        local_ref_values : [str]
            Reference values are the values known to the program.
        server_new_values : [str]
            New values are the values from the server that may be different
            from the local reference values
        """
        
        ref_set = set(local_ref_values)
        new_set = set(server_new_values)
        
        self.local_ref_only = ref_set.difference(new_set)
        self.new_only = new_set.difference(ref_set)
        self.in_both = ref_set.intersection(new_set)
        
        
    def __repr__(self):
        #TODO: This needs to be implemented
        pass
        

def fix_clip_values():
    
    """
    
    1) Copy list to clipboard
    2) Run this function:
        from crossref.utils import fix_clip_values as fc
        fc()
    3) Copy the printed result to an Excel file
    
    https://stackoverflow.com/questions/579687/how-do-i-copy-a-string-to-the-clipboard-on-windows-using-python
    """
    
    #Python 3
    from tkinter import Tk
    temp_str = Tk().clipboard_get()
    temp2 = temp_str.splitlines()
    
    output = [_clean_copied_option_values(x) for x in temp2]
    for x in output:
        print(x)
    
    #Tk().clipboard_set(output)
    

def load_filter_table(file_name):
    
    #Path
    #
    if not file_name.endswith('.tsv'):
        file_name = file_name + '.tsv'
                
    package_path = path.split(__file__)[0]
    root_path = path.split(package_path)[0]
    file_path = path.join(root_path,'docs','options',file_name)

    return pandas.read_csv(file_path,sep='\t')


def get_valid_options(temp_str,lead_in_text):
    """
    This parses a string of the format:
        
        temp_str = 'These are the options: test1,test2,test3'
        lead_in_text = 'options:'
        
        get_valid_options(temp_str,lead_in_text)
        
        => ['test1','test2','test3']
    """
    
    I = temp_str.find(lead_in_text)
    
    temp_str2 = temp_str[I+len(lead_in_text):]
    
    temp_values = temp_str2.split(',')
    
    current_values = sorted([x.strip() for x in temp_values])
    
    return current_values

def display_class(class_instance,pv,method_pv=None):
    
    #TODO: Handle methods
    
    return ('%s:\n' % type(class_instance) 
            + property_values_to_string(pv,extra_indentation=4))

def float_or_none_to_string(x):
    if x is None:
        return 'None'
    else:
        return '%0.2f'%x

def property_values_to_string(pv,extra_indentation = 0):
    """
    Parameters
    ----------
    pv : OrderedDict
        Keys are properties, values are values
    """

    # Max length

    keys = pv[::2]
    values = pv[1::2]

    key_lengths = [len(x) for x in keys]
    max_key_length = max(key_lengths) + extra_indentation
    space_padding = [max_key_length - x for x in key_lengths]
    key_display_strings = [' ' * x + y for x, y in zip(space_padding, keys)]

    str = u''
    for (key, value) in zip(key_display_strings, values):
        str += '%s: %s\n' % (key, value)

    return str

def get_list_class_display(value):
    """
    TODO: Go from a list of objects to:
    [class name] len(#)
    """
    if value is None:
       return 'None'  
    elif isinstance(value,list):
        #Check for 0 length
        try:
            if len(value) == 0:
                return u'[??] len(0)'
            else:
                return u'[%s] len(%d)' % (value[0].__class__.__name__,len(value))
        except:
            import pdb
            pdb.set_trace()
        #run the code
    else:
        return u'<%s>' % (value.__class__.__name__)

def get_truncated_display_string(input_string,max_length = 50):
    
    #TODO: We should really check for non-string and convert
    if input_string is None:
        return None
    elif isinstance(input_string,list):
        input_string = '%s'%input_string
    elif isinstance(input_string,dict):
        input_string = '%s'%input_string
        
    if len(input_string) > max_length:
        return input_string[:max_length] + '...'
    else:
        return input_string

def user_name_to_file_name(user_name):
    """
    Provides a standard way of going from a user_name to something that will
    be unique (should be ...) for files
    
    NOTE: NO extensions are added

    See Also:
    utils.get_save_root
    """
    
    #Create a valid save name from the user_name (email)
    #----------------------------------------------------------------------
    #Good enough for now ... 
    #Removes periods from email addresses, leaves other characters
    return user_name.replace('.','')

def get_unnasigned_json(json_data,populated_object):
    """
       Given an object which has had fields assigned to it, as well as the 
       JSON dict from which these values were retrieved, this function returns
       a list of keys that were not used for populating the object.
       
       In order to match the attribute names and dictionary keys must have the
       same names.
    """
    if len(json_data) == 0:
        return {}
    else:
        temp_keys = populated_object.__dict__.keys()
        return dict((key,json_data[key]) for key in set(json_data) if key not in temp_keys)

def assign_json(json_data, field_name, optional=True, default=None):
    
    """
    This function can be used to make an assignment to an object. Since the
    majority of returned json repsonses contain optional fields.
    """    
    
    if field_name in json_data:
        return json_data[field_name]
    elif optional:
        return default
    else:
        raise Exception("TODO: Fix me")
        
def clean_dict_keys(d):
    return {x.replace('-', '_'): d[x] for x in d.keys()}


def _clean_copied_option_values(str):
    
    str = str.strip()
    
    if str[-1] == ',':
        return str[1:-2]
    else:
        return str[1:-1]
    