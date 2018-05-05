# -*- coding: utf-8 -*-
"""
"""

class RequestError(Exception):
    pass

class InvalidDOI(Exception):
    pass

class UnhandledHTTPResonseFailure(Exception):
    pass