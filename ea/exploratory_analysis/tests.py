from django.test import TestCase

# Create your tests here.

from .models import Variables
import json
import requests

dataset_name = 'ne30'

class VariableTableTests(TestCase):
    
    def test_was_deleted_ok(self):
        '''
        should return a JSON object 
        { "variables" : "" }
        after being deleted and retrieved
        no matter what
        '''
        
        r = requests.get('http://localhost:8000/exploratory_analysis/dataset_variables/ne30/')
        print r.status_code
        print r.headers['content-type']
        print r.text
        print r.json()
        
        obj = {}
        obj['variables'] = ''
        
        json_obj = json.dumps(obj)#, skipkeys, ensure_ascii, check_circular, allow_nan, cls, indent, separators, encoding, default)
        print str(json_obj)
        a = 1
        b = 1
        self.assertEqual(json_obj,r.json())
        
        