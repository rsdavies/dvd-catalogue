from django import forms


class DvDForm(forms.Form):
    film_name = forms.CharField(label="what the film's name?", max_length=200, required=True)
    film_year = forms.DateField(label="when was the film released?", input_formats=['%Y-%m-%d'], required=False)
    film_location = forms.CharField(label="where does it live?", max_length=30, required=True)
