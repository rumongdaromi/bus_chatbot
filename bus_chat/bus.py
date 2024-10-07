import requests
from bs4 import BeautifulSoup

# 웹 페이지 요청
base = 'http://knyongintr.co.kr/board/bus_'
num = ["21","22","24","91","92","22-1"]
url = 'http://knyongintr.co.kr/board/bus_22.html'
bus_num = input("필요한 버스번호를 입력해주세요. ==> ")
if bus_num in num:
    url = base + bus_num + ".html"
    start_local = int(input("용인출발은 0, 터미널출발은 1을 입력해주세요. ==> "))

response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

# //*[@id="popup"]/div/div[2]/div/table/tbody
# //*[@id="popup"]/div/div[2]/table/tbody/tr[4]/td[1]
용인터미널출발 = []
종점출발 = []
# BeautifulSoup을 사용하여 HTML 파싱
soup = BeautifulSoup(response.content, 'html.parser')

# 테이블 tbody 요소 찾기
table_body = soup.select_one('#popup > div > div.content > div > table > tbody')
# table_body = soup.select_one('#popup > div > div.content > table > tbody')

# 각 행과 열의 시간 데이터 가져오기
if table_body:
    rows = []
    for row in table_body.find_all('tr'):
        row_data = []
        for cell in row.find_all('td'):
            row_data.append(cell.text.strip())
        rows.append(row_data)
        
    # 결과 출력
    for i in range(len(rows)):

        용인터미널출발.append(rows[i][0])        
        종점출발.append(rows[i][1])
       
else:
    print("테이블 tbody 요소를 찾을 수 없습니다.")


if start_local == 0:
    print("용인터미널출발 시간표입니다.")
    for i in 용인터미널출발:
        print(i)

elif start_local == 1:
    print("종점출발 시간표입니다.")
    for i in 종점출발:
        print(i)