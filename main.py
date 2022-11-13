import os
import random

import requests
from dotenv import load_dotenv
from pathlib import Path


def download_random_comic(path):
    last_comic_url = 'https://xkcd.com/info.0.json'
    response_last_comic_url = requests.get(last_comic_url)
    response_last_comic_url.raise_for_status()
    last_comic_number = int(response_last_comic_url.json()["num"])
    random_comic_number = random.randint(1, last_comic_number)
    random_comic_url = f'https://xkcd.com/{random_comic_number}/info.0.json'
    response_random_comic_url = requests.get(random_comic_url)
    response_random_comic_url.raise_for_status()
    random_comic = response_random_comic_url.json()
    comic_commentary = random_comic['alt']
    comic_url = random_comic['img']
    response_comic_url = requests.get(
        comic_url
    )
    response_comic_url.raise_for_status()
    filename = f'python_comics_number_{random_comic_number}.png'
    image = response_comic_url.content
    with open(Path(f'{path}', f'{filename}'), 'wb') as file:
        file.write(image)
    return filename, comic_commentary


def check_errors_vk_api(response):
    response = response.json()
    if response.get('error'):
        raise requests.HTTPError(
            response.get('error').get('error_code'),
            response.get('error').get('error_msg')
        )
    return response


def get_vk_upload_url(vk_access_token, vk_group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': vk_access_token,
        'group_id': vk_group_id,
        'v': '5.131'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    vk_upload_url = check_errors_vk_api(response)['response']['upload_url']
    vk_user_id = check_errors_vk_api(response)['response']['user_id']
    return vk_upload_url, vk_user_id


def upload_random_comic(path, vk_upload_url, filename):
    with open(Path(f'{path}', f'{filename}'), 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(vk_upload_url, files=files)
    response.raise_for_status()
    photo_vk = check_errors_vk_api(response)['photo']
    server_number = check_errors_vk_api(response)['server']
    hash_vk = check_errors_vk_api(response)['hash']
    return photo_vk, server_number, hash_vk


def save_random_comic(
            vk_access_token,
            filename,
            vk_upload_url,
            path,
            vk_user_id,
            vk_group_id):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    photo_vk, server_number, hash_vk = upload_random_comic(
        path,
        vk_upload_url,
        filename
    )
    params = {
        'access_token': vk_access_token,
        'owner_id': vk_user_id,
        'group_id': vk_group_id,
        'photo': photo_vk,
        'server': server_number,
        'hash': hash_vk,
        'v': '5.131'
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    image_id = check_errors_vk_api(response)['response'][0]['id']
    return image_id


def publish_random_comic(
            image_id,
            comic_commentary,
            vk_user_id,
            vk_access_token,
            vk_group_id):
    url = 'https://api.vk.com/method/wall.post'
    attachments = f'photo{vk_user_id}_{image_id}'
    params = {
        'access_token': vk_access_token,
        'owner_id': vk_user_id,
        'friends_only': '1',
        'attachments': attachments,
        'from_group': '1',
        'message': comic_commentary,
        'group_id': vk_group_id,
        'v': '5.131'
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    check_errors_vk_api(response)


def main():
    load_dotenv()
    vk_access_token = os.environ['VK_ACCESS_TOKEN']
    vk_group_id = os.environ['VK_GROUP_ID']
    Path('Python Comics').mkdir(parents=True, exist_ok=True)
    path = 'Python Comics'
    filename, comic_commentary = download_random_comic(path)
    vk_upload_url, vk_user_id = get_vk_upload_url(
        vk_access_token,
        vk_group_id
    )
    image_id = save_random_comic(
        vk_access_token,
        filename,
        vk_upload_url,
        path,
        vk_user_id,
        vk_group_id
    )
    try:
        publish_random_comic(
            image_id,
            comic_commentary,
            vk_user_id,
            vk_access_token,
            vk_group_id
        )
    finally:
        os.remove(Path(f'{path}', f'{filename}'))


if __name__ == '__main__':

    main()