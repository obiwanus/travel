from django import forms
from trips.models import Trip


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ('destination', 'start_date', 'end_date', 'user')