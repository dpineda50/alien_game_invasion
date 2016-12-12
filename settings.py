class Settings():
    """A class to store all settings for Alien Invasion"""
    def __init__(self):
        """Initialize the game's settings."""
        #Screen settings
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (230,230,230)

        #Ship Settings
        self.ship_speed_factor = 4
        self.ship_limit = 3
        
        #aliensssss
        self.alien_speed_factor = 2
        self.fleet_drop_speed = 4


        #alien directions
        self.fleet_direction = 1


        # Bullet Settings
        self.bullet_speed_factor = 5
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 3  

        #how quickly the game will increase in difficulty
        self.speedup_scale = 1.1

        #how quickly aliens are worth increases
        self.score_scale = 1.5

        self.initialize_dynamic_settings()
    def initialize_dynamic_settings(self):
        """Initialize the dynamice settings"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        #scoring
        self.alien_points = 50
        
        
        self.fleet_direction = 1
    def increase_speed(self):
        """Increase speed settings and alien points"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        
          
