import unittest.mock as mock
import unittest

from flask import Flask, request
from unittest.mock import call
from werkzeug.exceptions import HTTPException

import main

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

    @mock.patch('localpackages.imdb_service_request.get_amount_titles', return_value=1000)
    @mock.patch('localpackages.pub_sub_service_request.publish_offset', return_value='Message published.')
    def test_init_scraping_should_publish_offsets(self, mock_publish, \
      mock_get_amount_titles):
        app = Flask(__name__)

        with app.test_request_context(query_string={'year': '1980'}):
            main.init_scraping(request)

        mock_publish.assert_has_calls([call(1), call(251), call(501), call(751)])

