
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