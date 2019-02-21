# -*- coding: utf-8 -*-

import generation_sonnets
import datetime

from flask import Flask
app = Flask(__name__)

from flask import jsonify


@app.route("/new")
def new():
    schema=(('A', 'B', 'B', 'A'), ('A', 'B', 'B', 'A'), ('C', 'C', 'D'), ('E', 'D', 'E'))
    sonnet = generation_sonnets.generate(schema)
    sonnet_text = list()
    for st in sonnet:
        for verse in st:
            meta = "{} {} {}".format(verse['meta']['auteur'], verse['meta']['date'], verse['meta']['titre sonnet'])
            sonnet_text.append({'text': verse['text'], 'meta': format_meta(verse['meta'])})
        sonnet_text.append({'text': "\n", 'meta': ''})
    res = {'text': sonnet_text, 'date': get_date_time()}
    return jsonify(res)

@app.route("/new-html")
def new_html():
    schema=(('A', 'B', 'B', 'A'), ('A', 'B', 'B', 'A'), ('C', 'C', 'D'), ('E', 'D', 'E'))
    sonnet = generation_sonnets.generate(schema)
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