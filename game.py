import pygame
import random
import os
import time
import config

config.read_command_line()

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

MUSIC_END = pygame.USEREVENT + 1

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AIShoot")


# Load or generate images
def load_and_resize_image(filename, size):
    try:
        image = pygame.image.load(filename)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Error loading image {filename}: {e}")
        return None
    except FileNotFoundError:
        return None


# Ensure the initial images are loaded
enemy_image = None
bullet_image = None
background_image = None
high_background_image = None
low_background_image = None

current_enemy_image_file = None
current_background_image_file = None

# Load initial music
pygame.mixer.init()
is_music_playing = False

current_music_index = 0


def play_next_music():
    music_files = os.listdir(config.data["music_dir"])
    if len(music_files) > 0:
        global current_music_index
        global is_music_playing
        current_music_index = (current_music_index + 1) % len(music_files)
        next_music_file = os.path.join(config.data["music_dir"], music_files[current_music_index])
        pygame.mixer.music.stop()
        pygame.mixer.music.load(next_music_file)
        pygame.mixer.music.play(fade_ms=2000)
        pygame.mixer.music.set_endevent(MUSIC_END)
        is_music_playing = True
        print(f"Playing music: {next_music_file}")


# Init sound effects
shoot_sound = None

explosion_sound = []
last_explosion_filename = None
explosion_sound_idx = 0

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = None
        self.rect = None
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
        if shoot_sound is not None:
            shoot_sound.play()

    def set_sprite_image(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10


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
            self.image = enemy_image


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
            all_sprites.remove(self)
            bullets.remove(self)
            self.kill()


# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = Player()


def load_new_enemy_images():
    global enemy_image
    global current_enemy_image_file

    files = sorted(os.listdir(config.data['image_dir']),
                   key=lambda x: os.path.getmtime(os.path.join(config.data['image_dir'], x)))
    if files:
        newest_file = files[-1]
        if newest_file.startswith(config.data['enemy_sprite_filename']):
            if newest_file != current_enemy_image_file:
                current_enemy_image_file = newest_file
                new_enemy_image = load_and_resize_image(os.path.join(config.data['image_dir'], newest_file), (50, 50))
                if new_enemy_image:
                    print(f"Loaded new enemy image: {newest_file}")
                    return new_enemy_image
    return None

def load_new_explosion_sound():
    global explosion_sound
    global last_explosion_filename

    files = sorted(os.listdir(config.data['sound_dir']),
                   key=lambda x: os.path.getmtime(os.path.join(config.data['sound_dir'], x)))
    if files:
        newest_file = files[-1]
        if newest_file.startswith(config.data['explosion_sound_filename']):
            if newest_file != last_explosion_filename:
                last_explosion_filename = newest_file
                new_sound = pygame.mixer.Sound(os.path.join(config.data['sound_dir'], last_explosion_filename))
                if new_sound:
                    explosion_sound.append(new_sound)
                    print(f"Loaded new explosion sound image: {last_explosion_filename}")


def load_new_background_images():
    global background_image
    global current_background_image_file

    files = sorted(os.listdir(config.data['image_dir']),
                   key=lambda x: os.path.getmtime(os.path.join(config.data['image_dir'], x)))
    if files:
        newest_file = files[-1]
        if newest_file.startswith(config.data['background_filename']):
            if newest_file != current_background_image_file:
                current_background_image_file = newest_file
                new_background_image = load_and_resize_image(os.path.join(config.data['image_dir'], newest_file),
                                                             (SCREEN_WIDTH, SCREEN_HEIGHT * 2))
                if new_background_image:
                    print(f"Loaded new background image: {newest_file}")
                    return new_background_image
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
                if bullet_image is not None:
                    player.shoot()
            if event.key == pygame.K_ESCAPE:
                exit(0)
        elif event.type == MUSIC_END:
            # pygame.mixer.music.fadeout(2000)  # Fade-out over 2 seconds
            # pygame.time.set_timer(pygame.mixer.music.get_endevent(), 2000, loops=1)
            play_next_music()

    # Check for new generated media
    if time.time() - last_image_check > 0.5:
        # Check for music availability
        if is_music_playing is False:
            music_dir_files = os.listdir(config.data["music_dir"])
            if len(music_dir_files) > 0:
                play_next_music()
        # Check for player's sprite availability
        if player.image is None:
            sprite_image = load_and_resize_image(
                os.path.join(config.data['image_dir'], config.data['player_sprite_filename']), (50, 50))
            if sprite_image is not None:
                player.set_sprite_image(sprite_image)
                all_sprites.add(player)
        # Check for bullet's sprite availability
        if bullet_image is None:
            bullet_image = load_and_resize_image(
                os.path.join(config.data['image_dir'], config.data['bullet_sprite_filename']), (10, 30))

        new_enemy_image = load_new_enemy_images()
        if new_enemy_image:
            if enemy_image is None:
                enemy_image = new_enemy_image
                # Create enemies
                for i in range(8):
                    enemy = Enemy(enemy_image)
                    all_sprites.add(enemy)
                    enemies.add(enemy)
            else:
                enemy_image = new_enemy_image

        new_background_image = load_new_background_images()
        if new_background_image:
            if background_image is None:
                high_background_image = new_background_image
                low_background_image = new_background_image
                background_image = new_background_image
            else:
                background_image = new_background_image

        # Check for bullet sound availability
        if shoot_sound is None:
            try:
                shoot_sound = pygame.mixer.Sound(
                    os.path.join(config.data['sound_dir'], config.data['bullet_sound_filename'] + ".wav"))
            except FileNotFoundError:
                pass
        # Check for explosion sound availability
        load_new_explosion_sound()

        last_image_check = time.time()

    all_sprites.update()

    # Check for bullet-enemy collisions
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        if len(explosion_sound) > 0:
            explosion_sound[explosion_sound_idx].play()
            explosion_sound_idx += 1
            explosion_sound_idx = explosion_sound_idx % len(explosion_sound)
        enemy = Enemy(enemy_image)
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Check for player-enemy collisions
    #    if pygame.sprite.spritecollideany(player, enemies):
    #        running = False

    if background_image is not None:
        # Scroll the background
        background_y += scroll_speed
        if background_y >= SCREEN_HEIGHT:
            background_y = 0
            low_background_image = high_background_image
            high_background_image = background_image

        # Draw the background
        screen.blit(high_background_image, (0, background_y - SCREEN_HEIGHT))
        screen.blit(low_background_image, (0, background_y))

    # Draw all sprites
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
