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

line_bot_api = LineBotApi('ccY8HvjSeluggPMbmzc9isMqta9BuC7cyBLpXqdo9bNNmgblqW+7gK7GoJWB3bxyEKUlyVvzRUR+AWK7DvVsaKFOvMUawGNjU0Ys363sZsF6b/TF5N+ZCCfaQNuzuijfJIwA5xnq8SEqD4vu83ND+gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('37c93210c3bda52d8f164cd756def31e')

# @app.route("/")
# def test():
#   return 'OK!'


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  if event.message.text == "ありがとう":
    reply = "どういたしまして"
  else:
    reply = f"あなたは、{event.message.text}と言いました"
  line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text = reply))


if __name__ == "__main__":
    app.run()