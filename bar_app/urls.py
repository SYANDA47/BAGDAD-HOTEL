from django.urls import path
from . import views

app_name = 'bar_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('beer-menu/', views.beer_menu, name='beer_menu'),
    path('nyama-choma/', views.nyama_choma_menu, name='nyama_menu'),
    path('reservation/', views.make_reservation, name='reservation'),
]
