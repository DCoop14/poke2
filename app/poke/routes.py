from app.models import db, Pokemon, User
from flask import Blueprint, redirect, render_template, request, url_for, flash
from .forms import PokemonFinderForm
import requests
from flask_login import login_required, current_user

poke = Blueprint('poke', __name__, template_folder='poke_template')

@poke.route('/pokemon', methods=['GET', 'POST'])
def pokedex():
    form = PokemonFinderForm()
    my_dict = {}
    caught = False
    if request.method == "POST":
        if form.validate():
            name = form.poke_name.data

        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
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

            pokemon = Pokemon.query.filter_by(name=my_dict['name']).first()
            if Pokemon:
                pokemon = Pokemon(my_dict['img_url'], my_dict['name'], my_dict['ability'], my_dict['hp'], my_dict['base_experience'],my_dict['attack'], my_dict['defense'])
                db.session.add(pokemon)
                db.session.commit()

            if current_user.team.filter_by(name=pokemon.name).first():
                caught = True

    return render_template('pokemon.html', form=form, poke_dict=my_dict, caught=caught)



@poke.route('/catch/<string:poke_name>', methods=['GET'])
def catchpoke(poke_name):
    pokemon = Pokemon.query.filter_by(name=poke_name).first()
    if len(current_user.team.all()) < 5:
        current_user.team.append(pokemon)
        db.session.commit()
    else:
        flash('Your team is FULL!', 'danger')
        return redirect(url_for('poke.user_team'))
    return redirect(url_for('poke.pokedex'))

@poke.route('/release/<string:poke_name>', methods=['GET'])
def releasepoke(poke_name):
    pokemon = Pokemon.query.filter_by(name=poke_name).first()
    current_user.team.remove(pokemon)
    db.session.commit()
    return redirect(url_for('poke.user_team'))

@poke.route('/myteam', methods=['GET'])
def user_team():
    team = current_user.team.all()
    return render_template('myteam.html', team=team)


@poke.route('/battle')
def finduser():
    users = User.query.all()
    return render_template('battle.html',  users=users)


