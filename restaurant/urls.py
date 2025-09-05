from django.contrib import admin
from django.urls import path 
from restaurant.views import MenuDetailView ,MenuView,book_show

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu-item/', MenuView.as_view() , name='menu'),
    path('item/<int:pk>/', MenuDetailView.as_view() , name='menu-details'),
    path('book' , book_show, name="book_show"),
]