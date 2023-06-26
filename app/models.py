from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    targeted_school_year = db.Column(db.Integer, nullable=False)
    time_estimation = db.Column(db.Integer)
    objectives = db.Column(db.String(255))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    # Relationship fields
    related_links = db.relationship('RelatedLink', backref='task', lazy=True)
    tags = db.relationship('Tag', backref='task', lazy=True)
    trunk_contents = db.relationship('TrunkContent', backref='task', lazy=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class RelatedLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(255), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(100), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TrunkContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    schedule = db.Column(db.String(100), nullable=False)
    general_appraisal = db.Column(db.Text)
    # teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    tasks = db.relationship('Task', backref='course', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "year": self.year,
            "schedule": self.schedule,
            "general_appraisal": self.general_appraisal
            # and so on for the other fields
        }


class Objective(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    scoring = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
