# Model Response Design

Most (all?) endpoints return JSON. Rather than return JSON directly this code base returns response objects which contain the JSON. These objects have three primary goals.

1. Provide a nice printing of the JSON data from the console
2. Have minimal overhead
3. Allow at least first level subscripting of properties, rather than key lookups, which I find easier to type (e.g. result.reference_count vs result["reference_count"]

## Usage Notes

If you would like to work with the raw json you must do the following:

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
#We can't do data = result.references-count!
data = result['references-count']
```

Currently no guarantee is made regarding the presence of a field in the returned objects. Like a dictionary, the get method is supported
```python

```

## Result Lists

TODO: Describe this ...