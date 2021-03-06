import re
import requests
import config
import secrets


def process_html_passage(passage_html):
    # Remove all double spaces
    passage_html = re.sub(r" +", " ", passage_html)

    # Put all verse numbers in square brackets
    passage_html = re.sub(r"<sup(.*?)>(.*?)</sup>", r"[\2] ", passage_html)

    # Remove section headings
    passage_html = re.sub(r"<h(.)(.*?)>(.*?)</h\1>", "", passage_html)

    # Remove all remaining html tags
    passage_html = re.sub(r"<(.*?)>", "", passage_html)

    # Remove all double spaces again
    passage_html = re.sub(r" +", " ", passage_html)
    return passage_html


def get_bible_text(book, start_chapter, start_verse, end_chapter, end_verse,
                   with_verse_numbers=True):
    payload = {
        "q": "{book}+{start_chapter}:{start_verse}-{end_chapter}:{end_verse}".format(
            book=book, start_chapter=start_chapter, start_verse=start_verse,
            end_chapter=end_chapter, end_verse=end_verse)
    }
    try:
        response = requests.get(config.BIBLE_API_URL, params=payload, auth=(secrets.BIBLE_API_KEY, "X"))
        passage_html = response.json()["response"]["search"]["result"]["passages"][0]["text"]
        processed_passage = process_html_passage(passage_html)
        if not with_verse_numbers:
            # Remove section headings
            processed_passage = re.sub(r"( )*\[(.*?)\]( )*", "", processed_passage)
        return processed_passage
    except requests.exceptions.RequestException as e:
        print(e)
        return None


def remove_square_bracketed_verse_numbers(s):
    s = re.sub(r"( )*\[(.*?)\]( )*", "", s)
    s = re.sub(r"\.\b", ". ", s)
    return s
