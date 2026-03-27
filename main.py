import os
from dotenv import load_dotenv
from src.bots.telegram import run_bot

def main():
    """Main entry point for the Resume Optimizer Bot."""
    print("✨ Resume Optimizer Bot ✨")
    print("--------------------------")
    
    # Check for .env file
    if not os.path.exists(".env"):
        print("⚠️ .env file not found! Generating a template for you...")
        with open(".env", "w") as f:
            f.write("TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here\n")
            f.write("GEMINI_API_KEY=your_gemini_api_key_here\n")
        print("✅ .env template created. Please fill in your API keys and restart.")
        return

    # Run the bot
    try:
        run_bot()
    except Exception as e:
        print(f"❌ Critical Error: {str(e)}")

if __name__ == "__main__":
    main()
