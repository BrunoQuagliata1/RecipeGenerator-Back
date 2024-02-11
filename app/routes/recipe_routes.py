from flask import Blueprint, request, jsonify
from app.services.openai_service import query_gpt3
from ..models.models import Recipe, Tag
from .. import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import request, jsonify
from sqlalchemy import distinct, func


recipe_bp = Blueprint('recipe_bp', __name__)


@recipe_bp.route('/recipe', methods=['GET'])
def get_recipe():
    food_name = request.args.get('name')
    tag_names = request.args.get('tags')  # Tags are expected to be comma-separated

    query = Recipe.query

    if food_name:
        query = query.filter(Recipe.name.ilike(f"%{food_name}%"))

    if tag_names:
        tags_list = [tag.strip() for tag in tag_names.split(',')]  # Ensure tags are stripped of whitespace
        # Join with Tag and count the number of matches for each Recipe
        query = query.join(Recipe.tags).filter(Tag.name.in_(tags_list))
        query = query.group_by(Recipe.id).having(func.count(distinct(Tag.id)) == len(tags_list))

    recipes = query.all()

    if recipes:
        data = [{
            "name": recipe.name,
            "ingredients": recipe.ingredients,
            "steps": recipe.steps,  # Assuming you might also want to include steps
            "tags": [tag.name for tag in recipe.tags]
        } for recipe in recipes]
        return jsonify(data)
    else:
        return jsonify({"error": "Recipe not found"}), 404


@recipe_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

