# PokerNow Bot Framework

Welcome to the PokerNow Bot Framework, an advanced Python automation tool designed to interact with the "PokerNow" platform. Leveraging the power of Selenium, this framework offers a robust solution for automating game actions, managing sessions through cookies, and intelligently parsing the game state to make real-time decisions. Whether you're developing strategies for automated gameplay or conducting analysis on poker games, this framework provides the necessary tools to enhance your "PokerNow" experience.

## Features

- **Automated Session Management**: Seamlessly manage your sessions with automated cookie handling, allowing for persistent connections and ease of access to your "Poker Now" games.
- **Dynamic Game State Analysis**: Capture and interpret the live state of your poker game, including details such as pot size, community cards, player actions, and much more.
- **Strategic Action Execution**: Implement and execute custom strategies with supported actions like folding, checking, calling, and raising, tailored to the current game scenario.
- **Customizable Framework**: Designed with extensibility in mind, allowing for the integration of complex strategies and analytical tools to refine your poker playing algorithm.

## Getting Started

### Prerequisites

Ensure you have the following installed before proceeding:
- Python 3.6+
- Google Chrome or Mozilla Firefox
- Corresponding ChromeDriver or GeckoDriver for Selenium

### Installation

Clone the repository to your machine:

```sh
git clone https://github.com/Zehmosu/PokerNow.git
cd PokerNow
```

Install the necessary dependencies:

```sh
pip install -r requirements.txt
```

### Configuration

1. Update `cookie_path` in the `PokerClient` class with the path to your cookie file to enable session persistence.
2. Configure your bot by modifying the `PokerClient` initialization in your script to suit your game settings and strategies.


## Documentation

This section provides detailed explanations of the primary classes and methods within the PokerNow Bot Framework, guiding you through their purpose, parameters, and usage.

### Classes and Their Methods

#### `PokerClient`

Responsible for navigating to the "PokerNow" website, managing cookies, and orchestrating the overall game interaction.

- **`__init__(self, driver, cookie_path='pokernow_cookies.pkl')`**:
  - Initializes the poker client with a Selenium WebDriver and a path for cookie storage.
  - **Parameters**:
    - `driver`: Instance of Selenium WebDriver.
    - `cookie_path`: String path to save or load cookies.

- **`navigate(self, url)`**:
  - Navigates the WebDriver to a specified URL.
  - **Parameters**:
    - `url`: The URL to navigate to.

#### `CookieManager`

Handles the loading and saving of cookies for session persistence.

- **`load_cookies(self)`**:
  - Loads cookies from a file into the Selenium browser session.
- **`save_cookies(self)`**:
  - Saves the current session cookies to a file.

#### `GameStateManager`

Extracts and constructs the current game state from the "Poker Now" web interface.

- **`get_game_state(self)`**:
  - Returns a `GameState` object representing the current state of the game.

#### `ActionHelper`

Facilitates the execution of game actions such as fold, check, call, and raise.

- **`get_available_actions(self)`**:
  - Returns a dictionary of the actions currently available to the player.
- **`perform_action(self, action, amount=None)`**:
  - Executes a specified action.
  - **Parameters**:
    - `action`: The action to perform (e.g., 'Raise', 'Call').
    - `amount`: Optional amount for the 'Raise' action.

#### `ElementHelper`

Provides utility methods for interacting with web elements.

- **`get_text(self, selector, context=None)`**:
  - Retrieves text from a specified element.
  - **Parameters**:
    - `selector`: CSS selector for the element.
    - `context`: Optional parent element to scope the search.

- **`get_element(self, selector)`**:
  - Finds and returns a single web element matching the selector.
  - **Parameters**:
    - `selector`: CSS selector for the element.

- **`get_elements(self, selector)`**:
  - Finds and returns a list of web elements matching the selector.
  - **Parameters**:
    - `selector`: CSS selector for the elements.

### Usage Examples

#### Initializing the PokerClient

```python
from selenium import webdriver
from poker_bot import PokerClient

driver = webdriver.Chrome('/path/to/chromedriver')
poker_client = PokerClient(driver)
poker_client.navigate('https://pokernow.club/')
```

#### Loading and Saving Cookies

```python
# Load cookies to resume a session
poker_client.cookie_manager.load_cookies()

# Save cookies for future sessions
poker_client.cookie_manager.save_cookies()
```

#### Extracting Game State

```python
game_state = poker_client.game_state_manager.get_game_state()
print(game_state.players)
print(game_state.pot_size)
```

#### Performing Actions

```python
# Check if 'Raise' is an available action and perform it with an amount
poker_client.action_helper.perform_action('Raise', amount=100)

# Fold if it's the current player's turn
poker_client.action_helper.perform_action('Fold')
```

## Development

This framework is open for contributions! If you have improvements or new features in mind, feel free to fork the repo and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- Thanks to "PokerNow" for providing an engaging platform for poker enthusiasts.
- Selenium WebDriver for the incredible web automation capabilities.
