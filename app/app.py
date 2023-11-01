from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy    # Init SQLAlchemy
from sqlalchemy.exc import IntegrityError  # Throw error
from forms import LoginForm, SignupForm # import signup/login forms defined in forms.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Not needed?
app.config['SECRET_KEY'] = 'corn'  # For Flask_WTF form(s)

db = SQLAlchemy(app)

# app.app_context().push() # needed to fix weird glitch, idk


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(30), unique=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(30), unique=True) # email must be unique
    password = db.Column(db.String(30))


# Init db & tables if needed
with app.app_context():
    db.create_all()


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
@app.route("/", methods=['GET', 'POST'])
def home():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        # Verify login info
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return redirect(url_for('dashboard')) # Redirect to user dashboard
        else:
            error = "No success."
    return render_template("home.html", error=error, form=form)
@app.route("/tickets/")
def tickets():
    return render_template("tickets.html")
@app.route("/submit_ticket/")
def submit_ticket():
    return render_template("submit_ticket.html")
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    # Validation & Saving to db
    if form.is_submitted():
        try:
            result = request.form  # this line gives us access to the form data :P

            # Store stuff from form into database User entry
            new_user = User(username=form.username.data,
                            email=form.email.data,
                            password=form.password.data)
            db.session.add(new_user)
            db.session.commit()

            users = User.query.all()
            return render_template('user.html', users=users, result=result)
        # If repeat username, don't accept. Add input validation?
        except IntegrityError:
            db.session.rollback()
            return render_template('signup.html', form=form)
    return render_template('signup.html', form=form)

if __name__ == '__main__':
    app.run()
