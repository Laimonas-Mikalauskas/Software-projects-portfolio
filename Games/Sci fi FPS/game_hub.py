from flask import Flask, render_template, request   
app = Flask('__Space Guardian__')

class Game:
    def __init__(self, genre, release_date):
        self.name = "Space Guardian"
        self.genre = "Sci-fi FPS"
        self.release_date = "2026-03-01"


class Menu:
    def __init__(self, home, about, contacts, follow):
        self.home = home
        self.about = about
        self.ontacts = contacts
        self.follow = follow

class Player_Mode:
    def __init__(self, single_player, multiplayer):
        self.single_player = single_player
        self.multiplayer = multiplayer



games = []
players = []

@app.route('/')
def index():
    return render_template('index.html', games=games, players=players)

@app.route('/add_game', methods=['GET'] )
def add_game():
    name = request.form['name']
    genre = request.form['genre']
    release_date = request.form['release_date']
    new_game = Game(name=name, genre=genre, release_date=release_date)
    games.append(new_game)

@app.route('/menu', methods=['GET'])
def menu():
    home = request.form['home']
    about = request.form['about']
    contacts = request.form['contacts']
    follow = request.form['follow']
    new_menu = Menu(home=home, about=about, contacts=contacts, follow=follow)
    return render_template('menu.html', menu=new_menu)


@app.route('/player_mode', methods=['GET']) 
def player_mode():
    single_player = request.form['single_player']
    multiplayer = request.form['multiplayer']
    new_player_mode = Player_Mode(single_player=single_player, multiplayer=multiplayer)
    return render_template('player_mode.html', player_mode=new_player_mode)   
    

@app.route('/contacts', methods=['GET'])
def contacts():
    return render_template('contacts.html')

def contact():
    return render_template('contacts.html')





if __name__ == '__main__':
    app.run(debug=True)

