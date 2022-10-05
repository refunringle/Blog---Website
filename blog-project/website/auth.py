from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import db,User
from flask_login import login_user, logout_user, login_required,current_user
from werkzeug.security import generate_password_hash, check_password_hash




auth = Blueprint("auth", __name__)




# user login 

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully..", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect.', category='error')
                return render_template("login.html"),400
        else:
            flash('Email does not exist.', category='error')
            return render_template("login.html"),404

    return render_template("login.html")






# user registration

@auth.route("/signup", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password")
        password2 = request.form.get("repeat_password")
        

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email is already in use!', category='error')
            return render_template("registration.html"),409
        elif email == "":
            flash("Email shouldn't be empty!", category='error')
            return render_template("registration.html"),204
        elif username_exists:
            flash('Username is already in use!', category='error')
            return render_template("registration.html"),409
        elif password1 != password2:
            flash('Password don\'t match!', category='error')
            return render_template("registration.html"),401
        elif len(username) < 2:
            flash('Username is too short!', category='error')
            return render_template("registration.html"),400
        elif len(password1) <= 6:
            flash('Password is too short!', category='error')
            return render_template("registration.html"),400


        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created! Please login to continue')
            return redirect(url_for('auth.login'))

    return render_template("registration.html")





# user logout

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('logout successfully..',category='success')
    return redirect(url_for("views.home"))



#user email updation

@auth.route("/email", methods=['POST',])
def update_email():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        new_email = request.form.get("newEmail")

        user = User.query.filter_by(email=email).first()
        
        old_name=current_user.username
        old_id=current_user.id
        old_pass=current_user.password

        if new_email == "":
            flash("Email shouldn't be empty!", category='error')
            return render_template("dashboard.html"),204
        elif len(new_email) < 11:
            flash('Email is too short!', category='error')
            return render_template("dashboard.html"),400
        else:
            new_user=User(id=old_id,email=new_email,username=old_name,password=old_pass)
            if user:
                if user.email == new_email:
                    flash("Already in use, please enter different email..!", category="error")
                    return redirect(url_for('views.user_dashboard',id=current_user.id,username=current_user.username))
                if check_password_hash(user.password, password):
                    flash("Email updated successfully..", category='success')
                    db.session.merge(new_user)
                    db.session.commit()
                    login_user(new_user, remember=True)
                    return redirect(url_for('views.user_dashboard',id=current_user.id,username=current_user.username))
                else:
                    flash('Password is incorrect.', category='error')
            else:
                flash('Email does not exist.', category='error')

    return redirect(url_for('views.user_dashboard',id=current_user.id,username=current_user.username))





#user username updation

@auth.route("/username", methods=['POST',])
@login_required
def update_username():
    if request.method == 'POST':
        email = request.form.get("userNameEmail")
        password = request.form.get("password_")
       
        new_username = request.form.get("newUser")
        user = User.query.filter_by(email=email).first()

        
        old_id=current_user.id
        old_pass=current_user.password
        
        if new_username == "":
            flash("Username shouldn't be empty!", category='error')
        elif len(new_username) < 3:
            flash('Username is too short!', category='error')
        else:
            new_user=User(id=old_id,email=email,username=new_username,password=old_pass)
            if user:
                if user.username == new_username:
                    flash('Username already exists', category='error')
                    return redirect(url_for('views.user_dashboard',id=current_user.id,username=current_user.username))
                if check_password_hash(user.password, password):
                    flash("username updated successfully..", category='success')
                    db.session.merge(new_user)
                    db.session.commit()
                    login_user(new_user, remember=True)
                    return redirect(url_for('views.user_dashboard',id=current_user.id,username=current_user.username))
                else:
                    flash('Password is incorrect.', category='error')
            else:
                flash('Email does not exist.', category='error')

    return redirect(url_for('views.user_dashboard',id=current_user.id,username=current_user.username))




# user password updation

@auth.route("/password", methods=['POST',])
@login_required
def update_password():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        new_password = request.form.get("newPassword")
        confirm_password = request.form.get("repeat_password")

        user = User.query.filter_by(email=email).first()

        old_id=current_user.id
        old_name=current_user.username
        old_email=current_user.email        
        
        new_user=User(id=old_id,email=old_email,username=old_name,
                password=generate_password_hash(
                new_password, method='sha256'))
        
        if user:
            if new_password != confirm_password:
                flash('Password don\'t match!', category='error')
            elif len(new_password) <= 6:
                flash('Password is too short!', category='error')

            elif check_password_hash(user.password, password):
                flash("password updated successfully..", category='success')
                db.session.merge( new_user )
                db.session.commit()
                login_user( new_user, remember=True)
                return redirect(url_for('views.user_dashboard',id=current_user.id,username=current_user.username))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return redirect(url_for('views.user_dashboard',id=current_user.id,username=current_user.username))
