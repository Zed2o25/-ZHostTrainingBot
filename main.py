import os
import logging
import json
import random
from datetime import datetime
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Flask app for Render
app = Flask(__name__)

# =============================================================================
# COMPLETE 15-DAY TRAINING DATA (abbreviated for this example)
# =============================================================================

TRAINING_DATA = {
    1: {
        "title_ar": "اليوم الأول: الأساس المتين",
        "title_en": "Day 1: Solid Foundation",
        "materials": [
            {
                "type": "text",
                "title_ar": "أنت صانع أجواء",
                "title_en": "You Create Atmosphere",
                "content_ar": "في العالم الصوتي، أنت المسؤول عن صناعة المشاعر وتوجيه الطاقة.",
                "content_en": "In the audio world, you are responsible for creating emotions and directing energy."
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الأول",
            "title_en": "Day 1 Quiz",
            "questions": [
                {
                    "question_ar": "ما الفرق بين السماع والاستماع النشط؟",
                    "question_en": "What is the difference between hearing and active listening?",
                    "options_ar": ["السماع سلبي والاستماع نشط", "لا فرق بينهما", "السماع يحتاج تركيز", "الاستماع سلبي"],
                    "options_en": ["Hearing is passive and listening is active", "No difference", "Hearing needs focus", "Listening is passive"],
                    "correct": 0,
                    "explanation_ar": "السماع عملية سلبية بينما الاستماع النشط يتطلب التركيز والفهم",
                    "explanation_en": "Hearing is a passive process while active listening requires concentration and understanding"
                }
            ]
        }
    }
}

# Add remaining days structure
for day in range(2, 16):
    TRAINING_DATA[day] = {
        "title_ar": f"اليوم {day}: محتوى تدريبي",
        "title_en": f"Day {day}: Training Content",
        "materials": [
            {
                "type": "text",
                "title_ar": f"محتوى اليوم {day}",
                "title_en": f"Day {day} Content",
                "content_ar": f"هذا هو المحتوى التدريبي لليوم {day}. سيتم تحديثه قريباً.",
                "content_en": f"This is training content for Day {day}. It will be updated soon."
            }
        ],
        "quiz": {
            "title_ar": f"اختبار اليوم {day}",
            "title_en": f"Day {day} Quiz",
            "questions": [
                {
                    "question_ar": "سؤال اختبار اليوم",
                    "question_en": "Test question for today",
                    "options_ar": ["خيار أ", "خيار ب", "خيار ج", "خيار د"],
                    "options_en": ["Option A", "Option B", "Option C", "Option D"],
                    "correct": 0,
                    "explanation_ar": "شرح الإجابة الصحيحة",
                    "explanation_en": "Explanation of correct answer"
                }
            ]
        }
    }

# =============================================================================
# USER PROGRESS TRACKING
# =============================================================================

user_progress = {}
user_quiz_responses = {}
user_language = {}

# =============================================================================
# TELEGRAM BOT CLASS
# =============================================================================

class TrainingBot:
    def __init__(self, token):
        self.token = token
        self.application = Application.builder().token(token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("menu", self.show_main_menu))
        self.application.add_handler(CommandHandler("progress", self.show_progress))
        self.application.add_handler(CommandHandler("today", self.show_todays_training))
        self.application.add_handler(CommandHandler("language", self.change_language))
        self.application.add_handler(CallbackQueryHandler(self.handle_button_click))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    def get_user_language(self, user_id):
        return user_language.get(user_id, 'ar')
    
    def get_text(self, user_id, arabic_text, english_text):
        return arabic_text if self.get_user_language(user_id) == 'ar' else english_text
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_id = user.id
        
        if user_id not in user_progress:
            user_progress[user_id] = {
                "current_day": 1,
                "completed_days": set(),
                "quiz_scores": {},
                "last_activity": datetime.now().isoformat()
            }
        
        if user_id not in user_language:
            user_language[user_id] = 'ar'
        
        welcome_text = self.get_text(user_id,
            f"🎓 **مرحباً بك في البرنامج التدريبي، {user.first_name}!**\n\nاستخدم /menu للقائمة الرئيسية.",
            f"🎓 **Welcome to Training Program, {user.first_name}!**\n\nUse /menu for main menu."
        )
        
        keyboard = [
            [InlineKeyboardButton("🚀 ابدأ التعلم", callback_data="today_training")],
            [InlineKeyboardButton("📚 القائمة الرئيسية", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        keyboard = [
            [InlineKeyboardButton("📅 التدريب اليومي", callback_data="today_training")],
            [InlineKeyboardButton("📚 جميع الأيام", callback_data="all_days")],
            [InlineKeyboardButton("📊 تقدمي", callback_data="progress")],
            [InlineKeyboardButton("❓ الاختبارات", callback_data="quizzes_menu")],
            [InlineKeyboardButton("🌐 تغيير اللغة", callback_data="lang_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🏫 **القائمة الرئيسية**", reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_progress(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        progress = user_progress.get(user_id, {})
        current_day = progress.get("current_day", 1)
        completed_days = len(progress.get("completed_days", set()))
        
        progress_text = self.get_text(user_id,
            f"📊 **تقدمك**\nاليوم: {current_day}/15\nمكتمل: {completed_days}/15",
            f"📊 **Progress**\nDay: {current_day}/15\nCompleted: {completed_days}/15"
        )
        
        keyboard = [
            [InlineKeyboardButton("📚 متابعة", callback_data="today_training")],
            [InlineKeyboardButton("🏠 رئيسية", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(progress_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_todays_training(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        progress = user_progress.get(user_id, {})
        current_day = progress.get("current_day", 1)
        await self.show_day_overview(update, current_day)
    
    async def change_language(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar")],
            [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("اختر اللغة / Choose language:", reply_markup=reply_markup)
    
    async def handle_button_click(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        data = query.data
        
        if data == "main_menu":
            await self.show_main_menu_callback(query)
        elif data == "today_training":
            await self.show_todays_training_callback(query)
        elif data == "all_days":
            await self.show_all_days(query)
        elif data == "progress":
            await self.show_progress_callback(query)
        elif data == "quizzes_menu":
            await self.show_quizzes_menu(query)
        elif data.startswith("day_"):
            day_num = int(data.split("_")[1])
            await self.show_day_overview_callback(query, day_num)
        elif data.startswith("lang_"):
            user_id = query.from_user.id
            lang = data.split("_")[1]
            user_language[user_id] = lang
            await query.edit_message_text("✅ تم تغيير اللغة / Language changed")
            await self.show_main_menu_callback(query)
        elif data == "lang_menu":
            await self.change_language_callback(query)
    
    async def show_main_menu_callback(self, query):
        keyboard = [
            [InlineKeyboardButton("📅 التدريب اليومي", callback_data="today_training")],
            [InlineKeyboardButton("📚 جميع الأيام", callback_data="all_days")],
            [InlineKeyboardButton("📊 تقدمي", callback_data="progress")],
            [InlineKeyboardButton("❓ الاختبارات", callback_data="quizzes_menu")],
            [InlineKeyboardButton("🌐 تغيير اللغة", callback_data="lang_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🏫 **القائمة الرئيسية**", reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_todays_training_callback(self, query):
        user_id = query.from_user.id
        progress = user_progress.get(user_id, {})
        current_day = progress.get("current_day", 1)
        await self.show_day_overview_callback(query, current_day)
    
    async def show_all_days(self, query):
        keyboard = []
        for day in range(1, 16):
            keyboard.append([InlineKeyboardButton(f"اليوم {day}", callback_data=f"day_{day}")])
        keyboard.append([InlineKeyboardButton("🏠 رئيسية", callback_data="main_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📚 **جميع أيام التدريب**", reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_quizzes_menu(self, query):
        keyboard = []
        for day in range(1, 16):
            keyboard.append([InlineKeyboardButton(f"اختبار اليوم {day}", callback_data=f"quiz_{day}")])
        keyboard.append([InlineKeyboardButton("🏠 رئيسية", callback_data="main_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("❓ **الاختبارات**", reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_day_overview(self, update, day_num):
        user_id = update.effective_user.id if hasattr(update, 'effective_user') else update.from_user.id
        day_data = TRAINING_DATA.get(day_num, {})
        day_title = self.get_text(user_id, day_data.get("title_ar", f"اليوم {day_num}"), day_data.get("title_en", f"Day {day_num}"))
        
        overview_text = f"{day_title}\n\nالمواد المتاحة:\n"
        
        materials = day_data.get("materials", [])
        for i, material in enumerate(materials, 1):
            material_title = self.get_text(user_id, material.get("title_ar", ""), material.get("title_en", ""))
            overview_text += f"• {material_title}\n"
        
        keyboard = []
        for i, material in enumerate(materials):
            material_title = self.get_text(user_id, material.get("title_ar", ""), material.get("title_en", ""))
            keyboard.append([InlineKeyboardButton(f"📖 {material_title}", callback_data=f"material_{day_num}_{i}")])
        
        if day_data.get("quiz"):
            keyboard.append([InlineKeyboardButton("❓ اختبار", callback_data=f"quiz_{day_num}")])
        
        nav_buttons = []
        if day_num > 1:
            nav_buttons.append(InlineKeyboardButton("⬅️ السابق", callback_data=f"day_{day_num-1}"))
        if day_num < 15:
            nav_buttons.append(InlineKeyboardButton("التالي ➡️", callback_data=f"day_{day_num+1}"))
        
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        keyboard.append([InlineKeyboardButton("🏠 رئيسية", callback_data="main_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if isinstance(update, Update):
            await update.message.reply_text(overview_text, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await update.edit_message_text(overview_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_day_overview_callback(self, query, day_num):
        await self.show_day_overview(query, day_num)
    
    async def show_material(self, query, day_num, material_index):
        user_id = query.from_user.id
        day_data = TRAINING_DATA.get(day_num, {})
        materials = day_data.get("materials", [])
        
        if material_index >= len(materials):
            await query.answer("لا توجد مواد أخرى")
            return
        
        material = materials[material_index]
        content = self.get_text(user_id, material.get("content_ar", ""), material.get("content_en", ""))
        
        keyboard = []
        if material_index > 0:
            keyboard.append(InlineKeyboardButton("⬅️ السابق", callback_data=f"material_{day_num}_{material_index-1}"))
        if material_index < len(materials) - 1:
            keyboard.append(InlineKeyboardButton("التالي ➡️", callback_data=f"material_{day_num}_{material_index+1}"))
        
        if keyboard:
            keyboard = [keyboard]
        
        keyboard.append([InlineKeyboardButton("📋 نظرة عامة", callback_data=f"day_{day_num}")])
        keyboard.append([InlineKeyboardButton("🏠 رئيسية", callback_data="main_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(content, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def start_quiz(self, query, day_num):
        user_id = query.from_user.id
        user_quiz_responses[user_id] = {
            "day": day_num,
            "current_question": 0,
            "answers": [],
            "score": 0
        }
        await query.edit_message_text(f"بدء اختبار اليوم {day_num}...")
    
    async def change_language_callback(self, query):
        keyboard = [
            [InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar")],
            [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("اختر اللغة / Choose language:", reply_markup=reply_markup)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("استخدم /menu للقائمة الرئيسية")

# =============================================================================
# FLASK ROUTES & BOT INITIALIZATION
# =============================================================================

@app.route('/')
def home():
    return "Training Bot is running successfully! 🚀"

@app.route('/health')
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

def run_bot(token):
    """Run the Telegram bot with the provided token"""
    try:
        logging.info(f"🤖 Starting Telegram Bot with token: {token[:10]}...")
        bot = TrainingBot(token)
        logging.info("✅ Bot initialized successfully")
        bot.application.run_polling()
    except Exception as e:
        logging.error(f"❌ Failed to start bot: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    # Get token from environment variable
    token = os.environ.get('TELEGRAM_TOKEN')
    
    if not token:
        logging.error("❌ TELEGRAM_TOKEN not found in environment variables!")
        logging.info("💡 Please check Render environment variables:")
        logging.info("💡 1. Go to your Render dashboard")
        logging.info("💡 2. Click on your service 'zhosttrainingbot'")
        logging.info("💡 3. Go to 'Environment' tab")
        logging.info("💡 4. Make sure TELEGRAM_TOKEN is set correctly")
        logging.info("💡 5. Redeploy after making changes")
    else:
        logging.info(f"✅ TELEGRAM_TOKEN found: {token[:10]}...")
        
        # Start bot in background thread
        import threading
        logging.info("🚀 Starting bot thread...")
        bot_thread = threading.Thread(target=run_bot, args=(token,))
        bot_thread.daemon = True
        bot_thread.start()
        logging.info("✅ Bot thread started successfully")
    
    # Start Flask app (this will always run)
    logging.info("🌐 Starting Flask server...")
    app.run(host='0.0.0.0', port=port)
