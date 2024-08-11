from flask import Flask, render_template, request, flash, session, redirect, url_for, Blueprint, jsonify
from flask_login import login_user, current_user, login_required, logout_user

from werkzeug.security import generate_password_hash, check_password_hash
from extensions import basic_auth, db
from models import Customer, Site, Field, User, Invite
import uuid
account = Blueprint('account', __name__)

def validate_data(*fields):
    """Check if any of the provided fields are empty."""
    return any(field.strip() == "" for field in fields)

@account.route("/")
@account.route("/login", methods=['GET'])
def get_login():
    if current_user.is_authenticated:
        return redirect(url_for('start_time.main'))
    
    return render_template("account/login.html")

@account.route("/login", methods=["POST"])
def post_login():
    if current_user.is_authenticated:
        return redirect(url_for('start_time.main'))

    username = request.form.get("username", "").strip().lower()
    password = request.form.get("password", "").strip()

    if validate_data(username, password):
        flash('Invalid username or password')
        return redirect(url_for('account.get_login'))

    user = db.session.query(User).filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        login_user(user, remember=True)
        return redirect(url_for('start_time.main'))

    flash('Invalid username or password')
    return redirect(url_for('account.get_login'))
    

@account.route("/register", methods=["GET"])
def get_register():
    if current_user.is_authenticated:
        return redirect(url_for('start_time.main'))
    return render_template("account/register.html")

@account.route("/register", methods=["POST"])
def post_register():
    if current_user.is_authenticated:
        return redirect(url_for('start_time.main'))

    username = request.form.get("username", "").strip().lower()
    password = request.form.get("password", "").strip()
    invite_code = request.form.get("invite_code", "").strip()

    if validate_data(username, password, invite_code):
        flash('Invalid username, password, or invite code. Please try again.')
        return redirect(url_for('account.get_register'))

    invite = db.session.query(Invite).filter_by(invite_code=invite_code).first()
    if not invite or invite.is_redeemed:
        flash('Invite code is invalid or has already been used.')
        return redirect(url_for('account.get_register'))

    if db.session.query(User).filter_by(username=username).first():
        flash('Username already taken.')
        return redirect(url_for('account.get_register'))

    hashed_password = generate_password_hash(password, method='scrypt')

    new_user = User(
        uuid=str(uuid.uuid4()),
        username=username,
        password=hashed_password,
        privileges="user"
    )
    db.session.add(new_user)
    invite.is_redeemed = True

    db.session.commit()
    login_user(new_user)

    return redirect(url_for('start_time.main'))

# Expand on this later
@account.route("/generate_invite", methods=["GET"])
@login_required
def generate_invite():
    if current_user.privileges == "admin":
        invite_code = str(uuid.uuid4())
        new_invite = Invite(invite_code=invite_code)
        db.session.add(new_invite)
        db.session.commit()
        return jsonify({"code": 0, "invite_code": invite_code})
    else:
        return jsonify({"code": 1, "error": "You do not have permission to do that"})


@account.route("/logout", methods=["GET"])
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('account.get_login'))

@account.route("/change_password", methods=["GET"])
@login_required
def get_change_password():
    return render_template("account/change_password.html")


@account.route("/change_password", methods=["POST"])
@login_required
def post_change_password():
    current_password = request.form.get("currentPassword", "")
    new_password = request.form.get("newPassword", "") 
    
    if validate_data(current_password, new_password):
        flash('Invalid password provided')
        return redirect(url_for('start_time.main'))
    
    if not check_password_hash(current_user.password, current_password):
        flash('Invalid password provided')
        return redirect(url_for('start_time.main'))
    
    hashed_password = generate_password_hash(new_password, method='scrypt')
    current_user.password = hashed_password
    db.session.commit()
    
    flash('Password changed succesfully. Please log in again.')
    logout_user()
    return redirect(url_for('account.get_login'))
    