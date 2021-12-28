import re
from flask import Flask, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask.templating import render_template
from datetime import datetime

from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(250), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def report(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Error adding task."
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/')

    except:
        return "Unable to delete task"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        # update_content = request.form['content']
        task.content = request.form['content']
        # updated_task = Todo(content=update_content)

        try:
            # db.session.add(updated_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Error updating task."
    else:
        return render_template('update.html', task=task)

    # try:
    #     db.session.u(task_update)
    #     db.session.commit()
    #     return redirect('/')

    # except:
    #     return "Unable to delete task"


if __name__ == "__main__":
    app.run(debug=True)
