from rest_framework.serializers import ModelSerializer
from fanra.models import Person


class PersonSerialzer(ModelSerializer):
    class Meta:
        model = Person

        fields = ("id", "name", "image")
