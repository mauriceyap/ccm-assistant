import boto3


dynamodb = boto3.resource('dynamodb', region_name='eu-west-1',
                          endpoint_url=("https://dynamodb.eu-west-1."
                                        "amazonaws.com"))
table = dynamodb.Table('alexa-ChristChurchMayfairAssistant-playback')


def store_audio_url_for_user(user_id, audio_url):
    table.put_item(
        Item={
            'user_id': user_id,
            'audio_url': audio_url
        }
    )


def store_offset_for_user(user_id, offset):
    table.update_item(
        Key={
            'user_id': user_id
        },
        UpdateExpression="set offset=:o",
        ExpressionAttributeValues={
            ':o': offset
        }
    )


def get_data_for_user(user_id):
    response = table.get_item(
        Key={
            'user_id': user_id
        }
    )
    return response['Item']


def reset_user(user_id):
    table.delete_item(
        Key={
            'user_id': user_id
        }
    )
