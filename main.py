import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai

app = Flask(__name__)

# 設定 Line Bot 相關的資訊
line_bot_api_key = 'k1ApTQ4JNvCJBUAXixTjCVppqnoHfl8iasHyhejLIGbADH/+SseDSLmmf0ICutgmj46ec0HdkPpK6G08+UpSmdGKHNsckXr5cf+2knQscx3yJnTOsZDWRPcnSlU6OuAzhfePNXi1ADtNGAH7kzC7dgdB04t89/1O/w1cDnyilFU='
handler_key = 'da6616b3299cd94df2727f03b0742f2a'
line_bot_api = LineBotApi(line_bot_api_key)
handler = WebhookHandler(handler_key)

open_ai_api_key ='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'

# 設定 OpenAI 相關的資訊
openai.api_key = open_ai_api_key

# Line Bot 回應訊息的函式
def reply_text(reply_token, text):
    message = TextSendMessage(text=text)
    line_bot_api.reply_message(reply_token, message)

# OpenAI 生成文本的函式
def generate_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()

# Line Bot 接收訊息的 Webhook
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

# Line Bot 接收文字訊息的處理函式
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text

    # 使用 OpenAI 生成回應
    if text.startswith("OpenAI:"):
        prompt = text[8:]
        #response = generate_text(prompt)
        response = 'hello world'
        reply_text(event.reply_token, response)
    else:
        # 回應原本的訊息
        reply_text(event.reply_token, text)

if __name__ == "__main__":
    app.run()