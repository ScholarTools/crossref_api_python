# -*- coding: utf-8 -*-
"""
"""

from crossref import api
c = api.API() #c => CrossRef

#m = c.doi_meta('10.1109/TNSRE.2011.2163145')
#m = c.doi_meta('http://dx.doi.org/10.1088/1741-2560/6/5/055009')
#m = c.doi_meta('http://dx.doi.org/10.1642/0004-8038(2002)119[0088:SSCPEO]2.0.CO;2')

q = api.QueryOptions()

q.sample = 100

print(q)

#This apparently is not allowed
m = c.doi_list(options=q)

import pdb
pdb.set_trace()



#temp = api.

#Next, let's sample some dois and get the unique keys 

"""
           ISSN: ['1534-4320', '1558-0210']
          title: ['Limb-State Information Encoded by Peripheral and Central Somatosensory Neurons: Implications for an Afferent Interface']
            URL: http://dx.doi.org/10.1109/tnsre.2011.2163145
       subtitle: []
container-title: None
         prefix: http://id.crossref.org/prefix/10.1109
           type: journal-article
           page: 501-513
        subject: ['Medicine(all)']
          score: 1.0
         member: http://id.crossref.org/member/263
        created: {'date-parts': [[2011, 8, 31]], 'timestamp': 1314805584000, 'date-time': '2011-08-31T15:46:24Z'}
         volume: 19
published_print: None
        indexed: {'date-parts': [[2015, 12, 23]], 'timestamp': 1450846934707, 'date-time': '2015-12-23T05:02:14Z'}
"""

"""
           ISSN: ['1741-2560', '1741-2552']
          title: ['Microstimulation of primary afferent neurons in the L7 dorsal root ganglia using multielectrode arrays in anesthetized cats: thresholds and recruitment properties']
            URL: http://dx.doi.org/10.1088/1741-2560/6/5/055009
       subtitle: []
container-title: None
         prefix: http://id.crossref.org/prefix/10.1088
           type: journal-article
           page: 055009
        subject: ['Cellular and Molecular Neuroscience', 'Biomedical Engineering']
          score: 1.0
         member: http://id.crossref.org/member/266
        created: {'date-parts': [[2009, 9, 2]], 'date-time': '2009-09-02T03:14:49Z', 'timestamp': 1251861289000}
         volume: 6
published_print: None
        indexed: {'date-parts': [[2015, 12, 26]], 'date-time': '2015-12-26T16:13:53Z', 'timestamp': 1451146433719}
"""

"""
           ISSN: ['0004-8038']
          title: ['SEABIRD SUPERTREES: COMBINING PARTIAL ESTIMATES OF PROCELLARIIFORM PHYLOGENY']
            URL: http://dx.doi.org/10.1642/0004-8038(2002)119[0088:sscpeo]2.0.co;2
       subtitle: []
container-title: None
         prefix: http://id.crossref.org/prefix/10.1642
           type: journal-article
           page: 88
        subject: ['Animal Science and Zoology', 'Ecology, Evolution, Behavior and Systematics']
          score: 1.0
         member: http://id.crossref.org/member/1217
        created: {'date-time': '2006-07-12T20:06:57Z', 'timestamp': 1152734817000, 'date-parts': [[2006, 7, 12]]}
         volume: 119
published_print: None
        indexed: {'date-time': '2015-12-20T17:42:10Z', 'timestamp': 1450633330082, 'date-parts': [[2015, 12, 20]]}
"""

import pdb
pdb.set_trace()