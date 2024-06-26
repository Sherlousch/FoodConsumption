# Generated by Django 5.0.6 on 2024-06-20 21:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='FoodType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240, verbose_name='Name')),
                ('gas_emission_kg_co2', models.FloatField(verbose_name='Gas emission in kg CO2')),
                ('freshwater_withdrawal_l', models.FloatField(verbose_name='Freshwater withdrawal in L')),
                ('land_use_m2', models.FloatField(verbose_name='Land use in m2')),
            ],
        ),
        migrations.CreateModel(
            name='Consumption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_consumption', models.FloatField(verbose_name='kg consumed for human food')),
                ('feed_consumption', models.FloatField(verbose_name='kg consumed for animal feed')),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consumption_set', to='consumption.consumer', verbose_name='consumer')),
                ('food_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consumption.foodtype', verbose_name='food type')),
            ],
        ),
        migrations.AddConstraint(
            model_name='consumption',
            constraint=models.UniqueConstraint(fields=('consumer', 'food_type'), name='unique_consumer_food_type_combination'),
        ),
    ]
