from app import db
from models import User, CocktailIngredient, Cocktail, Ingredient, FavoriteCocktail

db.drop_all()
db.create_all()

user1 = User(username="ish",password="testpassword",)
user2 = User(username="joe",password="testpassword")
user3 = User(username="rob",password="testpassword")
user4 = User(username="bob",password="testpassword")
db.session.add_all([user1,user2,user3,user4])
db.session.commit()

ingredient1 = Ingredient(name="gin")
ingredient2 = Ingredient(name="vodka")
ingredient3 = Ingredient(name="wine")
ingredient4 = Ingredient(name="mead")
db.session.add_all([ingredient1,ingredient2,ingredient3,ingredient4])
db.session.commit()

cocktail1 = Cocktail(name="bahama mama")
cocktail2 = Cocktail(name="drinkydrink")
cocktail3 = Cocktail(name="other drink")
cocktail4 = Cocktail(name="great drink")
db.session.add_all([cocktail1,cocktail2,cocktail3,cocktail4])
db.session.commit()

cocktailingredient1 = CocktailIngredient(cocktail_id=1,ingredient_id=1)
cocktailingredient2 = CocktailIngredient(cocktail_id=1,ingredient_id=2)
cocktailingredient3 = CocktailIngredient(cocktail_id=1,ingredient_id=3)
cocktailingredient4 = CocktailIngredient(cocktail_id=1,ingredient_id=4)
db.session.add_all([cocktailingredient1,cocktailingredient2,cocktailingredient3,cocktailingredient4])
db.session.commit()

favoritecocktail1 = FavoriteCocktail(favorite_id=1,cocktail_id=1)
favoritecocktail2 = FavoriteCocktail(favorite_id=2,cocktail_id=2)
favoritecocktail3 = FavoriteCocktail(favorite_id=3,cocktail_id=3)
favoritecocktail4 = FavoriteCocktail(favorite_id=4,cocktail_id=4)
db.session.add_all([favoritecocktail1,favoritecocktail2,favoritecocktail3,favoritecocktail4])
db.session.commit()