# Generated by Django 5.0.6 on 2024-06-27 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='commune',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='district',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='education_level',
            field=models.CharField(choices=[('Seconde', '2nde A'), ('Seconde', '2nde C'), ('Seconde', '2nde G2'), ('Premiere', '1ère A'), ('Premiere', '1ère D'), ('Premiere', '1ère C'), ('Premiere', '1ère G2'), ('Terminale', 'Terminale A'), ('Terminale', 'Terminale C'), ('Terminale', 'Terminale D'), ('Terminale', 'Terminale G2'), ('cours preparatoir1', 'CP1'), ('cours preparatoir1', 'CP2'), ('cours élémentaire1', 'CE1'), ('cours élémentaire2', 'CE2'), ('Cours moyen1', 'CM1'), ('Cours moyen2', 'CM2'), ('Sixième', '6eme'), ('Cinquième', '5eme'), ('quartrième', '4eme'), ('Troixième', '3eme')], max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
