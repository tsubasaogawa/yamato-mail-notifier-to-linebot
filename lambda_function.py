import json
import os
from gmail import Gmail
from yamato import Yamato
# https://github.com/tsubasaogawa/linebot-publisher-layer
from linebot_publisher import LineBotPublisher


# Limit to fetch mails
MAX_RESULTS = 10


def generate_parcel_message(result):
    """
    Generate the output message.

    Parameters
    ----------
    result : dict
        parcel information

    Returns
    -------
    message : string
        output message
    """
    message = ''
    if result['name']:
        message = '{0}だよ'.format(result['name'])

    if result['date']:
        message = message + '\n日時: 　{0}'.format(result['date'])

    if result['parcel']:
        message = message + '\n発送元: {0}'.format(result['parcel'])

    return message


def lambda_handler(event={}, context={}):
    """
    Lambda handler.

    Parameters
    ----------
    event : dict
    context : dict

    Returns
    -------
    response : dict
        Return code and response body.
    """
    gmail = Gmail()
    yamato = Yamato()
    publisher = LineBotPublisher()
    newer_than = os.environ['NEWER_THAN']

    # Get message bodies
    messages = gmail.get_messages(
        maxResults=MAX_RESULTS,
        query=yamato.SEARCH_QUERY,
        newerThan=newer_than,
    )
    if not messages:
        return {
            'statusCode': 200,
            'body': json.dumps(
                'Not found yamato email in {0}'.format(newer_than)
            ),
        }

    # Extract parcel and date from message body
    for message in messages:
        parcel_info = yamato.get_parcel_and_date(message=message)
        if not parcel_info['parcel'] and not parcel_info['date']:
            print('Cannot obtain from messages!: {0}'.format(message))
            continue

        # Post to line
        publisher.post_text(
            os.environ['LINE_BOT_TO_ID'],
            generate_parcel_message(parcel_info),
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
    }


if __name__ == '__main__':
    lambda_handler()
