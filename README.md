# The program publishes comics in [https://vk.com](https://vk.com)

The program downloads comics from the resource [https://xkcd.com](https://xkcd.com). Uses the VKontakte API to publish 
these comics in [https://vk.com](https://vk.com)

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
For example: `VK_ACCESS_TOKEN=vk1.a.sscscs6546EESCSFS5454U0e.........`.

Then put the environment variable into the program.
For example: `access_token_vk = os.environ['VK_ACCESS_TOKEN']`.

Open your VKontakte community in a browser, and see your `vk_group_id` in the address bar.        
For example: [https://vk.com/club225463221](https://vk.com/club225463221), end your `vk_group id=225463221`.

When you receive the `vk_group_id`, put its value in the `.env` file.
For example: `VK_GROUP_ID=225463221`.

Then put the environment variable into the program.
For example: `vk_group_id = os.environ['VK_GROUP_ID']`.

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

* The `download_random_comic` function - downloads random comic from the resource [https://xkcd.com](https://xkcd.com).
* The `check_errors_vk_api` function - checks all responses from the VK api, and if the response contains an error, displays information about the error number and error text.
* The `get_vk_upload_url` function - gets the address to download the comic and 
* The `upload_random_comic` function - uploads the comic to the VK server.
* The `save_random_comic` function - saves the downloaded comic.
* The `publish_random_comic` function - publishes a comic on the VK wall.
* The `def main():` - main function. 

### Project Goals

This code was written for educational purposes as part of an online course for web developers at [dvmn.org](https://dvmn.org/).