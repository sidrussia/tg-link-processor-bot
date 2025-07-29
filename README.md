# Telegram Link Processor Bot

A Telegram bot for processing links and automatic publishing to channels. The bot automatically:

- 🔗 Extracts links from messages
- 🔄 Processes redirects (including JavaScript redirects via Selenium)
- 🧹 Cleans URLs from unnecessary parameters
- 🏷️ Adds hashtags based on content
- 📢 Publishes processed messages to channel

## ✨ Features

- **Smart URL Processing**: Support for HubSpot and other complex redirects
- **Automatic Hashtags**: Smart hashtag detection based on content
- **Clean Architecture**: Modular code structure
- **Error Handling**: Robust error handling
- **Admin Only**: Security - only admin can use the bot

## 🏗️ Project Architecture

```
bot/
├── main.py                    # Entry point
├── config/
│   └── settings.py           # Configuration
├── services/
│   ├── url_processor.py      # URL processing
│   ├── message_processor.py  # Message processing
│   └── selenium_service.py   # Selenium for JS redirects
└── handlers/
    ├── commands.py           # Command handlers
    └── messages.py           # Message handler
```

## 🚀 Installation and Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/telegram-link-processor-bot.git
cd telegram-link-processor-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup ChromeDriver (for Selenium)

**macOS:**
```bash
# Download ChromeDriver from https://chromedriver.chromium.org
# Extract to chromedriver-mac-x64/ folder
```

**Linux:**
```bash
# Install via package manager or download manually
sudo apt-get install chromium-chromedriver
```

### 4. Create .env File

```bash
cp .env.example .env
```

Edit the `.env` file:

```bash
BOT_TOKEN=your_token_from_botfather
CHANNEL_ID=-1001234567890
ADMIN_USER_ID=your_telegram_id
CHANNEL_USERNAME=channel_name
```

### 5. Getting Required Data

#### Bot Token:
1. Message [@BotFather](https://t.me/botfather)
2. Create bot: `/newbot`
3. Copy the token

#### Channel ID:
1. Add [@userinfobot](https://t.me/userinfobot) to channel
2. Copy channel ID (starts with -100)

#### Your ID:
1. Message [@userinfobot](https://t.me/userinfobot)
2. Copy your ID

## 🎯 Usage

### Start the Bot

```bash
python main.py
```
or
```bash
python3 main.py
```

### Bot Commands

- `/start` - Welcome and help
- `/test_selenium` - Test Selenium functionality
- `/stop` - Stop bot (admin only)

### Message Processing

Send the bot a message with a link:

```
👾 Game: Defeat the creatures that enter the wheel.
https://example.com/link
```

Bot will automatically:
1. Extract the link
2. Process redirects
3. Determine hashtag (#game)
4. Publish to channel:

```
👾 Game: Defeat the creatures that enter the wheel.

https://clean-final-url.com

@your_channel
#game
```

## 🏷️ Hashtag Rules

| Phrase in message     | Hashtag        |
|-----------------------|----------------|
| `useful:`             | `#useful`      |
| `haha:`               | `#haha`        |
| `cure boredom:`       | `#cure`        |
| `that's interesting:` | `#interesting` |
| `that's cool:`        | `#cool`        |
| `game:`               | `#game`        |

## 🔧 Configuration

### Adding New Hashtags

Edit `services/message_processor.py`:

```python
HASHTAG_RULES = {
    "useful:": "#useful",
    "new phrase:": "#new_hashtag",  # Add here
    # ...
}
```

### Changing Selenium Timeouts

To modify timeout settings, edit the `selenium_service.py` file in the `services/` folder:

- **Page load timeout**: Change the value in `set_page_load_timeout()` (default: 15 seconds)
- **Element search timeout**: Change the value in `implicitly_wait()` (default: 5 seconds)  
- **Redirect attempts**: Change the range value in the redirect loop (default: 5 attempts)

These settings control how long Selenium waits for pages to load and redirects to complete.

## 📋 Requirements

- Python 3.8+
- Chrome/Chromium browser
- ChromeDriver
- Telegram Bot Token
- Telegram Channel

## 📦 Dependencies

```
python-telegram-bot>=20.0
selenium>=4.0
python-dotenv>=0.19
requests>=2.25
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License.

## ⚠️ Security

- **Never commit .env file**
- Use bot only with trusted users
- Regularly update dependencies
- Don't publish tokens and IDs publicly

## 🐛 Troubleshooting

### Selenium Not Working

1. Check ChromeDriver installation
2. Update Chrome browser
3. Check chromedriver permissions

### Bot Not Responding

1. Check token in .env
2. Ensure bot is added to channel as admin
3. Check logs for errors

### Redirects Not Working

1. Test `/test_selenium` command
2. Ensure ChromeDriver availability
3. Check network connection

## 📞 Support

If you have questions or issues:

1. Check [Issues](https://github.com/your-username/telegram-link-processor-bot/issues)
2. Create new Issue with problem description
3. Include logs and system information