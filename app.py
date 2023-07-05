from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

items = []
db_path = 'checklist.db'


# create table in database
def create_table():
    conn = sqlite3.connect(db_path)  # setting connection
    c = conn.cursor()  # instantiating cursor

    # specifying the format of the data which will be stored in checklist database
    c.execute('''CREATE TABLE IF NOT EXISTS checklist
    (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT)''')
    conn.commit()
    conn.close()  # close database


# select items from database
def get_items():
    conn = sqlite3.connect(db_path)  # setting connection
    c = conn.cursor()  # instantiating cursor
    c.execute("SELECT * FROM checklist")
    items = c.fetchall()
    conn.close()
    return items


def add_item(item):
    conn = sqlite3.connect(db_path)  # setting connection
    c = conn.cursor()  # instantiating cursor
    c.execute("INSERT INTO checklist (item) VALUES (?)", (item,))
    conn.commit()
    conn.close()


def update_item(item_id, new_item):
    conn = sqlite3.connect(db_path)  # setting connection
    c = conn.cursor()  # instantiating cursor
    c.execute("UPDATE checklist SET item = ? WHERE id = ?", (new_item, item_id))
    conn.commit()
    conn.close()


def delete_item(item_id):
    conn = sqlite3.connect(db_path)  # setting connection
    c = conn.cursor()  # instantiating cursor
    c.execute("DELETE FROM checklist WHERE id = ?", (item_id,))


# create
@app.route('/add', methods=['POST'])
def add_task():
    item = request.form['item']
    add_item(item)  # add item to database
    return redirect('/')


# read
@app.route('/')
def checklist():
    create_table()  # create table
    items = get_items()  # get items from table
    return render_template('checklist.html', items=items)


# update endpoint
@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_task(item_id):
    if request.method == 'POST':
        new_item = request.form['item']
        update_item(item_id, new_item)
        return redirect('/')

    else:
        items = get_items()
        # we want to associate our tasks (items) with their id in case there are duplicate tasks
        item = next((x[1] for x in items if x[0] == item_id), None)
        return render_template('edit.html', item=item, item_id=item_id)


# delete
@app.route('/delete/<int:item_id>')
def delete_task(item_id):
    delete_item(item_id)  # delete item from database
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
