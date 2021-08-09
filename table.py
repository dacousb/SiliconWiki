import sys
import sqlite3 as sl


def get_rows():
    result = []
    con = sl.connect("articles.db")
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM ARTICLES")
    for row in rows:
        result.append(row)
    con.close()
    return result


def loaddb():
    # -db argument creates a new blank database
    con = sl.connect("articles.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS ARTICLES;")
    cur.execute("""
        CREATE TABLE ARTICLES (
            title TEXT UNIQUE,
            content TEXT
        );
    """)
    sql = "INSERT INTO ARTICLES (title, content) values(?, ?)"
    data = [
        ("Main",
         "SiliconWiki and its database have been successfully installed on this web server.  \n\
You can start creating and editing articles as in any other wiki software.\n\
### Welcome!\n\
You can start searching for articles with the search bar, you can also edit them!  \n\
To create a new article, search for the name of the article in the search bar,  \n\
you will be asked if you want to create it at the bottom.\n\
### Start using the API\n\
This web server incorporates a small API with the following requests available:\n\n\
* [/api/list](/api/list), lists all articles created in real time")
    ]
    cur.executemany(sql, data)

    rows = cur.execute("SELECT * FROM ARTICLES")
    for row in rows:
        print(row)

    con.commit()
    con.close()


if len(sys.argv) == 2:
    if sys.argv[1] == "-db":
        if input("This can break your current articles.db database! Continue? (y/N) ").lower() == "y":
            loaddb()
        else:
            print("No changes were made")
    else:
        print(" * Table module loaded, are you running this yourself? Create a blank database with -db")
else:
    print("Create a blank database with -db")
