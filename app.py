# -*- coding: utf-8 -*-

import generation_sonnets
import datetime

from flask import Flask
from flask import jsonify, request

app = Flask(__name__)

schemas = {
    'sonnet_sicilien':('ABAB','ABAB','CDE','CDE'),
    'sonnet_petrarquien':('ABBA','ABBA','CDE','CDE'),
    'sonnet_marotique':('ABBA','ABBA','CCD','EED'),
    'sonnet_francais':('ABBA','ABBA','CCD','EDE'),
    'sonnet_queneau':('ABAB','ABAB','CCD','EDE')
    }

@app.route("/new",  methods=['GET'])
def new():
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

@app.route("/new-html",  methods=['GET'])
def new_html():
    param_schema = request.args.get('schema', None)
    if param_schema in schemas:
        print('coucou', schemas[param_schema])
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