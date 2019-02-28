# -*- coding: utf-8 -*-

import generation_sonnets
import datetime
import json

from flask import Flask
from flask_restplus import Api, Resource

from flask import jsonify, request

app = Flask(__name__)
api = Api(app, version='0.9', title="API du projet Oupoco", description="API de test pour la mise en place du site web")

bd_meta = 'bd_meta.json'

schemas = {
    'sonnet_sicilien':('ABAB','ABAB','CDE','CDE'),
    'sonnet_petrarquien':('ABBA','ABBA','CDE','CDE'),
    'sonnet_marotique':('ABBA','ABBA','CCD','EED'),
    'sonnet_francais':('ABBA','ABBA','CCD','EDE'),
    'sonnet_queneau':('ABAB','ABAB','CCD','EDE')
    }


@api.route('/schemas')
class Schemas(Resource):
    def get(self):
        """ Returns the list of available schemas """
        return jsonify(schemas)

@api.route('/authors')
class Authors(Resource):
    def get(self):
        """ Returns the list of authors in the database """
        meta = json.load(open(bd_meta))
        authors = set([meta[s]['auteur'] for s in meta])
        return jsonify(list(authors))

@api.route("/new")
@api.doc(params={'schema': 'The name of a schema (i.e. sonnet_francais)'})
class New(Resource):
    def get(self):
        """ Returns a new sonnet in JSON"""
        param_schema = request.args.get('schema', None)
        if param_schema in schemas:
            sonnet = generation_sonnets.generate(schemas[param_schema])
        else:
            sonnet = generation_sonnets.generate()
        sonnet_text = list()
        for st in sonnet:
            for verse in st:
                sonnet_text.append({'text': verse['text'], 'meta': format_meta(verse['meta'])})
            sonnet_text.append({'text': "\n", 'meta': ''})
        res = {'text': sonnet_text, 'date': get_date_time()}
        return jsonify(res)

@api.route("/new-html")
@api.doc(params={'schema': 'The name of a schema (i.e. sonnet_francais)'})
class NewHtml(Resource):
    def get(self):
        """ Returns a new sonnet in HTML """
        param_schema = request.args.get('schema', None)
        if param_schema in schemas:
            sonnet = generation_sonnets.generate(schemas[param_schema])
        else:
            sonnet = generation_sonnets.generate()
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