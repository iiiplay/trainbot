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

start_sation=''
end_station=''


@csrf_exempt
def callback(request):
    global start_sation
    global end_station

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
                    if '@圖片'==mtext:
                        tool.sendMRTQuickReply(event)
                      
                    elif '捷運圖' in mtext:
                        img_url=''
                        city= mtext.split(':')[1]
                        if city=='臺北':
                            img_url='https://m.metro.taipei/img/routemap2020.png'
                        elif city=='臺中':
                            img_url='https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/%E5%8F%B0%E4%B8%AD%E6%8D%B7%E9%81%8B%E8%B7%AF%E7%B7%9A%E5%9C%96_%282020.01%29.png/750px-%E5%8F%B0%E4%B8%AD%E6%8D%B7%E9%81%8B%E8%B7%AF%E7%B7%9A%E5%9C%96_%282020.01%29.png' 
                        elif city=='高雄':
                            img_url='https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/%E9%AB%98%E9%9B%84%E6%8D%B7%E9%81%8B%E8%B7%AF%E7%B6%B2%E5%9C%96_%28C1-C14%E7%AB%99%E5%90%8D%E7%A2%BA%E5%AE%9A%E7%89%88%29.png/550px-%E9%AB%98%E9%9B%84%E6%8D%B7%E9%81%8B%E8%B7%AF%E7%B6%B2%E5%9C%96_%28C1-C14%E7%AB%99%E5%90%8D%E7%A2%BA%E5%AE%9A%E7%89%88%29.png'
                        
                        tool.sendImage(img_url,event)


                    elif '@車票'==mtext:
                        tool.sendTrainQuickReply("起始站",event)
                    
                    elif '起始站' in mtext:
                        start_sation=mtext.split(':')[1]
                        tool.sendTrainQuickReply("終點站",event)
                    
                    elif '終點站' in mtext:
                        end_sation=mtext.split(':')[1]
                        print(start_sation,end_sation)
                        message=getTrain.getTrain(start_sation,end_sation)                     
                        tool.sendText(message,event)   
                    
                    elif '@車票' in mtext:   

                        tool.sendQuickReply(event)    
                        #message=getTrain.getTrain()                     
                        #tool.sendText(message,event)                      
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


