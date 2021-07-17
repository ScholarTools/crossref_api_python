The following are search options for endpoints.

# Standard Options

These are described at:
https://github.com/CrossRef/rest-api-doc#parameters

All examples should be interpreted in the context of the endpoint. For example the following:

```query='electrical stimulation'```

Could be interpreted as:

```python
temp = api.works(query='electrical stimulation')
```

What is ambiguous from the example is the endpoint (api function). Some options limit the number of endpoints. Relevant functions are:

- api.funders()
- api.journals()
- api.licenses()
- api.members()
- api.works()




## Query

Use the query field to search for results. 
```query='electrical stimulation'```

## Filter

Results from searches can be filtered via the following pattern:

```
filter='from-pub-date:2004-04-04,until-pub-date:2008-08-08'
```

Filter data types:
* boolean: 
 - t,true,1
 - f,false,0
* date yyyy => 2014
 - TODO
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


- https://github.com/CrossRef/rest-api-doc#facet-counts
- [options](works_facet_options.tsv)

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