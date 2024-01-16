from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.core.paginator import Paginator
from app import models

PER_PAGE = 20


def paginate(objects, request, per_page=PER_PAGE):
    paginator = Paginator(list(objects), per_page)
    page = int(request.GET.get('page', 1))
    count = paginator.num_pages

    try:
        if page <= 0:
            page = 1
        elif page > count:
            page = count
    except:
        page = 1

    paginator_elements = [i for i in range(max(page - 4, 1), min(page + 4, count) + 1)]

    return [paginator.page(page), page, count, paginator_elements]


def question(request, question_id):
    question_item = models.Question.objects.get_by_id(question_id)
    arr_paginate = paginate(
        models.Answer.objects.get_by_question(question_id),
        request
    )

    context = {
        'question': question_item,
        'answers': arr_paginate[0],
        'tags': models.Tag.objects.get_popular(),
        'current_page': arr_paginate[1],
        'pages_count': arr_paginate[2],
        'paginator': arr_paginate[3]
    }

    return render(request, 'question.html', context=context)


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')


def hot(request):
    arr_paginate = paginate(
        models.Question.objects.get_hot(),
        request)

    answers = models.Answer.objects.get_count_by_questions(arr_paginate[0])

    context = {
        'questions': arr_paginate[0],
        'tags': models.Tag.objects.get_popular(),
        'answers': answers,
        'current_page': arr_paginate[1],
        'pages_count': arr_paginate[2],
        'paginator': arr_paginate[3]
    }

    return render(request, 'hot.html', context=context)


def index(request):
    arr_paginate = paginate(
        models.Question.objects.get_new(),
        request)

    answers = models.Answer.objects.get_count_by_questions(arr_paginate[0])

    context = {
        'questions': arr_paginate[0],
        'tags': models.Tag.objects.get_popular(),
        'answers': answers,
        'current_page': arr_paginate[1],
        'pages_count': arr_paginate[2],
        'paginator': arr_paginate[3]
    }

    return render(request, 'index.html', context=context)


def tag(request, selected_tag):
    questions = models.Question.objects.get_by_tag(selected_tag)

    arr_paginate = paginate(
        questions,
        request)

    context = {
        'questions': arr_paginate[0],
        'selected_tag': selected_tag,
        'tags': models.Tag.objects.get_popular(),
        'current_page': arr_paginate[1],
        'pages_count': arr_paginate[2],
        'paginator': arr_paginate[3]
    }

    return render(request, 'tag.html', context=context)


def page_404(req, exc):
    return HttpResponseNotFound('<h1> Page not found :( </h1>')
