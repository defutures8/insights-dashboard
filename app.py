from flask import Flask, render_template
from fetcher import get_articles, get_linkedin_posts
import os

app = Flask(__name__)

@app.route("/")
def index():
    articles = get_articles()
    linkedin = get_linkedin_posts()
    return render_template("index.html", articles=articles, linkedin=linkedin)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)