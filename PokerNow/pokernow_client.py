import time
from managers import CookieManager, GameStateManager, ActionHelper, ElementHelper

class PokerClient:
    def __init__(self, driver, cookie_path='pokernow_cookies.pkl'):
        self.home_url = 'https://pokernow.club/'
        self.driver = driver
        self.cookie_manager = CookieManager(driver, cookie_path)
        self.element_helper = ElementHelper(driver)
        self.game_state_manager = GameStateManager(self.element_helper)
        self.action_helper = ActionHelper(self.element_helper)
        self.navigate(self.home_url)
        self.cookie_manager.load_cookies()
        self.driver.refresh()

    def navigate(self, url):
        self.driver.get(url)