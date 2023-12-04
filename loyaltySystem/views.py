# views.py

from django.shortcuts import render
from .models import LoyaltySystem
from .models import StandardGuest, SilverGuest, GoldGuest, DiamondGuest

def loyalty_view(request):
    # Assuming the user is logged in, get the LoyaltySystem object for the logged-in user
    loyalty_system = LoyaltySystem.objects.get(user=request.user)

    # Pass the relevant data to the template context
    context = {
        'user': request.user,
        'total_points': loyalty_system.total_points,
        'membership_tier': loyalty_system.membership_tier,
    }

    return render(request, 'loyalty.html', context)