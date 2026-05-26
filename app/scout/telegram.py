import os
import requests


def send_vacancy_to_telegram(vacancy):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("⚠️ Ключі Telegram не знайдені в змінних оточення.")
        return False

    text = (
        f"🚀 <b>Нова цільова вакансія!</b>\n\n"
        f"💼 <b>Посада:</b> {vacancy.title}\n"
        f"🏢 <b>Компанія:</b> {vacancy.company}\n"
        f"🌐 <b>Джерело:</b> {vacancy.get_source_display()}\n\n"
        f"🔗 <a href='{vacancy.url}'>Перейти до вакансії</a>"
    )

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }

    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Помилка відправки в Telegram: {e}")
        return False
