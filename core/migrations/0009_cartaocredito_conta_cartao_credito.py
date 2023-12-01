# Generated by Django 4.2.7 on 2023-11-30 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_delete_extrato'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartaoCredito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_cartao', models.CharField(max_length=13)),
                ('cvv', models.CharField(max_length=3)),
                ('data_vencimento', models.DateField()),
                ('limite_disponivel', models.DecimalField(decimal_places=2, max_digits=6)),
                ('salario', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.AddField(
            model_name='conta',
            name='cartao_credito',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.cartaocredito'),
        ),
    ]