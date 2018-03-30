import requests
from xml.etree import ElementTree
import utils

NAMESPACE = {
    "ccm": "http://www.christchurchmayfair.org/",
    "itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"
}
SERVICE_NAMES = {
    "morning": "AM Service",
    "evening": "6PM Service"
}
DATA_URL = "http://www.christchurchmayfair.org/our-talks/podcast/"


def get_sermon(date, service):
    response = requests.get(DATA_URL)
    tree = ElementTree.fromstring(response.content)

    for item in tree.getchildren()[0].findall("item"):

        if (date == utils.date_from_ccm_xml_text(item.find("pubDate").text) and
                SERVICE_NAMES[service] == item.find("ccm:event",
                                                    NAMESPACE).text):
            return {
                "title": item.find("title").text,
                "passage": item.find("ccm:biblepassage", NAMESPACE).text,
                "series_name": item.find("ccm:seriesname", NAMESPACE).text,
                "speaker": item.find("ccm:author", NAMESPACE).text,
                "image_url": item.find("itunes:image", NAMESPACE).get("href"),
                "audio_url": item.find("link").text
            }
    return None

