# Generated by Django 4.0 on 2021-12-27 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='edit',
            name='title',
            field=models.CharField(default='default title', max_length=300),
            preserve_default=False,
        ),
    ]
