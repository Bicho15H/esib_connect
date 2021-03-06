# Generated by Django 3.2.6 on 2022-03-17 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClubNetwork', '0004_club_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='campus',
            field=models.CharField(default='USJ', max_length=20),
        ),
        migrations.AddField(
            model_name='club',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='club',
            name='phone',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='student',
            name='campus',
            field=models.CharField(default='USJ', max_length=20),
        ),
        migrations.AddField(
            model_name='student',
            name='country',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='student',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='student',
            name='phone',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='student',
            name='region',
            field=models.CharField(default='', max_length=20),
        ),
    ]
