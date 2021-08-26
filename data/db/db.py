import sqlite3
def makedb():
    conn = sqlite3.connect("./data/db/database.db")
    c=conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS warning(
            userid integer PRIMARY KEY,
            warns integer
            )""")
    conn.commit()
    conn.close()
def newuser(userid):
        conn = sqlite3.connect("./data/db/database.db")
        c=conn.cursor()
        c.execute("INSERT INTO warning VALUES (?,?)",(userid,0))
        conn.commit()
        conn.close()
def addwarn(userid):
        conn = sqlite3.connect("./data/db/database.db")
        c=conn.cursor()
        c.execute(f"SELECT warns FROM warning WHERE userid={userid}")
        warn=c.fetchone()
        newwarn=warn[0]+1
        c.execute(f"UPDATE warning SET warns={newwarn} WHERE userid={userid}")
        conn.commit()
        conn.close()
        return newwarn