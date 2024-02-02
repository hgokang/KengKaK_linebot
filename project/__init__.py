from flask import Flask, request, abort
from project.Config import *
from project.pic_to_str import *
from project.check_mont import *
from io import BytesIO
from PIL import Image
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, ImageMessage, TextSendMessage
import requests
import json
from project.gmail_reader import GmailClient

# Set up your Line API credentials

channel_secret = Channel_secret
channel_access_token = Channel_access_token

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    payload = request.json
    if 'replyToken' in payload['events'][0]:
        Reply_token = payload['events'][0]['replyToken']
    if 'text' in payload['events'][0]['message']:
        message = payload['events'][0]['message']['text']
        if 'ไอเก่ง' in message:
            Reply_message = 'ว่าไงน้อง'
            ReplyMessage(Reply_token,Reply_message,Channel_access_token)
        elif 'ตารางรายเดือน' in message:
            Reply_message = readfile()
            ReplyMessage(Reply_token,Reply_message,Channel_access_token)
        elif 'check' in message:
            check_month()
            Reply_message = readfile()
            ReplyMessage(Reply_token,Reply_message,Channel_access_token)
        elif 'ขอรหัส' in message:
            client = GmailClient(username, password)
            client.login()
            client.select_inbox()
            criteria = '(SUBJECT "Netflix")'
            criteria_bytes = criteria.encode('utf-8')
            message_ids = client.search_emails(criteria_bytes)
            msg = client.fetch_email(message_ids[len(message_ids)-1])
            client.save_email_content(msg)
            file_path = "netflix_link.txt"
            Reply_message = client.extract_access_code(file_path).strip("[]")
            client.close()
            client.logout()
            ReplyMessage(Reply_token,Reply_message,Channel_access_token)

    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def readfile():
    with open('test.txt', 'r', encoding='UTF-8') as file:
        return file.read()
    
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)

    with BytesIO(message_content.content) as image_bytes:
        img = Image.open(image_bytes)
        img.save("received_line.jpeg", "JPEG")

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f'{image_to_str()} \nตรวจสอบจำนวนเงินกับชื่อด้วยถ้าผิดแท็ก line มา')  # You can set 'text' to the text extracted from the image.
    )
def ReplyMessage(Reply_Token, TextMessage, Line_Access_Token):
    Line_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(Line_Access_Token)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization':Authorization
    }

    data = {
        'replyToken':Reply_Token,
        'messages':[{
            'type':'text',
            'text':TextMessage
        }]
    }

    data = json.dumps(data)
    r = requests.post(Line_API, headers=headers, data=data)
    return 200

# if __name__ == "__main__":
#     app.run(port = 200)
