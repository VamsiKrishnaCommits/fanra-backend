from requests import Request, Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from fanra.djikstra import build_graph
from fanra.models import Person,Query
from fanra.serializer import PersonSerialzer
from fanra.relations import populate
from rest_framework.filters import SearchFilter
from django.http import HttpResponse
from django.http import JsonResponse


class FetchCelebs(GenericViewSet, ListModelMixin):
    http_method_names = ["get"]
    serializer_class = PersonSerialzer
    filter_backends = [SearchFilter]
    search_fields = ["^name"]

    def get_queryset(self):
        # Get the search string from the request
        search_string = self.request.query_params.get('search', '')

        # If the search string is not empty, perform the search and return the results
        if search_string:
            return Person.objects.filter(name__contains=search_string)

        # If the search string is empty, return an empty queryset
        return Person.objects.none()


class FetchRelationShip(GenericViewSet):
    def retrieve(self, request: Request):
        celeb1 = request.GET['celeb1']
        celeb2 = request.GET['celeb2']
        Query.objects.create(celeb1=celeb1 , celeb2=celeb2)
        nodes , edges = populate(person1=celeb1, person2=celeb2 )
        response = {'nodes':nodes , 'edges':edges}
        return JsonResponse(response)


class Fetchbuild(GenericViewSet):
    def retrieve(self, request: Request):
        build_graph(force=True)
        return JsonResponse({})

class HealthCheck(GenericViewSet):
    def retrieve(self , request :Request):
        return JsonResponse({})