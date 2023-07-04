# backend/app/views/task_view.py
from flask import send_from_directory
from flask import Blueprint, request, jsonify, render_template
from ..models import db, Task, TrunkContent, Objective, File
from werkzeug.utils import secure_filename
import os

# make sure your app knows where to find the uploaded files
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

# Make sure to configure the allowed file types
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/tasks', methods=['GET'])
def tasks_view():
    tasks = Task.query.all()
    return render_template('tasks_view.html', tasks=tasks)


task_api_bp = Blueprint('task_api_bp', __name__)

@task_api_bp.route('/api/v1/tasks', methods=['POST'])
def create_task():
    content = request.form.get('content')
    targeted_school_year = request.form.get('targeted_school_year')
    time_estimation = request.form.get('time_estimation')
    additional_files = request.files.getlist('additional_files[]')

    new_task = Task(
        content=content,
        targeted_school_year=targeted_school_year,
        time_estimation=time_estimation,
    )

    objectives = request.form.getlist('objectives[]')
    for name in objectives:
        objective = Objective.query.filter_by(name=name).first()
        if not objective:
            objective = Objective(name=name)
            db.session.add(objective)
        new_task.objectives.append(objective)

    trunk_contents = request.form.getlist('trunk_contents[]')
    for name in trunk_contents:
        trunk_content = TrunkContent.query.filter_by(name=name).first()
        if not trunk_content:
            trunk_content = TrunkContent(name=name)
            db.session.add(trunk_content)
        new_task.trunk_contents.append(trunk_content)

    if additional_files:
        filenames = []
        for file in additional_files:
            if file and allowed_file(file.filename):
                file_path = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, file_path))
                filenames.append(file_path)

                new_file = File(
                    path=file_path,
                    task=new_task
                )

                db.session.add(new_file)

    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.to_dict()), 201


@task_api_bp.route('/api/v1/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])


@task_api_bp.route('/api/v1/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict())


@task_api_bp.route('/api/v1/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    task.content = data.get('content')
    task.name = data.get('name')
    task.targeted_school_year = data.get('targeted_school_year')
    task.time_estimation = data.get('time_estimation')
    db.session.commit()
    return jsonify(task.to_dict())


@task_api_bp.route('/api/v1/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return '', 204




@task_api_bp.route('/files/<filename>')
def get_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


@task_api_bp.route('/api/v1/objectives', methods=['GET'])
def get_objectives():
    query = request.args.get('q', '')
    objectives = Objective.query.filter(Objective.name.like(f'%{query}%')).all()
    return jsonify(objectives=[objective.to_dict() for objective in objectives])

@task_api_bp.route('/api/v1/trunk_contents', methods=['GET'])
def get_trunk_contents():
    query = request.args.get('q', '')
    trunk_contents = TrunkContent.query.filter(TrunkContent.name.like(f'%{query}%')).all()
    return jsonify(trunk_contents=[trunk_content.to_dict() for trunk_content in trunk_contents])
