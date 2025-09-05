from django.contrib import admin
from django.urls import path 
import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu-item/', views.MenuView , name='menu-view'),
    path('item/<int:item_id>', views.MenuDetailView , name='menu-details'),
]