# Generated by Django 4.0 on 2022-02-18 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bling', '0012_contareceber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contapagar',
            name='forma_pagamento',
        ),
    ]
