from flask import Flask, g, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'db/database'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def show_students():
    db = get_db()
    cur = db.cursor()
    cur.execute("select * from students")
    rows = cur.fetchall()
    return render_template('index.html', rows=rows)


@app.route('/add', methods=["POST"])
def add_post():
    db = get_db()
    cur = db.cursor()
    sql = "INSERT INTO students(name) VALUES (?)"
    value = (request.form['student'],)
    cur.execute(sql, value)
    db.commit()
    return redirect(url_for('show_students'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
