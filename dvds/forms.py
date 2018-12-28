from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, HouseHold, Location, DvD, Director, Actor, Genre

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
    def __init__(self, *args, **kwargs):
        user=kwargs.pop('user')
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


class SearchResultsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # get the search results
        results = kwargs.pop('results')
        super(SearchResultsForm, self).__init__(*args, **kwargs)
        choices = [(item.id, item.name) for item in results]
        self.fields["picked"] = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)


class SemiRandomForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # give dropdowns of various paramters to randomise by
        user = kwargs.pop("user")
        super(SemiRandomForm, self).__init__(*args, **kwargs)
        decade_choices = [('', '--------'),
                          ('2010', '2010s'), ('2000', '2000s'), 
                          ('1990', '90s'), ('1980', '80s'), ('1970', '70s'),
                          ('1960', '60s or earlier')]
        self.fields["era"] = forms.ChoiceField(choices=decade_choices, required=False, label="Decade")

        runtime_choices = [('','--------'),
                           ('60', '1 hour'), ('120', '2 hours'), 
                           ('180', '3 hours'), ('240', '4 hours')]
        self.fields["max_duration"] = forms.ChoiceField(choices=runtime_choices, required=False, label="Maximum Duration")

        rating_choices = [('','---------'),
                          ('2', 'Awful'), 
                          ('4', 'Mediochre'), 
                          ('6', 'Ok'), 
                          ('8', 'Great'), 
                          ('10', 'Awesome!')]
        self.fields["rating"] = forms.ChoiceField(choices=rating_choices, required=False, label="Rating")

        self.fields['director'] = forms.ModelChoiceField(label='Director', 
                                                         queryset=Director.objects.filter(dvd__where_stored__household__members__id=user.id),
                                                         required=False)

        self.fields['actor'] = forms.ModelChoiceField(label="Actor",
                                                      queryset=Actor.objects.filter(dvd__where_stored__household__members__id=user.id),
                                                      required=False)

        self.fields['genre'] = forms.ModelChoiceField(label="Genre",
                                                      queryset=Genre.objects.filter(dvd__where_stored__household__members__id=user.id),
                                                      required=False)
