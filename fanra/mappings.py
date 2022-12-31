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
    # Get the root of the working directory
    root_dir = os.getcwd()

    # Create the assets folder if it doesn't exist
    if not os.path.exists(f'{root_dir}/assets'):
        os.makedirs(f'{root_dir}/assets')

    # Get all the records in the Person table
    people = Person.objects.all()

    # Iterate through each record
    for person in people:
        # Check if the image URL is valid
        if person.image:
            try:
                # Send a request to the image URL
                response = requests.get(person.image)
                # If the request is successful (status code is 200)
                if response.status_code == 200:
                    # Open a file handle to save the image
                    f = open(f'{root_dir}/assets/{person.id}_{person.name}.jpg', 'wb')
                    # Write the image data to the file
                    f.write(response.content)
                    # Create a Django File object
                    django_file = File(f)
                    # Save the image to the Person model
            except Exception as e:
                # Print any errors that occurred
                print(e)
        # If the image URL is not valid, skip the record
        else:
            continue



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
