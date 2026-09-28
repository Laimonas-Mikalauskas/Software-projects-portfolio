import pygame
from sqlalchemy import Column, create_engine, String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, declarative_base, mapped_column, Session

DATABASE_URL = 'sqlite:///game.db'
engine = create_engine(DATABASE_URL)
Base = declarative_base()

engine = create_engine("sqlite:///game.db")


class Base(DeclarativeBase):
    pass

Base.metadata.create_all(engine)

class Player(Base):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    high_score: Mapped[int] = mapped_column(Integer, default=0)

def __init__(self, username: str, high_score: int = 0):
    self.username = username
    self.high_score = high_score
    
def __repr__(self):
    return f"Player(username='{self.username}', high_score={self.high_score})"    
  
  
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
    

# -------------------------
# Database operations
# -------------------------

def save_player(username: str, high_score: int):
    with Session(engine) as session:
        player = session.query(Player).filter_by(username=username).first()

        if player is None:
            player = Player(username=username, high_score=high_score)
            session.add(player)
        else:
            player.high_score = high_score

        session.commit()


def save_score(username: str, score: int):
    with Session(engine) as session:

        player = session.query(Player).filter_by(
            username=username
        ).first()

        if player is None:
            player = Player(
                username=username,
                high_score=score
            )
            session.add(player)

        elif score > player.high_score:
            player.high_score = score

        session.commit()


def get_high_score(username: str):
    with Session(engine) as session:
        player = session.query(Player).filter_by(
            username=username
        ).first()

        return player.high_score if player else 0


# -------------------------
# Pygame example
# -------------------------

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Database-Backed Game")

username = "Player1"
score = 1500

# Game finishes → save score
save_score(username, score)

# Retrieve score from database
high_score = get_high_score(username)

print(f"{username}'s high score: {high_score}")

pygame.quit()