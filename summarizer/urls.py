from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teach-yoruba/', views.teach_yoruba, name='teach_yoruba'),
    path("yoruba-chat/", views.teach_yoruba_chat, name="yoruba_chat"),
    path('summarize-ollama/', views.summarize_ollama, name='summarize_ollama'),
]
