# Introduction 

The following are components of works() endpoints that may or may not be present in the returned documents. More specifically, works with (or without) the requested fields can be requested using the appropriate filter parameter.

This list has been compiled from looking at the filter parameters for values that start with "has"

# Standard Options

These are described at:
https://github.com/CrossRef/rest-api-doc#parameters

## Query

Use the query field to search for results. 
```query='electrical stimulation'```

## Filter

Results from searches can be filtered via the following pattern:

# Standard Options

These are described at:
https://github.com/CrossRef/rest-api-doc#parameters

## Query

Use the query field to search for results. 
```query='electrical stimulation'```

## Filter

Results from searches can be filtered via the following pattern:

```
filter='from-pub-date:2004-04-04,until-pub-date:2008-08-08'
```

Filter data types:
* date yyyy => 2014
 - yyyy => 2014
 - yyyy

Filters for endpoints are:
- (Funders)[# funders-filters]
- (Works)[# works-filters]

## Rows

## Offset

## Sample

## Sort

## Order

## Facet

## Cursor
- https://github.com/CrossRef/rest-api-doc#deep-paging-with-cursors

# Funders Filters
- [options](funders_filters.tsv)

# Works Filters
- Source: https://github.com/CrossRef/rest-api-doc#filter-names
- [options](works_filters.tsv)
- boolean: {t,true,1,f,false,0}
- date: 

# Works Field Queries
- Source: https://github.com/CrossRef/rest-api-doc#works-field-queries
- [options](/works_field_queries.tsv)
```
filter='from-pub-date:2004-04-04,until-pub-date:2008-08-08'
```

Filter data types:
* date yyyy => 2014
 - yyyy => 2014
 - yyyy

Filters for endpoints are:
- (Funders)[# funders-filters]
- (Works)[# works-filters]

## Rows

## Offset

## Sample

## Sort

## Order

## Facet

## Cursor
- https://github.com/CrossRef/rest-api-doc#deep-paging-with-cursors

# Funders Filters
- [options](funders_filters.tsv)

# Works Filters
- Source: https://github.com/CrossRef/rest-api-doc#filter-names
- [options](works_filters.tsv)
- boolean: {t,true,1,f,false,0}
- date: 

# Works Field Queries
- Source: https://github.com/CrossRef/rest-api-doc#works-field-queries
- [options](/works_field_queries.tsv)
# Standard Options

These are described at:
https://github.com/CrossRef/rest-api-doc#parameters

## Query

Use the query field to search for results. 
```query='electrical stimulation'```

## Filter

Results from searches can be filtered via the following pattern:

```
filter='from-pub-date:2004-04-04,until-pub-date:2008-08-08'
```

Filter data types:
* date yyyy => 2014
 - yyyy => 2014
 - yyyy

Filters for endpoints are:
- (Funders)[# funders-filters]
- (Works)[# works-filters]

## Rows

## Offset

## Sample

## Sort

## Order

## Facet

## Cursor
- https://github.com/CrossRef/rest-api-doc#deep-paging-with-cursors

# Funders Filters
- [options](funders_filters.tsv)

# Works Filters
- Source: https://github.com/CrossRef/rest-api-doc#filter-names
- [options](works_filters.tsv)
- boolean: {t,true,1,f,false,0}
- date: 

# Works Field Queries
- Source: https://github.com/CrossRef/rest-api-doc#works-field-queries
- [options](/works_field_queries.tsv)
These options expect a boolean which can be either: 0,1,t,f,true,false

More on filtering can be found at:
TODO

# Abstract

- filter: 'has-abstract'
- property: 'abstract'

```python
>>> temp = api.works(filter='has-abstract:t')
	
>>> temp.citems[0].abstract

#TODO

```

# Affiliation

- filter: has-affiliation
- property: ...

```python
>>> temp = api.works(filter='has-affiliation:t')
	
>>> temp.citems[0].abstract

TODO

```

# Archive

- filter:has-archive

# Assertion

- filter:has-assertion

# Authenticated ORCID

- filter:has-authenticated-orcid

# Clinical Trial Number

- filter:has-clinical-trial-number

# Content Domain

- filter:has-content-domain

# Domain Restriction

- filter:has-domain-restriction

# Full Text

- filter:has-full-text

# Funder

- filter:has-funder

# License

- filter:has-license

# ORCID 

- filter:has-orcid

# References

- filter:has-references

# Relation

- filter:has-relation : bool
- filter:relation.type : TODO: Link to the current table 
- filter:relation.object : object identifier matches the identifier provided
- filter:relation.object-type


?? TODO: What is is-part-of???	
```python
>>> temp = api.works(filter='relation.type:is-part-of')
	
>>> temp.citems[0].relation
 
{'cites': [],
 'is-part-of': [{'asserted-by': 'subject',
   'id': '\n                                    10.5285/08fbe63d-fa6d-4a7a-b952-5932e3ab0452\n                                ',
   'id-type': 'doi'}]}
   
```

```python	
>>> temp = api.works(filter='relation.type:is-preprint-of',select='DOI,type,relation')
>>> temp.items[6]
{'DOI': '10.20944/preprints201712.0177.v1',
 'relation': {'is-preprint-of': [{'asserted-by': 'subject',
    'id': '10.3390/fib6010007',
    'id-type': 'doi'}]},
 'type': 'posted-content'}
```


## Update Policy

- filter:has-update-policy