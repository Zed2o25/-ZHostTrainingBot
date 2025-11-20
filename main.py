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
# COMPLETE TRAINING DATA FOR ALL 15 DAYS
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
                "content_ar": """
في العالم الصوتي، أنت المسؤول الوحيد عن صناعة المشاعر وتوجيه الطاقة
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
الأصالة: كن صادقاً في ردودك وتفاعلك، لا تتصنع شخصية غيرك
                """,
                "content_en": """
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
Clarifying questions: Do you mean that...? What happened next?

Building your vocal identity:
Confidence: Stemming from your belief in your value and what you offer
Energy: Make your energy positive and contagious even on ordinary days
Authenticity: Be honest in your responses and interactions, don't fake another personality
                """
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية",
                "title_en": "Practical Exercises",
                "content_ar": """
التمارين العملية الفردية:
تمرين التحليل (15 دقيقة): استمع لمضيف مشهور وحلل 3 مواقف استخدم فيها الاستماع النشط
تمرين التسجيل والتحليل الذاتي (30 دقيقة): سجل صوتك وأنت تتحدث عن كتاب أو فيلم، ثم حلل سرعتك، وضوحك، ونبرة صوتك
تمرين الارتجال (15 دقيقة): تحدث عن كلمة عشوائية لمدة 60 ثانية دون توقف

الأنشطة الجماعية:
لعبة همسة السلسلة (15 دقيقة): لتدريب دقة الاستماع ونقل المعلومة
المقابلة النشطة (20 دقيقة): يتدرب المتدربون على الاستماع بهدف الفهم وليس الرد

المهمة اليومية: استمع إلى مضيف آخر وحلل طريقته في التعامل مع ضيوفه وجمهوره
                """,
                "content_en": """
Individual Practical Exercises:
Analysis Exercise (15 minutes): Listen to a famous host and analyze 3 situations where they used active listening
Recording and Self-Analysis Exercise (30 minutes): Record your voice while talking about a book or movie, then analyze your speed, clarity, and tone
Improvisation Exercise (15 minutes): Talk about a random word for 60 seconds without stopping

Group Activities:
Chain Whisper Game (15 minutes): To train listening accuracy and information transfer
Active Interview (20 minutes): Trainees practice listening for understanding rather than responding

Daily Task: Listen to another host and analyze their way of dealing with guests and audience
                """
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
                },
                {
                    "question_ar": "ما الذي يميز الهوية الصوتية الأصيلة؟",
                    "question_en": "What distinguishes an authentic vocal identity?",
                    "options_ar": ["التصنع في التعامل", "الصدق في الردود والتفاعل", "تقليد شخصيات أخرى", "الحديث السريع دائماً"],
                    "options_en": ["Faking in interactions", "Honesty in responses and interactions", "Imitating other personalities", "Always speaking fast"],
                    "correct": 1,
                    "explanation_ar": "الأصالة في الهوية الصوتية تعني الصدق في الردود والتفاعل وعدم التصنع",
                    "explanation_en": "Authenticity in vocal identity means honesty in responses and interactions without pretense"
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
                "content_ar": """
الروتين اليومي للإحماء الصوتي:
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
تحدث ووجهك يعبر، ويديك تتحركان
                """,
                "content_en": """
Daily Vocal Warm-up Routine:
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
Speak with expressive facial expressions and hand movements
                """
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية",
                "title_en": "Practical Exercises",
                "content_ar": """
التمارين العملية الفردية:
تمرين الإحماء (20 دقيقة): التنفس والشفاه واللسان
تمرين التعبير الصوتي (20 دقيقة): اقرأ قصة للأطفال بتعابير مبالغ فيها
تمرين النبرة والسرعة (20 دقيقة): اقرأ خبراً جريدة بطرق مختلفة

الأنشطة الجماعية:
الاتحاد الصوتي (دويتو) (25 دقيقة): تقديم فقرة ترحيب بشكل متناغم
مسرح المشاعر (20 دقيقة): قراءة جملة محايدة بمشاعر مختلفة

المهمة اليومية: سجل نفسك تقول جملة "ماذا لو أخبرتك أن كل شيء تعرفه على وشك أن يتغير؟" بثلاث نبرات مختلفة
                """,
                "content_en": """
Individual Practical Exercises:
Warm-up Exercise (20 minutes): Breathing, lips, and tongue
Vocal Expression Exercise (20 minutes): Read a children's story with exaggerated expressions
Tone and Speed Exercise (20 minutes): Read a newspaper article in different ways

Group Activities:
Vocal Union (Duet) (25 minutes): Present a welcome segment in harmony
Emotion Theater (20 minutes): Read a neutral sentence with different emotions

Daily Task: Record yourself saying "What if I told you that everything you know is about to change?" in three different tones
                """
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
                },
                {
                    "question_ar": "ماذا تساعد الوقفات في الكلام؟",
                    "question_en": "What do pauses help with in speech?",
                    "options_ar": ["إطالة الوقت فقط", "إعطاء أهمية للمعلومات قبلها وبعدها", "إرباك المستمع", "تقليل الوضوح"],
                    "options_en": ["Only extending time", "Giving importance to information before and after them", "Confusing the listener", "Reducing clarity"],
                    "correct": 1,
                    "explanation_ar": "الوقفات تساعد في إبراز المعلومات المهمة قبلها وبعدها وتزيد من تأثيرها",
                    "explanation_en": "Pauses help highlight important information before and after them and increase their impact"
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
                "content_ar": """
المقدمة (الخطاف):
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
التلميح للمستقبل: في الحلقة القادمة، سنكشف عن سر...
                """,
                "content_en": """
Introduction (The Hook):
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
Hinting at the future: In the next episode, we will reveal the secret of...
                """
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية",
                "title_en": "Practical Exercises",
                "content_ar": """
التمارين العملية الفردية:
تمرين التخطيط (20 دقيقة): اختر موضوعاً واكتب له خطافاً ونقطة رئيسية وخاتمة
تمرين التسجيل (25 دقيقة): سجل فقرة مصغرة عن كتابك المفضل

الأنشطة الجماعية:
مصنع الخطافات (20 دقيقة): ابتكار خطافات لمواضيع عادية
التقديم المتناوب (دويتو) (30 دقيقة): تقديم فقرة سفر بشكل متناغم

المهمة اليومية: استمع لبداية برنامجين وحلل نوع الخطاف المستخدم
                """,
                "content_en": """
Individual Practical Exercises:
Planning Exercise (20 minutes): Choose a topic and write a hook, main point, and conclusion for it
Recording Exercise (25 minutes): Record a mini-segment about your favorite book

Group Activities:
Hook Factory (20 minutes): Creating hooks for ordinary topics
Alternating Presentation (Duet) (30 minutes): Presenting a travel segment in harmony

Daily Task: Listen to the beginning of two programs and analyze the type of hook used
                """
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
                },
                {
                    "question_ar": "ما هو العنصر الأكثر أهمية في محتوى الفقرة؟",
                    "question_en": "What is the most important element in paragraph content?",
                    "options_ar": ["التحدث عن مواضيع متعددة", "التركيز على نقطة رئيسية واحدة", "استخدام مصطلحات معقدة", "الإطالة في الشرح"],
                    "options_en": ["Talking about multiple topics", "Focusing on one main point", "Using complex terminology", "Extending explanations"],
                    "correct": 1,
                    "explanation_ar": "التركيز على نقطة رئيسية واحدة في كل فقرة يجعل المحتوى أكثر وضوحاً وتأثيراً",
                    "explanation_en": "Focusing on one main point in each paragraph makes the content clearer and more impactful"
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
                "content_ar": """
الفلسفة وراء الألعاب التنشيطية:
الهدف ليس اللعبة نفسها، بل التفاعل الاجتماعي الذي تخلقه
اللعبة مجرد وسيلة لجعل الجمهور يشعر بالراحة والمتعة
مثال: لعبة "ماذا ستفعل بمليون دولار" تفتح مجالاً للتعارف والإبداع

أنماط الألعاب التنشيطية:
ألعاب التعارف: "ما هي القوة الخارقة التي تريدها؟"
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
الحفاظ على طاقة عالية طوال الوقت
                """,
                "content_en": """
Philosophy behind Icebreaker Games:
The goal is not the game itself, but the social interaction it creates
The game is just a means to make the audience feel comfortable and enjoy
Example: The game "What would you do with a million dollars?" opens the door for acquaintance and creativity

Types of Icebreaker Games:
Acquaintance games: "What superpower would you want?"
Quick intelligence games: General knowledge questions
Guessing games: Guessing characters, movies, passwords
Picture games: Describing pictures without using forbidden words

How to present a game? Clear steps:
Step 1: State the game name enthusiastically
Step 2: Explain the rules simply and clearly
Step 3: Implement the game with motivation and commentary
Step 4: End by thanking participants and smooth transition

Golden tips for success:
Refereeing with fun not harshness
Time management and maintaining program pace
Maintaining high energy throughout
                """
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الرابع: الألعاب التنشيطية",
            "title_en": "Day 4 Quiz: Icebreaker Games",
            "questions": [
                {
                    "question_ar": "ما هو الهدف الرئيسي من الألعاب التنشيطية؟",
                    "question_en": "What is the main goal of icebreaker games?",
                    "options_ar": ["الفوز باللعبة", "التفاعل الاجتماعي وخلق أجواء مريحة", "إطالة وقت البرنامج", "إظهار ذكاء المضيف"],
                    "options_en": ["Winning the game", "Social interaction and creating comfortable atmosphere", "Extending program time", "Showing host's intelligence"],
                    "correct": 1,
                    "explanation_ar": "الهدف الرئيسي هو خلق تفاعل اجتماعي وجعل الجمهور يشعر بالراحة وليس اللعبة نفسها",
                    "explanation_en": "The main goal is to create social interaction and make the audience feel comfortable, not the game itself"
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
                "title_en": "Speed Energy and Its Management",
                "content_ar": """
طاقة السرعة وإدارتها:
هذه الفقرات تحتاج لطاقة عالية وتركيز حاد
تنفس بعمق قبل البدء لشحن طاقتك
حافظ على وتيرة سريعة ولكن مع وضوح في الكلام

أنواع ألعاب السرعة:
أسرع إجابة: يطرح السؤال وأول من يرفع يده يفوز
تحدي الـ 10 ثوانٍ: الإجابة必须在10 ثوانٍ
أغنية وكلمة: معرفة الأغنية أو كلمة مرتبطة بها
أسئلة "بنعم أو لا": أسئلة سريعة مباشرة

فن التعليق على الإجابات:
الإجابة الصحيحة: "أحسنت!"، "انطلقت كالصاروخ!"
الإجابة الخاطئة: "أوه، كادت!"، "الفكرة قريبة!"
نبرة التشويق: استخدم صوتاً مرتفعاً ومتحمساً للإجابات الصحيحة

أدوات التشويق والإثارة:
صوت المؤقت يزيد التوتر
المؤثرات الصوتية (جرس للفوز، صفارة للخطأ)
الخلفية الموسيقية السريعة
                """,
                "content_en": """
Speed Energy and Its Management:
These segments require high energy and sharp focus
Breathe deeply before starting to charge your energy
Maintain a fast pace but with clarity in speech

Types of Speed Games:
Fastest answer: Question is asked and first to raise hand wins
10-second challenge: Answer must be within 10 seconds
Song and word: Identifying the song or related word
"Yes or No" questions: Quick direct questions

Art of Commenting on Answers:
Correct answer: "Well done!", "You took off like a rocket!"
Wrong answer: "Oh, almost!", "The idea is close!"
Suspense tone: Use high and excited voice for correct answers

Tools for Suspense and Excitement:
Timer sound increases tension
Sound effects (bell for win, whistle for wrong)
Fast background music
                """
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الخامس: ألعاب السرعة",
            "title_en": "Day 5 Quiz: Speed Games",
            "questions": [
                {
                    "question_ar": "ما الذي يجب فعله قبل بدء فقرات السرعة؟",
                    "question_en": "What should be done before starting speed segments?",
                    "options_ar": ["التنفس بعمق لشحن الطاقة", "الحديث ببطء", "تجنب المؤثرات الصوتية", "تقليل سرعة الكلام"],
                    "options_en": ["Deep breathing to charge energy", "Speaking slowly", "Avoiding sound effects", "Reducing speech speed"],
                    "correct": 0,
                    "explanation_ar": "التنفس العميق قبل البدء يساعد في شحن الطاقة اللازمة لفقرات السرعة عالية الطاقة",
                    "explanation_en": "Deep breathing before starting helps charge the energy needed for high-energy speed segments"
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
                "title_ar": "محاربة الملل في تقديم المعلومات",
                "title_en": "Combating Boredom in Information Presentation",
                "content_ar": """
محاربة الملل في تقديم المعلومات:
اروي، لا تخبر: بدلاً من "كان الطقس بارداً" قل "كان الصقيع يتسلل عبر سترتي"
اربط المعلومة بحياة المستمع: اجعل المعلومة شخصية ومؤثرة
استخدم التشبيهات: "الإنترنت يشبه الطريق السريع للبيانات"

تبسيط المعلومات المعقدة:
التشبيه: "البلوك تشين يشبه دفتر حسابات موزع"
القصص: ابحث عن القصة الإنسانية خلف المعلومة
الأمثلة العملية: شرح النظريات من خلال تطبيقاتها اليومية

مصادر المعلومات ومصداقيتها:
تحقق دائماً من مصدر المعلومة
استخدم مواقع موثوقة ومراجع علمية
ذكر مصدرك يزيد من مصداقيتك

أنماط الفقرات الثقافية:
"هل تعلم؟" قصيرة وسريعة
"سؤال ثقافي" مع مشاركة الجمهور
"حكاية من التاريخ" بسرد قصصي مشوق
                """,
                "content_en": """
Combating Boredom in Information Presentation:
Narrate, don't tell: Instead of "the weather was cold" say "frost was creeping through my jacket"
Connect information to listener's life: Make information personal and impactful
Use analogies: "The internet is like a highway for data"

Simplifying Complex Information:
Analogy: "Blockchain is like a distributed ledger"
Stories: Find the human story behind the information
Practical examples: Explain theories through their daily applications

Information Sources and Credibility:
Always verify the source of information
Use reliable websites and scientific references
Mentioning your source increases your credibility

Types of Cultural Segments:
"Did you know?" short and fast
"Cultural question" with audience participation
"Tale from history" with exciting narrative
                """
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم السادس: الفقرات الثقافية",
            "title_en": "Day 6 Quiz: Cultural Segments",
            "questions": [
                {
                    "question_ar": "ما هو الفرق بين "أروي" و "أخبر" في تقديم المعلومات؟",
                    "question_en": "What is the difference between 'narrate' and 'tell' in information presentation?",
                    "options_ar": ["لا فرق بينهما", "الأروية تستخدم القصص والتشبيهات", "الأخبار أفضل من الأروية", "الأروية للمعلومات العلمية فقط"],
                    "options_en": ["No difference between them", "Narration uses stories and analogies", "Telling is better than narrating", "Narration is only for scientific information"],
                    "correct": 1,
                    "explanation_ar": "الأروية تعني استخدام القصص والتشبيهات لجعل المعلومة أكثر جاذبية وتأثيراً",
                    "explanation_en": "Narration means using stories and analogies to make information more attractive and impactful"
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
                "content_ar": """
استراتيجيات جذب التفاعل:
الأسئلة المفتوحة: "ما هو أكثر لحظة أعجبتكم؟" بدلاً من "هل أعجبكم البرنامج؟"
استطلاعات الرأي: استخدام أدوات التصويت في التطبيقات
الطلب المباشر: "شاركونا صور طعامكم!"، "ما رأيكم في...؟"

فن إدارة التعليقات المباشرة:
التعليق الإيجابي: اشكر ورد بالاسم ("شكراً لك يا أحمد")
التعليق السلبي: تعامل بذكاء:
اعترف بالمشكلة
أعد صياغة الملاحظة
رد بطريقة مهذبة
التعليق المسيء: تجاهله أو أخرجه بهدوء

أنماط الفقرات التفاعلية:
"الرأي والرأي الآخر": مناقشة قضايا مختلفة الآراء
"قصص من حياتكم": مشاركة قصص شخصية
"استشارات الجمهور": طلب النصائح والأفكار
                """,
                "content_en": """
Strategies for Attracting Interaction:
Open questions: "What moment did you like most?" instead of "Did you like the program?"
Opinion polls: Using voting tools in applications
Direct request: "Share photos of your food!", "What do you think about...?"

Art of Managing Live Comments:
Positive comment: Thank and respond by name ("Thank you, Ahmed")
Negative comment: Deal intelligently:
Acknowledge the problem
Rephrase the observation
Respond politely
Offensive comment: Ignore it or remove it calmly

Types of Interactive Segments:
"Opinion and Counter-opinion": Discussing issues with different opinions
"Stories from your lives": Sharing personal stories
"Audience consultations": Requesting advice and ideas
                """
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم السابع: الفقرات التفاعلية",
            "title_en": "Day 7 Quiz: Interactive Segments",
            "questions": [
                {
                    "question_ar": "كيف تتعامل مع التعليق السلبي بذكاء؟",
                    "question_en": "How do you deal intelligently with negative comments?",
                    "options_ar": ["تجاهله completely", "اعترف بالمشكلة وأعد صياغة الملاحظة", "تهاجم صاحب التعليق", "تغلق التعليقات"],
                    "options_en": ["Ignore it completely", "Acknowledge the problem and rephrase the observation", "Attack the commenter", "Close comments"],
                    "correct": 1,
                    "explanation_ar": "التعامل الذكي مع التعليقات السلبية يشمل الاعتراف بالمشكلة وإعادة صياغة الملاحظة والرد بأدب",
                    "explanation_en": "Intelligent dealing with negative comments includes acknowledging the problem, rephrasing the observation, and responding politely"
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
                "content_ar": """
حقيقة الارتجال:
الارتجال الحقيقي هو تحضير مسبق للأدوات وليس للنص
جهز "طقم النجاة" قبل أن تحتاجه

المواقف الطارئة الشائعة:
صمت مطبق: ضيف لا يتكلم أو عدم تفاعل
مشاكل تقنية: انقطاع الإنترنت، صوت غير واضح
تفاعل ضعيف: لا أحد يشارك
تعليقات محرجة: أسئلة أو ملاحظات غير متوقعة

أدوات الارتجال (طوق النجاة):
الفكاهة: اضحك على الموقف ("يبدو أن الإنترنت قرر أخذ استراحة!")
الاعتراف البسيط: "أعتذر، ظهري انقطع للحظة!"
العودة لنقطة سابقة: "هذا يذكرني بما كنا نتحدث عنه..."
الجعبة السرية: 3 قصص شخصية + 5 أسئلة عامة
                """,
                "content_en": """
The Truth About Improvisation:
Real improvisation is preparing tools in advance, not preparing text
Prepare a "survival kit" before you need it

Common Emergency Situations:
Total silence: Guest doesn't speak or no interaction
Technical problems: Internet disconnection, unclear sound
Weak interaction: No one participates
Embarrassing comments: Unexpected questions or observations

Improvisation Tools (Lifebuoy):
Humor: Laugh at the situation ("It seems the internet decided to take a break!")
Simple admission: "I apologize, my connection was cut for a moment!"
Return to a previous point: "This reminds me of what we were talking about..."
Secret stash: 3 personal stories + 5 general questions
                """
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الثامن: الارتجال",
            "title_en": "Day 8 Quiz: Improvisation",
            "questions": [
                {
                    "question_ar": "ما هي "الجعبة السرية" في الارتجال؟",
                    "question_en": "What is the 'secret stash' in improvisation?",
                    "options_ar": ["ملابس إضافية", "قصص شخصية وأسئلة عامة جاهزة", "أجهزة تقنية", "نصوص مكتوبة"],
                    "options_en": ["Extra clothes", "Ready personal stories and general questions", "Technical devices", "Written scripts"],
                    "correct": 1,
                    "explanation_ar": "الجعبة السرية تشمل قصص شخصية وأسئلة عامة جاهزة تستخدم في المواقف الطارئة",
                    "explanation_en": "The secret stash includes ready personal stories and general questions used in emergency situations"
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
                "content_ar": """
التحضير قبل البرنامج:
البحث عن الضيف: اقرأ عنه، شاهد مقابلات سابقة
تحديد الهدف: ما الرسالة الرئيسية من المقابلة؟
إعداد النقاط الرئيسية: 5-7 نقاط وليس نصاً كاملاً
الاتصال بالضيف: تعريفه بنمط البرنامج والنقاط الرئيسية

فن صياغة الأسئلة:
الأسئلة المفتوحة: "كيف كانت رحلتك؟"، "ما الذي دفعك لهذا القرار؟"
أسئلة المشاعر: "كيف شعرت في تلك اللحظة؟"
الأسئلة المتتابعة: ابنِ على إجابات الضيف

دورك كقائد أوركسترا:
لا تكن النجم: سلط الضوء على الضيف لا على نفسك
الاستماع ثم الكلام: الاستماع الجيد يولد أسئلة أفضل
إدارة الوقت: أنهِ الحوار بلباقة عندما يحين الموعد
                """,
                "content_en": """
Preparation Before the Program:
Research the guest: Read about them, watch previous interviews
Define the goal: What is the main message from the interview?
Prepare main points: 5-7 points not a full text
Contact the guest: Introduce them to the program style and main points

Art of Formulating Questions:
Open questions: "How was your journey?", "What drove you to this decision?"
Emotion questions: "How did you feel at that moment?"
Follow-up questions: Build on the guest's answers

Your Role as Orchestra Conductor:
Don't be the star: Spotlight the guest not yourself
Listen then speak: Good listening generates better questions
Time management: End the dialogue politely when time comes
                """
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم التاسع: إدارة الحوار",
            "title_en": "Day 9 Quiz: Dialogue Management",
            "questions": [
                {
                    "question_ar": "ما هو دور المضيف كقائد أوركسترا؟",
                    "question_en": "What is the host's role as an orchestra conductor?",
                    "options_ar": ["أن يكون النجم الرئيسي", "تسليط الضوء على الضيف", "الحديث أكثر من الضيف", "عدم الاستماع للضيف"],
                    "options_en": ["Being the main star", "Spotlighting the guest", "Talking more than the guest", "Not listening to the guest"],
                    "correct": 1,
                    "explanation_ar": "دور المضيف كقائد أوركسترا هو تسليط الضوء على الضيف وإدارة الحوار لا الهيمنة عليه",
                    "explanation_en": "The host's role as orchestra conductor is to spotlight the guest and manage the dialogue not dominate it"
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
                "content_ar": """
هندسة البرنامج:
الفكرة: ماذا تقدم؟ (ترفيه، تعليم، إلهام)
الجمهور: لمن تقدمه؟ (شباب، عائلات، متخصصون)
الهدف: لماذا تقدمه؟ (تسلية، معرفة، مجتمع)

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
طريقة الترحيب الخاصة
                """,
                "content_en": """
Program Engineering:
Idea: What do you offer? (Entertainment, education, inspiration)
Audience: Who do you offer it to? (Youth, families, specialists)
Goal: Why do you offer it? (Entertainment, knowledge, community)

Preparation Routine:
Research and information gathering
Writing main points
Preparing segments
Technical testing
Prior announcement

Flexible Script:
Not a text you read, but a roadmap
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
Special welcome method
                """
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم العاشر: بناء البرنامج",
            "title_en": "Day 10 Quiz: Program Building",
            "questions": [
                {
                    "question_ar": "ما هو السكريبت المرن؟",
                    "question_en": "What is a flexible script?",
                    "options_ar": ["نص ثابت تقرأه حرفياً", "خارطة طريق وليس نصاً جامداً", "قائمة بالكلمات الصعبة", "سجل للوقت فقط"],
                    "options_en": ["Fixed text you read literally", "Roadmap not a rigid text", "List of difficult words", "Time record only"],
                    "correct": 1,
                    "explanation_ar": "السكريبت المرن هو خارطة طريق تحتوي على النقاط الرئيسية وليس نصاً جامداً يجب قراءته حرفياً",
                    "explanation_en": "A flexible script is a roadmap containing main points not a rigid text that must be read literally"
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
                "content_ar": """
الموسيقى والمؤثرات الصوتية:
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
الضغط: توحيد مستوى الصوت
                """,
                "content_en": """
Music and Sound Effects:
The salt not the main dish: Excess spoils the experience
Introduction and conclusion: Distinctive and short music
Transitions: Light music between segments

Choosing Suitable Music:
Fun programs: Fast and rhythmic music
Serious programs: Calm music or no music
Sources: Use royalty-free music

Basic Audio Processing:
Noise removal: Removes microphone hiss
Equalization: Improves clarity
Compression: Unifies sound level
                """
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الحادي عشر: الإخراج الصوتي",
            "title_en": "Day 11 Quiz: Audio Production",
            "questions": [
                {
                    "question_ar": "ما دور الموسيقى في البرنامج الصوتي؟",
                    "question_en": "What is the role of music in an audio program?",
                    "options_ar": ["الطبق الرئيسي", "الملح الذي يضيف نكهة", "تغطية صوت المضيف", "إطالة مدة البرنامج"],
                    "options_en": ["The main dish", "The salt that adds flavor", "Covering the host's voice", "Extending program duration"],
                    "correct": 1,
                    "explanation_ar": "الموسيقى مثل الملح تضفي نكهة للبرنامج ولكن الإفراط فيها يفسد التجربة",
                    "explanation_en": "Music is like salt that adds flavor to the program but excess spoils the experience"
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
                "title_en": "Storytelling (The Art of Narrative)",
                "content_ar": """
الستوري تيلينغ (فن سرد القصة):
الهيكل الذهبي:
البداية: الشخصية في سياقها العادي
الحدث المحفز: شيء يغير كل شيء
الرحلة والصراع: التحديات
الذروة: لحظة الحسم
النهاية: التغيير والدرس

الدعابة الذكية:
اضحك على نفسك لا على الآخرين
المفارقة: "هدفي كان رياضياً محترفاً ولكن الأريكة كانت أقوى!"
المراقبة: التعليق على مواقف الحياة اليومية

التوقيت الكوميدي:
الوقفة قبل النكتة: تزيد التشويق
الوقفة بعد النكتة: تعطي وقتاً للضحك
الإيقاع: التناوب بين السرعة والبطء
                """,
                "content_en": """
Storytelling (The Art of Narrative):
The Golden Structure:
Beginning: Character in their normal context
Triggering event: Something changes everything
Journey and conflict: Challenges
Climax: Moment of decision
End: Change and lesson

Intelligent Humor:
Laugh at yourself not at others
Irony: "My goal was to be a professional athlete but the couch was stronger!"
Observation: Commenting on daily life situations

Comedic Timing:
Pause before the joke: Increases suspense
Pause after the joke: Gives time to laugh
Rhythm: Alternating between speed and slowness
                """
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الثاني عشر: التقديم المتقدم",
            "title_en": "Day 12 Quiz: Advanced Presentation",
            "questions": [
                {
                    "question_ar": "ما هي المرحلة الأولى في الهيكل الذهبي لسرد القصة؟",
                    "question_en": "What is the first stage in the golden structure of storytelling?",
                    "options_ar": ["الذروة", "البداية مع الشخصية في سياقها العادي", "النهاية", "الصراع"],
                    "options_en": ["The climax", "Beginning with character in normal context", "The end", "The conflict"],
                    "correct": 1,
                    "explanation_ar": "المرحلة الأولى هي البداية التي تعرض الشخصية في سياقها العادي قبل الحدث المحفز",
                    "explanation_en": "The first stage is the beginning that presents the character in their normal context before the triggering event"
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
                "content_ar": """
أنماط الشخصيات في الجمهور:
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
مراقبة نوعية التفاعل
                """,
                "content_en": """
Personality Types in the Audience:
Interactive: Comments and asks constantly
Supporter: Always present but rarely interacts
Critic: Only sees mistakes
Shy: Only listens

Building Community:
Repetition: Consistency with timing creates habit
Personal interaction: Calling them by names
Fulfilling desires: Customizing segments based on their requests

Collecting Feedback:
Quick surveys
Direct questions
Monitoring interaction quality
                """
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الثالث عشر: فهم الجمهور",
            "title_en": "Day 13 Quiz: Understanding Audience",
            "questions": [
                {
                    "question_ar": "كيف تبني مجتمعاً حول برنامجك؟",
                    "question_en": "How do you build a community around your program?",
                    "options_ar": ["بعدم الالتزام بموعد ثابت", "بالتكرار والمواظبة على الموعد", "بتجنب التفاعل الشخصي", "بعدم الرد على الطلبات"],
                    "options_en": ["By not committing to a fixed time", "By repetition and consistency with timing", "By avoiding personal interaction", "By not responding to requests"],
                    "correct": 1,
                    "explanation_ar": "المواظبة على موعد ثابت تخلق عادة عند الجمهور وتساهم في بناء مجتمع مخلص",
                    "explanation_en": "Consistency with a fixed time creates a habit for the audience and contributes to building a loyal community"
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
                "title_ar": "فنون الربط",
                "title_en": "Linking Arts",
                "content_ar": """
فنون الربط:
اللفظي: "والحديث عن السفر يحضرني لعبة عن دول العالم"
الصوتي: استخدام موسيقى انتقالية
المنطقي: "بعد كل هذا المرح، حان وقت الاستراحة بمعلومة مدهشة"

التمارين العملية الفردية:
التدريب النهائي الكبير (70 دقيقة): تسجيل حلقة برنامج كاملة 15-20 دقيقة

الأنشطة الجماعية:
البث المباشر الوهمي (90 دقيقة): محاكاة بث حي بفريق كامل

المهمة اليومية: سجل الحلقة كاملة وقيم أداءك
                """,
                "content_en": """
Linking Arts:
Verbal: "And talking about travel brings me to a game about world countries"
Audio: Using transition music
Logical: "After all this fun, it's time for a break with an amazing fact"

Individual Practical Exercises:
Final Comprehensive Training (70 minutes): Recording a full program episode 15-20 minutes

Group Activities:
Simulated Live Broadcast (90 minutes): Simulating a live broadcast with a full team

Daily Task: Record the full episode and evaluate your performance
                """
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الرابع عشر: التطبيق الشامل",
            "title_en": "Day 14 Quiz: Comprehensive Application",
            "questions": [
                {
                    "question_ar": "ما هو الربط اللفظي؟",
                    "question_en": "What is verbal linking?",
                    "options_ar": ["استخدام الموسيقى فقط", "ربط الفقرات بكلمات مناسبة", "الصمت بين الفقرات", "التحدث بلغة أجنبية"],
                    "options_en": ["Using music only", "Linking segments with appropriate words", "Silence between segments", "Speaking in a foreign language"],
                    "correct": 1,
                    "explanation_ar": "الربط اللفظي يعني استخدام كلمات مناسبة لربط الفقرات بسلاسة مثل الانتقال من موضوع لآخر",
                    "explanation_en": "Verbal linking means using appropriate words to link segments smoothly like transitioning from one topic to another"
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
                "content_ar": """
التقييم الذاتي الموضوعي:
استمع كجمهور: هل أنت مستمتع؟
استمع كخبير: حلل الوضوح، الطلاقة، التنظيم

خطة التطوير المستمر:
مواكبة الترندات
التعلم المستمر
طلب التغذية الراجعة

الاستدامة:
ضع حدوداً للراحة
تذكر "لماذا" بدأت
احتفل بالإنجازات

التمارين العملية الفردية:
تمرين التقييم الذاتي (30 دقيقة): تقييم تسجيل الحلقة الكاملة
تمرين التخطيط الاستراتيجي (30 دقيقة): خطة 90 يوم القادمة

الأنشطة الجماعية:
حلقة التغذية الراجعة (60 دقيقة): تقديم ملاحظات بناءة
احتفال التخرج (45 دقيقة): مشاركة الخطط المستقبلية

المهمة اليومية: اكتب رسالة لنفسك في الماضي
                """,
                "content_en": """
Objective Self-Evaluation:
Listen as an audience: Are you enjoying?
Listen as an expert: Analyze clarity, fluency, organization

Continuous Development Plan:
Keeping up with trends
Continuous learning
Requesting feedback

Sustainability:
Set boundaries for rest
Remember "why" you started
Celebrate achievements

Individual Practical Exercises:
Self-Evaluation Exercise (30 minutes): Evaluating the full episode recording
Strategic Planning Exercise (30 minutes): Plan for the next 90 days

Group Activities:
Feedback Circle (60 minutes): Providing constructive feedback
Graduation Celebration (45 minutes): Sharing future plans

Daily Task: Write a letter to your past self
                """
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الخامس عشر: التطوير المستمر",
            "title_en": "Day 15 Quiz: Continuous Development",
            "questions": [
                {
                    "question_ar": "ما هو مفتاح الاستدامة في العمل الصوتي؟",
                    "question_en": "What is the key to sustainability in audio work?",
                    "options_ar": ["العمل دون توقف", "وضع حدود للراحة وتذكر سبب البدء", "تجنب التقييم الذاتي", "عدم الاحتفال بالإنجازات"],
                    "options_en": ["Working non-stop", "Setting boundaries for rest and remembering why you started", "Avoiding self-evaluation", "Not celebrating achievements"],
                    "correct": 1,
                    "explanation_ar": "الاستدامة تعني الحفاظ على الطاقة والشغف من خلال وضع حدود للراحة وتذكر الهدف الأصلي",
                    "explanation_en": "Sustainability means maintaining energy and passion by setting boundaries for rest and remembering the original goal"
                }
            ]
        }
    }
}

# =============================================================================
# USER PROGRESS TRACKING
# =============================================================================

user_progress = {}
user_quiz_responses = {}
user_language = {}  # 'ar' for Arabic, 'en' for English

# =============================================================================
# TELEGRAM BOT CLASS
# =============================================================================

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
        
        # Callback query handlers
        self.application.add_handler(CallbackQueryHandler(self.handle_button_click, pattern="^(main_menu|today_training|all_days|progress|quizzes_menu|day_|material_|quiz_|answer_|next_|back_to_day|back_to_menu|lang_)"))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    def get_user_language(self, user_id):
        return user_language.get(user_id, 'ar')  # Default to Arabic
    
    def get_text(self, user_id, arabic_text, english_text):
        lang = self.get_user_language(user_id)
        return arabic_text if lang == 'ar' else english_text
    
    # =========================================================================
    # COMMAND HANDLERS
    # =========================================================================
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_id = user.id
        
        # Initialize user progress if new user
        if user_id not in user_progress:
            user_progress[user_id] = {
                "current_day": 1,
                "completed_days": set(),
                "quiz_scores": {},
                "last_activity": datetime.now().isoformat()
            }
        
        # Initialize language if not set
        if user_id not in user_language:
            user_language[user_id] = 'ar'  # Default to Arabic
        
        welcome_text = self.get_text(user_id,
            f"""
🎓 **مرحباً بك في البرنامج التدريبي الشامل لإعداد مضيف البرامج الصوتية المحترف، {user.first_name}!**

هذا البرنامج الشامل سيرشدك خلال 15 يوماً من التدريب المكثف مع:
• 📚 مواد تدريبية يومية
• 📊 اختبارات تفاعلية  
• 📈 متابعة التقدم
• 🎯 تمارين عملية

**كيفية استخدام البوت:**
• استخدم /menu للوصول إلى جميع الميزات
• استخدم /today للتدريب اليومي
• استخدم /progress لمتابعة تقدمك
• استخدم /language لتغيير اللغة

مستعد لبدء رحلة التعلم؟ اضغط على الزر أدناه! 🚀
            """,
            f"""
🎓 **Welcome to the Comprehensive Training Program for Professional Audio Hosts, {user.first_name}!**

This comprehensive program will guide you through 15 days of intensive training with:
• 📚 Daily training materials
• 📊 Interactive quizzes  
• 📈 Progress tracking
• 🎯 Practical exercises

**How to use this bot:**
• Use /menu to access all features
• Use /today for today's training
• Use /progress to check your progress
• Use /language to change language

Ready to begin your learning journey? Click the button below! 🚀
            """
        )
        
        keyboard = [
            [InlineKeyboardButton(
                self.get_text(user_id, "🚀 ابدأ التعلم", "🚀 Start Learning"), 
                callback_data="today_training"
            )],
            [InlineKeyboardButton(
                self.get_text(user_id, "📚 القائمة الرئيسية", "📚 Main Menu"), 
                callback_data="main_menu"
            )]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def change_language(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        keyboard = [
            [InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar")],
            [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "**Please choose your language / الرجاء اختيار اللغة:**",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        keyboard = [
            [InlineKeyboardButton(
                self.get_text(user_id, "📅 التدريب اليومي", "📅 Today's Training"), 
                callback_data="today_training"
            )],
            [InlineKeyboardButton(
                self.get_text(user_id, "📚 جميع أيام التدريب", "📚 All Training Days"), 
                callback_data="all_days"
            )],
            [InlineKeyboardButton(
                self.get_text(user_id, "📊 تقدمي", "📊 My Progress"), 
                callback_data="progress"
            )],
            [InlineKeyboardButton(
                self.get_text(user_id, "❓ الاختبارات", "❓ Take Quizzes"), 
                callback_data="quizzes_menu"
            )],
            [InlineKeyboardButton(
                self.get_text(user_id, "🌐 تغيير اللغة", "🌐 Change Language"), 
                callback_data="lang_menu"
            )]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        menu_text = self.get_text(user_id,
            "🏫 **القائمة الرئيسية للبرنامج التدريبي**\n\nاختر مسار التعلم:",
            "🏫 **Training Program Menu**\n\nChoose your learning path:"
        )
        
        await update.message.reply_text(menu_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_progress(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        progress = user_progress.get(user_id, {})
        
        current_day = progress.get("current_day", 1)
        completed_days = len(progress.get("completed_days", set()))
        total_days = 15
        
        progress_text = self.get_text(user_id,
            f"""
📊 **تقدمك في التعلم**

**اليوم الحالي:** {current_day}/15
**الأيام المكتملة:** {completed_days}/15
**نسبة الإنجاز:** {round((completed_days/total_days)*100)}%

**نتائج الاختبارات:**
            """,
            f"""
📊 **Your Learning Progress**

**Current Day:** {current_day}/15
**Completed Days:** {completed_days}/15
**Completion Rate:** {round((completed_days/total_days)*100)}%

**Quiz Scores:**
            """
        )
        
        # Add quiz scores
        quiz_scores = progress.get("quiz_scores", {})
        for day, score in quiz_scores.items():
            progress_text += f"• {self.get_text(user_id, f'اليوم {day}', f'Day {day}')}: {score}%\n"
        
        if not quiz_scores:
            progress_text += self.get_text(user_id, "• لم تحاول أي اختبار بعد\n", "• No quiz attempts yet\n")
        
        progress_text += self.get_text(user_id, "\nاستمر في التقدم! أنت تقوم بعمل رائع! 💪", "\nKeep going! You're doing great! 💪")
        
        keyboard = [
            [InlineKeyboardButton(
                self.get_text(user_id, "📚 متابعة التعلم", "📚 Continue Learning"), 
                callback_data="today_training"
            )],
            [InlineKeyboardButton(
                self.get_text(user_id, "🏠 القائمة الرئيسية", "🏠 Main Menu"), 
                callback_data="main_menu"
            )]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(progress_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_todays_training(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        progress = user_progress.get(user_id, {})
        current_day = progress.get("current_day", 1)
        
        await self.show_day_overview(update, current_day)
    
    # =========================================================================
    # CALLBACK QUERY HANDLERS
    # =========================================================================
    
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
        elif data.startswith("answer_"):
            parts = data.split("_")
            day_num = int(parts[1])
            question_index = int(parts[2])
            answer_index = int(parts[3])
            await self.handle_quiz_answer(query, day_num, question_index, answer_index)
        elif data.startswith("next_"):
            parts = data.split("_")
            day_num = int(parts[1])
            material_index = int(parts[2])
            await self.show_next_material(query, day_num, material_index)
        elif data.startswith("lang_"):
            lang = data.split("_")[1]
            user_language[user_id] = lang
            await query.edit_message_text(
                self.get_text(user_id, 
                    "✅ **تم تغيير اللغة إلى العربية**",
                    "✅ **Language changed to English**"
                ),
                parse_mode='Markdown'
            )
            await self.show_main_menu_callback(query)
        elif data == "lang_menu":
            await self.change_language_callback(query)
        elif data == "back_to_day":
            day_num = int(context.user_data.get("current_day", 1))
            await self.show_day_overview_callback(query, day_num)
        elif data == "back_to_menu":
            await self.show_main_menu_callback(query)
    
    async def change_language_callback(self, query):
        user_id = query.from_user.id
        keyboard = [
            [InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar")],
            [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "**Please choose your language / الرجاء اختيار اللغة:**",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def show_main_menu_callback(self, query):
        user_id = query.from_user.id
        keyboard = [
            [InlineKeyboardButton(
                self.get_text(user_id, "📅 التدريب اليومي", "📅 Today's Training"), 
                callback_data="today_training"
            )],
            [InlineKeyboardButton(
                self.get_text(user_id, "📚 جميع أيام التدريب", "📚 All Training Days"), 
                callback_data="all_days"
            )],
            [InlineKeyboardButton(
                self.get_text(user_id, "📊 تقدمي", "📊 My Progress"), 
                callback_data="progress"
            )],
            [InlineKeyboardButton(
                self.get_text(user_id, "❓ الاختبارات", "❓ Take Quizzes"), 
                callback_data="quizzes_menu"
            )],
            [InlineKeyboardButton(
                self.get_text(user_id, "🌐 تغيير اللغة", "🌐 Change Language"), 
                callback_data="lang_menu"
            )]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        menu_text = self.get_text(user_id,
            "🏫 **القائمة الرئيسية للبرنامج التدريبي**\n\nاختر مسار التعلم:",
            "🏫 **Training Program Menu**\n\nChoose your learning path:"
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
        total_days = 15
        
        progress_text = self.get_text(user_id,
            f"""
📊 **تقدمك في التعلم**

**اليوم الحالي:** {current_day}/15
**الأيام المكتملة:** {completed_days}/15
**نسبة الإنجاز:** {round((completed_days/total_days)*100)}%

**نتائج الاختبارات:**
            """,
            f"""
📊 **Your Learning Progress**

**Current Day:** {current_day}/15
**Completed Days:** {completed_days}/15
**Completion Rate:** {round((completed_days/total_days)*100)}%

**Quiz Scores:**
            """
        )
        
        quiz_scores = progress.get("quiz_scores", {})
        for day, score in quiz_scores.items():
            progress_text += f"• {self.get_text(user_id, f'اليوم {day}', f'Day {day}')}: {score}%\n"
        
        if not quiz_scores:
            progress_text += self.get_text(user_id, "• لم تحاول أي اختبار بعد\n", "• No quiz attempts yet\n")
        
        progress_text += self.get_text(user_id, "\nاستمر في التقدم! أنت تقوم بعمل رائع! 💪", "\nKeep going! You're doing great! 💪")
        
        keyboard = [
            [InlineKeyboardButton(
                self.get_text(user_id, "📚 متابعة التعلم", "📚 Continue Learning"), 
                callback_data="today_training"
            )],
            [InlineKeyboardButton(
                self.get_text(user_id, "🏠 القائمة الرئيسية", "🏠 Main Menu"), 
                callback_data="main_menu"
            )]
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
        
        await query.edit_message_text(
            self.get_text(user_id,
                "📚 **جميع أيام التدريب**\n\nاختر يوماً لعرض محتواه:",
                "📚 **All Training Days**\n\nSelect a day to view its content:"
            ),
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
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
        
        await query.edit_message_text(
            self.get_text(user_id,
                "❓ **الاختبارات المتاحة**\n\nاختبر معرفتك بعد كل يوم تدريبي:",
                "❓ **Available Quizzes**\n\nTest your knowledge after each training day:"
            ),
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    # =========================================================================
    # DAY OVERVIEW AND MATERIALS
    # =========================================================================
    
    async def show_day_overview(self, update, day_num):
        user_id = update.effective_user.id if hasattr(update, 'effective_user') else update.from_user.id
        day_data = TRAINING_DATA.get(day_num, {})
        day_title = self.get_text(user_id, day_data.get("title_ar", f"اليوم {day_num}"), day_data.get("title_en", f"Day {day_num}"))
        
        overview_text = f"""
{day_title}

{self.get_text(user_id, "**المواد المتاحة:**", "**Available Materials:**")}
"""
        
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
        else:  # It's a callback query
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
        
        if material['type'] == 'text':
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
                keyboard = [keyboard]  # Wrap in another list for single row
            
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
    
    async def show_next_material(self, query, day_num, material_index):
        await self.show_material(query, day_num, material_index)
    
    # =========================================================================
    # QUIZ SYSTEM
    # =========================================================================
    
    async def start_quiz(self, query, day_num):
        user_id = query.from_user.id
        day_data = TRAINING_DATA.get(day_num, {})
        quiz_data = day_data.get("quiz")
        
        if not quiz_data:
            await query.answer(self.get_text(user_id, "لا يوجد اختبار لهذا اليوم", "No quiz available for this day"))
            return
        
        user_quiz_responses[user_id] = {
            "day": day_num,
            "current_question": 0,
            "answers": [],
            "score": 0
        }
        
        await self.show_quiz_question(query, day_num, 0)
    
    async def show_quiz_question(self, query, day_num, question_index):
        user_id = query.from_user.id
        day_data = TRAINING_DATA.get(day_num, {})
        quiz_data = day_data.get("quiz")
        questions = quiz_data.get("questions", [])
        
        if question_index >= len(questions):
            await self.finish_quiz(query, day_num)
            return
        
        question_data = questions[question_index]
        
        question_text = self.get_text(user_id,
            f"""
❓ **السؤال {question_index + 1}/{len(questions)}**

{question_data['question_ar']}
            """,
            f"""
❓ **Question {question_index + 1}/{len(questions)}**

{question_data['question_en']}
            """
        )
        
        # Create answer buttons
        keyboard = []
        options = question_data['options_ar'] if self.get_user_language(user_id) == 'ar' else question_data['options_en']
        for i, option in enumerate(options):
            keyboard.append([InlineKeyboardButton(option, callback_data=f"answer_{day_num}_{question_index}_{i}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(question_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def handle_quiz_answer(self, query, day_num, question_index, answer_index):
        user_id = query.from_user.id
        day_data = TRAINING_DATA.get(day_num, {})
        quiz_data = day_data.get("quiz")
        questions = quiz_data.get("questions", [])
        
        if user_id not in user_quiz_responses or user_quiz_responses[user_id]["day"] != day_num:
            await query.answer(self.get_text(user_id, "انتهت جلسة الاختبار. يرجى البدء من جديد.", "Quiz session expired. Please start the quiz again."))
            return
        
        question_data = questions[question_index]
        is_correct = (answer_index == question_data['correct'])
        
        # Store the answer
        user_quiz_responses[user_id]["answers"].append({
            "question_index": question_index,
            "answer_index": answer_index,
            "is_correct": is_correct
        })
        
        if is_correct:
            user_quiz_responses[user_id]["score"] += 1
        
        # Show result
        result_text = self.get_text(user_id,
            f"""
{'✅ صح!' if is_correct else '❌ خطأ'}

**الشرح:** {question_data['explanation_ar']}
            """,
            f"""
{'✅ Correct!' if is_correct else '❌ Incorrect'}

**Explanation:** {question_data['explanation_en']}
            """
        )
        
        keyboard = [[InlineKeyboardButton(
            self.get_text(user_id, "السؤال التالي ➡️", "Next Question ➡️"), 
            callback_data=f"next_question_{day_num}_{question_index+1}"
        )]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(result_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def finish_quiz(self, query, day_num):
        user_id = query.from_user.id
        quiz_responses = user_quiz_responses.get(user_id, {})
        
        total_questions = len(TRAINING_DATA[day_num]["quiz"]["questions"])
        score = quiz_responses.get("score", 0)
        percentage = round((score / total_questions) * 100)
        
        # Update user progress
        if user_id not in user_progress:
            user_progress[user_id] = {"quiz_scores": {}, "completed_days": set()}
        
        user_progress[user_id]["quiz_scores"][day_num] = percentage
        user_progress[user_id]["completed_days"].add(day_num)
        user_progress[user_id]["current_day"] = min(day_num + 1, 15)
        
        # Determine performance message
        if percentage >= 90:
            performance = self.get_text(user_id, "🎉 ممتاز! أنت طالب نجم!", "🎉 Excellent! You're a star student!")
        elif percentage >= 70:
            performance = self.get_text(user_id, "👍 عمل رائع! تفهم المواد جيداً!", "👍 Great job! You understand the material well!")
        elif percentage >= 50:
            performance = self.get_text(user_id, "📚 جهد جيد! راجع المواد وحاول مرة أخرى!", "📚 Good effort! Review the materials and try again!")
        else:
            performance = self.get_text(user_id, "💪 لا تستسلم! راجع مواد اليوم وأعد الاختبار.", "💪 Don't give up! Review the day's materials and retake the quiz.")
        
        result_text = self.get_text(user_id,
            f"""
📊 **اكتمل الاختبار!**

**نتائج اختبار اليوم {day_num}:**
• النتيجة: {score}/{total_questions}
• النسبة: {percentage}%

{performance}

**ما التالي؟**
• راجع مواد اليوم إذا needed
• انتقل إلى اليوم التالي
• أعد هذا الاختبار لتحسين نتيجتك
            """,
            f"""
📊 **Quiz Complete!**

**Day {day_num} Quiz Results:**
• Score: {score}/{total_questions}
• Percentage: {percentage}%

{performance}

**What's next?**
• Review today's materials if needed
• Move on to the next day
• Retake this quiz to improve your score
            """
        )
        
        keyboard = [
            [InlineKeyboardButton(
                self.get_text(user_id, "📖 مراجعة المواد", "📖 Review Materials"), 
                callback_data=f"day_{day_num}"
            )],
            [InlineKeyboardButton(
                self.get_text(user_id, "❓ إعادة الاختبار", "❓ Retake Quiz"), 
                callback_data=f"quiz_{day_num}"
            )],
            [InlineKeyboardButton(
                self.get_text(user_id, "📅 اليوم التالي", "📅 Next Day"), 
                callback_data=f"day_{day_num+1}" if day_num < 15 else "main_menu"
            )],
            [InlineKeyboardButton(
                self.get_text(user_id, "🏠 القائمة الرئيسية", "🏠 Main Menu"), 
                callback_data="main_menu"
            )]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(result_text, reply_markup=reply_markup, parse_mode='Markdown')
        
        # Clean up quiz responses
        if user_id in user_quiz_responses:
            del user_quiz_responses[user_id]
    
    # =========================================================================
    # MESSAGE HANDLER
    # =========================================================================
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        text = update.message.text
        
        if any(greeting in text.lower() for greeting in ['hello', 'hi', 'hey', 'hola', 'مرحبا', 'السلام', 'اهلا']):
            await update.message.reply_text(
                self.get_text(user_id,
                    "👋 مرحباً! استخدم /menu للوصول إلى البرنامج التدريبي أو /start لبدء رحلة التعلم!",
                    "👋 Hello! Use /menu to access the training program or /start to begin your learning journey!"
                )
            )
        else:
            await update.message.reply_text(
                self.get_text(user_id,
                    "أنا هنا لمساعدتك في التدريب! استخدم /menu لرؤية جميع الخيارات المتاحة.",
                    "I'm here to help with your training! Use /menu to see all available options."
                )
            )

# =============================================================================
# FLASK ROUTES & BOT INITIALIZATION
# =============================================================================

@app.route('/')
def home():
    return "Training Bot is running successfully! 🚀"

@app.route('/health')
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

def run_bot():
    token = os.environ.get('TELEGRAM_TOKEN')
    if not token:
        logging.error("No TELEGRAM_TOKEN found in environment variables")
        return
    
    bot = TrainingBot(token)
    bot.application.run_polling()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    # Start bot in background thread
    import threading
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Start Flask app
    app.run(host='0.0.0.0', port=port)
