# backend/app/views/course_view.py
from flask import Blueprint, request, jsonify, redirect, render_template, flash, url_for
from ..models import db, Course

course_bp = Blueprint('course_interface', __name__)

# @course_bp.route('/courses', methods=['GET', 'POST'])
@course_bp.route('/courses', methods=['GET'])
def courses():
    # if request.method == 'POST':
    #     name = request.form['name']
    #     schedule = request.form['schedule']
    #     year = request.form['year']
    #     general_appraisal = request.form['general_appraisal']
    #     new_course = Course(name=name, schedule=schedule, year=year, general_appraisal=general_appraisal)
    #     db.session.add(new_course)
    #     db.session.commit()
    #     flash('New course was successfully created')
    #     return redirect(url_for('course_bp.get_courses'))

    # if it is not POST it must be a GET
    courses = Course.query.all()
    return render_template('course_view.html', courses=courses)


course_api_bp = Blueprint('course_api', __name__)

@course_api_bp.route('/api/v1/courses', methods=['POST'])
def create_course():
    data = request.get_json()
    new_course = Course(name=data['name'], 
                        schedule=data['schedule'], 
                        year=data['year'], 
                        general_appraisal=data['general_appraisal'])
    db.session.add(new_course)
    db.session.commit()
    return jsonify(new_course.to_dict()), 201

@course_api_bp.route('/api/v1/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses])

@course_api_bp.route('/api/v1/courses/<id>', methods=['GET'])
def get_course(id):
    course = Course.query.get_or_404(id)
    return jsonify(course.to_dict())

@course_api_bp.route('/api/v1/courses/<id>', methods=['PUT'])
def update_course(id):
    data = request.get_json()
    course = Course.query.get_or_404(id)
    course.name = data['name']
    course.schedule = data['schedule']
    course.year = data['year']
    course.general_appraisal = data['general_appraisal']
    db.session.commit()
    return jsonify(course.to_dict())

@course_api_bp.route('/api/v1/courses/<id>', methods=['DELETE'])
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return '', 204