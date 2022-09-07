FROM python:3.8

WORKDIR /sreality_scraper

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN playwright install
RUN playwright install-deps  

COPY ./scrapy ./scrapy
COPY ./templates ./templates
COPY scraper.py scraper.py
COPY web_app.py web_app.py
COPY start.sh start.sh

RUN chmod +x ./start.sh
CMD ["./start.sh"]