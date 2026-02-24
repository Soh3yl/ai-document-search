from django.urls import path
from . import views

urlpatterns = [
    path('api/search/', views.search_documents_api, name='api_search_documents'),
]