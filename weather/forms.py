from django import forms
from .models import City, Pref


class SearchCityForm(forms.Form):

    city = forms.CharField(label='city', max_length=20)

    class Meta:
        model = City


class ChangePreferenceForm(forms.Form):

    max_wind = forms.IntegerField(widget=forms.NumberInput(
        attrs={'placeholder': Pref.objects.last().max_wind}))
    min_temp = forms.IntegerField(widget=forms.NumberInput(
        attrs={'placeholder': Pref.objects.last().min_temp}))
