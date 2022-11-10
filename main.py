import os
import random

import requests
from dotenv import load_dotenv
from pathlib import Path


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
    return filename


def uploading_random_comic_to_server_vk(path, filename, upload_url_vk):
    with open(Path(f'{path}', f'{filename}'), 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url_vk, files=files)
        response.raise_for_status()
        response_from_server_vk = response.json()
        return response_from_server_vk


def saving_uploading_random_comic_in_album_vk(
            access_token_vk,
            response_from_server_vk,
            owner_id,
            group_id):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    photo_from_server_vk = response_from_server_vk['photo']
    server_number = response_from_server_vk['server']
    hash_from_server_vk = response_from_server_vk['hash']
    params = {
        'access_token': access_token_vk,
        'owner_id': owner_id,
        'group_id': group_id,
        'photo': photo_from_server_vk,
        'server': server_number,
        'hash': hash_from_server_vk,
        'v': '5.131'
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    image_id_from_response_server = response.json()['response'][0]['id']
    return image_id_from_response_server


def publish_random_comic_on_wall_vk(
            image_id_from_response_server,
            owner_id,
            random_comic,
            access_token_vk,
            group_id):
    url = 'https://api.vk.com/method/wall.post'
    attachments = f'photo{owner_id}_{image_id_from_response_server}'
    commentary_comic_picture = random_comic['alt']
    params = {
        'access_token': access_token_vk,
        'owner_id': owner_id,
        'friends_only': '1',
        'attachments': attachments,
        'from_group': '1',
        'message': commentary_comic_picture,
        'group_id': group_id,
        'v': '5.131'
    }
    response = requests.post(url, params=params)
    response.raise_for_status()


def main():
    load_dotenv()
    access_token_vk = os.environ['VK_ACCESS_TOKEN']
    upload_url_vk = os.environ['UPLOAD_URL_VK']
    owner_id = os.environ['OWNER_ID']
    group_id = os.environ['GROUP_ID']
    Path('Python Comics').mkdir(parents=True, exist_ok=True)
    path = 'Python Comics'
    random_number_comic = get_random_number_comic()
    random_comic = get_random_comic(random_number_comic)
    filename = download_random_comic(
        random_comic,
        path,
        random_number_comic
    )
    response_from_server_vk = uploading_random_comic_to_server_vk(
        path,
        filename,
        upload_url_vk
    )
    image_id_from_response_server = saving_uploading_random_comic_in_album_vk(
        access_token_vk,
        response_from_server_vk,
        owner_id,
        group_id
    )
    try:
        publish_random_comic_on_wall_vk(
            image_id_from_response_server,
            owner_id,
            random_comic,
            access_token_vk,
            group_id
        )
    finally:
        os.remove(Path(f'{path}', f'{filename}'))


if __name__ == '__main__':

    main()