# Generated by Django 5.1.2 on 2024-11-26 08:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('tone', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumni',
            name='linkedin_profile',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='alumni',
            name='field_of_work',
            field=models.ManyToManyField(blank=True, related_name='business_fields', to='tone.skill', verbose_name='Fields of Work/Expertise'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(default=datetime.date(2000, 1, 1)),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Other', max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='tone_user_set', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
