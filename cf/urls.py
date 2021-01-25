from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from cf import views

app_name = 'cf'
urlpatterns = [
    path('add_handle/', csrf_exempt(views.add_handle), name='add_handle'),
    path('add_problem/', csrf_exempt(views.add_problem), name='add_problem'),
    path('add_problems/', csrf_exempt(views.add_problems), name='add_problems'),
    path('get_list/start=<int:start>end=<int:end>/', views.get_list, name='get_list')
]
