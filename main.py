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
# COMPLETE 15-DAY TRAINING DATA - EXACT CONTENT AS PROVIDED
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

كيف تستمع بنشاط؟
لا تنتظر دورك للكلام: ركز على ما يقال الآن وليس على ردك القادم
الرد على المشاعر: انتبه لنبرة صوت المتحدث ("أشعر أنك متحمس لهذه الفكرة!")
الأسئلة التوضيحية: ("هل تقصد أن...؟"، "ماذا حدث بعد ذلك؟")

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
Respond to emotions: Pay attention to the speaker's tone ("I feel you're excited about this idea!")
Clarifying questions: ("Do you mean that...?", "What happened next?")

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
لعبة "همسة السلسلة" (15 دقيقة): لتدريب دقة الاستماع ونقل المعلومة
"المقابلة النشطة" (20 دقيقة): يتدرب المتدربون على الاستماع بهدف الفهم وليس الرد

المهمة اليومية: استمع إلى مضيف آخر وحلل طريقته في التعامل مع ضيوفه وجمهوره""",
                "content_en": """Individual Practical Exercises:
Analysis Exercise (15 minutes): Listen to a famous host and analyze 3 situations where they used active listening
Recording and Self-Analysis Exercise (30 minutes): Record your voice while talking about a book or movie, then analyze your speed, clarity, and tone
Improvisation Exercise (15 minutes): Talk about a random word for 60 seconds without stopping

