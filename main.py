import os
import logging
import sys
from flask import Flask
import threading
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

# =============================================================================
# COMPLETE 15-DAY TRAINING DATA
# =============================================================================

TRAINING_DATA = {
    1: {
        "title_ar": "اليوم الأول: الأساس المتين - الوجود الصوتي والاستماع النشط",
        "title_en": "Day 1: Solid Foundation - Vocal Presence and Active Listening",
        "materials": [
            {
                "type": "text",
                "title_ar": "أنت صانع أجواء",
                "title_en": "You Create the Atmosphere",
                "content_ar": """في العالم الصوتي، أنت المسؤول الوحيد عن صناعة المشاعر وتوجيه الطاقة
صوتك ليس مجرد وسيلة نقل معلومات، بل هو أداة صناعة المشاعر

مثال: عندما تتحدث عن موضوع مفرح، اجعل نبرة صوتك مرتفعة ومليئة بالحيوية
مثال: عندما تقدم موضوعاً جاداً، اخفض نبرة صوتك وأعطِ كل كلمة وزنها

الاستماع النشط ليس سماعاً:
السماع: عملية سلبية تتم دون تركيز
الاستماع: عملية نشطة تتطلب التركيز والفهم والاستجابة الذكية

كيف تستمتع بنشاط؟
لا تنتظر دورك للكلام: ركز على ما يقال الآن وليس على ردك القادم
الرد على المشاعر: انتبه لنبرة صوت المتحدث
الأسئلة التوضيحية: هل تقصد أن...؟ ماذا حدث بعد ذلك؟

صناعة هويتك الصوتية:
الثقة: نابعة من إيمانك بقيمتك وما تقدمه
الطاقة: اجعل طاقتك إيجابية ومعدية حتى في الأيام العادية
الأصالة: كن صادقاً في ردودك وتفاعلك، لا تتصنع شخصية غيرك""",
                "content_en": """In the audio world, you are solely responsible for creating emotions and directing energy
Your voice is not just a means of transmitting information, but a tool for creating emotions

Example: When talking about a happy topic, make your tone high and full of vitality
Example: When presenting a serious topic, lower your tone and give each word its weight

Active listening is not just hearing:
Hearing: A passive process without focus
Listening: An active process requiring concentration, understanding, and intelligent response

How to listen actively?
Don't wait for your turn to speak: Focus on what is being said now, not your next response
Respond to emotions: Pay attention to the speaker's tone
Clarifying questions: Do you mean that...? What happened next?

Building your vocal identity:
Confidence: Stemming from your belief in your value and what you offer
Energy: Make your energy positive and contagious even on ordinary days
Authenticity: Be honest in your responses and interactions, don't fake another personality"""
            },
            {
                "type": "text", 
                "title_ar": "التمارين العملية",
                "title_en": "Practical Exercises",
                "content_ar": """التمارين العملية الفردية:
تمرين التحليل (15 دقيقة): استمع لمضيف مشهور وحلل 3 مواقف استخدم فيها الاستماع النشط
تمرين التسجيل والتحليل الذاتي (30 دقيقة): سجل صوتك وأنت تتحدث عن كتاب أو فيلم، ثم حلل سرعتك، وضوحك، ونبرة صوتك
تمرين الارتجال (15 دقيقة): تحدث عن كلمة عشوائية لمدة 60 ثانية دون توقف

الأنشطة الجماعية:
لعبة همسة السلسلة (15 دقيقة): لتدريب دقة الاستماع ونقل المعلومة
المقابلة النشطة (20 دقيقة): يتدرب المتدربون على الاستماع بهدف الفهم وليس الرد

المهمة اليومية: استمع إلى مضيف آخر وحلل طريقته في التعامل مع ضيوفه وجمهوره""",
                "content_en": """Individual Practical Exercises:
Analysis Exercise (15 minutes): Listen to a famous host and analyze 3 situations where they used active listening
Recording and Self-Analysis Exercise (30 minutes): Record your voice while talking about a book or movie, then analyze your speed, clarity, and tone
Improvisation Exercise (15 minutes): Talk about a random word for 60 seconds without stopping

Group Activities:
Chain Whisper Game (15 minutes): To train listening accuracy and information transfer
Active Interview (20 minutes): Trainees practice listening for understanding rather than responding

Daily Task: Listen to another host and analyze their way of dealing with guests and audience"""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الأول: الوجود الصوتي والاستماع النشط",
            "title_en": "Day 1 Quiz: Vocal Presence and Active Listening",
            "questions": [
                {
                    "question_ar": "ما الفرق الرئيسي بين السماع والاستماع النشط؟",
                    "question_en": "What is the main difference between hearing and active listening?",
                    "options_ar": ["السماع نشط والاستماع سلبي", "السماع سلبي والاستماع نشط", "لا فرق بينهما", "السماع يحتاج تركيز والاستماع لا يحتاج"],
                    "options_en": ["Hearing is active and listening is passive", "Hearing is passive and listening is active", "No difference between them", "Hearing requires concentration and listening doesn't"],
                    "correct": 1,
                    "explanation_ar": "السماع عملية سلبية تتم دون تركيز بينما الاستماع النشط يتطلب التركيز والفهم والاستجابة الذكية",
                    "explanation_en": "Hearing is a passive process without focus, while active listening requires concentration, understanding, and intelligent response"
                }
            ]
        }
    }
}

# Add remaining days structure
for day in range(2, 16):
    TRAINING_DATA[day] = {
        "title_ar": f"اليوم {day}: محتوى تدريبي متقدم",
        "title_en": f"Day {day}: Advanced Training Content", 
        "materials": [
            {
                "type": "text",
                "title_ar": f"محتوى اليوم {day}",
                "title_en": f"Day {day} Content",
                "content_ar": f"هذا هو المحتوى التدريبي لليوم {day}. سيتم تحديثه قريباً بمزيد من التفاصيل.",
                "content_en": f"This is the training content for Day {day}. It will be updated soon with more details."
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
user_language = {}

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Audio Host Training Bot</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .container { max-width: 800px; margin: 0 auto; }
                .status { color: green; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎓 Audio Host Training Bot</h1>
                <p class="status">✅ Bot is running successfully!</p>
                <p>Visit your Telegram bot to start the 15-day training program.</p>
                <p><strong>Features:</strong></p>
                <ul style="text-align: left; display: inline-block;">
                    <li>15 days of comprehensive training</li>
                    <li>Arabic & English content</li>
                    <li>Interactive quizzes</li>
                    <li>Progress tracking</li>
                </ul>
            </div>
        </body>
    </html>
    """

@app.route('/health')
def health():
    return {"status": "healthy", "service": "audio_training_bot"}

def run_simple_bot(token):
    """Run a simple Telegram bot using requests"""
    import requests
    import time
    
    BASE_URL = f"https://api.telegram.org/bot{token}"
    
    def get_updates(offset=None):
        url = f"{BASE_URL}/getUpdates"
        params = {"timeout": 60, "offset": offset}
        try:
            response = requests.get(url, params=params, timeout=70)
            return response.json()
        except Exception as e:
            logging.error(f"Error getting updates: {e}")
            return {"ok": False, "result": []}
    
    def send_message(chat_id, text, reply_markup=None):
        url = f"{BASE_URL}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            return response.json()
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            return {"ok": False}
    
    def create_keyboard():
        """Create inline keyboard markup"""
        return {
            "inline_keyboard": [
                [{"text": "📅 التدريب اليومي", "callback_data": "today"}],
                [{"text": "📚 جميع الأيام", "callback_data": "all_days"}],
                [{"text": "📊 تقدمي", "callback_data": "progress"}],
                [{"text": "❓ الاختبارات", "callback_data": "quizzes"}],
                [{"text": "🌐 English", "callback_data": "english"}]
            ]
        }
    
    def create_days_keyboard():
        """Create keyboard for all days"""
        keyboard = []
        for day in range(1, 16):
            keyboard.append([{"text": f"اليوم {day}", "callback_data": f"day_{day}"}])
        keyboard.append([{"text": "🏠 القائمة الرئيسية", "callback_data": "main_menu"}])
        return {"inline_keyboard": keyboard}
    
    def get_user_language(user_id):
        return user_language.get(user_id, 'ar')
    
    def get_text(user_id, arabic_text, english_text):
        return arabic_text if get_user_language(user_id) == 'ar' else english_text
    
    # Initialize last update ID
    last_update_id = None
    
    logging.info("🤖 Starting simple bot polling...")
    
    while True:
        try:
            updates = get_updates(last_update_id)
            
            if updates.get("ok"):
                for update in updates["result"]:
                    last_update_id = update["update_id"] + 1
                    
                    # Handle messages
                    if "message" in update and "text" in update["message"]:
                        chat_id = update["message"]["chat"]["id"]
                        text = update["message"]["text"]
                        user_id = update["message"]["from"]["id"]
                        
                        # Initialize user progress
                        if user_id not in user_progress:
                            user_progress[user_id] = {
                                "current_day": 1,
                                "completed_days": set(),
                                "quiz_scores": {},
                                "last_activity": datetime.now().isoformat()
                            }
                        
                        # Initialize language
                        if user_id not in user_language:
                            user_language[user_id] = 'ar'
                        
                        if text == "/start":
                            welcome_text = get_text(user_id,
                                f"""🎓 **مرحباً بك في البرنامج التدريبي الشامل!**

هذا البرنامج المكثف لمدة 15 يوماً سيرشدك نحو الاحتراف في عالم البث الصوتي.

**ماذا ستتعلم؟**
• 🎯 15 يوماً من التدريب المكثف
• 📚 مواد تدريبية شاملة  
• ❓ اختبارات تفاعلية
• 📊 متابعة التقدم الشخصي

اختر من القائمة أدناه لبدء رحلتك! 🚀""",
                                f"""🎓 **Welcome to Comprehensive Training Program!**

This intensive 15-day program will guide you toward professionalism in audio broadcasting.

**What you'll learn:**
• 🎯 15 days of intensive training
• 📚 Comprehensive training materials
• ❓ Interactive quizzes  
• 📊 Personal progress tracking

Choose from the menu below to start your journey! 🚀"""
                            )
                            send_message(chat_id, welcome_text, create_keyboard())
                        
                        elif text == "/menu":
                            menu_text = get_text(user_id,
                                "🏫 **القائمة الرئيسية**\n\nاختر مسار التعلم:",
                                "🏫 **Main Menu**\n\nChoose your learning path:"
                            )
                            send_message(chat_id, menu_text, create_keyboard())
                        
                        elif text == "/progress":
                            progress = user_progress.get(user_id, {})
                            current_day = progress.get("current_day", 1)
                            completed_days = len(progress.get("completed_days", set()))
                            
                            progress_text = get_text(user_id,
                                f"""📊 **تقدمك في التعلم**

**اليوم الحالي:** {current_day}/15
**الأيام المكتملة:** {completed_days}/15
**نسبة الإنجاز:** {round((completed_days/15)*100)}%

**ما التالي؟**
• واصل التعلم من حيث توقفت
• راجع المواد السابقة
• اختبر معرفتك""",
                                f"""📊 **Your Learning Progress**

**Current Day:** {current_day}/15
**Completed Days:** {completed_days}/15
**Completion Rate:** {round((completed_days/15)*100)}%

**What's Next?**
• Continue learning from where you left off
• Review previous materials  
• Test your knowledge"""
                            )
                            send_message(chat_id, progress_text)
                        
                        elif text == "/today":
                            progress = user_progress.get(user_id, {})
                            current_day = progress.get("current_day", 1)
                            day_data = TRAINING_DATA.get(current_day, {})
                            day_title = get_text(user_id, day_data.get("title_ar", f"اليوم {current_day}"), day_data.get("title_en", f"Day {current_day}"))
                            
                            today_text = get_text(user_id,
                                f"{day_title}\n\nاستخدم /menu للعودة إلى القائمة الرئيسية.",
                                f"{day_title}\n\nUse /menu to return to the main menu."
                            )
                            send_message(chat_id, today_text)
                        
                        else:
                            help_text = get_text(user_id,
                                "👋 استخدم /menu للوصول إلى القائمة الرئيسية والتعرف على جميع الميزات المتاحة!",
                                "👋 Use /menu to access the main menu and discover all available features!"
                            )
                            send_message(chat_id, help_text)
                    
                    # Handle callback queries
                    elif "callback_query" in update:
                        query = update["callback_query"]
                        chat_id = query["message"]["chat"]["id"]
                        data = query["data"]
                        user_id = query["from"]["id"]
                        
                        # Answer callback query
                        requests.post(f"{BASE_URL}/answerCallbackQuery", json={
                            "callback_query_id": query["id"]
                        })
                        
                        if data == "main_menu":
                            menu_text = get_text(user_id,
                                "🏫 **القائمة الرئيسية**\n\nاختر مسار التعلم:",
                                "🏫 **Main Menu**\n\nChoose your learning path:"
                            )
                            send_message(chat_id, menu_text, create_keyboard())
                        
                        elif data == "today":
                            progress = user_progress.get(user_id, {})
                            current_day = progress.get("current_day", 1)
                            day_data = TRAINING_DATA.get(current_day, {})
                            day_title = get_text(user_id, day_data.get("title_ar", f"اليوم {current_day}"), day_data.get("title_en", f"Day {current_day}"))
                            
                            today_text = get_text(user_id,
                                f"{day_title}\n\nاستخدم /menu للعودة إلى القائمة الرئيسية.",
                                f"{day_title}\n\nUse /menu to return to the main menu."
                            )
                            send_message(chat_id, today_text)
                        
                        elif data == "all_days":
                            days_text = get_text(user_id,
                                "📚 **جميع أيام التدريب**\n\nاختر يوماً لعرض محتواه:",
                                "📚 **All Training Days**\n\nSelect a day to view its content:"
                            )
                            send_message(chat_id, days_text, create_days_keyboard())
                        
                        elif data == "progress":
                            progress = user_progress.get(user_id, {})
                            current_day = progress.get("current_day", 1)
                            completed_days = len(progress.get("completed_days", set()))
                            
                            progress_text = get_text(user_id,
                                f"📊 **تقدمك**\n\nاليوم: {current_day}/15\nمكتمل: {completed_days}/15\nالنسبة: {round((completed_days/15)*100)}%",
                                f"📊 **Progress**\n\nDay: {current_day}/15\nCompleted: {completed_days}/15\nRate: {round((completed_days/15)*100)}%"
                            )
                            send_message(chat_id, progress_text)
                        
                        elif data == "quizzes":
                            quizzes_text = get_text(user_id,
                                "❓ **الاختبارات**\n\nسيتم إضافة الاختبارات التفاعلية قريباً!",
                                "❓ **Quizzes**\n\nInteractive quizzes will be added soon!"
                            )
                            send_message(chat_id, quizzes_text)
                        
                        elif data == "english":
                            user_language[user_id] = 'en'
                            send_message(chat_id, "✅ Language changed to English!", create_keyboard())
                        
                        elif data.startswith("day_"):
                            day_num = int(data.split("_")[1])
                            day_data = TRAINING_DATA.get(day_num, {})
                            day_title = get_text(user_id, day_data.get("title_ar", f"اليوم {day_num}"), day_data.get("title_en", f"Day {day_num}"))
                            
                            day_text = get_text(user_id,
                                f"{day_title}\n\nاستخدم /menu للعودة إلى القائمة الرئيسية.",
                                f"{day_title}\n\nUse /menu to return to the main menu."
                            )
                            send_message(chat_id, day_text)
            
            time.sleep(1)
            
        except Exception as e:
            logging.error(f"Bot error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    # Get token
    token = os.environ.get('TELEGRAM_TOKEN')
    
    if token:
        logging.info(f"✅ TELEGRAM_TOKEN found! Starting simple bot...")
        
        # Start bot in a separate thread
        bot_thread = threading.Thread(target=run_simple_bot, args=(token,), daemon=True)
        bot_thread.start()
        logging.info("✅ Simple bot thread started!")
    else:
        logging.error("❌ TELEGRAM_TOKEN not found!")
    
    # Start Flask
    logging.info(f"🌐 Starting Flask on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
