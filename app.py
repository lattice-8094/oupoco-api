# -*- coding: utf-8 -*-

import generation_sonnets
import datetime
import json
from collections import Counter, defaultdict

from flask import Flask
from flask_restx import Api, Resource, reqparse
from flask_cors import CORS
from flask import jsonify, request

import logging

logger = logging.getLogger(__name__)
import logging.config

logging.config.fileConfig("./logging.conf")

# http://flask.pocoo.org/snippets/35/
class ReverseProxied(object):
    """Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.
    In nginx:
    ::
        location /myprefix {
            proxy_pass http://192.168.0.1:5001;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Scheme $scheme;
            proxy_set_header X-Script-Name /myprefix;
        }
    In Apache:
    ::
        <Location /myprefix>
            ProxyPass http://192.168.0.1:5001
            ProxyPassReverse http://192.168.0.1:5001
            RequestHeader set X-Script-Name /myprefix
        </Location>
    :param wsgi_app: the WSGI application
    Inspired by: http://flask.pocoo.org/snippets/35/
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get("HTTP_X_SCRIPT_NAME", "")
        if script_name:
            environ["SCRIPT_NAME"] = script_name
            path_info = environ["PATH_INFO"]
            if path_info.startswith(script_name):
                environ["PATH_INFO"] = path_info[len(script_name) :]

        scheme = environ.get("HTTP_X_SCHEME", "")
        if scheme:
            environ["wsgi.url_scheme"] = scheme
        return self.app(environ, start_response)


app = Flask(__name__)
CORS(app)
app.wsgi_app = ReverseProxied(app.wsgi_app)
api = Api(
    app,
    version="0.9",
    title="API du projet Oupoco",
    description="API pour la mise en place du site web",
)

bd_meta = "bd_meta.json"
meta = json.load(open(bd_meta))
authors = generation_sonnets.get_authors()
themes = generation_sonnets.get_themes()
dates = generation_sonnets.get_dates()

schemas = {
    "sonnet_sicilien1": ("ABAB", "ABAB", "CDE", "CDE"),
    "sonnet_sicilien2": ("ABAB", "ABAB", "CDC", "CDC"),
    "sonnet_petrarquien1": ("ABBA", "ABBA", "CDE", "CDE"),
    "sonnet_petrarquien2": ("ABBA", "ABBA", "CDC", "DCD"),
    "sonnet_petrarquien3": ("ABBA", "ABBA", "CDE", "DCE"),
    "sonnet_marotique": ("ABBA", "ABBA", "CCD", "EED"),
    "sonnet_francais": ("ABBA", "ABBA", "CCD", "EDE"),
    "sonnet_queneau": ("ABAB", "ABAB", "CCD", "EDE"),
    "sonnet_shakespearien": ("ABAB", "CDCD", "EFEF", "GG"),
    "sonnet_spencerien": ("ABAB", "BCBC", "CDCD", "EE"),
    "sonnet_irrationnel": ("AAB", "C", "BAAB", "C", "CDCCD"),
}

#dates = ("1800-1830", "1831-1850", "1851-1870", "1871-1890", "1891-1900", "1901-1950")


@api.route("/schemas")
class Schemas(Resource):
    def get(self):
        """ Returns the list of available schemas """
        return jsonify(schemas)


authors_parser = reqparse.RequestParser()
authors_parser.add_argument("dates", type=str, choices=tuple(dates), action="append")
authors_parser.add_argument("themes", type=str, choices=tuple(themes), action="append")
authors_parser.add_argument("femme", type=str, default="false")


@api.route("/authors")
class Authors(Resource):
    @api.expect(authors_parser)
    def get(self):
        """ Returns the list of authors in the database """
        args = authors_parser.parse_args()
        param_dates = args.get("dates", None)
        param_themes = args.get("themes", None)
        if args.get("femme") == "true":
            param_femme = True
        else:
            param_femme = False
        all_authors = generation_sonnets.get_authors()
        all_authors = sorted(all_authors, key=lambda author: author.split(" ")[-1])
        filtered_authors = generation_sonnets.get_authors(
            dates=param_dates, themes=param_themes, femme=param_femme
        )
        res = __active_values__(all_authors, filtered_authors)
        return jsonify(res)


authors_form_parser = reqparse.RequestParser()
authors_form_parser.add_argument(
    "dates", type=str, choices=tuple(dates), action="append"
)
authors_form_parser.add_argument(
    "themes", type=str, choices=tuple(themes), action="append"
)
authors_form_parser.add_argument("femme", type=str, default="false")

@api.route("/authors-form")
class AuthorsForm(Resource):
    @api.expect(authors_form_parser)
    def get(self):
        """ Returns a list of selected authors in the form """
        args = authors_form_parser.parse_args()
        param_dates = args.get("dates", None)
        param_themes = args.get("themes", None)
        if args.get("femme") == "true":
            param_femme = True
        else:
            param_femme = False
        all_authors = generation_sonnets.get_selected_authors()
        # all_authors = sorted(all_authors, key=lambda author: author.split(" ")[-1])
        filtered_authors = generation_sonnets.get_authors(
            dates=param_dates, themes=param_themes, femme=param_femme
        )
        res = __active_values__(all_authors, filtered_authors)
        return jsonify(res)


dates_parser = reqparse.RequestParser()
dates_parser.add_argument("authors", type=str, choices=tuple(authors), action="append")
dates_parser.add_argument("themes", type=str, choices=tuple(themes), action="append")
dates_parser.add_argument("femme", type=str, default="false")

@api.route("/dates")
class Dates(Resource):
    @api.expect(dates_parser)
    def get(self):
        """ Returns the list of available dates """
        args = dates_parser.parse_args()
        param_authors = args.get("authors", None)
        param_themes = args.get("themes", None)
        if args.get("femme") == 'true':
            param_femme = True
        else:
            param_femme = False
        all_dates = generation_sonnets.get_dates()
        filtered_dates = generation_sonnets.get_dates(
            authors=param_authors, themes=param_themes, femme=param_femme
        )
        res = __active_values__(all_dates, filtered_dates)
        return jsonify(res)


themes_parser = reqparse.RequestParser()
themes_parser.add_argument("dates", type=str, choices=tuple(dates), action="append")
themes_parser.add_argument("authors", type=str, choices=tuple(authors), action="append")
themes_parser.add_argument("femme", type=str, default="false")

@api.route("/themes")
class Themes(Resource):
    @api.expect(themes_parser)
    def get(self):
        """ Returns the list of themes in the database """
        args = themes_parser.parse_args()
        param_authors = args.get("authors", None)
        param_dates = args.get("dates", None)
        if args.get("femme") == "true":
            param_femme = True
        else:
            param_femme = False
        all_themes = generation_sonnets.get_themes()
        filtered_themes = generation_sonnets.get_themes(
            authors=param_authors, dates=param_dates, femme=param_femme
        )
        res = __active_values__(all_themes, filtered_themes)
        return jsonify(res)


new_parser = reqparse.RequestParser()
new_parser.add_argument("schema", type=str, choices=tuple(schemas.keys()))
new_parser.add_argument("authors", type=str, choices=tuple(authors), action="append")
new_parser.add_argument("dates", type=str, choices=tuple(dates), action="append")
new_parser.add_argument("order", type=bool, default=True)
new_parser.add_argument("themes", type=str, choices=tuple(themes), action="append")
new_parser.add_argument("femme", type=str, default="false")
new_parser.add_argument(
    "quality", type=str, choices=("1", "2", "3", "4", "5"), default="1"
)


@api.route("/new")
class New(Resource):
    @api.expect(new_parser)
    def get(self):
        """ Returns a new sonnet in JSON """
        args = new_parser.parse_args()
        param_schema = args.get("schema", None)
        param_date = args.get("dates", None)
        param_authors = args.get("authors", None)
        param_themes = args.get("themes", None)
        if args.get("femme") == "true":
            param_femme = True
        else:
            param_femme = False
        param_quality = args.get("quality", "1")
        if args.get("order") == "false":
            param_order = False
        else:
            param_order = True

        if param_schema in schemas:
            print(param_date)
            sonnet = generation_sonnets.generate(
                authors=param_authors,
                dates=param_date,
                schema=schemas[param_schema],
                order=param_order,
                themes=param_themes,
                femme=param_femme,
                quality=param_quality,
            )
        else:
            sonnet = generation_sonnets.generate(
                authors=param_authors,
                dates=param_date,
                order=param_order,
                themes=param_themes,
                femme=param_femme,
                quality=param_quality,
            )

        if sonnet:
            sonnet_text = list()
            for st in sonnet:
                for verse in st:
                    sonnet_text.append(
                        {"text": verse["text"], "meta": format_meta(verse["meta"])}
                    )
                sonnet_text.append({"text": "\n", "meta": ""})
            res = {"text": sonnet_text, "date": get_date_time()}
            return jsonify(res)
        else:
            res = {
                "error": "Génération impossible, veuillez modifier vos paramètres",
                "date": get_date_time(),
            }
            return jsonify(res)


@app.route("/new-html")
def new_html():
    """ Returns a new sonnet in HTML """
    args = new_parser.parse_args()
    param_schema = args.get("schema", None)
    param_date = args.get("dates", None)
    param_authors = args.get("authors", None)
    param_quality = args.get("quality", "1")
    if args.get("femme") == "false":
            param_femme = False
    else:
            param_femme = True
    if args.get("order") == "false":
        param_order = False
    else:
        param_order = True

    if param_schema in schemas:
        sonnet = generation_sonnets.generate(
            authors=param_authors,
            date=param_date,
            schema=schemas[param_schema],
            order=param_order,
            femme=param_femme,
            quality=param_quality,
        )
    else:
        sonnet = generation_sonnets.generate(
            authors=param_authors,
            date=param_date,
            order=param_order,
            femme=param_femme,
            quality=param_quality,
        )

    if sonnet is None:
        return ""
    sonnet_html = '<div id="sonnet">'
    for st in sonnet:
        sonnet_html += "<p>"
        for verse in st:
            sonnet_html += f"<span title='{format_meta(verse['meta'])}'>{verse['text']}</span><br/>"
        sonnet_html += "</p>"
    sonnet_html += "</div>"
    date = f"<small>{get_date_time()}</small>"
    return sonnet_html + date


def get_date_time():
    now = datetime.datetime.now()
    now_str = f"{now.year}/{now.month}/{now.day}-{now.hour}:{now.minute}:{now.second}:{now.microsecond}"
    return now_str


def format_meta(meta):
    return "{} {} {}".format(meta["auteur"], meta["date"], meta["titre sonnet"])


def __active_values__(all_values, filtered_values):
    """
    Return a list of dict, one per item in all_values,
    set the 'active' to yes if the item is in filtered_values, no otherwise
    Args:
        - all_values (list): list of str
        - filtered_values (list): list of str
    Returns:
        - list of dict [{'value': 'foo', 'active': 'yes}, {'value': 'bar', 'active': 'no'}]
    """
    res = []
    for item in all_values:
        if item in filtered_values:
            res.append({"value": item, "active": "yes"})
        else:
            res.append({"value": item, "active": "no"})
    return res
