import requests
from scout.telegram import send_vacancy_to_telegram
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from scout.models import Vacancy
from django.utils import timezone


class Command(BaseCommand):
    help = "Парсер вакансій Python з DOU.ua"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Починаємо збір даних з DOU..."))

        url = "https://jobs.dou.ua/vacancies/?category=Python&exp=0-1"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            vacancies = soup.find_all("li", class_="l-vacancy")

            new_count = 0

            for vac in vacancies:
                title_element = vac.find("a", class_="vt")
                if not title_element:
                    continue

                title = title_element.text.strip()
                vacancy_url = title_element.get("href")

                company_element = vac.find("a", class_="company")
                company = (
                    company_element.text.strip() if company_element else "Не вказано"
                )

                desc_element = vac.find("div", class_="sh-info")
                description = (
                    desc_element.text.strip() if desc_element else "Опис відсутній"
                )

                try:
                    vacancy, created = Vacancy.objects.get_or_create(
                        url=vacancy_url,
                        defaults={
                            "title": title,
                            "company": company,
                            "description": description,
                            "source": "DOU",
                            "pub_date": timezone.now(),
                        },
                    )

                    if created:
                        new_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"✅ Додано в БД: {title}")
                        )
                        send_vacancy_to_telegram(vacancy)
                    else:
                        self.stdout.write(self.style.WARNING(f"ℹ️ Вже є в БД: {title}"))

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"❌ Помилка збереження {title}: {e}")
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"\nГотово! Нових вакансій додано в базу: {new_count}"
                )
            )

        else:
            self.stdout.write(
                self.style.ERROR(f"Помилка доступу: {response.status_code}")
            )
