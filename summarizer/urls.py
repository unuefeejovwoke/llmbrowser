from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teach-yoruba/', views.teach_yoruba, name='teach_yoruba'),
]
