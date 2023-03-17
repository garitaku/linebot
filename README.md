# linebot
適当なワードを送信すると、そのワードを使用したダジャレを返してくれるbot。

LINE Messaging API SDKを使用。

ダジャレ自体は「ダジャレ・ステーション」様 "https://dajare.jp/" からスクレイピング(dajare.py)で取得。

取得結果がcsvデータになるため、それをcreate_db.pyでデータベース(sqlite)へ。

app.pyにてselect文で条件に合致するダジャレを取得しbotで送信。

![image](https://github.com/garitaku/linebot/blob/master/RPReplay_Final1679017192.gif)
