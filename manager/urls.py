from django.urls import path
from . import views

urlpatterns = [
    path('sales/',   views.sales_list,  name='sales_list'),
    path('draw/',    views.run_draw,     name='run_draw'),
    path('winners/', views.winners_list, name='manager_winners'),
]
