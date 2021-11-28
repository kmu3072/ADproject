import datetime
from sys import exit
from station_info import *
from line import Line
import requests
from bs4 import BeautifulSoup

station = input("역명: ").replace(" ", '')
no = input("호선:") + "호선"
direction = input("방향: ").replace(" ", '')
while True:
    try:
        Info = Line(station, no, direction)
    except:
        print('올바른 값이 입력되지 않았습니다')
        station = input("역명: ").replace(" ", '')
        no = input("호선:") + "호선"
        direction = input("방향: ").replace(" ", '')
    else:
        break

if station in except_stations and no != '05호선':  # 5호선 까치산의 경우 데이터베이스가 존재함
    timeline = Info.noInfoStations()
    exit()
elif no == '01호선':
    url = Info.line01()
elif no == '05호선':
    url = Info.line05()
else:
    url = Info.lineN()

print(url)
response = requests.get(url)

html = response.text
soup = BeautifulSoup(html, 'html.parser')

opportunity = soup.select_one('tr:nth-of-type(2) > td').get('rowspan')  # 배정된 열차 수 가져오기
# print(opportunity)

hour = datetime.datetime.now().hour  # - 시간만 따오기
if hour == 0:
    hour = 24
minute = datetime.datetime.now().minute  # - 분만 따오기
# print(datetime.datetime.now().weekday()) #(0이 월요일, 6이 일요일)

u_timelist = soup.select('tr')[2: int(opportunity) + 2]  # 상행 첫차부터 막차까지 뽑아오기
d_timelist = soup.select('tr')[int(opportunity) + 4: -1]  # 하행 첫차부터 막차까지 뽐아오기

if station in circle_line_6 and direction == '상행': # 응암순환선의 경우 상행 하행 구분이 
    direction = '하행'

if direction == '상행':  # 상행선
    min1 = 99
    min2 = 99
    res = ''
    for time in u_timelist:
        t = time.get_text().replace('\n', '')
        t1 = t.replace('상행(외선)', '')
        subh = int(t1[0:2]) - hour
        subm = int(t1[3:5]) - minute
        if (subh == 0 and subm >= 0) or (subh == 1 and subm > -60):
            res = t1
            break

    if res == '':  # 막차가 끊겼을 경우
        for time in u_timelist:
            t = time.get_text().replace('\n', '')
            t1 = t.replace('상행(외선)', '')
            if '(급행)' in t1[5:]:
                ex_rapid = t1.replace('(급행)', '')
                if ex_rapid[5:] == station:
                    print('이번 열차는 당역에 종착하는 열차입니다.')
                    break
                else:
                    print(res)
                    break
            elif t1[5:] == station:  # 열차가 당역에 종차할 시
                print('이번 열차는 당역에 종착하는 열차입니다.')
                break
            print(t1)  # 첫차 표시
            break

    elif station != '성수' and station != '신도림':  # 2호선의 경우, 순환 형태를 띰
        if '(급행)' in res[5:]:
            ex_rapid = res.replace('(급행)', '')
            if ex_rapid[5:] == station:
                print('이번 열차는 당역에 종착하는 열차입니다.')
            else:
                print(res)
        elif res[5:] == station:  # 열차가 당역에 종차할 시
            print('이번 열차는 당역에 종착하는 열차입니다.')

        else:
            print(res)

    else:
        print(res)

if direction == '하행':  # 하행선
    res = ''
    for time in d_timelist:
        t = time.get_text().replace('\n', '')
        t2 = t.replace('하행(내선)', '')
        subh = int(t2[0:2]) - hour
        subm = int(t2[3:5]) - minute
        if (subh == 0 and subm >= 0) or (subh == 1 and subm > -60):
            res = t2
            break

    if res == '':
        for time in d_timelist:
            t = time.get_text().replace('\n', '')
            t2 = t.replace('하행(내선)', '')
            if '(급행)' in t2[5:]:
                ex_rapid = t2.replace('(급행)', '')
                if ex_rapid[5:] == station:
                    print('이번 열차는 당역에 종착하는 열차입니다.')
                    break
                else:
                    print(res)
                    break
            elif t2[5:] == station:  # 열차가 당역에 종차할 시
                print('이번 열차는 당역에 종착하는 열차입니다.')
                break
            print(t2)
            break

    elif station != '성수' and station != '신도림':  # 2호선의 경우, 순환 형태를 띰
        if '(급행)' in res[5:]:
            ex_rapid = res.replace('(급행)', '')
            if ex_rapid[5:] == station:
                print('이번 열차는 당역에 종착하는 열차입니다.')
            else:
                print(res)
        elif res[5:] == station:  # 열차가 당역에 종차할 시
            print('이번 열차는 당역에 종착하는 열차입니다.')
        else:
            print(res)

    else:
        print(res)
