import os
import logging
import sys
from flask import Flask

# Configure logging to show everything
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Debug Page - Check Render logs for environment variables"

@app.route('/debug')
def debug():
    # Get ALL environment variables (be careful with this in production)
    env_vars = {k: v for k, v in os.environ.items()}
    
    # Check specifically for TELEGRAM_TOKEN
    token = os.environ.get('TELEGRAM_TOKEN')
    token_exists = bool(token)
    token_preview = token[:10] + "..." if token else "NOT FOUND"
    
    debug_info = {
        "all_environment_variables": list(env_vars.keys()),
        "TELEGRAM_TOKEN_exists": token_exists,
        "TELEGRAM_TOKEN_preview": token_preview,
        "TELEGRAM_TOKEN_full_length": len(token) if token else 0,
        "python_version": sys.version,
        "current_working_directory": os.getcwd(),
        "files_in_directory": os.listdir('.')
    }
    
    return debug_info

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    # Debug: Print ALL environment variables to logs
    logging.debug("=== ENVIRONMENT VARIABLES DEBUG ===")
    for key, value in os.environ.items():
        if 'TOKEN' in key or 'KEY' in key or 'SECRET' in key:
            # Hide sensitive values but show they exist
            logging.debug(f"{key}: {'*' * 10} (hidden for security)")
        else:
            logging.debug(f"{key}: {value}")
    
    # Specific check for TELEGRAM_TOKEN
    token = os.environ.get('TELEGRAM_TOKEN')
    if token:
        logging.info(f"✅ TELEGRAM_TOKEN FOUND! Length: {len(token)}, Preview: {token[:10]}...")
        logging.info("🚀 Starting bot...")
        
        # Import and start the bot here
        try:
            from telegram.ext import Application
            bot_app = Application.builder().token(token).build()
            
            # Add a simple start command
            from telegram import Update
            from telegram.ext import CommandHandler, ContextTypes
            
            async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
                await update.message.reply_text("🤖 Bot is working! Debug successful!")
            
            bot_app.add_handler(CommandHandler("start", start))
            
            # Start polling in a way that works with Render
            import threading
            def run_bot():
                bot_app.run_polling()
            
            bot_thread = threading.Thread(target=run_bot)
            bot_thread.daemon = True
            bot_thread.start()
            logging.info("✅ Bot thread started successfully!")
            
        except Exception as e:
            logging.error(f"❌ Bot startup failed: {e}")
            
    else:
        logging.error("❌ TELEGRAM_TOKEN NOT FOUND in environment variables!")
        logging.error("Please check:")
        logging.error("1. Render dashboard → Environment tab")
        logging.error("2. Key: TELEGRAM_TOKEN")
        logging.error("3. Value: your_bot_token_from_botfather")
        logging.error("4. No quotes, no spaces")
    
    logging.info(f"🌐 Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port)
