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

كيف تستمع بنشاط؟
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
                "title_ar": "تمارين الإحماء الصوتي",
                "title_en": "Vocal Warm-up Exercises",
                "content_ar": """تمارين الإحماء الصوتي (الروتين اليومي):
التنفس الحجابي: تنفس بعمق من الأنف بحيث يتمدد بطنك، وازفر ببطء من الفم
تمرين الشفاه: حرك شفتيك معاً وتحريكهما في كل الاتجاهات
تمرين اللسان: لمس سقف الحلق وتحريك اللسان بشكل دائري

وضوح الكلام هو الاحترافية ذاتها:
ركز على مخارج الحروف، خاصة الحروف التي تحتاج لجهد
تخيل أنك ترمي الكلمات مثل السهام، يجب أن تكون واضحة ومستقيمة
مثال: عند نطق كلمة مستقبل، ركز على كل حرف وخاصة حرف القاف""",
                "content_en": """Vocal Warm-up Exercises (Daily Routine):
Diaphragmatic breathing: Breathe deeply through your nose so your stomach expands, exhale slowly through your mouth
Lip exercises: Move your lips together and in all directions
Tongue exercises: Touch the roof of your mouth and move your tongue in circles

Speech clarity is professionalism itself:
Focus on letter articulation, especially letters that require effort
Imagine throwing words like arrows - they should be clear and straight
Example: When pronouncing the word future, focus on each letter especially the Qaf sound"""
            },
            {
                "type": "text",
                "title_ar": "موسيقى الكلام والتعبير",
                "title_en": "Speech Music and Expression",
                "content_ar": """موسيقى الكلام: كيف تصنع لحناً يجذب الأذن؟
النبرة: التغيير بين العالي والمنخفض يخلق تشويقاً
السرعة: سريعة للإثارة، بطيئة للتأكيد
الوقفات: استخدمها قبل وبعد المعلومات المهمة

لغة الجسد للصوت:
حتى لو لم يراك أحد، فإن ابتسامتك تسمع
تحدث ووجهك يعبر، ويديك تتحركان
الطاقة الإيجابية تنتقل عبر الصوت""",
                "content_en": """Speech music: How to create a melody that attracts the ear?
Tone: Changing between high and low creates suspense
Speed: Fast for excitement, slow for emphasis
Pauses: Use them before and after important information

Body language for voice:
Even if no one sees you, your smile can be heard
Speak with expressive face and moving hands
Positive energy transmits through voice"""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الثاني: أدوات الصوت والتعبير",
            "title_en": "Day 2 Quiz: Voice Tools and Expression",
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
                "title_ar": "المقدمة (الخطاف)",
                "title_en": "Introduction (The Hook)",
                "content_ar": """المقدمة (الخطاف):
لديك 10-15 ثانية فقط للإمساك بانتباه المستمع
أنواع الخطافات الفعالة:
السؤال الصادم: هل تعلم أن 90% من قراراتنا نتاج العقل الباطن؟
القصة المصغرة: كنت أجري أمس، وفجأة... وقعت!
الإحصائية المدهشة: يهدر طعام يكفي لإطعام مليار شخص سنوياً
الموقف الطريف: حاولت مرة أن أطهو بيضاً فاحترق المطبخ!""",
                "content_en": """Introduction (The Hook):
You only have 10-15 seconds to grab the listener's attention
Types of effective hooks:
Shocking question: Did you know that 90% of our decisions come from the subconscious?
Mini-story: I was running yesterday, and suddenly... I fell!
Amazing statistic: Enough food to feed one billion people is wasted annually
Funny situation: I once tried to cook eggs and the kitchen caught fire!"""
            },
            {
                "type": "text",
                "title_ar": "المحتوى والخاتمة",
                "title_en": "Content and Conclusion",
                "content_ar": """المحتوى (اللب):
ركز على نقطة رئيسية واحدة في كل فقرة
استخدم القصص لجعل المعلومة أكثر جاذبية
قدم أمثلة وتشبيهات لدعم فكرتك الرئيسية

الخاتمة (الختام المؤثر):
أنواع الخواتم:
التلخيص: إذن، الفكرة الرئيسية هي...
دعوة للتفاعل: ما رأيكم؟ اكتبوا في الدردشة
السؤال المفتوح: لو كانت لديكم فرصة لسؤال أحد المشاهير، فمن تختارون؟
التلميح للمستقبل: في الحلقة القادمة، سنكشف عن سر...""",
                "content_en": """Content (The Body):
Focus on one main point in each segment
Use stories to make information more attractive
Provide examples and analogies to support your main idea

Conclusion (Impactful Closing):
Types of conclusions:
Summary: So, the main idea is...
Call to interaction: What do you think? Write in the chat
Open question: If you had a chance to ask a celebrity, who would you choose?
Hint for the future: In the next episode, we'll reveal the secret of..."""
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
                "title_ar": "فلسفة الألعاب التنشيطية",
                "title_en": "Philosophy of Icebreaker Games",
                "content_ar": """الفلسفة وراء الألعاب التنشيطية:
الهدف ليس اللعبة نفسها، بل التفاعل الاجتماعي الذي تخلقه
اللعبة مجرد وسيلة لجعل الجمهور يشعر بالراحة والمتعة
مثال: لعبة ماذا ستفعل بمليون دولار تفتح مجالاً للتعارف والإبداع

أنماط الألعاب التنشيطية:
ألعاب التعارف: ما هي القوة الخارقة التي تريدها؟
ألعاب الذكاء السريع: أسئلة معلومات عامة
ألعاب التخمين: تخمين الشخصية، الفيلم، كلمة السر
ألعاب الصور: وصف الصورة دون استخدام كلمات ممنوعة""",
                "content_en": """Philosophy behind icebreaker games:
The goal is not the game itself, but the social interaction it creates
The game is just a means to make the audience feel comfortable and have fun
Example: What would you do with a million dollars game opens opportunities for networking and creativity

Types of icebreaker games:
Networking games: What superpower would you want?
Quick intelligence games: General knowledge questions
Guessing games: Guess the character, movie, password
Picture games: Describe the picture without using forbidden words"""
            },
            {
                "type": "text",
                "title_ar": "تقديم الألعاب بنجاح",
                "title_en": "Presenting Games Successfully",
                "content_ar": """كيف تقدم لعبة؟ خطوات واضحة:
الخطوة 1: اذكر اسم اللعبة بحماس
الخطوة 2: اشرح القواعد ببساطة ووضوح
الخطوة 3: نفذ اللعبة مع التحفيز والتعليق
الخطوة 4: أنهِ بشكر المشاركين والانتقال السلس

نصائح ذهبية للنجاح:
التحكيم بمرح وليس بقسوة
إدارة الوقت والمحافظة على وتيرة البرنامج
الحفاظ على طاقة عالية طوال الوقت""",
                "content_en": """How to present a game? Clear steps:
Step 1: Announce the game name with enthusiasm
Step 2: Explain the rules simply and clearly
Step 3: Implement the game with motivation and commentary
Step 4: End by thanking participants and smooth transition

Golden tips for success:
Referee with fun, not harshness
Time management and maintaining program pace
Maintain high energy throughout"""
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
تحدي الـ 10 ثوان: الإجابة 10 ثوان
أغنية وكلمة: معرفة الأغنية أو كلمة مرتبطة بها
أسئلة نعم أو لا: أسئلة سريعة مباشرة""",
                "content_en": """Speed energy and management:
These segments require high energy and sharp focus
Breathe deeply before starting to charge your energy
Maintain fast pace but with clarity in speech

Types of speed games:
Fastest answer: Question is asked and first to raise hand wins
10-second challenge: Answer must be within 10 seconds
Song and word: Identifying the song or related word
Yes or no questions: Quick direct questions"""
            },
            {
                "type": "text",
                "title_ar": "فن التعليق والتشويق",
                "title_en": "Art of Commentary and Suspense",
                "content_ar": """فن التعليق على الإجابات:
الإجابة الصحيحة: أحسنت!، انطلقت كالصاروخ!
الإجابة الخاطئة: أوه، كادت!، الفكرة قريبة!
نبرة التشويق: استخدم صوتاً مرتفعاً ومتحمساً للإجابات الصحيحة

أدوات التشويق والإثارة:
صوت المؤقت يزيد التوتر
المؤثرات الصوتية (جرس للفوز، صفارة للخطأ)
الخلفية الموسيقية السريعة""",
                "content_en": """Art of commenting on answers:
Correct answer: Well done! Took off like a rocket!
Wrong answer: Oh, almost! The idea is close!
Suspense tone: Use high and excited voice for correct answers

Tools for suspense and excitement:
Timer sound increases tension
Sound effects (bell for winning, whistle for wrong)
Fast background music"""
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
                }
            ]
        }
    },
    6: {
        "title_ar": "اليوم السادس: الفقرات الثقافية والمعلوماتية - من المعلومة الجافة إلى القصة المشوقة",
        "title_en": "Day 6: Cultural and Informational Segments - From Dry Information to Exciting Stories",
        "materials": [
            {
                "type": "text",
                "title_ar": "محاربة الملل في المعلومات",
                "title_en": "Fighting Boredom in Information",
                "content_ar": """محاربة الملل في تقديم المعلومات:
اروي، لا تخبر: بدلاً من كان الطقس بارداً قل كان الصقيع يتسلل عبر سترتي
اربط المعلومة بحياة المستمع: اجعل المعلومة شخصية ومؤثرة
استخدم التشبيهات: الإنترنت يشبه الطريق السريع للبيانات

تبسيط المعلومات المعقدة:
التشبيه: البلوك تشين يشبه دفتر حسابات موزع
القصص: ابحث عن القصة الإنسانية خلف المعلومة
الأمثلة العملية: شرح النظريات من خلال تطبيقاتها اليومية""",
                "content_en": """Fighting boredom in presenting information:
Narrate, don't tell: Instead of the weather was cold say the frost was creeping through my jacket
Connect information to the listener's life: Make the information personal and impactful
Use analogies: The internet is like a highway for data

Simplifying complex information:
Analogy: Blockchain is like a distributed ledger
Stories: Look for the human story behind the information
Practical examples: Explain theories through their daily applications"""
            },
            {
                "type": "text",
                "title_ar": "المصداقية والمصادر",
                "title_en": "Credibility and Sources",
                "content_ar": """مصادر المعلومات ومصداقيتها:
تحقق دائماً من مصدر المعلومة
استخدم مواقع موثوقة ومراجع علمية
ذكر مصدرك يزيد من مصداقيتك

أنماط الفقرات الثقافية:
هل تعلم؟ قصيرة وسريعة
سؤال ثقافي مع مشاركة الجمهور
حكاية من التاريخ بسرد قصصي مشوق""",
                "content_en": """Information sources and credibility:
Always verify the source of information
Use reliable websites and scientific references
Mentioning your source increases your credibility

Types of cultural segments:
Did you know? Short and fast
Cultural question with audience participation
Historical tale with exciting storytelling"""
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
                }
            ]
        }
    },
    7: {
        "title_ar": "اليوم السابع: الفقرات التفاعلية - قلب البرنامج النابض",
        "title_en": "Day 7: Interactive Segments - The Beating Heart of the Program",
        "materials": [
            {
                "type": "text",
                "title_ar": "استراتيجيات جذب التفاعل",
                "title_en": "Strategies for Attracting Interaction",
                "content_ar": """استراتيجيات جذب التفاعل:
الأسئلة المفتوحة: ما هو أكثر لحظة أعجبتكم؟ بدلاً من هل أعجبكم البرنامج؟
استطلاعات الرأي: استخدام أدوات التصويت في التطبيقات
الطلب المباشر: شاركونا صور طعامكم!، ما رأيكم في...؟

فن إدارة التعليقات المباشرة:
التعليق الإيجابي: اشكر ورد بالاسم (شكراً لك يا أحمد)
التعليق السلبي: تعامل بذكاء
التعليق المسيء: تجاهله أو أخرجه بهدوء""",
                "content_en": """Strategies for attracting interaction:
Open questions: What was your favorite moment? instead of Did you like the program?
Opinion polls: Using voting tools in applications
Direct request: Share your food photos! What do you think about...?

Art of managing live comments:
Positive comment: Thank and respond by name (Thank you, Ahmed)
Negative comment: Deal with it intelligently
Offensive comment: Ignore it or remove it calmly"""
            },
            {
                "type": "text",
                "title_ar": "أنماط الفقرات التفاعلية",
                "title_en": "Types of Interactive Segments",
                "content_ar": """أنماط الفقرات التفاعلية:
الرأي والرأي الآخر: مناقشة قضايا مختلفة الآراء
قصص من حياتكم: مشاركة قصص شخصية
استشارات الجمهور: طلب النصائح والأفكار

نصائح للتفاعل الناجح:
كن صادقاً في تفاعلك
تعامل مع الجمهور كأصدقاء
استخدم أسماء المشاركين
اشكر الجميع على المشاركة""",
                "content_en": """Types of interactive segments:
Opinion and counter-opinion: Discussing issues with different views
Stories from your lives: Sharing personal stories
Audience consultations: Requesting advice and ideas

Tips for successful interaction:
Be sincere in your interaction
Treat the audience as friends
Use participants' names
Thank everyone for participation"""
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
                "title_ar": "حقيقة الارتجال",
                "title_en": "The Truth About Improvisation",
                "content_ar": """حقيقة الارتجال:
الارتجال الحقيقي هو تحضير مسبق للأدوات وليس للنص
جهز طقم النجاة قبل أن تحتاجه

المواقف الطارئة الشائعة:
صمت مطبق: ضيف لا يتكلم أو عدم تفاعل
مشاكل تقنية: انقطاع الإنترنت، صوت غير واضح
تفاعل ضعيف: لا أحد يشارك
تعليقات محرجة: أسئلة أو ملاحظات غير متوقعة""",
                "content_en": """The truth about improvisation:
Real improvisation is preparing tools in advance, not the script
Prepare your survival kit before you need it

Common emergency situations:
Complete silence: Guest doesn't speak or no interaction
Technical problems: Internet disconnection, unclear sound
Weak interaction: No one participates
Embarrassing comments: Unexpected questions or remarks"""
            },
            {
                "type": "text",
                "title_ar": "أدوات الارتجال",
                "title_en": "Improvisation Tools",
                "content_ar": """أدوات الارتجال (طوق النجاة):
الفكاهة: اضحك على الموقف (يبدو أن الإنترنت قرر أخذ استراحة!)
الاعتراف البسيط: أعتذر، ظهري انقطع للحظة!
العودة لنقطة سابقة: هذا يذكرني بما كنا نتحدث عنه...
الجعبة السرية: 3 قصص شخصية + 5 أسئلة عامة

نصائح للارتجال الناجح:
حافظ على هدوئك
استخدم الفكاهة المناسبة
لا تخف من الصمت المؤقت
كن صادقاً مع جمهورك""",
                "content_en": """Improvisation tools (Lifebuoy):
Humor: Laugh at the situation (Looks like the internet decided to take a break!)
Simple acknowledgment: I apologize, my connection dropped for a moment!
Return to previous point: This reminds me of what we were talking about...
Secret kit: 3 personal stories + 5 general questions

Tips for successful improvisation:
Keep your calm
Use appropriate humor
Don't be afraid of temporary silence
Be honest with your audience"""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الثامن: الارتجال",
            "title_en": "Day 8 Quiz: Improvisation",
            "questions": [
                {
                    "question_ar": "ما هي حقيقة الارتجال الناجح؟",
                    "question_en": "What is the truth about successful improvisation?",
                    "options_ar": ["عدم التحضير مطلقاً", "التحضير المسبق للأدوات", "الحفظ عن ظهر قلب", "تجنب المواقف الصعبة"],
                    "options_en": ["Never preparing", "Preparing tools in advance", "Memorizing by heart", "Avoiding difficult situations"],
                    "correct": 1,
                    "explanation_ar": "الارتجال الناجح يعتمد على التحضير المسبق للأدوات والموارد وليس على الحظ",
                    "explanation_en": "Successful improvisation depends on preparing tools and resources in advance, not on luck"
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
                "title_ar": "التحضير قبل البرنامج",
                "title_en": "Preparation Before the Program",
                "content_ar": """التحضير قبل البرنامج:
البحث عن الضيف: اقرأ عنه، شاهد مقابلات سابقة
تحديد الهدف: ما الرسالة الرئيسية من المقابلة؟
إعداد النقاط الرئيسية: 5-7 نقاط وليس نصاً كاملاً
الاتصال بالضيف: تعريفه بنمط البرنامج والنقاط الرئيسية

فن صياغة الأسئلة:
الأسئلة المفتوحة: كيف كانت رحلتك؟، ما الذي دفعك لهذا القرار؟
أسئلة المشاعر: كيف شعرت في تلك اللحظة؟
الأسئلة المتتابعة: ابنِ على إجابات الضيف""",
                "content_en": """Preparation before the program:
Research the guest: Read about them, watch previous interviews
Define the goal: What is the main message from the interview?
Prepare main points: 5-7 points, not a full script
Contact the guest: Introduce them to the program style and main points

Art of formulating questions:
Open questions: How was your journey? What prompted this decision?
Emotion questions: How did you feel at that moment?
Follow-up questions: Build on the guest's answers"""
            },
            {
                "type": "text",
                "title_ar": "دورك كقائد أوركسترا",
                "title_en": "Your Role as Orchestra Conductor",
                "content_ar": """دورك كقائد أوركسترا:
لا تكن النجم: سلط الضوء على الضيف لا على نفسك
الاستماع ثم الكلام: الاستماع الجيد يولد أسئلة أفضل
إدارة الوقت: أنهِ الحوار بلباقة عندما يحين الموعد

نصائح للنجاح:
كن مستمعاً جيداً
احترم مساحة الضيف
ساعد الضيف الخجول
تحكم في الحوار بلطف""",
                "content_en": """Your role as orchestra conductor:
Don't be the star: Spotlight the guest, not yourself
Listen then speak: Good listening generates better questions
Time management: End the dialogue politely when time comes

Success tips:
Be a good listener
Respect the guest's space
Help the shy guest
Control the dialogue gently"""
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم التاسع: إدارة الحوار",
            "title_en": "Day 9 Quiz: Dialogue Management",
            "questions": [
                {
                    "question_ar": "ما هو دور المضيف في الحوار مع الضيوف؟",
                    "question_en": "What is the host's role in dialogue with guests?",
                    "options_ar": ["أن يكون النجم الرئيسي", "تسليط الضوء على الضيف", "التحدث أكثر من الضيف", "عدم الاستماع للضيف"],
                    "options_en": ["Being the main star", "Spotlighting the guest", "Talking more than the guest", "Not listening to the guest"],
                    "correct": 1,
                    "explanation_ar": "دور المضيف هو تسليط الضوء على الضيف وإدارة الحوار وليس أن يكون النجم الرئيسي",
                    "explanation_en": "The host's role is to spotlight the guest and manage the dialogue, not to be the main star"
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
                "title_ar": "هندسة البرنامج",
                "title_en": "Program Engineering",
                "content_ar": """هندسة البرنامج:
الفكرة: ماذا تقدم؟ (ترفيه، تعليم، إلهام)
الجمهور: لمن تقدمه؟ (شباب، عائلات، متخصصون)
الهدف: لماذا تقدمه؟ (تسلية، معرفة، مجتمع)

الروتين التحضيري:
البحث وجمع المعلومات
كتابة النقاط الرئيسية
التحضير للفقرات
الاختبار التقني
الإعلان المسبق""",
                "content_en": """Program engineering:
Idea: What do you offer? (Entertainment, education, inspiration)
Audience: Who do you offer it to? (Youth, families, specialists)
Goal: Why do you offer it? (Entertainment, knowledge, community)

Preparation routine:
Research and information gathering
Writing main points
Preparing segments
Technical testing
Advance announcement"""
            },
            {
                "type": "text",
                "title_ar": "السكريبت المرن والهوية",
                "title_en": "Flexible Script and Identity",
                "content_ar": """السكريبت المرن:
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
طريقة الترحيب الخاصة
النبرة الصوتية المميزة""",
                "content_en": """Flexible script:
Not a text you read, but a road map
Example:
0:00-0:02: Introduction + hook
0:02-0:05: Welcome + interaction
0:05-0:15: Main game
0:15-0:25: Guest interview
0:25-0:29: Audience interaction
0:29-0:30: Conclusion

Identity creation:
Program name and logo
Distinctive music
Special welcome method
Distinctive vocal tone"""
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
                "title_ar": "الموسيقى والمؤثرات الصوتية",
                "title_en": "Music and Sound Effects",
                "content_ar": """الموسيقى والمؤثرات الصوتية:
الملح وليس الطبق الرئيسي: الإفراط يفسد التجربة
المقدمة والخاتمة: موسيقى مميزة وقصيرة
الانتقالات: موسيقى خفيفة بين الفقرات

اختيار الموسيقى المناسبة:
البرامج المرحة: موسيقى سريعة وإيقاعية
البرامج الجادة: موسيقى هادئة أو بدون موسيقى
المصادر: استخدم موسيقى خالية من الحقوق""",
                "content_en": """Music and sound effects:
The salt, not the main dish: Excess spoils the experience
Introduction and conclusion: Distinctive and short music
Transitions: Light music between segments

Choosing appropriate music:
Fun programs: Fast and rhythmic music
Serious programs: Calm music or no music
Sources: Use royalty-free music"""
            },
            {
                "type": "text",
                "title_ar": "معالجة الصوت الأساسية",
                "title_en": "Basic Audio Processing",
                "content_ar": """معالجة الصوت الأساسية:
إزالة الضوضاء: تزيل همسة الميكروفون
معادلة الصوت: تحسين الوضوح
الضغط: توحيد مستوى الصوت

نصائح للجودة الصوتية:
استخدم ميكروفون جيد
سجل في مكان هادئ
اختبر الصوت قبل البث
حافظ على مستوى صوت متوازن""",
                "content_en": """Basic audio processing:
Noise removal: Removes microphone hiss
Equalization: Improves clarity
Compression: Unifies volume level

Audio quality tips:
Use a good microphone
Record in a quiet place
Test sound before broadcasting
Maintain balanced volume level"""
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
                "title_ar": "الستوري تيلينغ (فن سرد القصة)",
                "title_en": "Storytelling (The Art of Narration)",
                "content_ar": """الستوري تيلينغ (فن سرد القصة):
الهيكل الذهبي:
البداية: الشخصية في سياقها العادي
الحدث المحفز: شيء يغير كل شيء
الرحلة والصراع: التحديات
الذروة: لحظة الحسم
النهاية: التغيير والدرس

نصائح للسرد المؤثر:
استخدم التفاصيل الحسية
ابنِ التشويق تدريجياً
اجعل المستمع يشعر مع الشخصية""",
                "content_en": """Storytelling (The Art of Narration):
The golden structure:
Beginning: The character in their normal context
Triggering event: Something that changes everything
Journey and conflict: The challenges
Climax: The moment of decision
End: The change and lesson

Tips for impactful narration:
Use sensory details
Build suspense gradually
Make the listener feel with the character"""
            },
            {
                "type": "text",
                "title_ar": "الدعابة الذكية والتوقيت",
                "title_en": "Smart Humor and Timing",
                "content_ar": """الدعابة الذكية:
اضحك على نفسك لا على الآخرين
المفارقة: هدفي كان رياضياً محترفاً ولكن الأريكة كانت أقوى!
المراقبة: التعليق على مواقف الحياة اليومية

التوقيت الكوميدي:
الوقفة قبل النكتة: تزيد التشويق
الوقفة بعد النكتة: تعطي وقتاً للضحك
الإيقاع: التناوب بين السرعة والبطء""",
                "content_en": """Smart humor:
Laugh at yourself, not at others
Irony: My goal was to be a professional athlete but the couch was stronger!
Observation: Commenting on daily life situations

Comedic timing:
Pause before the joke: Increases suspense
Pause after the joke: Gives time to laugh
Rhythm: Alternating between speed and slowness"""
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
                "title_ar": "أنماط الشخصيات في الجمهور",
                "title_en": "Personality Types in the Audience",
                "content_ar": """أنماط الشخصيات في الجمهور:
المتفاعل: يعلق ويسأل باستمرار
المشجع: حاضر دائماً ونادر التفاعل
الناقد: يرى الأخطاء فقط
الخجول: يستمع فقط

فهم احتياجات كل نمط:
المتفاعل: يحتاج للإحساس بالتقدير
المشجع: يحتاج للشعور بالانتماء
الناقد: يحتاج للاستماع الجيد
الخجول: يحتاج للراحة والأمان""",
                "content_en": """Personality types in the audience:
Interactive: Constantly comments and asks questions
Supporter: Always present but rarely interacts
Critic: Only sees mistakes
Shy: Only listens

Understanding each type's needs:
Interactive: Needs to feel appreciated
Supporter: Needs to feel belonging
Critic: Needs good listening
Shy: Needs comfort and safety"""
            },
            {
                "type": "text",
                "title_ar": "بناء المجتمع والتفاعل",
                "title_en": "Building Community and Interaction",
                "content_ar": """بناء المجتمع:
التكرار: المواظبة على الموعد تخلق عادة
التفاعل الشخصي: مناداتهم بالأسماء
تلبية الرغبات: تخصيص فقرات بناء على طلباتهم

جمع التغذية الراجعة:
الاستبيانات السريعة
الأسئلة المباشرة
مراقبة نوعية التفاعل
تحليل الإحصائيات""",
                "content_en": """Building community:
Repetition: Consistency with timing creates habits
Personal interaction: Calling them by names
Fulfilling desires: Customizing segments based on their requests

Collecting feedback:
Quick surveys
Direct questions
Monitoring interaction quality
Analyzing statistics"""
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
                "title_ar": "فنون الربط والتكامل",
                "title_en": "Arts of Connection and Integration",
                "content_ar": """فنون الربط:
اللفظي: والحديث عن السفر يحضرني لعبة عن دول العالم
الصوتي: استخدام موسيقى انتقالية
المنطقي: بعد كل هذا المرح، حان وقت الاستراحة بمعلومة مدهشة

التكامل بين المهارات:
دمج الاستماع النشط مع إدارة الحوار
الجمع بين السرد القصصي والتفاعل
التوازن بين الجدية والمرح
الانتقال السلس بين الفقرات""",
                "content_en": """Arts of connection:
Verbal: And talking about travel brings me to a game about world countries
Audio: Using transition music
Logical: After all this fun, it's time for a break with an amazing fact

Integration between skills:
Combining active listening with dialogue management
Merging storytelling with interaction
Balancing seriousness and fun
Smooth transition between segments"""
            },
            {
                "type": "text",
                "title_ar": "البروفة النهائية",
                "title_en": "Final Rehearsal",
                "content_ar": """البروفة النهائية الشاملة:
التدريب على البرنامج الكامل
تسجيل الحلقة كاملة
التقييم الذاتي
التغذية الراجعة من الآخرين

نصائح للبروفة الناجحة:
تدرب كما لو كان بثاً حقيقياً
سجل وأعد الاستماع
اطلب رأي الأشخاص الموثوقين
ركز على نقاط الضعف""",
                "content_en": """Comprehensive final rehearsal:
Training on the complete program
Recording the full episode
Self-evaluation
Feedback from others

Tips for successful rehearsal:
Practice as if it were a real broadcast
Record and listen again
Ask for opinions from trusted people
Focus on weak points"""
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
                "title_ar": "التقييم الذاتي الموضوعي",
                "title_en": "Objective Self-Evaluation",
                "content_ar": """التقييم الذاتي الموضوعي:
استمع كجمهور: هل أنت مستمتع؟
استمع كخبير: حلل الوضوح، الطلاقة، التنظيم
ابحث عن نقاط القوة والضعف

معايير التقييم:
وضوح الصوت والكلام
تنظيم المحتوى
جودة التفاعل
الإبداع والتميز
الطاقة والإيجابية""",
                "content_en": """Objective self-evaluation:
Listen as an audience: Are you enjoying?
Listen as an expert: Analyze clarity, fluency, organization
Look for strengths and weaknesses

Evaluation standards:
Sound and speech clarity
Content organization
Interaction quality
Creativity and excellence
Energy and positivity"""
            },
            {
                "type": "text",
                "title_ar": "خطة التطوير المستمر",
                "title_en": "Continuous Development Plan",
                "content_ar": """خطة التطوير المستمر:
مواكبة الترندات
التعلم المستمر
طلب التغذية الراجعة
تحديث المهارات

الاستدامة والنمو:
ضع حدوداً للراحة
تذكر لماذا بدأت
احتفل بالإنجازات
ضع أهدافاً جديدة
استمر في التعلم دائماً""",
                "content_en": """Continuous development plan:
Keeping up with trends
Continuous learning
Requesting feedback
Updating skills

Sustainability and growth:
Set comfort boundaries
Remember why you started
Celebrate achievements
Set new goals
Always keep learning"""
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
                }
            ]
        }
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
                            day_data = TRAINING_DATA.get(day_num)
                            if day_data:
                                # Start quiz implementation
                                quiz_title = day_data['quiz']['title_ar'] if get_user_language(user_id) == 'ar' else day_data['quiz']['title_en']
                                start_text = get_text(user_id,
                                    f"بدء {quiz_title}",
                                    f"Starting {quiz_title}"
                                )
                                send_message(chat_id, start_text)
                                # Add quiz logic here
                            else:
                                error_text = get_text(user_id, "❌ الاختبار غير متوفر", "❌ Quiz not available")
                                send_message(chat_id, error_text)
            
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
