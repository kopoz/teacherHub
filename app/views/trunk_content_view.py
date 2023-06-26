# backend/app/views/trunk_content_view.py
from flask import Blueprint, request, jsonify
from ..models import db, TrunkContent

trunk_content_api_bp = Blueprint('trunk_content_api_bp', __name__)

@trunk_content_api_bp.route('/api/v1/trunk_contents', methods=['POST'])
def create_trunk_content():
    data = request.get_json()
    new_trunk_content = TrunkContent(name=data['name'], 
                                     content=data['content'])
    db.session.add(new_trunk_content)
    db.session.commit()
    return jsonify(new_trunk_content.to_dict()), 201

@trunk_content_api_bp.route('/api/v1/trunk_contents', methods=['GET'])
def get_trunk_contents():
    trunk_contents = TrunkContent.query.all()
    return jsonify([trunk_content.to_dict() for trunk_content in trunk_contents])

@trunk_content_api_bp.route('/api/v1/trunk_contents/<id>', methods=['GET'])
def get_trunk_content(id):
    trunk_content = TrunkContent.query.get_or_404(id)
    return jsonify(trunk_content.to_dict())

@trunk_content_api_bp.route('/api/v1/trunk_contents/<id>', methods=['PUT'])
def update_trunk_content(id):
    data = request.get_json()
    trunk_content = TrunkContent.query.get_or_404(id)
    trunk_content.name = data['name']
    trunk_content.content = data['content']
    db.session.commit()
    return jsonify(trunk_content.to_dict())

@trunk_content_api_bp.route('/api/v1/trunk_contents/<id>', methods=['DELETE'])
def delete_trunk_content(id):
    trunk_content = TrunkContent.query.get_or_404(id)
    db.session.delete(trunk_content)
    db.session.commit()
    return '', 204
