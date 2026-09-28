
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///game.db'
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    name = Column(String, default="Space Invaders")
    genre = Column(String, default="Sci-fi FPS")
    release_date = Column(Integer, default=(2026, 5, 1))

def __init__(self, name, genre, release_date):
    self.name = name
    self.genre = genre
    self.release_date = release_date

def __repr__(self):
    return f"Game(name='{self.name}', genre='{self.genre}', release_date={self.release_date})"        

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String, default="Player1, Player2, Player3, Player4, Player5, Player6, Player7, Player8, Player9, Player10")
    score = Column(Integer, default="1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000")
    level = Column(Integer, default="5, 10, 15, 20, 25, 30, 35, 40, 45, 50")

def __init__(self, name, score, level):
    self.name = name
    self.score = score
    self.level = level

def __repr__(self):
    return f"Player(name='{self.name}', score={self.score}, level={self.level})"
class Menu(Base):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True)
    home = Column(String, default="Home")
    about = Column(String, default="About")
    contacts = Column(String, default="Contacts")
    follow = Column(String, default="Follow")

def __init__(self, home, about, contacts, follow):
    self.home = home
    self.about = about
    self.contacts = contacts
    self.follow = follow  

def __repr__(self):
    return f"Menu(home='{self.home}', about='{self.about}', contacts='{self.contacts}', follow='{self.follow}')"      

class Leaderboard(Base):
    __tablename__ = 'leaderboards'
    id = Column(Integer, primary_key=True)
    player_accounts = Column(String, default="Player1, Player2, Player3, Player4, Player5, Player6, Player7, Player8, Player9, Player10")
    player_scores = Column(String, default="1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000")
    player_levels = Column(String, default="5, 10, 15, 20, 25, 30, 35, 40, 45, 50")

def __init__(self, player_accounts, player_scores, player_levels):
    self.player_accounts = player_accounts
    self.player_scores = player_scores
    self.player_levels = player_levels

def __repr__(self):
    return f"Leaderboard(player_accounts='{self.player_accounts}', player_scores='{self.player_scores}', player_levels='{self.player_levels}')"        
            
 
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_game(name, genre, release_date):
    new_game = Game(name=name, genre=genre, release_date=release_date)
    session.add(new_game)
    session.commit()

def add_player(name, score, level):
    new_player = Player(name=name, score=score, level=level)
    session.add(new_player)
    session.commit()    

def get_game(game_id):
    return session.query(Game).filter_by(id=game_id).first()

def get_players():
    return session.query(Player).all()

def update_player_score(player_id, new_score):
    player = session.query(Player).filter_by(id=player_id).first()
    if player:
        player.score = new_score
        session.commit()

def update_player_level(player_id, new_level):
    player = session.query(Player).filter_by(id=player_id).first()
    if player:
        player.level = new_level
        session.commit()

def delete_game(game_id):
    game = session.query(Game).filter_by(id=game_id).first()
    if game:
        session.delete(game)
        session.commit()

def delete_player(player_id):
    player = session.query(Player).filter_by(id=player_id).first()
    if player:
        session.delete(player)
        session.commit()
    
    # Add multiple players using a list
    players_data = [
        ("Player1", 1000, 5),
        ("Player2", 2000, 10),
        ("Player3", 3000, 15),
        ("Player4", 4000, 20),
        ("Player5", 5000, 25)
        ("Player6", 6000, 30),
        ("Player7", 7000, 35),
        ("Player8", 8000, 40),
        ("Player9", 9000, 45),
        ("Player10", 10000, 50)    
   ]
        
    for name, score, level in players_data:
        add_player(name, score, level)

    game = get_game(1)
    players = get_players()

    print("Games:")
    if game:
        print(f"{game.id}: {game.name} - {game.genre} - {game.release_date}")

    print("\nPlayers:")
    for player in players:
        print(f"{player.id}: {player.name} - Score: {player.score} - Level: {player.level}")

if __name__ == "__main__":
    add_game("Space Shooter", "Sci-fi FPS", (2026, 4, 12))

    session.close()