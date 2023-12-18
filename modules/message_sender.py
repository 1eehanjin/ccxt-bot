import requests

def send_telegram_message(text):
    token = "6665278737:AAGsegi1k9y3YBJUU1nraG1z3v6ft7KzKww"
    chat_id = "1322161937"  # 메시지를 받을 채팅 대상의 ID

    text = str(text)
    base_url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": text
    }

    response = requests.post(base_url, params=params)

    if response.status_code == 200:
        print("메시지 전송: " + text)
    else:
        print("메시지 전송에 실패했습니다.")