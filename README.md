# Parking-bot

## 웹페이지에서 실행

`index.html`을 브라우저에서 열고 필요한 값을 입력한 뒤 시작 버튼을 누르면, 해당 탭이 열려 있는 동안 JavaScript가 정해진 간격으로 Amano API를 직접 호출합니다.

브라우저 보안 정책 때문에 대상 API가 CORS를 허용하지 않으면 정적 웹페이지에서는 직접 호출이 차단될 수 있습니다. 이 경우에는 서버 또는 브라우저 확장/자동화 방식이 필요합니다.

## Python으로 반복 실행

처음 한 번은 예약 정보를 입력해서 설정 파일에 저장합니다. 차량 색상, 차량 브랜드, 항공사는 표시되는 목록에서 번호 또는 코드로 선택할 수 있습니다.

```bash
python3 parking_monitor.py --setup
```

입력한 값은 기본적으로 `.parking_config.json`에 저장됩니다. 다른 경로를 쓰려면 `--config`를 지정합니다.

```bash
python3 parking_monitor.py --config my_config.json --setup
```

이후에는 저장된 설정을 재사용해 반복 실행합니다.

```bash
python3 parking_monitor.py --interval 60
```

`--interval` 값은 초 단위입니다. 옵션을 생략하면 `PARKING_INTERVAL_SECONDS` 환경변수 또는 기본값 60초를 사용합니다.

일시 정보만 바꿀 때는 아래 명령을 사용합니다. 이름, 전화번호, 차량 정보, 항공사는 그대로 두고 출발 일시와 도착 일시만 다시 입력합니다.

```bash
python3 parking_monitor.py --dates
```

확인 날짜는 따로 입력하지 않고 출발 일시의 날짜를 자동으로 사용합니다. 예를 들어 출발 일시가 `2026-05-23 08:20`이면 확인 날짜는 `2026-05-23`으로 저장됩니다.

기본 설정 파일은 `.parking_config.json`이며, 개인정보가 들어갈 수 있어 git에는 포함하지 않습니다.
