from django.db import models

class Position(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название должности")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"

class Question(models.Model):
    text = models.TextField(verbose_name="Текст вопроса")
    explanation = models.TextField(verbose_name="Пояснение к ответу")
    positions = models.ManyToManyField(Position, related_name='questions', verbose_name="Должности")

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options', verbose_name="Вопрос")
    text = models.CharField(max_length=255, verbose_name="Текст варианта")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")

    def __str__(self):
        return f"{self.text} ({'Правильный' if self.is_correct else 'Неправильный'})"

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"

class TestResult(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name="Должность")
    correct_answers = models.IntegerField(verbose_name="Количество правильных ответов")
    total_questions = models.IntegerField(verbose_name="Всего вопросов")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата прохождения")

    def __str__(self):
        return f"{self.full_name} - {self.position} ({self.created_at.strftime('%d.%m.%Y')})"

    class Meta:
        verbose_name = "Результат теста"
        verbose_name_plural = "Результаты тестов"