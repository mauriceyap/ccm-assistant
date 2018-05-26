import json
import config
import handlers.events as events


def lambda_handler(event, context):
    # Log input event to CloudWatch
    print("EVENT OBJECT:\n{event_json}".format(event_json=json.dumps(event)))

    # Make sure only this Alexa skill can use this function
    application_id = (
        event["session"]["application"]["applicationId"]
        if "session" in event.keys()
        else event["context"]["System"]["application"]["applicationId"]
    )
    if application_id != config.APPLICATION_ID:
        raise ValueError("Invalid Application ID")

    if event["session"] and event["session"]["new"]:
        events.on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    request_type = event["request"]["type"]

    if request_type == "LaunchRequest":
        return events.on_launch()
    elif request_type == "IntentRequest":
        return events.on_intent(event["request"], event["session"], event["context"])
    elif request_type == "SessionEndedRequest":
        return events.on_session_ended(event["request"], event["session"])

# TEST ### DO NOT COMMIT ###


passage_event = {
    'session': {
        'application': {
            'applicationId': 'amzn1.ask.skill.dd677950-cade-4805-b1f1-ce2e3a3569f0'
        },
        'new': False
    },
    'request': {
        'type': 'IntentRequest',
        'name': 'GetSermonPassage',
        "intent": {
            "slots": {
                "Date": {
                    "name": "Date",
                    "value": "2018-02-18",
                    "confirmationStatus": "NONE"
                },
                "Service": {
                    "resolutions": {
                        "resolutionsPerAuthority": [
                            {
                                "status": {
                                    "code": "ER_SUCCESS_MATCH"
                                },
                                "values": [
                                    {
                                        "value": {
                                            "name": "Evening",
                                            "id": "EVENING"
                                        }
                                    }
                                ],
                                "authority": "amzn1.er-authority.echo-sdk.amzn1.ask.skill.dd677950-cade-4805-b1f1-ce2e3a3569f0.SERVICE"
                            }
                        ]
                    },
                    "name": "Service",
                    "value": "evening",
                    "confirmationStatus": "NONE"
                },
                "ReadPassage": {
                    "name": "ReadPassage",
                    "confirmationStatus": "NONE"
                }
            },
            "name": "GetSermonPassage",
            "confirmationStatus": "NONE"
        }
    },
    "context": {
        "AudioPlayer": {
            "token": "MAGIC_STRING_TOKEN",
            "playerActivity": "STOPPED",
            "offsetInMilliseconds": 268680
        },
        "System": {
            "device": {
                "deviceId": "amzn1.ask.device.AEC7PGJEI5V7YHS4PFVNHOAJT3ID3O2SMGLWWKASN737OE6QZG3F3HRLKFCGB3637E3SZBQSRGL2SML7YTM6D7U2TSUYCN5V2Z45L675ZLJV6OQMBHXHD2O7Y37UCWI5AK2ZDCKUUQEUSLDZPOW2SHLFV55Q",
                "supportedInterfaces": {
                    "AudioPlayer": {}
                }
            },
            "application": {
                "applicationId": "amzn1.ask.skill.dd677950-cade-4805-b1f1-ce2e3a3569f0"
            },
            "apiAccessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ.eyJhdWQiOiJodHRwczovL2FwaS5hbWF6b25hbGV4YS5jb20iLCJpc3MiOiJBbGV4YVNraWxsS2l0Iiwic3ViIjoiYW16bjEuYXNrLnNraWxsLmRkNjc3OTUwLWNhZGUtNDgwNS1iMWYxLWNlMmUzYTM1NjlmMCIsImV4cCI6MTUyMjUzNjcxMCwiaWF0IjoxNTIyNTMzMTEwLCJuYmYiOjE1MjI1MzMxMTAsInByaXZhdGVDbGFpbXMiOnsiY29uc2VudFRva2VuIjpudWxsLCJkZXZpY2VJZCI6ImFtem4xLmFzay5kZXZpY2UuQUVDN1BHSkVJNVY3WUhTNFBGVk5IT0FKVDNJRDNPMlNNR0xXV0tBU043MzdPRTZRWkczRjNIUkxLRkNHQjM2MzdFM1NaQlFTUkdMMlNNTDdZVE02RDdVMlRTVVlDTjVWMlo0NUw2NzVaTEpWNk9RTUJIWEhEMk83WTM3VUNXSTVBSzJaRENLVVVRRVVTTERaUE9XMlNITEZWNTVRIiwidXNlcklkIjoiYW16bjEuYXNrLmFjY291bnQuQUZTQk1HN1RVV0pVT0haWEdaWFZUSEZYNUhYT1NPQ1hDNExINTRONkFVRDVBSERWWjZWVE5WN0xBTzVESEU0SlBOMjNMRlJRRFVNQ0hITFJZSzZUNkk3Mlc2NjVKVVA2M0VaWkJHV0tHNzY3NE1NNklTRFBFQ0NTQVk2R0NKVTNNNlRDVlFLRUgzM0lFTFJaRExXRE5XMzdJRjJHWlUyTUpXUlE3UExEQU9URzdRTE5DRlFNUVVOUlREU0xLU0xRTElRUUxFWDdKSVdCU1pJIn19.FWCtCinlXVF4i4xwbIrmaBfzVq2jPx-0BtEgDyT1H-BSv9_-I_LV2P-Hat0Ibi25O3rYeav1S6iQevWxIG_M-nL2HKDd2Tt581S6gUBVzYxqU7HBWWmRG19njTPzkbU7LS_gDkV6IPyH5wLm3bTimqDh2DA7l--TcxbZ0wmI-nVMSpt6hxfBYC0HTN1vLIh_ZlC9vuGaCIlIli5bw-ytqdQCDm3LMavq_e5sj-OIZ1j8hKdSB3zVW_zhHRJvTgUnBb2tVcjVGFHHH-eiFdnzrlfwpG5sKk_Fk6DYhGhBkFlk-UEvRsktEH-fceQe1bPc1vjDU_Z-rwNN7HR7jCjA7Q",
            "user": {
                "userId": "amzn1.ask.account.AFSBMG7TUWJUOHZXGZXVTHFX5HXOSOCXC4LH54N6AUD5AHDVZ6VTNV7LAO5DHE4JPN23LFRQDUMCHHLRYK6T6I72W665JUP63EZZBGWKG7674MM6ISDPECCSAY6GCJU3M6TCVQKEH33IELRZDLWDNW37IF2GZU2MJWRQ7PLDAOTG7QLNCFQMQUNRTDSLKSLQLIQQLEX7JIWBSZI"
            },
            "apiEndpoint": "https://api.eu.amazonalexa.com"
        }
    }
}

