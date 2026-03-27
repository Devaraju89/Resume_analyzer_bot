# Resume AI Optimizer Bot 🤖

A powerful AI-driven tool that compares your resume to a job description (JD), giving you a rating out of 10 and optimization suggestions to improve your chances.

## 🚀 Features
- **JD Matching**: Paste your JD and upload your resume (PDF).
- **AI Rating**: Get a score out of 10 based on how well you fit the role.
- **Optimization Tips**: Get clear, actionable suggestions to improve your resume.
- **Resume Templates**: Suggestions for **Professional**, **Technical**, or **Creative** templates.
- **Telegram Integration**: Easy-to-use bot interface.

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.9+
- A Google Gemini API Key: [Get it here](https://aistudio.google.com/app/apikey)
- A Telegram Bot Token: [Create one via @BotFather](https://t.me/BotFather)

### 2. Installation
1. Clone or download this project.
2. Open a terminal in the project directory.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuration
1. Create a `.env` file in the root directory (or run `python main.py` once to generate a template).
2. Fill in your keys:
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### 4. Running the Bot
```bash
python main.py
```

## 📄 Templates
Check the `src/templates/` folder for sample markdown resumes:
- [Professional](src/templates/professional.md)
- [Technical](src/templates/technical.md)
- [Creative](src/templates/creative.md)

## 🔮 Future Roadmap (Discord/WhatsApp Support)
- **Discord**: Can be implemented using `discord.py`.
- **WhatsApp**: Requires the Twilio WhatsApp API or Similar.
- **Multi-Resume Support**: Compare multiple versions at once.
