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
       medications_info = {
        "aspirin": {
            "description": "阿司匹林，用於減輕疼痛、發燒和炎症。",
            "dosage": "一般劑量為每次 325-650 毫克，每 4-6 小時一次。",
            "usage": "口服，配水服用。飯後服用以減少胃部不適。",
            "precautions": "避免與其他非甾體抗炎藥同時使用。可能會引起胃腸道不適或出血。"
        },
        "ibuprofen": {
            "description": "布洛芬，是一種非甾體抗炎藥，用於減輕疼痛、發燒和炎症。",
            "dosage": "成人每次 200-400 毫克，每 4-6 小時一次。最大劑量不超過 3200 毫克/天。",
            "usage": "口服，最好隨餐服用以減少胃部不適。",
            "precautions": "避免長期使用，特別是有胃腸道潰瘍或出血風險者。"
        },
        "acetaminophen": {
            "description": "對乙酰氨基酚，用於減輕疼痛和發燒。",
            "dosage": "成人每次 500-1000 毫克，每 4-6 小時一次。最大劑量不超過 4000 毫克/天。",
            "usage": "口服，可隨餐或空腹服用。",
            "precautions": "避免與其他含有對乙酰氨基酚的藥物同時使用，以免過量。"
        },
        "amoxicillin": {
            "description": "阿莫西林，是一種抗生素，用於治療細菌感染。",
            "dosage": "成人每次 500 毫克，每 8 小時一次，或每次 875 毫克，每 12 小時一次。",
            "usage": "口服，可隨餐或空腹服用。",
            "precautions": "完成全程療程以防止抗藥性。若有過敏史應避免使用。"
        },
        "lisinopril": {
            "description": "拉西利普利，是一種ACE抑制劑，用於治療高血壓和心力衰竭。",
            "dosage": "成人通常起始劑量為 10 毫克，每天一次。根據病情調整劑量。",
            "usage": "口服，可隨餐或空腹服用。",
            "precautions": "監測血壓和腎功能。避免同時使用鉀補充劑。"
        },
        "metformin": {
            "description": "二甲雙胍，用於治療2型糖尿病。",
            "dosage": "成人通常起始劑量為 500 毫克，每天兩次。根據病情調整劑量。",
            "usage": "口服，隨餐服用以減少胃部不適。",
            "precautions": "監測腎功能。避免大量飲酒。"
        },
        "omeprazole": {
            "description": "奧美拉唑，用於治療胃酸過多和胃食管反流病。",
            "dosage": "成人通常劑量為 20 毫克，每天一次。根據病情調整劑量。",
            "usage": "口服，最好在早餐前30分鐘服用。",
            "precautions": "長期使用需醫生監督，可能影響鈣吸收。"
        },
        "simvastatin": {
            "description": "辛伐他汀，用於降低膽固醇和甘油三酯水平。",
            "dosage": "成人通常起始劑量為 10-20 毫克，每天一次，晚間服用。",
            "usage": "口服，晚餐後或睡前服用。",
            "precautions": "避免大量飲用葡萄柚汁，監測肝功能。"
        },
        "metoprolol": {
            "description": "美托洛爾，是一種β受體阻滯劑，用於治療高血壓、心絞痛和心律失常。",
            "dosage": "成人通常起始劑量為 50 毫克，每天一次或分次服用。",
            "usage": "口服，可隨餐或空腹服用。",
            "precautions": "避免突然停藥，可能引起心臟問題。"
        },
        "albuterol": {
            "description": "沙丁胺醇，用於緩解哮喘和慢性阻塞性肺疾病（COPD）的症狀。",
            "dosage": "每次 1-2 噴，根據需要使用，每 4-6 小時一次。",
            "usage": "吸入劑，按醫生指示使用。",
            "precautions": "過量使用可能引起心悸或震顫。"
        },
        "atorvastatin": {
            "description": "阿托伐他汀，用於降低膽固醇和甘油三酯水平。",
            "dosage": "成人通常起始劑量為 10-20 毫克，每天一次。",
            "usage": "口服，可隨餐或空腹服用。",
            "precautions": "避免大量飲用葡萄柚汁，監測肝功能。"
        },
        "gabapentin": {
            "description": "加巴噴丁，用於治療癲癇和神經性疼痛。",
            "dosage": "成人通常起始劑量為 300 毫克，每天三次。",
            "usage": "口服，可隨餐或空腹服用。",
            "precautions": "避免突然停藥，可能引起癲癇發作。"
        },
        "levothyroxine": {
            "description": "左旋甲狀腺素，用於治療甲狀腺功能減退。",
            "dosage": "成人通常起始劑量為 25-50 微克，每天一次。",
            "usage": "口服，早餐前30分鐘服用。",
            "precautions": "定期監測甲狀腺功能。避免與某些藥物同時服用。"
        },
        "hydrochlorothiazide": {
            "description": "氫氯噻嗪，用於治療高血壓和水腫。",
            "dosage": "成人通常起始劑量為 25-50 毫克，每天一次。",
            "usage": "口服，可隨餐或空腹服用。",
            "precautions": "監測血壓和腎功能。避免脫水。"
        },
        "sertraline": {
            "description": "舍曲林，是一種選擇性5-羥色胺再攝取抑制劑（SSRI），用於治療抑鬱症、焦慮症和強迫症。",
            "dosage": "成人通常起始劑量為 50 毫克，每天一次。",
            "usage": "口服，可隨餐或空腹服用。",
            "precautions": "避免突然停藥，可能引起戒斷症狀。"
        },
        "losartan": {
            "description": "氯沙坦，用於治療高血壓和腎病。",
            "dosage": "成人通常起始劑量為 50 毫克，每天一次。",
            "usage": "口服，可隨餐或空腹服用。",
            "precautions": "監測血壓和腎功能。避免同時使用鉀補充劑。"
        },
        "furosemide": {
            "description": "呋塞米，是一種利尿劑，用於治療水腫和高血壓。",
            "dosage": "成人通常劑量為 20-80 毫克，每天一次或分次服用。",
            "usage": "口服，可隨餐或空腹服用。",
            "precautions": "監測電解質水平和腎功能。"
        },
        "citalopram": {
            "description": "西酞普蘭，是一種選擇性5-羥色胺再攝取抑制劑（SSRI），用於治療抑鬱症和焦慮症。",
            "dosage": "成人通常起始劑量為 20 毫克，每天一次。",
            "usage": "口服，可隨餐或空腹服用。",
            "precautions": "避免突然停藥，可能引起戒斷症状。"
        }
        # 添加更多藥物的信息
    }

    if msg in medications_info:
        med_info = medications_info[msg]
        response = f"{med_info['description']}\n\n用量：{med_info['dosage']}\n服用方法：{med_info['usage']}\n注意事項：{med_info['precautions']}"
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
