from django.urls import path
from . import views

urlpatterns = [
    path('api/reporters/', views.reporters),
    path('api/issues/', views.issues),
]