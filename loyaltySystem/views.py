# views.py

from django.shortcuts import render
from .models import StandardGuest, SilverGuest, GoldGuest, DiamondGuest

def loyalty_view(request):
    return render(request, 'loyalty.html')