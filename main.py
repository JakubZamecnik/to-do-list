import os
from flask import Flask, render_template, request, url_for, redirect
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, DateTime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)

db_path = os.path.join(app.instance_path, 'tasks.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(app)

class Task(db.Model):
    __tablename__ = 'task'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250))
    description: Mapped[str | None] = mapped_column(String(250), nullable=True)
    date_of_issue: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task = Task(
            title=request.form['title'],
            description=request.form['description'],
            due_date=datetime.strptime(request.form['due_date'], '%Y-%m-%d')
        )
        db.session.add(task)
        db.session.commit()

    tasks = Task.query.all()
    now = datetime.utcnow()
    return render_template('index.html', tasks=tasks, now=now)

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = True
        db.session.delete(task)  # smaže task z databáze
        db.session.commit()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
