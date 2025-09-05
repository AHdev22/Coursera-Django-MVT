from django.shortcuts import render
from .models import MenuItem
from django.views import View
# Create your views here.

class MenuView(View):
    def get(self, request):
        menu_items = MenuItem.objects.all()
        return render(request, 'main/menu.html', {'menu_items': menu_items})
