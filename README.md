Here's the updated README.md with the new `is_your_turn` method added to the `GameStateManager` class:

```markdown
# PokerNow Client

A client for interacting with PokerNow.club using Selenium.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [PokerClient](#pokerclient)
  - [Initialization](#initialization)
  - [Methods](#methods)
- [GameStateManager](#gamestatemanager)
  - [get_game_state](#get_game_state)
  - [is_your_turn](#is_your_turn)
  - [get_winners](#get_winners)
  - [get_community_cards](#get_community_cards)
  - [get_players_info](#get_players_info)
  - [get_player_status](#get_player_status)
  - [get_player_cards](#get_player_cards)
  - [get_dealer_position](#get_dealer_position)
  - [get_current_player](#get_current_player)
  - [get_blinds](#get_blinds)
  - [parse_stack_value](#parse_stack_value)
- [ActionHelper](#actionhelper)
  - [get_available_actions](#get_available_actions)
  - [perform_action](#perform_action)
  - [handle_raise](#handle_raise)
  - [check_and_handle_fold_confirmation](#check_and_handle_fold_confirmation)
- [ElementHelper](#elementhelper)
  - [wait_for_element](#wait_for_element)
  - [is_element_present](#is_element_present)
  - [get_text](#get_text)
  - [get_element](#get_element)
  - [get_elements](#get_elements)
- [Models](#models)
  - [Card](#card)
  - [GameState](#gamestate)
  - [PlayerInfo](#playerinfo)
  - [PlayerState](#playerstate)
- [CookieManager](#cookiemanager)
  - [load_cookies](#load_cookies)
  - [save_cookies](#save_cookies)
- [Support](#support)
- [Contributing](#contributing)
- [License](#license)

## Installation

You can install the PokerNow Client using pip:

```
pip install PokerNow
```

## Usage

Here's an example of how to use the PokerNow Client:

```python
from selenium import webdriver
from pokernow import PokerClient
import time

# Create a new instance of a WebDriver
driver = webdriver.Firefox()

# Initialize the PokerClient with the driver and specify the cookie file path
client = PokerClient(driver, cookie_path='cookie_file.pkl')

# Navigate to the PokerNow.club login page
client.navigate('https://network.pokernow.club/sessions/new')

# Wait for the user to manually complete the login process and press Enter
input("Please complete the login process in the browser and press Enter to continue...")

# Save the cookies after successful login
client.cookie_manager.save_cookies()

# Navigate to a specific game or table (replace with your actual game link)
client.navigate('https://www.pokernow.club/games/pglev4PZzEvMv6DGgVNGbZz5J')

# Wait for the game to load
time.sleep(5)

# Retrieve the current game state
game_state = client.game_state_manager.get_game_state()
print("Game Type:", game_state.game_type)
print("Pot Size:", game_state.pot_size)
print("Community Cards:", [str(card) for card in game_state.community_cards])
print("Players:")
for player in game_state.players:
    print("  Name:", player.name)
    print("  Stack:", player.stack)
    print("  Bet:", player.bet_value)
    print("  Cards:", [str(card) for card in player.cards])
    print("  Status:", player.status)
    print("  Hand Message:", player.hand_message)
print("Dealer Position:", game_state.dealer_position)
print("Current Player:", game_state.current_player)
print("Blinds:", game_state.blinds)
print("Winners:")
for winner in game_state.winners:
    print("  Name:", winner['name'])
    print("  Stack Info:", winner['stack_info'])
print("Is Your Turn:", game_state.is_your_turn)

# Perform actions based on the game state and your strategy
available_actions = client.action_helper.get_available_actions()
print("Available Actions:", list(available_actions.keys()))

if 'Call' in available_actions:
    client.action_helper.perform_action('Call')
elif 'Check' in available_actions:
    client.action_helper.perform_action('Check')
elif 'Raise' in available_actions:
    client.action_helper.perform_action('Raise', amount=100)
else:
    client.action_helper.perform_action('Fold')

