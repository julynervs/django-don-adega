# Generated by Django 4.0 on 2022-02-17 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bling', '0008_alter_pedido_vlr_desconto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='numero_pedido_loja',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]