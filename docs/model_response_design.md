# Model Response Design

Most (all?) endpoints return JSON. Rather than return parsed JSON directly this code base returns response objects which contain the parsed JSON. The design goals for these objects are:

1. Provide nice printing of the JSON data from the console
2. Have minimal overhead
3. Allow at least first level subscripting of properties, rather than key lookups, which I find easier to type (e.g. result.reference_count vs result["reference_count"]

## Usage Notes

If you would like to work with the parsed JSON you can do the following:

```python
#Get the underlying JSON data that was returned
data = result.json
```

Alternatively, the works endpoint supports return_type='json', which returns the raw message. (TODO: The other endpoints should support this as well)

```
>>> result = api.works(return_type='json')
>>> result.keys()
dict_keys(['status', 'message-type', 'message-version', 'message'])
```

Some fields are not safe for object access. This typically occurs with hyphens. In this case dictionary like access must be used.

```python
#Get a field that is not safe to access with dot notation
#We can't do:
#   data = result.references-count!

#Do this instead
data = result['references-count']
```

Currently no guarantee is made regarding the presence of a field in the returned objects. Like a dictionary, the get() method is supported

```python
#Format .get(key_name,default=None)
data = result.get('references-count')

#Specifying a default - 0 - if key is not present
data = result.get('references-count',0)
```

## Result Lists

Searches are designed to return a set of results. The http request returns JSON which contains a list of dictionary elements. This library wraps those results in search result classes. The design goals for these objects are the same as the individual dictionary classes but also:

1. Support paging (NYI)
2. Support returning the individual list elements as classes at the time theyare accessed, rather than when the search result class is created.


The raw  data are exposed in the 'items' property. The class also exposes a 'citems' property which is short for 'class items'. The .citems property can be accessed like a standard list (TODO: are ranges supported?), and returns each element as a class, rather than just a dictionary.

```python
#TODO...
```