from flask import render_template, Blueprint, request
loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='templates')

from exceptions import DataLayerError, PictureWrongTypeError
from utils import PostsHandler
from utils import save_uploaded_picture

import logging
logging.basicConfig(filename='basic.log', level=logging.INFO, encoding='UTF-8')


@loader_blueprint.route('/post')
def create_new_post_page():
    """ переходим на страничку добавления нового поста """
    return render_template("post_form.html")

@loader_blueprint.route('/post', methods=['POST'])
def create_new_post_from_user_data_page():
    """ создаем новый пост """
    picture = request.files.get('picture', None)
    content = request.form.get('content', None)
    posts_handler = PostsHandler('posts.json')

    if not picture or not content:
        logging.info('данные не загружены')
        return 'данные не загружены'
    try:
        picture_path = save_uploaded_picture(picture)
    except PictureWrongTypeError:
        logging.info('Попытка загрузить неверный тип файла')
        return 'Вы пытаетесь загрузить неверный тип файла'
    except FileNotFoundError:
        return 'Не удалось сохранить файл, путь не найден'

    picture_url = '/' + picture_path

    post_object = {'pic': picture_url, 'content': content}

    try:
        logging.info('добавлен новый пост')
        posts_handler.add_post(post_object)
    except:
        return 'Не удалось добавить пост, ошибка записи в файл списка постов'

    return render_template('post_uploaded.html', picture_url=picture_url, content=content)
