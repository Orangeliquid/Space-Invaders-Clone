from game import main
import pygame
import sys
from config import (ENEMY_STARTING_SPEED, STARTING_SCORE, STARTING_PROJECTILE_COOLDOWN, ENEMY_PROJECTILE_SPAWN_CHANCE,
                    ENEMY_PROJECTILE_SPEED, INTRO_STATUS)

"""TODO
- Add game mechanic for enemies getting to close to shields and eventually killing player if they get low enough
- clear print statements
- asses methods for non needed code
- push to github
"""

round_count = 1
game_over = False

while not game_over:
    # Call starting parameters main function call for round start
    if round_count == 1:
        result = main(ENEMY_STARTING_SPEED, STARTING_SCORE, STARTING_PROJECTILE_COOLDOWN, ENEMY_PROJECTILE_SPAWN_CHANCE,
                      ENEMY_PROJECTILE_SPEED, INTRO_STATUS)
    else:
        # Handle subsequent rounds with updated parameters
        result = main(enemy_speed, last_score, max_projectile_cooldown, enemy_projectile_spawn_chance,
                      enemy_projectile_speed, intro_status)

    # Check the result of the main function call
    if result[0] == "new_round":
        # Start a new round with updated parameters
        (enemy_speed, last_score, max_projectile_cooldown, enemy_projectile_spawn_chance, enemy_projectile_speed,
         intro_status) = result[1]
        round_count += 1

    elif result == "restart":
        # Restart the game
        round_count = 1
        enemy_speed = ENEMY_STARTING_SPEED
        last_score = STARTING_SCORE
        max_projectile_cooldown = STARTING_PROJECTILE_COOLDOWN
        enemy_projectile_spawn_chance = ENEMY_PROJECTILE_SPAWN_CHANCE
        enemy_projectile_speed = ENEMY_PROJECTILE_SPEED

    elif result == "exit":
        # Exit the game loop
        game_over = True
        pygame.quit()
        sys.exit()


"""['arial', 'arialblack', 'bahnschrift', 'calibri', 'cambria', 'cambriamath', 'candara', 'comicsansms', 'consolas',
 'constantia', 'corbel', 'couriernew', 'ebrima', 'franklingothicmedium', 'gabriola', 'gadugi', 'georgia', 'impact',
  'inkfree', 'javanesetext', 'leelawadeeui', 'leelawadeeuisemilight', 'lucidaconsole', 'lucidasans', 'malgungothic', 'malgungothicsemilight', 'microsofthimalaya', 'microsoftjhenghei', 'microsoftjhengheiui', 'microsoftnewtailue', 'microsoftphagspa', 'microsoftsansserif', 'microsofttaile', 'microsoftyahei', 'microsoftyaheiui', 'microsoftyibaiti', 'mingliuextb', 'pmingliuextb', 'mingliuhkscsextb', 'mongolianbaiti', 'msgothic', 'msuigothic', 'mspgothic', 'mvboli', 'myanmartext', 'nirmalaui', 'nirmalauisemilight', 'palatinolinotype', 'segoemdl2assets', 'segoeprint', 'segoescript', 'segoeui', 'segoeuiblack', 'segoeuiemoji', 'segoeuihistoric', 'segoeuisemibold', 'segoeuisemilight', 'segoeuisymbol', 'simsun', 'nsimsun', 'simsunextb', 'sitkasmall', 'sitkatext', 'sitkasubheading', 'sitkaheading', 'sitkadisplay', 'sitkabanner', 'sylfaen', 'symbol', 'tahoma', 'timesnewroman', 'trebuchetms', 'verdana', 'webdings', 'wingdings', 'yugothic', 'yugothicuisemibold', 'yugothicui', 'yugothicmedium', 'yugothicuiregular', 'yugothicregular', 'yugothicuisemilight', 'holomdl2assets', 'gayatri', 'gothamblack', 'gothambook', 'applesdgothicneo', 'notosansjp']"""
