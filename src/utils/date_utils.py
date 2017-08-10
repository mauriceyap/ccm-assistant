from datetime import datetime
import re


def sunday_from(amazon_date):
    # Returns a datetime object for the given Amazon.DATE
    if re.match(r'20\d\d-\d\d-\d\d', amazon_date):
        date = datetime.strptime(amazon_date, '%Y-%m-%d').date()
        if date.weekday() == 6:
            return date
        else:

            raise RuntimeError("That day isn't a Sunday. What's the date"
                               " of the service you're after? ")
    elif re.match(r"20\d\d-W\d\d-WE", amazon_date):
        # Convert weekend to Sunday
        return datetime.strptime(amazon_date[:-3] + "-0", "%Y-W%W-%w").date()
    elif re.match(r"20\d\d-W\d\d", amazon_date):
        # Convert week to Sunday
        return datetime.strptime(amazon_date + "-0", "%Y-W%W-%w").date()
    else:
        print(amazon_date)
        return None
