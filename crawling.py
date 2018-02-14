import json
import websocket
import requests
from bs4 import BeautifulSoup

data = {'cinemaCode1': '4253', 'mBookingType': '2'}
req = requests.post('http://m.megabox.co.kr/pages/mBooking/Booking_List_M.jsp', data=data)

html = req.text
#
soup = BeautifulSoup(html, 'html.parser')
#
cinema_texts = soup.select('a')

cinema_list = []

for a in cinema_texts:
	cinema_list.append(a.text)

# print(cinema_list)

final_list = []

final_str = ''

# for i in range(0, len(cinema_list)):
#     if '관람가' in cinema_list[i]:
#         num = cinema_list[i].find('관람가')
#         final_list.append('\n')  # 한 영화의 정보를 모두 출력한 다음 개행문자를 삽입.
#         final_list.append('*' + cinema_list[i][num + 3:] + '*' + ':point_right:')  # 영화 제목 삽입부분.
#     elif (('~' in cinema_list[i]) and (i == len(cinema_list) - 1)) :
#         num = cinema_list[i].find('~')  # 시간요소 추출
#         final_list.append(cinema_list[i][:num + 6])  # 시간요소만 삽입. 별도의 처리 X
#     elif (('~' in cinema_list[i]) and (cinema_list[i+1] == '\n')) :  # 시간을 표시하는 원소이면서 리스트의 맨 끝부분일 경우.
#         num = cinema_list[i].find('~')  # 시간요소 추출
#         final_list.append(cinema_list[i][:num + 6])  # 시간요소만 삽입. 별도의 처리 X
#     else:
#         num = cinema_list[i].find('~')
#         final_list.append(cinema_list[i][:num + 6] + '/')


# print(len(cinema_list)-1)

for i in cinema_list :
	# print(i)
	if '관람가' in i :
		num = i.find('관람가')
		final_list.append('\n')
		final_list.append('*' + i[num+3:] + '*' + ':point_right:')
	else:
		num = i.find('~')
		final_list.append(i[:num+6])
		final_list.append('/') # 시간 정표를 final_list에 추가하고, '/' 를 리스트에 추가해줌

final_list.append('') #마지막 슬래쉬를 판별하기위한 공백 리스트


del final_list[0] # 맨앞의 계행 문자를 제거


for i in range(0, len(final_list)-1):
	if final_list[i+1] == '' : #리스트의 맨끝이 ''이면 /를 제거
		final_list[i] = ''
	elif '\n' in final_list[i+1]: #리스트의 다음문자가 계행 문자면 /를 제거
		final_list[i] = ''


for i in final_list: # 리스트를 문자열로 변환 및 띄어쓰기 추가
	final_str += str(i) + ' '


def on_message(ws, message):
    message = json.loads(message)
    if 'type' in message.keys() and message['type'] != 'message':
        return
    if '영화' in message['text']:
        return_msg = {
            'channel': message['channel'],
            'type': 'message',
            'text': final_str  # 위에서 설정한 버스 시간표 텍스트
        }
        ws.send(json.dumps(return_msg))


token = 'xoxb-314380206166-YkkPLCluq4jX7Af363ekkwmJ'
get_url = requests.get('https://slack.com/api/rtm.connect?token=' + token)
print(get_url.json()['url'])
socket_endpoint = get_url.json()['url']
print('Connecting to', socket_endpoint)

websocket.enableTrace(True)
ws = websocket.WebSocketApp(socket_endpoint, on_message=on_message)
ws.run_forever()
