# -*- coding: utf-8 -*-
"""
"""

import crossref.doi as cdoi

#Is valid?
#---------------------------------------------------
doi = '10.1111/cheese'
doi_valid_status = cdoi.is_valid(doi)
print('DOI valid status: %s' % doi_valid_status)

#Gettng the DOI link
#----------------------------------------------------
#TODO: Should verify that this throws the expected error
#doi = '10.1111/cheese'
#link = cdoi.get_doi_link(doi)
#print('DOI link is: %s' % link)

doi = '10.1111/j.1525-1403.2006.00056.x'
link = cdoi.get_doi_link(doi)
print('DOI link is: %s' % link)

#Cleaning the DOI
#----------------------------------------------------
#TODO: Need to validate output
doi = 'doi:10.1002/nau.1930090206'
cleaned_doi = cdoi.clean_doi(doi,_format='value')
print('Cleaned doi to value is: %s' % cleaned_doi)

doi = 'http://dx.doi.org/10.1002/nau.1930090206'
cleaned_doi = cdoi.clean_doi(doi,_format='value')
print('Cleaned doi to value is: %s' % cleaned_doi)

doi = 'https://dx.doi.org/10.1002/nau.1930090206'
cleaned_doi = cdoi.clean_doi(doi,_format='value')
print('Cleaned doi to value is: %s' % cleaned_doi)

doi = '10.1002/nau.1930090206'
cleaned_doi = cdoi.clean_doi(doi,_format='value')
print('Cleaned doi to value is: %s' % cleaned_doi)