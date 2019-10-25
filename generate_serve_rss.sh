#! /bin/bash

python3 generate_rss.py &
cd rss
python3 -m http.server 