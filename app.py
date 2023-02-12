from random import choice
import sqlite3
from create_db import create_db
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi(
    'ccY8HvjSeluggPMbmzc9isMqta9BuC7cyBLpXqdo9bNNmgblqW+7gK7GoJWB3bxyEKUlyVvzRUR+AWK7DvVsaKFOvMUawGNjU0Ys363sZsF6b/TF5N+ZCCfaQNuzuijfJIwA5xnq8SEqD4vu83ND+gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('37c93210c3bda52d8f164cd756def31e')

@app.route("/")
def test():
  return 'OK!'

create_db()


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


users = {}


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    select_test = f"SELECT dajare FROM test WHERE dajare LIKE '%{event.message.text}%';"
    print(select_test)
    cur.execute(select_test)
    select_dajare = cur.fetchall()
    if len(select_dajare) == 0:
        reply = 'そのワードを使用したダジャレはまだないよ！'
        line_bot_api.reply_message(
            event.reply_token,TextSendMessage(text=reply))
    else:
        reply = choice(select_dajare)
        line_bot_api.reply_message(
            event.reply_token,TextSendMessage(text=reply[0]))

    # userId = event.source.user_id
    # if event.message.text == "ありがとう":
    #     reply = "どういたしまして"
    # elif event.message.text == "勉強開始":
    #     reply = "計測を開始します"
    #     if not userId in users:
    #         users[userId]={}
    #         users[userId]['total']=0
    #     users[userId]['start'] = time()#現在時間(1970年1月1日からの秒数)
    # elif event.message.text == "勉強終了":
    #     end = time()
    #     difference = int(end - users[userId]['start'])
    #     users[userId]['total']+=difference
    #     hour = difference // 3600
    #     minute = (difference % 3600) // 60
    #     second = difference % 60
    #     reply = f"ただいまの勉強時間は{hour}時間{minute}分{second}秒です。お疲れ様でした。現在合計で{users[userId]['total']}秒勉強しています。"
    # else:
    #     reply = f"あなたは、{event.message.text}と言いました"




if __name__ == "__main__":
    app.run(debug=True)
