import requests_mock
import unittest.mock as mock
import unittest

import localpackages.imdb_service_request as imdb_service_request

def fileLoader(filename):
    with open(filename, 'r', encoding='unicode_escape') as f:
        return f.read()

class ImdbServiceRequestTest(unittest.TestCase):

    def test_get_amount_titles_should_should_success(self):
        api_endpoint = 'https://www.imdb.com/search/title/' \
          '?title_type=tv_movie&release_date=1980-01-01,1980-12-31' \
          '&view=simple&count=1'

        year = '1980'
        request_response_file = './assets_test/get_amount_titles.txt'

        with requests_mock.Mocker() as rm:
            rm.get(api_endpoint, text=fileLoader(request_response_file), status_code=200)
            amount_titles = imdb_service_request.get_amount_titles(year)

        self.assertEqual(amount_titles, 1514)

    def test_get_offsets_by_page_size_should_success(self):
        amount_title = 1514

        offsets = imdb_service_request.get_offsets_by_page_size(amount_title)
        self.assertEquals(offsets, [1, 251, 501, 751, 1001, 1251, 1501])

    def test_get_offsets_by_page_size_should_success_when_given_multipe(self):
        amount_title = 1000

        offsets = imdb_service_request.get_offsets_by_page_size(amount_title)
        self.assertEquals(offsets, [1, 251, 501, 751])

    def test_get_offsets_by_page_size_should_success_when_given_less_page_size(self):
        amount_title = 3

        offsets = imdb_service_request.get_offsets_by_page_size(amount_title)
        self.assertEquals(offsets, [1])

    def test_get_titles_info_from_html_success(self):
        html_file = './assets_test/get_amount_titles.txt'
        text=fileLoader(html_file)

        title_info = imdb_service_request.get_titles_info_from_html(text)

        self.assertEqual(title_info, '1-1 of 1,514 titles.')

    def test_get_titles_info_from_html_should_raise_exception(self):
        html_file = './assets_test/simple_html.txt'
        text=fileLoader(html_file)

        with self.assertRaises(Exception) as context:
            imdb_service_request.get_titles_info_from_html(text)

        self.assertTrue(
            'The titles info could not be found. Check the selector.' \
                in str(context.exception))

    def test_get_titles_number_from_titles_info_success(self):
        titles_info = '1-1 of 1,514 titles.'
        number_of_titles = \
            imdb_service_request.get_titles_number_from_titles_info(\
                titles_info)
        self.assertEqual(number_of_titles, 1514)


