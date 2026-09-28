try:
    import pygame
except ImportError as e:
    raise ImportError(
        "pygame is required to run this program. Install it with `pip install pygame`."
    ) from e

import random
pygame.init()


WIDTH, HEIGHT = 2560, 1600
FPS = 60

STAR_SIZE = 10
STAR_COLOR = (255, 255, 255)
STARS = 450

PLAYER_ROWS, PLAYER_COLS = 1, 1
PLAYER_SIZE = 50
PLAYER_MOVE_SPEED = 400.0
PLAYER_INITIAL_HEALTH = 150

ENEMY_ROWS, ENEMY_COLS = 3, 6 
ENEMY_X_SPACING, ENEMY_Y_SPACING = 120, 100
ENEMY_START_X = 100
ENEMY_START_Y = 30
ENEMY_SIZE = 50
ENEMY_INITIAL_HEALTH = 26

PLAYER_BULLET_SPEED = 500
ENEMY_BULLET_SPEED = 300
BULLET_SIZE = (10, 10)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (50, 200, 255)
ENEMY_COLOR = (255, 80, 80)
PLAYER_BULLET_COLOR = (blue := (100, 200, 255))
ENEMY_BULLET_COLOR = (red := (255, 150, 150))



class Star(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((STAR_SIZE, STAR_SIZE))
        self.image.fill(STAR_COLOR)
        self.blink_timer = random.uniform(5, 10)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt):
        self.blink_timer -= dt
        if self.blink_timer <= 0:
            self.image.fill(STAR_COLOR if self.image.get_at((0, 0)) == BLACK else BLACK)
            self.blink_timer = random.uniform(5, 10)
        self.rect.y += 20 * dt
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direction, color):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.direction = direction

    def update(self, dt):
        self.rect.y += self.direction * self.speed * dt
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = PLAYER_MOVE_SPEED
        self.health = PLAYER_INITIAL_HEALTH

    def update(self, keys, dt):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed * dt
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed * dt
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed * dt
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed * dt

    def shoot(self, player_bullets):
        bullet = Bullet(self.rect.centerx, self.rect.top, PLAYER_BULLET_SPEED, -1, PLAYER_BULLET_COLOR)
        player_bullets.add(bullet)

    def draw_health_bar(self, surface):
        bar_width = 50
        bar_height = 10
        health_percentage = self.health / PLAYER_INITIAL_HEALTH
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 15, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y - 15, bar_width * health_percentage, bar_height))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_bullets):
        super().__init__()
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.image.fill(ENEMY_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = ENEMY_INITIAL_HEALTH
        self.max_health = ENEMY_INITIAL_HEALTH
        self.columns = ENEMY_COLS
        self.direction = 1
        self.shoot_timer = 0
        self.shoot_interval = 1000
        self.enemy_bullets = enemy_bullets
        
    def update(self, dt):
        self.rect.x += self.direction * 2
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.direction *= -1
            self.rect.y += 10
        
        self.shoot_timer += dt * 1000
        if self.shoot_timer >= self.shoot_interval:
            bullet = Bullet(self.rect.centerx, self.rect.centery, ENEMY_BULLET_SPEED, 1, ENEMY_BULLET_COLOR)
            self.enemy_bullets.add(bullet)
            self.shoot_timer = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery, ENEMY_BULLET_SPEED, 1, ENEMY_BULLET_COLOR)
        self.enemy_bullets.add(bullet)
        self.sound_manager.play_enemy_shoot()  # Play enemy shoot sound        

    def take_damage(self, dmg=1):
        self.health -= dmg
        if self.health <= 0:
            self.kill()
            return True
        return False

    def draw_health_bar(self, surface):
        bar_width = self.rect.width
        bar_height = 5
        bar_x = self.rect.left
        bar_y = self.rect.top - bar_height - 2
        pygame.draw.rect(surface, (200, 30, 30), (bar_x, bar_y, bar_width, bar_height))
        health_width = int(bar_width * (self.health / self.max_health))
        if health_width > 0:
            pygame.draw.rect(surface, (30, 220, 30), (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock()
        self.dt = 0
        
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemy_columns = ENEMY_COLS
        self.health = pygame.sprite.Group()
        
        
        self.player = Player(WIDTH // 2, HEIGHT - 140)
        self.enemies.add(Enemy(100, 100, self.enemy_bullets))
        
        # Create stars
        for _ in range(STARS):
            x = int(random.random() * WIDTH)
            y = int(random.random() * HEIGHT)
            self.stars.add(Star(x, y))
        
        # Create enemies
        for row in range(ENEMY_ROWS):
            for col in range(ENEMY_COLS):
                enemy_x = ENEMY_START_X + col * ENEMY_X_SPACING
                enemy_y = ENEMY_START_Y + row * ENEMY_Y_SPACING
                self.enemies.add(Enemy(enemy_x, enemy_y, self.enemy_bullets))

                self.enemy_columns = 6

    def update(self):
        self.dt = self.clock.get_time() / 1000.0
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.dt)

        self.player_bullets.update(self.dt)
        self.enemy_bullets.update(self.dt)
        self.stars.update(self.dt)
        self.enemies.update(self.dt)
        self.health.update(self.dt)
       
        # Player bullets hitting enemies
        for bullet in self.player_bullets:
            hit_enemies = pygame.sprite.spritecollide(bullet, self.enemies, False)
            for enemy in hit_enemies:
                enemy.take_damage(1)
                bullet.kill()

        # Enemy bullets hitting player
        for bullet in self.enemy_bullets:
            if pygame.sprite.collide_rect(bullet, self.player):
                self.player.health -= 1
                bullet.kill()
                if self.player.health <= 0:
                    return False
        
        return True

    def draw(self):
        self.screen.fill(BLACK)  
        self.stars.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.player_bullets.draw(self.screen)
        self.enemies.draw(self.screen)
        self.enemy_bullets.draw(self.screen)
        
        self.player.draw_health_bar(self.screen)
        for enemy in self.enemies:
            enemy.draw_health_bar(self.screen)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.shoot(self.player_bullets)
                    
            
            if not self.update():
                print("Game Over!")
                running = False
            
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
