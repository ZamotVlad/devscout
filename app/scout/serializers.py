from rest_framework import serializers
from .models import Vacancy, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class VacancySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Vacancy
        fields = [
            "id",
            "title",
            "company",
            "url",
            "description",
            "source",
            "work_format",
            "employment_type",
            "skills",
            "pub_date",
        ]
