from flask import Flask, render_template, request, url_for, redirect, session,flash
from datetime import timedelta,datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "flaskappsecret"
app.permanent_session_lifetime = timedelta(minutes=10)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False, unique=True)
    lname = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now())
    #password_hash = db.Column(db.String(128))


    def __repr__(self):
        return '<fname=%r>' % self.fname


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('base.html')
@app.route('/home')
def home():
    if "email" in session:
        fname = session["email"]
        return render_template("home.html", fname=fname)
    else:
        return render_template("home.html")
@app.route('/features')
def features():
    if "email" in session:
        fname = session["email"]
        return render_template("features.html", fname=fname)
    else:
        return render_template("features.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    if "email" not in session:
        if request.method == "POST":
            session.permanent = True
            email = request.form["email"]
            session["email"] = email
            return redirect(url_for("profile"))
        else:
            return render_template("login.html")
    else:
            return redirect(url_for("profile"))

@app.route("/profile")
def profile():
    if "email" in session:
        fname = session["email"]
        return render_template("user.html", fname=fname)
    else:
        return redirect(url_for("login"))
@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        return redirect(url_for("login"))
    else:
        return render_template("signup.html")
@app.route("/logout")
def logout():
    session.pop("email", None)
    session.pop("fname", None)  
    return redirect(url_for("login"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
        app.run(debug=True)


