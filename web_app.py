import pandas as pd
import sqlalchemy
from flask import Flask
from flask import render_template

# load data from database
engine = sqlalchemy.create_engine(
    "postgresql://postgres:password@postgres:5432/sreality_db"
)
df = pd.read_sql_table("flats", engine)
df_list = df.values.tolist()

app = Flask(__name__)

# invoke template
@app.route("/")
def home():
    return render_template("home.html", flats=df_list)


# run web app
if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")
