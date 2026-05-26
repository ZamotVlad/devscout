import os
import io
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from django.core.management.base import BaseCommand
from django.core.management import call_command
from scout.models import Vacancy


class Command(BaseCommand):
    help = "Запуск інтерактивного Telegram-бота з фільтрами бази"

    def handle(self, *args, **kwargs):
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        ADMIN_ID = os.environ.get("TELEGRAM_CHAT_ID")

        if not bot_token or not ADMIN_ID:
            self.stdout.write(
                self.style.ERROR("❌ Токен або ID адміністратора не знайдено!")
            )
            return

        bot = telebot.TeleBot(bot_token)
        self.stdout.write(self.style.SUCCESS("🤖 Бот успішно запущений..."))

        @bot.message_handler(commands=["start", "menu"])
        def send_welcome(message):
            if str(message.chat.id) != str(ADMIN_ID):
                bot.send_message(message.chat.id, "⛔ Доступ заборонено.")
                return

            markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.add(
                KeyboardButton("🕷 Спарсити DOU"), KeyboardButton("🦄 Спарсити Djinni")
            )
            markup.add(
                KeyboardButton("📂 Всі вакансії"),
                KeyboardButton("🕷 Тільки DOU"),
                KeyboardButton("🦄 Тільки Djinni"),
            )

            bot.send_message(
                message.chat.id, "Привіт, бос! 🎯 Що робимо?", reply_markup=markup
            )

        def send_vacancies(chat_id, source_filter=None):
            bot.send_message(chat_id, "🔍 Шукаю в базі...")

            if source_filter:
                vacancies = Vacancy.objects.filter(source=source_filter).order_by(
                    "-pub_date"
                )[:15]
            else:
                vacancies = Vacancy.objects.all().order_by("-pub_date")[:15]

            if not vacancies:
                bot.send_message(chat_id, "📭 За цим фільтром вакансій поки немає.")
                return

            bot.send_message(chat_id, f"Ось найсвіжіші ({len(vacancies)} шт):")
            for vac in vacancies:
                text = (
                    f"💼 <b>{vac.title}</b>\n"
                    f"🏢 {vac.company} | 🌐 {vac.get_source_display()}\n"
                    f"🔗 <a href='{vac.url}'>Перейти до вакансії</a>"
                )
                bot.send_message(
                    chat_id, text, parse_mode="HTML", disable_web_page_preview=True
                )

        @bot.message_handler(content_types=["text"])
        def handle_text(message):
            if str(message.chat.id) != str(ADMIN_ID):
                return

            if message.text == "🕷 Спарсити DOU":
                bot.send_message(message.chat.id, "⏳ Запускаю розвідку на DOU...")
                try:
                    out = io.StringIO()
                    call_command("parse_dou", stdout=out, no_color=True)
                    bot.send_message(
                        message.chat.id,
                        f"✅ <b>Звіт DOU:</b>\n<pre>{out.getvalue()}</pre>",
                        parse_mode="HTML",
                    )
                except Exception as e:
                    bot.send_message(message.chat.id, f"❌ Помилка: {e}")

            elif message.text == "🦄 Спарсити Djinni":
                bot.send_message(message.chat.id, "⏳ Обходжу Cloudflare на Djinni...")
                try:
                    out = io.StringIO()
                    call_command("parse_djinni", stdout=out, no_color=True)
                    bot.send_message(
                        message.chat.id,
                        f"✅ <b>Звіт Djinni:</b>\n<pre>{out.getvalue()}</pre>",
                        parse_mode="HTML",
                    )
                except Exception as e:
                    bot.send_message(message.chat.id, f"❌ Помилка: {e}")

            elif message.text == "📂 Всі вакансії":
                send_vacancies(message.chat.id)
            elif message.text == "🕷 Тільки DOU":
                send_vacancies(message.chat.id, source_filter="DOU")
            elif message.text == "🦄 Тільки Djinni":
                send_vacancies(message.chat.id, source_filter="DJINNI")
            else:
                bot.send_message(
                    message.chat.id, "Команда невідома. Використовуй кнопки 👇"
                )

        bot.polling(none_stop=True)
