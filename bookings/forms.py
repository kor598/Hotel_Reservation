from django import forms

class AvailabilityForm(forms.Form):
    ROOM_TYPES = (
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('FAMILY', 'Family'),
    )
    
    room_type = forms.ChoiceField(label='Room Type', choices=ROOM_TYPES, required=True)
    check_in = forms.DateTimeField(label='Check In', required=True, input_formats=["%Y-%m-%d%H:%M", ])
    check_out = forms.DateTimeField(label='Check Out', required=True, input_formats=["%Y-%m-%d%H:%M", ])
        