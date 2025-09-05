from django.shortcuts import get_object_or_404, render
from .models import MenuItem
from django.views import View
# Create your views here.

class MenuView(View):
    def get(self, request):
        menu_items = MenuItem.objects.all()
        return render(request, 'menu.html', {'menu_items': menu_items})

class MenuDetailView(View):
    def get(self, request, pk):
        item = get_object_or_404(MenuItem, pk=pk)
        return render(request, 'item.html', {'item': item})