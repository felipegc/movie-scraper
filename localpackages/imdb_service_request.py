import requests
import re
from bs4 import BeautifulSoup


PAGE_SIZE = 250 # TODO(felipe) this should go to a file with params


def get_amount_titles(year):
    imdb_url_base = 'https://www.imdb.com/search/title/?' \
      'title_type=tv_movie&' \
      'release_date={}-01-01,{}-12-31&' \
      'view=simple&count=1'

    api_endpoint = imdb_url_base.format(year, year)
    response = requests.get(api_endpoint)
    titles_info = get_titles_info_from_html(response.content)
    titles_number = get_titles_number_from_titles_info(titles_info)

    return titles_number


def get_offsets_by_page_size(amount_titles):
    cur_offset = 1
    offsets = [cur_offset]

    while cur_offset < amount_titles:
        cur_offset += PAGE_SIZE
        if cur_offset < amount_titles:
            offsets.append(cur_offset)

    return offsets


def get_titles_info_from_html(content):
    soup = BeautifulSoup(content, 'html.parser')
    title_selector = '#pagecontent div .nav .desc span:first-child'

    html = list(soup.children)[3] # get only the html
    page_content = html.select(title_selector)
    if len(page_content) == 0:
        raise Exception(
            'The titles info could not be found. Check the selector.')

    return page_content[0].get_text()


def get_titles_number_from_titles_info(titles_info):
    #1-1 of 1,514 titles.
    pattern = re.compile(r'\d-\d of ([\d,]+) titles')
    match = re.search(pattern, titles_info).group(1)
    return int(match.replace(',', ''))




