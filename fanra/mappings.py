import requests
from bs4 import BeautifulSoup
from fanra.models import *
import requests
from django.core.files import File
import os


def mapshit(html_table):
    table = html_table
    rows = table.findAll("tr")
    cellen = len(rows[1].findAll("td"))

    for j in range(1, len(rows)):
        cells = rows[j].findAll("td")
        name = ""
        ref = ""
        try:
            name = cells[2 - (cellen - len(cells))].text
            ref = cells[2 - (cellen - len(cells))].find("a").get("href")

        except Exception as e:
            ref = None
        movie = Movie.objects.create(name=name, ref=ref)

        try:
            name = cells[3 - (cellen - len(cells))].text
            ref = cells[3 - (cellen - len(cells))].find("a").get("href")
        except Exception as e:
            ref = None

        print("yes")

        try:
            if ref is not None:
                director = Person.objects.get(ref=ref)
            else:
                director = Person.objects.create(name=name, ref=ref)
        except Exception as e:
            director = Person.objects.create(name=name, ref=ref)
        movie.cast.add(director)

        try:
            cast = cells[4 - (cellen - len(cells))]
            for actor in cast.findAll("a"):
                try:
                    name = actor.text
                    ref = actor["href"]
                except Exception as e:
                    ref = None

                try:
                    if ref is not None:
                        actor = Person.objects.get(ref=ref)
                    else:
                        actor = Person.objects.create(name=name, ref=ref)
                except Exception as e:
                    actor = Person.objects.create(name=name, ref=ref)
                movie.cast.add(actor)
        except Exception as e:
            pass


def get_table(year):
    url = "https://en.wikipedia.org/wiki/List_of_Telugu_films_of_{year}".format(
        year=year
    )
    r = requests.get(url)

    html_table = BeautifulSoup(r.text, "html.parser").findAll(
        "table",
        {
            "class": [
                "wikitable sortable",
                "wikitable sortable mw-collapsible",
                "wikitable",
            ]
        },
    )
    r.close()

    return html_table
    # --- loop from first table , from first row



def download_and_save_images():
    root_dir = os.getcwd()

    # Set the path to the assets directory
    assets_dir = f'{root_dir}/images'

    for person in Person.objects.all():
        # Check if the image field is not empty
        if person.image:
            # Construct the image URL
            image_url = f'https://image.tmdb.org/t/p/w500{person.image}'
            # Download the image
            try:
                response = requests.get(image_url)
                response.raise_for_status()
                with open(f"{assets_dir}{person.image}", 'wb') as f:
                    f.write(response.content)
            except requests.exceptions.HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
            except requests.exceptions.ConnectionError as conn_err:
                print(f'Error Connecting: {conn_err}')
            except requests.exceptions.Timeout as time_err:
                print(f'Timeout error: {time_err}')
            except requests.exceptions.RequestException as req_err:
                print(f'Request error: {req_err}')
        else:
            print(f'No image found for {person.name}')

def convert_filenames():
    # Get the root of the working directory
    root_dir = os.getcwd()

    # Set the path to the assets directory
    assets_dir = f'{root_dir}/assets'

    # Iterate over the files in the assets directory
    for filename in os.listdir(assets_dir):
        # Get the file path
        file_path = f'{assets_dir}/{filename}'
        # Check if the file is a regular file (not a directory)
        if os.path.isfile(file_path):
            # Replace %20 with spaces in the file name
            new_filename = filename.replace('%20', ' ')
            # Get the new file path
            new_file_path = f'{assets_dir}/{new_filename}'
            # Rename the file
            os.rename(file_path, new_file_path)


def tdm_data():
    import pdb
    pdb.set_trace()
    print("hello")
    for page in range(1,119):
        print(f'-------Processing page {page}/110---------')
        # Make a GET request to the TMDB API for searching movies
        response = requests.get(f'https://api.themoviedb.org/3/discover/movie?api_key=f5d242e55b5082b6477f1821b1bc17c6&with_original_language=te&page={page}&language=en&primary_release_date.lte=2023-01-31')
        data = response.json()

    # Iterate through the results and create a new Movie and Person model for each movie and cast member
        for result in data['results']:
            movie_response = requests.get(f'https://api.themoviedb.org/3/movie/{result["id"]}?api_key=f5d242e55b5082b6477f1821b1bc17c6')
            movie_data = movie_response.json()
            credits_response = requests.get(f'https://api.themoviedb.org/3/movie/{result["id"]}/credits?api_key=f5d242e55b5082b6477f1821b1bc17c6')
            credits_data = credits_response.json()
            
            # Create new Movie model and save to the database
            movie = Movie(id=result['id'], name=movie_data['title'], ref=movie_data['imdb_id'])
            movie.save()

            # Iterate through the cast information and create new Person models for each cast member
            for cast_member in credits_data['cast']:
                person = Person(id=cast_member['id'], name=cast_member['name'], image=cast_member['profile_path'])
                person.save()
                movie.cast.add(person)
            movie.save()
            
            for i in range(len(credits_data['cast'])):
                for j in range(i+1,len(credits_data['cast'])):
                    person1 = Person.objects.get(id=credits_data['cast'][i]['id'])
                    person2 = Person.objects.get(id=credits_data['cast'][j]['id'])
                    relation = Relation(person1=person1, person2=person2, relation=movie)
                    relation.save()
        print("-----processing-done-------")




def map_backward():
    for relation in Relation.objects.all():
        rel=Relation(person1= relation.person2, person2= relation.person1 ,relation = relation.relation)
        rel.save()



