# Generated by Django 3.2.4 on 2021-06-27 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KDA_app', '0034_child_case_data_punishment'),
    ]

    operations = [
        migrations.AddField(
            model_name='child_case_data',
            name='enroll_date_1',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='child_case_data',
            name='enroll_date_2',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='child_case_data',
            name='enroll_date_3',
            field=models.DateField(blank=True, null=True),
        ),
    ]
