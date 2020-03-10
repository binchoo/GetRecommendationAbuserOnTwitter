from django.urls import path, include
from . import views

urlpatterns = [
    path('directives/', views.get_directives_fast),
    path('directives-test/', views.get_directives_slow)
]
