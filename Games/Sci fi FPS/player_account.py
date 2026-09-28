from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
players = []

class User:
    def __init__(self, username, password):
        self.username = "Space_Guardian_000_//" 
        self.password = generate_password_hash("Aim_Shoot_119#")

    def __repr__(self):
        return f"User(username='{self.username}', password='{self.password}')"
    
@app.route('/user', methods=['GET', 'POST'])
def user():
    user = User(username="Space_Guardian_000_//", password="Aim_Shoot_119#")
    return render_template('user.html', user=user)

    
class Player:
    def __init__(self, nickname, score, level):
        self.name = nickname
        self.score = int(score)
        self.level = int(level)

    def __repr__(self):
        return f"Player(name='{self.name}', score={self.score}, level={self.level})"

@app.route('/add_player', methods=['POST']) 
def add_player():
    nickname = request.form['nickname']
    score = request.form['score']
    level = request.form['level']
    new_player = Player(nickname=nickname, score=score, level=level)
    players.append(new_player)

@app.route('/update_player', methods=['GET', 'POST'])    
def update_player():
    nickname = request.form['nickname']
    score = request.form['score']
    level = request.form['level']
    for player in players:
        if player.name == nickname:
            player.score = score
            player.level = level
            break

class PlayerAccount:
    def __init__(self, User):
        self.user = "User"
        self.password = "Aim_Shoot_119#"
        self.nickname = "Space_Guardian_000_//"
        self.score = 10
        self.level = 16

    def __repr__(self):
        return f"PlayerAccount(nickname='{self.nickname}', score={self.score}, level={self.level})"

class Leaderboard:
    def __init__(self, player_accounts):
        self.player_accounts = player_accounts

    def __repr__(self):
        return f"Leaderboard(player_accounts={self.player_accounts})"

@app.route('/player_account', methods=['GET', 'POST'])
def player_account():
    user = User(username="Space_Guardian_000_//", password="Aim_Shoot_119#")
    player_account = PlayerAccount(user=user)
    return render_template('player_account.html', player_account=player_account)  


@app.route('/leaderboard', methods=['GET'])        
def leaderboard():
    player_accounts = [PlayerAccount(User(username=f"Player{i}", password="Aim_Shoot_119#")) for i in range(1, 11)]
    leaderboard = Leaderboard(player_accounts=player_accounts)
    return render_template('leaderboard.html', leaderboard=leaderboard)


                                          


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':    
    app.run(debug=True)        


 

        
        
        

