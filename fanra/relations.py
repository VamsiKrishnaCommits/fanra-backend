from pydoc import visiblename
from fanra.models import *
import wikipedia
import requests
import json
from fanra.djikstra import find_shortest_relation_with_person
WIKI_REQUEST = "http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles="


def relations():
    movies = Movie.objects.all()
    for movie in movies:
        for person1 in movie.cast.all():
            for person2 in movie.cast.all():
                if person1 == person2:
                    continue
                Relation.objects.create(
                    person1=person1, person2=person2, relation=movie
                )


cache = {}


def find_route_custom(person1: Person, person2: Person):
    # maintain a queue of paths
    queue = []
    visited = {}
    visited[person1] = True
    # push the first path into the queue
    queue.append([[person1]])
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1][0]
        # path found
        if node == person2:
            return path
        # enumerate all adjacent nodes, construct a
        # new path and push it into the queue
        relations = Relation.objects.filter(person1=node)

        for relation in relations:
            if visited.get(relation.person2) == True:
                continue
            new_path = list(path)
            new_path.append([relation.person2, relation.relation.name])
            visited[relation.person2] = True
            queue.append(new_path)


def find_route(person1: Person, person2: Person):
    visited = {}
    queue = []
    queue.append(person1)
    visited[person1] = True
    while queue:
        s = queue.pop(0)
        relations = Relation.objects.filter(person1=s)

        for relation in relations:
            if visited.get(relation.person2) == True:
                continue
            if relation.person2 == person2:
                return
            print(relation.person2.name + "    " + relation.relation.name)

            queue.append(relation.person2)
            visited[relation.person2] = True


def find_disconnected():
    visited = {}
    queue = []
    visited = {}

    count = 0
    total_size = 0
    sigma_sum = 0
    for person in Person.objects.all():
        if visited.get(person, False) == True:
            continue

        if visited.get(person, False) == False:
            count = count + 1
        visited[person] = True
        # push the first path into the queue
        queue.append(person)
        print(person.name)
        size = 1
        while queue:
            node = queue.pop(0)

            relations = Relation.objects.filter(person1=node)

            for relation in relations:
                if visited.get(relation.person2) == True:
                    continue
                visited[relation.person2] = True
                queue.append(relation.person2)
                size = size + 1
                print(relation.person2.name)
        print("--------------------------")
        sigma_sum = sigma_sum + size

    return count


def populate(person1: str, person2: str):
    person1 = Person.objects.get(id=person1)
    person2 = Person.objects.get(id=person2)
    path = find_shortest_relation_with_person(person1, person2)
    nodes= []
    edges=[]
    counter= 0
    for i in range(1,len(path)):
        
        nodes.append({'id':counter , 'label':path[i][0].name , 'color':'blue'})
        counter=counter+1
        if  path[i][1]:
            nodes.append({'id':counter , 'label':path[i][1].name , 'color':'green'})
            counter=counter+1
            edges.append({'from':counter-2, 'to':counter-1, 'label':''})
            edges.append({'from':counter-1 , 'to': counter , 'label':'' })

    
    return nodes , edges


def populate_images():
    persons = Person.objects.all()
    for person in persons:
        url = get_wiki_image(person.name)
        person.image = url
        person.save()


def get_wiki_image(search_term):
    try:
        result = wikipedia.search(search_term, results=1)
        wikipedia.set_lang("en")
        wkpage = wikipedia.WikipediaPage(title=result[0])
        title = wkpage.title
        response = requests.get(WIKI_REQUEST + title)
        json_data = json.loads(response.text)
        img_link = list(json_data["query"]["pages"].values())[0]["original"]["source"]
        return img_link
    except:
        return 0


from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "populates the tables with configurations required for notifications"

    def handle(self, *args, **options):

        l = populate(args[0], args[1])
        self.stdout.write(
            self.style.SUCCESS(
                f"Populated tables with configurations for notifications.",
            )
        )
