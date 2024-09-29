# Stackup Helper Bot

**Stackup Helper Bot** is a multi-functional Discord bot designed to help users answer general questions, and provide administrative tools for server management. It integrates Google Generative AI (Gemini API) to generate answers from text files or generative AI, and includes conversation context storage for more natural and context-aware responses. Additionally, the bot offers Zendesk Reader integration, allowing it to retrieve and respond to queries based on content from Zendesk documents.

---

## Features

### 1. General Question Answering
- **Command**: `!ask [question]`
  - Users can ask questions, and the bot first tries to find the answer in a predefined text file (`faq_data.txt`). If no answer is found, the bot generates a response using the **Google Gemini API**.
  - Conversation context is stored to make future responses more context-aware.

### 2. Zendesk Reader Integration
- The bot can fetch data from Zendesk articles and documentation, enhancing its knowledge base to provide more specific answers when needed.

### 3. Admin Commands
- **Command**: `!kick [user]`
  - Kicks a specified user from the server.
  
- **Command**: `!mute [user] [hours]`
  - Mutes a user for a specified number of hours, temporarily preventing them from sending messages.

- **Command**: `!deletechatlog`
  - Deletes the chat log that stores conversation history.

### 4. Conversation Context Storage
- The bot logs all user queries and responses in a `chat_log.txt` file. This allows it to provide context-based responses and improve future interactions with the user.

### 5. Help Command
- **Command**: `!help`
  - Provides a list of all available commands, as well as a brief description of the bot's functionalities.

---

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/stackup-helper-bot.git
cd stackup-helper-bot
```

### 2. Install Dependencies
**Use the `requirements.txt` file to install all the necessary dependencies:**
```bash
pip install -r requirements.txt
```
**Your `requirements.txt` should include dependencies such as:**
```bash
discord.py
python-dotenv
google-generativeai
zendesk
```

### 3. Configure Environment Variables
**Create a `.env` file to store sensitive environment variables such as your Discord Bot Token and Google Gemini API key.**
**In your project directory, create a file called .env.Add the following lines to the .env file:**
```bash
DISCORD_TOKEN=your-discord-bot-token
GEMINI_API_KEY=your-google-gemini-api-key
```

### 4. Running the Bot:
**Once everything is set up, you can start the bot with the following command:**
```bash
python main.py
```

---
## Commands List

### General Commands
- **`!ask [question]`**: Ask a question and get an answer from the bot. It first checks a predefined text file for the answer, and if not found, it generates an answer using the Gemini API.
  
- **`!hello`**: Sends a greeting message.

- **`!serverinfo`**: Displays the current server name and the number of members.

- **`!help`**: Lists all commands and provides information about each.

### Admin Commands
- **`!kick [user]`**: Kicks a specified user from the server.

- **`!mute [user] [hours]`**: Temporarily mutes a user for the given number of hours.

- **`!deletechatlog`**: Deletes the stored chat log that records the conversation history.


## Logging Feature
The bot logs all user queries, responses, and response times in a `chat_log.txt` file. Admins can delete this chat log using the `!deletechatlog` command to clear the stored conversation history.

## Google Gemini API Configuration
### Steps to Configure:
1. Visit the Google Cloud Console and create a new project.
2. Enable the Google Generative AI API.
3. Obtain your API key and add it to the `.env` file as `GEMINI_API_KEY`.

The bot uses this API to generate answers when no answer is found in the predefined text file.

## How to Install Dependencies
To install all the dependencies required for the bot, use the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Contributing
Feel free to fork the repository and contribute to the project by adding features or fixing bugs. Submit a pull request once your changes are ready.
