# Generated by Django 5.0.1 on 2024-11-24 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0002_alter_itemorder_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemorder',
            name='order_date',
            field=models.DateField(),
        ),
    ]