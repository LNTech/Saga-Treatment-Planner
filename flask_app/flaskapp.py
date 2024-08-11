# flaskapp.py
from flask import Flask, render_template, redirect, url_for, request, flash, session
from extensions import basic_auth, db
from blueprints.start_time import start_time
from blueprints.account import account
from werkzeug.security import generate_password_hash
from models import User
import uuid
from flask_login import LoginManager, login_user, current_user
from discord_bot.run import run as run_bot
app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = ''
app.config['BASIC_AUTH_PASSWORD'] = ''
basic_auth.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.secret_key = "devkey"
app.config['SESSION_TYPE'] = 'filesystem'

login_manager = LoginManager()
login_manager.login_view = 'account.get_login'
login_manager.init_app(app)

app.register_blueprint(start_time, url_prefix="/start-time/")
app.register_blueprint(account, url_prefix="/account/")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=["GET"])
def index():
    user_exists = db.session.query(User.id).first()
    if user_exists is None:
        return redirect(url_for('post_setup'))
    return render_template("index.html")
    

@app.route("/setup", methods=["GET"])
def get_setup():
    user_exists = db.session.query(User.id).first()
    if user_exists:
        return redirect(url_for('index'))
    return render_template("setup.html")


@app.route("/setup", methods=["POST"])
def post_setup():
    user_exists = db.session.query(User.id).first()
    if user_exists:
        return redirect(url_for('index'))
        
    username = request.form.get("username")
    password = request.form.get("password")

    if username == "" or username is None:
        flash('Invalid username')
        return redirect(url_for('get_setup'))
    
    hashed_password = generate_password_hash(password, method='scrypt')
    new_user = User(uuid=str(uuid.uuid4()), username=username, password=hashed_password, privileges="admin")
    db.session.add(new_user)
    db.session.commit()
    db.session.refresh(new_user)
    login_user(new_user)
    return redirect(url_for('start_time.main'))

if __name__ == "__main__":
    run_bot()
    with app.app_context():
        db.create_all()
    app.run(debug=True)