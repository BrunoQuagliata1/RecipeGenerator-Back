import pandas as pd
from app import create_app, db
from app.models.models import Recipe, Tag
from tqdm import tqdm  # Import tqdm for progress bar

def populate_db_from_csv(csv_path):
    app = create_app()
    with app.app_context():  # Context management for the application
        recipes_df = pd.read_csv(csv_path)
        recipes_df = recipes_df[['name', 'ingredients', 'steps', 'tags']]
        recipes_df['name'] = recipes_df['name'].fillna("")

        # Fetch existing recipes and tags to minimize database queries
        existing_recipes = {recipe.name for recipe in Recipe.query.all()}
        existing_tags = {tag.name: tag for tag in Tag.query.all()}

        progress_bar = tqdm(recipes_df.iterrows(), total=len(recipes_df), desc="Importing Recipes", unit="recipe")
        
        for _, row in progress_bar:
            if row['name'] not in existing_recipes:
                recipe = Recipe(
                    name=row['name'],
                    ingredients=row['ingredients'],
                    steps=row['steps']
                )

                tag_names = row['tags'].split(',') if pd.notnull(row['tags']) else []
                for tag_name in tag_names:
                    tag_name = tag_name.strip()
                    if tag_name not in existing_tags:
                        tag = Tag(name=tag_name)
                        db.session.add(tag)
                        existing_tags[tag_name] = tag  # Add to existing_tags for future reference
                    recipe.tags.append(existing_tags[tag_name])

                db.session.add(recipe)

        # Use try-except for error handling during commit
        try:
            db.session.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            db.session.rollback()

if __name__ == '__main__':
    csv_path = './RAW_recipes.csv'  # Replace with the actual path to your CSV file
    populate_db_from_csv(csv_path)
