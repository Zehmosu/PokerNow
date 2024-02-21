import os
import pickle
import time
from enum import Enum, auto
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By

# Models
class Card:
    @staticmethod
    def parse_card_class(card_class):
        parts = card_class.split()
        suit = None
        rank = None
        for part in parts:
            if part.startswith("card-s-"):
                rank = part.split("-")[-1].upper()
                rank_dict = {'2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', 'T': '10', 'J': 'Jack', 'Q': 'Queen', 'K': 'King', 'A': 'Ace'}
                rank = rank_dict.get(rank, rank)
            elif part in ["card-c", "card-d", "card-h", "card-s"]:
                suit_dict = {"card-c": "Clubs", "card-d": "Diamonds", "card-h": "Hearts", "card-s": "Spades"}
                suit = suit_dict.get(part)
        return f'{rank} of {suit}' if rank and suit else 'Unknown Card'

class GameState:
    def __init__(self, game_type, pot_size, community_cards, players, dealer_position, current_player, blinds, winners=None):
        self.game_type = game_type
        self.pot_size = pot_size
        self.community_cards = community_cards
        self.players = players
        self.dealer_position = dealer_position
        self.current_player = current_player
        self.blinds = blinds
        self.winners = winners

class PlayerInfo:
    def __init__(self, name, stack, bet_value, cards, status, hand_message=''):
        self.name = name
        self.stack = stack
        self.bet_value = bet_value
        self.cards = cards
        self.status = status
        self.hand_message = hand_message

# Managers
class CookieManager:
    def __init__(self, driver, cookie_path):
        self.driver = driver
        self.cookie_path = cookie_path

    def load_cookies(self):
        if os.path.exists(self.cookie_path):
            cookies = pickle.load(open(self.cookie_path, 'rb'))
            current_url = self.driver.current_url
            for cookie in cookies:
                if cookie.get('domain', '') in current_url:
                    self.driver.add_cookie(cookie)
        else:
            self.save_cookies()

    def save_cookies(self):
        pickle.dump(self.driver.get_cookies(), open(self.cookie_path, 'wb'))

class GameStateManager:
    def __init__(self, element_helper):
        self.element_helper = element_helper

    def get_game_state(self):
        return GameState(
            game_type=self.element_helper.get_text('.table-game-type'),
            pot_size=self.element_helper.get_text('.table-pot-size .main-value'),
            community_cards=self.get_community_cards(),
            players=self.get_players_info(),
            dealer_position=self.get_dealer_position(),
            current_player=self.get_current_player(),
            blinds=self.get_blinds(),
            winners=self.get_winners()
        )
        
    def get_winners(self):
        winners = []
        try:
            winner_elements = self.element_helper.get_elements('.table-player.winner')
            for winner_element in winner_elements:
                # Extract the winner's name
                name = self.element_helper.get_text('.table-player-name a', winner_element)
                
                # Extract the stack value which might include winnings
                stack_value = self.element_helper.get_text('.table-player-stack .normal-value', winner_element)
                
                # Extract the winnings, if there are any
                prize = self.element_helper.get_text('.table-player-stack-prize .normal-value', winner_element)
                stack_with_prize = f"{stack_value} (+{prize})" if prize else stack_value
                
                # Add the winner's information to the list
                winners.append({'name': name, 'stack_info': stack_with_prize})
        except Exception as e:
            print(f"Error getting winners: {e}")
        return winners
        
    def get_community_cards(self):
        card_elements = self.element_helper.get_elements('.table-cards .card-container')
        return [Card.parse_card_class(card.get_attribute('class')) for card in card_elements]

    def get_players_info(self):
        players = []
        for player_element in self.element_helper.get_elements('.table-player'):
            # Extract hand message if available
            hand_message = self.element_helper.get_text('.player-hand-message .name', player_element)

            players.append(PlayerInfo(
                name=self.element_helper.get_text('.table-player-name a', player_element),
                stack=self.parse_stack_value(self.element_helper.get_text('.table-player-stack', player_element)),
                bet_value=self.element_helper.get_text('.table-player-bet-value', player_element),
                cards=self.get_player_cards(player_element),
                status=self.get_player_status(player_element),
                hand_message=hand_message
            ))
        return players

    def get_player_status(self, player_element):
        class_list = player_element.get_attribute('class').split()
        if 'decision-current' in class_list:
            return PlayerState.CURRENT
        if 'fold' in class_list:
            return PlayerState.FOLDED
        if 'fold  offline' in class_list or 'Waiting (Offline)' in class_list:
            return PlayerState.OFFLINE
        return PlayerState.ACTIVE

    def get_player_cards(self, player_element):
        card_elements = player_element.find_elements(By.CSS_SELECTOR, '.table-player-cards .card-container')
        return [Card.parse_card_class(card.get_attribute('class')) for card in card_elements]

    def get_dealer_position(self):
        dealer_button = self.element_helper.get_element('.dealer-button-ctn')
        return dealer_button.get_attribute('class') if dealer_button else 'unknown'

    def get_current_player(self):
        current_player_element = self.element_helper.get_element('.table-player.decision-current')
        return self.element_helper.get_text('.table-player-name a', current_player_element) if current_player_element else 'unknown'

    def get_blinds(self):
        blinds_text = self.element_helper.get_text('.blind-value-ctn .blind-value')
        return blinds_text.split(' / ')

    def parse_stack_value(self, stack_value):
        if '+' in stack_value:
            stack_value = stack_value.split('+')[0]
        return stack_value.strip()

