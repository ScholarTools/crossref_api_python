#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

import requests
from bs4 import BeautifulSoup

#This sort of works, but the values are a different form
"""
relations_url = 'https://www.crossref.org/schemas/relations.xsd'

temp = requests.get(relations_url)

soup = BeautifulSoup(temp.text, 'xml')

tags = soup.find_all('xsd:element',{'name':'inter_work_relation'})
t2 = tags[0].find_all('xsd:enumeration')

values = sorted([x['value'] for x in t2])

known_relations = ['basedOnData',
 'compiles',
 'continues',
 'documents',
 'hasComment',
 'hasDerivation',
 'hasPart',
 'hasRelatedMaterial',
 'hasReply',
 'hasReview',
 'isBasedOn',
 'isBasisFor',
 'isCommentOn',
 'isCompiledBy',
 'isContinuedBy',
 'isDataBasisFor',
 'isDerivedFrom',
 'isDocumentedBy',
 'isPartOf',
 'isReferencedBy',
 'isRelatedMaterial',
 'isReplyTo',
 'isRequiredBy',
 'isReviewOf',
 'isSupplementTo',
 'isSupplementedBy',
 'references',
 'requires']
"""

def test_schemas():
    
    LEAD_IN_TEXT = 'but must be one of:'
    
    temp = api.works(filter='relation.type:madeUpRelation')
    
    temp_str = api.last_error['message'][0]['message']
     
    I = temp_str.find(LEAD_IN_TEXT)
    
    temp_str2 = temp_str[I+len(LEAD_IN_TEXT):]
    
    temp_values = temp_str2.split(',')
    
    current_values = sorted([x.strip() for x in temp_values])
    
    known_values = ['based-on-data',
 'compiles',
 'continues',
 'documents',
 'has-comment',
 'has-derivation',
 'has-expression',
 'has-format',
 'has-manifestation',
 'has-manuscript',
 'has-part',
 'has-preprint',
 'has-related-material',
 'has-reply',
 'has-review',
 'has-translation',
 'has-version',
 'is-based-on',
 'is-basis-for',
 'is-comment-on',
 'is-compiled-by',
 'is-continued-by',
 'is-data-basis-for',
 'is-derived-from',
 'is-documented-by',
 'is-expression-of',
 'is-identical-to',
 'is-manifestation-of',
 'is-manuscript-of',
 'is-original-form-of',
 'is-part-of',
 'is-preprint-of',
 'is-referenced-by',
 'is-related-material',
 'is-replaced-by',
 'is-reply-to',
 'is-required-by',
 'is-review-of',
 'is-same-as',
 'is-supplement-to',
 'is-supplemented-by',
 'is-translation-of',
 'is-varient-form-of',
 'is-version-of',
 'references',
 'replaces',
 'requires']
    