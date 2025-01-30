from django.shortcuts import render
from django.http import JsonResponse
from baseapp.models import Position, Question, Option, TestResult
import json


def index(request):
    positions = Position.objects.all()
    return render(request, 'testing/index.html', {'positions': positions})


def get_questions(request):
    position_id = request.GET.get('position_id')
    questions = Question.objects.filter(positions__id=position_id).prefetch_related('options')

    questions_data = []
    for question in questions:
        options = [{'id': opt.id, 'text': opt.text} for opt in question.options.all()]
        correct_answer = question.options.get(is_correct=True).text

        questions_data.append({
            'id': question.id,
            'text': question.text,
            'options': [opt['text'] for opt in options],
            'correctAnswer': correct_answer,
            'explanation': question.explanation
        })

    return JsonResponse({'questions': questions_data})


def save_result(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        result = TestResult.objects.create(
            full_name=data['fullName'],
            position_id=data['position'],
            correct_answers=data['correct'],
            total_questions=data['total']
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)