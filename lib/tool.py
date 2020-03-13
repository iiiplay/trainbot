from django.conf import settings
from linebot import LineBotApi,WebhookParser
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent,TextSendMessage,TextMessage,ImageSendMessage,StickerSendMessage,LocationSendMessage,VideoSendMessage

line_bot_api=LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


def sendText(message,event):
    message=TextSendMessage(text=message)
    line_bot_api.reply_message(event.reply_token,message)        

def sendImage(img_url,event):
    message=ImageSendMessage(
                                original_content_url=img_url,
                                preview_image_url=img_url,
                        )

    line_bot_api.reply_message(event.reply_token,message)

#傳送貼圖
def sendSticker(p_id,s_id,event):
    try:
        message=StickerSendMessage(
            package_id=p_id,
            sticker_id=s_id,
        )

        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='傳送失敗!'))    

#地點
def sendLocation(info,event):
    message=LocationSendMessage(        
                                title='my location', address='Tainan', 
                                latitude=22.994821, longitude=120.196452          
                        )

    message=LocationSendMessage(  
         info[0],info[1],info[2],info[3]     
                               
                        )

    line_bot_api.reply_message(event.reply_token,message)


def sendVideoMessage(video_url,image_url,event):
    
    message=VideoSendMessage(
            original_content_url=video_url,
            preview_image_url=image_url,
    )

    line_bot_api.reply_message(event.reply_token,message)
   