# views.py

from django.shortcuts import render
from .models import StandardGuest, SilverGuest, GoldGuest, DiamondGuest

def check_in_view(request, guest_id, nights, guest_type):
    # Dictionary to map guest types to model classes
    guest_classes = {
        'standard': StandardGuest,
        'silver': SilverGuest,
        'gold': GoldGuest,
        'diamond': DiamondGuest,
    }

    # Retrieve the guest from the database based on the guest type
    guest = guest_classes.get(guest_type, StandardGuest).objects.get(pk=guest_id)

    # Create a stay record for the guest
    stay = guest.stays.create(nights=nights)

    # Perform check-in, apply loyalty points, and calculate discount
    guest.check_in(nights)
    discount_percentage = guest.apply_discount()

    # Render the check-in success page
    return render(request, 'check_in_success.html', {'guest': guest, 'stay': stay, 'discount_percentage': discount_percentage})
