import json
import pandas as pd
import sqlalchemy

from bs4 import BeautifulSoup
from sqlalchemy_utils import database_exists, create_database

# read the scraped data
f = open("scrapy/data.json")
site_json = json.loads(f.read())

# set lists for parsed data
ids = []
names = []
locality = []
images = []
img_names = []

# parse the html code
for page in site_json:

    soup = BeautifulSoup(page["text"], features="lxml")
    soup.prettify()

    flats = soup.find_all("div", class_="property ng-scope")

    for flat in flats:
        ids.append(flat["data-dot-data"].split('"')[3])
        names.append(flat.find("span", class_="name ng-binding").get_text())
        locality.append(flat.find("span", class_="locality ng-binding").get_text())

        img = []
        tmp = flat.find_all("img")
        for i in range(0, 3):
            img.append(tmp[i]["src"])
        images.append(img)

# create pandas dataframe from parsed data
df_reality = pd.DataFrame(
    {"ids": ids, "name": names, "locality": locality, "images": images}
)
split_df = pd.DataFrame(df_reality["images"].tolist(), columns=["img1", "img2", "img3"])
df_reality = pd.concat([df_reality, split_df], axis=1)
df_reality = df_reality.drop("images", axis=1)

# save dataframe to postgres database
engine = sqlalchemy.create_engine(
    "postgresql://postgres:password@localhost:5432/sreality_db"
)

if not database_exists(engine.url):
    create_database(engine.url)

df_reality.to_sql("flats", engine, index=False, if_exists="replace")
