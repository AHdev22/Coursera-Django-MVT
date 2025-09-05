from django.contrib import admin
from django.urls import path 
from restaurant.views import MenuDetailView ,MenuView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu-item/', MenuView.as_view() , name='menu'),
    path('item/<int:item_id>', MenuDetailView.as_view() , name='menu-details'),
]