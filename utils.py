import json
from exceptions import DataLayerError, PictureUploadError
from pprint import pprint as pp

class PostsHandler:

    def __init__(self, path):
        self.path = path


    def load_post_from_json(self):
        """ загружает данные из  JSON файла """
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                posts = json.load(file)
            return posts
        except (FileNotFoundError, json.JSONDecodeError):
            raise DataLayerError('Что-то не так с файлом...')


    def search_posts_for_substring(self, substring):

        substring_lower = substring.lower()
        posts_found = []

        posts = self.load_post_from_json()
        for post in posts:
            if substring_lower in post['content'].lower():
                posts_found.append(post)

        return posts_found

    def add_post(self, post):
        posts = self.load_post_from_json()
        posts.append(post)
        self.save_post_to_json(posts)

    def save_post_to_json(self, posts):
        try:
            with open(self.path, 'w', encoding='utf-8') as file:
                json.dump(posts, file, ensure_ascii=False)
        except FileNotFoundError:
            raise DataLayerError



# posts_handler = PostsHandler('posts.json')
# posts = posts_handler.search_posts_for_substring('погулять')
# pp(posts)

from exceptions import PictureWrongTypeError

def save_uploaded_picture(picture):

    file_name = picture.filename
    file_type = file_name.split('.')[-1]

    if file_type not in ['jpg', 'jpeg', 'png', 'svg']:
        raise PictureWrongTypeError

    picture.save(f'./uploads/images/{file_name}')


    return f'uploads/images/{file_name}'