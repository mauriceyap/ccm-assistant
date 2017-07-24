import yaml


def get_passage(date, service):
    # Returns a dictionary of the book and start and end chapters and verses
    # for the given service
    with open('data/passages.yaml', 'r') as f:
        passage = yaml.load(f)[date][service]
        f.close()
        return passage


def get_passage_response(date, service):
    # Returns the Alexa response for the passage for the given service
    passage = get_passage(date, service)

    response = str(passage['book']) + ' chapter ' + \
               str(passage['start']['chapter'])
    # Case - start and finish in same chapter
    if passage['start']['chapter'] == passage['end']['chapter']:
        response += ' verses ' + str(passage['start']['verse']) + ' to ' + \
                   str(passage['end']['verse'])
    else:
        response += ' verse ' + str(passage['start']['verse']) + \
                    ' to chapter ' + str(passage['end']['chapter']) + \
                    ' verse ' + str(passage['end']['verse'])
    return response
