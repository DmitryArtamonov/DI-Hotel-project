from django.shortcuts import render
from .models import RoomCategory

def home_page(request):
    context = {'categories': RoomCategory.objects.all}
    return render(request, 'homepage.html', context)


