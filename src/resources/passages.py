import os
import csv


def get_passage(date, service):
    # Returns a dictionary of the book and start and end chapters and verses
    # for the given service

    with open(os.path.join(os.environ["LAMBDA_TASK_ROOT"], "resources", "data",
                           "passages.csv"), "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['date'] == date.strftime('%Y-%m-%d'):
                if not row['{} book'.format(service)]:
                    return None

                return {
                    'book': row['{} book'.format(service)],
                    'start': {
                        'chapter': row['{} start chapter'.format(service)],
                        'verse': row['{} start verse'.format(service)]
                    },
                    'end': {
                        'chapter': row['{} end chapter'.format(service)],
                        'verse': row['{} end verse'.format(service)]
                    }
                }
        return None


def get_passage_response(date, service):
    # Returns the Alexa response for the passage for the given service
    passage = get_passage(date, service)

    response = "{} chapter {}".format(
        str(passage["book"]),
        str(passage["start"]["chapter"])
    )
    # Start and finish in same chapter?
    if passage["start"]["chapter"] == passage["end"]["chapter"]:
        response += " verses {} to {}".format(
            str(passage["start"]["verse"]),
            str(passage["end"]["verse"])
        )
    else:
        response += " verse {} to chapter {}".format(
            str(passage["start"]["verse"]),
            str(passage["end"]["chapter"]),
            str(passage["end"]["verse"])
        )
    return response
