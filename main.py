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
                "content_ar": "في العالم الصوتي، أنت المسؤول الوحيد عن صناعة المشاعر وتوجيه الطاقة\nصوتك ليس مجرد وسيلة نقل معلومات، بل هو أداة صناعة المشاعر\n\nمثال: عندما تتحدث عن موضوع مفرح، اجعل نبرة صوتك مرتفعة ومليئة بالحيوية\nمثال: عندما تقدم موضوعاً جاداً، اخفض نبرة صوتك وأعطِ كل كلمة وزنها\n\nالاستماع النشط ليس سماعاً:\nالسماع: عملية سلبية تتم دون تركيز\nالاستماع: عملية نشطة تتطلب التركيز والفهم والاستجابة الذكية\n\nكيف تستمتع بنشاط؟\nلا تنتظر دورك للكلام: ركز على ما يقال الآن وليس على ردك القادم\nالرد على المشاعر: انتبه لنبرة صوت المتحدث\nالأسئلة التوضيحية: هل تقصد أن...؟ ماذا حدث بعد ذلك؟\n\nصناعة هويتك الصوتية:\nالثقة: نابعة من إيمانك بقيمتك وما تقدمه\nالطاقة: اجعل طاقتك إيجابية ومعدية حتى في الأيام العادية\nالأصالة: كن صادقاً في ردودك وتفاعلك، لا تتصنع شخصية غيرك",
                "content_en": "In the audio world, you are solely responsible for creating emotions and directing energy\nYour voice is not just a means of transmitting information, but a tool for creating emotions\n\nExample: When talking about a happy topic, make your tone high and full of vitality\nExample: When presenting a serious topic, lower your tone and give each word its weight\n\nActive listening is not just hearing:\nHearing: A passive process without focus\nListening: An active process requiring concentration, understanding, and intelligent response\n\nHow to listen actively?\nDon't wait for your turn to speak: Focus on what is being said now, not your next response\nRespond to emotions: Pay attention to the speaker's tone\nClarifying questions: Do you mean that...? What happened next?\n\nBuilding your vocal identity:\nConfidence: Stemming from your belief in your value and what you offer\nEnergy: Make your energy positive and contagious even on ordinary days\nAuthenticity: Be honest in your responses and interactions, don't fake another personality"
            },
            {
                "type": "text",
                "title_ar": "التمارين العملية",
                "title_en": "Practical Exercises",
                "content_ar": "التمارين العملية الفردية:\nتمرين التحليل (15 دقيقة): استمع لمضيف مشهور وحلل 3 مواقف استخدم فيها الاستماع النشط\nتمرين التسجيل والتحليل الذاتي (30 دقيقة): سجل صوتك وأنت تتحدث عن كتاب أو فيلم، ثم حلل سرعتك، وضوحك، ونبرة صوتك\nتمرين الارتجال (15 دقيقة): تحدث عن كلمة عشوائية لمدة 60 ثانية دون توقف\n\nالأنشطة الجماعية:\nلعبة همسة السلسلة (15 دقيقة): لتدريب دقة الاستماع ونقل المعلومة\nالمقابلة النشطة (20 دقيقة): يتدرب المتدربون على الاستماع بهدف الفهم وليس الرد\n\nالمهمة اليومية: استمع إلى مضيف آخر وحلل طريقته في التعامل مع ضيوفه وجمهوره",
                "content_en": "Individual Practical Exercises:\nAnalysis Exercise (15 minutes): Listen to a famous host and analyze 3 situations where they used active listening\nRecording and Self-Analysis Exercise (30 minutes): Record your voice while talking about a book or movie, then analyze your speed, clarity, and tone\nImprovisation Exercise (15 minutes): Talk about a random word for 60 seconds without stopping\n\nGroup Activities:\nChain Whisper Game (15 minutes): To train listening accuracy and information transfer\nActive Interview (20 minutes): Trainees practice listening for understanding rather than responding\n\nDaily Task: Listen to another host and analyze their way of dealing with guests and audience"
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
                "content_ar": "الروتين اليومي للإحماء الصوتي:\nالتنفس الحجابي: تنفس بعمق من الأنف بحيث يتمدد بطنك، وازفر ببطء من الفم\nتمرين الشفاه: تحريك الشفاه معاً وتحريكهما في كل الاتجاهات\nتمرين اللسان: لمس سقف الحلق وتحريك اللسان بشكل دائري\n\nوضوح الكلام هو الاحترافية ذاتها:\nركز على مخارج الحروف، خاصة الحروف التي تحتاج لجهد\nتخيل أنك ترمي الكلمات مثل السهام، يجب أن تكون واضحة ومستقيمة\nمثال: عند نطق كلمة مستقبل، ركز على كل حرف وخاصة حرف القاف\n\nموسيقى الكلام: كيف تصنع لحناً يجذب الأذن؟\nالنبرة: التغيير بين العالي والمنخفض يخلق تشويقاً\nالسرعة: سريعة للإثارة، بطيئة للتأكيد\nالوقفات: استخدمها قبل وبعد المعلومات المهمة\n\nلغة الجسد للصوت:\nحتى لو لم يراك أحد، فإن ابتسامتك تسمع\nتحدث ووجهك يعبر، ويديك تتحركان",
                "content_en": "Daily Vocal Warm-up Routine:\nDiaphragmatic breathing: Breathe deeply through your nose so your abdomen expands, and exhale slowly through your mouth\nLip exercise: Move lips together and move them in all directions\nTongue exercise: Touch the roof of the mouth and move the tongue in circles\n\nSpeech clarity is professionalism itself:\nFocus on letter articulation, especially letters that require effort\nImagine throwing words like arrows - they should be clear and straight\nExample: When pronouncing the word future, focus on each letter especially the Qaf sound\n\nMusic of speech: How to create a melody that attracts the ear?\nTone: Changing between high and low creates suspense\nSpeed: Fast for excitement, slow for emphasis\nPauses: Use them before and after important information\n\nBody language for voice:\nEven if no one sees you, your smile can be heard\nSpeak with expressive facial expressions and hand movements"
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
                "content_ar": "المقدمة (الخطاف):\nلديك 10-15 ثانية فقط للإمساك بانتباه المستمع\nأنواع الخطافات الفعالة:\nالسؤال الصادم: هل تعلم أن 90% من قراراتنا نتاج العقل الباطن؟\nالقصة المصغرة: كنت أجري أمس، وفجأة... وقعت!\nالإحصائية المدهشة: يهدر طعام يكفي لإطعام مليار شخص سنوياً\nالموقف الطريف: حاولت مرة أن أطهو بيضاً فاحترق المطبخ!\n\nالمحتوى (اللب):\nركز على نقطة رئيسية واحدة في كل فقرة\nاستخدم القصص لجعل المعلومة أكثر جاذبية\nقدم أمثلة وتشبيهات لدعم فكرتك الرئيسية\nمثال: بدلاً من وصف مكان ممل، احكِ قصة حدثت لك فيه\n\nالخاتمة (الختام المؤثر):\nأنواع الخواتم:\nالتلخيص: إذن، الفكرة الرئيسية هي...\nدعوة للتفاعل: ما رأيكم؟ اكتبوا في الدردشة\nالسؤال المفتوح: لو كانت لديكم فرصة لسؤال أحد المشاهير، فمن تختارون؟\nالتلميح للمستقبل: في الحلقة القادمة، سنكشف عن سر...",
                "content_en": "Introduction (The Hook):\nYou only have 10-15 seconds to grab the listener's attention\nTypes of effective hooks:\nShocking question: Did you know that 90% of our decisions are products of the subconscious mind?\nMini-story: I was running yesterday, and suddenly... I fell!\nAmazing statistic: Enough food is wasted annually to feed one billion people!\nAmusing situation: I once tried to cook eggs and the kitchen caught fire!\n\nContent (The Core):\nFocus on one main point in each paragraph\nUse stories to make information more attractive\nProvide examples and analogies to support your main idea\nExample: Instead of describing a boring place, tell a story that happened to you there\n\nConclusion (The Impactful Closing):\nTypes of conclusions:\nSummary: So, the main idea is...\nCall to interaction: What do you think? Write in the chat\nOpen question: If you had the chance to ask a celebrity, who would you choose?\nHinting at the future: In the next episode, we will reveal the secret of..."
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
    },
    4: {
        "title_ar": "اليوم الرابع: فقرات الألعاب التنشيطية - كسر الجليد وبناء المجتمعات",
        "title_en": "Day 4: Icebreaker Segments - Breaking Barriers and Building Communities",
        "materials": [
            {
                "type": "text",
                "title_ar": "فلسفة الألعاب التنشيطية",
                "title_en": "Philosophy of Icebreaker Games",
                "content_ar": "الفلسفة وراء الألعاب التنشيطية:\nالهدف ليس اللعبة نفسها، بل التفاعل الاجتماعي الذي تخلقه\nاللعبة مجرد وسيلة لجعل الجمهور يشعر بالراحة والمتعة\nمثال: لعبة 'ماذا ستفعل بمليون دولار' تفتح مجالاً للتعارف والإبداع\n\nأنماط الألعاب التنشيطية:\nألعاب التعارف: 'ما هي القوة الخارقة التي تريدها؟'\nألعاب الذكاء السريع: أسئلة معلومات عامة\nألعاب التخمين: تخمين الشخصية، الفيلم، كلمة السر\nألعاب الصور: وصف الصورة دون استخدام كلمات ممنوعة\n\nكيف تقدم لعبة؟ خطوات واضحة:\nالخطوة 1: اذكر اسم اللعبة بحماس\nالخطوة 2: اشرح القواعد ببساطة ووضوح\nالخطوة 3: نفذ اللعبة مع التحفيز والتعليق\nالخطوة 4: أنهِ بشكر المشاركين والانتقال السلس\n\nنصائح ذهبية للنجاح:\nالتحكيم بمرح وليس بقسوة\nإدارة الوقت والمحافظة على وتيرة البرنامج\nالحفاظ على طاقة عالية طوال الوقت",
                "content_en": "Philosophy behind Icebreaker Games:\nThe goal is not the game itself, but the social interaction it creates\nThe game is just a means to make the audience feel comfortable and enjoy\nExample: The game 'What would you do with a million dollars?' opens the door for acquaintance and creativity\n\nTypes of Icebreaker Games:\nAcquaintance games: 'What superpower would you want?'\nQuick intelligence games: General knowledge questions\nGuessing games: Guessing characters, movies, passwords\nPicture games: Describing pictures without using forbidden words\n\nHow to present a game? Clear steps:\nStep 1: State the game name enthusiastically\nStep 2: Explain the rules simply and clearly\nStep 3: Implement the game with motivation and commentary\nStep 4: End by thanking participants and smooth transition\n\nGolden tips for success:\nRefereeing with fun not harshness\nTime management and maintaining program pace\nMaintaining high energy throughout"
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
                "content_ar": "طاقة السرعة وإدارتها:\nهذه الفقرات تحتاج لطاقة عالية وتركيز حاد\nتنفس بعمق قبل البدء لشحن طاقتك\nحافظ على وتيرة سريعة ولكن مع وضوح في الكلام\n\nأنواع ألعاب السرعة:\nأسرع إجابة: يطرح السؤال وأول من يرفع يده يفوز\nتحدي الـ 10 ثوانٍ: الإجابة必须在10 ثوانٍ\nأغنية وكلمة: معرفة الأغنية أو كلمة مرتبطة بها\nأسئلة 'بنعم أو لا': أسئلة سريعة مباشرة\n\nفن التعليق على الإجابات:\nالإجابة الصحيحة: 'أحسنت!'، 'انطلقت كالصاروخ!'\nالإجابة الخاطئة: 'أوه، كادت!'، 'الفكرة قريبة!'\nنبرة التشويق: استخدم صوتاً مرتفعاً ومتحمساً للإجابات الصحيحة\n\nأدوات التشويق والإثارة:\nصوت المؤقت يزيد التوتر\nالمؤثرات الصوتية (جرس للفوز، صفارة للخطأ)\nالخلفية الموسيقية السريعة",
                "content_en": "Speed Energy and Its Management:\nThese segments require high energy and sharp focus\nBreathe deeply before starting to charge your energy\nMaintain a fast pace but with clarity in speech\n\nTypes of Speed Games:\nFastest answer: Question is asked and first to raise hand wins\n10-second challenge: Answer must be within 10 seconds\nSong and word: Identifying the song or related word\n'Yes or No' questions: Quick direct questions\n\nArt of Commenting on Answers:\nCorrect answer: 'Well done!', 'You took off like a rocket!'\nWrong answer: 'Oh, almost!', 'The idea is close!'\nSuspense tone: Use high and excited voice for correct answers\n\nTools for Suspense and Excitement:\nTimer sound increases tension\nSound effects (bell for win, whistle for wrong)\nFast background music"
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
                "content_ar": "محاربة الملل في تقديم المعلومات:\nاروي، لا تخبر: بدلاً من 'كان الطقس بارداً' قل 'كان الصقيع يتسلل عبر سترتي'\nاربط المعلومة بحياة المستمع: اجعل المعلومة شخصية ومؤثرة\nاستخدم التشبيهات: 'الإنترنت يشبه الطريق السريع للبيانات'\n\nتبسيط المعلومات المعقدة:\nالتشبيه: 'البلوك تشين يشبه دفتر حسابات موزع'\nالقصص: ابحث عن القصة الإنسانية خلف المعلومة\nالأمثلة العملية: شرح النظريات من خلال تطبيقاتها اليومية\n\nمصادر المعلومات ومصداقيتها:\nتحقق دائماً من مصدر المعلومة\nاستخدم مواقع موثوقة ومراجع علمية\nذكر مصدرك يزيد من مصداقيتك\n\nأنماط الفقرات الثقافية:\n'هل تعلم؟' قصيرة وسريعة\n'سؤال ثقافي' مع مشاركة الجمهور\n'حكاية من التاريخ' بسرد قصصي مشوق",
                "content_en": "Combating Boredom in Information Presentation:\nNarrate, don't tell: Instead of 'the weather was cold' say 'frost was creeping through my jacket'\nConnect information to listener's life: Make information personal and impactful\nUse analogies: 'The internet is like a highway for data'\n\nSimplifying Complex Information:\nAnalogy: 'Blockchain is like a distributed ledger'\nStories: Find the human story behind the information\nPractical examples: Explain theories through their daily applications\n\nInformation Sources and Credibility:\nAlways verify the source of information\nUse reliable websites and scientific references\nMentioning your source increases your credibility\n\nTypes of Cultural Segments:\n'Did you know?' short and fast\n'Cultural question' with audience participation\n'Tale from history' with exciting narrative"
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم السادس: الفقرات الثقافية",
            "title_en": "Day 6 Quiz: Cultural Segments",
            "questions": [
                {
                    "question_ar": "ما هو الفرق بين أروي وأخبر في تقديم المعلومات؟",
                    "question_en": "What is the difference between narrate and tell in information presentation?",
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
                "content_ar": "استراتيجيات جذب التفاعل:\nالأسئلة المفتوحة: 'ما هو أكثر لحظة أعجبتكم؟' بدلاً من 'هل أعجبكم البرنامج؟'\nاستطلاعات الرأي: استخدام أدوات التصويت في التطبيقات\nالطلب المباشر: 'شاركونا صور طعامكم!'، 'ما رأيكم في...؟'\n\nفن إدارة التعليقات المباشرة:\nالتعليق الإيجابي: اشكر ورد بالاسم ('شكراً لك يا أحمد')\nالتعليق السلبي: تعامل بذكاء:\nاعترف بالمشكلة\nأعد صياغة الملاحظة\nرد بطريقة مهذبة\nالتعليق المسيء: تجاهله أو أخرجه بهدوء\n\nأنماط الفقرات التفاعلية:\n'الرأي والرأي الآخر': مناقشة قضايا مختلفة الآراء\n'قصص من حياتكم': مشاركة قصص شخصية\n'استشارات الجمهور': طلب النصائح والأفكار",
                "content_en": "Strategies for Attracting Interaction:\nOpen questions: 'What moment did you like most?' instead of 'Did you like the program?'\nOpinion polls: Using voting tools in applications\nDirect request: 'Share photos of your food!', 'What do you think about...?'\n\nArt of Managing Live Comments:\nPositive comment: Thank and respond by name ('Thank you, Ahmed')\nNegative comment: Deal intelligently:\nAcknowledge the problem\nRephrase the observation\nRespond politely\nOffensive comment: Ignore it or remove it calmly\n\nTypes of Interactive Segments:\n'Opinion and Counter-opinion': Discussing issues with different opinions\n'Stories from your lives': Sharing personal stories\n'Audience consultations': Requesting advice and ideas"
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
                "content_ar": "حقيقة الارتجال:\nالارتجال الحقيقي هو تحضير مسبق للأدوات وليس للنص\nجهز 'طقم النجاة' قبل أن تحتاجه\n\nالمواقف الطارئة الشائعة:\nصمت مطبق: ضيف لا يتكلم أو عدم تفاعل\nمشاكل تقنية: انقطاع الإنترنت، صوت غير واضح\nتفاعل ضعيف: لا أحد يشارك\nتعليقات محرجة: أسئلة أو ملاحظات غير متوقعة\n\nأدوات الارتجال (طوق النجاة):\nالفكاهة: اضحك على الموقف ('يبدو أن الإنترنت قرر أخذ استراحة!')\nالاعتراف البسيط: 'أعتذر، ظهري انقطع للحظة!'\nالعودة لنقطة سابقة: 'هذا يذكرني بما كنا نتحدث عنه...'\nالجعبة السرية: 3 قصص شخصية + 5 أسئلة عامة",
                "content_en": "The Truth About Improvisation:\nReal improvisation is preparing tools in advance, not preparing text\nPrepare a 'survival kit' before you need it\n\nCommon Emergency Situations:\nTotal silence: Guest doesn't speak or no interaction\nTechnical problems: Internet disconnection, unclear sound\nWeak interaction: No one participates\nEmbarrassing comments: Unexpected questions or observations\n\nImprovisation Tools (Lifebuoy):\nHumor: Laugh at the situation ('It seems the internet decided to take a break!')\nSimple admission: 'I apologize, my connection was cut for a moment!'\nReturn to a previous point: 'This reminds me of what we were talking about...'\nSecret stash: 3 personal stories + 5 general questions"
            }
        ],
        "quiz": {
            "title_ar": "اختبار اليوم الثامن: الارتجال",
            "title_en": "Day 8 Quiz: Improvisation",
            "questions": [
                {
                    "question_ar": "ما هي 'الجعبة السرية' في الارتجال؟",
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
                "content_ar": "التحضير قبل البرنامج:\nالبحث عن الضيف: اقرأ عنه، شاهد مقابلات سابقة\nتحديد الهدف: ما الرسالة الرئيسية من المقابلة؟\nإعداد النقاط الرئيسية: 5-7 نقاط وليس نصاً كاملاً\nالاتصال بالضيف: تعريفه بنمط البرنامج والنقاط الرئيسية\n\nفن صياغة الأسئلة:\nالأسئلة المفتوحة: 'كيف كانت رحلتك؟'، 'ما الذي دفعك لهذا القرار؟'\nأسئلة المشاعر: 'كيف شعرت في تلك اللحظة؟'\nالأسئلة المتتابعة: ابنِ على إجابات الضيف\n\nدورك كقائد أوركسترا:\nلا تكن النجم: سلط الضوء على الضيف لا على نفسك\nالاستماع ثم الكلام: الاستماع الجيد يولد أسئلة أفضل\nإدارة الوقت: أنهِ الحوار بلباقة عندما يحين الموعد",
                "content_en": "Preparation Before the Program:\nResearch the guest: Read about them, watch previous interviews\nDefine the goal: What is the main message from the interview?\nPrepare main points: 5-7 points not a full text\nContact the guest: Introduce them to the program style and main points\n\nArt of Formulating Questions:\nOpen questions: 'How was your journey?', 'What drove you to this decision?'\nEmotion questions: 'How did you feel at that moment?'\nFollow-up questions: Build on the guest's answers\n\nYour Role as Orchestra Conductor:\nDon't be the star: Spotlight the guest not yourself\nListen then speak: Good listening generates better questions\nTime management: End the dialogue politely when time comes"
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
                "content_ar": "هندسة البرنامج:\nالفكرة: ماذا تقدم؟ (ترفيه، تعليم، إلهام)\nالجمهور: لمن تقدمه؟ (شباب، عائلات، متخصصون)\nالهدف: لماذا تقدمه؟ (تسلية، معرفة، مجتمع)\n\nالروتين التحضيري:\nالبحث وجمع المعلومات\nكتابة النقاط الرئيسية\nالتحضير للفقرات\nالاختبار التقني\nالإعلان المسبق\n\nالسكريبت المرن:\nليس نصاً تقرأه، بل خارطة طريق\nمثال:\n0:00-0:02: مقدمة + خطاف\n0:02-0:05: ترحيب + تفاعل\n0:05-0:15: لعبة رئيسية\n0:15-0:25: مقابلة ضيف\n0:25-0:29: تفاعل جمهور\n0:29-0:30: خاتمة\n\nصناعة الهوية:\nاسم البرنامج وشعاره\nالموسيقى المميزة\nطريقة الترحيب الخاصة",
                "content_en": "Program Engineering:\nIdea: What do you offer? (Entertainment, education, inspiration)\nAudience: Who do you offer it to? (Youth, families, specialists)\nGoal: Why do you offer it? (Entertainment, knowledge, community)\n\nPreparation Routine:\nResearch and information gathering\nWriting main points\nPreparing segments\nTechnical testing\nPrior announcement\n\nFlexible Script:\nNot a text you read, but a roadmap\nExample:\n0:00-0:02: Introduction + hook\n0:02-0:05: Welcome + interaction\n0:05-0:15: Main game\n0:15-0:25: Guest interview\n0:25-0:29: Audience interaction\n0:29-0:30: Conclusion\n\nIdentity Creation:\nProgram name and logo\nDistinctive music\nSpecial welcome method"
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
                "content_ar": "الموسيقى والمؤثرات الصوتية:\nالملح وليس الطبق الرئيسي: الإفراط يفسد التجربة\nالمقدمة والخاتمة: موسيقى مميزة وقصيرة\nالانتقالات: موسيقى خفيفة بين الفقرات\n\nاختيار الموسيقى المناسبة:\nالبرامج المرحة: موسيقى سريعة وإيقاعية\nالبرامج الجادة: موسيقى هادئة أو بدون موسيقى\nالمصادر: استخدم موسيقى خالية من الحقوق\n\nمعالجة الصوت الأساسية:\nإزالة الضوضاء: تزيل همسة الميكروفون\nمعادلة الصوت: تحسين الوضوح\nالضغط: توحيد مستوى الصوت",
                "content_en": "Music and Sound Effects:\nThe salt not the main dish: Excess spoils the experience\nIntroduction and conclusion: Distinctive and short music\nTransitions: Light music between segments\n\nChoosing Suitable Music:\nFun programs: Fast and rhythmic music\nSerious programs: Calm music or no music\nSources: Use royalty-free music\n\nBasic Audio Processing:\nNoise removal: Removes microphone hiss\nEqualization: Improves clarity\nCompression: Unifies sound level"
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
                "content_ar": "الستوري تيلينغ (فن سرد القصة):\nالهيكل الذهبي:\nالبداية: الشخصية في سياقها العادي\nالحدث المحفز: شيء يغير كل شيء\nالرحلة والصراع: التحديات\nالذروة: لحظة الحسم\nالنهاية: التغيير والدرس\n\nالدعابة الذكية:\nاضحك على نفسك لا على الآخرين\nالمفارقة: 'هدفي كان رياضياً محترفاً ولكن الأريكة كانت أقوى!'\nالمراقبة: التعليق على مواقف الحياة اليومية\n\nالتوقيت الكوميدي:\nالوقفة قبل النكتة: تزيد التشويق\nالوقفة بعد النكتة: تعطي وقتاً للضحك\nالإيقاع: التناوب بين السرعة والبطء",
                "content_en": "Storytelling (The Art of Narrative):\nThe Golden Structure:\nBeginning: Character in their normal context\nTriggering event: Something changes everything\nJourney and conflict: Challenges\nClimax: Moment of decision\nEnd: Change and lesson\n\nIntelligent Humor:\nLaugh at yourself not at others\nIrony: 'My goal was to be a professional athlete but the couch was stronger!'\nObservation: Commenting on daily life situations\n\nComedic Timing:\nPause before the joke: Increases suspense\nPause after the joke: Gives time to laugh\nRhythm: Alternating between speed and slowness"
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
                "content_ar": "أنماط الشخصيات في الجمهور:\nالمتفاعل: يعلق ويسأل باستمرار\nالمشجع: حاضر دائماً ونادر التفاعل\nالناقد: يرى الأخطاء فقط\nالخجول: يستمع فقط\n\nبناء المجتمع:\nالتكرار: المواظبة على الموعد تخلق عادة\nالتفاعل الشخصي: مناداتهم بالأسماء\nتلبية الرغبات: تخصيص فقرات بناء على طلباتهم\n\nجمع التغذية الراجعة:\nالاستبيانات السريعة\nالأسئلة المباشرة\nمراقبة نوعية التفاعل",
                "content_en": "Personality Types in the Audience:\nInteractive: Comments and asks constantly\nSupporter: Always present but rarely interacts\nCritic: Only sees mistakes\nShy: Only listens\n\nBuilding Community:\nRepetition: Consistency with timing creates habit\nPersonal interaction: Calling them by names\nFulfilling desires: Customizing segments based on their requests\n\nCollecting Feedback:\nQuick surveys\nDirect questions\nMonitoring interaction quality"
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
                "content_ar": "فنون الربط:\nاللفظي: 'والحديث عن السفر يحضرني لعبة عن دول العالم'\nالصوتي: استخدام موسيقى انتقالية\nالمنطقي: 'بعد كل هذا المرح، حان وقت الاستراحة بمعلومة مدهشة'\n\nالتمارين العملية الفردية:\nالتدريب النهائي الكبير (70 دقيقة): تسجيل حلقة برنامج كاملة 15-20 دقيقة\n\nالأنشطة الجماعية:\nالبث المباشر الوهمي (90 دقيقة): محاكاة بث حي بفريق كامل\n\nالمهمة اليومية: سجل الحلقة كاملة وقيم أداءك",
                "content_en": "Linking Arts:\nVerbal: 'And talking about travel brings me to a game about world countries'\nAudio: Using transition music\nLogical: 'After all this fun, it's time for a break with an amazing fact'\n\nIndividual Practical Exercises:\nFinal Comprehensive Training (70 minutes): Recording a full program episode 15-20 minutes\n\nGroup Activities:\nSimulated Live Broadcast (90 minutes): Simulating a live broadcast with a full team\n\nDaily Task: Record the full episode and evaluate your performance"
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
                "content_ar": "التقييم الذاتي الموضوعي:\nاستمع كجمهور: هل أنت مستمتع؟\nاستمع كخبير: حلل الوضوح، الطلاقة، التنظيم\n\nخطة التطوير المستمر:\nمواكبة الترندات\nالتعلم المستمر\nطلب التغذية الراجعة\n\nالاستدامة:\nضع حدوداً للراحة\nتذكر 'لماذا' بدأت\nاحتفل بالإنجازات\n\nالتمارين العملية الفردية:\nتمرين التقييم الذاتي (30 دقيقة): تقييم تسجيل الحلقة الكاملة\nتمرين التخطيط الاستراتيجي (30 دقيقة): خطة 90 يوم القادمة\n\nالأنشطة الجماعية:\nحلقة التغذية الراجعة (60 دقيقة): تقديم ملاحظات بناءة\nاحتفال التخرج (45 دقيقة): مشاركة الخطط المستقبلية\n\nالمهمة اليومية: اكتب رسالة لنفسك في الماضي",
                "content_en": "Objective Self-Evaluation:\nListen as an audience: Are you enjoying?\nListen as an expert: Analyze clarity, fluency, organization\n\nContinuous Development Plan:\nKeeping up with trends\nContinuous learning\nRequesting feedback\n\nSustainability:\nSet boundaries for rest\nRemember 'why' you started\nCelebrate achievements\n\nIndividual Practical Exercises:\nSelf-Evaluation Exercise (30 minutes): Evaluating the full episode recording\nStrategic Planning Exercise (30 minutes): Plan for the next 90 days\n\nGroup Activities:\nFeedback Circle (60 minutes): Providing constructive feedback\nGraduation Celebration (45 minutes): Sharing future plans\n\nDaily Task: Write a letter to your past self"
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
user_language = {}

# =============================================================================
# TELEGRAM BOT CLASS
# =============================================================================

class TrainingBot:
    def __init__(self, token):
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
            f"🎓 **مرحباً بك في البرنامج التدريبي الشامل، {user.first_name}!**\n\nهذا البرنامج المكثف لمدة 15 يوماً سيرشدك نحو الاحتراف في عالم البث الصوتي.\n\nاستخدم /menu للوصول إلى القائمة الرئيسية.",
            f"🎓 **Welcome to Comprehensive Training Program, {user.first_name}!**\n\nThis intensive 15-day program will guide you toward professionalism in audio broadcasting.\n\nUse /menu to access the main menu."
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
        menu_text = self.get_text(user_id, "🏫 **القائمة الرئيسية**", "🏫 **Main Menu**")
        await update.message.reply_text(menu_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_progress(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        progress = user_progress.get(user_id, {})
        current_day = progress.get("current_day", 1)
        completed_days = len(progress.get("completed_days", set()))
        
        progress_text = self.get_text(user_id,
            f"📊 **تقدمك في التعلم**\n\n**اليوم الحالي:** {current_day}/15\n**الأيام المكتملة:** {completed_days}/15\n**نسبة الإنجاز:** {round((completed_days/15)*100)}%",
            f"📊 **Your Learning Progress**\n\n**Current Day:** {current_day}/15\n**Completed Days:** {completed_days}/15\n**Completion Rate:** {round((completed_days/15)*100)}%"
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
            await query.edit_message_text("✅ تم تغيير اللغة / Language changed")
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
        menu_text = self.get_text(user_id, "🏫 **القائمة الرئيسية**", "🏫 **Main Menu**")
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
        keyboard.append([InlineKeyboardButton("🏠 رئيسية", callback_data="main_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = self.get_text(user_id, "📚 **جميع أيام التدريب**", "📚 **All Training Days**")
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
        keyboard.append([InlineKeyboardButton("🏠 رئيسية", callback_data="main_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = self.get_text(user_id, "❓ **الاختبارات المتاحة**", "❓ **Available Quizzes**")
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def show_day_overview(self, update, day_num):
        user_id = update.effective_user.id if hasattr(update, 'effective_user') else update.from_user.id
        day_data = TRAINING_DATA.get(day_num, {})
        day_title = self.get_text(user_id, day_data.get("title_ar", f"اليوم {day_num}"), day_data.get("title_en", f"Day {day_num}"))
        
        overview_text = f"{day_title}\n\n{self.get_text(user_id, 'المواد المتاحة:', 'Available materials:')}\n"
        
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
    
    async def show_next_material(self, query, day_num, material_index):
        await self.show_material(query, day_num, material_index)
    
    async def start_quiz(self, query, day_num):
        user_id = query.from_user.id
        day_data = TRAINING_DATA.get(day_num, {})
        quiz_data = day_data.get("quiz")
        
        if not quiz_data:
            await query.answer("لا يوجد اختبار")
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
        question_text = self.get_text(user_id, question_data['question_ar'], question_data['question_en'])
        options = question_data['options_ar'] if self.get_user_language(user_id) == 'ar' else question_data['options_en']
        
        full_text = f"❓ **{question_index + 1}/{len(questions)}**\n\n{question_text}"
        
        keyboard = []
        for i, option in enumerate(options):
            keyboard.append([InlineKeyboardButton(option, callback_data=f"answer_{day_num}_{question_index}_{i}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(full_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def handle_quiz_answer(self, query, day_num, question_index, answer_index):
        user_id = query.from_user.id
        day_data = TRAINING_DATA.get(day_num, {})
        questions = day_data.get("quiz", {}).get("questions", [])
        
        if user_id not in user_quiz_responses:
            await query.answer("جلسة منتهية")
            return
        
        question_data = questions[question_index]
        is_correct = (answer_index == question_data['correct'])
        
        user_quiz_responses[user_id]["answers"].append({
            "question_index": question_index,
            "answer_index": answer_index,
            "is_correct": is_correct
        })
        
        if is_correct:
            user_quiz_responses[user_id]["score"] += 1
        
        explanation = self.get_text(user_id, question_data['explanation_ar'], question_data['explanation_en'])
        result_text = f"{'✅ صح!' if is_correct else '❌ خطأ'}\n\n{explanation}"
        
        keyboard = [[InlineKeyboardButton("التالي ➡️", callback_data=f"next_question_{day_num}_{question_index+1}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(result_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def finish_quiz(self, query, day_num):
        user_id = query.from_user.id
        quiz_responses = user_quiz_responses.get(user_id, {})
        total_questions = len(TRAINING_DATA[day_num]["quiz"]["questions"])
        score = quiz_responses.get("score", 0)
        percentage = round((score / total_questions) * 100)
        
        if user_id not in user_progress:
            user_progress[user_id] = {"quiz_scores": {}, "completed_days": set()}
        
        user_progress[user_id]["quiz_scores"][day_num] = percentage
        user_progress[user_id]["completed_days"].add(day_num)
        user_progress[user_id]["current_day"] = min(day_num + 1, 15)
        
        result_text = self.get_text(user_id,
            f"📊 **اكتمل الاختبار!**\n\n**النتيجة:** {score}/{total_questions}\n**النسبة:** {percentage}%",
            f"📊 **Quiz Complete!**\n\n**Score:** {score}/{total_questions}\n**Percentage:** {percentage}%"
        )
        
        keyboard = [
            [InlineKeyboardButton("📖 مراجعة", callback_data=f"day_{day_num}")],
            [InlineKeyboardButton("❓ إعادة", callback_data=f"quiz_{day_num}")],
            [InlineKeyboardButton("📅 التالي", callback_data=f"day_{day_num+1}" if day_num < 15 else "main_menu")],
            [InlineKeyboardButton("🏠 رئيسية", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(result_text, reply_markup=reply_markup, parse_mode='Markdown')
        
        if user_id in user_quiz_responses:
            del user_quiz_responses[user_id]
    
    async def change_language_callback(self, query):
        keyboard = [
            [InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar")],
            [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("اختر اللغة / Choose language:", reply_markup=reply_markup)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        text = update.message.text
        
        if any(greeting in text.lower() for greeting in ['hello', 'hi', 'hey', 'مرحبا', 'السلام']):
            await update.message.reply_text("👋 مرحباً! استخدم /menu للقائمة الرئيسية")
        else:
            await update.message.reply_text("استخدم /menu للوصول إلى القائمة الرئيسية")

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
    
    import threading
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    app.run(host='0.0.0.0', port=port)
