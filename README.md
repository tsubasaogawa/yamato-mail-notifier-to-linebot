# yamato-mail-notifier-to-linebot

Post text from mail sent by kuroneko yamato to linebot.

![image](https://raw.githubusercontent.com/tsubasaogawa/yamato-mail-notifier-to-linebot/images/image.png)

Now it can read the mail consisted of the following subject:

- お荷物お届けのお知らせ
- 再配達依頼受付完了のお知らせ

## Setup

### Clone the repository

:

### Enable GMail API and create client id

Download client_id.json to `yamato-mail-notifier-to-linebot` directory.

FYI: https://news.mynavi.jp/article/zeropython-22/

### Install libraries

```bash
cd yamato-mail-notifier-to-linebot
pip install -r requirements.txt -t .
```

### Create credentials

```bash
python gmail_auth.py
ls credentials-gmail.json
# assert that the json file exists
```

### Upload directory to S3

```bash
zip -r ../yamato-mail-notifier-to-linebot.zip .
aws s3 cp ../yamato-mail-notifier-to-linebot.zip 's3://your-s3-bucket-name/foo/bar'
```

Create lambda function using uploaded one.

### Set environment variables on your AWS management console

- LINE_BOT_ACCESS_TOKEN
  - Access token to use line bot.
- LINE_BOT_TO_ID
  - [user|room|group] ID that function posts to.
- NEWER_THAN
  - Search mails sent within it. ex. `1h`

### Create linebot-publisher-layer

In order to post to line bot, you should create [lambda layer](https://github.com/tsubasaogawa/linebot-publisher-layer) separately.
