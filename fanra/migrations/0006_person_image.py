# Generated by Django 4.1 on 2022-12-03 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fanra", "0005_alter_relation_relation"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="image",
            field=models.URLField(null=True),
        ),
    ]
