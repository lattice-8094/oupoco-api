"""
Générateur de fichier rss
1 strophe par minute
"""

import schedule
import time
import datetime
import pytz
import re
from feedgen.feed import FeedGenerator
import generation_sonnets

RSS_FILE = "rss/rss.xml"
timezone = pytz.timezone("Europe/Paris")


def write_rss_feed(rss_str, rss_file=RSS_FILE):
    """
    Dirty hack to remove namespace declaration and atom:link element which hang on apps.lattice.cnrs.fr
    """
    rss_str = rss_str.decode("utf-8")
    rss_str = re.sub(r"<rss.+?>", "<rss>", rss_str)
    rss_str = re.sub(r"<atom:link.+?>", "", rss_str)
    with open(rss_file, 'w') as out:
        out.write(rss_str)

def job():
    schema=('ABAB','ABAB','CCD','EDE')
    for st_schema in schema:
        stanza = ""
        sonnet = generation_sonnets.generate(schema=tuple(st_schema))
        for st in sonnet:   
            for verse in st:
                stanza += verse['text']
                stanza += "\n"
        fe = fg.add_entry()
        if len(st_schema) == 4:
            fe.title('Quatrain')
        else:
            fe.title('Tercet')
        fe.description(stanza)
        fe.pubDate(timezone.localize(datetime.datetime.now()))
        rssfeed = fg.rss_str(pretty=True)
        #print(rssfeed)
        write_rss_feed(rssfeed)
        #fg.rss_file(rss_file, pretty=True)
        time.sleep(60)


fg = FeedGenerator()
fg.title('Oupoco feed')
fg.subtitle('Une strophe par minute, un sonnet toutes les 5 minutes')
fg.link( href='http://apps.lattice.cnrs.fr/oupoco-rss/rss.xml', rel='self' )
fg.language('fr')
fg.lastBuildDate(timezone.localize(datetime.datetime.now()))
rssfeed = fg.rss_str(pretty=True)
write_rss_feed(rssfeed)


schedule.every(5).minutes.do(job)
#schedule.every().hour.do(job)
#schedule.every().day.at("10:30").do(job)
#schedule.every(5).to(10).minutes.do(job)
#schedule.every().monday.do(job)
#schedule.every().wednesday.at("13:15").do(job)
#schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)