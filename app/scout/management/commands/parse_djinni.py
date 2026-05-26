import requests
from scout.telegram import send_vacancy_to_telegram
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from scout.models import Vacancy
from django.utils import timezone
import xml.etree.ElementTree as ET


class Command(BaseCommand):
    help = "Парсер вакансій Python з Djinni.co (через RSS + Глибока ETL фільтрація)"

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.WARNING("Обходимо Cloudflare через RSS-стрічку...")
        )

        url = "https://djinni.co/jobs/rss/?primary_keyword=Python"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            try:
                root = ET.fromstring(response.content)
                items = root.findall("./channel/item")

                if not items:
                    self.stdout.write(self.style.ERROR("У RSS-стрічці порожньо."))
                    return

                title_stop_words = [
                    "senior",
                    "middle",
                    "lead",
                    "staff",
                    "principal",
                    "architect",
                    "head",
                    "tech lead",
                    "c++",
                    "qa",
                    "aqa",
                    "embedded",
                    "радіоінженер",
                    "data engineer",
                    "ros2",
                    "devops",
                    "hardware",
                ]

                exp_stop_words = [
                    "від 2 років",
                    "від 3 років",
                    "від 4 років",
                    "від 5 років",
                    "2+ роки",
                    "3+ роки",
                    "4+ роки",
                    "5+ років",
                    "2+ years",
                    "3+ years",
                    "4+ years",
                    "5+ years",
                    "2 years of",
                    "3 years of",
                    "4 years of",
                ]

                new_count = 0
                title_filtered = 0
                exp_filtered = 0

                for item in items:
                    title_raw = item.find("title").text
                    if " at " in title_raw:
                        title, company = title_raw.split(" at ", 1)
                    else:
                        title = title_raw
                        company = "Анонімна компанія"

                    title_lower = title.lower()
                    if any(word in title_lower for word in title_stop_words):
                        title_filtered += 1
                        continue

                    html_description = item.find("description").text
                    clean_description = BeautifulSoup(
                        html_description, "html.parser"
                    ).get_text(separator=" | ", strip=True)
                    desc_lower = clean_description.lower()

                    if any(phrase in desc_lower for phrase in exp_stop_words):
                        exp_filtered += 1
                        continue

                    vacancy_url = item.find("link").text

                    vacancy, created = Vacancy.objects.get_or_create(
                        url=vacancy_url,
                        defaults={
                            "title": title.strip(),
                            "company": company.strip(),
                            "description": clean_description[:2000],
                            "source": "DJINNI",
                            "pub_date": timezone.now(),
                        },
                    )

                    if created:
                        new_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"✅ Ідеальний Match: {title[:50]}")
                        )
                        send_vacancy_to_telegram(vacancy)

                self.stdout.write(
                    self.style.WARNING(
                        f"Відфільтровано за назвою (Senior/Не наш профіль): {title_filtered}"
                    )
                )
                self.stdout.write(
                    self.style.WARNING(
                        f"Відфільтровано за досвідом (Приховані сеньйори): {exp_filtered}"
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Готово! Максимально цільових вакансій додано: {new_count}"
                    )
                )

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Помилка обробки: {e}"))
        else:
            self.stdout.write(
                self.style.ERROR(f"Помилка доступу: {response.status_code}")
            )
