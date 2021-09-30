import bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    username = db.Column(db.String(80),unique=True,nullable=False)

    password = db.Column(db.String(100),nullable=False)

    favorite_id = db.Column(db.Integer,db.Sequence("favorite_id"),unique=True)

    favoritecocktails = db.relationship("Cocktail",secondary="favorite_cocktails")

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
    
    @classmethod
    def signup(cls, username, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd
        )

        db.session.add(user)
        return user




class Cocktail(db.Model):
    __tablename__ = "cocktails"

    id = db.Column(db.Integer,primary_key=True)

    name = db.Column(db.String(80),nullable=False)

    ingredients = db.relationship("Ingredient",secondary="cocktail_ingredients")


class FavoriteCocktail(db.Model):
    __tablename__ = "favorite_cocktails"

    favorite_id = db.Column(db.Integer,db.ForeignKey("users.favorite_id"),primary_key=True)

    cocktail_id = db.Column(db.Integer,db.ForeignKey("cocktails.id"),primary_key=True)

class Ingredient(db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    name = db.Column(db.String(80),nullable=False)

class CocktailIngredient(db.Model):
    __tablename__ = "cocktail_ingredients"

    cocktail_id = db.Column(db.Integer,db.ForeignKey("cocktails.id"),primary_key=True)
    
    ingredient_id = db.Column(db.Integer,db.ForeignKey("ingredients.id"),primary_key=True)





