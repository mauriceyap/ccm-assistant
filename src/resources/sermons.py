import requests
from xml.etree import ElementTree
import utils
import config


def get_sermon(date, service):
    response = requests.get(config.SERMONS_XML_URL)
    tree = ElementTree.fromstring(response.content)

    for item in tree.getchildren()[0].findall("item"):

        if (date == utils.date_from_ccm_xml_text(item.find("pubDate").text)
                and config.SERMONS_XML_SERVICE_NAMES[service] == item.find(
                    "ccm:event", config.SERMONS_XML_NAMESPACE).text):
            return {
                "title": item.find("title").text,
                "passage": item.find("ccm:biblepassage", config.SERMONS_XML_NAMESPACE).text,
                "series_name": item.find("ccm:seriesname", config.SERMONS_XML_NAMESPACE).text,
                "speaker": item.find("ccm:author", config.SERMONS_XML_NAMESPACE).text,
                "image_url": item.find("itunes:image", config.SERMONS_XML_NAMESPACE).get("href"),
                "audio_url": item.find("link").text
            }
    return None

