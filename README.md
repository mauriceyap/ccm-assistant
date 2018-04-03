# Christ Church Mayfair Assistant

![](https://travis-ci.org/travis-ci/travis-web.svg?branch=master)

AWS Lambda function for Christ Church Mayfair Assistant Alexa skill.

## Features:
- Gets the Bible passage reading for each service
  
  *Alexa, get me the reading for the morning service this Sunday from CCM?*
  
  ***Matthew chapter 17, verses 21 to 28 - would you like me to read it?***
  
- Plays recordings of past sermons

  *Alexa, ask CCM to play me the sermon at two weeks ago in the evening*
  
  ***Okay. [The sermon recording]***
  
- Tells you when the next event is

  *Alexa, when's the next event from CCM?*
  
  ***Prayer meeting tomorrow evening at 6***
  
## Contributing
### Adding bible passage readings for future sermons
Add rows to `src/resources/data/passages.csv`

### Running and testing locally:
- Install dependencies by running `pip install -r src/requirements.txt`
- Add these environment variables:
  - `LAMBDA_TASK_ROOT` - the file path of the `src/` directory
- Make the file, `src/secrets.py`, containing API keys and the like. Rename the file
  `src/secrets.py.template` and either get your own keys or email mauriceyap@hotmail.co.uk
