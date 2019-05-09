from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.admin.sites import site
from django import forms

from suit.widgets import SuitDateWidget

from .models import (
    FormOfStudySemester,
    #~ GroupStream,
    GroupStreamSemester,
    Group,
    CurriculumRecord,
)

#~ class BlogRawIdWidget(widgets.ForeignKeyRawIdWidget):
    #~ def url_parameters(self):
        #~ res = super().url_parameters()
        #~ res['type__exact'] = 'PROJ'
        #~ return res

class FormOfStudySemesterFormset(forms.BaseInlineFormSet):
    def clean(self):
        super(FormOfStudySemesterFormset, self).clean()
        count = 0
        for ik, iv in enumerate(self.forms):
            idr = iv.cleaned_data.get('date_range')
            if idr is not None:
                count += 1
                for jk, jv in enumerate(self.forms[ik+1:]):
                    jdr = jv.cleaned_data.get('date_range')
                    if jdr is not None and idr.are_overlap(jdr):
                        error = _("Date ranges are overlapping.")
                        raise forms.ValidationError(error)
        if count < 1:
            name = FormOfStudySemester._meta.verbose_name
            error = _("You must have at least one {}.")
            raise forms.ValidationError(error)
        elif count > int(self.data['semesters']):
            n1 = FormOfStudySemester._meta.verbose_name_plural
            n2 = self.instance._meta.get_field('semesters').verbose_name
            error = _("You may not have {} more than {}.")
            raise forms.ValidationError(error.format(n1, n2))

class GroupStreamSemesterForm(forms.ModelForm):
    class Meta:
        model = GroupStreamSemester
        widgets = {
            'start_date': SuitDateWidget,
            'end_date': SuitDateWidget,
        }
        exclude = ()

#~ class CurriculumRecordAdminForm(forms.ModelForm):
    #~ def __init__(self, *args, **kwargs):
        #~ super().__init__(*args, **kwargs)
        #~ self.fields['department'].queryset = Blog.objects.filter(type='PROJ')
        #~ print(vars(CurriculumRecord._meta.get_field('group')))
        #~ arg_dict = {
            #~ 'rel': CurriculumRecord._meta.get_field('group').remote_field,
            #~ 'admin_site': site,
        #~ }
        #~ widget = widgets.ForeignKeyRawIdWidget(**arg_dict)
        #~ self.fields['group'].widget = widget

    #~ class Meta:
        #~ fields = '__all__'
        #~ model = CurriculumRecord
