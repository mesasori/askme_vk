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
    if int(page) > pages_count(len(objects)):
        page = 1
    return [paginator.page(page), int(page)]


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
    count = pages_count(len(ANSWERS))
    current_page = arr_paginate[1]
    paginator_items = get_paginator(current_page, count)
    return render(request, 'question.html',
                  {
                      'question': item,
                      'answers': arr_paginate[0],
                      'current_page': current_page,
                      'pages_count': count,
                      'paginator': paginator_items})


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')


def hot(request):
    return render(request, 'hot.html', {'questions': paginate(QUESTIONS, request)})


def index(request):
    arr_paginate = paginate(QUESTIONS, request)
    count = pages_count(len(QUESTIONS))
    current_page = arr_paginate[1]
    paginator_items = get_paginator(current_page, count)
    return render(request, 'index.html',
                  {
                      'questions': arr_paginate[0],
                      'current_page': current_page,
                      'pages_count': count,
                      'paginator': paginator_items
                  })


def tag(request, selected_tag):
    questions_list = []
    for item in QUESTIONS:
        if selected_tag in item['tag']:
            questions_list.append(item)

    count = pages_count(len(questions_list))
    arr_paginate = paginate(questions_list, request)
    current_page = arr_paginate[1]
    paginator_items = get_paginator(current_page, count)
    return render(request, 'tag.html',
                  {
                      'questions': paginate(questions_list, request)[0],
                      'selected_tag': selected_tag,
                      'current_page': current_page,
                      'pages_count': count,
                      'paginator': paginator_items}
                  )
