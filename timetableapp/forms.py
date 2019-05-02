from django import forms

from .models import Faculty, Department, Subject

#~ class SubjectForm(forms.ModelForm):
    #~ department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.TextInput)
        #~ bar = forms.ModelChoiceField(queryset=Bar.all_objects,
            #~ label=_("Bar"),
            #~ widget=widgets.ForeignKeyRawIdWidget(
                #~ RelWrapper(Foo._meta.get_field('bar').rel,
#~ Bar.all_objects)))

    #~ class Meta:
        #~ model = Subject
        #~ fields = ('name', 'department',)
