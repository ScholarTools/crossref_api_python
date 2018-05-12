#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

#from crossref.filters import works_examples as we

import crossref

api = crossref.API()

temp = api.works(filter='has-funder:t')

