import pandas as pd
import datetime

class Line:
    def __init__(self, station, no, direction):
        station_info = pd.read_csv('station_id.csv', encoding='CP949')
        self.station = station
        self.no = no
        self.direction = direction
        station_info = station_info[station_info['전철역명'] == station]
        station_info = station_info[station_info['호선'] == no]

        self.station_no = station_info.iloc[0]['외부코드']

    def line01(self):

        if self.station == '광명':
            url = "https://bus.go.kr/getSubway_6.jsp?statnId=1001075410&subwayId=1001&tabmn=5"

        elif self.station == '서동탄':
            self.station_no = self.station_no.replace('P', '')
            self.station_no = self.station_no.replace('-', '')
            url = "https://bus.go.kr/getSubway_6.jsp?statnId=100180" + self.station_no + "&subwayId=1001&tabmn=5"

        elif 'P' in self.station_no:
            self.station_no = self.station_no.replace('P', '')
            sno = int(self.station_no)
            if sno > 173:
                sno -= 1
                if sno > 175:
                    sno -= 1
            url = "https://bus.go.kr/getSubway_6.jsp?statnId=1001080" + str(sno) + "&subwayId=1001&tabmn=5"

        elif '-' in self.station_no:
            self.station_no = self.station_no.replace('-', '')
            sno = int(self.station_no)
            print(sno)
            url = "https://bus.go.kr/getSubway_6.jsp?statnId=100100" + str(sno) + "&subwayId=1001&tabmn=5"
        else:
            url = "https://bus.go.kr/getSubway_6.jsp?statnId=1001000" + self.station_no + "&subwayId=1001&tabmn=5"

        return url

    def line05(self):

        if 'P' in self.station_no:
            self.station_no = self.station_no.replace('P', '')

            url = "https://bus.go.kr/getSubway_6.jsp?statnId=1005080" + self.station_no + "&subwayId=1005&tabmn=5"

        elif '-' in self.station_no:
            station_no = self.station_no.replace('-', '')
            sno = int(station_no)
            print(sno)
            url = "https://bus.go.kr/getSubway_6.jsp?statnId=100500" + str(sno) + "&subwayId=1005&tabmn=5"
        else:
            url = "https://bus.go.kr/getSubway_6.jsp?statnId=1005000" + self.station_no + "&subwayId=1005&tabmn=5"

        return url

    def lineN(self):
        if '-' in self.station_no:
            station_no = self.station_no.replace('-', '')
            sno = int(station_no)
            print(sno)
            url = "https://bus.go.kr/getSubway_6.jsp?statnId=100200" + str(sno) + "&subwayId=1002&tabmn=5"
        else:
            url = "https://bus.go.kr/getSubway_6.jsp?statnId=100" + self.no[1:2] + "000" + self.station_no + "&subwayId=100" + self.no[
                                                                                                                 1:2] + "&tabmn=5&sub=3"
        return url

    def noInfoStations(self):
        f = open(self.station+".txt", encoding="utf-8")
        timelines = f.readlines()
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        cnt = 0
        t_last = 0
        for time in timelines:
            t = time.replace('\n', '')
            if t[0:2]:
                if int(t[0:2]) < t_last:
                    break
                else:
                    t_last = int(t[0:2])
                    cnt += 1

        u_list = timelines[0:cnt]
        d_list = timelines[cnt+1 : ]

        if self.station == '까치산':
            for time in timelines:
                t = time.replace('\n', '')
                subh = int(t[0:2]) - hour
                subm = int(t[3:5]) - minute
                if self.direction == '하행':
                    print('이번 열차는 당역에 종착하는 열차입니다.')
                    return
                if (subh == 0 and subm >= 0) or (subh == 1 and subm > -60):
                    res = t
                    break
            print(res)

        elif self.station == '중앙보훈병원':
            for time in timelines:
                t = time.replace('\n', '')
                subh = int(t[0:2]) - hour
                subm = int(t[3:5]) - minute
                if self.direction == '상행':
                    print('이번 열차는 당역에 종착하는 열차입니다.')
                    return
                if (subh == 0 and subm >= 0) or (subh == 1 and subm > -60):
                    res = t
                    break
            print(res)

        elif self.direction == '상행':
            for time in u_list:
                t = time.replace('\n', '')
                subh = int(t[0:2]) - hour
                subm = int(t[3:5]) - minute
                if subh == 0 and subm > 0:
                    res = t
                    break
            print(res)

        elif self.direction == '하행':
            for time in d_list:
                t = time.replace('\n', '')
                subh = int(t[0:2]) - hour
                subm = int(t[3:5]) - minute
                if subh == 0 and subm > 0:
                    res = t
                    break
            print(res)
