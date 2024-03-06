from django.urls import path
from .views import my_vieww


urlpatterns = [
    path('', my_vieww, name='test'),

]
