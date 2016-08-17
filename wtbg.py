#!/usr/bin/env python3

from flask import Flask, render_template
import os
import sqlite3

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'wtbg.db'),
))

# Logging! (http://stackoverflow.com/a/14042671)
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('wtbg_app.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s (%(levelname)s): %(message)s [line %(lineno)d'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def query_db(query, args=(), one=False):
    cur = connect_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    print("Initializing DB")
    with app.app_context():
        db = connect_db()
        db.execute("DROP TABLE IF EXISTS things")
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    print("DB Initialized")

@app.route('/')
def main():
    rows = query_db("SELECT * FROM things ORDER BY sent_at DESC")
    return render_template('index.html', rows=rows)

if __name__ == '__main__':
    app.run()
