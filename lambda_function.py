import base64
import chardet
import email
import os
import re
import sys
import httplib2
from apiclient import discovery
import gmail_auth


SEARCH_QUERY = 'from: mail@kuronekoyamato.co.jp AND (subject: お荷物お届けのお知らせ OR subject: 再配達依頼受付完了のお知らせ)'
PATTERNS = {
    'parcel_and_date': [
      r"(.+) 様からのお荷物を　【(.+)】　にお届け予定です。",
    ],
    'date_only': [
      r"(.+)にお届けに参りましたが、ご不在でしたので持ち帰りました。",
      r"■ご希望日時　　　：(.+)",
    ]
}

def get_gmail_service():
    # ユーザー認証の取得
    credentials = gmail_auth.gmail_user_auth()
    http = credentials.authorize(httplib2.Http())
    # GmailのAPIを利用する
    service = discovery.build('gmail', 'v1', http=http)
    return service


def get_messages():
    service = get_gmail_service()

    # メッセージの一覧を取得
    messages = service.users().messages()
    msg_list = messages.list(
        userId='me',
        maxResults=3,
        q=_generate_query_from_yamato()
    ).execute()

    msgs = []
    for msg in msg_list['messages']:
        msg = messages.get(userId='me', id=msg['id'], format='raw').execute()

        raw_msg = base64.urlsafe_b64decode(msg['raw'])
        email_msg = email.message_from_bytes(raw_msg)
        msgs.append(email_msg.get_payload(decode=True).decode('iso-2022-jp'))

    return msgs

def _generate_query_from_yamato():
    return SEARCH_QUERY


if __name__ == '__main__':
  patterns = {}
  for key, part_of_patterns in PATTERNS.items():
    patterns[key] = list(map(lambda v: re.compile(v), part_of_patterns))

  # メッセージの取得を実行
  messages = get_messages()
  for message in messages:
    result = {}
    for pattern in patterns['parcel_and_date']:
      match = pattern.search(message)
      if match:
        result['parcel'] = match.group(1)
        result['date'] = match.group(2)
        print('{0}: {1}'.format(match.group(1), match.group(2)))
        break
    if not result:
        for pattern in patterns['date_only']:
          match = pattern.search(message)
          if match:
            result['date'] = match.group(1)
            print('{0}'.format(match.group(1)))
            break
    if not result:
      print('No Info.')

