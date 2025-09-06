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




def reservation_page(request):
    date = None

    if request.method == "POST":
        # Create a reservation
        date = request.POST.get("date")
        time = request.POST.get("time")

        if date and time:
            Reservation.objects.create(
                user=request.user,
                date=date,
                time=time,
            )
        # after saving, we still want to show reservations for the same date

    else:
        # GET request
        date = request.GET.get("date")

    # If a date is chosen (either POST or GET), show reservations
    reservations = None
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