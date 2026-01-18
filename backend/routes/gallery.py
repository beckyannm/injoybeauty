"""
Gallery routes for Jamie's Beauty Studio.
"""
from flask import Blueprint, jsonify, request
from models import GalleryImage

gallery_bp = Blueprint('gallery', __name__)


@gallery_bp.route('/api/gallery', methods=['GET'])
def get_gallery():
    """Get all gallery images."""
    category = request.args.get('category')
    
    if category:
        images = GalleryImage.get_by_category(category)
    else:
        images = GalleryImage.get_all()
    
    return jsonify(images)


@gallery_bp.route('/api/gallery/featured', methods=['GET'])
def get_featured():
    """Get featured gallery images for homepage."""
    images = GalleryImage.get_featured()
    return jsonify(images)


@gallery_bp.route('/api/gallery/categories', methods=['GET'])
def get_categories():
    """Get list of gallery categories."""
    images = GalleryImage.get_all()
    categories = list(set(img['category'] for img in images if img['category']))
    return jsonify(sorted(categories))
