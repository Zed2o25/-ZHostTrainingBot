import os
import logging
import sys
from flask import Flask
from telegram.ext import Application
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes, CallbackQueryHandler
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
                },
                {
                    "question_ar": "ما هي إحدى طرق الاستماع النشط؟",
                    "question_en": "What is one method of active listening?",
                    "options_ar": ["الانتظار للرد فقط", "التركيز على الرد القادم", "الرد على مشاعر المتحدث", "مقاطعة المتحدث"],
                    "options_en": ["Waiting only to respond", "Focusing on the next response", "Responding to the speaker's emotions", "Interrupting the speaker"],
                    "correct": 2,
                    "explanation_ar": "الرد على مشاعر المتحدث من خلال الانتباه لنبرة صوتهم يساعد في الاستماع النشط",
                    "explanation_en": "Responding to the speaker's emotions by paying attention to their tone helps in active listening"
                }
            ]
        }
    },
    2: {
        "title_ar": "اليوم الثاني: إتقان أدواتك - آلة الصوت والتعبير",
        "title_en": "Day 2: Mastering Your Tools - Voice Machine and Expression",
        "materials": [
            {
                "type": "text",
                "title_ar": "تمارين الإحماء الصوتي",
                "title_en": "Vocal Warm-up Exercises",
                "content_ar": """الروتين اليومي للإحماء الصوتي:
التنفس الحجابي: تنفس بعمق من الأنف بحيث يتمدد بطنك، وازفر ببطء من الفم
تمرين الشفاه: تحريك الشفاه معاً وتحريكهما في كل الاتجاهات
تمرين اللسان: لمس سقف الحلق وتحريك اللسان بشكل دائري

وضوح الكلام هو الاحترافية ذاتها:
ركز على مخارج الحروف، خاصة الحروف التي تحتاج لجهد
تخيل أنك ترمي الكلمات مثل السهام، يجب أن تكون واضحة ومستقيمة
مثال: عند نطق كلمة مستقبل، ركز على كل حرف وخاصة حرف القاف

موسيقى الكلام: كيف تصنع لحناً يجذب الأذن؟
النبرة: التغيير بين العالي والمنخفض يخلق تشويقاً
السرعة: سريعة للإثارة، بطيئة للتأكيد
الوقفات: استخدمها قبل وبعد المعلومات المهمة

لغة الجسد للصوت:
حتى لو لم يراك أحد، فإن ابتسامتك تسمع
تحدث ووجهك يعبر، ويديك تتحركان""",
                "content_en": """Daily Vocal Warm-up Routine:
Diaphragmatic breathing: Breathe deeply through your nose so your abdomen expands, and exhale slowly through your mouth
Lip exercise: Move lips together and move them in all directions
Tongue exercise: Touch the roof of the mouth and move the tongue in circles

Speech clarity is professionalism itself:
Focus on letter articulation, especially letters that require effort
Imagine throwing words like arrows - they should be clear and straight
Example: When pronouncing the word future, focus on each letter especially the Qaf sound

Music of speech: How to create a melody that attracts the ear?
Tone: Changing between high and low creates suspense
Speed: Fast for excitement, slow for emphasis
Pauses: Use them before and after important information

Body language for voice:
Even if no one sees you, your smile can be heard
Speak with expressive facial expressions and hand movements"""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الثاني: آلة الصوت والتعبير",
            "title_en": "Day 2 Quiz: Voice Machine and Expression",
            "questions": [
                {
                    "question_ar": "ما هو التنفس الحجابي؟",
                    "question_en": "What is diaphragmatic breathing?",
                    "options_ar": ["التنفس من الصدر فقط", "التنفس العميق من الأنف مع تمدد البطن", "التنفس السريع من الفم", "حبس النفس"],
                    "options_en": ["Breathing from chest only", "Deep breathing through nose with abdominal expansion", "Rapid breathing through mouth", "Holding breath"],
                    "correct": 1,
                    "explanation_ar": "التنفس الحجابي يتم من خلال التنفس بعمق من الأنف بحيث يتمدد البطن ثم الزفير ببطء من الفم",
                    "explanation_en": "Diaphragmatic breathing is done by breathing deeply through the nose so the abdomen expands, then exhaling slowly through the mouth"
                }
            ]
        }
    },
    3: {
        "title_ar": "اليوم الثالث: هيكل الفقرة الناجحة - البناء المحكم",
        "title_en": "Day 3: Successful Paragraph Structure - Precise Construction",
        "materials": [
            {
                "type": "text",
                "title_ar": "هيكل الفقرة الناجحة",
                "title_en": "Successful Paragraph Structure",
                "content_ar": """المقدمة (الخطاف):
لديك 10-15 ثانية فقط للإمساك بانتباه المستمع
أنواع الخطافات الفعالة:
السؤال الصادم: هل تعلم أن 90% من قراراتنا نتاج العقل الباطن؟
القصة المصغرة: كنت أجري أمس، وفجأة... وقعت!
الإحصائية المدهشة: يهدر طعام يكفي لإطعام مليار شخص سنوياً
الموقف الطريف: حاولت مرة أن أطهو بيضاً فاحترق المطبخ!

المحتوى (اللب):
ركز على نقطة رئيسية واحدة في كل فقرة
استخدم القصص لجعل المعلومة أكثر جاذبية
قدم أمثلة وتشبيهات لدعم فكرتك الرئيسية
مثال: بدلاً من وصف مكان ممل، احكِ قصة حدثت لك فيه

الخاتمة (الختام المؤثر):
أنواع الخواتم:
التلخيص: إذن، الفكرة الرئيسية هي...
دعوة للتفاعل: ما رأيكم؟ اكتبوا في الدردشة
السؤال المفتوح: لو كانت لديكم فرصة لسؤال أحد المشاهير، فمن تختارون؟
التلميح للمستقبل: في الحلقة القادمة، سنكشف عن سر...""",
                "content_en": """Introduction (The Hook):
You only have 10-15 seconds to grab the listener's attention
Types of effective hooks:
Shocking question: Did you know that 90% of our decisions are products of the subconscious mind?
Mini-story: I was running yesterday, and suddenly... I fell!
Amazing statistic: Enough food is wasted annually to feed one billion people!
Amusing situation: I once tried to cook eggs and the kitchen caught fire!

Content (The Core):
Focus on one main point in each paragraph
Use stories to make information more attractive
Provide examples and analogies to support your main idea
Example: Instead of describing a boring place, tell a story that happened to you there

Conclusion (The Impactful Closing):
Types of conclusions:
Summary: So, the main idea is...
Call to interaction: What do you think? Write in the chat
Open question: If you had the chance to ask a celebrity, who would you choose?
Hinting at the future: In the next episode, we will reveal the secret of..."""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الثالث: هيكل الفقرة",
            "title_en": "Day 3 Quiz: Paragraph Structure",
            "questions": [
                {
                    "question_ar": "كم ثانية لديك للإمساك بانتباه المستمع في المقدمة؟",
                    "question_en": "How many seconds do you have to grab the listener's attention in the introduction?",
                    "options_ar": ["5-10 ثوان", "10-15 ثانية", "20-30 ثانية", "60 ثانية"],
                    "options_en": ["5-10 seconds", "10-15 seconds", "20-30 seconds", "60 seconds"],
                    "correct": 1,
                    "explanation_ar": "لديك فقط 10-15 ثانية في المقدمة للإمساك بانتباه المستمع بما يعرف بالخطاف",
                    "explanation_en": "You only have 10-15 seconds in the introduction to grab the listener's attention with what is known as the hook"
                }
            ]
        }
    }
}

# Add remaining days structure
for day in range(4, 16):
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

# Global bot application
bot_app = None

@app.route('/')
def home():
    return "🎓 Audio Host Training Bot is running! Visit your Telegram bot to start learning."

@app.route('/health')
def health():
    return {"status": "healthy", "bot_running": bot_app is not None}

class TrainingBot:
    def __init__(self, token):
        self.application = Application.builder().token(token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("menu", self.show_main_menu))
        self.application.add_handler(CommandHandler("progress", self.show_progress))
        self.application.add_handler(CommandHandler("today", self.show_todays_training))
        self.application.add_handler(CommandHandler("language", self.change_language))
        
        # Callback query handler
        self.application.add_handler(CallbackQueryHandler(self.handle_button_click))
        
        # Message handler
        from telegram.ext import MessageHandler, filters
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    def get_user_language(self, user_id):
        return user_language.get(user_id, 'ar')
    
    def get_text(self, user_id, arabic_text, english_text):
        return arabic_text if self.get_user_language(user_id) == 'ar' else english_text
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_id = user.id
        
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
        
        welcome_text = self.get_text(user_id,
            f"""🎓 **مرحباً بك في البرنامج التدريبي الشامل، {user.first_name}!**

هذا البرنامج المكثف لمدة 15 يوماً سيرشدك نحو الاحتراف في عالم البث الصوتي.

**ماذا ستتعلم؟**
• 🎯 15 يوماً من التدريب المكثف
• 📚 مواد تدريبية شاملة  
• ❓ اختبارات تفاعلية
• 📊 متابعة التقدم الشخصي

استخدم /menu للوصول إلى القائمة الرئيسية وبدء رحلتك! 🚀""",
            f"""🎓 **Welcome to Comprehensive Training Program, {user.first_name}!**

This intensive 15-day program will guide you toward professionalism in audio broadcasting.

**What you'll learn:**
• 🎯 15 days of intensive training
• 📚 Comprehensive training materials
• ❓ Interactive quizzes  
• 📊 Personal progress tracking

Use /menu to access the main menu and start your journey! 🚀"""
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
            [InlineKeyboardButton("📚 جميع أيام التدريب", callback_data="all_days")],
            [InlineKeyboardButton("📊 تقدمي", callback_data="progress")],
            [InlineKeyboardButton("❓ الاختبارات", callback_data="quizzes_menu")],
            [InlineKeyboardButton("🌐 تغيير اللغة", callback_data="lang_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        menu_text = self.get_text(user_id,
            "🏫 **القائمة الرئيسية**\n\nاختر مسار التعلم:",
            "🏫 **Main Menu**\n\nChoose your learning path:"
        )
        
        await update.message.reply_text(menu_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_progress(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        progress = user_progress.get(user_id, {})
        current_day = progress.get("current_day", 1)
        completed_days = len(progress.get("completed_days", set()))
        
        progress_text = self.get_text(user_id,
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
        
        keyboard = [
            [InlineKeyboardButton("📚 متابعة التعلم", callback_data="today_training")],
            [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(progress_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_todays_training(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        progress = user_progress.get(user_id, {})
        current_day = progress.get("current_day", 1)
        await self.show_day_overview(update, current_day)
    
    async def change_language(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        keyboard = [
            [InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar")],
            [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = self.get_text(user_id,
            "🌐 **اختر اللغة**",
            "🌐 **Choose Language**"
        )
        
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def handle_button_click(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        data = query.data
        user_id = query.from_user.id
        
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
        elif data.startswith("material_"):
            parts = data.split("_")
            day_num = int(parts[1])
            material_index = int(parts[2])
            await self.show_material(query, day_num, material_index)
        elif data.startswith("quiz_"):
            day_num = int(data.split("_")[1])
            await self.start_quiz(query, day_num)
        elif data.startswith("lang_"):
            lang = data.split("_")[1]
            user_language[user_id] = lang
            await query.edit_message_text(
                self.get_text(user_id, "✅ تم تغيير اللغة إلى العربية", "✅ Language changed to English")
            )
            await self.show_main_menu_callback(query)
        elif data == "lang_menu":
            await self.change_language_callback(query)
    
    async def show_main_menu_callback(self, query):
        user_id = query.from_user.id
        keyboard = [
            [InlineKeyboardButton("📅 التدريب اليومي", callback_data="today_training")],
            [InlineKeyboardButton("📚 جميع أيام التدريب", callback_data="all_days")],
            [InlineKeyboardButton("📊 تقدمي", callback_data="progress")],
            [InlineKeyboardButton("❓ الاختبارات", callback_data="quizzes_menu")],
            [InlineKeyboardButton("🌐 تغيير اللغة", callback_data="lang_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        menu_text = self.get_text(user_id,
            "🏫 **القائمة الرئيسية**\n\nاختر مسار التعلم:",
            "🏫 **Main Menu**\n\nChoose your learning path:"
        )
        
        await query.edit_message_text(menu_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_todays_training_callback(self, query):
        user_id = query.from_user.id
        progress = user_progress.get(user_id, {})
        current_day = progress.get("current_day", 1)
        await self.show_day_overview_callback(query, current_day)
    
    async def show_progress_callback(self, query):
        user_id = query.from_user.id
        progress = user_progress.get(user_id, {})
        current_day = progress.get("current_day", 1)
        completed_days = len(progress.get("completed_days", set()))
        
        progress_text = self.get_text(user_id,
            f"📊 **تقدمك**\n\nاليوم: {current_day}/15\nمكتمل: {completed_days}/15\nالنسبة: {round((completed_days/15)*100)}%",
            f"📊 **Progress**\n\nDay: {current_day}/15\nCompleted: {completed_days}/15\nRate: {round((completed_days/15)*100)}%"
        )
        
        keyboard = [
            [InlineKeyboardButton("📚 متابعة", callback_data="today_training")],
            [InlineKeyboardButton("🏠 رئيسية", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(progress_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_all_days(self, query):
        user_id = query.from_user.id
        keyboard = []
        for day in range(1, 16):
            day_data = TRAINING_DATA.get(day, {})
            day_title = self.get_text(user_id, day_data.get("title_ar", f"اليوم {day}"), day_data.get("title_en", f"Day {day}"))
            keyboard.append([InlineKeyboardButton(day_title, callback_data=f"day_{day}")])
        
        keyboard.append([InlineKeyboardButton(
            self.get_text(user_id, "🏠 القائمة الرئيسية", "🏠 Main Menu"), 
            callback_data="main_menu"
        )])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = self.get_text(user_id,
            "📚 **جميع أيام التدريب**\n\nاختر يوماً لعرض محتواه:",
            "📚 **All Training Days**\n\nSelect a day to view its content:"
        )
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_quizzes_menu(self, query):
        user_id = query.from_user.id
        keyboard = []
        for day in range(1, 16):
            day_data = TRAINING_DATA.get(day, {})
            if day_data.get("quiz"):
                keyboard.append([InlineKeyboardButton(
                    self.get_text(user_id, f"اختبار اليوم {day}", f"Day {day} Quiz"), 
                    callback_data=f"quiz_{day}"
                )])
        
        keyboard.append([InlineKeyboardButton(
            self.get_text(user_id, "🏠 القائمة الرئيسية", "🏠 Main Menu"), 
            callback_data="main_menu"
        )])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = self.get_text(user_id,
            "❓ **الاختبارات المتاحة**\n\nاختبر معرفتك بعد كل يوم تدريبي:",
            "❓ **Available Quizzes**\n\nTest your knowledge after each training day:"
        )
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_day_overview(self, update, day_num):
        user_id = update.effective_user.id if hasattr(update, 'effective_user') else update.from_user.id
        day_data = TRAINING_DATA.get(day_num, {})
        day_title = self.get_text(user_id, day_data.get("title_ar", f"اليوم {day_num}"), day_data.get("title_en", f"Day {day_num}"))
        
        overview_text = f"{day_title}\n\n{self.get_text(user_id, '**المواد المتاحة:**', '**Available Materials:**')}\n"
        
        materials = day_data.get("materials", [])
        for i, material in enumerate(materials, 1):
            material_title = self.get_text(user_id, material.get("title_ar", ""), material.get("title_en", ""))
            overview_text += f"• {material_title}\n"
        
        quiz_title = self.get_text(user_id, day_data.get("quiz", {}).get("title_ar", "متاح"), day_data.get("quiz", {}).get("title_en", "Available"))
        overview_text += f"\n**{self.get_text(user_id, 'الاختبار:', 'Quiz:')}** {quiz_title}"
        
        # Create buttons for materials
        keyboard = []
        for i, material in enumerate(materials):
            material_title = self.get_text(user_id, material.get("title_ar", ""), material.get("title_en", ""))
            keyboard.append([InlineKeyboardButton(f"📖 {material_title}", callback_data=f"material_{day_num}_{i}")])
        
        # Add quiz button if available
        if day_data.get("quiz"):
            keyboard.append([InlineKeyboardButton(
                self.get_text(user_id, "❓ اختبار", "❓ Take Quiz"), 
                callback_data=f"quiz_{day_num}"
            )])
        
        # Navigation buttons
        nav_buttons = []
        if day_num > 1:
            nav_buttons.append(InlineKeyboardButton(
                self.get_text(user_id, "⬅️ اليوم السابق", "⬅️ Previous Day"), 
                callback_data=f"day_{day_num-1}"
            ))
        if day_num < 15:
            nav_buttons.append(InlineKeyboardButton(
                self.get_text(user_id, "اليوم التالي ➡️", "Next Day ➡️"), 
                callback_data=f"day_{day_num+1}"
            ))
        
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        keyboard.append([InlineKeyboardButton(
            self.get_text(user_id, "🏠 القائمة الرئيسية", "🏠 Main Menu"), 
            callback_data="main_menu"
        )])
        
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
            await query.answer(self.get_text(user_id, "لا توجد مواد أخرى", "No more materials available"))
            return
        
        material = materials[material_index]
        content = self.get_text(user_id, material.get("content_ar", ""), material.get("content_en", ""))
        
        # Create navigation buttons
        keyboard = []
        if material_index > 0:
            keyboard.append(InlineKeyboardButton(
                self.get_text(user_id, "⬅️ السابق", "⬅️ Previous"), 
                callback_data=f"material_{day_num}_{material_index-1}"
            ))
        if material_index < len(materials) - 1:
            keyboard.append(InlineKeyboardButton(
                self.get_text(user_id, "التالي ➡️", "Next ➡️"), 
                callback_data=f"material_{day_num}_{material_index+1}"
            ))
        
        if keyboard:
            keyboard = [keyboard]
        
        keyboard.append([InlineKeyboardButton(
            self.get_text(user_id, "📋 نظرة عامة على اليوم", "📋 Day Overview"), 
            callback_data=f"day_{day_num}"
        )])
        keyboard.append([InlineKeyboardButton(
            self.get_text(user_id, "🏠 القائمة الرئيسية", "🏠 Main Menu"), 
            callback_data="main_menu"
        )])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(content, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def start_quiz(self, query, day_num):
        user_id = query.from_user.id
        day_data = TRAINING_DATA.get(day_num, {})
        quiz_data = day_data.get("quiz")
        
        if not quiz_data:
            await query.answer(self.get_text(user_id, "لا يوجد اختبار لهذا اليوم", "No quiz available for this day"))
            return
        
        quiz_title = self.get_text(user_id, quiz_data.get("title_ar", ""), quiz_data.get("title_en", ""))
        await query.edit_message_text(f"بدء {quiz_title}...")
    
    async def change_language_callback(self, query):
        user_id = query.from_user.id
        keyboard = [
            [InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar")],
            [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        text = self.get_text(user_id,
            "🌐 **اختر اللغة**",
            "🌐 **Choose Language**"
        )
        
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        text = update.message.text
        
        response = self.get_text(user_id,
            "👋 استخدم /menu للوصول إلى القائمة الرئيسية والتعرف على جميع الميزات المتاحة!",
            "👋 Use /menu to access the main menu and discover all available features!"
        )
        
        await update.message.reply_text(response)

def run_bot(token):
    """Run the Telegram bot"""
    global bot_app
    try:
        logging.info("🤖 Creating bot application...")
        bot_app = TrainingBot(token)
        logging.info("✅ Bot setup completed successfully!")
        logging.info("🚀 Starting bot polling...")
        bot_app.application.run_polling()
    except Exception as e:
        logging.error(f"❌ Bot failed: {e}")
        import traceback
        logging.error(traceback.format_exc())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    # Get token
    token = os.environ.get('TELEGRAM_TOKEN')
    
    if token:
        logging.info(f"✅ TELEGRAM_TOKEN found! Starting bot...")
        
        # Start bot in a separate thread
        bot_thread = threading.Thread(target=run_bot, args=(token,), daemon=True)
        bot_thread.start()
        logging.info("✅ Bot thread started!")
    else:
        logging.error("❌ TELEGRAM_TOKEN not found!")
    
    # Start Flask
    logging.info(f"🌐 Starting Flask on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
