# Generated by Django 2.2 on 2019-05-01 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(unique=True, verbose_name='Number')),
                ('address', models.CharField(blank=True, default=None, max_length=128, null=True, unique=True, verbose_name='Address')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, default=None, max_digits=9, null=True, verbose_name='Longitude')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, default=None, max_digits=9, null=True, verbose_name='Longitude')),
            ],
            options={
                'verbose_name': 'Building',
                'verbose_name_plural': 'Buildings',
            },
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(unique=True, verbose_name='Number')),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetableapp.Building', verbose_name='Building')),
            ],
            options={
                'verbose_name': 'Classroom',
                'verbose_name_plural': 'Classrooms',
            },
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.PositiveSmallIntegerField(verbose_name='Semester')),
            ],
            options={
                'verbose_name': 'Curriculum',
                'verbose_name_plural': 'Curriculums',
            },
        ),
        migrations.CreateModel(
            name='CurriculumEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lectures', models.PositiveSmallIntegerField(verbose_name='Number of lectures')),
                ('practices', models.PositiveSmallIntegerField(verbose_name='Number of practices')),
                ('laboratory', models.PositiveSmallIntegerField(verbose_name='Number of laboratory')),
                ('independentWork', models.PositiveSmallIntegerField(verbose_name='Amount of independent work')),
                ('curriculum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetableapp.Curriculum', verbose_name='Curriculum')),
            ],
            options={
                'verbose_name': 'Curriculum entry',
                'verbose_name_plural': 'Curriculum entries',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Name')),
                ('abbreviation', models.CharField(blank=True, default=None, max_length=16, null=True, unique=True, verbose_name='Abbreviation')),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Name')),
                ('abbreviation', models.CharField(blank=True, default=None, max_length=16, null=True, unique=True, verbose_name='Abbreviation')),
            ],
            options={
                'verbose_name': 'Faculty',
                'verbose_name_plural': 'Faculties',
            },
        ),
        migrations.CreateModel(
            name='GroupState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Name')),
                ('suffix', models.CharField(blank=True, max_length=16, unique=True, verbose_name='Suffix')),
                ('semesters', models.PositiveSmallIntegerField(default=8, verbose_name='Number of semesters')),
                ('priority', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)], default=5, verbose_name='Priority')),
            ],
            options={
                'verbose_name': 'Group state',
                'verbose_name_plural': 'Group states',
                'order_with_respect_to': 'priority',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=128, verbose_name='First name')),
                ('middleName', models.CharField(max_length=128, verbose_name='Middle name')),
                ('lastName', models.CharField(max_length=128, verbose_name='Last name')),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'Persons',
                'unique_together': {('firstName', 'middleName', 'lastName')},
            },
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(unique=True, verbose_name='Number')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Name')),
                ('abbreviation', models.CharField(max_length=16, unique=True, verbose_name='Abbreviation')),
            ],
            options={
                'verbose_name': 'Specialty',
                'verbose_name_plural': 'Specialties',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='timetableapp.Department', verbose_name='Department')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='timetableapp.Person', verbose_name='Person')),
            ],
            options={
                'verbose_name': 'Teacher',
                'verbose_name_plural': 'Teachers',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Name')),
                ('department', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='timetableapp.Department', verbose_name='Department')),
            ],
            options={
                'verbose_name': 'Subject',
                'verbose_name_plural': 'Subjects',
            },
        ),
        migrations.CreateModel(
            name='GroupStream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveSmallIntegerField(choices=[(2019, 2019), (2018, 2018), (2017, 2017), (2016, 2016), (2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012), (2011, 2011), (2010, 2010), (2009, 2009), (2008, 2008), (2007, 2007), (2006, 2006), (2005, 2005), (2004, 2004), (2003, 2003), (2002, 2002), (2001, 2001), (2000, 2000), (1999, 1999), (1998, 1998), (1997, 1997), (1996, 1996), (1995, 1995), (1994, 1994), (1993, 1993), (1992, 1992), (1991, 1991), (1990, 1990), (1989, 1989), (1988, 1988), (1987, 1987), (1986, 1986), (1985, 1985), (1984, 1984), (1983, 1983), (1982, 1982), (1981, 1981), (1980, 1980), (1979, 1979), (1978, 1978), (1977, 1977), (1976, 1976), (1975, 1975), (1974, 1974), (1973, 1973), (1972, 1972), (1971, 1971), (1970, 1970), (1969, 1969), (1968, 1968), (1967, 1967), (1966, 1966), (1965, 1965), (1964, 1964), (1963, 1963), (1962, 1962), (1961, 1961), (1960, 1960), (1959, 1959), (1958, 1958), (1957, 1957), (1956, 1956), (1955, 1955), (1954, 1954), (1953, 1953), (1952, 1952), (1951, 1951), (1950, 1950), (1949, 1949), (1948, 1948), (1947, 1947), (1946, 1946), (1945, 1945), (1944, 1944), (1943, 1943), (1942, 1942), (1941, 1941), (1940, 1940), (1939, 1939), (1938, 1938), (1937, 1937), (1936, 1936), (1935, 1935), (1934, 1934), (1933, 1933), (1932, 1932), (1931, 1931), (1930, 1930), (1929, 1929), (1928, 1928), (1927, 1927), (1926, 1926), (1925, 1925), (1924, 1924), (1923, 1923), (1922, 1922), (1921, 1921), (1920, 1920), (1919, 1919), (1918, 1918), (1917, 1917), (1916, 1916), (1915, 1915), (1914, 1914), (1913, 1913), (1912, 1912), (1911, 1911), (1910, 1910), (1909, 1909), (1908, 1908), (1907, 1907), (1906, 1906), (1905, 1905), (1904, 1904), (1903, 1903), (1902, 1902), (1901, 1901), (1900, 1900)], default=2019, verbose_name='Year')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='timetableapp.Specialty', verbose_name='Specialty')),
                ('state', models.ForeignKey(default={'priority': 1}, on_delete=django.db.models.deletion.PROTECT, to='timetableapp.GroupState', verbose_name='State')),
            ],
            options={
                'verbose_name': 'Group stream',
                'verbose_name_plural': 'Group streams',
                'unique_together': {('specialty', 'year', 'state')},
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(blank=True, choices=[(None, '-'), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)], default=None, null=True, verbose_name='Number')),
                ('group_stream', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='timetableapp.GroupStream', verbose_name='Group stream')),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='timetableapp.Group', verbose_name='Parent node')),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
                'unique_together': {('group_stream', 'parent', 'number')},
            },
        ),
        migrations.AddField(
            model_name='department',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='timetableapp.Faculty', verbose_name='Faculty'),
        ),
        migrations.CreateModel(
            name='CurriculumEntryTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('responsibility', models.PositiveSmallIntegerField(choices=[(0, 'Lectures'), (1, 'Practices'), (2, 'Laboratory')], default=0, verbose_name='Responsibility')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetableapp.CurriculumEntry', verbose_name='Curriculum entry')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetableapp.Group', verbose_name='Group')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetableapp.Teacher', verbose_name='Teacher')),
            ],
            options={
                'verbose_name': 'Teacher for curriculum entry',
                'verbose_name_plural': 'Teachers for curriculum entries',
                'unique_together': {('entry', 'group', 'responsibility')},
            },
        ),
        migrations.CreateModel(
            name='CurriculumEntrySubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetableapp.CurriculumEntry', verbose_name='Curriculum entry')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetableapp.Subject', verbose_name='Subject')),
            ],
            options={
                'verbose_name': 'Subject for curriculum entry',
                'verbose_name_plural': 'Subjects for curriculum entries',
            },
        ),
        migrations.AddField(
            model_name='curriculumentry',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetableapp.Group', verbose_name='Group'),
        ),
        migrations.AddField(
            model_name='curriculumentry',
            name='subjects',
            field=models.ManyToManyField(through='timetableapp.CurriculumEntrySubject', to='timetableapp.Subject', verbose_name='Subjects'),
        ),
        migrations.AddField(
            model_name='curriculumentry',
            name='teachers',
            field=models.ManyToManyField(through='timetableapp.CurriculumEntryTeacher', to='timetableapp.Teacher', verbose_name='Teachers'),
        ),
        migrations.AddField(
            model_name='curriculum',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetableapp.GroupStream', verbose_name='Group stream'),
        ),
        migrations.CreateModel(
            name='TimetableEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson', models.PositiveSmallIntegerField(choices=[(1, 'numerator - mon - 1 lesson'), (2, 'numerator - mon - 2 lesson'), (3, 'numerator - mon - 3 lesson'), (4, 'numerator - mon - 4 lesson'), (5, 'numerator - mon - 5 lesson'), (33, 'numerator - tue - 1 lesson'), (34, 'numerator - tue - 2 lesson'), (35, 'numerator - tue - 3 lesson'), (36, 'numerator - tue - 4 lesson'), (37, 'numerator - tue - 5 lesson'), (65, 'numerator - wed - 1 lesson'), (66, 'numerator - wed - 2 lesson'), (67, 'numerator - wed - 3 lesson'), (68, 'numerator - wed - 4 lesson'), (69, 'numerator - wed - 5 lesson'), (97, 'numerator - thu - 1 lesson'), (98, 'numerator - thu - 2 lesson'), (99, 'numerator - thu - 3 lesson'), (100, 'numerator - thu - 4 lesson'), (101, 'numerator - thu - 5 lesson'), (129, 'numerator - fri - 1 lesson'), (130, 'numerator - fri - 2 lesson'), (131, 'numerator - fri - 3 lesson'), (132, 'numerator - fri - 4 lesson'), (133, 'numerator - fri - 5 lesson'), (161, 'numerator - sat - 1 lesson'), (162, 'numerator - sat - 2 lesson'), (163, 'numerator - sat - 3 lesson'), (164, 'numerator - sat - 4 lesson'), (165, 'numerator - sat - 5 lesson'), (257, 'denominator - mon - 1 lesson'), (258, 'denominator - mon - 2 lesson'), (259, 'denominator - mon - 3 lesson'), (260, 'denominator - mon - 4 lesson'), (261, 'denominator - mon - 5 lesson'), (289, 'denominator - tue - 1 lesson'), (290, 'denominator - tue - 2 lesson'), (291, 'denominator - tue - 3 lesson'), (292, 'denominator - tue - 4 lesson'), (293, 'denominator - tue - 5 lesson'), (321, 'denominator - wed - 1 lesson'), (322, 'denominator - wed - 2 lesson'), (323, 'denominator - wed - 3 lesson'), (324, 'denominator - wed - 4 lesson'), (325, 'denominator - wed - 5 lesson'), (353, 'denominator - thu - 1 lesson'), (354, 'denominator - thu - 2 lesson'), (355, 'denominator - thu - 3 lesson'), (356, 'denominator - thu - 4 lesson'), (357, 'denominator - thu - 5 lesson'), (385, 'denominator - fri - 1 lesson'), (386, 'denominator - fri - 2 lesson'), (387, 'denominator - fri - 3 lesson'), (388, 'denominator - fri - 4 lesson'), (389, 'denominator - fri - 5 lesson'), (417, 'denominator - sat - 1 lesson'), (418, 'denominator - sat - 2 lesson'), (419, 'denominator - sat - 3 lesson'), (420, 'denominator - sat - 4 lesson'), (421, 'denominator - sat - 5 lesson')], default=0, verbose_name='Number of lesson')),
                ('classroom', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='timetableapp.Classroom', verbose_name='Classroom')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetableapp.CurriculumEntry', verbose_name='Curriculum entry')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetableapp.Group', verbose_name='Group')),
                ('teacher', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='timetableapp.Teacher', verbose_name='Teacher')),
            ],
            options={
                'verbose_name': 'Timetable entry',
                'verbose_name_plural': 'Timetable entries',
                'unique_together': {('lesson', 'classroom'), ('entry', 'group', 'lesson')},
            },
        ),
        migrations.CreateModel(
            name='SemesterSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.PositiveSmallIntegerField(default=0, verbose_name='Semester')),
                ('startDate', models.DateField(blank=True, default=None, null=True, verbose_name='Start date')),
                ('endDate', models.DateField(blank=True, default=None, null=True, verbose_name='End date')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetableapp.GroupStream', verbose_name='Group stream')),
            ],
            options={
                'verbose_name': 'Semester schedule',
                'verbose_name_plural': 'Semester schedule',
                'unique_together': {('group', 'semester')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='curriculum',
            unique_together={('group', 'semester')},
        ),
    ]