print(lambda_handler(passage_event, None))

sermon_event = {
    "session": {
        "new": False,
        "sessionId": "amzn1.echo-api.session.d443b4d8-75ff-464f-8ab1-34a9a87d0029",
        "user": {
            "userId": "amzn1.ask.account.AFSBMG7TUWJUOHZXGZXVTHFX5HXOSOCXC4LH54N6AUD5AHDVZ6VTNV7LAO5DHE4JPN23LFRQDUMCHHLRYK6T6I72W665JUP63EZZBGWKG7674MM6ISDPECCSAY6GCJU3M6TCVQKEH33IELRZDLWDNW37IF2GZU2MJWRQ7PLDAOTG7QLNCFQMQUNRTDSLKSLQLIQQLEX7JIWBSZI"
        },
        "application": {
            "applicationId": "amzn1.ask.skill.dd677950-cade-4805-b1f1-ce2e3a3569f0"
        }
    },
    "version": "1.0",
    "request": {
        "locale": "en-GB",
        "timestamp": "2018-03-31T22:41:00Z",
        "dialogState": "IN_PROGRESS",
        "intent": {
            "slots": {
                "Date": {
                    "name": "Date",
                    "value": "2018-02-11",
                    "confirmationStatus": "NONE"
                },
                "Service": {
                    "resolutions": {
                        "resolutionsPerAuthority": [
                            {
                                "status": {
                                    "code": "ER_SUCCESS_MATCH"
                                },
                                "values": [
                                    {
                                        "value": {
                                            "name": "Evening",
                                            "id": "EVENING"
                                        }
                                    }
                                ],
                                "authority": "amzn1.er-authority.echo-sdk.amzn1.ask.skill.dd677950-cade-4805-b1f1-ce2e3a3569f0.SERVICE"
                            }
                        ]
                    },
                    "name": "Service",
                    "value": "evening",
                    "confirmationStatus": "NONE"
                }
            },
            "name": "PlaySermon",
            "confirmationStatus": "NONE"
        },
        "requestId": "amzn1.echo-api.request.5c739460-7e20-44a3-af6b-c69158d92e58",
        "type": "IntentRequest"
    },
    "context": {
        "AudioPlayer": {
            "token": "https://0elu033c2a.execute-api.eu-west-1.amazonaws.com/prod/m3uGenerator?url=http://www.christchurchmayfair.org/wp-content/uploads/talks/630/2018/March/2018_03_25_6PM_Psalm_22_Phil_Allcock.mp3",
            "playerActivity": "STOPPED",
            "offsetInMilliseconds": 5064
        },
        "System": {
            "device": {
                "deviceId": "amzn1.ask.device.AEC7PGJEI5V7YHS4PFVNHOAJT3ID3O2SMGLWWKASN737OE6QZG3F3HRLKFCGB3637E3SZBQSRGL2SML7YTM6D7U2TSUYCN5V2Z45L675ZLJV6OQMBHXHD2O7Y37UCWI5AK2ZDCKUUQEUSLDZPOW2SHLFV55Q",
                "supportedInterfaces": {
                    "AudioPlayer": {}
                }
            },
            "application": {
                "applicationId": "amzn1.ask.skill.dd677950-cade-4805-b1f1-ce2e3a3569f0"
            },
            "apiAccessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ.eyJhdWQiOiJodHRwczovL2FwaS5hbWF6b25hbGV4YS5jb20iLCJpc3MiOiJBbGV4YVNraWxsS2l0Iiwic3ViIjoiYW16bjEuYXNrLnNraWxsLmRkNjc3OTUwLWNhZGUtNDgwNS1iMWYxLWNlMmUzYTM1NjlmMCIsImV4cCI6MTUyMjUzOTY2MCwiaWF0IjoxNTIyNTM2MDYwLCJuYmYiOjE1MjI1MzYwNjAsInByaXZhdGVDbGFpbXMiOnsiY29uc2VudFRva2VuIjpudWxsLCJkZXZpY2VJZCI6ImFtem4xLmFzay5kZXZpY2UuQUVDN1BHSkVJNVY3WUhTNFBGVk5IT0FKVDNJRDNPMlNNR0xXV0tBU043MzdPRTZRWkczRjNIUkxLRkNHQjM2MzdFM1NaQlFTUkdMMlNNTDdZVE02RDdVMlRTVVlDTjVWMlo0NUw2NzVaTEpWNk9RTUJIWEhEMk83WTM3VUNXSTVBSzJaRENLVVVRRVVTTERaUE9XMlNITEZWNTVRIiwidXNlcklkIjoiYW16bjEuYXNrLmFjY291bnQuQUZTQk1HN1RVV0pVT0haWEdaWFZUSEZYNUhYT1NPQ1hDNExINTRONkFVRDVBSERWWjZWVE5WN0xBTzVESEU0SlBOMjNMRlJRRFVNQ0hITFJZSzZUNkk3Mlc2NjVKVVA2M0VaWkJHV0tHNzY3NE1NNklTRFBFQ0NTQVk2R0NKVTNNNlRDVlFLRUgzM0lFTFJaRExXRE5XMzdJRjJHWlUyTUpXUlE3UExEQU9URzdRTE5DRlFNUVVOUlREU0xLU0xRTElRUUxFWDdKSVdCU1pJIn19.TVCQiE5x5w8tnOkaIo8SZ8BJQkhE6dpu_OD6aH33hEdoky1tJYoV1TIVjNrLiJqf6xOE0INbtnvy-H4QX4ZgmxFIrlJ27FozshA-LtucGIGaSfSwK54Dp8xFf25HoXhzHdUR9nln9TGagVKCom7ePWUocFh2j3oZFlmof9HonZlArWRYoKMaYbM_LF-5Xacfot9PsuSxAFMYx04w9-OuiETQWnKVTW4eBxib8VX2HLRj42TwxxkvIeo5yB2exi7Nh5WheUTiGfKpnuc-aM6CS6xi4GiD_Gg3-qyuzxGOHzSt2QWy8mGxqzhw3YD8cdyZUEF91sK8aP-nzG8IqyLcVA",
            "user": {
                "userId": "amzn1.ask.account.AFSBMG7TUWJUOHZXGZXVTHFX5HXOSOCXC4LH54N6AUD5AHDVZ6VTNV7LAO5DHE4JPN23LFRQDUMCHHLRYK6T6I72W665JUP63EZZBGWKG7674MM6ISDPECCSAY6GCJU3M6TCVQKEH33IELRZDLWDNW37IF2GZU2MJWRQ7PLDAOTG7QLNCFQMQUNRTDSLKSLQLIQQLEX7JIWBSZI"
            },
            "apiEndpoint": "https://api.eu.amazonalexa.com"
        }
    }
}

