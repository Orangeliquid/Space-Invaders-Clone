import pygame
from config import DEFENDER_COLOR, UFO_COLOR, FONT_SIZE, FONT_NAME, WINDOW_WIDTH, WINDOW_HEIGHT
import random

''' Entities to create for game

mystery alien = 1 runs across top screen above 40 point alien - worth 100 points
'A' 40 point aliens = 11 - top row = total: 440
'B' 20 point aliens = 11 x 2 middle rows = total: 440
'C' 10 point aliens = 11 x 2 bottom rows = total: 220

4 breakable shields
1 player that can shoot vertically 
'''


class Player:
    def __init__(self, projectile_cooldown_max):
        # Set attributes directly
        self.width = 60
        self.height = 40
        self.color = DEFENDER_COLOR
        self.speed = 7
        self.projectiles = pygame.sprite.Group()
        self.projectile_cooldown = 0
        self.projectile_cooldown_max = projectile_cooldown_max
        self.move_left = False
        self.move_right = False
        self.window_width = WINDOW_WIDTH
        self.image = pygame.image.load("assets/sprites/space__0006_Player.png").convert_alpha()  # Load player image
        self.image = self.change_image_color(image=self.image, new_color=self.color)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = ((WINDOW_WIDTH - self.width) // 2, WINDOW_HEIGHT - 150)

    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        elif direction == "right" and self.rect.right < self.window_width:
            self.rect.x += self.speed

    def draw(self, screen):
        # Draw player image at the current position
        screen.blit(self.image, self.rect)

    def shoot(self):
        if self.projectile_cooldown <= 0:
            projectile = PlayerProjectile(self.rect.centerx, self.rect.top)
            self.projectiles.add(projectile)
            self.projectile_cooldown = self.projectile_cooldown_max

    def update_projectiles(self, screen, alien_list, ufo_single, scoreboard):
        self.projectiles.update()
        for projectile in self.projectiles.copy():
            if projectile.rect.bottom <= 0:
                self.projectiles.remove(projectile)
            else:
                # Check for collisions with enemies
                enemy_hit_list = pygame.sprite.spritecollide(projectile, alien_list, True)
                for enemy in enemy_hit_list:
                    print("Enemy Hit!!!")
                    print(enemy)
                    enemy.explode(screen)
                    scoreboard.update_score(20)
                    self.projectiles.remove(projectile)
                ufo_hit = pygame.sprite.spritecollideany(projectile, ufo_single)
                if ufo_hit:
                    print("Ufo Hit")
                    ufo_hit.explode(screen)
                    scoreboard.update_score(100)

        self.projectile_cooldown -= 1

    def draw_projectiles(self, screen):
        self.projectiles.draw(screen)

    @staticmethod
    def change_image_color(image, new_color):
        # Create a copy of the original image
        new_image = image.copy()
        # Fill the image with the new color
        new_image.fill(new_color, special_flags=pygame.BLEND_MULT)
        return new_image


class Enemy(pygame.sprite.Sprite):
    all_enemies = pygame.sprite.Group()

    def __init__(self, x, y, alien_type, speed=1):
        super().__init__()
        self.enemy_width = 40
        self.enemy_height = 30
        self.alien_type = alien_type
        self.image_index = 0
        self.images = self.load_images()
        self.image = pygame.transform.scale(self.images[self.image_index], (self.enemy_width, self.enemy_height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.direction = 1  # 1 for right, -1 for left
        self.frame_counter = 0
        self.explosion_timer = 0
        self.animation_delay = 10  # Adjust this value to control animation speed

    def load_images(self):
        if self.alien_type == 'A':
            return [pygame.image.load("assets/sprites/space__0000_A1.png").convert_alpha(),
                    pygame.image.load("assets/sprites/space__0001_A2.png").convert_alpha()]
        elif self.alien_type == 'B':
            return [pygame.image.load("assets/sprites/space__0002_B1.png").convert_alpha(),
                    pygame.image.load("assets/sprites/space__0003_B2.png").convert_alpha()]
        elif self.alien_type == 'C':
            return [pygame.image.load("assets/sprites/space__0004_C1.png").convert_alpha(),
                    pygame.image.load("assets/sprites/space__0005_C2.png").convert_alpha()]

    def update(self):
        # Move horizontally
        self.rect.x += self.speed * self.direction

        # Increment frame counter
        self.frame_counter += 1

        # Check if it's time to change the image based on animation delay
        if self.frame_counter >= self.animation_delay:
            # Increment image index and loop back if necessary
            self.image_index = (self.image_index + 1) % len(self.images)

            # Update image based on current direction
            self.image = pygame.transform.scale(self.images[self.image_index],
                                                (self.enemy_width, self.enemy_height))

            # Reset frame counter
            self.frame_counter = 0

        # Check if any enemy reaches the left or right edge of the screen
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            # If so, reverse the direction and move down
            self.direction *= -1
            self.rect.y += self.enemy_height  # Move down

    def explode(self, screen):
        print("Enemy Exploded!")  # Add this line to verify if explosion is triggered
        # Replace the enemy image with an explosion sprite
        explosion_image = pygame.image.load("assets/sprites/space__0009_EnemyExplosion.png").convert_alpha()
        self.image = pygame.transform.scale(explosion_image, (self.enemy_width, self.enemy_height))
        screen.blit(self.image, self.rect)
        # Remove the enemy from the group
        self.kill()

    @classmethod
    def move_group(cls):
        if cls.all_enemies:
            # Move all enemies down
            for enemy in cls.all_enemies:
                enemy.rect.y += enemy.enemy_height
                enemy.y += enemy.enemy_height

                # Check if the enemies reached the bottom of the screen
                if enemy.rect.bottom >= WINDOW_WIDTH:
                    # Reset enemy's position
                    enemy.rect.y = 0
                    enemy.y = 0


class Ufo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 60
        self.height = 40
        self.y = 100
        self.x = 10
        self.color = UFO_COLOR
        self.appear = False
        self.speed = 1
        self.direction = 1
        self.rng_ceiling = 1000
        self.move_left = False
        self.move_right = True
        self.frame_counter = 0
        self.animation_delay = 10  # Adjust this value to control animation speed
        self.window_width = WINDOW_WIDTH
        self.image = pygame.image.load("assets/sprites/space__0007_UFO.png").convert_alpha()  # Load player image
        self.image = self.change_image_color(image=self.image, new_color=self.color)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def display_ufo(self):
        rng = random.randint(0, self.rng_ceiling)
        if rng <= 1:
            self.appear = True
            self.rng_ceiling += 200
            print(self.rng_ceiling)
            return self.appear
        else:
            return self.appear

    def update(self, screen):
        if self.display_ufo():
            # draw ufo
            self.draw(screen)

            # Move horizontally
            self.rect.x += self.speed * self.direction

            # Increment frame counter
            self.frame_counter += 1

            # Check if any enemy reaches the left or right edge of the screen
            if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
                # If so, reverse the direction by changing x val
                self.appear = False
                self.direction *= -1
                self.x = 800
        else:
            pass

    def draw(self, screen):
        # Draw player image at the current position
        screen.blit(self.image, self.rect)

    def explode(self, screen):
        print("Enemy Exploded!")  # Add this line to verify if explosion is triggered
        # Replace the enemy image with an explosion sprite
        explosion_image = pygame.image.load("assets/sprites/space__0009_EnemyExplosion.png").convert_alpha()
        self.image = pygame.transform.scale(explosion_image, (self.width, self.height))
        screen.blit(self.image, self.rect)
        # Remove the enemy from the group
        self.kill()
        # self.appear = True

    @staticmethod
    def change_image_color(image, new_color):
        # Create a copy of the original image
        new_image = image.copy()
        # Fill the image with the new color
        new_image.fill(new_color, special_flags=pygame.BLEND_MULT)
        return new_image


class PlayerProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/sprites/projectiles/Projectile_Player.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class EnemyProjectile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = None
        self.rect = None
        self.x = random.randint(10, 850)
        self.y = 90
        self.appear = False
        self.rng_ceiling = 1  # Adjust this value as needed
        self.speed = 2

        # Initialize image and rect
        self.set_image(self.choose_projectile())

    def display_enemy_projectile(self):
        rng = random.randint(0, self.rng_ceiling)
        if rng <= 1:
            self.appear = True
            self.rng_ceiling += 200
            print(f"Enemy proj display ceiling: {self.rng_ceiling}")
            return self.appear
        else:
            return self.appear

    def update(self, screen):
        if self.display_enemy_projectile():
            chosen_image = self.choose_projectile()
            self.set_image(chosen_image)
            self.draw(screen)
            self.y += self.speed
            self.rect.y = self.y

            # Check if projectile reaches the bottom of the screen
            if self.rect.top >= WINDOW_HEIGHT:
                self.appear = False
                self.kill()  # Automatically removes from sprite groups
        else:
            pass

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)

    def set_image(self, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))

    @staticmethod
    def choose_projectile():
        projectile_list = [
            "assets/sprites/projectiles/ProjectileB_1.png",
            "assets/sprites/projectiles/ProjectileB_2.png",
            "assets/sprites/projectiles/ProjectileB_3.png",
            "assets/sprites/projectiles/ProjectileB_4.png",
        ]
        return random.choice(projectile_list)


class Shield:
    def __init__(self, x):
        self.x = x
        self.y = 600
        self.shield_width = 110
        self.shield_height = 70
        self.color = DEFENDER_COLOR
        self.image = pygame.image.load("assets/sprites/space__0008_ShieldFull.png").convert_alpha()
        self.image = self.change_image_color(image=self.image, new_color=self.color)
        self.image = pygame.transform.scale(self.image, (self.shield_width, self.shield_height))

    def draw(self, screen):
        # Draw player image at the current position
        screen.blit(self.image, (self.x, self.y))

    @staticmethod
    def change_image_color(image, new_color):
        # Create a copy of the original image
        new_image = image.copy()
        # Fill the image with the new color
        new_image.fill(new_color, special_flags=pygame.BLEND_MULT)
        return new_image


class Baseline:
    def __init__(self):
        self.x = 40
        self.y = 780
        self.line_width = 950
        self.line_height = 5
        self.rect = pygame.Rect(self.x, self.y, self.line_width, self.line_height)
        self.color = DEFENDER_COLOR

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def draw_credits_text(self, screen):
        # Load the font
        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        # Create a text surface with "Credits"
        text_surface = font.render("C R E D I T   0 0", True, (255, 255, 255))  # White color
        # Get the rectangle of the text surface
        text_rect = text_surface.get_rect()
        # Set the position of the text surface relative to the baseline
        text_rect.midtop = (self.line_width - 150, self.y + 5)  # Adjust the vertical position as needed
        # Draw the text surface on the screen
        screen.blit(text_surface, text_rect)