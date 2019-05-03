from django.db import models


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
        self.__important_fields = getattr(self, 'important_fields')
        self.__related_models = getattr(self, 'related_models')
        for field in self.__important_fields:
            try:
                setattr(self, '__original_%s' % field, getattr(self, field))
            except:
                setattr(self, '__original_%s' % field, None)

    def has_changed(self):
        for field in self.__important_fields:
            orig = '__original_%s' % field
            new_value = None
            try: new_value = getattr(self, field)
            except: pass
            if getattr(self, orig) != new_value:
                return True
        return False

    def clean(self, *args, **kwargs):
        models = []
        for i in self.__related_models:
            models.append((apps.get_model('timetableapp', i[0]), i[1]))
        fields = self.__important_fields
        exists = False
        for i in models:
            if i[0].objects.filter(**{i[1]: self}).exists():
                exists = True
                break
        if exists and self.has_changed():
            error = _("{} fields can't be changed when {} exists")
            flds = [str(self._meta.get_field(i).verbose_name) for i in fields]
            f = _(" and ").join(flds)
            mdls = [str(i[0]._meta.verbose_name) for i in models]
            m = _(" and ").join(mdls)
            raise ValidationError(error.format(f, m))
        super(ReadOnlyOnExistForeignKey, self).clean(*args, **kwargs)
