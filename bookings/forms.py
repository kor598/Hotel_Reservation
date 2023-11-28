from django import forms

class AvailabilityForm(forms.Form):

    check_in = forms.DateTimeField(label='Check In', required=True, input_formats=["%Y-%m-%d", ])
    check_out = forms.DateTimeField(label='Check Out', required=True, input_formats=["%Y-%m-%d", ])
        