# -*- coding: utf-8 -*-

import generation_sonnets
import datetime

from flask import Flask
app = Flask(__name__)

from flask import jsonify


@app.route("/new")
def new():
    sonnet = generation_sonnets.generate()
    sonnet_txt = ""
    for l in sonnet:
        sonnet_txt += l
        sonnet_txt += "\n"
    res = {'text': sonnet, 'date': get_date_time()}
    return jsonify(res)

@app.route("/new-html")
def new_html():
    sonnet = generation_sonnets.generate()
    sonnet_html = '<div id="sonnet">'
    for l in sonnet:
        if l == "":
            sonnet_html += "<p/>"
        else:
            sonnet_html += f"{l}<br/>"
    sonnet_html += '</div>'
    date = f"<small>{get_date_time()}</small>"
    return sonnet_html+date

def get_date_time():
    now = datetime.datetime.now()
    now_str = f"{now.year}/{now.month}/{now.day}-{now.hour}:{now.minute}:{now.second}:{now.microsecond}"
    return now_str