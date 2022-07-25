from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///./mydata.db'
db = SQLAlchemy(app)

class todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),unique=True,nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<id %r>' %self.id

@app.route("/",methods=['GET','POST'])
def index():
    if request.method == 'POST':
        task_name = request.form['content']
        new_task = todo(name=task_name)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue in adding task"
    else:
        tasks = todo.query.order_by(todo.date_created).all()
        return render_template("index.html",tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem in deleting task"

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task_to_update = todo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.name = request.form['content']
        try:
            db.session.commit()
            return redirect('/')

        except:
            return "There was a problem in updating"
    else:
        return render_template('update.html', task=task_to_update)
if __name__=='__main__':
    app.run(debug=True)