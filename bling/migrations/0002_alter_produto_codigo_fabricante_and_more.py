# Generated by Django 4.0 on 2022-02-11 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bling', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='codigo_fabricante',
            field=models.CharField(default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='produtokit',
            name='codigo_fabricante',
            field=models.CharField(default='', max_length=255, null=True),
        ),
    ]
