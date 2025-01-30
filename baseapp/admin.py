from django.contrib import admin
from .models import Position, Question, Option, TestResult

admin.site.register(Position)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(TestResult)