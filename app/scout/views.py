from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import redirect
from .tasks import run_dou_parser_task, run_djinni_parser_task
from .models import Vacancy


def vacancy_list(request):
    source_filter = request.GET.get("source")
    search_query = request.GET.get("q")

    vacancies = Vacancy.objects.all()

    if source_filter:
        vacancies = vacancies.filter(source=source_filter)

    if search_query:
        vacancies = vacancies.filter(title__icontains=search_query) | vacancies.filter(
            description__icontains=search_query
        )

    vacancies = vacancies.order_by("-pub_date").distinct()
    total_count = vacancies.count()

    paginator = Paginator(vacancies, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "current_source": source_filter,
        "search_query": search_query,
        "total_count": total_count,
    }
    return render(request, "scout/vacancy_list.html", context)

def trigger_parser_view(request, site_name):
    if not request.user.is_staff:
        messages.error(request, "⛔ Доступ заборонено!")
        return redirect("scout:vacancy_list")

    if site_name == "dou":
        run_dou_parser_task.delay()
        messages.success(
            request, "🚀 Фоновий парсер DOU успішно запущено через Celery!"
        )
    elif site_name == "djinni":
        run_djinni_parser_task.delay()
        messages.success(
            request, "🚀 Фоновий парсер Djinni успішно запущено через Celery!"
        )

    return redirect("scout:vacancy_list")
