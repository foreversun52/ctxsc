# Generated by Django 2.1.15 on 2021-03-11 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='material_price',
            field=models.CharField(max_length=50, null=True, verbose_name='材料价格'),
        ),
    ]