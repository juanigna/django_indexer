# Generated by Django 4.2.9 on 2024-05-19 22:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_nativetx_id_alter_nativetx_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nativetx',
            name='erc20Txs',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.erc20tx'),
        ),
    ]
