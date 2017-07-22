import re
import requests

BIBLE_SEARCH_API_KEY = 'xfrxzZpI8YdyOvTFP2RJkhn0FYQRNnfq3xZgOtrc'
TRANSLATION = 'ESV'  # Can't use NIV - it's still in copyright


def process_html_passage(passage_html):
    # Remove all double spaces
    passage_html = re.sub(r' +', ' ', passage_html)

    # Put all verse numbers in square brackets
    passage_html = re.sub(r'<sup(.*?)>(.*?)</sup>', r'[\2] ', passage_html)

    # Remove section headings
    passage_html = re.sub(r'<h(.)(.*?)>(.*?)</h\1>', '', passage_html)

    # Remove all remaining html tags
    passage_html = re.sub(r'<(.*?)>', '', passage_html)
    return passage_html


def get_bible_text(book, start_chapter, start_verse, end_chapter, end_verse):
    api_call_url = 'https://bibles.org/v2/eng-' + TRANSLATION +\
                   '/passages.js?q[]=' + book + '+' + start_chapter + ':' \
                   + start_verse + '-' + end_chapter + ':' + end_verse
    print(api_call_url)
    response = requests.get(api_call_url, auth=(BIBLE_SEARCH_API_KEY, 'X '))
    passage_html = \
        response.json()['response']['search']['result']['passages'][0]['text']
    return process_html_passage(passage_html)
