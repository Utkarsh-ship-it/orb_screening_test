import unittest
from src import problem3

class TestFetchCaltransOffices(unittest.TestCase):
    '''
        
        - checking for URL call.
        - Checking table element exist in html page or not.
    '''
    def setUp(self):
         self.ws_obj = problem3.FetchCaltransOffices()

    def tearDown(self):
        pass

    def test_call_url(self):
       
        self.ws_obj.call_url()
        self.assertEqual(self.ws_obj.r.ok, True)

    def test_process_html_page(self):
        self.ws_obj.url = 'https://dot.ca.gov/'
        self.ws_obj.call_url()
        self.assertEqual(self.ws_obj.process_html_page(), False)

if __name__ == '__main__':
    unittest.main()