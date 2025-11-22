import os
import logging
import sys
from flask import Flask
import threading
from datetime import datetime, time, timedelta
import time as time_module
import schedule
import requests

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
                "title_ar": "المقدمة",
                "title_en": "Introduction",
                "content_ar": """أهلاً بك في رحلتك نحو الاحتراف في عالم البث الصوتي. هذا البرنامج هو دليلك الشامل الذي سيأخذ بيدك خطوة بخطوة من البداية إلى المستوى المتقدم، مع شرح مفصل لكل مفهوم، وأمثلة عملية، وتمارين تطبيقية ستجعلك مضيفاً محترفاً قادراً على قيادة أي برنامج صوتي بثقة واحترافية.""",
                "content_en": """Welcome to your journey towards professionalism in the world of audio broadcasting. This program is your comprehensive guide that will take you step by step from beginner to advanced level, with detailed explanation of every concept, practical examples, and applied exercises that will make you a professional host capable of leading any audio program with confidence and professionalism."""
            },
            {
                "type": "text",
                "title_ar": "الهدف",
                "title_en": "Objective",
                "content_ar": """فهم قوة الصوت كأداة اتصال، وتطوير مهارة الاستماع كأساس لأي تفاعل ناجح.""",
                "content_en": """Understanding the power of voice as a communication tool, and developing listening skills as the foundation for any successful interaction."""
            },
            {
                "type": "text",
                "title_ar": "المحتوى النظري الموسع",
                "title_en": "Extended Theoretical Content",
                "content_ar": """أنت صانع أجواء:

في العالم الصوتي، أنت المسؤول الوحيد عن صناعة المشاعر وتوجيه الطاقة

صوتك ليس مجرد وسيلة نقل معلومات، بل هو أداة صناعة المشاعر

مثال: عندما تتحدث عن موضوع مفرح، اجعل نبرة صوتك مرتفعة ومليئة بالحيوية
مثال: عندما تقدم موضوعاً جاداً، اخفض نبرة صوتك وأعطِ كل كلمة وزنها

الاستماع النشط ليس سماعاً:
السماع: عملية سلبية تتم دون تركيز
الاستماع: عملية نشطة تتطلب التركيز والفهم والاستجابة الذكية

كيف تستمع بنشاط؟
لا تنتظر دورك للكلام: ركز على ما يقال الآن وليس على ردك القادم
الرد على المشاعر: انتبه لنبرة صوت المتحدث
الأسئلة التوضيحية: مثل هل تقصد أن...؟، ماذا حدث بعد ذلك؟

صناعة هويتك الصوتية:
الثقة: نابعة من إيمانك بقيمتك وما تقدمه
الطاقة: اجعل طاقتك إيجابية ومعدية حتى في الأيام العادية
الأصالة: كن صادقاً في ردودك وتفاعلك، لا تتصنع شخصية غيرك""",
                "content_en": """You Create the Atmosphere:

In the audio world, you are solely responsible for creating emotions and directing energy

Your voice is not just a means of transmitting information, but a tool for creating emotions

Example: When talking about a happy topic, make your tone high and full of vitality
Example: When presenting a serious topic, lower your tone and give each word its weight

Active listening is not just hearing:
Hearing: A passive process without focus
Listening: An active process requiring concentration, understanding, and intelligent response

How to listen actively?
Don't wait for your turn to speak: Focus on what is being said now, not your next response
Respond to emotions: Pay attention to the speaker's tone
Clarifying questions: Like do you mean that...?, What happened next?

Building your vocal identity:
Confidence: Stemming from your belief in your value and what you offer
Energy: Make your energy positive and contagious even on ordinary days
Authenticity: Be honest in your responses and interactions, don't fake another personality"""
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية الفردية",
                "title_en": "Individual Practical Exercises",
                "content_ar": """تمرين التحليل (15 دقيقة): استمع لمضيف مشهور وحلل 3 مواقف استخدم فيها الاستماع النشط
تمرين التسجيل والتحليل الذاتي (30 دقيقة): سجل صوتك وأنت تتحدث عن كتاب أو فيلم، ثم حلل سرعتك، وضوحك، ونبرة صوتك
تمرين الارتجال (15 دقيقة): تحدث عن كلمة عشوائية لمدة 60 ثانية دون توقف""",
                "content_en": """Analysis Exercise (15 minutes): Listen to a famous host and analyze 3 situations where they used active listening
Recording and Self-Analysis Exercise (30 minutes): Record your voice while talking about a book or movie, then analyze your speed, clarity, and tone
Improvisation Exercise (15 minutes): Talk about a random word for 60 seconds without stopping"""
            },
            {
                "type": "text",
                "title_ar": "الأنشطة الجماعية",
                "title_en": "Group Activities",
                "content_ar": """لعبة "همسة السلسلة" (15 دقيقة): لتدريب دقة الاستماع ونقل المعلومة
"المقابلة النشطة" (20 دقيقة): يتدرب المتدربون على الاستماع بهدف الفهم وليس الرد""",
                "content_en": """Chain Whisper Game (15 minutes): To train listening accuracy and information transfer
Active Interview (20 minutes): Trainees practice listening for understanding rather than responding"""
            },
            {
                "type": "text",
                "title_ar": "المهمة اليومية",
                "title_en": "Daily Task",
                "content_ar": """استمع إلى مضيف آخر وحلل طريقته في التعامل مع ضيوفه وجمهوره""",
                "content_en": """Listen to another host and analyze their way of dealing with guests and audience"""
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
                "title_ar": "الهدف",
                "title_en": "Objective",
                "content_ar": """التحكم الفني في صوتك لجعله أداة مرنة وجذابة.""",
                "content_en": """Technical control of your voice to make it a flexible and attractive tool."""
            },
            {
                "type": "text",
                "title_ar": "المحتوى النظري الموسع",
                "title_en": "Extended Theoretical Content",
                "content_ar": """تمارين الإحماء الصوتي (الروتين اليومي):

التنفس الحجابي: تنفس بعمق من الأنف بحيث يتمدد بطنك، وازفر ببطء من الفم

تمرين الشفاه: برّر شفتيك معاً وتحريكهما في كل الاتجاهات

تمرين اللسان: لمس سقف الحلق وتحريك اللسان بشكل دائري

وضوح الكلام هو الاحترافية ذاتها:

ركز على مخارج الحروف، خاصة الحروف التي تحتاج لجهد مثل ق، غ، ظ، ر

تخيل أنك ترمي الكلمات مثل السهام، يجب أن تكون واضحة ومستقيمة

مثال: عند نطق كلمة مستقبل، ركز على كل حرف وخاصة حرف القاف

موسيقى الكلام: كيف تصنع لحناً يجذب الأذن؟

النبرة: التغيير بين العالي والمنخفض يخلق تشويقاً

السرعة: سريعة للإثارة، بطيئة للتأكيد

الوقفات: استخدمها قبل وبعد المعلومات المهمة

لغة الجسد للصوت:

حتى لو لم يراك أحد، فإن ابتسامتك تسمع

تحدث ووجهك يعبر، ويديك تتحركان""",
                "content_en": """Vocal Warm-up Exercises (Daily Routine):

Diaphragmatic breathing: Breathe deeply through your nose so your stomach expands, exhale slowly through your mouth

Lip exercises: Purse your lips together and move them in all directions

Tongue exercises: Touch the roof of your mouth and move your tongue in circles

Speech clarity is professionalism itself:

Focus on letter articulation, especially letters that require effort like Qaf, Ghayn, Dhad, Ra

Imagine throwing words like arrows - they should be clear and straight

Example: When pronouncing the word future, focus on each letter especially the Qaf letter

Speech Music: How to Create a Melody That Attracts the Ear?

Tone: Changing between high and low creates suspense

Speed: Fast for excitement, slow for emphasis

Pauses: Use them before and after important information

Body Language for Voice:

Even if no one sees you, your smile can be heard

Speak with expressive face and moving hands"""
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية الفردية",
                "title_en": "Individual Practical Exercises",
                "content_ar": """تمرين الإحماء (20 دقيقة): التنفس والشفاه واللسان
تمرين التعبير الصوتي (20 دقيقة): اقرأ قصة للأطفال بتعابير مبالغ فيها
تمرين النبرة والسرعة (20 دقيقة): اقرأ خبراً جريدة بطرق مختلفة""",
                "content_en": """Warm-up Exercise (20 minutes): Breathing, lips, and tongue
Vocal Expression Exercise (20 minutes): Read a children's story with exaggerated expressions
Tone and Speed Exercise (20 minutes): Read a newspaper article in different ways"""
            },
            {
                "type": "text",
                "title_ar": "الأنشطة الجماعية",
                "title_en": "Group Activities",
                "content_ar": """الاتحاد الصوتي (دويتو) (25 دقيقة): تقديم فقرة ترحيب بشكل متناغم
مسرح المشاعر (20 دقيقة): قراءة جملة محايدة بمشاعر مختلفة""",
                "content_en": """Vocal Union (Duet) (25 minutes): Present a welcome segment in harmony
Theater of Emotions (20 minutes): Read a neutral sentence with different emotions"""
            },
            {
                "type": "text",
                "title_ar": "المهمة اليومية",
                "title_en": "Daily Task",
                "content_ar": """سجل نفسك تقول جملة "ماذا لو أخبرتك أن كل شيء تعرفه على وشك أن يتغير؟" بثلاث نبرات مختلفة""",
                "content_en": """Record yourself saying the sentence "What if I told you that everything you know is about to change?" in three different tones"""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الثاني: إتقان أدواتك",
            "title_en": "Day 2 Quiz: Mastering Your Tools",
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
                "title_ar": "الهدف",
                "title_en": "Objective",
                "content_ar": """تعلم بناء أي فقرة على هيكل منطقي ومشوق من البداية للنهاية.""",
                "content_en": """Learn to build any segment on a logical and exciting structure from beginning to end."""
            },
            {
                "type": "text",
                "title_ar": "المحتوى النظري الموسع",
                "title_en": "Extended Theoretical Content",
                "content_ar": """المقدمة (الخطاف):

لديك 10-15 ثانية فقط للإمساك بانتباه المستمع

أنواع الخطافات الفعالة:

السؤال الصادم: هل تعلم أن 90% من قراراتنا نتاج العقل الباطن؟

القصة المصغرة: كنت أجري أمس، وفجأة... وقعت!

الإحصائية المدهشة: يُهدر طعام يكفي لإطعام مليار شخص سنوياً

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

Shocking question: Did you know that 90% of our decisions come from the subconscious?

Mini-story: I was running yesterday, and suddenly... I fell!

Amazing statistic: Enough food to feed one billion people is wasted annually

Funny situation: I once tried to cook eggs and the kitchen caught fire!

Content (The Body):

Focus on one main point in each segment

Use stories to make information more attractive

Provide examples and analogies to support your main idea

Example: Instead of describing a boring place, tell a story that happened to you there

Conclusion (The Impactful Closing):

Types of conclusions:

Summary: So, the main idea is...

Call to interaction: What do you think? Write in the chat

Open question: If you had a chance to ask a celebrity, who would you choose?

Hint for the future: In the next episode, we'll reveal the secret of..."""
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية الفردية",
                "title_en": "Individual Practical Exercises",
                "content_ar": """تمرين التخطيط (20 دقيقة): اختر موضوعاً واكتب له خطافاً ونقطة رئيسية وخاتمة
تمرين التسجيل (25 دقيقة): سجل فقرة مصغرة عن كتابك المفضل""",
                "content_en": """Planning Exercise (20 minutes): Choose a topic and write a hook, main point, and conclusion for it
Recording Exercise (25 minutes): Record a mini-segment about your favorite book"""
            },
            {
                "type": "text",
                "title_ar": "الأنشطة الجماعية",
                "title_en": "Group Activities",
                "content_ar": """مصنع الخطافات (20 دقيقة): ابتكار خطافات لمواضيع عادية
التقديم المتناوب (دويتو) (30 دقيقة): تقديم فقرة سفر بشكل متناغم""",
                "content_en": """Hook Factory (20 minutes): Create hooks for ordinary topics
Alternating Presentation (Duet) (30 minutes): Present a travel segment in harmony"""
            },
            {
                "type": "text",
                "title_ar": "المهمة اليومية",
                "title_en": "Daily Task",
                "content_ar": """استمع لبداية برنامجين وحلل نوع الخطاف المستخدم""",
                "content_en": """Listen to the beginning of two programs and analyze the type of hook used"""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الثالث: هيكل الفقرة",
            "title_en": "Day 3 Quiz: Segment Structure",
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
    },
    4: {
        "title_ar": "اليوم الرابع: فقرات الألعاب التنشيطية - كسر الجليد وبناء المجتمعات",
        "title_en": "Day 4: Icebreaker Segments - Breaking Barriers and Building Communities",
        "materials": [
            {
                "type": "text",
                "title_ar": "الهدف",
                "title_en": "Objective",
                "content_ar": """إتقان تقديم الألعاب التي تكسر حاجز الصمت بين المستمعين.""",
                "content_en": """Mastering the presentation of games that break the silence barrier between listeners."""
            },
            {
                "type": "text",
                "title_ar": "المحتوى النظري الموسع",
                "title_en": "Extended Theoretical Content",
                "content_ar": """الفلسفة وراء الألعاب التنشيطية:

الهدف ليس اللعبة نفسها، بل التفاعل الاجتماعي الذي تخلقه

اللعبة مجرد وسيلة لجعل الجمهور يشعر بالراحة والمتعة

مثال: لعبة ماذا ستفعل بمليون دولار تفتح مجالاً للتعارف والإبداع

أنماط الألعاب التنشيطية:

ألعاب التعارف: ما هي القوة الخارقة التي تريدها؟

ألعاب الذكاء السريع: أسئلة معلومات عامة

ألعاب التخمين: تخمين الشخصية، الفيلم، كلمة السر

ألعاب الصور: وصف الصورة دون استخدام كلمات ممنوعة

كيف تقدم لعبة؟ خطوات واضحة:

الخطوة 1: اذكر اسم اللعبة بحماس

الخطوة 2: اشرح القواعد ببساطة ووضوح

الخطوة 3: نفذ اللعبة مع التحفيز والتعليق

الخطوة 4: أنهِ بشكر المشاركين والانتقال السلس

نصائح ذهبية للنجاح:

التحكيم بمرح وليس بقسوة

إدارة الوقت والمحافظة على وتيرة البرنامج

الحفاظ على طاقة عالية طوال الوقت""",
                "content_en": """The Philosophy Behind Icebreaker Games:

The goal is not the game itself, but the social interaction it creates

The game is just a means to make the audience feel comfortable and have fun

Example: What would you do with a million dollars game opens opportunities for networking and creativity

Types of Icebreaker Games:

Networking games: What superpower would you want?

Quick intelligence games: General knowledge questions

Guessing games: Guess the character, movie, password

Picture games: Describe the picture without using forbidden words

How to Present a Game? Clear Steps:

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
                "title_ar": "التمارين العملية الفردية",
                "title_en": "Individual Practical Exercises",
                "content_ar": """تمرين شرح القواعد (20 دقيقة): اشرح قواعد لعبتين في 30 ثانية لكل منهما
تمرين التقديم الكامل (30 دقيقة): سجل فقرة لعبة كاملة مع متسابقين وهميين""",
                "content_en": """Rules Explanation Exercise (20 minutes): Explain rules of two games in 30 seconds each
Full Presentation Exercise (30 minutes): Record a complete game segment with imaginary contestants"""
            },
            {
                "type": "text",
                "title_ar": "الأنشطة الجماعية",
                "title_en": "Group Activities",
                "content_ar": """تحدي كسر الجليد (25 دقيقة): تصميم ألعاب جديدة وتقديمها
الدويو المرح (30 دقيقة): تقديم لعبة تخمين الشخصية بشكل ثنائي""",
                "content_en": """Icebreaker Challenge (25 minutes): Design new games and present them
Fun Duet (30 minutes): Present Guess the Character game as a duo"""
            },
            {
                "type": "text",
                "title_ar": "المهمة اليومية",
                "title_en": "Daily Task",
                "content_ar": """صمم لعبة تنشيطية جديدة واكتب قوانينها في 5 أسطر""",
                "content_en": """Design a new icebreaker game and write its rules in 5 lines"""
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
                "title_ar": "الهدف",
                "title_en": "Objective",
                "content_ar": """تطوير القدرة على إدارة فقرات سريعة الإيقاع.""",
                "content_en": """Developing the ability to manage fast-paced segments."""
            },
            {
                "type": "text",
                "title_ar": "المحتوى النظري الموسع",
                "title_en": "Extended Theoretical Content",
                "content_ar": """طاقة السرعة وإدارتها:

هذه الفقرات تحتاج لطاقة عالية وتركيز حاد

تنفس بعمق قبل البدء لشحن طاقتك

حافظ على وتيرة سريعة ولكن مع وضوح في الكلام

أنواع ألعاب السرعة:

أسرع إجابة: يطرح السؤال وأول من يرفع يده يفوز

تحدي الـ 10 ثوانٍ: الإجابة 10 ثوانٍ

أغنية وكلمة: معرفة الأغنية أو كلمة مرتبطة بها

أسئلة بنعم أو لا: أسئلة سريعة مباشرة

فن التعليق على الإجابات:

الإجابة الصحيحة: أحسنت!، انطلقت كالصاروخ!

الإجابة الخاطئة: أوه، كادت!، الفكرة قريبة!

نبرة التشويق: استخدم صوتاً مرتفعاً ومتحمساً للإجابات الصحيحة

أدوات التشويق والإثارة:

صوت المؤقت يزيد التوتر

المؤثرات الصوتية مثل جرس للفوز، صفارة للخطأ

الخلفية الموسيقية السريعة""",
                "content_en": """Speed Energy and Management:

These segments require high energy and sharp focus

Breathe deeply before starting to charge your energy

Maintain fast pace but with clarity in speech

Types of Speed Games:

Fastest answer: Question is asked and first to raise hand wins

10-second challenge: Answer must be within 10 seconds

Song and word: Identifying the song or related word

Yes or no questions: Quick direct questions

Art of Commenting on Answers:

Correct answer: Well done!, Took off like a rocket!

Wrong answer: Oh, almost!, The idea is close!

Suspense tone: Use high and excited voice for correct answers

Tools for Suspense and Excitement:

Timer sound increases tension

Sound effects like bell for winning, whistle for wrong

Fast background music"""
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية الفردية",
                "title_en": "Individual Practical Exercises",
                "content_ar": """تمرين الطلاقة والسرعة (20 دقيقة): قراءة أسئلة عامة بسرعة ووضوح
تمرين المحاكاة الكاملة (35 دقيقة): تسجيل فقرة ألعاب سرعة كاملة""",
                "content_en": """Fluency and Speed Exercise (20 minutes): Reading general questions quickly and clearly
Full Simulation Exercise (35 minutes): Recording a complete speed games segment"""
            },
            {
                "type": "text",
                "title_ar": "الأنشطة الجماعية",
                "title_en": "Group Activities",
                "content_ar": """ماراثون الأسئلة الخاطفة (30 دقيقة): منافسة بين فريقين بأسئلة سريعة
ثنائي السرعة (25 دقيقة): تقديم فقرة سرعة بشكل ثنائي منسق""",
                "content_en": """Flash Questions Marathon (30 minutes): Competition between two teams with quick questions
Speed Duet (25 minutes): Presenting a speed segment as a coordinated duo"""
            },
            {
                "type": "text",
                "title_ar": "المهمة اليومية",
                "title_en": "Daily Task",
                "content_ar": """شاهد برنامج ألعاب سريعة وحلل كيف يحافظ المضيف على طاقته""",
                "content_en": """Watch a fast-paced game show and analyze how the host maintains their energy"""
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
}

TRAINING_DATA.update({
    6: {
        "title_ar": "اليوم السادس: الفقرات الثقافية والمعلوماتية - من المعلومة الجافة إلى القصة المشوقة",
        "title_en": "Day 6: Cultural and Informational Segments - From Dry Information to Exciting Stories",
        "materials": [
            {
                "type": "text",
                "title_ar": "الهدف",
                "title_en": "Objective",
                "content_ar": """تحويل المعلومات الجافة إلى محتوى شيق وسهل الفهم.""",
                "content_en": """Transforming dry information into engaging and easy-to-understand content."""
            },
            {
                "type": "text",
                "title_ar": "المحتوى النظري الموسع",
                "title_en": "Extended Theoretical Content",
                "content_ar": """محاربة الملل في تقديم المعلومات:

اروي، لا تخبر: بدلاً من كان الطقس بارداً قل كان الصقيع يتسلل عبر سترتي

اربط المعلومة بحياة المستمع: اجعل المعلومة شخصية ومؤثرة

استخدم التشبيهات: الإنترنت يشبه الطريق السريع للبيانات

تبسيط المعلومات المعقدة:

التشبيه: البلوك تشين يشبه دفتر حسابات موزع

القصص: ابحث عن القصة الإنسانية خلف المعلومة

الأمثلة العملية: شرح النظريات من خلال تطبيقاتها اليومية

مصادر المعلومات ومصداقيتها:

تحقق دائماً من مصدر المعلومة

استخدم مواقع موثوقة ومراجع علمية

ذكر مصدرك يزيد من مصداقيتك

أنماط الفقرات الثقافية:

هل تعلم؟ قصيرة وسريعة

سؤال ثقافي مع مشاركة الجمهور

حكاية من التاريخ بسرد قصصي مشوق""",
                "content_en": """Fighting Boredom in Presenting Information:

Narrate, don't tell: Instead of the weather was cold say the frost was creeping through my jacket

Connect information to the listener's life: Make the information personal and impactful

Use analogies: The internet is like a highway for data

Simplifying Complex Information:

Analogy: Blockchain is like a distributed ledger

Stories: Look for the human story behind the information

Practical examples: Explain theories through their daily applications

Information Sources and Credibility:

Always verify the source of information

Use reliable websites and scientific references

Mentioning your source increases your credibility

Types of Cultural Segments:

Did you know? short and fast

Cultural question with audience participation

Historical tale with exciting storytelling"""
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية الفردية",
                "title_en": "Individual Practical Exercises",
                "content_ar": """تمرين التبسيط (20 دقيقة): اشرح مفهوماً معقداً في 5 أسطر بتشبيه بسيط
تمرين الإعداد والتسجيل (30 دقيقة): سجل فقرة هل تعلم؟ كاملة""",
                "content_en": """Simplification Exercise (20 minutes): Explain a complex concept in 5 lines with a simple analogy
Preparation and Recording Exercise (30 minutes): Record a complete Did you know? segment"""
            },
            {
                "type": "text",
                "title_ar": "الأنشطة الجماعية",
                "title_en": "Group Activities",
                "content_ar": """تحويل المعلومة إلى قصة (30 دقيقة): حول معلومات جافة إلى قصص مشوقة
الحوار الثقافي (دويتو) (25 دقيقة): ناقش موضوعاً ثقافياً بشكل حواري""",
                "content_en": """Transforming Information into Stories (30 minutes): Turn dry information into exciting stories
Cultural Dialogue (Duet) (25 minutes): Discuss a cultural topic in a conversational style"""
            },
            {
                "type": "text",
                "title_ar": "المهمة اليومية",
                "title_en": "Daily Task",
                "content_ar": """ابحث عن حقيقة علمية مدهشة واكتبها في منشور بأسلوب جذاب""",
                "content_en": """Research an amazing scientific fact and write it in an attractive post style"""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم السادس: الفقرات الثقافية",
            "title_en": "Day 6 Quiz: Cultural Segments",
            "questions": [
                {
                    "question_ar": "كيف نحارب الملل في تقديم المعلومات؟",
                    "question_en": "How do we fight boredom in presenting information?",
                    "options_ar": ["باستخدام القصص والتشبيهات", "باستخدام مصطلحات معقدة", "بالتحدث بسرعة", "بعدم الربط بحياة المستمع"],
                    "options_en": ["Using stories and analogies", "Using complex terms", "Speaking quickly", "Not connecting to listener's life"],
                    "correct": 0,
                    "explanation_ar": "استخدام القصص والتشبيهات وربط المعلومات بحياة المستمع يحارب الملل",
                    "explanation_en": "Using stories, analogies and connecting information to the listener's life fights boredom"
                },
                {
                    "question_ar": "لماذا يجب ذكر مصدر المعلومة؟",
                    "question_en": "Why should we mention the source of information?",
                    "options_ar": ["لإطالة الوقت", "لزيادة المصداقية", "لتعقيد المحتوى", "لإرباك المستمع"],
                    "options_en": ["To extend time", "To increase credibility", "To complicate content", "To confuse the listener"],
                    "correct": 1,
                    "explanation_ar": "ذكر المصدر يزيد من مصداقية المضيف ويبني الثقة مع الجمهور",
                    "explanation_en": "Mentioning the source increases the host's credibility and builds trust with the audience"
                }
            ]
        }
    }
})
# =============================================================================
# DAYS 7-15 COMPLETE CONTENT - INSERT AFTER DAY 6
# =============================================================================

TRAINING_DATA.update({
    7: {
        "title_ar": "اليوم السابع: الفقرات التفاعلية - قلب البرنامج النابض",
        "title_en": "Day 7: Interactive Segments - The Beating Heart of the Program",
        "materials": [
            {
                "type": "text",
                "title_ar": "الهدف",
                "title_en": "Objective",
                "content_ar": """تحويل البرنامج من حوار منفرد إلى حوار جماعي.""",
                "content_en": """Transforming the program from a solo dialogue to a collective dialogue."""
            },
            {
                "type": "text",
                "title_ar": "المحتوى النظري الموسع",
                "title_en": "Extended Theoretical Content",
                "content_ar": """استراتيجيات جذب التفاعل:

الأسئلة المفتوحة: ما هو أكثر لحظة أعجبتكم؟ بدلاً من هل أعجبكم البرنامج؟

استطلاعات الرأي: استخدام أدوات التصويت في التطبيقات

الطلب المباشر: شاركونا صور طعامكم!، ما رأيكم في...؟

فن إدارة التعليقات المباشرة:

التعليق الإيجابي: اشكر ورد بالاسم مثل شكراً لك يا أحمد

التعليق السلبي: تعامل بذكاء:

اعترف بالمشكلة

أعد صياغة الملاحظة

رد بطريقة مهذبة

التعليق المسيء: تجاهله أو أخرجه بهدوء

أنماط الفقرات التفاعلية:

الرأي والرأي الآخر: مناقشة قضايا مختلفة الآراء

قصص من حياتكم: مشاركة قصص شخصية

استشارات الجمهور: طلب النصائح والأفكار""",
                "content_en": """Strategies for Attracting Interaction:

Open questions: What was your favorite moment? instead of Did you like the program?

Opinion polls: Using voting tools in applications

Direct request: Share your food photos!, What do you think about...?

Art of Managing Live Comments:

Positive comment: Thank and respond by name like Thank you, Ahmed

Negative comment: Deal with it intelligently:

Acknowledge the problem

Rephrase the note

Respond politely

Offensive comment: Ignore it or remove it calmly

Types of Interactive Segments:

Opinion and Counter-Opinion: Discussing issues with different views

Stories from Your Lives: Sharing personal stories

Audience Consultations: Requesting advice and ideas"""
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية الفردية",
                "title_en": "Individual Practical Exercises",
                "content_ar": """تمرين صياغة الأسئلة (25 دقيقة): اكتب أسئلة مفتوحة لمواضيع مختلفة
تمرين إدارة الأزمات (30 دقيقة): تدرب على الرد على تعليقات صعبة""",
                "content_en": """Question Formulation Exercise (25 minutes): Write open questions for different topics
Crisis Management Exercise (30 minutes): Practice responding to difficult comments"""
            },
            {
                "type": "text",
                "title_ar": "الأنشطة الجماعية",
                "title_en": "Group Activities",
                "content_ar": """محاكاة البث المباشر (40 دقيقة): إدارة تعليقات حية من الجمهور
ثنائي التفاعل (30 دقيقة): إدارة التفاعل بشكل ثنائي منسق""",
                "content_en": """Live Broadcast Simulation (40 minutes): Manage live comments from the audience
Interactive Duet (30 minutes): Manage interaction as a coordinated duo"""
            },
            {
                "type": "text",
                "title_ar": "المهمة اليومية",
                "title_en": "Daily Task",
                "content_ar": """ادخل إلى بث مباشر وحلل طريقة تفاعل المضيف مع التعليقات""",
                "content_en": """Enter a live broadcast and analyze how the host interacts with comments"""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم السابع: الفقرات التفاعلية",
            "title_en": "Day 7 Quiz: Interactive Segments",
            "questions": [
                {
                    "question_ar": "ما هي أفضل أنواع الأسئلة لجذب التفاعل؟",
                    "question_en": "What are the best types of questions to attract interaction?",
                    "options_ar": ["الأسئلة المغلقة", "الأسئلة المفتوحة", "الأسئلة المعقدة", "الأسئلة الطويلة"],
                    "options_en": ["Closed questions", "Open questions", "Complex questions", "Long questions"],
                    "correct": 1,
                    "explanation_ar": "الأسئلة المفتوحة تشجع على التفاعل والمشاركة أكثر من الأسئلة المغلقة",
                    "explanation_en": "Open questions encourage more interaction and participation than closed questions"
                },
                {
                    "question_ar": "كيف تتعامل مع التعليق السلبي؟",
                    "question_en": "How do you handle a negative comment?",
                    "options_ar": ["بالتجاهل التام", "بالصراخ", "بالتعامل بذكاء والاعتراف بالمشكلة", "بحذف التعليق فوراً"],
                    "options_en": ["Complete ignoring", "Shouting", "Dealing intelligently and acknowledging the problem", "Deleting the comment immediately"],
                    "correct": 2,
                    "explanation_ar": "التعامل الذكي مع التعليقات السلبية يشمل الاعتراف بالمشكلة والرد المهذب",
                    "explanation_en": "Intelligent handling of negative comments includes acknowledging the problem and polite response"
                }
            ]
        }
    },
    8: {
        "title_ar": "اليوم الثامن: فن الارتجال - عندما تفاجئك الأقدار",
        "title_en": "Day 8: The Art of Improvisation - When Destiny Surprises You",
        "materials": [
            {
                "type": "text",
                "title_ar": "الهدف",
                "title_en": "Objective",
                "content_ar": """التعامل مع المواقف الطارئة ببرودة الأعصاب والذكاء.""",
                "content_en": """Dealing with emergency situations with cool nerves and intelligence."""
            },
            {
                "type": "text",
                "title_ar": "المحتوى النظري الموسع",
                "title_en": "Extended Theoretical Content",
                "content_ar": """حقيقة الارتجال:

الارتجال الحقيقي هو تحضير مسبق للأدوات وليس للنص

جهز طقم النجاة قبل أن تحتاجه

المواقف الطارئة الشائعة:

صمت مطبق: ضيف لا يتكلم أو عدم تفاعل

مشاكل تقنية: انقطاع الإنترنت، صوت غير واضح

تفاعل ضعيف: لا أحد يشارك

تعليقات محرجة: أسئلة أو ملاحظات غير متوقعة

أدوات الارتجال (طوق النجاة):

الفكاهة: اضحك على الموقف مثل يبدو أن الإنترنت قرر أخذ استراحة!

الاعتراف البسيط: أعتذر، ظهري انقطع للحظة!

العودة لنقطة سابقة: هذا يذكرني بما كنا نتحدث عنه...

الجعبة السرية: 3 قصص شخصية + 5 أسئلة عامة""",
                "content_en": """The Truth About Improvisation:

Real improvisation is preparing tools in advance, not the script

Prepare your survival kit before you need it

Common Emergency Situations:

Complete silence: Guest doesn't speak or no interaction

Technical problems: Internet disconnection, unclear sound

Weak interaction: No one participates

Embarrassing comments: Unexpected questions or remarks

Improvisation Tools (Lifebuoy):

Humor: Laugh at the situation like Looks like the internet decided to take a break!

Simple acknowledgment: I apologize, my connection dropped for a moment!

Return to previous point: This reminds me of what we were talking about...

Secret kit: 3 personal stories + 5 general questions"""
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية الفردية",
                "title_en": "Individual Practical Exercises",
                "content_ar": """تمرين الجعبة السرية (20 دقيقة): اكتب 3 قصص و5 أسئلة عامة واحفظهم
تمرين لعب الأدوار (30 دقيقة): تمثيل مواقف طارئة والتدرب على حلها""",
                "content_en": """Secret Kit Exercise (20 minutes): Write 3 stories and 5 general questions and memorize them
Role-playing Exercise (30 minutes): Act out emergency situations and practice solving them"""
            },
            {
                "type": "text",
                "title_ar": "الأنشطة الجماعية",
                "title_en": "Group Activities",
                "content_ar": """ساحة الارتجال (45 دقيقة): مواقف طارئة عشوائية وحلول فورية
إنقاذ الشريك (دويتو) (30 دقيقة): تدخل لإنقاذ الشريك في موقف صعب""",
                "content_en": """Improvisation Arena (45 minutes): Random emergency situations and instant solutions
Partner Rescue (Duet) (30 minutes): Intervene to rescue your partner in a difficult situation"""
            },
            {
                "type": "text",
                "title_ar": "المهمة اليومية",
                "title_en": "Daily Task",
                "content_ar": """فكر في موقف طارئ حدث معك وكيف كان يمكن تحسين تعاملك""",
                "content_en": """Think about an emergency situation that happened to you and how you could have improved your handling of it"""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الثامن: فن الارتجال",
            "title_en": "Day 8 Quiz: The Art of Improvisation",
            "questions": [
                {
                    "question_ar": "ما هي حقيقة الارتجال الناجح؟",
                    "question_en": "What is the truth about successful improvisation?",
                    "options_ar": ["عدم التحضير مطلقاً", "التحضير المسبق للأدوات", "الحفظ عن ظهر قلب", "تجنب المواقف الصعبة"],
                    "options_en": ["Never preparing", "Preparing tools in advance", "Memorizing by heart", "Avoiding difficult situations"],
                    "correct": 1,
                    "explanation_ar": "الارتجال الناجح يعتمد على التحضير المسبق للأدوات والموارد وليس على الحظ",
                    "explanation_en": "Successful improvisation depends on preparing tools and resources in advance, not on luck"
                },
                {
                    "question_ar": "ما هي إحدى أدوات الارتجال؟",
                    "question_en": "What is one of the improvisation tools?",
                    "options_ar": ["الصمت الدائم", "الفكاهة والضحك على الموقف", "إنهاء البرنامج فوراً", "إلقاء اللوم على الآخرين"],
                    "options_en": ["Permanent silence", "Humor and laughing at the situation", "Ending the program immediately", "Blaming others"],
                    "correct": 1,
                    "explanation_ar": "الفكاهة أداة فعالة للتعامل مع المواقف الطارئة بطريقة إيجابية",
                    "explanation_en": "Humor is an effective tool for dealing with emergency situations in a positive way"
                }
            ]
        }
    },
    9: {
        "title_ar": "اليوم التاسع: فن إدارة الحوار مع الضيوف - أنت قائد الأوركسترا",
        "title_en": "Day 9: The Art of Managing Dialogue with Guests - You are the Orchestra Conductor",
        "materials": [
            {
                "type": "text",
                "title_ar": "الهدف",
                "title_en": "Objective",
                "content_ar": """استضافة الضيوف واستخراج أفضل ما لديهم.""",
                "content_en": """Hosting guests and extracting the best from them."""
            },
            {
                "type": "text",
                "title_ar": "المحتوى النظري الموسع",
                "title_en": "Extended Theoretical Content",
                "content_ar": """التحضير قبل البرنامج:

البحث عن الضيف: اقرأ عنه، شاهد مقابلات سابقة

تحديد الهدف: ما الرسالة الرئيسية من المقابلة؟

إعداد النقاط الرئيسية: 5-7 نقاط وليس نصاً كاملاً

الاتصال بالضيف: تعريفه بنمط البرنامج والنقاط الرئيسية

فن صياغة الأسئلة:

الأسئلة المفتوحة: كيف كانت رحلتك؟، ما الذي دفعك لهذا القرار؟

أسئلة المشاعر: كيف شعرت في تلك اللحظة؟

الأسئلة المتتابعة: ابنِ على إجابات الضيف

دورك كقائد أوركسترا:

لا تكن النجم: سلط الضوء على الضيف لا على نفسك

الاستماع ثم الكلام: الاستماع الجيد يولد أسئلة أفضل

إدارة الوقت: أنهِ الحوار بلباقة عندما يحين الموعد""",
                "content_en": """Preparation Before the Program:

Research the guest: Read about them, watch previous interviews

Define the goal: What is the main message from the interview?

Prepare main points: 5-7 points, not a full script

Contact the guest: Introduce them to the program style and main points

Art of Formulating Questions:

Open questions: How was your journey?, What prompted this decision?

Emotion questions: How did you feel at that moment?

Follow-up questions: Build on the guest's answers

Your Role as Orchestra Conductor:

Don't be the star: Spotlight the guest, not yourself

Listen then speak: Good listening generates better questions

Time management: End the dialogue politely when time comes"""
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية الفردية",
                "title_en": "Individual Practical Exercises",
                "content_ar": """تمرين البحث (25 دقيقة): ابحث عن شخصية مشهورة واكتب 5 أسئلة لها
تمرين المقابلة (50 دقيقة): أجرِ مقابلة مع صديق كضيف""",
                "content_en": """Research Exercise (25 minutes): Research a famous personality and write 5 questions for them
Interview Exercise (50 minutes): Conduct an interview with a friend as a guest"""
            },
            {
                "type": "text",
                "title_ar": "الأنشطة الجماعية",
                "title_en": "Group Activities",
                "content_ar": """مقابلة الخبير (40 دقيقة): مقابلة ثنائية مع ضيف خبير
تحليل المقابلة (30 دقيقة): تحليل مقابلة تلفزيونية مشهورة""",
                "content_en": """Expert Interview (40 minutes): Duo interview with expert guest
Interview Analysis (30 minutes): Analyze a famous television interview"""
            },
            {
                "type": "text",
                "title_ar": "المهمة اليومية",
                "title_en": "Daily Task",
                "content_ar": """شاهد مقابلة وحلل أسلوب المضيف في إدارة الحوار""",
                "content_en": """Watch an interview and analyze the host's style in managing the dialogue"""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم التاسع: إدارة الحوار مع الضيوف",
            "title_en": "Day 9 Quiz: Managing Dialogue with Guests",
            "questions": [
                {
                    "question_ar": "ما هو دور المضيف في الحوار مع الضيوف؟",
                    "question_en": "What is the host's role in dialogue with guests?",
                    "options_ar": ["أن يكون النجم الرئيسي", "تسليط الضوء على الضيف", "التحدث أكثر من الضيف", "عدم الاستماع للضيف"],
                    "options_en": ["Being the main star", "Spotlighting the guest", "Talking more than the guest", "Not listening to the guest"],
                    "correct": 1,
                    "explanation_ar": "دور المضيف هو تسليط الضوء على الضيف وإدارة الحوار وليس أن يكون النجم الرئيسي",
                    "explanation_en": "The host's role is to spotlight the guest and manage the dialogue, not to be the main star"
                },
                {
                    "question_ar": "كم نقطة رئيسية يجب إعدادها للمقابلة؟",
                    "question_en": "How many main points should be prepared for the interview?",
                    "options_ar": ["10-15 نقطة", "5-7 نقاط", "نقطة واحدة فقط", "لا داعي للإعداد"],
                    "options_en": ["10-15 points", "5-7 points", "Only one point", "No need for preparation"],
                    "correct": 1,
                    "explanation_ar": "5-7 نقاط رئيسية تكفي لتوجيه الحوار دون التقيد بنص جامد",
                    "explanation_en": "5-7 main points are sufficient to guide the dialogue without being tied to a rigid script"
                }
            ]
        }
    },
    10: {
        "title_ar": "اليوم العاشر: بناء البرنامج - من الفكرة إلى الخطة التنفيذية",
        "title_en": "Day 10: Program Building - From Idea to Executive Plan",
        "materials": [
            {
                "type": "text",
                "title_ar": "الهدف",
                "title_en": "Objective",
                "content_ar": """الانتقال من فقرات منفصلة إلى برنامج متكامل.""",
                "content_en": """Transitioning from separate segments to an integrated program."""
            },
            {
                "type": "text",
                "title_ar": "المحتوى النظري الموسع",
                "title_en": "Extended Theoretical Content",
                "content_ar": """هندسة البرنامج:

الفكرة: ماذا تقدم؟ مثل ترفيه، تعليم، إلهام

الجمهور: لمن تقدمه؟ مثل شباب، عائلات، متخصصون

الهدف: لماذا تقدمه؟ مثل تسلية، معرفة، مجتمع

الروتين التحضيري:

البحث وجمع المعلومات

كتابة النقاط الرئيسية

التحضير للفقرات

الاختبار التقني

الإعلان المسبق

السكريبت المرن:

ليس نصاً تقرأه، بل خارطة طريق

مثال:

0:00-0:02: مقدمة + خطاف

0:02-0:05: ترحيب + تفاعل

0:05-0:15: لعبة رئيسية

0:15-0:25: مقابلة ضيف

0:25-0:29: تفاعل جمهور

0:29-0:30: خاتمة

صناعة الهوية:

اسم البرنامج وشعاره

الموسيقى المميزة

طريقة الترحيب الخاصة""",
                "content_en": """Program Engineering:

Idea: What do you offer? Like entertainment, education, inspiration

Audience: Who do you offer it to? Like youth, families, specialists

Goal: Why do you offer it? Like entertainment, knowledge, community

Preparation Routine:

Research and information gathering

Writing main points

Preparing segments

Technical testing

Advance announcement

Flexible Script:

Not a text you read, but a road map

Example:

0:00-0:02: Introduction + hook

0:02-0:05: Welcome + interaction

0:05-0:15: Main game

0:15-0:25: Guest interview

0:25-0:29: Audience interaction

0:29-0:30: Conclusion

Identity Creation:

Program name and logo

Distinctive music

Special welcome method"""
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية الفردية",
                "title_en": "Individual Practical Exercises",
                "content_ar": """تمرين التصميم (45 دقيقة): صمم برنامجك المثالي كاملاً""",
                "content_en": """Design Exercise (45 minutes): Design your ideal program completely"""
            },
            {
                "type": "text",
                "title_ar": "الأنشطة الجماعية",
                "title_en": "Group Activities",
                "content_ar": """غرفة التخطيط الإبداعي (50 دقيقة): تصميم برامج جديدة في مجموعات
تقديم الهوية (دويتو) (35 دقيقة): تقديم البرنامج بشكل ثنائي""",
                "content_en": """Creative Planning Room (50 minutes): Design new programs in groups
Identity Presentation (Duet) (35 minutes): Present the program as a duo"""
            },
            {
                "type": "text",
                "title_ar": "المهمة اليومية",
                "title_en": "Daily Task",
                "content_ar": """اكتب رابطة البرنامج كاملة بجميع تفاصيل الفقرات""",
                "content_en": """Write the complete program script with all segment details"""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم العاشر: بناء البرنامج",
            "title_en": "Day 10 Quiz: Program Building",
            "questions": [
                {
                    "question_ar": "ما هو السكريبت المرن؟",
                    "question_en": "What is a flexible script?",
                    "options_ar": ["نص جامد للحفظ", "خارطة طريق مرنة", "قائمة بالكلمات", "رسالة بريد إلكتروني"],
                    "options_en": ["Rigid text for memorization", "Flexible road map", "Word list", "Email message"],
                    "correct": 1,
                    "explanation_ar": "السكريبت المرن هو خارطة طريق تساعد في التنقل بين فقرات البرنامج وليس نصاً جامداً",
                    "explanation_en": "A flexible script is a road map that helps navigate between program segments, not a rigid text"
                },
                {
                    "question_ar": "ما هي عناصر هندسة البرنامج؟",
                    "question_en": "What are the elements of program engineering?",
                    "options_ar": ["الفكرة والجمهور والهدف", "الموسيقى فقط", "الألوان والتصميم", "الصوت فقط"],
                    "options_en": ["Idea, audience, and goal", "Music only", "Colors and design", "Sound only"],
                    "correct": 0,
                    "explanation_ar": "هندسة البرنامج تشمل الفكرة (المحتوى)، الجمهور (المستهدف)، والهدف (الغاية)",
                    "explanation_en": "Program engineering includes the idea (content), audience (target), and goal (purpose)"
                }
            ]
        }
    },
    11: {
        "title_ar": "اليوم الحادي عشر: الإخراج الصوتي - اللمسات الأخيرة الاحترافية",
        "title_en": "Day 11: Audio Production - Professional Final Touches",
        "materials": [
            {
                "type": "text",
                "title_ar": "الهدف",
                "title_en": "Objective",
                "content_ar": """استخدام الموسيقى والمؤثرات لتحسين جودة البرنامج.""",
                "content_en": """Using music and effects to improve program quality."""
            },
            {
                "type": "text",
                "title_ar": "المحتوى النظري الموسع",
                "title_en": "Extended Theoretical Content",
                "content_ar": """الموسيقى والمؤثرات الصوتية:

الملح وليس الطبق الرئيسي: الإفراط يفسد التجربة

المقدمة والخاتمة: موسيقى مميزة وقصيرة

الانتقالات: موسيقى خفيفة بين الفقرات

اختيار الموسيقى المناسبة:

البرامج المرحة: موسيقى سريعة وإيقاعية

البرامج الجادة: موسيقى هادئة أو بدون موسيقى

المصادر: استخدم موسيقى خالية من الحقوق

معالجة الصوت الأساسية:

إزالة الضوضاء: تزيل همسة الميكروفون

معادلة الصوت: تحسين الوضوح

الضغط: توحيد مستوى الصوت""",
                "content_en": """Music and Sound Effects:

The salt, not the main dish: Excess spoils the experience

Introduction and conclusion: Distinctive and short music

Transitions: Light music between segments

Choosing Appropriate Music:

Fun programs: Fast and rhythmic music

Serious programs: Calm music or no music

Sources: Use royalty-free music

Basic Audio Processing:

Noise removal: Removes microphone hiss

Equalization: Improves clarity

Compression: Unifies volume level"""
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية الفردية",
                "title_en": "Individual Practical Exercises",
                "content_ar": """تمرين المونتاج البسيط (50 دقيقة): دمج الصوت مع الموسيقى ومعالجة الصوت""",
                "content_en": """Simple Editing Exercise (50 minutes): Merge sound with music and process audio"""
            },
            {
                "type": "text",
                "title_ar": "الأنشطة الجماعية",
                "title_en": "Group Activities",
                "content_ar": """تحدي المونتاج السريع (40 دقيقة): مونتاج مقدمة برنامج في وقت محدد
ثنائي الصوت (30 دقيقة): تحقيق تناغم صوتي بين مقدمين""",
                "content_en": """Quick Editing Challenge (40 minutes): Edit a program introduction within a set time
Sound Duet (30 minutes): Achieve vocal harmony between two presenters"""
            },
            {
                "type": "text",
                "title_ar": "المهمة اليومية",
                "title_en": "Daily Task",
                "content_ar": """أنشئ 3 مقاطع صوتية للبرنامج (مقدمة، خاتمة، انتقالات)""",
                "content_en": """Create 3 audio clips for the program (introduction, conclusion, transitions)"""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الحادي عشر: الإخراج الصوتي",
            "title_en": "Day 11 Quiz: Audio Production",
            "questions": [
                {
                    "question_ar": "ما دور الموسيقى في البرنامج الصوتي؟",
                    "question_en": "What is the role of music in audio programs?",
                    "options_ar": ["الطبق الرئيسي", "الملح الذي يضيف نكهة", "إزالة الصوت الأساسي", "إطالة مدة البرنامج"],
                    "options_en": ["The main dish", "The salt that adds flavor", "Removing the main sound", "Extending program duration"],
                    "correct": 1,
                    "explanation_ar": "الموسيقى هي مثل الملح الذي يضيف نكهة ولا يجب أن تطغى على المحتوى الرئيسي",
                    "explanation_en": "Music is like salt that adds flavor and should not overwhelm the main content"
                },
                {
                    "question_ar": "ما هي معالجة الصوت الأساسية؟",
                    "question_en": "What is basic audio processing?",
                    "options_ar": ["إزالة الضوضاء والمعادلة والضغط", "تسجيل الصوت فقط", "إضافة المؤثرات فقط", "رفع الصوت فقط"],
                    "options_en": ["Noise removal, equalization, and compression", "Only recording sound", "Only adding effects", "Only increasing volume"],
                    "correct": 0,
                    "explanation_ar": "المعالجة الأساسية تشمل إزالة الضوضاء، معادلة الصوت، وضغط مستوى الصوت",
                    "explanation_en": "Basic processing includes noise removal, sound equalization, and volume compression"
                }
            ]
        }
    },
    12: {
        "title_ar": "اليوم الثاني عشر: فنون التقديم المتقدمة - لمسة العبقرية",
        "title_en": "Day 12: Advanced Presentation Arts - The Touch of Genius",
        "materials": [
            {
                "type": "text",
                "title_ar": "الهدف",
                "title_en": "Objective",
                "content_ar": """تطوير مهارات متقدمة تميزك عن غيرك.""",
                "content_en": """Developing advanced skills that distinguish you from others."""
            },
            {
                "type": "text",
                "title_ar": "المحتوى النظري الموسع",
                "title_en": "Extended Theoretical Content",
                "content_ar": """الستوري تيلينغ (فن سرد القصة):

الهيكل الذهبي:

البداية: الشخصية في سياقها العادي

الحدث المحفز: شيء يغير كل شيء

الرحلة والصراع: التحديات

الذروة: لحظة الحسم

النهاية: التغيير والدرس

الدعابة الذكية:

اضحك على نفسك لا على الآخرين

المفارقة: هدفي كان رياضياً محترفاً ولكن الأريكة كانت أقوى!

المراقبة: التعليق على مواقف الحياة اليومية

التوقيت الكوميدي:

الوقفة قبل النكتة: تزيد التشويق

الوقفة بعد النكتة: تعطي وقتاً للضحك

الإيقاع: التناوب بين السرعة والبطء""",
                "content_en": """Storytelling (The Art of Narration):

The Golden Structure:

Beginning: The character in their normal context

Triggering event: Something that changes everything

Journey and conflict: The challenges

Climax: The moment of decision

End: The change and lesson

Smart Humor:

Laugh at yourself, not at others

Irony: My goal was to be a professional athlete but the couch was stronger!

Observation: Commenting on daily life situations

Comedic Timing:

Pause before the joke: Increases suspense

Pause after the joke: Gives time to laugh

Rhythm: Alternating between speed and slowness"""
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية الفردية",
                "title_en": "Individual Practical Exercises",
                "content_ar": """تمرين سرد القصة (25 دقيقة): احكِ قصة من طفولتك بهيكل ذهبي
تمرين الدعابة (25 دقيقة): حول عادة غريبة لقصة مضحكة""",
                "content_en": """Storytelling Exercise (25 minutes): Tell a story from your childhood with a golden structure
Humor Exercise (25 minutes): Turn a strange habit into a funny story"""
            },
            {
                "type": "text",
                "title_ar": "الأنشطة الجماعية",
                "title_en": "Group Activities",
                "content_ar": """مسابقة سرد القصص (40 دقيقة): سرد قصص عن صور عشوائية
الحوار الكوميدي (دويتو) (35 دقيقة): مناقشة مواضيع يومية بشكل فكاهي""",
                "content_en": """Storytelling Competition (40 minutes): Tell stories about random pictures
Comedic Dialogue (Duet) (35 minutes): Discuss daily topics in a humorous way"""
            },
            {
                "type": "text",
                "title_ar": "المهمة اليومية",
                "title_en": "Daily Task",
                "content_ar": """أعد صياغة قصة إخبارية كقصة مشوقة""",
                "content_en": """Rewrite a news story as an exciting story"""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الثاني عشر: التقديم المتقدم",
            "title_en": "Day 12 Quiz: Advanced Presentation",
            "questions": [
                {
                    "question_ar": "ما هو الهيكل الذهبي لسرد القصة؟",
                    "question_en": "What is the golden structure of storytelling?",
                    "options_ar": ["البداية والنهاية فقط", "البداية، الوسط، النهاية", "الهيكل الذهبي المكون من 5 أجزاء", "لا يوجد هيكل محدد"],
                    "options_en": ["Beginning and end only", "Beginning, middle, end", "The 5-part golden structure", "No specific structure"],
                    "correct": 2,
                    "explanation_ar": "الهيكل الذهبي لسرد القصة يتكون من 5 أجزاء: البداية، الحدث المحفز، الرحلة، الذروة، النهاية",
                    "explanation_en": "The golden structure of storytelling consists of 5 parts: beginning, triggering event, journey, climax, end"
                },
                {
                    "question_ar": "ما هي الدعابة الذكية؟",
                    "question_en": "What is smart humor?",
                    "options_ar": ["الضحك على الآخرين", "الضحك على النفس", "السخرية من الجميع", "عدم استخدام الدعابة"],
                    "options_en": ["Laughing at others", "Laughing at oneself", "Mocking everyone", "Not using humor"],
                    "correct": 1,
                    "explanation_ar": "الدعابة الذكية تعني الضحك على النفس والتعليق على مواقف الحياة اليومية بشكل إيجابي",
                    "explanation_en": "Smart humor means laughing at oneself and commenting on daily life situations in a positive way"
                }
            ]
        }
    },
    13: {
        "title_ar": "اليوم الثالث عشر: فهم جمهورك - من مستمع إلى مشجع",
        "title_en": "Day 13: Understanding Your Audience - From Listener to Fan",
        "materials": [
            {
                "type": "text",
                "title_ar": "الهدف",
                "title_en": "Objective",
                "content_ar": """فهم الجمهور وبناء مجتمع مخلص.""",
                "content_en": """Understanding the audience and building a loyal community."""
            },
            {
                "type": "text",
                "title_ar": "المحتوى النظري الموسع",
                "title_en": "Extended Theoretical Content",
                "content_ar": """أنماط الشخصيات في الجمهور:

المتفاعل: يعلق ويسأل باستمرار

المشجع: حاضر دائماً ونادر التفاعل

الناقد: يرى الأخطاء فقط

الخجول: يستمع فقط

بناء المجتمع:

التكرار: المواظبة على الموعد تخلق عادة

التفاعل الشخصي: مناداتهم بالأسماء

تلبية الرغبات: تخصيص فقرات بناء على طلباتهم

جمع التغذية الراجعة:

الاستبيانات السريعة

الأسئلة المباشرة

مراقبة نوعية التفاعل""",
                "content_en": """Personality Types in the Audience:

Interactive: Constantly comments and asks questions

Supporter: Always present but rarely interacts

Critic: Only sees mistakes

Shy: Only listens

Building Community:

Repetition: Consistency with timing creates habits

Personal interaction: Calling them by names

Fulfilling desires: Customizing segments based on their requests

Collecting Feedback:

Quick surveys

Direct questions

Monitoring interaction quality"""
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية الفردية",
                "title_en": "Individual Practical Exercises",
                "content_ar": """تمرين التحليل (25 دقيقة): تصنيف المتفاعلين في بث مباشر
تمرين التصميم (25 دقيقة): تصميم استبيان إلكتروني بسيط""",
                "content_en": """Analysis Exercise (25 minutes): Classify interactors in a live broadcast
Design Exercise (25 minutes): Design a simple electronic survey"""
            },
            {
                "type": "text",
                "title_ar": "الأنشطة الجماعية",
                "title_en": "Group Activities",
                "content_ar": """إنشاء شخصية المشجع المثالي (45 دقيقة): تجسيد الجمهور المستهدف
استراتيجية بناء المجتمع (دويتو) (30 دقيقة): تخطيط لبناء مجتمع""",
                "content_en": """Creating the Ideal Fan Persona (45 minutes): Embody the target audience
Community Building Strategy (Duet) (30 minutes): Planning to build a community"""
            },
            {
                "type": "text",
                "title_ar": "المهمة اليومية",
                "title_en": "Daily Task",
                "content_ar": """اكتب منشوراً يطلب أفكاراً للفقرات من المتابعين""",
                "content_en": """Write a post requesting segment ideas from followers"""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الثالث عشر: فهم الجمهور",
            "title_en": "Day 13 Quiz: Understanding Audience",
            "questions": [
                {
                    "question_ar": "كيف نبني مجتمعاً مخلصاً حول البرنامج؟",
                    "question_en": "How do we build a loyal community around the program?",
                    "options_ar": ["بالتكرار والتفاعل الشخصي", "بالتجاهل المستمر", "بعدم الرد على التعليقات", "باستخدام مصطلحات معقدة"],
                    "options_en": ["Through repetition and personal interaction", "Through constant ignoring", "By not responding to comments", "By using complex terms"],
                    "correct": 0,
                    "explanation_ar": "بناء المجتمع المخلص يتم من خلال التكرار في المواعيد والتفاعل الشخصي مع الجمهور",
                    "explanation_en": "Building a loyal community happens through timing consistency and personal interaction with the audience"
                },
                {
                    "question_ar": "ما هي احتياجات المشجع في الجمهور؟",
                    "question_en": "What are the needs of the supporter in the audience?",
                    "options_ar": ["التقدير المستمر", "الشعور بالانتماء", "النقد الدائم", "التجاهل"],
                    "options_en": ["Constant appreciation", "Feeling of belonging", "Constant criticism", "Ignoring"],
                    "correct": 1,
                    "explanation_ar": "المشجع يحتاج للشعور بالانتماء للمجتمع والبرنامج",
                    "explanation_en": "The supporter needs to feel a sense of belonging to the community and program"
                }
            ]
        }
    },
    14: {
        "title_ar": "اليوم الرابع عشر: التطبيق الشامل - بروفة الإخراج النهائي",
        "title_en": "Day 14: Comprehensive Application - Final Rehearsal",
        "materials": [
            {
                "type": "text",
                "title_ar": "الهدف",
                "title_en": "Objective",
                "content_ar": """دمج كل المهارات في برنامج كامل.""",
                "content_en": """Integrating all skills into a complete program."""
            },
            {
                "type": "text",
                "title_ar": "المحتوى النظري الموسع",
                "title_en": "Extended Theoretical Content",
                "content_ar": """فنون الربط:

اللفظي: والحديث عن السفر يحضرني لعبة عن دول العالم

الصوتي: استخدام موسيقى انتقالية

المنطقي: بعد كل هذا المرح، حان وقت الاستراحة بمعلومة مدهشة""",
                "content_en": """Arts of Connection:

Verbal: And talking about travel brings me to a game about world countries

Audio: Using transition music

Logical: After all this fun, it's time for a break with an amazing fact"""
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية الفردية",
                "title_en": "Individual Practical Exercises",
                "content_ar": """التدريب النهائي الكبير (70 دقيقة): تسجيل حلقة برنامج كاملة 15-20 دقيقة""",
                "content_en": """Final Comprehensive Training (70 minutes): Record a complete program episode 15-20 minutes"""
            },
            {
                "type": "text",
                "title_ar": "الأنشطة الجماعية",
                "title_en": "Group Activities",
                "content_ar": """البث المباشر الوهمي (90 دقيقة): محاكاة بث حي بفريق كامل""",
                "content_en": """Simulated Live Broadcast (90 minutes): Simulate a live broadcast with a full team"""
            },
            {
                "type": "text",
                "title_ar": "المهمة اليومية",
                "title_en": "Daily Task",
                "content_ar": """سجل الحلقة كاملة وقيم أداءك""",
                "content_en": """Record the complete episode and evaluate your performance"""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الرابع عشر: التطبيق الشامل",
            "title_en": "Day 14 Quiz: Comprehensive Application",
            "questions": [
                {
                    "question_ar": "ما هو الهدف من البروفة النهائية؟",
                    "question_en": "What is the goal of the final rehearsal?",
                    "options_ar": ["إضاعة الوقت", "دمج جميع المهارات", "التوقف عن التعلم", "عدم التحضير"],
                    "options_en": ["Wasting time", "Integrating all skills", "Stopping learning", "Not preparing"],
                    "correct": 1,
                    "explanation_ar": "البروفة النهائية تهدف إلى دمج جميع المهارات المكتسبة وتطبيقها بشكل متكامل",
                    "explanation_en": "The final rehearsal aims to integrate all acquired skills and apply them comprehensively"
                },
                {
                    "question_ar": "ما هي أنواع الربط بين الفقرات؟",
                    "question_en": "What are the types of connection between segments?",
                    "options_ar": ["اللفظي والصوتي والمنطقي", "الصوتي فقط", "البصري فقط", "لا يوجد ربط"],
                    "options_en": ["Verbal, audio, and logical", "Audio only", "Visual only", "No connection"],
                    "correct": 0,
                    "explanation_ar": "الربط بين الفقرات يشمل الربط اللفظي، الصوتي، والمنطقي لتحقيق تدفق سلس",
                    "explanation_en": "Connection between segments includes verbal, audio, and logical connection to achieve smooth flow"
                }
            ]
        }
    },
    15: {
        "title_ar": "اليوم الخامس عشر: التقييم والتطوير المستمر - رحلة لا تتوقف",
        "title_en": "Day 15: Evaluation and Continuous Development - A Journey That Never Stops",
        "materials": [
            {
                "type": "text",
                "title_ar": "الهدف",
                "title_en": "Objective",
                "content_ar": """وضع خطة للتطوير المستمر.""",
                "content_en": """Developing a plan for continuous development."""
            },
            {
                "type": "text",
                "title_ar": "المحتوى النظري الموسع",
                "title_en": "Extended Theoretical Content",
                "content_ar": """التقييم الذاتي الموضوعي:

استمع كجمهور: هل أنت مستمتع؟

استمع كخبير: حلل الوضوح، الطلاقة، التنظيم

خطة التطوير المستمر:

مواكبة الترندات

التعلم المستمر

طلب التغذية الراجعة

الاستدامة:

ضع حدوداً للراحة

تذكر لماذا بدأت

احتفل بالإنجازات""",
                "content_en": """Objective Self-Evaluation:

Listen as an audience: Are you enjoying?

Listen as an expert: Analyze clarity, fluency, organization

Continuous Development Plan:

Keeping up with trends

Continuous learning

Requesting feedback

Sustainability:

Set comfort boundaries

Remember why you started

Celebrate achievements"""
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية الفردية",
                "title_en": "Individual Practical Exercises",
                "content_ar": """تمرين التقييم الذاتي (30 دقيقة): تقييم تسجيل الحلقة الكاملة
تمرين التخطيط الاستراتيجي (30 دقيقة): خطة 90 يوم القادمة""",
                "content_en": """Self-Evaluation Exercise (30 minutes): Evaluate the recording of the complete episode
Strategic Planning Exercise (30 minutes): Plan for the next 90 days"""
            },
            {
                "type": "text",
                "title_ar": "الأنشطة الجماعية",
                "title_en": "Group Activities",
                "content_ar": """حلقة التغذية الراجعة (60 دقيقة): تقديم ملاحظات بناءة
احتفال التخرج (45 دقيقة): مشاركة الخطط المستقبلية""",
                "content_en": """Feedback Circle (60 minutes): Provide constructive feedback
Graduation Celebration (45 minutes): Share future plans"""
            },
            {
                "type": "text",
                "title_ar": "المهمة اليومية",
                "title_en": "Daily Task",
                "content_ar": """اكتب رسالة لنفسك في الماضي""",
                "content_en": """Write a letter to your past self"""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الخامس عشر: التطوير المستمر",
            "title_en": "Day 15 Quiz: Continuous Development",
            "questions": [
                {
                    "question_ar": "ما هو سر النجاح المستمر في مجال الاستضافة الصوتية؟",
                    "question_en": "What is the secret of continuous success in audio hosting?",
                    "options_ar": ["التوقف عن التعلم", "التطوير المستمر", "التكرار دون تجديد", "عدم طلب التغذية الراجعة"],
                    "options_en": ["Stopping learning", "Continuous development", "Repetition without renewal", "Not requesting feedback"],
                    "correct": 1,
                    "explanation_ar": "سر النجاح المستمر هو التطوير المستمر والتعلم الدائم ومواكبة الجديد",
                    "explanation_en": "The secret of continuous success is continuous development, permanent learning, and keeping up with new trends"
                },
                {
                    "question_ar": "لماذا يجب الاحتفال بالإنجازات؟",
                    "question_en": "Why should we celebrate achievements?",
                    "options_ar": ["للتوقف عن العمل", "لتحفيز الاستمرار والتطور", "لإضاعة الوقت", "للتقليل من الإنجازات"],
                    "options_en": ["To stop working", "To motivate continuation and development", "To waste time", "To minimize achievements"],
                    "correct": 1,
                    "explanation_ar": "الاحتفال بالإنجازات يحفز على الاستمرار ويبني الثقة للتطور المستقبلي",
                    "explanation_en": "Celebrating achievements motivates continuation and builds confidence for future development"
                }
            ]
        }
    }
})
# =============================================================================
# USER PROGRESS INITIALIZATION FUNCTION
# =============================================================================

def initialize_user_progress(user_id):
    """Initialize or reset user progress with comprehensive tracking"""
    user_progress[user_id] = {
        "current_day": 1,
        "completed_days": set(),
        "quiz_scores": {},
        "last_activity": datetime.now().isoformat(),
        "streak_count": 0,
        "last_active_date": datetime.now().date().isoformat(),
        "completed_voice_exercises": 0,
        "breathing_sessions_completed": 0,
        "storytelling_skills": 0,
        "total_study_time": 0,
        "achievements_unlocked": []
    }
    
    # Initialize reminder preferences
    user_reminder_preferences[user_id] = {
        "breathing_reminders": True,
        "daily_reminders": True,
        "quiz_reminders": True
    }
    
    # Initialize language to Arabic by default
    user_language[user_id] = 'ar'
    
    logging.info(f"✅ Initialized progress for user {user_id}")

# =============================================================================
# USER PROGRESS TRACKING AND QUIZ STATE MANAGEMENT
# =============================================================================

user_progress = {}
user_language = {}
user_quiz_state = {}
user_reminder_preferences = {}
user_achievements = {}

# Breathing reminder times (6 times daily)
BREATHING_REMINDER_TIMES = [
    time(8, 0),   # 8:00 AM - Morning start
    time(11, 0),  # 11:00 AM - Mid-morning
    time(14, 0),  # 2:00 PM - After lunch
    time(17, 0),  # 5:00 PM - Evening
    time(20, 0),  # 8:00 PM - Night
    time(22, 0)   # 10:00 PM - Before sleep
]

# Achievement system
ACHIEVEMENTS = {
    "early_bird": {
        "name_ar": "طائر الصباح",
        "name_en": "Early Bird", 
        "description_ar": "أكمل 5 أيام متتالية",
        "description_en": "Complete 5 days in a row",
        "icon": "🐦",
        "condition": lambda user_data: user_data.get("streak_count", 0) >= 5
    },
    "quiz_master": {
        "name_ar": "سيد الاختبارات",
        "name_en": "Quiz Master",
        "description_ar": "احصل على 90%+ في 3 اختبارات",
        "description_en": "Score 90%+ on 3 quizzes", 
        "icon": "🏆",
        "condition": lambda user_data: len([score for score in user_data.get("quiz_scores", {}).values() if score >= 0.9]) >= 3
    }
}

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

# Reminder System Class
class ReminderSystem:
    def __init__(self, send_message_func):
        self.send_message = send_message_func
        self.setup_schedule()
    
    def setup_schedule(self):
        """Setup scheduled reminders"""
        for reminder_time in BREATHING_REMINDER_TIMES:
            schedule.every().day.at(reminder_time.strftime("%H:%M")).do(self.send_breathing_reminders)
        logging.info("✅ Scheduled reminders setup completed")
    
    def send_breathing_reminders(self):
        """Send breathing exercise reminders to all users with preferences enabled"""
        logging.info("🔔 Sending breathing reminders...")
        for user_id, preferences in user_reminder_preferences.items():
            if preferences.get("breathing_reminders", True):
                language = user_language.get(user_id, 'ar')
                if language == 'ar':
                    message = "💨 وقت تمرين التنفس!\n\nخذ دقيقة للتنفس بعمق:\n• شهيق من الأنف (4 ثوان)\n• احتفظ بالنفس (4 ثوان)\n• زفير من الفم (6 ثوان)\n\nهذا يحسن جودة صوتك ويهدئ الأعصاب! 🎯"
                else:
                    message = "💨 Breathing Exercise Time!\n\nTake a minute for deep breathing:\n• Inhale through nose (4 seconds)\n• Hold breath (4 seconds)\n• Exhale through mouth (6 seconds)\n\nThis improves your voice quality and calms nerves! 🎯"
                
                try:
                    self.send_message(user_id, message)
                    logging.info(f"✅ Sent breathing reminder to user {user_id}")
                except Exception as e:
                    logging.error(f"❌ Failed to send reminder to {user_id}: {e}")
    
    def run_pending(self):
        """Run pending scheduled tasks"""
        schedule.run_pending()

# Helper functions
def send_breathing_reminder(send_func, user_id):
    """Send immediate breathing exercise"""
    language = user_language.get(user_id, 'ar')
    if language == 'ar':
        message = "💨 **تمرين التنفس العميق**\n\nلتحسين جودة صوتك:\n\n1. 🤲 اجلس مستقيماً\n2. 🌬️ شهيق من الأنف (4 ثوان)\n3. ⏱️ احتفظ بالنفس (4 ثوان)\n4. 🗣️ زفير من الفم (6 ثوان)\n5. 🔁 كرر 5 مرات\n\n🎯 النتيجة: صوت أوضح وطاقة أفضل!"
    else:
        message = "💨 **Deep Breathing Exercise**\n\nTo improve your voice quality:\n\n1. 🤲 Sit straight\n2. 🌬️ Inhale through nose (4 seconds)\n3. ⏱️ Hold breath (4 seconds)\n4. 🗣️ Exhale through mouth (6 seconds)\n5. 🔁 Repeat 5 times\n\n🎯 Result: Clearer voice and better energy!"
    
    send_func(user_id, message)
    
    # Track completion
    if user_id in user_progress:
        user_progress[user_id]["breathing_sessions_completed"] = user_progress[user_id].get("breathing_sessions_completed", 0) + 1

def format_progress_dashboard(user_id, language):
    """Format user progress dashboard"""
    progress = user_progress.get(user_id, {})
    current_day = progress.get("current_day", 1)
    completed_days = len(progress.get("completed_days", set()))
    total_days = 15
    
    if language == 'ar':
        dashboard = f"""📊 **لوحة التقدم الشخصي**

🎯 **التقدم العام:**
• اليوم الحالي: {current_day}/{total_days}
• الأيام المكتملة: {completed_days}/{total_days}
• نسبة الإنجاز: {(completed_days/total_days)*100:.1f}%

🏆 **الإنجازات:**
• تمارين الصوت المكتملة: {progress.get('completed_voice_exercises', 0)}
• جلسات التنفس: {progress.get('breathing_sessions_completed', 0)}
• مهارات سرد القصص: {progress.get('storytelling_skills', 0)}%

💪 **استمر في التقدم!**"""
    else:
        dashboard = f"""📊 **Personal Progress Dashboard**

🎯 **Overall Progress:**
• Current Day: {current_day}/{total_days}
• Completed Days: {completed_days}/{total_days}
• Completion Rate: {(completed_days/total_days)*100:.1f}%

🏆 **Achievements:**
• Voice Exercises Completed: {progress.get('completed_voice_exercises', 0)}
• Breathing Sessions: {progress.get('breathing_sessions_completed', 0)}
• Storytelling Skills: {progress.get('storytelling_skills', 0)}%

💪 **Keep Going!**"""
    
    return dashboard

def calculate_average_quiz_score(user_id):
    """Calculate average quiz score for user"""
    progress = user_progress.get(user_id, {})
    quiz_scores = progress.get("quiz_scores", {})
    if not quiz_scores:
        return 0
    
    total_score = sum(quiz_scores.values())
    total_possible = len(quiz_scores) * 2  # 2 questions per quiz
    return (total_score / total_possible) * 100

def run_simple_bot(token):
    """Run a simple Telegram bot using requests"""
    BASE_URL = f"https://api.telegram.org/bot{token}"
    
    # Initialize reminder system
    def bot_send_message(chat_id, text):
        send_message(chat_id, text)
    
    reminder_system = ReminderSystem(bot_send_message)
    
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
        """Create enhanced main keyboard with new features"""
        if language == 'ar':
            return {
                "inline_keyboard": [
                    [{"text": "📅 التدريب اليومي", "callback_data": "today"}],
                    [{"text": "📚 جميع الأيام", "callback_data": "all_days"}],
                    [{"text": "📊 لوحة التقدم", "callback_data": "dashboard"}],
                    [{"text": "❓ الاختبارات", "callback_data": "quizzes"}],
                    [{"text": "🏆 إنجازاتي", "callback_data": "achievements"}],
                    [{"text": "⚙️ الإعدادات", "callback_data": "settings"}],
                    [{"text": "🌐 English", "callback_data": "switch_language"}]
                ]
            }
        else:
            return {
                "inline_keyboard": [
                    [{"text": "📅 Today's Training", "callback_data": "today"}],
                    [{"text": "📚 All Days", "callback_data": "all_days"}],
                    [{"text": "📊 Progress Dashboard", "callback_data": "dashboard"}],
                    [{"text": "❓ Quizzes", "callback_data": "quizzes"}],
                    [{"text": "🏆 My Achievements", "callback_data": "achievements"}],
                    [{"text": "⚙️ Settings", "callback_data": "settings"}],
                    [{"text": "🌐 العربية", "callback_data": "switch_language"}]
                ]
            }

    def create_settings_keyboard(language, user_id):
        """Create settings keyboard"""
        preferences = user_reminder_preferences.get(user_id, {})
        
        if language == 'ar':
            breathing_text = "🔔 تمارين التنفس: ✅" if preferences.get("breathing_reminders", True) else "🔔 تمارين التنفس: ❌"
            daily_text = "📅 التذكير اليومي: ✅" if preferences.get("daily_reminders", True) else "📅 التذكير اليومي: ❌"
            
            return {
                "inline_keyboard": [
                    [{"text": breathing_text, "callback_data": "toggle_breathing"}],
                    [{"text": daily_text, "callback_data": "toggle_daily"}],
                    [{"text": "💨 تمرين تنفس الآن", "callback_data": "breathing_now"}],
                    [{"text": "🏠 القائمة الرئيسية", "callback_data": "main_menu"}]
                ]
            }
        else:
            breathing_text = "🔔 Breathing Exercises: ✅" if preferences.get("breathing_reminders", True) else "🔔 Breathing Exercises: ❌"
            daily_text = "📅 Daily Reminders: ✅" if preferences.get("daily_reminders", True) else "📅 Daily Reminders: ❌"
            
            return {
                "inline_keyboard": [
                    [{"text": breathing_text, "callback_data": "toggle_breathing"}],
                    [{"text": daily_text, "callback_data": "toggle_daily"}],
                    [{"text": "💨 Breathing Exercise Now", "callback_data": "breathing_now"}],
                    [{"text": "🏠 Main Menu", "callback_data": "main_menu"}]
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
        time_module.sleep(2)
        
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
            initialize_user_progress(user_id)
        
        user_progress[user_id]['quiz_scores'][quiz_state['day']] = score
        
        # Clean up quiz state
        if user_id in user_quiz_state:
            del user_quiz_state[user_id]
    
    # Initialize last update ID
    last_update_id = None
    
    logging.info("🤖 Starting Zain Training Bot...")
    
    while True:
        try:
            reminder_system.run_pending()
            updates = get_updates(last_update_id)
            
            if updates.get("ok"):
                for update in updates["result"]:
                    last_update_id = update["update_id"] + 1
                    
                    # Handle messages
                    if "message" in update and "text" in update["message"]:
                        chat_id = update["message"]["chat"]["id"]
                        text = update["message"]["text"]
                        user_id = update["message"]["from"]["id"]
                        
                        # Initialize user progress using the new function
                        if user_id not in user_progress:
                            initialize_user_progress(user_id)
                        
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
                        
                        elif text == "/dashboard":
                            dashboard = format_progress_dashboard(user_id, user_language.get(user_id, 'ar'))
                            send_message(chat_id, dashboard)
                        
                        elif text == "/breathing":
                            send_breathing_reminder(lambda uid, msg: send_message(chat_id, msg), user_id)
                        
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
                        
                        # Initialize user progress using the new function
                        if user_id not in user_progress:
                            initialize_user_progress(user_id)
                        
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
                        
                        elif data == "dashboard":
                            dashboard = format_progress_dashboard(user_id, user_language.get(user_id, 'ar'))
                            send_message(chat_id, dashboard)
                        
                        elif data == "achievements":
                            achievements = user_achievements.get(user_id, [])
                            language = user_language.get(user_id, 'ar')
                            
                            if language == 'ar':
                                if achievements:
                                    achievement_text = "🏆 **إنجازاتك:**\n\n"
                                    for achievement_id in achievements:
                                        achievement = ACHIEVEMENTS[achievement_id]
                                        achievement_text += f"{achievement['icon']} **{achievement['name_ar']}**\n{achievement['description_ar']}\n\n"
                                else:
                                    achievement_text = "🎯 لم تحصل على أي إنجازات بعد. استمر في التعلم! 💪"
                            else:
                                if achievements:
                                    achievement_text = "🏆 **Your Achievements:**\n\n"
                                    for achievement_id in achievements:
                                        achievement = ACHIEVEMENTS[achievement_id]
                                        achievement_text += f"{achievement['icon']} **{achievement['name_en']}**\n{achievement['description_en']}\n\n"
                                else:
                                    achievement_text = "🎯 You haven't unlocked any achievements yet. Keep learning! 💪"
                            
                            send_message(chat_id, achievement_text)
                        
                        elif data == "settings":
                            settings_text = get_text(user_id,
                                "⚙️ **إعدادات التذكيرات**\n\nاختر التذكيرات التي تريد تفعيلها:",
                                "⚙️ **Reminder Settings**\n\nChoose which reminders to enable:"
                            )
                            send_message(chat_id, settings_text, create_settings_keyboard(user_language.get(user_id, 'ar'), user_id))
                        
                        elif data == "toggle_breathing":
                            if user_id not in user_reminder_preferences:
                                user_reminder_preferences[user_id] = {"breathing_reminders": True, "daily_reminders": True}
                            user_reminder_preferences[user_id]["breathing_reminders"] = not user_reminder_preferences[user_id].get("breathing_reminders", True)
                            settings_text = get_text(user_id,
                                "⚙️ **إعدادات التذكيرات**\n\nاختر التذكيرات التي تريد تفعيلها:",
                                "⚙️ **Reminder Settings**\n\nChoose which reminders to enable:"
                            )
                            send_message(chat_id, settings_text, create_settings_keyboard(user_language.get(user_id, 'ar'), user_id))
                        
                        elif data == "toggle_daily":
                            if user_id not in user_reminder_preferences:
                                user_reminder_preferences[user_id] = {"breathing_reminders": True, "daily_reminders": True}
                            user_reminder_preferences[user_id]["daily_reminders"] = not user_reminder_preferences[user_id].get("daily_reminders", True)
                            settings_text = get_text(user_id,
                                "⚙️ **إعدادات التذكيرات**\n\nاختر التذكيرات التي تريد تفعيلها:",
                                "⚙️ **Reminder Settings**\n\nChoose which reminders to enable:"
                            )
                            send_message(chat_id, settings_text, create_settings_keyboard(user_language.get(user_id, 'ar'), user_id))
                        
                        elif data == "breathing_now":
                            send_breathing_reminder(lambda uid, msg: send_message(chat_id, msg), user_id)
                        
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
            
            time_module.sleep(1)
            
        except Exception as e:
            logging.error(f"Bot error: {e}")
            time_module.sleep(5)

def run_scheduler():
    """Run the schedule checker in a separate thread"""
    while True:
        try:
            schedule.run_pending()
            time_module.sleep(60)  # Check every minute
        except Exception as e:
            logging.error(f"Scheduler error: {e}")
            time_module.sleep(60)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    # Get token
    token = os.environ.get('TELEGRAM_TOKEN')
    
    if token:
        logging.info(f"✅ TELEGRAM_TOKEN found! Starting Zain Training Bot...")
        
        # Start bot in a separate thread
        bot_thread = threading.Thread(target=run_simple_bot, args=(token,), daemon=True)
        bot_thread.start()
        
        # Start scheduler in a separate thread
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        
        logging.info("✅ Zain Training Bot started!")
        logging.info("✅ Scheduler started!")
    else:
        logging.error("❌ TELEGRAM_TOKEN not found!")
    
    # Start Flask
    logging.info(f"🌐 Starting Flask on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
