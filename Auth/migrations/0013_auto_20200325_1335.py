# Generated by Django 2.2.2 on 2020-03-25 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0012_auto_20200324_0558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=True),
        ),
    ]
