import pytest
from django.urls import reverse
from django.utils import timezone
from scout.models import Vacancy


@pytest.mark.django_db
def test_vacancy_list_search_and_filter(client):
    """
    Перевіряє, що пошуковий запит 'q' та фільтр 'source'
    правильно відсікають нерелевантні вакансії у View.
    """
    now = timezone.now()

    Vacancy.objects.create(
        title="Junior Python Developer",
        company="Tech Team",
        url="https://dou.ua/company/test1/",
        description="Шукаємо крутого Django розробника.",
        source="DOU",
        pub_date=now,
    )

    Vacancy.objects.create(
        title="React Engineer",
        company="Web App",
        url="https://djinni.co/q/test2/",
        description="JavaScript розробник на повну зайнятість.",
        source="DJINNI",
        pub_date=now,
    )

    url = reverse("scout:vacancy_list")

    # --- ПЕРЕВІРКА 1: Робота пошуку за ключовим словом 'q' ---
    response_search = client.get(url, {"q": "Python"})
    assert response_search.status_code == 200
    assert response_search.context["total_count"] == 1
    assert "Junior Python Developer" in response_search.content.decode("utf-8")

    # --- ПЕРЕВІРКА 2: Робота фільтра за джерелом 'source' ---
    response_filter = client.get(url, {"source": "DJINNI"})
    assert response_filter.status_code == 200
    assert response_filter.context["total_count"] == 1
    assert "React Engineer" in response_filter.content.decode("utf-8")
