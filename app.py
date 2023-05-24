from bs4 import BeautifulSoup
import requests
import json
import time
from flask import Flask, request, jsonify, make_response
from datetime import datetime, timedelta
url = 'http://sejong.korea.ac.kr/campuslife/facilities/dining/weeklymenu'


def addDays(sourceData, cnt):
    targetData = sourceData + timedelta(days = cnt)
    return targetData

def getWeekFirstDay(sourceData):
    temporaryDate = datetime(sourceData.year, sourceData.month, sourceData.day)
    weekDayCnt = temporaryDate.weekday()
    targetDate = addDays(temporaryDate, -weekDayCnt)
    return targetDate.strftime('%Y-%m-%d')

def datetimeToStr(sourceData):
    t = datetime(sourceData.year, sourceData.month, sourceData.day)
    return t.strftime('%Y-%m-%d')

#now = datetime.today().strftime('%Y%m%d')
def getMenuToJson():
    html = requests.get(url).text
    bsObject = BeautifulSoup(html, 'html.parser')
    ret = {}
    now = datetime.today().strftime('%Y %m %d').split(' ')
    year, month, day = int(now[0]), int(now[1]), int(now[2])
    weekday = getWeekFirstDay(datetime(year, month, day)).split('-')
    for i in range(2, 7): 
        selector = f'#sCont > div.subArea > div:nth-child(12) > table > tbody > tr:nth-child(2) > td:nth-child({i})'
        res = str(bsObject.select_one(selector)).split('<p>')[1:]
        for j in range(len(res)):
            res[j] = res[j].replace('</p>', '').replace('</td>', '').replace('<span style="font-size: 10pt;">', '').replace('</span>', '')
        year, month, day = int(weekday[0]), int(weekday[1]), int(weekday[2]) + i - 2
        current = datetimeToStr(datetime(year, month, day))
        t = [x for x in res]
        ret[current] = t
    return json.dumps(ret, ensure_ascii=False)

menu = getMenuToJson()
app = Flask(__name__)
@app.route('/')
def returnMenu():
    return make_response(menu)

if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0')