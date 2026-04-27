# Font: Noto Sans
import argparse
import json
import os
from pathlib import Path
import time
from datetime import datetime, timedelta, timezone

CONFIG_PATH = Path(os.environ.get('PARKING_CONFIG_PATH', '.parking_config.json'))
DEFAULT_DEPARTING_AT = os.environ.get('PARKING_DEPARTING_AT', '2026-05-21 07:00')

CAR_COLORS = (
    ("BLACK", "검정"),
    ("WHITE", "흰색"),
    ("SILVER", "은색"),
    ("GRAY", "회색"),
    ("BROWN", "갈색"),
    ("GREEN", "녹색"),
    ("RED", "빨강"),
    ("BLUE", "파랑"),
    ("YELLOW", "노랑"),
    ("PURPLE", "보라"),
    ("WINE", "자주"),
    ("ETC", "기타"),
)

CAR_BRANDS = (
    ("HY", "현대"),
    ("KI", "기아"),
    ("CH", "쉐보레"),
    ("RE", "르노삼성"),
    ("KG", "쌍용"),
    ("GE", "제네시스"),
    ("VE", "벤츠"),
    ("BMW", "BMW"),
    ("AU", "아우디"),
    ("VW", "폭스바겐"),
    ("TO", "도요타"),
    ("LE", "렉서스"),
    ("HO", "혼다"),
    ("MI", "미니"),
    ("FO", "포드"),
    ("FU", "푸조"),
    ("VO", "볼보"),
    ("PO", "포르쉐"),
    ("CA", "캐딜락"),
    ("ZE", "지프"),
    ("LI", "링컨"),
    ("CY", "크라이슬러"),
    ("NI", "닛산"),
    ("IN", "인피니티"),
    ("JA", "재규어"),
    ("LA", "랜드로버"),
    ("CI", "시트로엥"),
    ("FE", "페라리"),
    ("FI", "피아트"),
    ("RO", "롤스로이스"),
    ("MA", "마세라티"),
    ("TE", "테슬라"),
    ("LAM", "람보르기니"),
    ("VEN", "벤틀리"),
    ("ETC", "기타"),
)

AIRLINES = (
    ("KE", "대한항공"),
    ("LJ", "진에어"),
    ("RS", "에어서울"),
    ("BX", "에어부산"),
    ("GA", "가루다인도네시아"),
    ("DL", "델타항공"),
    ("MF", "샤먼항공"),
    ("AF", "에어프랑스"),
    ("KL", "KLM네덜란드항공"),
    ("CI", "중화항공"),
    ("SK", "스칸디나비아항공"),
    ("OZ", "아시아나항공"),
)

DEFAULT_CONFIG = {
    "name": os.environ.get('PARKING_NAME', ''),
    "phone": os.environ.get('PARKING_PHONE', ''),
    "car_number": os.environ.get('PARKING_CAR_NUMBER', ''),
    "car_model": os.environ.get('PARKING_CAR_MODEL', 'NX450h+'),
    "car_color": os.environ.get('PARKING_CAR_COLOR', 'BLACK'),
    "car_brand": os.environ.get('PARKING_CAR_BRAND', 'LE'),
    "check_date": os.environ.get('PARKING_CHECK_DATE', DEFAULT_DEPARTING_AT[:10]),
    "arrived_at": os.environ.get('PARKING_ARRIVED_AT', '2026-05-25 16:30'),
    "departing_at": DEFAULT_DEPARTING_AT,
    "departing_air": os.environ.get('PARKING_DEPARTING_AIR', 'KE'),
}

REQUIRED_FIELDS = (
    "name",
    "phone",
    "car_number",
    "car_model",
    "car_color",
    "car_brand",
    "arrived_at",
    "departing_at",
    "departing_air",
)

SETUP_FIELDS = (
    ("name", "이름"),
    ("phone", "전화번호"),
    ("car_number", "차량번호"),
    ("car_model", "차량 모델"),
    ("car_color", "차량 색상", CAR_COLORS),
    ("car_brand", "차량 브랜드", CAR_BRANDS),
    ("departing_at", "출발 일시(YYYY-MM-DD HH:MM)"),
    ("arrived_at", "도착 일시(YYYY-MM-DD HH:MM)"),
    ("departing_air", "항공사", AIRLINES),
)

DATE_FIELDS = (
    ("departing_at", "출발 일시(YYYY-MM-DD HH:MM)"),
    ("arrived_at", "도착 일시(YYYY-MM-DD HH:MM)"),
)


def parse_interval(value):
    try:
        return max(1, int(value))
    except (TypeError, ValueError):
        return 60


INTERVAL_SECONDS = parse_interval(os.environ.get('PARKING_INTERVAL_SECONDS', '60'))


def log(message):
    print(message, flush=True)


def get_now_str():
    kst = timezone(timedelta(hours=9))
    return datetime.now(kst).strftime('%Y-%m-%d %H:%M:%S')


def load_config(config_path):
    config = DEFAULT_CONFIG.copy()
    if config_path.exists():
        with config_path.open('r', encoding='utf-8') as config_file:
            saved_config = json.load(config_file)
        config.update({key: value for key, value in saved_config.items() if value is not None})
    config["check_date"] = get_check_date(config)
    return config


def save_config(config_path, config):
    config["check_date"] = get_check_date(config)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n",
        encoding='utf-8',
    )
    log(f"[저장] 설정을 {config_path}에 저장했습니다.")


