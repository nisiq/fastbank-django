# Generated by Django 4.2.7 on 2023-11-23 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_conta_agencia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='saldo',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
