import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


app = Flask(__name__)

##Connect to Database
app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    
##with app.app_context():
    ##db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    if request.method == 'POST':
        new_task = Tasks(text=request.form["task"])
        db.session.add(new_task)
        db.session.commit()
        all_tasks = Tasks.query.all()
        return render_template("index.html", date=today, task_list=all_tasks)
    all_tasks = Tasks.query.all()
    return render_template("index.html", date=today, task_list=all_tasks)

@app.route("/delete/<int:task_id>")
def delete(task_id):
    task_to_delete = Tasks.query.get(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect((url_for("home")))

if __name__ == '__main__':
    app.run(debug=True)
