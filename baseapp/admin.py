# admin.py
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Position, Question, Option, TestResult


class OptionInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        correct_count = 0
        for form in self.forms:
            if form.cleaned_data.get('is_correct'):
                correct_count += 1

        if correct_count != 1:
            raise ValidationError('Должен быть ровно один правильный ответ')


class OptionInline(admin.TabularInline):
    model = Option
    formset = OptionInlineFormSet
    extra = 4
    min_num = 2
    fields = ['text', 'is_correct']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'get_positions', 'get_correct_answer']
    filter_horizontal = ['positions']
    inlines = [OptionInline]

    def get_positions(self, obj):
        return ", ".join([p.name for p in obj.positions.all()])

    get_positions.short_description = 'Должности'

    def get_correct_answer(self, obj):
        try:
            return obj.options.get(is_correct=True).text
        except Option.DoesNotExist:
            return "Не указан"

    get_correct_answer.short_description = 'Правильный ответ'


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position', 'correct_answers', 'total_questions', 'created_at']
    list_filter = ['position', 'created_at']
    search_fields = ['full_name']
    readonly_fields = ['created_at']

    def has_add_permission(self, request):
        return False