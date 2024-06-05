from flaskapp import app
from extensions import db

__author__ = "Luke Oliver"
__version__ = "1.0.0"

# Make database and tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
