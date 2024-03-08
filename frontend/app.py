#! /usr/bin/env python


"""
----------------
Optional WebApp.
----------------
Launch this file to start the WebApp (must be launched from frontend/ folder).

The app is based on bottle framework as it is lightweight.
"""


if __name__ != "__main__":
    raise ImportError("This file can't be imported.")


import bottle
import pymongo


mongo_client = pymongo.MongoClient("192.168.1.31")
mongo_database = mongo_client.BDAtiny
movies = mongo_database.json_movies


@bottle.route("/")
@bottle.view("index")
def index():
    return {}


@bottle.route("/search/<pattern>")
@bottle.view("search")
def search(pattern):
    """
    Return the result of the search for the given pattern.
    The search is made by looking for the substring, there's no fancy stuff here.
    If only one corresponding movie is found, redirects to the movie page.
    :param: pattern - The search pattern
    :return: The loaded file or a HTTP error
    """
    corresponding = list(movies.find(
        {"titles.primary": {"$regex": f"{pattern}", "$options": "i"}},
        limit=50
    ))

    if len(corresponding) == 1:
        bottle.redirect(f"/{corresponding[0]['mid']}")

    return {"movies": corresponding, "pattern": pattern}


@bottle.route("/<mid>")
@bottle.view("movie")
def movie(mid):
    """
    Return the movie page based on imdb mid
    :param: mid - The search pattern
    :return: The loaded file or a HTTP error
    """
    corresponding = movies.find_one(
        {"mid": {"$regex": f"{mid}", "$options": "i"}},
        hint="mid_1"
    )

    return {"movie": corresponding}


@bottle.route("/assets/<filepath:re:.*\.css>")
def send_static_css(filepath) -> bottle.HTTPError|bottle.HTTPResponse:
    """
    Serve all stylesheets
    :param: filepath - The file path in URL
    :return: The loaded file or a HTTP error
    """
    return bottle.static_file(filepath, "assets/")


@bottle.route("/assets/<filepath:re:.*\.js>")
def send_static_scripts(filepath) -> bottle.HTTPError|bottle.HTTPResponse:
    """
    Serve all script files
    :param: filepath - The file path in URL
    :return: The loaded file or a HTTP error
    """
    return bottle.static_file(filepath, "assets/")


@bottle.route("/assets/<filepath:re:.*\.(svg|png|jpeg)>")
def send_static_images(filepath) -> bottle.HTTPError|bottle.HTTPResponse:
    """
    Serve all image files
    :param: filepath - The file path in URL
    :return: The loaded file or a HTTP error
    """
    return bottle.static_file(filepath, "assets/")


bottle.run(debug=True)