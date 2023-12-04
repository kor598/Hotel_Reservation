from django import forms

# Create your forms here.
# check in and check out dates
class AvailabilityForm(forms.Form):

    check_in_date = forms.DateTimeField(label='Check In', required=True, input_formats=["%Y-%m-%d", ])
    check_out_date = forms.DateTimeField(label='Check Out', required=True, input_formats=["%Y-%m-%d", ])
        