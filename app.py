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
    msg = event.message.text.strip().lower()
    questions_answers = {
         "aspirin": "阿司匹林，用於減輕疼痛、發燒和炎症。",
        "ibuprofen": "布洛芬，是一種非甾體抗炎藥，用於減輕疼痛、發燒和炎症。",
        "acetaminophen": "對乙酰氨基酚，用於減輕疼痛和發燒。",
        "amoxicillin": "阿莫西林，是一種抗生素，用於治療細菌感染。",
        "lisinopril": "拉西利普利，是一種ACE抑制劑，用於治療高血壓和心力衰竭。",
        "metformin": "二甲雙胍，用於治療2型糖尿病。",
        "omeprazole": "奧美拉唑，用於治療胃酸過多和胃食管反流病。",
        "simvastatin": "辛伐他汀，用於降低膽固醇和甘油三酯水平。",
        "metoprolol": "美托洛爾，是一種β受體阻滯劑，用於治療高血壓、心絞痛和心律失常。",
        "albuterol": "沙丁胺醇，用於緩解哮喘和慢性阻塞性肺疾病（COPD）的症狀。",
        "atorvastatin": "阿托伐他汀，用於降低膽固醇和甘油三酯水平。",
        "gabapentin": "加巴噴丁，用於治療癲癇和神經性疼痛。",
        "levothyroxine": "左旋甲狀腺素，用於治療甲狀腺功能減退。",
        "hydrochlorothiazide": "氫氯噻嗪，用於治療高血壓和水腫。",
        "sertraline": "舍曲林，是一種選擇性5-羥色胺再攝取抑制劑（SSRI），用於治療抑鬱症、焦慮症和強迫症。",
        "losartan": "氯沙坦，用於治療高血壓和腎病。",
        "furosemide": "呋塞米，是一種利尿劑，用於治療水腫和高血壓。",
        "warfarin": "華法林，是一種抗凝劑，用於預防血栓形成。",
        "citalopram": "西酞普蘭，是一種SSRI，用於治療抑鬱症和焦慮症。",
        "montelukast": "孟魯司特，用於預防哮喘和治療過敏性鼻炎。"
    }
    if msg in questions_answers:
        response = questions_answers[msg]
    else:
        response = "對不起，我不太明白你的意思。"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response)
    )

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
