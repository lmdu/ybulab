# Generated by Django 5.1 on 2024-08-29 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('specimen', '0007_alter_sample_collect_date_alter_sample_store_method_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '无'), (1, '在库'), (2, '在用'), (3, '用完')], default=0),
        ),
    ]
