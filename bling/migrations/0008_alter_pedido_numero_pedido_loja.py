# Generated by Django 4.0 on 2022-02-11 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bling', '0007_alter_item_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='numero_pedido_loja',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
