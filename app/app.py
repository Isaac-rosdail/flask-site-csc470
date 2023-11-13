from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy    # Init SQLAlchemy
from forms import RegisterForm, LoginForm  # Import register/login forms
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Not needed?
app.config['SECRET_KEY'] = 'corn'  # For Flask_WTF form(s)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "home"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Define models (User, Ticket)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(30), unique=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(30), unique=True) # email must be unique
    password = db.Column(db.String(30), nullable=False)
    role = db.Column(db.Integer)
    dept = db.Column(db.String(30))


class Ticket(db.Model):
    ticket_id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer) # get dept from finding user based on their user_id?
    title = db.Column(db.String(30))
    description = db.Column(db.String(100))
    location = db.Column(db.String(30))
    attachment = db.Column(db.String(30))


## GRANT SELECT ONLY, row level security? # Grant, select, # SELECT - view it, # Adding Tickets Table
# Init db & tables if needed
with app.app_context():
    db.create_all()


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() # Check if user is in db first
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('dashboard'))  # Changed redirect to profile page
    return render_template("home.html", form=form)
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
@app.route("/tickets/")
def tickets():
    return render_template("tickets.html")
@app.route("/submit_ticket/")
def submit_ticket():
    return render_template("submit_ticket.html")
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    # Validation & Saving to db
    if form.validate_on_submit():
        # Store stuff from form into database User entry
        new_user = User(username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('/register.html', form=form)
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run()
