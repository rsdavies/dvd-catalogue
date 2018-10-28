from django import forms


class DvDForm(forms.Form):
    film_name = forms.CharField(label="what the dvd's name?", max_length=200, required=True)
    film_year = forms.CharField(label="what year was it released?", required=False)
    film_location = forms.CharField(label="where does it live?", max_length=30, required=True)
    type = forms.ChoiceField(label="Its is a ", initial='', choices=[('film', 'film'), ('series', 'series')])


class PickerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # get the list
        possibles = kwargs.pop('possibles')
        super(PickerForm, self).__init__(*args, **kwargs)
        choices = [(item['imdb_id'], "%s, %s" % (item['title'], item['year'])) for item in possibles]
        self.fields["Which one is it?"] = forms.RadioSelect(choices)


