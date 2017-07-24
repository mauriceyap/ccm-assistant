from datetime import datetime


def sunday_from(amazon_date):
    # TODO
    # Handle specific date
    if len(amazon_date) == 10:  # TODO use regex for this
        date = datetime.strptime(amazon_date, '%Y-%m-%d')
        return date
    else:
        return None
