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

### Running the Bot

To start the bot, use the following example as a guide:

```python
from selenium import webdriver
from poker_bot import PokerClient

# Initialize Selenium WebDriver
driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

# Create and configure the PokerClient
poker_client = PokerClient(driver)
poker_client.navigate('https://pokernow.club/games/YOUR_GAME_ID')
```

## Development

This framework is open for contributions! If you have improvements or new features in mind, feel free to fork the repo and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- Thanks to "PokerNow" for providing an engaging platform for poker enthusiasts.
- Selenium WebDriver for the incredible web automation capabilities.
