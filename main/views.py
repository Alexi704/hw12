from flask import render_template, Blueprint, request
import utils
from exceptions import DataLayerError

import logging
logging.basicConfig(filename='basic.log', level=logging.INFO, encoding='UTF-8')

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')
search_blueprint = Blueprint('search_blueprint', __name__, template_folder='templates')

@main_blueprint.route('/')
def main_page():
    """ главная страничка сайта """
    logging.info('Запрошена главная страница')
    return render_template("index.html")

@search_blueprint.route('/search')
def search_page():
    """ поисковая страничка """
    s = request.args.get('s', '')
    posts_handler = utils.PostsHandler('posts.json')
    logging.info('Выполняется поиск')
    try:
        posts = posts_handler.search_posts_for_substring(s)
        return render_template("post_list.html", posts=posts, s=s)
    except DataLayerError:
        return 'Поврежден файл с данными'
