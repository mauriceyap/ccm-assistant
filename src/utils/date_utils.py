import datetime
import re


def sunday_from(amazon_date):
    # Returns a datetime object for the given Amazon.DATE
    if re.match(r"20\d\d-\d\d-\d\d", amazon_date):
        date = datetime.datetime.strptime(amazon_date, "%Y-%m-%d").date()
        if date.weekday() == 6:
            return date
        else:
            raise RuntimeError("That day isn't a Sunday. What's the date"
                               " of the service you're after? ")
    elif re.match(r"20\d\d-W\d\d-WE", amazon_date):
        # Convert weekend to Sunday
        return datetime.datetime.strptime(
            amazon_date[:-3] + "-0", "%Y-W%W-%w").date()
    elif re.match(r"20\d\d-W\d\d", amazon_date):
        # Convert week to Sunday
        return datetime.datetime.strptime(
            amazon_date + "-0", "%Y-W%W-%w").date()
    else:
        print(amazon_date)
        return None


def is_not_in_future(date):
    return date <= date.today()


def date_from_ccm_xml_text(text):
    return datetime.datetime.strptime(text[:-6], "%a, %d %b %Y %H:%M:%S").date()


def normalise_future_sermon_date(intent):
    # if date is over 30 days in the future, take it back one year
    original_date = datetime.datetime.strptime(intent["slots"]["Date"]["value"],
                                               "%Y-%m-%d").date()
    if (original_date - datetime.date.today()).days > 30:

        new_date = datetime.date(original_date.year - 1, original_date.month,
                                 original_date.day)
        intent["slots"]["Date"]["value"] = new_date
    return intent


def normalise_future_passage_date(intent):
    # if date is over five months in the future, take it back one year
    original_date = datetime.datetime.strptime(intent["slots"]["Date"]["value"],
                                               "%Y-%m-%d").date()
    if (original_date - datetime.date.today()).days > 150:

        new_date = datetime.date(original_date.year - 1, original_date.month,
                                 original_date.day)
        intent["slots"]["Date"]["value"] = new_date
    return intent
