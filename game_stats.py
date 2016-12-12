#game_stats.py
class GameStats():
	"""Track statistics"""

	def __init__(self,ai_settings):
		"""Initialize stats"""
		self.ai_settings = ai_settings
		self.reset_stats()

                self.high_score = 0
		# sTART 
		self.game_active = False

	def reset_stats(self):
		"""initialize stats that will change during gameplay"""
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		
