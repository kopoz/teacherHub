# backend/app/views/objective_view.py
from flask import Blueprint, request, jsonify
from ..models import db, Objective

objective_bp = Blueprint('objective_bp', __name__)

@objective_bp.route('/objectives', methods=['POST'])
def create_objective():
    data = request.get_json()
    new_objective = Objective(name=data['name'], 
                              content=data['content'])
    db.session.add(new_objective)
    db.session.commit()
    return jsonify(new_objective.to_dict()), 201

@objective_bp.route('/objectives', methods=['GET'])
def get_objectives():
    objectives = Objective.query.all()
    return jsonify([objective.to_dict() for objective in objectives])

@objective_bp.route('/objectives/<id>', methods=['GET'])
def get_objective(id):
    objective = Objective.query.get_or_404(id)
    return jsonify(objective.to_dict())

@objective_bp.route('/objectives/<id>', methods=['PUT'])
def update_objective(id):
    data = request.get_json()
    objective = Objective.query.get_or_404(id)
    objective.name = data['name']
    objective.content = data['content']
    db.session.commit()
    return jsonify(objective.to_dict())

@objective_bp.route('/objectives/<id>', methods=['DELETE'])
def delete_objective(id):
    objective = Objective.query.get_or_404(id)
    db.session.delete(objective)
    db.session.commit()
    return '', 204
