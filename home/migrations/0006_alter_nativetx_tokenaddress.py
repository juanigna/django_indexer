# Generated by Django 4.2.9 on 2024-05-19 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_nativetx_r_alter_nativetx_s_alter_nativetx_v'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nativetx',
            name='tokenAddress',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Token Address'),
        ),
    ]