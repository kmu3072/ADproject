import pandas as pd
import requests
from bs4 import BeautifulSoup

station_info = pd.read_csv('station_id.csv', encoding='CP949')

try:
    station = "신길"
    no = '05호선'
    line = '하행'

    station_info = station_info[station_info['전철역명'] == station]
    station_info = station_info[station_info['호선'] == no]

    station_no = station_info.iloc[0]['외부코드']

    if station == '광명':
        url = "https://bus.go.kr/getSubway_6.jsp?statnId=1001075410&subwayId=1001&tabmn=5"

    elif station == '서동탄':
        station_no = station_no.replace('P', '')
        station_no = station_no.replace('-', '')
        url = "https://bus.go.kr/getSubway_6.jsp?statnId=100180" + station_no + "&subwayId=1001&tabmn=5"

    elif 'P' in station_no:
        station_no = station_no.replace('P', '')
        sno = int(station_no)
        if sno > 173:
            sno -= 1
            if sno > 175:
                sno -= 1
        url = "https://bus.go.kr/getSubway_6.jsp?statnId=1001080" + str(sno) + "&subwayId=1001&tabmn=5"


    elif '-' in station_no:
        station_no = station_no.replace('-', '')
        sno = int(station_no)
        url = "https://bus.go.kr/getSubway_6.jsp?statnId=100200" + str(sno) + "&subwayId=1002&tabmn=5"
    else:
        url = "https://bus.go.kr/getSubway_6.jsp?statnId=100" + no[1:2] + "000" + station_no + "&subwayId=100" + no[
                                                                                                                 1:2] + "&tabmn=5"

    print(url)
    response = requests.get(url)

    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    opportunity = int(soup.select_one('tr:nth-of-type(2) > td').get('rowspan'))
    print(opportunity)
    # uptrain = []
    # downtrain = []
    # arrivestationlist = soup.select('tr')[1:]   #int(opportunity)+2
    u_timelist = soup.select('tr')[3:opportunity + 2]  # int(opportunity)+2
    d_timelist = soup.select('tr')[opportunity + 3:]

    if line == '상행':
        for time in u_timelist:
            t = time.get_text().replace('\n', '')
            t1 = t.replace('하행(내선)', '')
            if len(t1) < 100:
                print(t1)

    if line == '하행':
        for time in d_timelist:
            t = time.get_text().replace('\n', '')
            t2 = t.replace('하행(내선)', '')
            if len(t2) < 100:
                print(t2)

except:
    print('잘못된 입력값')