def prompt_value(label, current_value):
    suffix = f" [{current_value}]" if current_value else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or current_value


def get_choice_label(choices, value):
    for choice_value, choice_label in choices:
        if choice_value == value:
            return choice_label
    return value


def prompt_choice(label, current_value, choices):
    current_label = get_choice_label(choices, current_value)
    print(f"{label} 선택 [{current_label or current_value}]")
    for index, (choice_value, choice_label) in enumerate(choices, 1):
        print(f"  {index}. {choice_label} ({choice_value})")

    while True:
        value = input("번호 또는 코드 입력, Enter=유지: ").strip()
        if not value:
            return current_value

        if value.isdigit():
            choice_index = int(value) - 1
            if 0 <= choice_index < len(choices):
                return choices[choice_index][0]

        normalized_value = value.upper()
        if any(choice_value == normalized_value for choice_value, _ in choices):
            return normalized_value

        print("목록의 번호 또는 코드를 입력해주세요.")


def get_check_date(config):
    departing_at = config.get("departing_at", "")
    if len(departing_at) >= 10:
        return departing_at[:10]
    return config.get("check_date", "")


def configure(config_path, fields):
    config = load_config(config_path)
    for field in fields:
        if len(field) == 3:
            key, label, choices = field
            config[key] = prompt_choice(label, config.get(key, ''), choices)
        else:
            key, label = field
            config[key] = prompt_value(label, config.get(key, ''))
    save_config(config_path, config)


def missing_required_fields(config):
    return [field for field in REQUIRED_FIELDS if not config.get(field)]


def reserve_now(now_str, config):
    import requests

    reserve_url = "https://api.amanopark.co.kr/api/web/booking/reservation"
    
    # 시크릿 변수를 활용한 Payload 구성
    payload = {
        "name": config["name"],
        "phone": config["phone"],
        "carType": "BASIC",
        "carNumber": config["car_number"],
        "carModel": config["car_model"],
        "carColor": config["car_color"],
        "carBrand": config["car_brand"],
        "type": "BASIC",
        "arrivedAt": config["arrived_at"],
        "departingAt": config["departing_at"],
        "customerRequest": None,
        "root": "WEB",
        "isUsingCarWash": False,
        "isCrew": False,
        "carWashType": None,
        "departingAir": config["departing_air"]
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json",
        "Origin": "https://valet.amanopark.co.kr",
        "Referer": "https://valet.amanopark.co.kr/"
    }

    try:
        response = requests.post(reserve_url, json=payload, headers=headers, timeout=25)
        if response.status_code == 200:
            log(f"[예약 성공] {now_str} - {config['departing_at']} 예약이 완료되었습니다.")
            return True
        else:
            log(f"[예약 실패] {now_str} - 자리는 났으나 예약 서버 응답 오류: {response.status_code} {response.text}")
    except Exception as e:
        log(f"[예약 오류] {now_str} - 자동 예약 중 오류: {e}")

    return False


def check_and_reserve(config):
    import requests

    now = get_now_str()
    
    check_url = "https://api.amanopark.co.kr/api/web/setting/booking/check"
    params = {"date": config["check_date"], "type": "BASIC"}
    
    try:
        response = requests.get(check_url, params=params, timeout=25)
        response.raise_for_status()
        data = response.json()
        
        if data.get('data') is True:
            log(f"[예약 가능] {now} - {config['check_date']} 예약 가능 상태입니다. 예약을 시도합니다.")
            return reserve_now(now, config)

        log(f"[만차] {now} - {config['check_date']} 아직 예약 가능 상태가 아닙니다.")
    except Exception as e:
        log(f"[조회 오류] {now} - {e}")

    return False


def run_forever(interval_seconds, config):
    log(f"[시작] {config['check_date']} 예약 확인을 {interval_seconds}초 간격으로 반복합니다.")

    while True:
        success = check_and_reserve(config)
        if success:
            log("[중단] 예약 성공으로 반복 실행을 종료합니다.")
            break

        time.sleep(interval_seconds)


def parse_args():
    parser = argparse.ArgumentParser(description="Amano parking reservation monitor")
    parser.add_argument(
        "--config",
        type=Path,
        default=CONFIG_PATH,
        help="설정 파일 경로. 기본값: PARKING_CONFIG_PATH 또는 .parking_config.json",
    )
    parser.add_argument(
        "--setup",
        action="store_true",
        help="예약 정보를 입력받아 설정 파일에 저장합니다.",
    )
    parser.add_argument(
        "--dates",
        action="store_true",
        help="기존 설정에서 날짜/시간 정보만 수정합니다.",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=INTERVAL_SECONDS,
        help="반복 실행 간격(초). 기본값: PARKING_INTERVAL_SECONDS 또는 60",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.setup:
        configure(args.config, SETUP_FIELDS)
        raise SystemExit(0)

    if args.dates:
        configure(args.config, DATE_FIELDS)
        raise SystemExit(0)

    settings = load_config(args.config)
    missing_fields = missing_required_fields(settings)
    if missing_fields:
        log(f"[설정 필요] 누락된 값: {', '.join(missing_fields)}")
        log(f"먼저 실행하세요: python3 parking_monitor.py --setup")
        raise SystemExit(1)

    try:
        run_forever(max(1, args.interval), settings)
    except KeyboardInterrupt:
        log("\n[중단] 사용자 요청으로 종료합니다.")
