from bullet import Bullet
import sys
import pygame
from time import sleep
from alien import Alien
from button import Button

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create a fleet of aliens"""
    #we need to figure how many aliens fit on screen
    #so we create one and divide see how many would fit on the screen
    #also remember to leave space between aliens
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    
    alien.x = alien_width + 2 * alien_width * alien_number
    
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_of_rows(ai_settings, ship_height, alien_height):
    """ how many rows fit in the screen"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2* alien_height))
    return number_rows

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to key presses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        #create a bullet when space is pressed
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.QUIT:
        pygame.display.quit()
        sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
    """FIre a bullet"""
    if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)

def check_keyup_events(event,ship):
    """Respond to Key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
                
def check_events(ai_settings, screen, stats, play_button, ship, aliens,bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)

def check_play_button(ai_settings, screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    """Start a new game when clicking play button"""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    #Make sure that clicking in the middle of the game
    #where the play button would be, won't create a new game
    #weird small but
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        
        #I think the mouse is distracting
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

def update_screen(ai_settings, screen,stats,sb, ship, aliens, bullets, play_button):
    """Update images on the screen and flip to the new screen."""
    screen.fill(ai_settings.bg_color)
    #redraw all bullets behind ships and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    #if state is false, we draw a play button
    if not stats.game_active:
        play_button.draw_button()
    
    pygame.display.flip()

def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets):
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #the alien is inflicting pain on the ship
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
            break

def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):
    """Update aliens position"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()

    #look for alien-ship collision
    #spritecollideany(sprite,group)
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
        print("YOU WERE TOO LATE!")
    check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets)
    
    
def update_bullets(ai_settings,screen,stats,sb,ship,aliens, bullets):
    """update position of bullets and get rid of old bullets."""
    # update bullet positions.
    bullets.update()

        #we need to check if bullet is out of bounds
        #create a copy for the for loop as to not destroy the iterator
        #making sure we check every bullet
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats,sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """REspond to bullet-alien collisions."""
    #remove any bullets that have collided
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()

    if len(aliens)== 0:
        #Destroy existing bullets,speed up game and create new fleet"
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings,screen,ship,aliens)

def get_number_of_aliens_x(ai_settings, alien_width):
    """Figuring out how many aliens fit in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_of_aliens_x = int(available_space_x / (2 * alien_width))
    return number_of_aliens_x

def create_fleet(ai_settings, screen, ship, aliens):
    """create a fleet"""
    alien = Alien(ai_settings, screen)
    number_of_aliens_x = get_number_of_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_of_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_of_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
def check_fleet_edges(ai_settings,aliens):
    """REspon appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break;
def change_fleet_direction(ai_settings,aliens):
    """Drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """REspond to ship being hit"""
    if stats.ships_left > 0:
        #decrement ships_left
        stats.ships_left -= 1
        #  empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #Create a new fleet and center the ship
        create_fleet(ai_settings,screen, ship, aliens)
        ship.center_ship()

        #Hol' up
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
def chech_high_score(stats,sb):
    """Check if there is a new high score"""
    if stats.score > stats.hihg_score:
        stats.high_score = stats.score
        sb.prep_high_score()
