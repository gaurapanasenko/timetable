from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import widgets, fields

from suit.widgets import SuitDateWidget

from .settings import *

from .models import (
    FormOfStudySemester,
    Curriculum,
)

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

class CurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum
        widgets = {
            'start_date': SuitDateWidget,
            'end_date': SuitDateWidget,
        }
        exclude = ()
