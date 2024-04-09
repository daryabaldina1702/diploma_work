from rest_framework import generics, status
from rest_framework.response import Response
from .models import Description, Summary_text, Rating, Editor
from .forms import SummarizationForm, RatingForm
from rest_framework.decorators import api_view
from transformers import AutoTokenizer, T5ForConditionalGeneration
import requests
import json
from django.shortcuts import redirect
from .serializers import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class DescriptionList(generics.ListAPIView):
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer


class DescriptionDetail(generics.RetrieveAPIView):
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer


class DescriptionCreate(generics.CreateAPIView):
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer


@api_view(['POST'])
def get_and_save_description_by_id(request, work_program_id):
    if request.method == 'POST':
        try:
            description = Description.objects.get(work_program_id=work_program_id)
            serializer = DescriptionSerializer(description)
            return Response(serializer.data)
        except Description.DoesNotExist:
            # Your API logic to fetch description from external source and save it
            api_url = 'https://op.itmo.ru/api/workprogram/detail/'
            url = f'{api_url}{work_program_id}'

            auth_url = "https://op.itmo.ru/auth/token/login"
            auth_data = {"username": "analytic", "password": "datatest"}

            # Получение токена авторизации
            try:
                token_txt = requests.post(auth_url, data=auth_data).text
                token = json.loads(token_txt)["auth_token"]
            except requests.exceptions.RequestException as e:
                error_message = f'Ошибка аутентификации: {e}'
                return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Формирование заголовков с токеном авторизации
            headers = {'Content-Type': "application/json", 'Authorization': "Token " + token}

            # Выполнение запроса к API с авторизацией
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Проверка на ошибки HTTP
                description_data = response.json()
                description_text = description_data.get('description', '')
                # Save description in your database
                Description.objects.create(work_program_id=work_program_id, description_text=description_text)
                return Response({'description': description_text})
            except requests.exceptions.RequestException as e:
                return Response({'error': f'Description for ID {work_program_id} does not exist'},
                                status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Invalid HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UpdateDescription(generics.UpdateAPIView):
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer


class DeleteDescription(generics.DestroyAPIView):
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer


@swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['max_length', 'special_token', 'truncation'],
        properties={
            'max_length': openapi.Schema(type=openapi.TYPE_INTEGER),
            'special_token': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            'truncation': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        }
    ))
@api_view(['POST'])
def summarize_text(request, work_program_id):
    if request.method == 'POST':
        data = request.data
        
        # Полученные гиперпараметры из JSON-запроса
        max_length = data.get('max_length', 600)
        special_token = data.get('special_token', False)
        truncation = data.get('truncation', False)

        # Применяем модель для суммаризации текста
        model_name = "IlyaGusev/rut5_base_headline_gen_telegram"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = T5ForConditionalGeneration.from_pretrained(model_name)

        try:
            description = Description.objects.get(work_program_id=work_program_id)
            description_text = description.description_text
        except Description.DoesNotExist:
            return Response({'error': 'Description not found'}, status=status.HTTP_404_NOT_FOUND)

        input_ids = tokenizer(
            [description_text],
            max_length=max_length,
            add_special_tokens=special_token,
            padding="max_length",
            truncation=truncation,
            return_tensors="pt"
        )["input_ids"]

        output_ids = model.generate(
            input_ids=input_ids
        )[0]

        summary = tokenizer.decode(output_ids, skip_special_tokens=True)

        # Создаем и сохраняем объект Summary_text в базе данных
        summary_object = Summary_text.objects.create(summarize_text=summary, wp_id=description)
        
        return Response({'summary': summary}, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class SummaryList(generics.ListAPIView):
    queryset = Summary_text.objects.all()
    serializer_class = SummaryTextSerializer


class UpdateSummary(generics.UpdateAPIView):
    queryset = Summary_text.objects.all()
    serializer_class = SummaryTextSerializer


class DeleteSummary(generics.DestroyAPIView):
    queryset = Summary_text.objects.all()
    serializer_class = SummaryTextSerializer


@swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['rating_score', 'comment_text', 'author'],
        properties={
            'rating_score': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            'comment_text': openapi.Schema(type=openapi.TYPE_STRING),
            'author': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ))
@api_view(['POST'])
def create_rating(request, summarization_id):
    if request.method == 'POST':
        rating_score = request.data.get('rating_score')
        comment_text = request.data.get('comment_text')
        author = request.data.get('author')

        # Создание объекта рейтинга и сохранение его в базе данных
        Rating.objects.create(
            summarization_id=Summary_text.objects.get(summarization_id=summarization_id),
            rating_score=rating_score,
            comment_text=comment_text,
            author=author
        )
        return Response({'message': 'Rating created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Invalid HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def program_editors(request, work_program_id):
    # Получаем всех редакторов, связанных с данной программой
    editors = Editor.objects.filter(work_program_id=work_program_id)
    serializer = EditorSerializer(editors, many=True)
    return Response(serializer.data)


class RatingList(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
