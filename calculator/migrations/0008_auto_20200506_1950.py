# Generated by Django 3.0.5 on 2020-05-06 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0007_auto_20200506_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('I', 'Insurance'), ('P', 'Property Taxes'), ('E', 'Electricity'), ('A', 'Administration fees'), ('O', 'Other')], max_length=1),
        ),
    ]
