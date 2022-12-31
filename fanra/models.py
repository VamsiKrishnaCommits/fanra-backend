from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=255)
    ref = models.CharField(max_length=255, null=True)
    image = models.URLField(null=True)
    connection = models.ManyToManyField(to="self", blank=True)


class Movie(models.Model):
    name = models.CharField(max_length=255)
    ref = models.CharField(max_length=255, null=True)
    cast = models.ManyToManyField(to=Person, blank=True)


class Relation(models.Model):
    person1 = models.ForeignKey(
        to=Person, related_name="person1", on_delete=models.CASCADE
    )
    person2 = models.ForeignKey(
        to=Person, related_name="person2", on_delete=models.CASCADE
    )
    relation = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