print(lambda_handler(sermon_event, None))

another_sermon_event = {
    "session": {
        "new": False,
        "sessionId": "amzn1.echo-api.session.55c32e19-ddf7-469b-a7cc-528f850869b6",
        "user": {
            "userId": "amzn1.ask.account.AFSBMG7TUWJUOHZXGZXVTHFX5HXOSOCXC4LH54N6AUD5AHDVZ6VTNV7LAO5DHE4JPN23LFRQDUMCHHLRYK6T6I72W665JUP63EZZBGWKG7674MM6ISDPECCSAY6GCJU3M6TCVQKEH33IELRZDLWDNW37IF2GZU2MJWRQ7PLDAOTG7QLNCFQMQUNRTDSLKSLQLIQQLEX7JIWBSZI"
        },
        "application": {
            "applicationId": "amzn1.ask.skill.dd677950-cade-4805-b1f1-ce2e3a3569f0"
        }
    },
    "version": "1.0",
    "request": {
        "locale": "en-GB",
        "timestamp": "2018-04-02T00:27:13Z",
        "dialogState": "IN_PROGRESS",
        "intent": {
            "slots": {
                "Date": {
                    "name": "Date",
                    "value": "2019-03-18",
                    "confirmationStatus": "NONE"
                },
                "Service": {
                    "resolutions": {
                        "resolutionsPerAuthority": [
                            {
                                "status": {
                                    "code": "ER_SUCCESS_MATCH"
                                },
                                "values": [
                                    {
                                        "value": {
                                            "name": "Evening",
                                            "id": "EVENING"
                                        }
                                    }
                                ],
                                "authority": "amzn1.er-authority.echo-sdk.amzn1.ask.skill.dd677950-cade-4805-b1f1-ce2e3a3569f0.SERVICE"
                            }
                        ]
                    },
                    "name": "Service",
                    "value": "evening",
                    "confirmationStatus": "NONE"
                }
            },
            "name": "PlaySermon",
            "confirmationStatus": "NONE"
        },
        "requestId": "amzn1.echo-api.request.7592bc82-05be-4446-bdf6-2906d5418a1c",
        "type": "IntentRequest"
    },
    "context": {
        "AudioPlayer": {
            "token": "https://0elu033c2a.execute-api.eu-west-1.amazonaws.com/prod/m3uGenerator?url=http://www.christchurchmayfair.org/wp-content/uploads/talks/630/2017/May/2017_05_28_6PM_Amos_5_Matt_Fuller.mp3",
            "playerActivity": "STOPPED",
            "offsetInMilliseconds": 133800
        },
        "System": {
            "device": {
                "deviceId": "amzn1.ask.device.AEC7PGJEI5V7YHS4PFVNHOAJT3ID3O2SMGLWWKASN737OE6QZG3F3HRLKFCGB3637E3SZBQSRGL2SML7YTM6D7U2TSUYCN5V2Z45L675ZLJV6OQMBHXHD2O7Y37UCWI5AK2ZDCKUUQEUSLDZPOW2SHLFV55Q",
                "supportedInterfaces": {
                    "AudioPlayer": {}
                }
            },
            "application": {
                "applicationId": "amzn1.ask.skill.dd677950-cade-4805-b1f1-ce2e3a3569f0"
            },
            "apiAccessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ.eyJhdWQiOiJodHRwczovL2FwaS5hbWF6b25hbGV4YS5jb20iLCJpc3MiOiJBbGV4YVNraWxsS2l0Iiwic3ViIjoiYW16bjEuYXNrLnNraWxsLmRkNjc3OTUwLWNhZGUtNDgwNS1iMWYxLWNlMmUzYTM1NjlmMCIsImV4cCI6MTUyMjYzMjQzMywiaWF0IjoxNTIyNjI4ODMzLCJuYmYiOjE1MjI2Mjg4MzMsInByaXZhdGVDbGFpbXMiOnsiY29uc2VudFRva2VuIjpudWxsLCJkZXZpY2VJZCI6ImFtem4xLmFzay5kZXZpY2UuQUVDN1BHSkVJNVY3WUhTNFBGVk5IT0FKVDNJRDNPMlNNR0xXV0tBU043MzdPRTZRWkczRjNIUkxLRkNHQjM2MzdFM1NaQlFTUkdMMlNNTDdZVE02RDdVMlRTVVlDTjVWMlo0NUw2NzVaTEpWNk9RTUJIWEhEMk83WTM3VUNXSTVBSzJaRENLVVVRRVVTTERaUE9XMlNITEZWNTVRIiwidXNlcklkIjoiYW16bjEuYXNrLmFjY291bnQuQUZTQk1HN1RVV0pVT0haWEdaWFZUSEZYNUhYT1NPQ1hDNExINTRONkFVRDVBSERWWjZWVE5WN0xBTzVESEU0SlBOMjNMRlJRRFVNQ0hITFJZSzZUNkk3Mlc2NjVKVVA2M0VaWkJHV0tHNzY3NE1NNklTRFBFQ0NTQVk2R0NKVTNNNlRDVlFLRUgzM0lFTFJaRExXRE5XMzdJRjJHWlUyTUpXUlE3UExEQU9URzdRTE5DRlFNUVVOUlREU0xLU0xRTElRUUxFWDdKSVdCU1pJIn19.E8SeH0FkNxXHKqRDO_P5cbdr54AjfyAE-sV55v6WRJ6RUaMDDibwqJUzFKPq3p5ek5xto7TKQ3Q1c_EB0Y4xnxjMLlN1eQrW02vnUQcYP0vXyz1HIvQosoRhVqsCuwEP7Hl3tksYtyDg4L9Jd16YAqka_5birLllTADtG0cuHDwFKQ8DraphzZcx7H-HVRboGqAwj5Fmy6WVgxWwvb-HwrrhXNQZ7nOr0H9Mh45xutW_sj9YCYKmsa_tg0c_fqhwl7HQxtpGqSmADEadawisWD5reTRUa8VG1B1t2szuUHaPvekNSFWhNtl1xo_kwmyCbqtlbbEZmr9J-Qv84LUGVw",
            "user": {
                "userId": "amzn1.ask.account.AFSBMG7TUWJUOHZXGZXVTHFX5HXOSOCXC4LH54N6AUD5AHDVZ6VTNV7LAO5DHE4JPN23LFRQDUMCHHLRYK6T6I72W665JUP63EZZBGWKG7674MM6ISDPECCSAY6GCJU3M6TCVQKEH33IELRZDLWDNW37IF2GZU2MJWRQ7PLDAOTG7QLNCFQMQUNRTDSLKSLQLIQQLEX7JIWBSZI"
            },
            "apiEndpoint": "https://api.eu.amazonalexa.com"
        }
    }
}

print(lambda_handler(another_sermon_event, None))
