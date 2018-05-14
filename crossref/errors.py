# -*- coding: utf-8 -*-
"""
"""

class CrossrefAPIError(Exception):
    """User errors in usage of the Crossref API"""
    pass

class RequestError(Exception):
    pass

class InvalidDOI(Exception):
    pass

class UnhandledHTTPResonseFailure(Exception):
    pass