from re import L
from flask import Flask, render_template, session, g,request
from werkzeug.utils import redirect
from models import connect_db, db, User,Ingredient,Cocktail,FavoriteCocktail,CocktailIngredient
from forms import LoginForm,UserAddForm
import os
import requests

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///mycocktailsdb'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

@app.before_request
def add_user_to_g():
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        user = User.signup(
                username=form.username.data,
                password=form.password.data
            )
        db.session.commit()

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)

@app.route('/signout')
def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

        return redirect('/login')

@app.route('/login/<user>')
def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            return redirect("/")

    return render_template('login.html', form=form)



@app.route("/")
def homepage():
    rtrigger = False
    strigger = False
    if g.user:
        # load favorites
        name_image = []
        for cocktail in g.user.favoritecocktails:
            drink_name = cocktail.name
            # get image from api
            json_data = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink_name}").json()

            image_data = json_data["drinks"][0]["strDrinkThumb"]
            name_data = json_data["drinks"][0]["strDrink"]
            n_i = (image_data,name_data,cocktail.id)
            name_image.append(n_i)
        return render_template('homepage.html',user=g.user,favorites=name_image,rtrigger=rtrigger,strigger=strigger)
    else:
        return redirect('/signup')


@app.route("/random")
def get_random_drink():
    strigger=False
    rtrigger=True
    if g.user:
        json_data = requests.get("https://www.thecocktaildb.com/api/json/v1/1/random.php").json()
        random_drink_image = json_data["drinks"][0]['strDrinkThumb']
        random_drink_name = json_data["drinks"][0]['strDrink']
     
        drink_id = json_data["drinks"][0]["idDrink"]
        random_drink_ingredients = []
        for property in json_data["drinks"][0]:
            if property.startswith("strIngredient"):
                if json_data["drinks"][0][property]:
                    if property not in random_drink_ingredients:
                        random_drink_ingredients.append(json_data["drinks"][0][property])
                    

        name_image = []
        for cocktail in g.user.favoritecocktails:
            drink_name = cocktail.name
            # get image from api
            json_data = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink_name}").json()

            image_data = json_data["drinks"][0]["strDrinkThumb"]
            name_data = json_data["drinks"][0]["strDrink"]
            n_i = (image_data,name_data,cocktail.id)
            name_image.append(n_i)

        return render_template('homepage.html',user=g.user,rtrigger=rtrigger,random_drink_image=random_drink_image,random_drink_ingredients=random_drink_ingredients,random_drink_name=random_drink_name,favorites=name_image,drink_id=drink_id,strigger=strigger)

@app.route("/addtofavorites/<int:id>")
def add_to_favorites(id):
    if g.user:
        json_data = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={id}").json()

        drink_ingredients = []
        for property in json_data["drinks"][0]:
            if property.startswith("strIngredient"):
                if json_data["drinks"][0][property]:
                    if property not in drink_ingredients:
                        drink_ingredients.append(json_data["drinks"][0][property])

        db_cocktail = Cocktail(name=json_data["drinks"][0]["strDrink"])
        db.session.add(db_cocktail)
        db.session.commit()

        db_cocktail = Cocktail.query.filter_by(name=json_data["drinks"][0]["strDrink"]).first()

        fc = FavoriteCocktail(favorite_id=g.user.favorite_id,cocktail_id=db_cocktail.id)
        db.session.add(fc)
        db.session.commit()

        for ingredient in drink_ingredients:
            if (not Ingredient.query.filter_by(name=ingredient).first()):
                db_ingredient = Ingredient(name=ingredient)
                db.session.add(db_ingredient)
                db.session.commit()
            db_ingredient = Ingredient.query.filter_by(name=ingredient).first()

            ci = CocktailIngredient(cocktail_id=db_cocktail.id,ingredient_id=db_ingredient.id)
            db.session.add(ci)
            db.session.commit()
        return redirect("/")


@app.route("/search/",methods=["POST"])
def get_drink():
    rtrigger = False
    strigger = True
    if g.user:
        search = request.form["search_input"].replace(" ","%20")
        json_data = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={search}").json()
        search_drink_image = json_data["drinks"][0]['strDrinkThumb']
        search_drink_name = json_data["drinks"][0]['strDrink']
        search_drink_id = json_data["drinks"][0]["idDrink"]
        search_drink_ingredients = []
        for property in json_data["drinks"][0]:
            if property.startswith("strIngredient"):
                if json_data["drinks"][0][property]:
                    if property not in search_drink_ingredients:
                        search_drink_ingredients.append(json_data["drinks"][0][property])
                    

        name_image = []
        for cocktail in g.user.favoritecocktails:
            drink_name = cocktail.name
            # get image from api
            json_data = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink_name}").json()

            image_data = json_data["drinks"][0]["strDrinkThumb"]
            name_data = json_data["drinks"][0]["strDrink"]

            n_i = (image_data,name_data,cocktail.id)
            name_image.append(n_i)

        return render_template('homepage.html',user=g.user,search_drink_image=search_drink_image,search_drink_ingredients=search_drink_ingredients,search_drink_name=search_drink_name,favorites=name_image,drink_id=search_drink_id,strigger=strigger,rtrigger=rtrigger)


@app.route("/cocktaildetails/<int:id>")
def show_details(id):
    if g.user:
        cocktail = Cocktail.query.get(id)
        drink_name = cocktail.name
            # get image from api
        json_data = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink_name}").json()

        image_data = json_data["drinks"][0]["strDrinkThumb"]
        name_data = json_data["drinks"][0]["strDrink"]
        
        return render_template("cocktaildetails.html",cocktail=cocktail,image_data=image_data)

            


          
        


    
