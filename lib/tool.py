from django.conf import settings
from linebot import LineBotApi,WebhookParser
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent,TextSendMessage,TextMessage,ImageSendMessage,StickerSendMessage,LocationSendMessage,VideoSendMessage,QuickReply
from linebot.models import QuickReplyButton,MessageAction
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
   
TRAIN_STATION={'基隆': '0900-基隆', '七堵': '0930-七堵', '南港': '0980-南港',
 '松山': '0990-松山', '臺北': '1000-臺北', '萬華': '1010-萬華', '板橋': '1020-板橋',
  '樹林': '1040-樹林', '桃園': '1080-桃園', '中壢': '1100-中壢', '新竹': '1210-新竹',
   '竹南': '1250-竹南', '苗栗': '3160-苗栗', '豐原': '3230-豐原', '臺中': '3300-臺中', 
   '彰化': '3360-彰化', '員林': '3390-員林', ' 斗六': '3470-斗六', '嘉義': '4080-嘉義', 
   '新營': '4120-新營', '臺南': '4220-臺南', '岡山': '4310-岡山', '新左營': '4340-新左營',
    '高雄': '4400-高雄', '屏東': '5000-屏東', '潮州': '5050-潮州', '臺東': '6000-臺東', 
    '玉里': '6110-玉里', '花蓮': '7000-花蓮', '蘇澳新': '7130-蘇澳新', '宜蘭': '7190-宜蘭',
     '瑞芳': '7360-瑞芳'}


def sendTrainQuickReply(text,event):
    items=[]
   
    for key in list(TRAIN_STATION.keys())[:13]:
        items.append(QuickReplyButton(action=MessageAction(key,text+":"+key)))
        
     
    message=TextSendMessage(text=text,quick_reply=QuickReply(items))
    
    line_bot_api.reply_message(event.reply_token,message)        


def sendMRTQuickReply(event):
    
    items=[
        QuickReplyButton(action=MessageAction("臺北","捷運圖:臺北")),
        QuickReplyButton(action=MessageAction("臺中","捷運圖:臺中")),      
        QuickReplyButton(action=MessageAction("高雄","捷運圖:高雄")),
    ]
    
    quick_reply=QuickReply(items)


    message=TextSendMessage(text="請選擇地點",quick_reply=quick_reply)
    
    line_bot_api.reply_message(event.reply_token,message)   



def sendQuickReply(event):


    items=[
        QuickReplyButton(action=MessageAction("臺北","@臺北")),
        QuickReplyButton(action=MessageAction("臺中","@臺中")),
        QuickReplyButton(action=MessageAction("台南","@台南")),
        QuickReplyButton(action=MessageAction("高雄","@高雄")),
    ]
    
    quick_reply=QuickReply(items)


    message=TextSendMessage(text="請選擇地點",quick_reply=quick_reply)
    
    line_bot_api.reply_message(event.reply_token,message)        
