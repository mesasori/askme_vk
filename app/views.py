from django.shortcuts import render
from django.core.paginator import Paginator
import math

PER_PAGE = 10

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'content': f'Long lorem ipsum {i}',
        'like': i + 1,
        'tag': []
    } for i in range(1000)
]

for i in range(1000):
    if i % 2 == 0:
        QUESTIONS[i]['tag'] = ['CSS', 'HTML']
    else:
        QUESTIONS[i]['tag'] = ['Python', 'Django']
    if i % 3 == 0:
        QUESTIONS[i]['tag'] = ['JavaScript', 'Voloshin', 'bender']

ANSWERS = [
    {
        'id': i,
        'content': f'Long lorem ipsum long lorem ipsum long lorem ipsum {i}',
        'like': i + 1
    } for i in range(1000)
]


def paginate(objects, request, per_page=PER_PAGE):
    paginator = Paginator(objects, per_page)
    page = request.GET.get('page', 1)


    count = pages_count(len(objects))
    paginator_items = get_paginator(int(page), count)

    return [paginator.page(page), int(page), count, paginator_items]


def pages_count(objects, per_page=PER_PAGE):
    return math.ceil(objects / per_page)


def get_paginator(current_page, count):
    start_page = max(current_page - 4, 1)
    end_page = min(current_page + 4, count)
    arr = [i for i in range(start_page, end_page + 1)]
    return arr


def question(request, question_id):
    item = QUESTIONS[question_id]
    arr_paginate = paginate(ANSWERS, request)

    return render(request, 'question.html',
                  {
                      'question': item,
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


def hot(request):
    arr_paginate = paginate(QUESTIONS, request)
    return render(request, 'hot.html', {'questions': arr_paginate[0]})


def index(request):
    arr_paginate = paginate(QUESTIONS, request)

    return render(request, 'index.html',
                  {
                      'questions': arr_paginate[0],
                      'current_page': arr_paginate[1],
                      'pages_count': arr_paginate[2],
                      'paginator': arr_paginate[3]
                  })


def tag(request, selected_tag):
    questions_list = []
    for item in QUESTIONS:
        if selected_tag in item['tag']:
            questions_list.append(item)

    arr_paginate = paginate(questions_list, request)
    return render(request, 'tag.html',
                  {
                      'questions': arr_paginate[0],
                      'selected_tag': selected_tag,
                      'current_page': arr_paginate[1],
                      'pages_count': arr_paginate[2],
                      'paginator': arr_paginate[3]}
                  )
