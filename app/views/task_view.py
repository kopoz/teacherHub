# backend/app/views/task_view.py
from flask import Blueprint, request, jsonify, render_template
from ..models import db, Task

task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/tasks', methods=['GET'])
def tasks_view():
    tasks = Task.query.all()
    return render_template('tasks_view.html', tasks=tasks)

task_api_bp = Blueprint('task_api_bp', __name__)

@task_api_bp.route('/api/v1/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(name=data['name'], 
                    content=data['content'], 
                    related_links=data['related_links'], 
                    tags=data['tags'], 
                    targeted_school_year=data['targeted_school_year'], 
                    time_estimation=data['time_estimation'], 
                    objectives=data['objectives'], 
                    trunk_content=data['trunk_content'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@task_api_bp.route('/api/v1/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@task_api_bp.route('/api/v1/tasks/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict())

@task_api_bp.route('/api/v1/tasks/<id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    task = Task.query.get_or_404(id)
    task.name = data['name']
    task.content = data['content']
    task.related_links = data['related_links']
    task.tags = data['tags']
    task.targeted_school_year = data['targeted_school_year']
    task.time_estimation = data['time_estimation']
    task.objectives = data['objectives']
    task.trunk_content = data['trunk_content']
    db.session.commit()
    return jsonify(task.to_dict())

@task_api_bp.route('/api/v1/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return '', 204
