from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, HouseHold, Location

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
    location_name = forms.CharField(label='Location Name', max_length=30,
                                    widget=forms.TextInput(
                                        attrs={'class':'form-control', 
                                               'placeholder':'Enter Location Name Here'
                                               })
                                    )
    location_desc = forms.CharField(label='Location Description', max_length=200,
                                    widget=forms.TextInput(attrs={'class':'form-control', 
                                                                  'placeholder': 'Enter description here'
                                                                  })
                                                           )       

LocationFormSet = forms.formset_factory(LocationSetupForm, extra=1)

class DvDForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(DvDForm, self).__init__(*args, **kwargs)
        self.fields["name"] = forms.CharField(label="what the dvd's name?", max_length=200, required=True)
        self.fields["year"] = forms.CharField(label="what year was it released?", required=False)
        self.fields["location"] = forms.ModelChoiceField(label="location", queryset=Location.objects.filter(household__members__id=user.id))
        self.fields["type"] = forms.ChoiceField(label="Its is a ", initial='', choices=[('film', 'film'), ('series', 'series')])


class PickerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # get the list
        possibles = kwargs.pop('possibles')
        super(PickerForm, self).__init__(*args, **kwargs)
        choices = [(item['imdb_id'], "%s, %s" % (item['title'], item['year'])) for item in possibles]
        self.fields["picked"] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
        # todo, move all the sorting and saving here? 