# Helpers
class ActionHelper:
    def __init__(self, element_helper):
        self.element_helper = element_helper

    def get_available_actions(self):
        available_actions = {}
        for action_name, selector in {
            'Call': '.game-decisions-ctn .button-1.call',
            'Raise': '.game-decisions-ctn .button-1.raise',
            'Check': '.game-decisions-ctn .button-1.check',
            'Fold': '.game-decisions-ctn .button-1.fold'
        }.items():
            element = self.element_helper.get_element(selector)
            if element and element.is_displayed() and not element.get_attribute('disabled'):
                available_actions[action_name] = element
        return available_actions

    def perform_action(self, action, amount=None):
        available_actions = self.get_available_actions()
        if action == 'Raise' and available_actions.get('Raise'):
            self.handle_raise(amount)
        elif action in available_actions:
            available_actions[action].click()
            if action == 'Fold':
                self.check_and_handle_fold_confirmation()
        else:
            print(f"Action {action} not available.")

    def handle_raise(self, amount):
        raise_button = self.element_helper.get_element('.game-decisions-ctn .button-1.raise')
        if raise_button:
            raise_button.click()
            time.sleep(1)
            raise_input = self.element_helper.get_element('.raise-controller-form .value-input-ctn .value')
            if raise_input:
                raise_input.clear()
                raise_input.send_keys(str(amount))
            confirm_button = self.element_helper.get_element('.raise-controller-form .bet')
            if confirm_button:
                confirm_button.click()

    def check_and_handle_fold_confirmation(self):
        try:
            confirm_button = self.element_helper.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.alert-1-buttons button.middle-gray')))
            confirm_button.click()
        except Exception as e:
            print(f"Error: {e}")

class ElementHelper:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_element(self, selector, timeout=10):
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            return True
        except TimeoutException:
            print(f"Element {selector} not found within {timeout} seconds")
            return False

    def is_element_present(self, selector):
        try:
            self.driver.find_element(By.CSS_SELECTOR, selector)
            return True
        except NoSuchElementException:
            return False

    def get_text(self, selector, context=None):
        try:
            element = context.find_element(By.CSS_SELECTOR, selector) if context else self.driver.find_element(By.CSS_SELECTOR, selector)
            return element.text.strip()
        except NoSuchElementException:
            return ""

    def get_element(self, selector):
        try:
            return self.driver.find_element(By.CSS_SELECTOR, selector)
        except NoSuchElementException:
            return None

    def get_elements(self, selector):
        try:
            return self.driver.find_elements(By.CSS_SELECTOR, selector)
        except NoSuchElementException:
            return []

# Enums
class PlayerState(Enum):
    ACTIVE = auto()
    FOLDED = auto()
    CURRENT = auto()
    OFFLINE = auto()

class PlayerAction(Enum):
    CALL = auto()
    RAISE = auto()
    CHECK = auto()
    FOLD = auto()

# Client
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