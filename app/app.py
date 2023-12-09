from flask import Flask, render_template, request, redirect, url_for
from forms import RegisterForm, LoginForm, TicketForm  # Import forms from forms.py
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy  # Init SQLAlchemy
from flask_paginate import Pagination

app = Flask(__name__)
app.secret_key = 'corn'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Not needed?
app.config['SECRET_KEY'] = 'corn'  # For Flask_WTF form(s)
db = SQLAlchemy(app)

# Setup for persistent login sessions across site/app
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "home"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


# Define models (User, Ticket)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(30), unique=True)  # email must be unique
    password = db.Column(db.String(30), nullable=False)
    role = db.Column(db.Integer)
    dept = db.Column(db.String(30))


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.String(30))  # get dept from finding user based on their user_id?
    assigned_to = db.Column(db.String(30))
    status = db.Column(db.String(30))
    priority = db.Column(db.String(30))
    dept = db.Column(db.String(30))
    title = db.Column(db.String(30))
    description = db.Column(db.String(100))
    location = db.Column(db.String(30))
    attachment = db.Column(db.String(30))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    content = db.Column(db.String(30))

# Init db & tables if needed
with app.app_context():
    db.create_all()


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")


@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    # Check for user in db, if password matches, redirect to dashboard template
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template("home.html", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # Store form info as new user
        new_user = User(name=form.name.data,
                        username=form.username.data,
                        email=form.email.data,
                        password=form.password.data,
                        role=form.role.data,
                        dept=form.dept.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('register.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


def filter_tickets(username,filter_type):
    if filter_type=='created':
        ticket_list = Ticket.query.filter_by(created_by=username).all()
        #print(ticket_list[0].created_by)
        return ticket_list
    elif filter_type=='assigned':
        ticket_list = Ticket.query.filter_by(assigned_to=username).all()
        return ticket_list
    else:
        if current_user.role==2:
            ticket_list = Ticket.query.all()
        else:
            ticket_list = Ticket.query.filter_by(dept=current_user.dept).all()
    return ticket_list

# Pagination settings
PER_PAGE = 5  # Number of tickets per page

@app.route("/tickets", methods=['GET', 'POST'])
@login_required
def tickets():
    
    username = request.args.get('username','admin')
    filter_type = request.args.get('filter_type', 'all')
    user_tickets = filter_tickets(username, filter_type)
    
    page = int(request.args.get('page', 1))
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    pagination = Pagination(page=page, total=len(user_tickets), per_page=PER_PAGE, css_framework='bootstrap4')
    
    #print(user_tickets[0])
    return render_template('tickets.html', tickets=user_tickets[start:end],pagination=pagination)

@app.route("/users", methods=['GET', 'POST'])
@login_required
def users():
    user_list = User.query.all()
    
    page = int(request.args.get('page', 1))
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    pagination = Pagination(page=page, total=len(user_list), per_page=PER_PAGE, css_framework='bootstrap4')
    
    #print(user_tickets[0])
    return render_template('users.html', users=user_list)


@app.route("/submit_ticket", methods=['GET', 'POST'])
@login_required
def submit_ticket():
    form = TicketForm()

    if current_user.role==0:
        del form.priority
        del form.status

    # Pre-fill 'created_by' field
    if request.method == 'GET':
        form.created_by.data = current_user.username

    if form.validate_on_submit():
        # Store form data as new ticket
        new_ticket = Ticket(created_by=form.created_by.data,
                            title=form.title.data,
                            assigned_to = form.assigned_to.default,
                            status=getattr(form, 'status', None) and form.status.data or 'Open',
                            priority=getattr(form, 'priority', None) and form.priority.data or 'Low',
                            description=form.description.data,
                            location=form.location.data,
                            attachment=form.attachment.data)
        
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for('tickets'))

    return render_template("submit_ticket.html", form=form)


@app.route('/edit_ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)  # Grab ticket based on ticket_id match
    form = TicketForm(obj=ticket)

    # Fill form with data from current ticket
    if form.validate_on_submit():
        ticket.dept = form.dept.data
        ticket.title = form.title.data
        ticket.assigned_to = form.assigned_to.data
        ticket.status = form.status.data
        ticket.priority = form.priority.data
        ticket.description = form.description.data
        ticket.location = form.location.data
        ticket.attachment = form.attachment.data

        db.session.commit()  # Save any changes
        return redirect(url_for('tickets'))

    return render_template('edit_ticket.html', form=form)

@app.route('/_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)  # Grab a user based on user_id match
    form = RegisterForm(obj=User)

    if form.validate_on_submit():
        # Update form info for user
        user = User(name=form.name.data,
                        username=form.username.data,
                        email=form.email.data,
                        role=form.role.data,
                        dept=form.dept.data)
        db.session.commit()
        return redirect(url_for('users'))

    return render_template('modify_user.html', form=form)


@app.route('/delete_ticket/<int:ticket_id>', methods=['GET','POST'])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)  # Grab ticket based on ticket_id match

    db.session.delete(ticket)
    db.session.commit()  # Save any changes

    return redirect(url_for('tickets'))

@app.route('/delete_user/<int:user_id>', methods=['GET','POST'])
@login_required
def delete_user(user_id):
    user = Ticket.query.get_or_404(user_id)  # Grab user based on user_id match

    db.session.delete(user)
    db.session.commit()  # Save any changes

    return redirect(url_for('users'))

@app.route('/ticket/<int:ticket_id>')
def view_ticket(ticket_id):
    # Retrieve the ticket details from the database based on the ticket_id
    ticket = Ticket.query.get_or_404(ticket_id)
    
    # For simplicity, assuming there's a 'comments' attribute in the Ticket model
    comments = Comment.query.filter_by(ticket_id=ticket_id).all()

    return render_template('ticket_detail.html', ticket=ticket, comments=comments)

if __name__ == '__main__':
    app.run()
