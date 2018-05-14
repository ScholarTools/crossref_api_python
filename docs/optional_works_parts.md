# Introduction 

The following are components of works() endpoints that may or may not be present in the returned documents. More specifically, works with (or without) the requested fields can be requested using the appropriate filter parameter.

# Abstract

- filter: has-abstract

# Affiliation

- filter: has-affiliation

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