
import pygame

from settings import Settings
from ship import Ship
from game_stats import GameStats
import game_functions as gf
from pygame.sprite import Group

from button import Button
from scoreboard import Scoreboard

def run_game():
#initializing game and create a screen 
    pygame.init()
    ai_settings = Settings()

    screen = pygame.display.set_mode((
            ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    ship = Ship(ai_settings, screen)

    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    #make a group to store bullets
    bullets = Group()
    play_button = Button(ai_settings,screen,"Play")
    #make an alien
    aliens = Group()

    gf.create_fleet(ai_settings, screen, ship, aliens)
#start the main loop for gameplay
    while True:
        #note any keyboard clicks or mouse clicks
        #if the game is active we still need to check if user quits game
        gf.check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets)

        if stats.game_active:
            ship.update()
            gf.update_aliens(ai_settings,stats, screen, ship, aliens,bullets)
            gf.update_bullets(ai_settings,screen,stats,sb, ship, aliens,bullets)
        gf.update_screen(ai_settings, screen,stats, sb, ship, aliens, bullets, play_button)
run_game()
