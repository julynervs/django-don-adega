# Generated by Django 4.0 on 2022-02-16 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bling', '0004_alter_contato_cpf_cnpj'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='data',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='data_saida',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='produto',
            name='codigo',
            field=models.CharField(blank=True, default='', max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='produto',
            name='data_alteracao',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='produto',
            name='data_inclusao',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='produto',
            name='data_validade',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='produtokit',
            name='data_alteracao',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='produtokit',
            name='data_inclusao',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
