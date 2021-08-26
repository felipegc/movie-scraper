import unittest.mock as mock
import unittest
import main

from flask import Flask, request
from werkzeug.exceptions import HTTPException

class MainInitScrapingTest(unittest.TestCase):
    def test_init_scraping_should_fail_without_param(self):
        app = Flask(__name__)

        with app.test_request_context(query_string={}):
            try:
                main.init_scraping(request)
            except HTTPException as e:
                self.assertEqual(e.code, 400)
                self.assertEqual(e.description, \
                    'Make sure to specify the param: year')

    def test_init_scraping_should_fail_without_year_param(self):
        app = Flask(__name__)

        with app.test_request_context(query_string={'not_year': 'test'}):
            try:
                main.init_scraping(request)
            except HTTPException as e:
                self.assertEqual(e.code, 400)
                self.assertEqual(e.description, \
                    'Year is a mandatory param')

    @mock.patch('localpackages.imdb_service_request.get_amount_titles', return_value=3000)
    @mock.patch('localpackages.pub_sub_utils.publish', return_value='Felipe')
    def test_init_scraping(self, mock_1, mock_2):
        app = Flask(__name__)

        with app.test_request_context(query_string={'year': '1980'}):
            res = main.init_scraping(request)

        self.assertEqual(res, 'The jobs to process the pages were submitted')

