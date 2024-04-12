import pygame
from game import main
from config import (ENEMY_STARTING_SPEED, STARTING_SCORE, STARTING_PROJECTILE_COOLDOWN, ENEMY_PROJECTILE_SPAWN_CHANCE,
                    ENEMY_PROJECTILE_SPEED)

"""TODO
- Add gameover screen functionality(restart or quit?)
- Add game mechanic for enemies getting to close to shields and eventually killing player if they get low enough
- clear print statements
- asses methods for non needed code
- push to github
"""

main(ENEMY_STARTING_SPEED, STARTING_SCORE, STARTING_PROJECTILE_COOLDOWN, ENEMY_PROJECTILE_SPAWN_CHANCE,
     ENEMY_PROJECTILE_SPEED)

"""['arial', 'arialblack', 'bahnschrift', 'calibri', 'cambria', 'cambriamath', 'candara', 'comicsansms', 'consolas',
 'constantia', 'corbel', 'couriernew', 'ebrima', 'franklingothicmedium', 'gabriola', 'gadugi', 'georgia', 'impact',
  'inkfree', 'javanesetext', 'leelawadeeui', 'leelawadeeuisemilight', 'lucidaconsole', 'lucidasans', 'malgungothic', 'malgungothicsemilight', 'microsofthimalaya', 'microsoftjhenghei', 'microsoftjhengheiui', 'microsoftnewtailue', 'microsoftphagspa', 'microsoftsansserif', 'microsofttaile', 'microsoftyahei', 'microsoftyaheiui', 'microsoftyibaiti', 'mingliuextb', 'pmingliuextb', 'mingliuhkscsextb', 'mongolianbaiti', 'msgothic', 'msuigothic', 'mspgothic', 'mvboli', 'myanmartext', 'nirmalaui', 'nirmalauisemilight', 'palatinolinotype', 'segoemdl2assets', 'segoeprint', 'segoescript', 'segoeui', 'segoeuiblack', 'segoeuiemoji', 'segoeuihistoric', 'segoeuisemibold', 'segoeuisemilight', 'segoeuisymbol', 'simsun', 'nsimsun', 'simsunextb', 'sitkasmall', 'sitkatext', 'sitkasubheading', 'sitkaheading', 'sitkadisplay', 'sitkabanner', 'sylfaen', 'symbol', 'tahoma', 'timesnewroman', 'trebuchetms', 'verdana', 'webdings', 'wingdings', 'yugothic', 'yugothicuisemibold', 'yugothicui', 'yugothicmedium', 'yugothicuiregular', 'yugothicregular', 'yugothicuisemilight', 'holomdl2assets', 'gayatri', 'gothamblack', 'gothambook', 'applesdgothicneo', 'notosansjp']"""
