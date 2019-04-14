from apiclient import discovery
import base64
import email
import httplib2

import gmail_auth

class Gmail:
  def __init__(self):
    self.service = self._get_gmail_service()

  def _get_gmail_service(self):
    # ユーザー認証の取得
    credentials = gmail_auth.gmail_user_auth()
    http = credentials.authorize(httplib2.Http())
    # GmailのAPIを利用する
    service = discovery.build('gmail', 'v1', http=http, cache_discovery=False)
    return service

  def get_messages(self, maxResults=10, query='', newerThan='1h'):
    # メッセージの一覧を取得
    messages = self.service.users().messages()
    if newerThan:
      query = query + ' newer_than:{0}'.format(newerThan)

    msg_list = messages.list(
      userId='me',
      maxResults=maxResults,
      q=query,
    ).execute()
    if not 'messages' in msg_list:
      return []

    msgs = []
    for msg in msg_list['messages']:
      msg = messages.get(userId='me', id=msg['id'], format='raw').execute()

      raw_msg = base64.urlsafe_b64decode(msg['raw'])
      email_msg = email.message_from_bytes(raw_msg)
      msgs.append(email_msg.get_payload(decode=True).decode('iso-2022-jp'))

    return msgs