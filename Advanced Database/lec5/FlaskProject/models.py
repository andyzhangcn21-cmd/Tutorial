from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserInput(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
