"""
Générateur de fichier rss
1 sonnet par minute
"""

import schedule
import time
import datetime
import pytz
import re
import requests
import json
from feedgen.feed import FeedGenerator

RSS_FILE = "rss/rss.xml"
OUPOCO_CALL = "http://oupoco_api/new"
timezone = pytz.timezone("Europe/Paris")


def write_rss_feed(rss_str, rss_file=RSS_FILE):
    """
    Dirty hack to remove namespace declaration and atom:link element which hang on apps.lattice.cnrs.fr
    """
    rss_str = rss_str.decode("utf-8")
    rss_str = re.sub(r"<rss.+?>", "<rss>", rss_str)
    rss_str = re.sub(r"<atom:link.+?>", "", rss_str)
    with open(rss_file, "w") as out:
        out.write(rss_str)


def restart():
    """
    start a new rss file
    """
    fg = FeedGenerator()
    fg.title("Oupoco feed")
    fg.subtitle("Une strophe par minute")
    fg.link(href="https://apps.lattice.cnrs.fr/oupoco_rss/rss.xml", rel="self")
    fg.language("fr")
    fg.lastBuildDate(timezone.localize(datetime.datetime.now()))
    rssfeed = fg.rss_str(pretty=True)
    write_rss_feed(rssfeed)


def job():
    schema = ("ABAB", "ABAB", "CCD", "EDE")
    resp = requests.get(OUPOCO_CALL)
    sonnet_json = json.loads(resp.content)
    for item in sonnet_json["text"]:
        fe = fg.add_entry()
        fe.title(item["meta"])
        fe.description(item["text"])
        fe.pubDate(timezone.localize(datetime.datetime.now()))
    rssfeed = fg.rss_str(pretty=True)
    write_rss_feed(rssfeed)
    # fg.rss_file(rss_file, pretty=True)
    time.sleep(60)


fg = FeedGenerator()
fg.title("Oupoco feed")
fg.subtitle("Une strophe par minute")
fg.link(href="https://apps.lattice.cnrs.fr/oupoco_rss/rss.xml", rel="self")
fg.language("fr")
fg.lastBuildDate(timezone.localize(datetime.datetime.now()))
rssfeed = fg.rss_str(pretty=True)
write_rss_feed(rssfeed)


schedule.every(1).minutes.do(job)
schedule.every().monday.do(restart)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
