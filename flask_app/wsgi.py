# wsgi.py
from flaskapp import app
from extensions import db
from discord_bot.run import run as run_bot

__author__ = "Luke Oliver"
__version__ = "2.0.0"

# Make database and tables
with app.app_context():
    db.create_all()

run_bot()

if __name__ == "__main__":
    app.run()
