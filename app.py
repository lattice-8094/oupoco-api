# -*- coding: utf-8 -*-

import generation_sonnets
import datetime
import json

from flask import Flask
from flask_restplus import Api, Resource, reqparse

from flask import jsonify, request

app = Flask(__name__)
api = Api(app, version='0.9', title="API du projet Oupoco", description="API de test pour la mise en place du site web")

bd_meta = 'bd_meta.json'
meta = json.load(open(bd_meta))
authors = set([meta[s]['auteur'] for s in meta])

schemas = {
    'sonnet_sicilien1':('ABAB','ABAB','CDE','CDE'),
    'sonnet_sicilien2':('ABAB','ABAB','CDC','CDC'),
    'sonnet_petrarquien1':('ABBA','ABBA','CDE','CDE'),
    'sonnet_petrarquien2':('ABBA','ABBA','CDC','DCD'),
    'sonnet_petrarquien3':('ABBA','ABBA','CDE','DCE'),
    'sonnet_marotique':('ABBA','ABBA','CCD','EED'),
    'sonnet_francais':('ABBA','ABBA','CCD','EDE'),
    'sonnet_queneau':('ABAB','ABAB','CCD','EDE'),
    'sonnet_shakespearien':('ABAB','CDCD','EFEF','GG'),
    'sonnet_spencerien':('ABAB','BCBC','CDCD','EE'),
    'sonnet_irrationnel':('AAB','C','BAAB','C','CDCCD')
    }

dates = ('1800-1830', '1831-1850', '1851-1870', '1871-1890', '1891-1900', '1901-1950')

@api.route('/schemas')
class Schemas(Resource):
    def get(self):
        """ Returns the list of available schemas """
        return jsonify(schemas)

@api.route('/authors')
class Authors(Resource):
    def get(self):
        """ Returns the list of authors in the database """
        return jsonify(list(authors))

@api.route('/dates')
class Schemas(Resource):
    def get(self):
        """ Returns the list of available dates """
        return jsonify(dates)


new_parser = reqparse.RequestParser()
new_parser.add_argument('schema', type=str, choices=tuple(schemas.keys()))
new_parser.add_argument('authors', type=str, choices=tuple(authors), action='append')
new_parser.add_argument('date', type=str, choices=dates)

@api.route("/new")
class New(Resource):
    @api.expect(new_parser)
    def get(self):
        """ Returns a new sonnet in JSON """
        args = new_parser.parse_args()
        param_schema = args.get('schema', None)
        param_date = args.get('date', None)
        param_authors = args.get('authors', None)
        print(param_authors)

        if param_schema in schemas:
            sonnet = generation_sonnets.generate(authors=param_authors, date=param_date, schema=schemas[param_schema])
        else:
            sonnet = generation_sonnets.generate(authors=param_authors, date=param_date)

        if sonnet is None:
            return ""
        sonnet_text = list()
        for st in sonnet:
            for verse in st:
                sonnet_text.append({'text': verse['text'], 'meta': format_meta(verse['meta'])})
            sonnet_text.append({'text': "\n", 'meta': ''})
        res = {'text': sonnet_text, 'date': get_date_time()}
        return jsonify(res)

@app.route("/new-html")
def new_html():
    """ Returns a new sonnet in HTML """
    args = new_parser.parse_args()
    param_schema = args.get('schema', None)
    param_date = args.get('date', None)
    param_authors = args.get('authors', None)

    if param_schema in schemas:
        sonnet = generation_sonnets.generate(authors=param_authors, date=param_date, schema=schemas[param_schema])
    else:
        sonnet = generation_sonnets.generate(authors=param_authors, date=param_date)

    if sonnet is None: 
            return ""
    sonnet_html = '<div id="sonnet">'
    for st in sonnet:
        sonnet_html += "<p>"
        for verse in st:
            sonnet_html += f"<span title='{format_meta(verse['meta'])}'>{verse['text']}</span><br/>"
        sonnet_html += "</p>"
    sonnet_html += '</div>'
    date = f"<small>{get_date_time()}</small>"
    return sonnet_html+date

def get_date_time():
    now = datetime.datetime.now()
    now_str = f"{now.year}/{now.month}/{now.day}-{now.hour}:{now.minute}:{now.second}:{now.microsecond}"
    return now_str

def format_meta(meta):
    return "{} {} {}".format(meta['auteur'], meta['date'], meta['titre sonnet'])
