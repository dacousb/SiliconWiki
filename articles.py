import sqlite3 as sl
from table import get_rows
import markdown


class Article:
    title = None
    content = None
    found = False


class EscapeHtml(markdown.extensions.Extension):
    def extendMarkdown(self, md):
        md.preprocessors.deregister('html_block')
        md.inlinePatterns.deregister('html')


def get_article(article_name, raw=False):
    article_result = Article()
    for row in get_rows():
        if row[0].lower() == article_name.lower():
            article_result.title = row[0]
            if raw:
                article_result.content = row[1]
            else:
                article_result.content = markdown.markdown(
                    row[1], extensions=[EscapeHtml()])
            article_result.found = True
            break
    return article_result


def save_edit(title, content, new_article=False):
    con = sl.connect("articles.db")
    cur = con.cursor()
    if not new_article and title not in [row[0] for row in get_rows()]:
        return
    if new_article and title in [row[0] for row in get_rows()]:
        return
    try:
        cur.executemany("INSERT OR REPLACE INTO ARTICLES (title, content) values(?, ?)", [
                        (title, content)])
    except Exception as e:
        print("[!] Error updating database ->", e)
    con.commit()
    con.close()


def search_for(query):
    for row in get_rows():
        if row[0].lower() == query.lower():
            return row[0]
    result = []
    for row in get_rows():
        if query in row[0].lower():
            result.append(row[0])
    return result
