from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


from linebot import LineBotApi,WebhookParser
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent,TextSendMessage,TextMessage,ImageSendMessage,StickerSendMessage,LocationSendMessage,VideoSendMessage


line_bot_api=LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser=WebhookParser(settings.LINE_CHANNEL_SECRET)


from lib import tool,getTrain

@csrf_exempt
def callback(request):
    if request.method=='POST':
        signature=request.META['HTTP_X_LINE_SIGNATURE']
        body=request.body.decode('utf-8')        
        try:
            events=parser.parse(body,signature)            
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()       
     
        #進行訊息的循環判斷
        for event in events:            
            if isinstance(event,MessageEvent):   
                if isinstance(event.message,TextMessage):
                    mtext=event.message.text               
                    print(mtext.split())       
                    if '車票' in mtext:                  
                        message=getTrain.getTrain()                     
                        tool.sendText(message,event)                      
                    elif '地點' in mtext:
                        tool.sendLocation(['my location','Tainan', 
                                22.994821, 120.19645],event)                      
                    elif '影片' in mtext:                               
                        tool.sendVideoMessage('https://www.radiantmediaplayer.com/media/bbb-360p.mp4',
                        'https://assets.piliapp.com/s3pxy/mrt_taiwan/taipei/20190910_zh.png',event)                                        
                    elif '捷運' in mtext:                        
                        tool.img_url='https://assets.piliapp.com/s3pxy/mrt_taiwan/taipei/20190910_zh.png'
                        if '高雄' in mtext:
                            img_url='https://assets.piliapp.com/s3pxy/mrt_taiwan/kaohsiung/201811_zh-Hant.png'
                        tool.sendImage(img_url,event)
                    else:                       
                        tool.sendText('資料庫無此資料',event)                   

            
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


