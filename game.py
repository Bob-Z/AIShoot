import pygame
import random
import os
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shoot 'Em Up")

# Directory to load generated images and music
image_dir = "generated_image"
music_dir = "generated_music"
sound_dir = "generated_sound"

# Load or generate images
def load_and_resize_image(filename, size):
    try:
        image = pygame.image.load(filename).convert_alpha()  # Load image with alpha channel
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Error loading image {filename}: {e}")
        return None

# Ensure the initial images are loaded
player_image = load_and_resize_image(os.path.join(image_dir, 'player.png'), (50, 50))
enemy_image = load_and_resize_image(os.path.join(image_dir, 'enemy.png'), (50, 50))
bullet_image = load_and_resize_image(os.path.join(image_dir, 'bullet.png'), (10, 30))
background_image = load_and_resize_image(os.path.join(image_dir, 'background.png'), (SCREEN_WIDTH, SCREEN_HEIGHT * 2))

# Load initial music
pygame.mixer.init()
background_music = os.path.join(music_dir, "background_music.mid")
if os.path.exists(background_music):
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.play(-1)  # Loop the music indefinitely
    print(f"Loaded and playing background music: {background_music}")
else:
    print(f"Error: Background music file not found: {background_music}")

# Load sound effects
shoot_sound = pygame.mixer.Sound(os.path.join(sound_dir, "shoot.wav"))
hit_sound = []
hit_sound_idx = 0
for i in range(5):
    hit_sound.append(pygame.mixer.Sound(os.path.join(sound_dir, f'hit{i}.wav')))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()  # Play shoot sound

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 8)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(1, 8)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create enemies
for i in range(8):
    enemy = Enemy(enemy_image)
    all_sprites.add(enemy)
    enemies.add(enemy)

# Function to load new enemy images from the directory
def load_new_enemy_images():
    global enemy_image
    files = sorted(os.listdir(image_dir), key=lambda x: os.path.getmtime(os.path.join(image_dir, x)))
    if files:
        newest_file = files[-1]
        if newest_file.startswith("new_enemy_"):
            new_enemy_image = load_and_resize_image(os.path.join(image_dir, newest_file), (50, 50))
            if new_enemy_image:
                print(f"Loaded new enemy image: {newest_file}")  # Debugging information
                return new_enemy_image
    return None

# Initialize the running variable
running = True

# Background scrolling variables
background_y = 0
scroll_speed = 2

# Game loop
clock = pygame.time.Clock()
last_image_check = time.time()

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Check for new enemy images every 0.5 seconds
    if time.time() - last_image_check > 0.5:
        new_enemy_image = load_new_enemy_images()
        if new_enemy_image:
            enemy_image = new_enemy_image
        last_image_check = time.time()

    all_sprites.update()

    # Check for bullet-enemy collisions
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        hit_sound[hit_sound_idx].play()  # Play hit sound
        hit_sound_idx += 1
        hit_sound_idx = hit_sound_idx % len(hit_sound)
        enemy = Enemy(enemy_image)
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Check for player-enemy collisions
    if pygame.sprite.spritecollideany(player, enemies):
        running = False

    # Scroll the background
    background_y += scroll_speed
    if background_y >= SCREEN_HEIGHT:
        background_y = 0

    # Draw the background
    screen.blit(background_image, (0, background_y - SCREEN_HEIGHT))
    screen.blit(background_image, (0, background_y))

    # Draw all sprites
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
