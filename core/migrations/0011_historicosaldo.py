# Generated by Django 4.2.7 on 2023-12-04 17:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_historicocartaocredito'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricoSaldo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('saque', 'Saque'), ('deposito', 'Depósito'), ('transferencia', 'Transferência'), ('emprestimo', 'Empréstimo')], max_length=20)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_transacao', models.DateTimeField(default=django.utils.timezone.now)),
                ('conta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.conta')),
            ],
        ),
    ]