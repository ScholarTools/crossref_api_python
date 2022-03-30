#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Let's have this be where we define options
"""

class WorksOptions():
    
    #https://api.crossref.org/swagger-ui/index.html#/Works/get_works
    
    """
    fields = [
        query.affiliation - query contributor affiliations
query.author - query author given and family names
query.bibliographic - query bibliographic information, useful for citation look up, includes titles, authors, ISSNs and publication years
query.chair - query chair given and family names
query.container-title - query container title aka. publication name
query.contributor - query author, editor, chair and translator given and family names
query.degree - query degree
query.editor - query editor given and family names
query.event-acronym - query acronym of the event
query.event-location - query location of the event
query.event-name - query name of the event
query.event-sponsor - query sponsor of the event
query.event-theme - query theme of the event
query.funder-name - query name of the funder
query.publisher-location - query location of the publisher
query.publisher-name - query publisher name
query.standards-body-acronym - query acronym of the standards body
query.standards-body-name - query standards body name
query.title - query title
query.translator - query translator given and family names]
    """
    
    def __init__(**kwargs):
        pass
    
    def query_descriptions():
        pass
        str = """
        query.affiliation - query contributor affiliations
        query.author - query author given and family names
        query.bibliographic - query bibliographic information, useful for citation look up, includes titles, authors, ISSNs and publication years
        query.chair - query chair given and family names
        query.container-title - query container title aka. publication name
        query.contributor - query author, editor, chair and translator given and family names
        query.degree - query degree
        query.editor - query editor given and family names
        query.event-acronym - query acronym of the event
        query.event-location - query location of the event
        query.event-name - query name of the event
        query.event-sponsor - query sponsor of the event
        query.event-theme - query theme of the event
        query.funder-name - query name of the funder
        query.publisher-location - query location of the publisher
        query.publisher-name - query publisher name
        query.standards-body-acronym - query acronym of the standards body
        query.standards-body-name - query standards body name
        query.title - query title
        query.translator - query translator given and family names
        
        
        """
    
        print()