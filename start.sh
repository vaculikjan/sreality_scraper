#!/bin/bash
cd scrapy
rm data.json | scrapy crawl reality_spider
cd ..
python3 scraper.py
python3 web_app.py