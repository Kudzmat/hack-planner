from flask import Flask, render_template, request, redirect

app = Flask(__name__)

items = []


# create
@app.route('/add', methods=['POST'])
def add_item():
    item = request.form['item']
    items.append(item)

    return redirect('/')


# read
@app.route('/')
def checklist():
    return render_template('checklist.html', items=items)


# update endpoint
@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = items[item_id - 1]  # retrieve the item based on its index

    if request.method == 'POST':
        new_item = request.form['item']
        items[item_id - 1] = new_item  # update item with new value

        return redirect('/')

    return render_template('edit.html', item=item, item_id=item_id)


# delete
@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    del items[item_id - 1]  # delete item at the index
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)