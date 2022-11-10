# The program publishes comics in contact

The program downloads comics from the resource [https://xkcd.com](https://xkcd.com). Uses the VKontakte API to publish these comics

### Software environment and installation:

Python3 should already be installed.

### Program installation:

Download the code: [https://github.com/VAChess777/Lesson_6_web_servises_API_Devman](https://github.com/VAChess777/Lesson_6_web_servises_API_Devman), or clone the `git` repository to a local folder:
```
git clone https://github.com/VAChess777/Lesson_6_web_servises_API_Devman
```

### Installing dependencies:
 
Use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```bach
pip install -r requirements.txt
```

### About environment variables:

For the program to work, you will need `API tokens`, which you will then place in the 
environment variables.  The values of which you will put in the `.env` file.

For the work of the program `main.py`. To post on the wall, you need a user `access_token`. To get it, VKontakte wants 
an 'app'. Create it on the Vkontakte page for developers. You can create an application in the 'My Applications' section. 
Link to it in the header of the page [https://vk.com/dev](https://vk.com/dev). As the application type, you should 
specify `standalone` — this is the appropriate type for applications that simply run on the computer. Get the user's `access_token`. 
It is needed so that your application has access to your account and can post messages in groups. To get `access_token`, 
you need to use the `Implicit Flow` procedure, a detailed description of this procedure can be found at [https://vk.com/dev/implicit_flow_user](https://vk.com/dev/implicit_flow_user).
The token looks like a string like `access_token=vk1.a.sscscs6546EESCSFS5454U0e...`, it will appear in the address bar, signed as `access_token`.

When you receive the `access_token`, put its value in the `.env` file.
For example: `'VK_ACCESS_TOKEN'=vk1.a.sscscs6546EESCSFS5454U0e.........`.

Then put this value in an environment variable in the program.
For example: `access_token_vk = os.environ['VK_ACCESS_TOKEN']`.

Open your  VKontakte community and see your `group_id` in the address bar [https://vk.com/club654651345](https://vk.com/club654651345)

When you receive the `group_id`, put its value in the `.env` file.
For example: `'GROUP_ID'='654651345`.

Then put this value in an environment variable in the program.
For example: `group_id = os.environ['GROUP_ID']`.

Use the `photos.getWallUploadServer` method and get the server address for uploading the image [https://dev.vk.com/method/photos.getWallUploadServer](https://dev.vk.com/method/photos.getWallUploadServer)
After successful execution, it returns an object with the fields `upload_url`, `album_id`, `user_id`.

When you receive the `upload_url` put its value in the `.env` file.
For example: `'UPLOAD_URL_VK'='https://pu.vk.com/d54002/ss8895/upload.php?act=do_add&mid=9.......'`.

Then put this value in an environment variable in the program.
For example: `upload_url_vk = os.environ['UPLOAD_URL_VK']`.

When you receive the `user_id` put its value in the `.env` file.
For example: `'OWNER_ID'='789456...'`.

Then put this value in an environment variable in the program.
For example: `owner_id = os.environ['OWNER_ID']`.

To use all of the above environment variables in programs, use the `load_dotenv()` module.

### How to run the program:

Run the script ```main.py``` with the command:
```bach
$ python main.py
```

### How the program works:

The program consists of 1 script:

```main.py``` - The program downloads comics from the resource [https://xkcd.com](https://xkcd.com). Uses the VKontakte API to publish these comics.
            
### Features works of the program:

The `main.py` program contains the functions:

* The `get_random_comic` function - downloads a random comic from a resource [https://xkcd.com](https://xkcd.com).
* The `get_random_number_comic` function - gets the total number of comics and selects a random comic number.
* The `download_random_comic` function - downloads a random comic.
* The `uploading_random_comic_to_server_vk` function - uploads the comic to the VK server.
* The `saving_uploading_random_comic_in_album_vk` function - saves the downloaded comic.
* The `publish_random_comic_on_wall_vk` function - publishes a comic on the VK wall.
* The `def main():` - main function. 

### Project Goals

This code was written for educational purposes as part of an online course for web developers at [dvmn.org](https://dvmn.org/).