# Generated by Django 4.1.5 on 2023-01-20 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fanra", "0006_person_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="person",
            name="ref",
        ),
        migrations.AddField(
            model_name="movie",
            name="image",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="id",
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="person",
            name="id",
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="person",
            name="image",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
