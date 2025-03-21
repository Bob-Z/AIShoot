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


bullet_image = None
high_background_image = None
low_background_image = None
shoot_sound = None
is_music_playing = False

explosion_sound_idx = 0
background_image_idx = 0
enemy_image_idx = 0
music_index = 0

player_init_done = False
enemy_init_done = False

# Load initial music
pygame.mixer.init()


def play_next_music():
    global is_music_playing
    music_files = os.listdir(config.data["music_dir"])
    if len(music_files) > 0:
        global music_index
        next_music_file = os.path.join(config.data["music_dir"], music_files[music_index])
        pygame.mixer.music.stop()
        pygame.mixer.music.load(next_music_file)
        pygame.mixer.music.play(fade_ms=2000)
        pygame.mixer.music.set_endevent(MUSIC_END)
        print(f"Playing music: {next_music_file}")
        music_index = (music_index + 1) % len(music_files)
        is_music_playing = True


def get_next_background_image():
    global background_image_idx
    bg_image = load_and_resize_image(
        os.path.join(config.data['image_dir'],
                     config.data['background_filename'] + str(background_image_idx) + ".png"),
        (SCREEN_WIDTH, SCREEN_HEIGHT * 2))
    if bg_image is not None:
        background_image_idx = (background_image_idx + 1) % len(
            [entry for entry in os.listdir(config.data['image_dir']) if
             entry.startswith(config.data['background_filename'])])

    return bg_image


def get_next_explosion_sound():
    global explosion_sound_idx
    sound = pygame.mixer.Sound(os.path.join(config.data['sound_dir'],
                                            config.data['explosion_sound_filename'] + str(
                                                explosion_sound_idx) + ".wav"))
    if sound is not None:
        explosion_sound_idx = (explosion_sound_idx + 1) % len(
            [entry for entry in os.listdir(config.data['sound_dir']) if
             entry.startswith(config.data['explosion_sound_filename'])])

    return sound


def get_next_player_image():
    return load_and_resize_image(
        os.path.join(config.data['image_dir'], config.data['player_sprite_filename']),
        (config.data['player_sprite_width'], config.data['player_sprite_height']))


def get_next_enemy_image():
    global enemy_image_idx
    sprite_image = load_and_resize_image(
        os.path.join(config.data['image_dir'],
                     config.data['enemy_sprite_filename'] + str(enemy_image_idx) + ".png"),
        (config.data['enemy_sprite_width'], config.data['enemy_sprite_height']))
    if sprite_image is not None:
        enemy_image_idx = (enemy_image_idx + 1) % len([entry for entry in os.listdir(config.data['image_dir']) if
                                                       entry.startswith(config.data['enemy_sprite_filename'])])
    return sprite_image


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
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
        drawn_sprites.add(bullet)
        bullets.add(bullet)
        if shoot_sound is not None:
            shoot_sound.play()


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = get_next_enemy_image()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 8)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.set_sprite_image()

    def set_sprite_image(self):
        global enemy_image_idx
        get_next_enemy_image()

        self.image = get_next_enemy_image()
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
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
            drawn_sprites.remove(self)
            bullets.remove(self)
            self.kill()


# Create sprite groups
drawn_sprites = pygame.sprite.Group()
colliding_enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = None

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
            play_next_music()

        # Check for bullet's sprite availability
        if bullet_image is None:
            bullet_image = load_and_resize_image(
                os.path.join(config.data['image_dir'], config.data['bullet_sprite_filename']),
                (config.data['bullet_sprite_width'], config.data['bullet_sprite_height']))

        # Check for bullet sound availability
        if shoot_sound is None:
            try:
                shoot_sound = pygame.mixer.Sound(
                    os.path.join(config.data['sound_dir'], config.data['bullet_sound_filename'] + ".wav"))
            except FileNotFoundError:
                pass

        # Check for player image availability
        if player_init_done is False:
            image = get_next_player_image()
            if image is not None:
                player = Player(image)
                drawn_sprites.add(player)
                player_init_done = True

        # Check for enemy image availability
        if enemy_init_done is False:
            enemy_image_qty = len([entry for entry in os.listdir(config.data['image_dir']) if
                                   entry.startswith(config.data['enemy_sprite_filename'])])
            if enemy_image_qty > 0:
                # Create enemies
                for i in range(8):
                    enemy = Enemy()
                    drawn_sprites.add(enemy)
                    colliding_enemies.add(enemy)

                enemy_init_done = True

        last_image_check = time.time()

    drawn_sprites.update()

    # Check for bullet-enemy collisions
    hits = pygame.sprite.groupcollide(colliding_enemies, bullets, True, True)
    for hit in hits:
        explosion_sound = get_next_explosion_sound()
        if explosion_sound is not None:
            explosion_sound.play()
        enemy = Enemy()
        drawn_sprites.add(enemy)
        colliding_enemies.add(enemy)

    # Check for player-enemy collisions
    #    if pygame.sprite.spritecollideany(player, enemies):
    #        running = False

    if low_background_image is None:
        bg_image = get_next_background_image()
        if bg_image is not None:
            low_background_image = bg_image
            high_background_image = bg_image
    else:
        # Scroll the background
        background_y += scroll_speed
        if background_y >= SCREEN_HEIGHT:
            background_y = 0
            low_background_image = high_background_image
            high_background_image = get_next_background_image()

        # Draw the background
        screen.blit(high_background_image, (0, background_y - SCREEN_HEIGHT))
        screen.blit(low_background_image, (0, background_y))

    # Draw all sprites
    drawn_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
