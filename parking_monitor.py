# Font: Noto Sans
import requests
import os
from datetime import datetime, timedelta, timezone

# 깃허브 시크릿에서 정보 가져오기
BOT_TOKEN = os.environ.get('PARKING_BOT_TOKEN')
MY_CHAT_ID = os.environ.get('PARKING_CHAT_ID')

# 개인정보 시크릿 가져오기
USER_NAME = os.environ.get('PARKING_NAME')
USER_PHONE = os.environ.get('PARKING_PHONE')
USER_CAR_NUM = os.environ.get('PARKING_CAR_NUMBER')

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": MY_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def reserve_now(now_str):
    reserve_url = "https://api.amanopark.co.kr/api/web/booking/reservation"
    
    # 시크릿 변수를 활용한 Payload 구성
    payload = {
        "name": USER_NAME,
        "phone": USER_PHONE,
        "carType": "BASIC",
        "carNumber": USER_CAR_NUM,
        "carModel": "NX450h+",
        "carColor": "BLACK",
        "carBrand": "LE",
        "type": "BASIC",
        "arrivedAt": "2026-05-21 07:00", 
        "departingAt": "2026-05-25 16:30",
        "customerRequest": None,
        "root": "WEB",
        "isUsingCarWash": False,
        "isCrew": False,
        "carWashType": None,
        "departingAir": "KE"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json",
        "Origin": "https://valet.amanopark.co.kr",
        "Referer": "https://valet.amanopark.co.kr/"
    }

    try:
        response = requests.post(reserve_url, json=payload, headers=headers)
        if response.status_code == 200:
            send_alert(f"✅ **[자동 예약 성공!]**\n{now_str}에 5월 21일 예약이 완료되었습니다!")
        else:
            send_alert(f"⚠️ [예약 시도 실패] 자리는 났으나 예약 서버 응답 오류: {response.text}")
    except Exception as e:
        send_alert(f"❌ [에러] 자동 예약 중 오류: {str(e)}")

def check_and_reserve():
    kst = timezone(timedelta(hours=9))
    now = datetime.now(kst).strftime('%Y-%m-%d %H:%M:%S')
    
    check_url = "https://api.amanopark.co.kr/api/web/setting/booking/check"
    params = {"date": "2026-05-25", "type": "BASIC"}
    
    try:
        response = requests.get(check_url, params=params)
        data = response.json()
        
        if data.get('data') is True:
            reserve_now(now)
        else:
            # 알림이 너무 잦으면 아래 줄을 주석 처리하세요
            send_alert(f"ℹ️ [상태 보고] {now} 현재 아직 만차입니다.")
            print(f"{now} - 아직 만차")
    except Exception as e:
        print(f"조회 중 오류: {e}")

if __name__ == "__main__":
    check_and_reserve()
