from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True)
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(120), nullable=False)  # path to file on server
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'path': self.path,
            'task_id': self.task_id,
        }

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=True)
    name = db.Column(db.String(120))
    targeted_school_year = db.Column(db.String(120))
    time_estimation = db.Column(db.Integer)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', 
        backref=db.backref('tasks', lazy=True))
    additional_files = db.relationship('File', backref='task', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'name': self.name,
            'targeted_school_year': self.targeted_school_year,
            'time_estimation': self.time_estimation,
        }