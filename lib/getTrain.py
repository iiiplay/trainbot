import requests
from bs4 import BeautifulSoup


station={}

# =============================================================================
# 取得常用站點
# =============================================================================
def getStation(url): 
        
    resp=requests.get(url)
    if resp.status_code!=200:
        return 'error'
    
    soup=BeautifulSoup(resp.text,'lxml')
    
    citys=soup.find(id='cityHot').find('ul').find_all('li')
    
    for city in citys:
        name=city.find('button').text
        code=city.find('button')['title']
        
        station[name]=code
    
    print('取得站點資料ok')
    
    request_url=soup.find(id='queryForm')['action']
    crsf_code=soup.find(id='queryForm').find('input',{'name':'_csrf'})['value']
    #crsf_code=soup.find(id='queryForm').find('input')['value']
    
    return request_url,crsf_code

def getTrain(start='臺中',end='高雄'):
    url='https://www.railway.gov.tw/tra-tip-web/tip'

    request_url,crsf_code=getStation(url) 
    print(station)
    print(request_url,crsf_code)
    import time

    today=time.strftime('%Y/%m/%d')
    stime=time.strftime("%H:%M", time.localtime()) 
    print(stime)
    sTime='20:00'
    eTime='23:59'

    start_station=station[start]
    end_station=station[end]


    form_data={
        
        '_csrf': crsf_code,
        'trainTypeList': 'ALL',
        'transfer': 'ONE',
        'startStation': start_station,
        'endStation': end_station,
        'rideDate': today,
        'startOrEndTime': 'true',
        'startTime': sTime,
        'endTime': eTime    
    }

    print(form_data)

    print('https://www.railway.gov.tw'+request_url)

    resp=requests.post('https://www.railway.gov.tw'+request_url,data=form_data)

    if resp.status_code==200:
        soup=BeautifulSoup(resp.text,'lxml')
    
        trs=soup.find('table').find('tbody').find_all('tr',class_='trip-column')

        message=''
        for tr in trs:       
            tds=tr.find_all('td')      
            print(tds[0].text.strip(),tds[1].text,tds[2].text,tds[3].text,
                tds[-1].text.strip())

            str1=tds[0].text.strip()+'\t'+tds[1].text+'\t'+tds[2].text+'\t'+tds[3].text+'\t'+\
            tds[-1].text.strip()+'\n'        
            message+=str1

        return message
