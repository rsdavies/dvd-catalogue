from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, HouseHold

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class HouseholdSetupForm(forms.Form):
    household_name = forms.CharField(label="What do you want to call your household?", max_length=30)
 
class LocationSetupForm(forms.Form):
    location_name = forms.CharField(max_length=30)
    location_desc = forms.CharField(max_length=200)       


class DvDForm(forms.Form):
    name = forms.CharField(label="what the dvd's name?", max_length=200, required=True)
    year = forms.CharField(label="what year was it released?", required=False)
    location = forms.CharField(label="where does it live?", max_length=30, required=True)
    type = forms.ChoiceField(label="Its is a ", initial='', choices=[('film', 'film'), ('series', 'series')])
    

class PickerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # get the list
        possibles = kwargs.pop('possibles')
        super(PickerForm, self).__init__(*args, **kwargs)
        choices = [(item['imdb_id'], "%s, %s" % (item['title'], item['year'])) for item in possibles]
        self.fields["picked"] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
        # todo, move all the sorting and saving here? 

