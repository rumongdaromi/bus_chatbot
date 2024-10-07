from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request,"mainpage.html")
# Create your views here.


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

import json
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class YounginBus:
    def __init__(self, bus_num):
        self.bus_num = bus_num

    def bus_time(self, start_flag):  # start_flag를 매개변수로 추가
        base = 'http://knyongintr.co.kr/board/bus_'
        url = base + self.bus_num + ".html"
        
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        youngin_start = []
        end_point = []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        table_body = soup.select_one('#popup > div > div.content > table > tbody')

        if table_body:
            for row in table_body.find_all('tr'):
                row_data = [cell.text.strip() for cell in row.find_all('td')]
                if len(row_data) >= 2:
                    youngin_start.append(row_data[0])
                    end_point.append(row_data[1])
        else:
            table_body = soup.select_one('#popup > div > div.content > div > table > tbody')
            if table_body:
                for row in table_body.find_all('tr'):
                    row_data = [cell.text.strip() for cell in row.find_all('td')]
                    if len(row_data) >= 2:
                        youngin_start.append(row_data[0])
                        end_point.append(row_data[1])

        return youngin_start, end_point

@csrf_exempt
def message_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        # 입력 메시지를 파싱
        parts = user_message.split()
        if len(parts) != 2:
            return JsonResponse({'reply': "올바른 형식이 아닙니다. 예: '용인출발 22' 또는 '종점출발 22'."})

        direction = parts[0]  # '용인출발' 또는 '종점출발'
        bus_num = parts[1]  # 버스 번호

        if not bus_num.isdigit():
            return JsonResponse({'reply': "버스 번호는 숫자로 입력해야 합니다."})

        # YounginBus 인스턴스 생성
        bus = YounginBus(bus_num)
        start_flag = 0 if direction == "용인출발" else 1  # 출발 방향에 따라 start_flag 설정
        youngin_start, end_point = bus.bus_time(start_flag)  # start_flag를 전달

        # 시간표 응답 준비
        if start_flag == 0:  # 용인 출발
            reply = f"{bus_num}번 버스 시간표 (용인 출발):\n"
            reply += "-" * 30 + "\n"
            for start in youngin_start:
                reply += f"용인 출발: {start}\n"
            reply += "-" * 30 + "\n"
        else:  # 종점 출발
            reply = f"{bus_num}번 버스 시간표 (종점 출발):\n"
            reply += "-" * 30 + "\n"
            for end in end_point:
                reply += f"종점 출발: {end}\n"
            reply += "-" * 30 + "\n"

        reply += "시간표 끝입니다."
        return JsonResponse({'reply': reply})

    return JsonResponse({'error': 'Invalid request'}, status=400)





