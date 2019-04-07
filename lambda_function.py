import httplib2, os
from apiclient import discovery
import gmail_auth # 先ほど作成したプログラム

# Gmailのサービスを取得
def gmail_get_service():
    # ユーザー認証の取得
    credentials = gmail_auth.gmail_user_auth()
    http = credentials.authorize(httplib2.Http())
    # GmailのAPIを利用する
    service = discovery.build('gmail', 'v1', http=http)
    return service

# メッセージの一覧を取得
def gmail_get_messages():
    service = gmail_get_service()
    # メッセージの一覧を取得
    messages = service.users().messages()
    msg_list = messages.list(userId='me', maxResults=10).execute()

    # 取得したメッセージの一覧を表示
    for msg in msg_list['messages']:
        topid = msg['id']
        msg = messages.get(userId='me', id=topid).execute()
        print("---")
        print(msg['snippet']) # 要約を表示


if __name__ == '__main__':
  # メッセージの取得を実行
  gmail_get_messages()
