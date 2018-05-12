# -*- coding: utf-8 -*-
"""
"""

class CrossrefError(Exception):
    pass

class RequestError(Exception):
    pass

class InvalidDOI(Exception):
    pass

class UnhandledHTTPResonseFailure(Exception):
    pass