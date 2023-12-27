from django.shortcuts import render
from django.core.paginator import Paginator
from app import models

PER_PAGE = 10


def paginate(objects, request, per_page=PER_PAGE):
    paginator = Paginator(objects, per_page)
    page = int(request.GET.get('page', 1))
    count = paginator.num_pages

    try:
        if page <= 0:
            page = 1
        elif page > count:
            page = count
    except:
        page = 1

    paginator_elements = [i for i in range(max(page - 4, 2), min(page + 4, count) + 1)]

    return [paginator.page(page), page, count, paginator_elements]


def question(request, question_id):
    question_item = models.Question.objects.get_by_id(question_id)
    arr_paginate = paginate(
        models.Answer.objects.get_by_question(question_id),
        request)

    return render(request, 'question.html',
                  {
                      'question': question_item,
                      'answers': arr_paginate[0],
                      'current_page': arr_paginate[1],
                      'pages_count': arr_paginate[2],
                      'paginator': arr_paginate[3]})


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
    return render(request, 'hot.html',
                  {
                      'questions': arr_paginate[0],
                      'current_page': arr_paginate[1],
                      'pages_count': arr_paginate[2],
                      'paginator': arr_paginate[3]
                  })


def index(request):
    arr_paginate = paginate(
        models.Question.objects.get_new(),
        request)

    return render(request, 'index.html',
                  {
                      'questions': arr_paginate[0],
                      'current_page': arr_paginate[1],
                      'pages_count': arr_paginate[2],
                      'paginator': arr_paginate[3]
                  })


def tag(request, tag_title):
    arr_paginate = paginate(
        models.Question.objects.get_by_tag(tag_title),
        request)
    return render(request, 'tag.html',
                  {
                      'questions': arr_paginate[0],
                      'selected_tag': tag_title,
                      'current_page': arr_paginate[1],
                      'pages_count': arr_paginate[2],
                      'paginator': arr_paginate[3]}
                  )
