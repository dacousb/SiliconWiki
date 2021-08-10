from flask import Flask, render_template, request, redirect, abort
from articles import get_article, save_edit, search_for
from table import get_rows
import config

app = Flask(__name__, template_folder="templates")
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
@app.route("/wiki/")
def index():
    return redirect("/wiki/Main")


@app.route("/wiki/<article_name>/")
def wiki(article_name):
    article_object = get_article(article_name)
    title = article_object.title
    content = article_object.content
    if not article_object.found:
        abort(404)
    return redirect("/wiki/" + title) if title != article_name else\
        render_template("wiki.html", title=title, content=content)


@app.route("/edit/<article_name>/")
def edit(article_name):
    article_object = get_article(article_name, True)
    title = article_object.title
    content = article_object.content
    if not article_object.found:
        abort(404)
    return redirect("/edit/" + title) if title != article_name else\
        render_template("edit.html", title=title, content=content,
                        protected=True if article_name in config.protected_pages else False)


@app.route("/create/<article_name>/")
def create(article_name):
    save_edit(article_name[0].upper() + article_name[1:],
              "This is a brand new article. Start [editing it](/edit/" + article_name + ")!", True)
    return redirect("/wiki/" + article_name)


@app.route("/search")
def search():
    query = request.args.get("q")
    if query != query.split("/")[0]:
        return redirect("/search?q=" + query.split("/")[0])
    if query is None or not query.strip():
        return redirect("/")
    result = search_for(query)
    if type(result) == str:
        return redirect("/wiki/" + result)
    return render_template("wiki.html", title="Search results", result=result, query=query)


@app.route("/post/<article_name>/", methods=["POST"])
def post(article_name):
    content = request.form["content"]
    pin = request.form["pin"]
    if article_name in config.protected_pages and pin != config.protected_pages_pin:
        abort(403)
    if content:
        save_edit(article_name, content)
        return redirect("/wiki/" + article_name)
    abort(500)


@app.route("/api/<req>/")
def api(req):
    if req == "list":
        return {key[0]: "/wiki/" + key[0] for key in get_rows()}
    abort(404)
