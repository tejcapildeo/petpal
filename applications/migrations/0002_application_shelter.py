# Generated by Django 4.2.7 on 2023-11-15 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='shelter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.shelter'),
        ),
    ]