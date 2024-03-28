from django.urls import path
from .views import check_description, DescriptionList, description_detail, DescriptionCreate, get_and_save_description_by_id,\
UpdateDescription, DeleteDescription, summarize_text

urlpatterns = [
    path('main/', check_description),
    path('descriptions/', DescriptionList.as_view()),
    path('description/<int:pk>', description_detail),
    path('create_description/',  DescriptionCreate.as_view()),
    path('API/description/',  get_and_save_description_by_id),
    path('description/update/<int:pk>', UpdateDescription.as_view()),
    path("description/delete/<int:pk>", DeleteDescription.as_view()),
    path('summarize/',  summarize_text)
]
