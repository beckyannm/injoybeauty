"""
Services routes for Jamie's Beauty Studio.
"""
from flask import Blueprint, jsonify, request
from models import Service

services_bp = Blueprint('services', __name__)


@services_bp.route('/api/services', methods=['GET'])
def get_services():
    """Get all services, optionally filtered by category."""
    category = request.args.get('category')
    
    if category:
        services = Service.get_by_category(category)
    else:
        services = Service.get_all()
    
    return jsonify(services)


@services_bp.route('/api/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    """Get a specific service by ID."""
    service = Service.get_by_id(service_id)
    
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    
    return jsonify(service)


@services_bp.route('/api/services/categories', methods=['GET'])
def get_categories():
    """Get list of service categories."""
    categories = Service.get_categories()
    return jsonify(categories)
