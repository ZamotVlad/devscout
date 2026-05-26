from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Назва навички")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Навичка"
        verbose_name_plural = "Навички"


class Vacancy(models.Model):
    SOURCE_CHOICES = [
        ("DOU", "DOU.ua"),
        ("DJINNI", "Djinni.co"),
    ]

    FORMAT_CHOICES = [
        ("REMOTE", "Віддалено"),
        ("OFFICE", "Офіс"),
        ("HYBRID", "Гібрид"),
    ]

    EMPLOYMENT_CHOICES = [
        ("FULL", "Повна зайнятість"),
        ("PART", "Неповна зайнятість"),
        ("INTERN", "Стажування/Інтернатура"),
        ("FREELANCE", "Фріланс/Проєкт"),
    ]

    title = models.CharField(max_length=255, verbose_name="Посада")
    company = models.CharField(max_length=255, verbose_name="Компанія")
    url = models.URLField(unique=True, verbose_name="Посилання")
    description = models.TextField(verbose_name="Опис вакансії")

    salary_min = models.IntegerField(null=True, blank=True, verbose_name="ЗП від")
    salary_max = models.IntegerField(null=True, blank=True, verbose_name="ЗП до")

    source = models.CharField(
        max_length=20, choices=SOURCE_CHOICES, verbose_name="Джерело"
    )

    work_format = models.CharField(
        max_length=20,
        choices=FORMAT_CHOICES,
        null=True,
        blank=True,
        verbose_name="Формат роботи",
    )
    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_CHOICES,
        null=True,
        blank=True,
        verbose_name="Тип зайнятості",
    )

    skills = models.ManyToManyField(
        Skill, related_name="vacancies", blank=True, verbose_name="Ключові навички"
    )

    pub_date = models.DateTimeField(verbose_name="Дата публікації")
    created_at = models.DateTimeField(auto_now_add=True)
    is_sent_to_telegram = models.BooleanField(
        default=False, verbose_name="Відправлено в ТГ"
    )

    def __str__(self):
        return f"{self.title} at {self.company}"

    class Meta:
        verbose_name = "Вакансія"
        verbose_name_plural = "Вакансії"
        ordering = ["-pub_date"]
