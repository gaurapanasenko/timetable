from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import Exists
from django.apps import apps
from django.core.exceptions import ValidationError

class PositiveTinyIntegerField(models.PositiveSmallIntegerField):
    description = "Tiny Integer Field"
    def db_type(self, connection):
        if any(_ in connection.settings_dict['ENGINE'] for _ in ['pyodbc', 'mysql']):
            return 'tinyint UNSIGNED'
        else:
            return 'smallint UNSIGNED'

class ReadOnlyOnExistForeignKey(object):
    def __init__(self, *args, **kwargs):
        super(ReadOnlyOnExistForeignKey, self).__init__(*args, **kwargs)
        self.__readonly_fields = []
        rof = []
        try: rof = getattr(self, 'readonly_fields')
        except AttributeError: pass
        for i in rof:
            a = []
            for j in i[0]:
                x = True
                for k in self._meta._relation_tree:
                    if k.model.__name__ == j:
                        a.append((k.model, k.name))
                        x = False
                if x:
                    error = _("{} and {} are not related.")
                    name = self.__class__.__name__
                    raise Exception(error.format(name, j))
            b = []
            for j in i[1]:
                b.append(j)
                try:
                    setattr(self, '__original_%s' % j, getattr(self, j))
                except:
                    setattr(self, '__original_%s' % j, None)
            self.__readonly_fields.append((a, b))

    def has_changed(self):
        arr = []
        for k, v in enumerate(self.__readonly_fields):
            for field in v[1]:
                orig = '__original_%s' % field
                new_value = None
                try: new_value = getattr(self, field)
                except: pass
                if getattr(self, orig) != new_value:
                    arr.append(k)
                    break
        return arr

    def clean(self, *args, **kwargs):
        hs = self.has_changed()
        fields = [self.__readonly_fields[i] for i in hs]
        if fields:
            adict = {}
            edict = {}
            for ki, vi in enumerate(fields):
                for kj, vj in enumerate(vi[0]):
                    f = vj[0].objects.filter(**{vj[1]: self.id})
                    name = 'exists%s%s' % (ki, kj)
                    adict[name] = Exists(f)
                    edict[name] = (vj[0], vi[1])
            selffilter = type(self).objects.filter(pk=self.id)
            response = selffilter.annotate(**adict).values(*adict)[0]
            for k, v in response.items():
                error = _("{} fields can't be changed when {} exists.")
                pair = edict[k]
                m = str(pair[0]._meta.verbose_name)
                flds = [str(self._meta.get_field(i).verbose_name) for i in pair[1]]
                f = _(' and ').join(flds)
                raise ValidationError(error.format(f, m))
        super(ReadOnlyOnExistForeignKey, self).clean(*args, **kwargs)
