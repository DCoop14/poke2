from app import app
from flask import render_template, request, redirect, url_for, flash
import requests
from app.forms import PokemonSearchForm, LoginForm
from flask import Blueprint, render_template
from app.models import User
#from app.services import get_pokemon

auth = Blueprint('auth', __name__, template_folder='authtemplates')

#import login funcitonality
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

@app.route('/')
def index():
    poke = [{'img' : 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTSZw51Y3OJDZjr8xRtbnXBMZA50XpbhkdQMNFf3_npUojFw-WJjx52-7RHbA_vLGLhmVs&usqp=CAU'}]
    return render_template('index.html', names=poke)

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/login', methods = ["GET", "POST"])
def logMeIn():
    if current_user.is_authinticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data
            # Query user based off of username
            user = User.query.filter_by(username=username).first()
            print(user.username, user.password, user.id)
            if user:
                # compare passwords
                if check_password_hash(user.password, password):
                    flash('You have successfully logged in!', 'success')
                    login_user(user)
                    return redirect(url_for('index'))
                else:
                    flash('Incorrect username/password combination.', 'danger')
            else:
                flash('User with that username does not exist.', 'danger')

    return render_template('login.html', form=form)


@app.route('/search', methods = ["GET", 'POST'])
def searchPokemon():
    form = PokemonSearchForm()
    my_dict = {}

    if request.method == "POST":
        if form.validate():
            poke_name = form.name.data
            
 
        url = f"https://pokeapi.co/api/v2/pokemon/{poke_name}"
        res = requests.get(url)
        if res.ok:
            data = res.json()
            my_dict = {
                'name': data['name'],
                'ability': data['abilities'][0]['ability']['name'],
                'base_experience' : data['base_experience'],
                'img_url': data['sprites']['front_shiny'],
                "hp" : data['stats'][0]['base_stat'],
                'attack': data['stats'][1]['base_stat'],
                'defense' : data['stats'][2]['base_stat']
            }
              
    
    return render_template('searchpokemon.html', form=form, pokemon=my_dict)