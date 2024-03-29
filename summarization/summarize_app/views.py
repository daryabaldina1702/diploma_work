from django.shortcuts import render, get_object_or_404
from .models import Description, Summary_text, Rating, Editor
from django.http import HttpResponse
from .forms import ProgramIdForm, SummarizationForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
import requests
import json
from transformers import AutoTokenizer, T5ForConditionalGeneration



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

# обновляет описание (руками)
class UpdateDescription(UpdateView):
    model = Description
    fields = ['description_text']
    template_name = 'update_description.html'
    success_url = '/main'

# удаляет описание по id
class DeleteDescription(DeleteView):
    model = Description
    template_name = 'del_description.html'
    success_url = '/main'

# функция, которая выдает реферированные тексты + позволяет добавлять параметры
def summarize_text(request):
    summary = None
    description_text = None
    if request.method == 'POST':
        form = SummarizationForm(request.POST) 
        if form.is_valid():
            #полученные гиперпараметры из формы
            max_length_from_user = form.cleaned_data['max_length']
            special_token = form.cleaned_data['special_token']
            truncation_from_user = form.cleaned_data['truncation']
            
            # Получаем ID описания из формы
            description_id = form.cleaned_data['description_id']

            try:
                #проверяем, есть ли в базе реферированный текст
                sum_description = Summary_text.objects.get(wp_id=description_id)
                summary = sum_description.summirize_text
            except Summary_text.DoesNotExist:
                # Применяем модель для суммаризации текста
                model_name = "IlyaGusev/rut5_base_headline_gen_telegram"
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = T5ForConditionalGeneration.from_pretrained(model_name)

                #гиперпараметры
                max_length= max_length_from_user if max_length_from_user else 600
                add_special_tokens = True if special_token else False
                truncation = True if truncation_from_user else False
                
                #достаем описание 
                try:
                    description = Description.objects.get(work_program_id=description_id)
                    description_text = description.description_text
                except Description.DoesNotExist:
                    return render(request, 'summarization.html', {'form': form,'error_msg': 'Описания не существует'})

                input_ids = tokenizer(
                    [description_text],
                    max_length=max_length,
                    add_special_tokens=add_special_tokens,
                    padding="max_length",
                    truncation=truncation,
                    return_tensors="pt"
                )["input_ids"]

                output_ids = model.generate(
                    input_ids=input_ids
                )[0]

                summary = tokenizer.decode(output_ids, skip_special_tokens=True)

                # Создаем и сохраняем объект Summary_text в базу данных
                summary_object = Summary_text(summarize_text=summary, wp_id = description)
                summary_object.save()

    else:
        form = SummarizationForm()

    return render(request, 'summarization.html', {'form': form,'summary': summary})

#функция, которая обновляет аннотированный текст
class UpdateSummary(UpdateView):
    model = Summary_text
    fields = ['summarize_text']
    template_name = 'update_summary.html'
    success_url = '/main'

# функция, которая удаляет аннотированный текст
class DeleteSummary(DeleteView):
    model = Summary_text
    template_name = 'del_summary.html'
    success_url = '/main'

# функция, которая добавляет оценку тексту
class RatingCreateView(CreateView):
    model = Rating
    fields = ['summarization_id', 'rating_score', 'comment_text', 'author']
    template_name = 'create_comment.html'
    success_url = '/main'

# функция, которая позволяет просматривать редакторов описания
def program_editors(request, work_program_id):
    # Получаем объект программы работы по ее ID или отображаем ошибку 404, если программа не найдена
    program = get_object_or_404(Description, pk=work_program_id)
    
    # Получаем всех редакторов, связанных с данной программой
    editors = Editor.objects.filter(work_program_id=program)
    
    # Отображаем страницу с информацией о редакторах программы
    return render(request, 'editors.html', {'editors': editors})



# функция, которая изменяет описание, если оно изменилось по API, а если нет, то оставляет таким же
# функция, которая заменяет оригинальный текст описания на реферированный текст