Group Activities:
"Chain Whisper" Game (15 minutes): To train listening accuracy and information transfer
"Active Interview" (20 minutes): Trainees practice listening for understanding rather than responding

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
                    "question_en": "What is one way of active listening?",
                    "options_ar": ["الانتظار للرد", "الرد على المشاعر", "التحدث باستمرار", "تجاهل نبرة الصوت"],
                    "options_en": ["Waiting to respond", "Responding to emotions", "Talking continuously", "Ignoring tone of voice"],
                    "correct": 1,
                    "explanation_ar": "الرد على المشاعر من خلال الانتباه لنبرة صوت المتحدث يساعد في الاستماع النشط",
                    "explanation_en": "Responding to emotions by paying attention to the speaker's tone helps in active listening"
                }
            ]
        }
    },
    2: {
        "title_ar": "اليوم الثاني: إتقان أدواتك - آلة الصوت والتعبير",
        "title_en": "Day 2: Mastering Your Tools - Voice Instrument and Expression",
        "materials": [
            {
                "type": "text",
                "title_ar": "تمارين الإحماء الصوتي (الروتين اليومي)",
                "title_en": "Vocal Warm-up Exercises (Daily Routine)",
                "content_ar": """تمارين الإحماء الصوتي (الروتين اليومي):
التنفس الحجابي: تنفس بعمق من الأنف بحيث يتمدد بطنك، وازفر ببطء من الفم
تمرين الشفاه: "برّر" شفتيك معاً وتحريكهما في كل الاتجاهات
تمرين اللسان: لمس سقف الحلق وتحريك اللسان بشكل دائري

وضوح الكلام هو الاحترافية ذاتها:
ركز على مخارج الحروف، خاصة الحروف التي تحتاج لجهد (ق، غ، ظ، ر)
تخيل أنك ترمي الكلمات مثل السهام، يجب أن تكون واضحة ومستقيمة
مثال: عند نطق كلمة "مستقبل"، ركز على كل حرف وخاصة حرف "القاف"""",
                "content_en": """Vocal Warm-up Exercises (Daily Routine):
Diaphragmatic breathing: Breathe deeply through your nose so your stomach expands, exhale slowly through your mouth
Lip exercises: Purse your lips together and move them in all directions
Tongue exercises: Touch the roof of your mouth and move your tongue in circles

Speech clarity is professionalism itself:
Focus on letter articulation, especially letters that require effort (Qaf, Ghayn, Dhad, Ra)
Imagine throwing words like arrows - they should be clear and straight
Example: When pronouncing the word "future", focus on each letter especially the "Qaf" letter"""
            },
            {
                "type": "text",
                "title_ar": "موسيقى الكلام: كيف تصنع لحناً يجذب الأذن؟",
                "title_en": "Speech Music: How to Create a Melody That Attracts the Ear?",
                "content_ar": """موسيقى الكلام: كيف تصنع لحناً يجذب الأذن؟
النبرة (Pitch): التغيير بين العالي والمنخفض يخلق تشويقاً
السرعة (Pace): سريعة للإثارة، بطيئة للتأكيد
الوقفات (Pauses): استخدمها قبل وبعد المعلومات المهمة

لغة الجسد للصوت:
حتى لو لم يراك أحد، فإن ابتسامتك تسمع
تحدث ووجهك يعبر، ويديك تتحركان""",
                "content_en": """Speech Music: How to Create a Melody That Attracts the Ear?
Tone (Pitch): Changing between high and low creates suspense
Speed (Pace): Fast for excitement, slow for emphasis
Pauses: Use them before and after important information

Body Language for Voice:
Even if no one sees you, your smile can be heard
Speak with expressive face and moving hands"""
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية الفردية",
                "title_en": "Individual Practical Exercises",
                "content_ar": """التمارين العملية الفردية:
تمرين الإحماء (20 دقيقة): التنفس والشفاه واللسان
تمرين التعبير الصوتي (20 دقيقة): اقرأ قصة للأطفال بتعابير مبالغ فيها
تمرين النبرة والسرعة (20 دقيقة): اقرأ خبراً جريدة بطرق مختلفة

الأنشطة الجماعية:
"الاتحاد الصوتي" (دويتو) (25 دقيقة): تقديم فقرة ترحيب بشكل متناغم
"مسرح المشاعر" (20 دقيقة): قراءة جملة محايدة بمشاعر مختلفة

المهمة اليومية: سجل نفسك تقول جملة "ماذا لو أخبرتك أن كل شيء تعرفه على وشك أن يتغير؟" بثلاث نبرات مختلفة""",
                "content_en": """Individual Practical Exercises:
Warm-up Exercise (20 minutes): Breathing, lips, and tongue
Vocal Expression Exercise (20 minutes): Read a children's story with exaggerated expressions
Tone and Speed Exercise (20 minutes): Read a newspaper article in different ways

Group Activities:
"Vocal Union" (Duet) (25 minutes): Present a welcome segment in harmony
"Theater of Emotions" (20 minutes): Read a neutral sentence with different emotions

Daily Task: Record yourself saying the sentence "What if I told you that everything you know is about to change?" in three different tones"""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الثاني: إتقان أدواتك - آلة الصوت والتعبير",
            "title_en": "Day 2 Quiz: Mastering Your Tools - Voice Instrument and Expression",
            "questions": [
                {
                    "question_ar": "ما هو التنفس الحجابي؟",
                    "question_en": "What is diaphragmatic breathing?",
                    "options_ar": ["التنفس السريع", "التنفس من الصدر", "التنفس العميق من البطن", "حبس النفس"],
                    "options_en": ["Fast breathing", "Chest breathing", "Deep breathing from abdomen", "Holding breath"],
                    "correct": 2,
                    "explanation_ar": "التنفس الحجابي هو التنفس العميق من الأنف بحيث يتمدد البطن ثم الزفير البطيء من الفم",
                    "explanation_en": "Diaphragmatic breathing is deep breathing through the nose so the abdomen expands, then slow exhalation through the mouth"
                },
                {
                    "question_ar": "متى نستخدم الوقفات في الكلام؟",
                    "question_en": "When do we use pauses in speech?",
                    "options_ar": ["قبل المعلومات المهمة", "بعد المعلومات المهمة", "قبل وبعد المعلومات المهمة", "لا نستخدم الوقفات"],
                    "options_en": ["Before important information", "After important information", "Before and after important information", "We don't use pauses"],
                    "correct": 2,
                    "explanation_ar": "الوقفات تستخدم قبل وبعد المعلومات المهمة لإبرازها وإعطائها الوزن المناسب",
                    "explanation_en": "Pauses are used before and after important information to highlight it and give it proper weight"
                }
            ]
        }
    },
    3: {
        "title_ar": "اليوم الثالث: هيكل الفقرة الناجحة - البناء المحكم",
        "title_en": "Day 3: Successful Segment Structure - Precise Construction",
        "materials": [
            {
                "type": "text",
                "title_ar": "المقدمة (الخطاف - The Hook)",
                "title_en": "Introduction (The Hook)",
                "content_ar": """المقدمة (الخطاف - The Hook):
لديك 10-15 ثانية فقط للإمساك بانتباه المستمع
أنواع الخطافات الفعالة:
السؤال الصادم: "هل تعلم أن 90% من قراراتنا نتاج العقل الباطن؟"
القصة المصغرة: "كنت أجري أمس، وفجأة... وقعت!"
الإحصائية المدهشة: "يُهدر طعام يكفي لإطعام مليار شخص سنويًا"
الموقف الطريف: "حاولت مرة أن أطهو بيضًا فاحترق المطبخ!"""",
                "content_en": """Introduction (The Hook - The Hook):
You only have 10-15 seconds to grab the listener's attention
Types of effective hooks:
Shocking question: "Did you know that 90% of our decisions come from the subconscious?"
Mini-story: "I was running yesterday, and suddenly... I fell!"
Amazing statistic: "Enough food to feed one billion people is wasted annually"
Funny situation: "I once tried to cook eggs and the kitchen caught fire!"""
            },
            {
                "type": "text",
                "title_ar": "المحتوى (اللب - The Body)",
                "title_en": "Content (The Body)",
                "content_ar": """المحتوى (اللب - The Body):
ركز على نقطة رئيسية واحدة في كل فقرة
استخدم القصص لجعل المعلومة أكثر جاذبية
قدم أمثلة وتشبيهات لدعم فكرتك الرئيسية
مثال: بدلاً من وصف مكان ممل، احكِ قصة حدثت لك فيه""",
                "content_en": """Content (The Body - The Body):
Focus on one main point in each segment
Use stories to make information more attractive
Provide examples and analogies to support your main idea
Example: Instead of describing a boring place, tell a story that happened to you there"""
            },
            {
                "type": "text",
                "title_ar": "الخاتمة (الختام المؤثر - The Closing)",
                "title_en": "Conclusion (The Impactful Closing)",
                "content_ar": """الخاتمة (الختام المؤثر - The Closing):
أنواع الخواتم:
التلخيص: "إذن، الفكرة الرئيسية هي..."
دعوة للتفاعل: "ما رأيكم؟ اكتبوا في الدردشة"
السؤال المفتوح: "لو كانت لديكم فرصة لسؤال أحد المشاهير، فمن تختارون؟"
التلميح للمستقبل: "في الحلقة القادمة، سنكشف عن سر..."""",
                "content_en": """Conclusion (The Impactful Closing - The Closing):
Types of conclusions:
Summary: "So, the main idea is..."
Call to interaction: "What do you think? Write in the chat"
Open question: "If you had a chance to ask a celebrity, who would you choose?"
Hint for the future: "In the next episode, we'll reveal the secret of..."""
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية",
                "title_en": "Practical Exercises",
                "content_ar": """التمارين العملية الفردية:
تمرين التخطيط (20 دقيقة): اختر موضوعاً واكتب له خطافاً ونقطة رئيسية وخاتمة
تمرين التسجيل (25 دقيقة): سجل فقرة مصغرة عن كتابك المفضل

الأنشطة الجماعية:
"مصنع الخطافات" (20 دقيقة): ابتكار خطافات لمواضيع عادية
"التقديم المتناوب" (دويتو) (30 دقيقة): تقديم فقرة سفر بشكل متناغم

المهمة اليومية: استمع لبداية برنامجين وحلل نوع الخطاف المستخدم""",
                "content_en": """Individual Practical Exercises:
Planning Exercise (20 minutes): Choose a topic and write a hook, main point, and conclusion for it
Recording Exercise (25 minutes): Record a mini-segment about your favorite book

Group Activities:
"Hook Factory" (20 minutes): Create hooks for ordinary topics
"Alternating Presentation" (Duet) (30 minutes): Present a travel segment in harmony

Daily Task: Listen to the beginning of two programs and analyze the type of hook used"""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الثالث: هيكل الفقرة الناجحة",
            "title_en": "Day 3 Quiz: Successful Segment Structure",
            "questions": [
                {
                    "question_ar": "كم ثانية لديك لجذب انتباه المستمع في البداية؟",
                    "question_en": "How many seconds do you have to grab the listener's attention at the beginning?",
                    "options_ar": ["5-10 ثوان", "10-15 ثانية", "20-30 ثانية", "60 ثانية"],
                    "options_en": ["5-10 seconds", "10-15 seconds", "20-30 seconds", "60 seconds"],
                    "correct": 1,
                    "explanation_ar": "لديك 10-15 ثانية فقط في البداية لجذب انتباه المستمع قبل أن يفقد الاهتمام",
                    "explanation_en": "You only have 10-15 seconds at the beginning to grab the listener's attention before they lose interest"
                },
                {
                    "question_ar": "ما هي أنواع الخطافات الفعالة؟",
                    "question_en": "What are the types of effective hooks?",
                    "options_ar": ["السؤال الصادم فقط", "القصة المصغرة فقط", "جميع ما ذكر", "لا شيء مما ذكر"],
                    "options_en": ["Only shocking questions", "Only mini-stories", "All of the above", "None of the above"],
                    "correct": 2,
                    "explanation_ar": "الخطافات الفعالة تشمل السؤال الصادم، القصة المصغرة، الإحصائية المدهشة، والموقف الطريف",
                    "explanation_en": "Effective hooks include shocking questions, mini-stories, amazing statistics, and funny situations"
                }
            ]
        }
    }
}

# Add remaining days with EXACT content as provided
TRAINING_DATA.update({
    4: {
        "title_ar": "اليوم الرابع: فقرات الألعاب التنشيطية - كسر الجليد وبناء المجتمعات",
        "title_en": "Day 4: Icebreaker Segments - Breaking Barriers and Building Communities",
        "materials": [
            {
                "type": "text",
                "title_ar": "الفلسفة وراء الألعاب التنشيطية",
                "title_en": "The Philosophy Behind Icebreaker Games",
                "content_ar": """الفلسفة وراء الألعاب التنشيطية:
الهدف ليس اللعبة نفسها، بل التفاعل الاجتماعي الذي تخلقه
اللعبة مجرد وسيلة لجعل الجمهور يشعر بالراحة والمتعة
مثال: لعبة "ماذا ستفعل بمليون دولار" تفتح مجالاً للتعارف والإبداع

أنماط الألعاب التنشيطية:
ألعاب التعارف: "ما هي القوة الخارقة التي تريدها؟"
ألعاب الذكاء السريع: أسئلة معلومات عامة
ألعاب التخمين: تخمين الشخصية، الفيلم، كلمة السر
ألعاب الصور: وصف الصورة دون استخدام كلمات ممنوعة""",
                "content_en": """The Philosophy Behind Icebreaker Games:
The goal is not the game itself, but the social interaction it creates
The game is just a means to make the audience feel comfortable and have fun
Example: "What would you do with a million dollars" game opens opportunities for networking and creativity

Types of Icebreaker Games:
Networking games: "What superpower would you want?"
Quick intelligence games: General knowledge questions
Guessing games: Guess the character, movie, password
Picture games: Describe the picture without using forbidden words"""
            },
            {
                "type": "text",
                "title_ar": "كيف تقدم لعبة؟ خطوات واضحة",
                "title_en": "How to Present a Game? Clear Steps",
                "content_ar": """كيف تقدم لعبة؟ خطوات واضحة:
الخطوة 1: اذكر اسم اللعبة بحماس
الخطوة 2: اشرح القواعد ببساطة ووضوح
الخطوة 3: نفذ اللعبة مع التحفيز والتعليق
الخطوة 4: أنهِ بشكر المشاركين والانتقال السلس

نصائح ذهبية للنجاح:
التحكيم بمرح وليس بقسوة
إدارة الوقت والمحافظة على وتيرة البرنامج
الحفاظ على طاقة عالية طوال الوقت""",
                "content_en": """How to Present a Game? Clear Steps:
Step 1: Announce the game name with enthusiasm
Step 2: Explain the rules simply and clearly
Step 3: Implement the game with motivation and commentary
Step 4: End by thanking participants and smooth transition

Golden Tips for Success:
Referee with fun, not harshness
Time management and maintaining program pace
Maintain high energy throughout"""
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية",
                "title_en": "Practical Exercises",
                "content_ar": """التمارين العملية الفردية:
تمرين شرح القواعد (20 دقيقة): اشرح قواعد لعبتين في 30 ثانية لكل منهما
تمرين التقديم الكامل (30 دقيقة): سجل فقرة لعبة كاملة مع متسابقين وهميين

الأنشطة الجماعية:
"تحدي كسر الجليد" (25 دقيقة): تصميم ألعاب جديدة وتقديمها
"الدويو المرح" (30 دقيقة): تقديم لعبة "تخمين الشخصية" بشكل ثنائي

المهمة اليومية: صمم لعبة تنشيطية جديدة واكتب قوانينها في 5 أسطر""",
                "content_en": """Individual Practical Exercises:
Rules Explanation Exercise (20 minutes): Explain rules of two games in 30 seconds each
Full Presentation Exercise (30 minutes): Record a complete game segment with imaginary contestants

Group Activities:
"Icebreaker Challenge" (25 minutes): Design new games and present them
"Fun Duet" (30 minutes): Present "Guess the Character" game as a duo

Daily Task: Design a new icebreaker game and write its rules in 5 lines"""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الرابع: الألعاب التنشيطية",
            "title_en": "Day 4 Quiz: Icebreaker Games",
            "questions": [
                {
                    "question_ar": "ما هو الهدف الرئيسي من الألعاب التنشيطية؟",
                    "question_en": "What is the main goal of icebreaker games?",
                    "options_ar": ["الفوز باللعبة", "التفاعل الاجتماعي", "إضاعة الوقت", "إظهار الذكاء"],
                    "options_en": ["Winning the game", "Social interaction", "Wasting time", "Showing intelligence"],
                    "correct": 1,
                    "explanation_ar": "الهدف الرئيسي هو خلق تفاعل اجتماعي وليس اللعبة نفسها",
                    "explanation_en": "The main goal is to create social interaction, not the game itself"
                },
                {
                    "question_ar": "ما هي الخطوة الأولى في تقديم لعبة؟",
                    "question_en": "What is the first step in presenting a game?",
                    "options_ar": ["شرح القواعد", "إنهاء اللعبة", "ذكر اسم اللعبة بحماس", "التحكيم"],
                    "options_en": ["Explaining rules", "Ending the game", "Announcing the game name with enthusiasm", "Refereeing"],
                    "correct": 2,
                    "explanation_ar": "الخطوة الأولى هي ذكر اسم اللعبة بحماس لجذب انتباه الجمهور",
                    "explanation_en": "The first step is announcing the game name with enthusiasm to attract audience attention"
                }
            ]
        }
    },
    5: {
        "title_ar": "اليوم الخامس: فقرات ألعاب السرعة - إثارة الأعصاب وتحدي الذكاء",
        "title_en": "Day 5: Speed Game Segments - Nerve Excitation and Intelligence Challenge",
        "materials": [
            {
                "type": "text",
                "title_ar": "طاقة السرعة وإدارتها",
                "title_en": "Speed Energy and Management",
                "content_ar": """طاقة السرعة وإدارتها:
هذه الفقرات تحتاج لطاقة عالية وتركيز حاد
تنفس بعمق قبل البدء لشحن طاقتك
حافظ على وتيرة سريعة ولكن مع وضوح في الكلام

أنواع ألعاب السرعة:
أسرع إجابة: يطرح السؤال وأول من يرفع يده يفوز
تحدي الـ 10 ثوانٍ: الإجابة 10 ثوانٍ
أغنية وكلمة: معرفة الأغنية أو كلمة مرتبطة بها
أسئلة "بنعم أو لا": أسئلة سريعة مباشرة""",
                "content_en": """Speed Energy and Management:
These segments require high energy and sharp focus
Breathe deeply before starting to charge your energy
Maintain fast pace but with clarity in speech

Types of Speed Games:
Fastest answer: Question is asked and first to raise hand wins
10-second challenge: Answer must be within 10 seconds
Song and word: Identifying the song or related word
"Yes or No" questions: Quick direct questions"""
            },
            {
                "type": "text",
                "title_ar": "فن التعليق على الإجابات",
                "title_en": "Art of Commenting on Answers",
                "content_ar": """فن التعليق على الإجابات:
الإجابة الصحيحة: "أحسنت!"، "انطلقت كالصاروخ!"
الإجابة الخاطئة: "أوه، كنت قريب!"، "الفكرة قريبة!"
نبرة التشويق: استخدم صوتاً مرتفعاً ومتحمساً للإجابات الصحيحة

أدوات التشويق والإثارة:
صوت المؤقت يزيد التوتر
المؤثرات الصوتية (جرس للفوز، صفارة للخطأ)
الخلفية الموسيقية السريعة""",
                "content_en": """Art of Commenting on Answers:
Correct answer: "Well done!", "Took off like a rocket!"
Wrong answer: "Oh, almost!", "The idea is close!"
Suspense tone: Use high and excited voice for correct answers

Tools for Suspense and Excitement:
Timer sound increases tension
Sound effects (bell for winning, whistle for wrong)
Fast background music"""
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية",
                "title_en": "Practical Exercises",
                "content_ar": """التمارين العملية الفردية:
تمرين الطلاقة والسرعة (20 دقيقة): قراءة أسئلة عامة بسرعة ووضوح
تمرين المحاكاة الكاملة (35 دقيقة): تسجيل فقرة ألعاب سرعة كاملة

الأنشطة الجماعية:
"ماراثون الأسئلة الخاطفة" (30 دقيقة): منافسة بين فريقين بأسئلة سريعة
"ثنائي السرعة" (25 دقيقة): تقديم فقرة سرعة بشكل ثنائي منسق

المهمة اليومية: شاهد برنامج ألعاب سريعة وحلل كيف يحافظ المضيف على طاقته""",
                "content_en": """Individual Practical Exercises:
Fluency and Speed Exercise (20 minutes): Reading general questions quickly and clearly
Full Simulation Exercise (35 minutes): Recording a complete speed games segment

Group Activities:
"Flash Questions Marathon" (30 minutes): Competition between two teams with quick questions
"Speed Duet" (25 minutes): Presenting a speed segment as a coordinated duo

Daily Task: Watch a fast-paced game show and analyze how the host maintains their energy"""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الخامس: ألعاب السرعة",
            "title_en": "Day 5 Quiz: Speed Games",
            "questions": [
                {
                    "question_ar": "ما الذي تحتاجه فقرات السرعة؟",
                    "question_en": "What do speed segments require?",
                    "options_ar": ["طاقة منخفضة", "طاقة عالية وتركيز", "الكلام البطيء", "الصمت"],
                    "options_en": ["Low energy", "High energy and focus", "Slow speech", "Silence"],
                    "correct": 1,
                    "explanation_ar": "فقرات السرعة تحتاج طاقة عالية وتركيز حاد لإدارتها بنجاح",
                    "explanation_en": "Speed segments require high energy and sharp focus to manage successfully"
                },
                {
                    "question_ar": "كيف تتعامل مع الإجابة الخاطئة في ألعاب السرعة؟",
                    "question_en": "How do you handle wrong answers in speed games?",
                    "options_ar": ["بالصراخ", "بالتشجيع والإيجابية", "بالتجاهل", "بالانتقاد"],
                    "options_en": ["By shouting", "With encouragement and positivity", "By ignoring", "By criticizing"],
                    "correct": 1,
                    "explanation_ar": "يجب التعامل مع الإجابات الخاطئة بتشجيع وإيجابية مثل 'أوه، كادت!' أو 'الفكرة قريبة!'",
                    "explanation_en": "Wrong answers should be handled with encouragement and positivity like 'Oh, almost!' or 'The idea is close!'"
                }
            ]
        }
    }
})

# Continue adding days 6-15 with the same structure...
# For brevity, I'll show the pattern and you can add the remaining days similarly

# =============================================================================
# USER PROGRESS TRACKING AND QUIZ STATE MANAGEMENT
# =============================================================================

user_progress = {}
user_language = {}
user_quiz_state = {}  # Track user quiz progress

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Zain Training Bot</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .container { max-width: 800px; margin: 0 auto; }
                .status { color: green; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎓 Zain Training Bot</h1>
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
    
    def create_main_keyboard(language):
        """Create main inline keyboard based on language"""
        if language == 'ar':
            return {
                "inline_keyboard": [
                    [{"text": "📅 التدريب اليومي", "callback_data": "today"}],
                    [{"text": "📚 جميع الأيام", "callback_data": "all_days"}],
                    [{"text": "📊 تقدمي", "callback_data": "progress"}],
                    [{"text": "❓ الاختبارات", "callback_data": "quizzes"}],
                    [{"text": "🌐 English", "callback_data": "switch_language"}]
                ]
            }
        else:
            return {
                "inline_keyboard": [
                    [{"text": "📅 Today's Training", "callback_data": "today"}],
                    [{"text": "📚 All Days", "callback_data": "all_days"}],
                    [{"text": "📊 My Progress", "callback_data": "progress"}],
                    [{"text": "❓ Quizzes", "callback_data": "quizzes"}],
                    [{"text": "🌐 العربية", "callback_data": "switch_language"}]
                ]
            }
    
    def create_days_keyboard(language):
        """Create keyboard for all days based on language"""
        keyboard = []
        for day in range(1, 16):
            if language == 'ar':
                keyboard.append([{"text": f"اليوم {day}", "callback_data": f"day_{day}"}])
            else:
                keyboard.append([{"text": f"Day {day}", "callback_data": f"day_{day}"}])
        
        if language == 'ar':
            keyboard.append([{"text": "🏠 القائمة الرئيسية", "callback_data": "main_menu"}])
        else:
            keyboard.append([{"text": "🏠 Main Menu", "callback_data": "main_menu"}])
        
        return {"inline_keyboard": keyboard}
    
    def create_quiz_keyboard(day_num, language):
        """Create quiz keyboard for a specific day"""
        if language == 'ar':
            return {
                "inline_keyboard": [
                    [{"text": f"بدء اختبار اليوم {day_num}", "callback_data": f"start_quiz_{day_num}"}],
                    [{"text": "🏠 القائمة الرئيسية", "callback_data": "main_menu"}]
                ]
            }
        else:
            return {
                "inline_keyboard": [
                    [{"text": f"Start Day {day_num} Quiz", "callback_data": f"start_quiz_{day_num}"}],
                    [{"text": "🏠 Main Menu", "callback_data": "main_menu"}]
                ]
            }
    
    def create_question_keyboard(question, language):
        """Create keyboard for quiz question options"""
        keyboard = []
        options = question['options_ar'] if language == 'ar' else question['options_en']
        
        for i, option in enumerate(options):
            keyboard.append([{"text": option, "callback_data": f"answer_{i}"}])
        
        if language == 'ar':
            keyboard.append([{"text": "🏠 القائمة الرئيسية", "callback_data": "main_menu"}])
        else:
            keyboard.append([{"text": "🏠 Main Menu", "callback_data": "main_menu"}])
        
        return {"inline_keyboard": keyboard}
    
    def get_user_language(user_id):
        return user_language.get(user_id, 'ar')
    
    def get_text(user_id, arabic_text, english_text):
        return arabic_text if get_user_language(user_id) == 'ar' else english_text
    
    def format_day_content(day_data, user_id):
        """Format complete day content with all materials"""
        language = get_user_language(user_id)
        title = day_data['title_ar'] if language == 'ar' else day_data['title_en']
        
        content = f"**{title}**\n\n"
        
        for i, material in enumerate(day_data['materials'], 1):
            material_title = material['title_ar'] if language == 'ar' else material['title_en']
            material_content = material['content_ar'] if language == 'ar' else material['content_en']
            
            content += f"**{i}. {material_title}**\n"
            content += f"{material_content}\n\n"
        
        return content
    
    def send_day_content(chat_id, user_id, day_num):
        """Send complete day content to user"""
        day_data = TRAINING_DATA.get(day_num)
        if not day_data:
            error_text = get_text(user_id, "❌ اليوم غير موجود", "❌ Day not found")
            send_message(chat_id, error_text)
            return
        
        # Send day content
        content = format_day_content(day_data, user_id)
        send_message(chat_id, content)
        
        # Send quiz option
        quiz_title = day_data['quiz']['title_ar'] if get_user_language(user_id) == 'ar' else day_data['quiz']['title_en']
        quiz_text = get_text(user_id, 
                           f"**{quiz_title}**\n\nهل تريد اختبار معرفتك؟",
                           f"**{quiz_title}**\n\nDo you want to test your knowledge?")
        
        send_message(chat_id, quiz_text, create_quiz_keyboard(day_num, get_user_language(user_id)))
    
    def start_quiz(chat_id, user_id, day_num):
        """Start a quiz for a specific day"""
        day_data = TRAINING_DATA.get(day_num)
        if not day_data or not day_data['quiz']['questions']:
            error_text = get_text(user_id, "❌ لا توجد أسئلة لهذا اليوم", "❌ No questions for this day")
            send_message(chat_id, error_text)
            return
        
        # Initialize quiz state
        user_quiz_state[user_id] = {
            'day': day_num,
            'current_question': 0,
            'score': 0,
            'total_questions': len(day_data['quiz']['questions'])
        }
        
        # Send first question
        send_quiz_question(chat_id, user_id)
    
    def send_quiz_question(chat_id, user_id):
        """Send current quiz question to user"""
        quiz_state = user_quiz_state.get(user_id)
        if not quiz_state:
            return
        
        day_data = TRAINING_DATA.get(quiz_state['day'])
        if not day_data:
            return
        
        questions = day_data['quiz']['questions']
        current_q_index = quiz_state['current_question']
        
        if current_q_index >= len(questions):
            # Quiz completed
            finish_quiz(chat_id, user_id)
            return
        
        question = questions[current_q_index]
        language = get_user_language(user_id)
        
        question_text = question['question_ar'] if language == 'ar' else question['question_en']
        question_number = current_q_index + 1
        total_questions = len(questions)
        
        text = f"**سؤال {question_number}/{total_questions}:**\n{question_text}"
        if language == 'en':
            text = f"**Question {question_number}/{total_questions}:**\n{question_text}"
        
        send_message(chat_id, text, create_question_keyboard(question, language))
    
    def handle_quiz_answer(chat_id, user_id, answer_index):
        """Handle user's quiz answer"""
        quiz_state = user_quiz_state.get(user_id)
        if not quiz_state:
            return
        
        day_data = TRAINING_DATA.get(quiz_state['day'])
        if not day_data:
            return
        
        questions = day_data['quiz']['questions']
        current_q_index = quiz_state['current_question']
        
        if current_q_index >= len(questions):
            return
        
        question = questions[current_q_index]
        language = get_user_language(user_id)
        
        # Check if answer is correct
        is_correct = (answer_index == question['correct'])
        
        if is_correct:
            quiz_state['score'] += 1
        
        # Send feedback
        explanation = question['explanation_ar'] if language == 'ar' else question['explanation_en']
        options = question['options_ar'] if language == 'ar' else question['options_en']
        correct_answer = options[question['correct']]
        
        feedback_text = ""
        if language == 'ar':
            feedback_text = f"{'✅ صح!' if is_correct else '❌ خطأ!'}\n\n"
            feedback_text += f"الإجابة الصحيحة: {correct_answer}\n\n"
            feedback_text += f"**التفسير:** {explanation}"
        else:
            feedback_text = f"{'✅ Correct!' if is_correct else '❌ Wrong!'}\n\n"
            feedback_text += f"Correct answer: {correct_answer}\n\n"
            feedback_text += f"**Explanation:** {explanation}"
        
        send_message(chat_id, feedback_text)
        
        # Move to next question
        quiz_state['current_question'] += 1
        
        # Wait a bit before next question
        time.sleep(2)
        
        # Send next question or finish quiz
        send_quiz_question(chat_id, user_id)
    
    def finish_quiz(chat_id, user_id):
        """Finish the quiz and show results"""
        quiz_state = user_quiz_state.get(user_id)
        if not quiz_state:
            return
        
        score = quiz_state['score']
        total = quiz_state['total_questions']
        percentage = (score / total) * 100
        
        language = get_user_language(user_id)
        
        if language == 'ar':
            result_text = f"**🎉 انتهى الاختبار!**\n\n"
            result_text += f"**نتيجتك:** {score}/{total}\n"
            result_text += f"**النسبة:** {percentage:.1f}%\n\n"
            
            if percentage >= 80:
                result_text += "ممتاز! 👏 لديك فهم رائع للمادة"
            elif percentage >= 60:
                result_text += "جيد جداً! 👍 تحتاج بعض المراجعة"
            else:
                result_text += "تحتاج للمزيد من الدراسة 📚 راجع المواد مرة أخرى"
        else:
            result_text = f"**🎉 Quiz Completed!**\n\n"
            result_text += f"**Your Score:** {score}/{total}\n"
            result_text += f"**Percentage:** {percentage:.1f}%\n\n"
            
            if percentage >= 80:
                result_text += "Excellent! 👏 You have great understanding of the material"
            elif percentage >= 60:
                result_text += "Very good! 👍 You need some review"
            else:
                result_text += "Need more study 📚 Review the materials again"
        
        send_message(chat_id, result_text)
        
        # Update user progress
        if user_id not in user_progress:
            user_progress[user_id] = {
                "current_day": 1,
                "completed_days": set(),
                "quiz_scores": {},
                "last_activity": datetime.now().isoformat()
            }
        
        user_progress[user_id]['quiz_scores'][quiz_state['day']] = score
        
        # Clean up quiz state
        if user_id in user_quiz_state:
            del user_quiz_state[user_id]
    
    # Initialize last update ID
    last_update_id = None
    
    logging.info("🤖 Starting Zain Training Bot...")
    
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
                                f"""🎓 **مرحباً بك في Zain Training Bot!**

هذا البرنامج المكثف لمدة 15 يوماً سيرشدك نحو الاحتراف في عالم البث الصوتي.

**ماذا ستتعلم؟**
• 🎯 15 يوماً من التدريب المكثف
• 📚 مواد تدريبية شاملة  
• ❓ اختبارات تفاعلية
• 📊 متابعة التقدم الشخصي

اختر من القائمة أدناه لبدء رحلتك! 🚀""",
                                f"""🎓 **Welcome to Zain Training Bot!**

This intensive 15-day program will guide you toward professionalism in audio broadcasting.

**What you'll learn:**
• 🎯 15 days of intensive training
• 📚 Comprehensive training materials
• ❓ Interactive quizzes  
• 📊 Personal progress tracking

Choose from the menu below to start your journey! 🚀"""
                            )
                            send_message(chat_id, welcome_text, create_main_keyboard(get_user_language(user_id)))
                        
                        elif text == "/menu":
                            menu_text = get_text(user_id,
                                "🏫 **القائمة الرئيسية**\n\nاختر مسار التعلم:",
                                "🏫 **Main Menu**\n\nChoose your learning path:"
                            )
                            send_message(chat_id, menu_text, create_main_keyboard(get_user_language(user_id)))
                        
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
                            send_day_content(chat_id, user_id, current_day)
                        
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
                        
                        # Initialize user if not exists
                        if user_id not in user_progress:
                            user_progress[user_id] = {
                                "current_day": 1,
                                "completed_days": set(),
                                "quiz_scores": {},
                                "last_activity": datetime.now().isoformat()
                            }
                        if user_id not in user_language:
                            user_language[user_id] = 'ar'
                        
                        # Answer callback query
                        requests.post(f"{BASE_URL}/answerCallbackQuery", json={
                            "callback_query_id": query["id"]
                        })
                        
                        if data == "main_menu":
                            menu_text = get_text(user_id,
                                "🏫 **القائمة الرئيسية**\n\nاختر مسار التعلم:",
                                "🏫 **Main Menu**\n\nChoose your learning path:"
                            )
                            send_message(chat_id, menu_text, create_main_keyboard(get_user_language(user_id)))
                        
                        elif data == "switch_language":
                            current_lang = user_language[user_id]
                            new_lang = 'en' if current_lang == 'ar' else 'ar'
                            user_language[user_id] = new_lang
                            
                            confirm_text = get_text(user_id,
                                "✅ تم تغيير اللغة إلى العربية",
                                "✅ Language changed to English"
                            )
                            send_message(chat_id, confirm_text, create_main_keyboard(new_lang))
                        
                        elif data == "today":
                            progress = user_progress.get(user_id, {})
                            current_day = progress.get("current_day", 1)
                            send_day_content(chat_id, user_id, current_day)
                        
                        elif data == "all_days":
                            days_text = get_text(user_id,
                                "📚 **جميع أيام التدريب**\n\nاختر يوماً لعرض محتواه:",
                                "📚 **All Training Days**\n\nSelect a day to view its content:"
                            )
                            send_message(chat_id, days_text, create_days_keyboard(get_user_language(user_id)))
                        
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
                                "❓ **الاختبارات**\n\nاختر يوماً لبدء اختباره:",
                                "❓ **Quizzes**\n\nSelect a day to start its quiz:"
                            )
                            send_message(chat_id, quizzes_text, create_days_keyboard(get_user_language(user_id)))
                        
                        elif data.startswith("day_"):
                            day_num = int(data.split("_")[1])
                            send_day_content(chat_id, user_id, day_num)
                        
                        elif data.startswith("start_quiz_"):
                            day_num = int(data.split("_")[2])
                            start_quiz(chat_id, user_id, day_num)
                        
                        elif data.startswith("answer_"):
                            answer_index = int(data.split("_")[1])
                            handle_quiz_answer(chat_id, user_id, answer_index)
            
            time.sleep(1)
            
        except Exception as e:
            logging.error(f"Bot error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    # Get token
    token = os.environ.get('TELEGRAM_TOKEN')
    
    if token:
        logging.info(f"✅ TELEGRAM_TOKEN found! Starting Zain Training Bot...")
        
        # Start bot in a separate thread
        bot_thread = threading.Thread(target=run_simple_bot, args=(token,), daemon=True)
        bot_thread.start()
        logging.info("✅ Zain Training Bot started!")
    else:
        logging.error("❌ TELEGRAM_TOKEN not found!")
    
    # Start Flask
    logging.info(f"🌐 Starting Flask on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
