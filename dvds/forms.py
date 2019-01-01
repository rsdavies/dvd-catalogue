from django import forms
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, HouseHold, Location, DvD, Director, Actor, Genre
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, Field
from crispy_forms.bootstrap import FieldWithButtons, StrictButton


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class HouseholdSetupForm(forms.Form):
    household_name = forms.CharField(label="what do you want to call your household?", max_length=30)
 
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
        self.helper=FormHelper()
        self.helper.form_id = 'id_pickerForm'
        self.helper.action = 'post'
        self.helper.layout = Layout(Fieldset('Is it one of these?',
                                              Field('picked'),
                                              Submit('submit', 'Submit')
                                            ))
        self.helper.form_show_labels = False

class SemiRandomForm(forms.Form):
    # give dropdowns of various paramters to randomise by
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")   
        super(SemiRandomForm, self).__init__(*args, **kwargs)
        decade_choices = [('', '--------'),
                            ('2010', '2010s'), ('2000', '2000s'), 
                            ('1990', '90s'), ('1980', '80s'), ('1970', '70s'),
                            ('1960', '60s or earlier')]
        self.fields['era'] = forms.ChoiceField(choices=decade_choices, required=False, label="Decade")

        runtime_choices = [('','--------'),
                            ('60', '1 hour'), ('120', '2 hours'), 
                            ('180', '3 hours'), ('240', '4 hours')]
        self.fields['max_duration'] = forms.ChoiceField(choices=runtime_choices, required=False, label="Maximum Duration")

        rating_choices = [('','---------'),
                            ('2', 'awful'), 
                            ('4', 'mediochre'), 
                            ('6', 'ok'), 
                            ('8', 'great'), 
                            ('10', 'awesome!')]
        self.fields['rating'] = forms.ChoiceField(choices=rating_choices, required=False, label="Rating")

        self.fields['director'] = forms.ModelChoiceField(label='Director', 
                                        queryset=Director.objects.filter(dvd__where_stored__household__members__id=user.id).distinct(),
                                        required=False)

        self.fields['actor'] = forms.ModelChoiceField(label="Actor",
                                        queryset=Actor.objects.filter(dvd__where_stored__household__members__id=user.id).distinct(),
                                        required=False)

        self.fields['genre'] = forms.ModelChoiceField(label="Genre",
                                        queryset=Genre.objects.filter(dvd__where_stored__household__members__id=user.id).distinct(),
                                        required=False)
        self.helper=FormHelper()
        self.helper.form_id = 'id_semiRandomForm'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        # possibly need a reverse in form_action?
        self.helper.form_action = 'filtered_random'
        self.helper.layout = Layout(Fieldset('Narrow down your selection',
                                              Field('era'),
                                              Field('max_duration'),
                                              Field('rating'),
                                              Field('director'),
                                              Field('actor'),
                                              Field('genre'),
                                              ),
                                              Submit('submit', 'submit')
                                              )
        
class SearchForm(forms.Form):
    search_box = forms.CharField(label='Search', required=True)
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper()
        self.helper.form_id = 'id-searchForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'search'
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(Fieldset('Search',
                                    FieldWithButtons(
                                    'search_box', StrictButton("search")))
                                    )
        self.helper.form_show_labels = False
        
class ChooseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ChooseForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper()
        self.helper.form_id = 'id_chooseForm'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(Submit('pick', 'Pick', css_class="choose_submit"))

