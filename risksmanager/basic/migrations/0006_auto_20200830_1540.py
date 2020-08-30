# Generated by Django 2.2.12 on 2020-08-30 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0005_auto_20200830_1507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='controls',
        ),
        migrations.AddField(
            model_name='project',
            name='controls',
            field=models.ManyToManyField(blank=True, default='', null=True, related_name='controls', to='basic.ProjectControl'),
        ),
    ]
