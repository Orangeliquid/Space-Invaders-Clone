import pygame
import sys
import random
from entities import Player, Baseline, Shield, Enemy, Ufo, EnemyProjectile
from score import Lives, Scoreboard
from config import WINDOW_WIDTH, WINDOW_HEIGHT, STARTING_PLAYER_LIVES, FONT_NAME, FONT_SIZE, DEFENDER_COLOR, UFO_COLOR


def main(enemy_speed, starting_score, max_projectile_cooldown, enemy_projectile_spawn_chance, enemy_projectile_speed,
         intro_status):
    pygame.init()
    clock = pygame.time.Clock()

    window_width, window_height = WINDOW_WIDTH, WINDOW_HEIGHT
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Space Invaders")

    # Create scoreboard on screen
    scoreboard = Scoreboard(starting_score)

    # Create Baseline on screen
    baseline = Baseline()

    # Creates the player platform
    player = Player(max_projectile_cooldown, STARTING_PLAYER_LIVES)
    player_single = pygame.sprite.GroupSingle(player)

    # Create the lives object and pass then player instance
    lives = Lives(player, 3)  # Assuming the player starts with 3 lives

    # Create the UFO object
    ufo_instance = Ufo()
    ufo_single = pygame.sprite.GroupSingle(ufo_instance)

    # Create the shields
    all_shields = pygame.sprite.Group()
    shield_x_positions = [150, 350, 550, 750]
    for x in shield_x_positions:
        shield = Shield(x)
        all_shields.add(shield)
    # print(all_shields)

    # Create a group to hold all the enemy sprites
    all_enemies = pygame.sprite.Group()

    # Create and add 40 point aliens (type 'A')
    for i in range(11):
        enemy = Enemy(50 + i * 60, 100, 'A', speed=enemy_speed)
        all_enemies.add(enemy)

    # Create and add 20 point aliens (type 'B')
    for i in range(11):
        for j in range(2):
            enemy = Enemy(50 + i * 60, 150 + j * 50, 'B', speed=enemy_speed)
            all_enemies.add(enemy)

    # Create and add 10 point aliens (type 'C')
    for i in range(11):
        for j in range(2):
            enemy = Enemy(50 + i * 60, 250 + j * 50, 'C', speed=enemy_speed)
            all_enemies.add(enemy)

    # Add a flag to check if the space bar is pressed
    space_pressed = False

    # Add a flag to determine if an enemy projectile is active
    enemy_projectile_active = False

    font = pygame.font.Font(FONT_NAME, FONT_SIZE)
    # Introductory phase
    intro_text = font.render("Space Invaders!", True, DEFENDER_COLOR)
    screen.blit(intro_text, (300, 350))
    pygame.display.flip()

    intro_active = intro_status

    # Introductory phase
    while intro_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Check for key press to skip intro
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_SPACE]:
            intro_active = False

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left = True
                elif event.key == pygame.K_RIGHT:
                    player.move_right = True
                elif event.key == pygame.K_SPACE:
                    # Set the flag to indicate space bar is pressed
                    space_pressed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.move_left = False
                elif event.key == pygame.K_RIGHT:
                    player.move_right = False
                elif event.key == pygame.K_SPACE:
                    # Reset the flag when space bar is released
                    space_pressed = False

        # Shoot if space bar is held down
        if space_pressed:
            player.shoot()

        # Move the player based on key states
        if player.move_left:
            player.move("left")
        if player.move_right:
            player.move("right")

        # Clear the screen
        screen.fill((0, 0, 0))

        # Update game states
        player.update_projectiles(screen, all_enemies, ufo_single, scoreboard, all_shields)
        all_enemies.update(screen, all_shields, player_single)
        lives.update_lives(screen)

        # Draw static scoreboard
        scoreboard.draw_starting_score(screen)
        scoreboard.draw_static_score(screen)

        # Draw Baseline
        baseline.draw(screen)
        baseline.draw_credits_text(screen)

        # Draw Lives
        lives.draw_lives_text(screen)
        lives.draw_player_sprites(screen)

        # Draw the player/platform
        player.draw(screen)

        # Draw the shields
        for shield in all_shields:
            shield.draw(screen)

        # Check if there are enemies to move
        if len(all_enemies) > 0:
            # Move the enemy group
            Enemy.move_group()

        # draw projectiles
        player.draw_projectiles(screen)

        # draw the enemies and ufo
        all_enemies.draw(screen)
        ufo_single.update(screen)

        # Check if there's no enemy projectile on the screen, then spawn a new one
        if not enemy_projectile_active:
            if random.randint(0, 1000) <= enemy_projectile_spawn_chance:
                enemy_projectile_active = True
                new_enemy_projectile = EnemyProjectile(enemy_projectile_speed)  # Create a new instance
        else:
            # Update the existing enemy projectile
            new_enemy_projectile.update(screen, scoreboard, all_shields, player_single, lives)
            if not new_enemy_projectile.appear:  # Check if it's no longer visible
                enemy_projectile_active = False  # Set the flag to False

        # Check if player has expended all lives
        if player.lives == 0:
            # Display game over message
            game_over_text = font.render("Game Over", True, UFO_COLOR)
            screen.blit(game_over_text, (330, 200))
            pygame.display.flip()
            pygame.time.delay(2000)  # Wait for 2 seconds before checking for user input

            # Ask the user if they want to play again
            replay_text = font.render("Press Enter to Play Again", True, UFO_COLOR)
            screen.blit(replay_text, (100, 300))
            pygame.display.flip()

            # This extra blit will be displayed under the blit above
            replay_text = font.render("or Backspace to Exit", False, UFO_COLOR)
            screen.blit(replay_text, (150, 400))
            pygame.display.flip()

            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:  # Enter key
                            return "restart"
                        elif event.key == pygame.K_BACKSPACE:
                            return "exit"

        # Check if all enemies are dead beside ufo
        elif all_enemies is None or len(all_enemies) == 0:
            print("All enemies are dead")
            print(f"all_enemies total: {all_enemies}")

            # Increase the speed of all enemies
            enemy_speed += 1

            # Maintain current score
            last_score = scoreboard.score

            # increase shooting speed by lowering max projectile cooldown
            max_projectile_cooldown -= .5

            # increase chance for enemy projectile to spawn
            enemy_projectile_spawn_chance += 5

            # increase enemy projectile speed
            enemy_projectile_speed += 1

            # intro status false, it only plays for the first round
            intro_status = False

            # Restart the level or proceed to the next level
            return "new_round", (enemy_speed, last_score, max_projectile_cooldown, enemy_projectile_spawn_chance,
                                 enemy_projectile_speed, intro_status)
        else:
            pass

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)
