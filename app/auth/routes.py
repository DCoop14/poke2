from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import LoginForm, UserRegistrationForm

from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

from app.models import User

auth = Blueprint('auth', __name__, template_folder='authtemplates')

from app.models import db




@auth.route('/login',methods = ["GET","POST"] )
def logIn():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Your logged in!', 'success')
                    login_user(user)
                else:
                    flash('Incorrect username or password.', 'danger')
            else:
                flash('Username does not exist.', 'danger')

    return render_template('login.html', form=form)


@auth.route('/logout')
def logOut():
    flash("You logged out.", 'success')
    logout_user()
    return redirect(url_for('auth.logIn'))






@auth.route('/register', methods=["GET", "POST"])
def register():
    form = UserRegistrationForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data

            user = User(username, first_name, last_name, email, password)

            db.session.add(user)
            db.session.commit()
            flash("Successfully registered.", 'success')
            return redirect(url_for('auth.logIn'))
        else:
            flash('Please fill in all requirements!', 'danger')
    return render_template('register.html', form = form)