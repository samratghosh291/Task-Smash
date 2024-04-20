#Imports
from flask import Flask, render_template, redirect,request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


#My App
app = Flask(__name__)
Scss(app)

#Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db= SQLAlchemy(app)

# Data Class ~ Row of Data  
class MyTask(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    complete =db.Column(db.Integer, default=0)
    created =db.Column(db.DateTime,default=datetime.utcnow)


    def __repr__(self)-> str:
        return f"Task{self.id}"
    
with app.app_context():
    db.create_all()
    

# Request to webpages 
# Home Page  
@app.route("/", methods=["GET","POST"])
def index():
    # Add the task  
    if request.method == "POST":
        current_content = request.form["content"]
        new_task = MyTask(content=current_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
        
    # Show the current task    
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks=tasks)
        


# Delete the task
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task= MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"


# Update the task
@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id:int):
    task= MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    else:
        return render_template('edit.html', task=task)






if __name__ in "__main__":
    app.run(debug=True)