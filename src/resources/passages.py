import yaml


def get_passage(date, service):
    # Returns a dictionary of the book and start and end chapters and verses
    # for the given service
    with open("data/passages.yaml", "r") as f:
        passage = yaml.load(f)[date][service]
        f.close()
        return passage


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
