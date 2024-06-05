from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======python的函數庫==========
import tempfile, os
import datetime
import time
import traceback
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if msg == "查詢圖書":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入您要查詢的圖書名稱或作者。")
        )
    elif "查詢圖書:" in msg:
        book_name = msg.replace("查詢圖書:", "").strip()
        books = search_books(book_name)
        reply = "我們找到以下與“{}”相關的書籍：\n".format(book_name)
        for i, book in enumerate(books):
            reply += "{}. {}\n".format(i+1, book['title'])
        reply += "請輸入您想了解的書籍編號，或者輸入“返回”返回主菜單。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )
    elif msg == "預約座位":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請選擇您要預約的日期（格式：YYYY-MM-DD）。")
        )
    elif re.match(r"\d{4}-\d{2}-\d{2}", msg):
        date = msg.strip()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="請選擇您要預約的時間段：\n1. 上午（09:00-12:00）\n2. 下午（13:00-17:00）\n3. 晚上（18:00-21:00）"
            )
        )
    elif msg in ["1", "2", "3"]:
        timeslot = {"1": "上午（09:00-12:00）", "2": "下午（13:00-17:00）", "3": "晚上（18:00-21:00）"}[msg]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="您已成功預約。感謝您的使用！")
        )
    elif msg == "查詢借閱狀態":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入您的借閱證號碼。")
        )
    elif re.match(r"\d+", msg):
        card_number = msg.strip()
        borrow_status = get_borrow_status(card_number)
        reply = "您當前借閱的書籍有：\n"
        for book in borrow_status:
            reply += "{} - 歸還期限：{}\n".format(book['title'], book['due_date'])
        reply += "請輸入“續借”以延長借閱期限，或者輸入“返回
                line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )
    elif msg == "續借":
        extend_borrowing()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="您的借閱期限已延長。")
        )
    else:
        questions_answers = {
            "apple": "蘋果",
            "banana": "香蕉",
            "cat": "貓",
            "dog": "狗",
            # ... existing questions_answers ...
        }
        if msg in questions_answers:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(questions_answers[msg]))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(msg))

def search_books(query):
    books = [
        {'title': '哈利波特與魔法石'},
        {'title': '哈利波特與密室'},
        {'title': '哈利波特與阿茲卡班的囚徒'}
    ]
    return books

def get_borrow_status(card_number):
    borrow_status = [
        {'title': '大數據時代', 'due_date': '2024-06-15'},
        {'title': '人工智能簡史', 'due_date': '2024-06-20'}
    ]
    return borrow_status

def extend_borrowing():
    pass

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
