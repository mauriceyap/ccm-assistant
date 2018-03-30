import boto3
#import os


dynamodb = boto3.resource('dynamodb', region_name='eu-west-1',
                          endpoint_url=("https://dynamodb.eu-west-1."
                                        "amazonaws.com")#,
                          #aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
                          #aws_secret_access_key=os.environ['AWS_SECRET_KEY']
                          )
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
