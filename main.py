import os
import random

import requests
from dotenv import load_dotenv
from pathlib import Path


def download_random_comic(path):
    last_comic_url = 'https://xkcd.com/info.0.json'
    last_comic_response = requests.get(last_comic_url)
    last_comic_response.raise_for_status()
    last_comic_number = int(last_comic_response.json()["num"])
    random_comic_number = random.randint(1, last_comic_number)
    random_comic_url = f'https://xkcd.com/{random_comic_number}/info.0.json'
    random_comic_response = requests.get(random_comic_url)
    random_comic_response.raise_for_status()
    random_comic = random_comic_response.json()
    comic_commentary = random_comic['alt']
    comic_url = random_comic['img']
    comic_response = requests.get(
        comic_url
    )
    comic_response.raise_for_status()
    filename = f'python_comics_number_{random_comic_number}.png'
    image = comic_response.content
    with open(Path(f'{path}', f'{filename}'), 'wb') as file:
        file.write(image)
    return filename, comic_commentary


def check_vk_api_errors(response):
    response = response.json()
    if response.get('error'):
        raise requests.HTTPError(
            response.get('error').get('error_code'),
            response.get('error').get('error_msg')
        )


def get_vk_upload_url(vk_access_token, vk_group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': vk_access_token,
        'group_id': vk_group_id,
        'v': '5.131'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    check_vk_api_errors(response)
    total_response = response.json()
    vk_upload_url = total_response['response']['upload_url']
    return vk_upload_url


def upload_random_comic(path, vk_upload_url, filename):
    with open(Path(f'{path}', f'{filename}'), 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(vk_upload_url, files=files)
    response.raise_for_status()
    check_vk_api_errors(response)
    total_response = response.json()
    vk_photo = total_response['photo']
    server_number = total_response['server']
    vk_hash = total_response['hash']
    return vk_photo, server_number, vk_hash


def save_random_comic(
            vk_access_token,
            filename,
            vk_upload_url,
            path,
            vk_group_id):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    vk_photo, server_number, vk_hash = upload_random_comic(
        path,
        vk_upload_url,
        filename
    )
    params = {
        'access_token': vk_access_token,
        'group_id': vk_group_id,
        'photo': vk_photo,
        'server': server_number,
        'hash': vk_hash,
        'v': '5.131'
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    check_vk_api_errors(response)
    total_response = response.json()
    image_id = total_response['response'][0]['id']
    owner_id = total_response['response'][0]['owner_id']
    return image_id, owner_id


def publish_random_comic(
            image_id,
            owner_id,
            comic_commentary,
            vk_access_token,
            vk_group_id):
    url = 'https://api.vk.com/method/wall.post'
    attachments = f'photo{owner_id}_{image_id}'
    params = {
        'access_token': vk_access_token,
        'owner_id': - int(vk_group_id),
        'friends_only': 1,
        'attachments': attachments,
        'from_group': 1,
        'message': comic_commentary,
        'group_id': vk_group_id,
        'v': '5.131'
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    check_vk_api_errors(response)


def main():
    load_dotenv()
    vk_access_token = os.environ['VK_ACCESS_TOKEN']
    vk_group_id = os.environ['VK_GROUP_ID']
    Path('Python Comics').mkdir(parents=True, exist_ok=True)
    path = 'Python Comics'
    filename, comic_commentary = download_random_comic(path)
    vk_upload_url = get_vk_upload_url(
        vk_access_token,
        vk_group_id
    )
    image_id, owner_id = save_random_comic(
        vk_access_token,
        filename,
        vk_upload_url,
        path,
        vk_group_id
    )
    try:
        publish_random_comic(
            image_id,
            owner_id,
            comic_commentary,
            vk_access_token,
            vk_group_id
        )
    finally:
        os.remove(Path(f'{path}', f'{filename}'))


if __name__ == '__main__':

    main()