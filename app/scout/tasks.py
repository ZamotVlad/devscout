from datetime import timedelta
from django.utils import timezone
from scout.models import Vacancy
from celery import shared_task
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)


@shared_task
def run_dou_parser_task():
    logger.info("Запускаю фоновий парсинг DOU...")
    call_command("parse_dou")
    return "Парсинг DOU успішно завершено!"


@shared_task
def run_djinni_parser_task():
    logger.info("Запускаю фоновий парсинг Djinni...")
    call_command("parse_djinni")
    return "Парсинг Djinni успішно завершено!"


@shared_task
def cleanup_old_vacancies():
    logger.info("Запускаю очищення старих вакансій...")

    threshold_date = timezone.now() - timedelta(days=30)

    deleted_count, _ = Vacancy.objects.filter(pub_date__lte=threshold_date).delete()

    logger.info(f"Прибирання завершено. Видалено записів: {deleted_count}")
    return f"Видалено {deleted_count} старих вакансій."
