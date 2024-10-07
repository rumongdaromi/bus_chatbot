from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('your-api-endpoint/',views.message_api, name='message_api'),
]