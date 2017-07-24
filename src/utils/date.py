from datetime import datetime


def sunday_from(amazon_date):
    # TODO
    # Returns a datetime object for the given Amazon.DATE
    if len(amazon_date) == 10:  # TODO use regex for this
        date = datetime.strptime(amazon_date, '%Y-%m-%d').date()
        return date
    else:
        return None
