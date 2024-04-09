from django.urls import path
from . import views

urlpatterns = [
    path('descriptions/', views.DescriptionList.as_view(), name='description-list'),
    path('descriptions/<int:pk>/', views.DescriptionDetail.as_view(), name='description-detail'),
    path('descriptions/create/', views.DescriptionCreate.as_view(), name='description-create'),
    path('descriptions/update/<int:pk>/', views.UpdateDescription.as_view(), name='description-update'),
    path('descriptions/delete/<int:pk>/', views.DeleteDescription.as_view(), name='description-delete'),
    path('description/api/<int:work_program_id>/', views.get_and_save_description_by_id, name='description-api'),
    path('summarize/<int:work_program_id>/', views.summarize_text, name='summarize-text'),
    path('summaries/', views.SummaryList.as_view(), name='summary-list'),
    path('summaries/update/<int:pk>/', views.UpdateSummary.as_view(), name='summary-update'),
    path('summaries/delete/<int:pk>/', views.DeleteSummary.as_view(), name='summary-delete'),
    path('ratings/create/<int:summarization_id>/', views.create_rating, name='rating-create'),
    path('editors/<int:work_program_id>/', views.program_editors, name='program-editors'),
    path('ratings/', views.RatingList.as_view(), name='rating-list'),
]
