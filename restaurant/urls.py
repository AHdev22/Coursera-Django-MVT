from django.contrib import admin
from django.urls import path 
from restaurant.views import MenuDetailView ,MenuView,book_show, about_show,home_show,reservation_page
urlpatterns = [
    path('menu-item/', MenuView.as_view() , name='menu'),
    path('item/<int:pk>/', MenuDetailView.as_view() , name='menu-details'),
    path('book/' , book_show, name="book_show"),
    path('about/' , about_show, name="about_show"),
    path('home/' , home_show, name="home_show"),
    path("reservations/", reservation_page, name="reservation_page"),
]