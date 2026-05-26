import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="highlight_skills")
def highlight_skills(text):
    if not text:
        return ""

    skills = [
        "Python",
        "Django",
        "FastAPI",
        "Flask",
        "Celery",
        "Redis",
        "PostgreSQL",
        "SQL",
        "Docker",
        "Docker Compose",
        "REST API",
        "Git",
        "GitLab",
        "Linux",
        "AIOHTTP",
    ]

    highlighted = text
    for skill in skills:
        pattern = re.compile(rf"\b({re.escape(skill)})\b", re.IGNORECASE)
        highlighted = pattern.sub(
            r'<strong class="text-primary">\1</strong>', highlighted
        )

    return mark_safe(highlighted)
