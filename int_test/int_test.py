import unittest

from app import app


class IntegrationTest(unittest.TestCase):
    def test_function(self):
        tester = app.test_client(self)
        print(tester.environ_base)
        response = tester.get('/auth/hello', content_type='html/text')
        self.assertEqual(response.status_code, 200)
