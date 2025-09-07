from django.shortcuts import get_object_or_404, render,redirect
from .models import MenuItem,Reservation
from django.views import View
from django.contrib.auth.decorators import login_required
# Create your views here.

class MenuView(View):
    def get(self, request):
        menu = MenuItem.objects.all()
        return render(request, 'menu.html', {'menu': menu})

class MenuDetailView(View):
    def get(self, request, pk):
        item = get_object_or_404(MenuItem, pk=pk)
        return render(request, 'item.html', {'item': item})
    
def book_show(request):
    return render(request,"book.html")

def about_show(request):
    return render(request,"About.html")

def home_show(request):
    return render(request,"Home.html")




from datetime import datetime

from django.contrib import messages
from datetime import datetime

def reservation_page(request):
    date = None
    reservations = None

    if request.method == "POST":
        date = request.POST.get("date")
        time = request.POST.get("time")

        if date and time:
            try:
                # Convert both "1:30 PM" and "13:30"
                try:
                    time_obj = datetime.strptime(time, "%I:%M %p").time()
                except ValueError:
                    time_obj = datetime.strptime(time, "%H:%M").time()

                # 🔹 check if this slot is already taken
                exists = Reservation.objects.filter(date=date, time=time_obj).exists()
                if exists:
                    messages.error(request, "This time slot is already reserved!")
                else:
                    Reservation.objects.create(
                        user=request.user,
                        date=date,
                        time=time_obj,
                    )
                    messages.success(request, "Reservation created successfully!")

            except ValueError:
                messages.error(request, "Invalid time format.")

    else:
        date = request.GET.get("date")

    if date:
        reservations = (
            Reservation.objects.filter(date=date)
            .select_related("user")
            .order_by("time")
        )

    return render(
        request,
        "reservation.html",
        {"reservations": reservations, "date": date},
    )
