# PokerNow Bot Framework 

## Introduction

The PokerNow Bot Framework is a sophisticated Python library that automates interactions on the "PokerNow" platform. Built atop Selenium, it provides an array of functionalities designed for automating game decisions, session management through cookies, and analyzing the game state in real-time. This tool is perfect for those looking to develop automated strategies for poker gameplay or for analytical purposes, offering a deep dive into the mechanics of online poker.

## Core Features

- **Session Management**: Automated cookie handling ensures seamless session continuity and easy access to poker games.
- **Real-time Game Analysis**: Interprets the live game state, including pot size, community cards, and player actions, to inform strategy decisions.
- **Automated Game Actions**: Supports strategic gameplay through automated actions like folding, checking, calling, and raising based on the game state.
- **Framework Customization**: Offers a flexible architecture for the integration of advanced strategies and analytics, enabling users to tailor the bot's behavior to their preferences.

## Installation Guide

### System Requirements

- Python 3.6 or newer
- Google Chrome or Mozilla Firefox
- Selenium WebDriver compatible with your browser version

### Setup Instructions

Clone the PokerNow Bot Framework repository:

```sh
git clone https://github.com/Zehmosu/PokerNow.git
cd PokerNow
```

Install the required Python dependencies:

```sh
pip install -r requirements.txt
```

### Configuration Steps

1. **Cookie Management**: Specify the path to your cookie file in the `PokerClient` constructor to enable automatic session handling.
2. **Bot Customization**: Adjust the initialization parameters in `PokerClient` to fit your game's configuration and strategic approach.

## Detailed Documentation

### Key Components

#### `PokerClient`

The central orchestrator for navigating "PokerNow", handling sessions, and managing game interactions.

- **`__init__(driver, cookie_path='pokernow_cookies.pkl')`**: Sets up the client with a WebDriver instance and a cookie storage path.
- **`navigate(url)`**: Directs the WebDriver to a specified URL.

#### `CookieManager`

Manages browser cookies to maintain session states across gameplays.

- **`load_cookies()`**: Imports cookies from a file into the browser session.
- **`save_cookies()`**: Exports current session cookies to a file.

#### `GameStateManager`

Analyzes the webpage to construct a current representation of the game state.

- **`get_game_state()`**: Retrieves a snapshot of the current game state.

#### `ActionHelper`

Enables the execution of in-game actions based on available options and strategy.

- **`get_available_actions()`**: Lists actions that the player can currently take.
- **`perform_action(action, amount=None)`**: Executes a chosen action, optionally specifying an amount for actions like raising.

#### `ElementHelper`

Facilitates interaction with web elements using Selenium, aiding in data extraction and action execution.

- **`get_text(selector, context=None)`**: Extracts text from specified elements.
- **`get_element(selector)`**: Retrieves a single element matching the selector.
- **`get_elements(selector)`**: Retrieves a list of elements matching the selector.

### Advanced Usage Examples

#### Starting a Session

```python
from selenium import webdriver
from poker_bot import PokerClient

driver = webdriver.Chrome('/path/to/chromedriver')
poker_client = PokerClient(driver)
poker_client.navigate('https://pokernow.club/games/YOUR_GAME_ID')
```

#### Session and Game State Management

```python
# Assume you're continuing a previous session
poker_client.cookie_manager.load_cookies()

# Refresh the game state to reflect the current situation
game_state = poker_client.game_state_manager.get_game_state()
print("Current Pot Size:", game_state.pot_size)
```

#### Automated Decision Making

```python
# Example of a simple decision-making logic
if 'Raise' in poker_client.action_helper.get_available_actions():
    poker_client.action_helper.perform_action('Raise', amount=50)
else:
    poker_client.action_helper.perform_action('Check')
```

## Contributing

We welcome contributions to the PokerNow Bot Framework! Whether you're fixing bugs, adding new features, or improving the documentation, your help is appreciated. Please fork the repository and submit a pull request with your changes.

## Acknowledgements

- "PokerNow" for creating a platform that brings poker enthusiasts together online.
- The Selenium project, for their powerful tools for web automation.

## License

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file included with the code.

This enhanced README provides a comprehensive overview of the PokerNow Bot Framework, ensuring users have all the information needed to get started, understand the framework's capabilities, and

 contribute to its development.
