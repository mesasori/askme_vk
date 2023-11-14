from django.shortcuts import render
from django.core.paginator import Paginator

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'content': f'Long lorem ipsum {i}',
        'like': i + 1,
        'tag': []
    } for i in range(50)
]

for i in range(50):
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
    } for i in range(3)
]


def paginate(objects, request, per_page=10):
    paginator = Paginator(objects, per_page)
    page = request.GET.get('page', 1)
    return paginator.page(page)


# Create your views here.
def index(request):
    return render(request, 'index.html', {'questions': paginate(QUESTIONS, request)})


def question(request, question_id):
    item = QUESTIONS[question_id]
    return render(request, 'question.html', {'question': item, 'answers': ANSWERS})


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')


def hot(request):
    return render(request, 'hot.html', {'questions': paginate(QUESTIONS, request)})


def tag(request, selected_tag):
    questions_list = []
    for item in QUESTIONS:
        if selected_tag in item['tag']:
            questions_list.append(item)
    return render(request, 'tag.html', {'questions': paginate(questions_list, request), 'selected_tag': selected_tag})