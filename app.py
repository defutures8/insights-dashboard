from flask import Flask, render_template
from fetcher import get_hero_article, get_recommended, get_three_col, get_linkedin_posts, get_youtube_posts
import os

app = Flask(__name__)

app.jinja_env.globals.update(enumerate=enumerate)

@app.route("/")
def index():
    hero = get_hero_article()
    recommended = get_recommended()
    three_col = get_three_col()
    linkedin = get_linkedin_posts()
    youtube = get_youtube_posts()

    # Mix LinkedIn and YouTube alternating into one row of 4
    combined = []
    li_iter = iter(linkedin)
    yt_iter = iter(youtube)
    for i in range(4):
        if i % 2 == 0:
            post = next(li_iter, None) or next(yt_iter, None)
        else:
            post = next(yt_iter, None) or next(li_iter, None)
        if post:
            combined.append(post)

    return render_template("index.html",
        hero=hero,
        recommended=recommended,
        three_col=three_col,
        social=combined,
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)