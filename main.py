import requests
import os
from dotenv import load_dotenv
from pathlib import Path
import random

# -------------------------------------------------------------------------------------------------------
# def get_last_comic():
#     url = 'https://xkcd.com/info.0.json'
#     response = requests.get(url)
#     response.raise_for_status()
#     number_last_comic = response.json()['num']
#     url_last_comic = response.json()['img']
#     comment_last_comic = response.json()['alt']
#     print(comment_last_comic)


def get_random_comic(random_number_comic):
    url = f'https://xkcd.com/{random_number_comic}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    random_comic = response.json()
    return random_comic


def get_random_number_comic():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    number_last_comic = int(response.json()["num"])
    random_number_comic = random.randint(1, number_last_comic)
    return random_number_comic


def download_random_comic(random_comic, path, random_number_comic):
    random_comic_url = random_comic['img']
    filename = f'python_comics_number_{random_number_comic}.png'
    response = requests.get(random_comic_url)
    response.raise_for_status()
    image = response.content
    with open(Path(f'{path}', f'{filename}'), 'wb') as file:
        file.write(image)

def main():
    Path('Python Comics').mkdir(parents=True, exist_ok=True)
    path = 'Python Comics'
    # get_last_comic()

    random_number_comic = get_random_number_comic()
    random_comic = get_random_comic(random_number_comic)
    download_random_comic(random_comic, path, random_number_comic)

if __name__ == '__main__':

    main()























