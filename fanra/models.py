from django.db import models


class Person(models.Model):
    id = models.CharField(primary_key=True , max_length=255)
    name = models.CharField(max_length=255)
    image = models.CharField(null=True , max_length=255)
    connection = models.ManyToManyField(to="self", blank=True)


class Movie(models.Model):
    id = models.CharField(primary_key=True , max_length=255)
    name = models.CharField(max_length=255)
    ref = models.CharField(max_length=255, null=True)
    cast = models.ManyToManyField(to=Person, blank=True)
    image = models.CharField(null=True,max_length=255)



class Relation(models.Model):
    person1 = models.ForeignKey(
        to=Person, related_name="person1", on_delete=models.CASCADE
    )
    person2 = models.ForeignKey(
        to=Person, related_name="person2", on_delete=models.CASCADE
    )
    relation = models.ForeignKey(to=Movie, on_delete=models.CASCADE)


