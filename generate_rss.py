"""
Générateur de fichier rss
1 strophe par minute
"""

import schedule
import time
import datetime
import pytz
from feedgen.feed import FeedGenerator
import generation_sonnets

rss_file = "rss/rss.xml"
fg = FeedGenerator()
fg.title('Oupoco feed')
fg.subtitle('Une strophe par minute, un sonnet toutes les 5 minutes')
fg.link( href='http://apps.lattice.cnrs.fr/oupoco-rss/rss.xml', rel='self' )
fg.language('fr')
fg.rss_file(rss_file, extensions=False, pretty=True)


def job():
    schema=('ABAB','ABAB','CCD','EDE')
    for st_schema in schema:
        stanza = ""
        sonnet = generation_sonnets.generate(schema=tuple(st_schema))
        for st in sonnet:   
            for verse in st:
                stanza += verse['text']
                stanza += "<lb/>"
        fe = fg.add_entry()
        if len(st_schema) == 4:
            fe.title('Quatrain')
        else:
            fe.title('Tercet')
        fe.description(stanza)
        fe.pubDate(pytz.utc.localize(datetime.datetime.now()))
        #rssfeed  = fg.rss_str(pretty=True)
        #print(rssfeed)
        fg.rss_file(rss_file, pretty=True)
        time.sleep(60)

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