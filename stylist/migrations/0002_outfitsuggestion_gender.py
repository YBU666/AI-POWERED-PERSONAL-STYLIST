# Generated by Django 5.2 on 2025-04-27 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stylist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='outfitsuggestion',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('non_binary', 'Non-Binary'), ('other', 'Other')], max_length=20, null=True),
        ),
    ]
