# -*- coding: utf-8 -*-
"""
"""

from crossref import api
c = api.API()
m = c.doi_meta('10.1109/TNSRE.2011.2163145')

import pdb
pdb.set_trace()