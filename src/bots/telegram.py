import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from src.analyzer.core import ResumeAnalyzer
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Logger
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# States
WAITING_FOR_RESUME = 1
WAITING_FOR_JD = 2

# Global analyzer instance
analyzer = ResumeAnalyzer()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Greets the user and starts the conversation."""
    await update.message.reply_text(
        "👋 Welcome to the Resume Optimizer Bot!\n\n"
        "I'll help you rate and optimize your resume against a Job Description (JD).\n\n"
        "To begin, please upload your resume in **PDF** format."
    )
    return WAITING_FOR_RESUME

async def handle_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the resume PDF upload."""
    document = update.message.document
    if document and document.mime_type == 'application/pdf':
        file = await context.bot.get_file(document.file_id)
        # Create a temp file path
        if not os.path.exists("temp"):
            os.mkdir("temp")
        file_path = f"temp/{document.file_name}"
        await file.download_to_drive(file_path)
        
        # Extract text
        resume_text = analyzer.extract_text_from_pdf(file_path)
        context.user_data['resume_text'] = resume_text
        # Clean up
        os.remove(file_path)

        await update.message.reply_text(
            "✅ Resume received! Now, please paste the Job Description (JD) text."
        )
        return WAITING_FOR_JD
    else:
        await update.message.reply_text("❌ Please upload a valid PDF resume.")
        return WAITING_FOR_RESUME

async def handle_jd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the JD text and triggers analysis."""
    jd_text = update.message.text
    resume_text = context.user_data.get('resume_text', "")
    
    # 1. Run analysis (Rating, Suggestions, etc)
    analysis_result = await analyzer.analyze(resume_text, jd_text)
    await update.message.reply_text(f"🚀 **Executive Analysis Live:**\n\n{analysis_result}")

    # 4. Create and Send DOCX
    await update.message.reply_text("✨ Polishing your Premium Optimized Resume... hang tight! 🛠️")
    updated_resume_text = await analyzer.generate_updated_resume(resume_text, jd_text)
    
    docx_file = analyzer.generate_docx(updated_resume_text)
    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=docx_file,
        filename="Premium_Optimized_Resume.docx",
        caption="🎉 Your professional editable CV is ready!"
    )

    # 5. Create and Send PDF
    pdf_file = analyzer.generate_pdf(updated_resume_text)
    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=pdf_file,
        filename="Premium_Optimized_Resume.pdf",
        caption="📑 Your ready-to-send PDF CV!"
    )

    await update.message.reply_text(
        "🔥 **BAM! That's how you crush it.** Your resume is now optimized for the job.\n\n"
        "Need to analyze another version? Just type /start to begin again! 🌟"
    )
    
    # End conversation
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels the conversation."""
    await update.message.reply_text("🚫 Session cancelled. Type /start to begin again.")
    return ConversationHandler.END

def run_bot():
    """Starts the Telegram bot."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ Error: TELEGRAM_BOT_TOKEN is missing from your .env file!")
        return

    application = ApplicationBuilder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WAITING_FOR_RESUME: [MessageHandler(filters.Document.ALL, handle_resume)],
            WAITING_FOR_JD: [MessageHandler(filters.TEXT & (~filters.COMMAND), handle_jd)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    print("🚀 Bot is running...")
    application.run_polling()
