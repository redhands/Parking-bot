# Font: Noto Sans
import requests
import os
from datetime import datetime

# 깃허브 시크릿 설정
BOT_TOKEN = os.environ.get('PARKING_BOT_TOKEN')
MY_CHAT_ID = os.environ.get('PARKING_CHAT_ID')

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": MY_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"텔레그램 전송 에러: {e}")

def check_parking():
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # 성백님이 찾으신 직통 API 주소
    api_url = "https://api.amanopark.co.kr/api/web/setting/booking/check"
    params = {
        "date": "2026-05-21",
        "type": "BASIC"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Origin": "https://valet.amanopark.co.kr",
        "Referer": "https://valet.amanopark.co.kr/"
    }

    try:
        response = requests.get(api_url, params=params, headers=headers)
        data = response.json() # 결과 예: {"data": false}
        
        # 서버 응답에서 'data' 값이 true인지 확인
        is_available = data.get('data', False)

        if is_available:
            msg = f"🚨 **[주차대행 자리 발생!]**\n성백님, 5월 21일 예약이 가능합니다!\n지금 즉시 예약하세요: https://valet.amanopark.co.kr/booking"
            send_alert(msg)
            print(f"{now} - 자리가 났습니다! 알림 전송 완료.")
        else:
            # 자리가 없을 때도 보고 (성백님 요청사항)
            msg = f"ℹ️ [파킹봇 상태 보고]\n조회 시간: {now}\n5월 21일은 아직 **만차**입니다. 계속 감시할게요!"
            send_alert(msg)
            print(f"{now} - 아직 만차입니다.")

    except Exception as e:
        error_msg = f"❌ [파킹봇 오류]\n데이터를 가져오지 못했습니다: {str(e)}"
        send_alert(error_msg)
        print(error_msg)

if __name__ == "__main__":
    check_parking()
