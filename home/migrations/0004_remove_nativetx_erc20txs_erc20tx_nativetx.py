# Generated by Django 4.2.9 on 2024-05-19 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_nativetx_erc20txs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nativetx',
            name='erc20Txs',
        ),
        migrations.AddField(
            model_name='erc20tx',
            name='nativeTx',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.nativetx'),
        ),
    ]