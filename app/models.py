from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

_trunk_contents = db.Table('trunk_contents',
                           db.Column('trunkcontent_id', db.Integer, db.ForeignKey(
                               'trunk_content.id'), primary_key=True),
                           db.Column('task_id', db.Integer, db.ForeignKey(
                               'task.id'), primary_key=True)
                           )

_objectives = db.Table('objectives',
                       db.Column('objective_id', db.Integer, db.ForeignKey(
                           'objective.id'), primary_key=True),
                       db.Column('task_id', db.Integer, db.ForeignKey(
                           'task.id'), primary_key=True)
                       )

_labels = db.Table('labels',
                       db.Column('label_id', db.Integer, db.ForeignKey(
                           'label.id'), primary_key=True),
                       db.Column('task_id', db.Integer, db.ForeignKey(
                           'task.id'), primary_key=True)
                       )


class TrunkContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Objective(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

class Label(db.Model):
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
    targeted_school_year = db.Column(db.String(120))
    time_estimation = db.Column(db.Integer)
    trunk_contents = db.relationship('TrunkContent', secondary=_trunk_contents, lazy='subquery',
                                     backref=db.backref('tasks', lazy=True))
    objectives = db.relationship('Objective', secondary=_objectives, lazy='subquery',
                                 backref=db.backref('tasks', lazy=True))
    labels = db.relationship('Label', secondary=_labels, lazy='subquery',
                                 backref=db.backref('tasks', lazy=True))
    additional_files = db.relationship('File', backref='task', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'targeted_school_year': self.targeted_school_year,
            'time_estimation': self.time_estimation,
        }
