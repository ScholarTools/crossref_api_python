#!/usr/bin/python
from collections import Counter

# Read in dois.txt and separate by commas
f = open('../dois.txt', 'r')
dois = f.read().split(',')

# Remove all "" elements
dois = list(set(dois) - set(""))

prefixes = []
names = []

for x in range(0,len(dois)):
    if dois[x][2:5] != '10.':
        continue
    prefixes.append(dois[x][2:9])
    names.append(dois[x][2:-1])

# Count and return each unique prefix with the number of times it occurs
p = Counter(prefixes)
top = p.most_common(len(p))

print top

print len(p)

# Create list of DOIs with each unique prefix represented once, in decreasing order of occurrence
examples = []
for x in range(0,len(p)):
    pre = top[x][0]
    for y in range(0,len(prefixes)):
        if pre == prefixes[y]:
            examples.append(names[y])
            break

print len(examples)
print examples
print len(prefixes)

'''
TODO:
    - Set up git and push this into one of the existing ScholarTools repositories
    - Use mendeley_python and/or crossref_api_python to resolve each DOI in examples[] to a provider
    - After resolving to providers, sum up the multiple instances of each provider to get the four most popular
        - e.g. multiple prefixes could link to the same provider, so be sure to incorporate the frequencies linked to
        each prefix in top[], not just the direct number of prefixes per provider
'''
