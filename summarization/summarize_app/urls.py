from django.urls import path
from .views import  DescriptionList, description_detail, DescriptionCreate, get_and_save_description_by_id,\
UpdateDescription, DeleteDescription, summarize_text, create_rating, program_editors, main_page, SummaryList, RatingList, DeleteSummary,\
UpdateSummary
#check_description

urlpatterns = [
    path('main/', main_page, name = 'main_page'),
    # path('main/', check_description),
    path('descriptions/', DescriptionList.as_view(), name = 'description'),
    path('description/<int:pk>', description_detail, name = 'info'),
    path('create_description/',  DescriptionCreate.as_view(), name = 'create_description'),
    path('API/description/',  get_and_save_description_by_id, name = 'get_description'),
    path('description/update/<int:pk>', UpdateDescription.as_view(), name = 'update_description'),
    path("description/delete/<int:pk>", DeleteDescription.as_view(), name = 'delete_description'),
    path('summarize/<int:work_program_id>',  summarize_text, name = 'summarization'),
    path('summarize/', SummaryList.as_view(), name = 'summary'),
    path('summarize/update/<int:pk>', UpdateSummary.as_view(), name = 'update_summary'),
    path("summarize/delete/<int:pk>", DeleteSummary.as_view(), name = 'delete_summary'),
    path('rating/<int:summarization_id>', create_rating, name = 'rating'),
    path('rating/', RatingList.as_view(), name= 'all_rating'),
    path('description/editors/<int:work_program_id>', program_editors, name = 'editors'),
]
