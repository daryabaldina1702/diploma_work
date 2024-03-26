from django.shortcuts import render
from .models import Description
from django.http import HttpResponse
from .forms import ProgramIdForm
from django.views.generic import ListView, CreateView
import requests
import json


# функция, которая проверяет, что описание есть в БД
def check_description(request):
    description_exists = None
    if request.method == 'POST':
        form = ProgramIdForm(request.POST)
        if form.is_valid():
            work_program_id = form.cleaned_data['work_program_id']
            try:
                program = Description.objects.get(pk=work_program_id)
                if hasattr(program, 'description_text'):
                    description_exists = True
            except Description.DoesNotExist:
                    description_exists = False
    else:
        form = ProgramIdForm()
    return render(request, 'description_check.html', {'form': form, 'description_exists': description_exists})

# функция, которая выводит все описания
class DescriptionList(ListView):
    model = Description
    template_name = 'list_descriptions.html'

# функция, которая выводит описание по id
def description_detail(request, pk):
    try:
        description = Description.objects.get(work_program_id=pk)
    except Description.DoesNotExist:
        description = None

    return render(request, 'description_detail.html', {'description': description})

# функция, которая добавляет описание
class DescriptionCreate(CreateView):
    model = Description
    fields = ['work_program_id', 'description_text']  # Укажите здесь все поля, которые должны быть в форме
    template_name='create_description.html'
    success_url = '/main'

#функция, которая отдает пользователю описание по ID, а если его нет в БД, то подтягивает описание через API конструктора
def get_and_save_description_by_id(request):
    description_text = None
    if request.method == 'POST':
        description_id = request.POST.get('description_id')
        if description_id == '':
            return render(request, 'description_detail_API.html', {'error_message': 'Вы не указали ID'})
        try:
            description = Description.objects.get(work_program_id=description_id)
            description_text = description.description_text
        except Description.DoesNotExist:
            api_url = 'https://op.itmo.ru/api/workprogram/detail/'
            url = f'{api_url}{description_id}'
            
            auth_url = "https://op.itmo.ru/auth/token/login"
            auth_data = {"username": "analytic", "password": "datatest"}

            # Получение токена авторизации
            try:
                token_txt = requests.post(auth_url, data=auth_data).text
                token = json.loads(token_txt)["auth_token"]
            except requests.exceptions.RequestException as e:
                error_message = f'Error authenticating: {e}'
                return render(request, 'description_detail_API.html', {'error_message': error_message})

            # Формирование заголовков с токеном авторизации
            headers = {'Content-Type': "application/json", 'Authorization': "Token " + token}

            # Выполнение запроса к API с авторизацией
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Проверка на ошибки HTTP
                description_data = response.json()
                description_text = description_data['description']
                print(description_text)
                Description.objects.create(work_program_id=description_id, description_text=description_text)
            except requests.exceptions.RequestException as e:
                return render(request, 'description_detail_API.html', {'error_message': f'Описания для данного ID не существует'})
    
    return render(request, 'description_detail_API.html', {'description': description_text})



# функция, которая собирает статистику по БД
# обновляет описание (руками)
# функция, которая изменяет описание, если оно изменилось по API, а если нет, то оставляет таким же
# удаляет описание по id
# функция, которая выдает реферированные тексты + позволяет добавлять параметры
# функция, которая добавляет оценку тексту
# функция, которая заменяет оригинальный текс описания на реферированный текст