# Close the browser when finished
driver.quit()
```

Make sure to have the appropriate WebDriver (e.g., ChromeDriver) installed and available in your system's PATH.

## PokerClient

The `PokerClient` class is the main entry point for interacting with PokerNow.club.

### Initialization

```python
def __init__(self, driver, cookie_path='pokernow_cookies.pkl')
```

- `driver`: The Selenium WebDriver instance.
- `cookie_path` (optional): The path to the cookie file for storing and loading cookies. Default is 'pokernow_cookies.pkl'.

### Methods

- `navigate(url)`: Navigates to the specified URL.

## GameStateManager

The `GameStateManager` class is responsible for managing and retrieving the game state information.

### get_game_state

```python
def get_game_state(self)
```

Retrieves the current game state, including game type, pot size, community cards, players' information, dealer position, current player, blinds, winners, and whether it's your turn.

### is_your_turn

```python
def is_your_turn(self)
```

Checks if it's your turn to act in the current game.

### get_winners

```python
def get_winners(self)
```

Retrieves the winners of the current hand, including their names and stack information.

### get_community_cards

```python
def get_community_cards(self)
```

Retrieves the community cards on the table.

### get_players_info

```python
def get_players_info(self)
```

Retrieves information about all players at the table, including their names, stack sizes, bet values, cards, status, and hand messages.

### get_player_status

```python
def get_player_status(self, player_element)
```

Determines the status of a player based on the player element.

### get_player_cards

```python
def get_player_cards(self, player_element)
```

Retrieves the cards of a player based on the player element.

### get_dealer_position

```python
def get_dealer_position(self)
```

Retrieves the position of the dealer button.

### get_current_player

```python
def get_current_player(self)
```

Retrieves the name of the current player.

### get_blinds

```python
def get_blinds(self)
```

Retrieves the values of the blinds.

### parse_stack_value

```python
def parse_stack_value(self, stack_value)
```

Parses the stack value string and returns the numeric value.

## ActionHelper

The `ActionHelper` class provides methods for interacting with the game and performing actions.

### get_available_actions

```python
def get_available_actions(self)
```

Retrieves the available actions for the current player.

### perform_action

```python
def perform_action(self, action, amount=None)
```

Performs the specified action (e.g., 'Call', 'Raise', 'Check', 'Fold') with an optional amount for raising.

### handle_raise

```python
def handle_raise(self, amount)
```

Handles the raise action by entering the raise amount and confirming the bet.

### check_and_handle_fold_confirmation

```python
def check_and_handle_fold_confirmation(self)
```

Checks for a fold confirmation dialog and handles it if present.

## ElementHelper

The `ElementHelper` class provides utility methods for interacting with web elements using Selenium.

### wait_for_element

```python
def wait_for_element(self, selector, timeout=10)
```

Waits for an element to be present on the page within the specified timeout.

### is_element_present

```python
def is_element_present(self, selector)
```

Checks if an element is present on the page.

### get_text

```python
def get_text(self, selector, context=None)
```

Retrieves the text of an element specified by the selector, optionally within a specific context element.

### get_element

```python
def get_element(self, selector)
```

Retrieves a single element specified by the selector.

### get_elements

```python
def get_elements(self, selector)
```

Retrieves multiple elements specified by the selector.

## Models

The `models` module contains data models used throughout the project.

### Card

Represents a playing card with rank and suit.

### GameState

Represents the state of the game, including game type, pot size, community cards, players' information, dealer position, current player, blinds, winners, and whether it's your turn.

### PlayerInfo

Represents information about a player, including name, stack size, bet value, cards, status, and hand message.

### PlayerState

Enum representing the possible states of a player (CURRENT, FOLDED, OFFLINE, ACTIVE).

## CookieManager

The `CookieManager` class handles loading and saving cookies for the PokerNow.club website.

### load_cookies

```python
def load_cookies(self)
```

Loads cookies from the specified cookie file, if it exists.

### save_cookies

```python
def save_cookies(self)
```

Saves the current cookies to the specified cookie file.

## Support

If you find this project helpful and would like to support its development, you can buy me a coffee at [https://buymeacoffee.com/zehm](https://buymeacoffee.com/zehm). Your support is greatly appreciated!

## Contributing

Contributions are welcome! Please submit a pull request or open an issue on the GitHub repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
```
