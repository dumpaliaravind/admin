# -*- coding: utf-8 -*-
import json

def readable_json(jsonData):
    '''
    INPUT   1. jsonData (json) - JSON value to be formatted.
    OUTPUT  1. (json) - Formatted JSON data.
    '''
    return json.dumps(jsonData, indent=4, sort_keys=True)