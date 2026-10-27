# Generator for js/learning_outcomes_data.js
import json, re

# Read parsed sample records from scratch/parsed_sample.json
with open('scratch/parsed_sample.json', 'r', encoding='utf-8') as f:
    records = json.load(f)

with open('skill_areas_data.json', 'r', encoding='utf-8') as f:
    sk_data = json.load(f)

skill_areas = sorted(list(set(item['skillArea'].strip() for item in sk_data if 'skillArea' in item)), key=len, reverse=True)
skill_areas.extend([
    'Measurement (Length, Weight, Capacity, Time, Money)',
    'Measurement, Recording & Representation'
])
skill_areas = sorted(skill_areas, key=len, reverse=True)

sub_skills = sorted(list(set(item['activity'].strip() for item in sk_data if 'activity' in item)), key=len, reverse=True)
sub_skills.extend([
    'Vocabulary',
    'Vocbulary',
    'Labelled Diagrams & Flow Charts',
    'Microscopy & Slide Preparation',
    'Chemical Word Equations',
    'Graphs',
    'Linear Equations',
    'Algebraic Identities'
])
sub_skills = sorted(sub_skills, key=len, reverse=True)

def clean_str(s):
    if not s:
        return ""
    return (s.replace('‘', "'")
             .replace('’', "'")
             .replace('“', '"')
             .replace('”', '"')
             .replace('–', '-')
             .replace('—', '-')
             .replace('\uFFFD', "'")
             .strip())

final_outcomes = []
for r in records:
    text = r['raw_rest']
    matched_sa = None
    for sa in skill_areas:
        if text.startswith(sa):
            matched_sa = sa
            break
    after_sa = text[len(matched_sa):].strip() if matched_sa else text
    matched_sub = None
    for sub in sub_skills:
        if after_sa.startswith(sub):
            matched_sub = sub
            break
    outcome = clean_str(after_sa[len(matched_sub):].strip() if matched_sub else after_sa)
    normalized_sub = 'Vocabulary' if matched_sub == 'Vocbulary' else (matched_sub or 'General')
    final_outcomes.append({
        'id': r['id'],
        'class': r['class'],
        'masterclassId': r['masterclassId'],
        'subject': r['subject'],
        'skillArea': clean_str(matched_sa or 'General'),
        'subSkillArea': clean_str(normalized_sub),
        'learningOutcome': outcome
    })

# Define the Quizzes strictly grounded in the file
quizzes = [
    {
        "id": "quiz-eng-comm",
        "title": "Everyday English & Communication Quiz",
        "subject": "English",
        "class": "Class I - Class VIII",
        "skillArea": "Listening, Speaking & Vocabulary",
        "description": "Test understanding of classroom instructions, phonetic blends, opposite words, and polite expressions directly from the learning outcomes.",
        "questions": [
            {
                "id": "q1",
                "prompt": "According to the learning outcomes, which of the following is a simple instruction a student carries out?",
                "options": [
                    "Shut the door",
                    "Climb the skyscraper",
                    "Build an electric motor",
                    "Write an encyclopedia"
                ],
                "answer": 0,
                "explanation": "Learning Outcome #1 lists carrying out simple instructions such as ‘Shut the door’, ‘Bring me the book’, and such others."
            },
            {
                "id": "q2",
                "prompt": "Which words are given in the outcomes as examples of common blends with 'br' and 'fr'?",
                "options": [
                    "brother and frog",
                    "boy and sun",
                    "fan and rat",
                    "day and night"
                ],
                "answer": 0,
                "explanation": "Learning Outcome #5 specifies producing words with common blends like ‘br’, ‘fr’ like ‘brother’, ‘frog’ etc."
            },
            {
                "id": "q3",
                "prompt": "Which of these is explicitly identified as an example pair of opposites in the curriculum?",
                "options": [
                    "day / night",
                    "boy / sun",
                    "big / pink",
                    "fan / hen"
                ],
                "answer": 0,
                "explanation": "Learning Outcome #57 identifies opposites like ‘day/night’, ‘close/open’, and such others."
            },
            {
                "id": "q4",
                "prompt": "Which polite / formulaic expression is given in the outcomes for communicating politely?",
                "options": [
                    "May I borrow your book?",
                    "Give me that immediately!",
                    "You must finish now!",
                    "Silence in the hall!"
                ],
                "answer": 0,
                "explanation": "Learning Outcome #359 includes formulaic/polite expressions such as ‘May I borrow your book?’ and ‘I would like to differ’."
            },
            {
                "id": "q5",
                "prompt": "Which reference books are specifically mentioned in the outcomes to find meanings and spelling of unfamiliar words?",
                "options": [
                    "Dictionary, thesaurus and encyclopedia",
                    "Posters and television subtitles only",
                    "Railway timetables only",
                    "Comic books and fiction only"
                ],
                "answer": 0,
                "explanation": "Learning Outcomes #279 and #369 state that students refer to dictionary, thesaurus and encyclopedia as reference books for meaning and spelling."
            }
        ]
    },
    {
        "id": "quiz-math-concepts",
        "title": "Mathematics & Spatial Thinking Quiz",
        "subject": "Mathematics",
        "class": "Class I - Class VIII",
        "skillArea": "Numbers, Measurement & Geometry",
        "description": "Assess knowledge of physical features of shapes, non-uniform units of length, division facts, and variables from the file.",
        "questions": [
            {
                "id": "q1",
                "prompt": "How does the curriculum describe the physical features of a ball and a box?",
                "options": [
                    "A ball rolls, a box slides",
                    "A ball slides, a box rolls",
                    "Both a ball and a box only roll",
                    "Both a ball and a box only slide"
                ],
                "answer": 0,
                "explanation": "Learning Outcome #24 describes the physical features of various solids/shapes (e.g., a ball rolls, a box slides)."
            },
            {
                "id": "q2",
                "prompt": "Which non-uniform units are listed for estimating and measuring short lengths?",
                "options": [
                    "Finger, hand span, forearm length, footsteps",
                    "Centimetres, metres, and kilometres",
                    "Grams and kilograms using balances",
                    "Litres and millilitres in containers"
                ],
                "answer": 0,
                "explanation": "Learning Outcome #17 specifies non-uniform units like a finger, hand span, length of a forearm, footsteps, etc."
            },
            {
                "id": "q3",
                "prompt": "How is the meaning of division facts explained in the learning outcomes?",
                "options": [
                    "By equal grouping/sharing and repeated subtraction",
                    "By multiplying numbers and adding remainders",
                    "By drawing pie charts and pictographs",
                    "By measuring lengths using a ruler"
                ],
                "answer": 0,
                "explanation": "Learning Outcome #90 explains the meaning of division facts by equal grouping/sharing and finds it by repeated subtraction (e.g., 12 ÷ 3)."
            },
            {
                "id": "q4",
                "prompt": "What algebraic expression is given in the outcomes to generalise the perimeter of a rectangle with sides x units and 3 units?",
                "options": [
                    "2(x + 3) units",
                    "x + 3 units",
                    "3x units",
                    "2x + 3 units"
                ],
                "answer": 0,
                "explanation": "Learning Outcome #210 provides the exact example: perimeter of a rectangle with sides x units and 3 units is 2(x+3) units."
            },
            {
                "id": "q5",
                "prompt": "What estimate is given in the curriculum for the volume of a bucket compared to a mug?",
                "options": [
                    "Volume of a bucket is about 20 times that of a mug",
                    "Volume of a bucket is about 2 times that of a mug",
                    "A bucket and a mug have identical volume",
                    "Volume of a mug is 20 times that of a bucket"
                ],
                "answer": 0,
                "explanation": "Learning Outcome #181 states: estimates the volume of a solid body in known units (e.g., volume of a bucket is about 20 times that of a mug)."
            }
        ]
    },
    {
        "id": "quiz-sci-evs",
        "title": "Science & Environmental Studies Quiz",
        "subject": "Science & EVS",
        "class": "Class III - Class VIII",
        "skillArea": "Scientific Inquiry, Processes & Classification",
        "description": "Test understanding of reversible changes, scientific models, chemical word equations, and cause-effect relationships from the provided file.",
        "questions": [
            {
                "id": "q1",
                "prompt": "According to the classification outcomes, processes and changes can be classified as:",
                "options": [
                    "Reversible and irreversible changes",
                    "Loud and quiet changes",
                    "Heavy and light changes",
                    "Expensive and inexpensive changes"
                ],
                "answer": 0,
                "explanation": "Learning Outcome #227 classifies processes into reversible and irreversible changes."
            },
            {
                "id": "q2",
                "prompt": "Which working models are students guided to construct using materials from their surroundings in Class VI?",
                "options": [
                    "Pinhole camera, periscope, electric torch",
                    "Steam engine and airplane",
                    "Motorcycle and submarine",
                    "Digital smartphone and computer"
                ],
                "answer": 0,
                "explanation": "Learning Outcome #238 states: constructs models using materials from surroundings and explains their working (pinhole camera, periscope, electric torch)."
            },
            {
                "id": "q3",
                "prompt": "Which cause-and-effect relationship is explicitly stated in the curriculum?",
                "options": [
                    "Relates deficiency diseases with diet",
                    "Relates deficiency diseases with loud noise",
                    "Relates air quality with rock types",
                    "Relates wind speed with soil colour"
                ],
                "answer": 0,
                "explanation": "Learning Outcome #231 relates processes and phenomena with causes (deficiency diseases with diet; adaptations with habitats; air quality with pollutants)."
            },
            {
                "id": "q4",
                "prompt": "For which of the following chemical reactions do students write word equations in Science?",
                "options": [
                    "Acid-base reactions, corrosion, photosynthesis, respiration",
                    "Boiling water and freezing ice only",
                    "Slicing vegetables and peeling fruit",
                    "Folding paper and drawing diagrams"
                ],
                "answer": 0,
                "explanation": "Learning Outcome #311 lists writing word equations for: acid-base reactions, corrosion, photosynthesis, respiration."
            },
            {
                "id": "q5",
                "prompt": "Which specimens are specifically listed for microscopic slide preparation to describe microscopic features?",
                "options": [
                    "Microorganisms, onion peel, human cheek cells",
                    "Metal wire, plastic beads, rubber bands",
                    "Sand grains, coins, cotton thread",
                    "Paper strips, wood splinters, stones"
                ],
                "answer": 0,
                "explanation": "Learning Outcome #407 lists preparing slides of microorganisms, onion peel, human cheek cells, etc."
            }
        ]
    },
    {
        "id": "quiz-soc-gov",
        "title": "Social Science, History & Civics Quiz",
        "subject": "Social Science",
        "class": "Class VI - Class VIII",
        "skillArea": "History, Geography & Governance",
        "description": "Assess learning of ancient Indian contributions, celestial bodies, levels of government, and constitutional provisions.",
        "questions": [
            {
                "id": "q1",
                "prompt": "How does the geography curriculum distinguish Sun, Earth, and Moon in the solar system?",
                "options": [
                    "Sun as star, Earth as planet, Moon as satellite",
                    "Sun as planet, Earth as star, Moon as asteroid",
                    "Sun, Earth and Moon are all stars",
                    "Sun, Earth and Moon are all planets"
                ],
                "answer": 0,
                "explanation": "Learning Outcome #241 distinguishes between stars, planets and satellites (Sun, Earth and Moon)."
            },
            {
                "id": "q2",
                "prompt": "Which significant contributions are listed for ancient Indian kingdoms and dynasties in the outcomes?",
                "options": [
                    "Ashokan inscriptions, Gupta coins, Ratha temples by Pallavas",
                    "Modern paper currency and steam engines",
                    "Telegraph networks and skyscrapers",
                    "Automobile highways and digital computers"
                ],
                "answer": 0,
                "explanation": "Learning Outcome #249 lists significant contributions: Ashokan inscriptions, Gupta coins, Ratha temples by Pallavas."
            },
            {
                "id": "q3",
                "prompt": "What are the three levels of government identified in the social science curriculum?",
                "options": [
                    "Local, state and union",
                    "Primary, middle and senior",
                    "Rural, forest and coastal",
                    "Domestic, regional and international"
                ],
                "answer": 0,
                "explanation": "Learning Outcome #262 identifies levels of government – local, state and union."
            },
            {
                "id": "q4",
                "prompt": "Which public facilities are identified as being provided by the Government?",
                "options": [
                    "Water, sanitation, road, electricity",
                    "Private luxury cars and mansions",
                    "Amusement parks and cinemas only",
                    "Commercial airlines and resorts only"
                ],
                "answer": 0,
                "explanation": "Learning Outcome #440 identifies the role of Government in providing public facilities (water, sanitation, road, electricity)."
            },
            {
                "id": "q5",
                "prompt": "Which specific laws are described as examples of the law-making process in the curriculum?",
                "options": [
                    "Domestic Violence Act, RTI Act, RTE Act",
                    "Sports rulebook and library regulation",
                    "Highway toll rules and speed limits",
                    "Classroom seating guidelines"
                ],
                "answer": 0,
                "explanation": "Learning Outcome #435 describes the process of making a law (e.g., Domestic Violence Act, RTI Act, RTE Act)."
            }
        ]
    }
]

# Define the Mini-Games strictly grounded in the file
# CRITICAL: Every game card and screen must display "MINI GAME"
mini_games = [
    {
        "id": "mg-match-pairs",
        "title": "Curriculum Concept Match",
        "format": "Match the Pairs",
        "subject": "Integrated Curriculum",
        "time": "2 min",
        "instructions": "Tap a card on the left column, then tap its matching concept on the right based on facts from the curriculum outcomes.",
        "pairs": [
            ["Ball", "Rolls"],
            ["Box", "Slides"],
            ["Sun", "Star"],
            ["Earth", "Planet"],
            ["Moon", "Satellite"],
            ["Ashokan", "Inscriptions"],
            ["Gupta", "Coins"],
            ["Pallavas", "Ratha temples"]
        ]
    },
    {
        "id": "mg-fill-blank",
        "title": "Curriculum Word Fill",
        "format": "Fill in the Blank",
        "subject": "English & Science",
        "time": "2 min",
        "instructions": "Complete each statement with the exact term established in the learning outcomes.",
        "items": [
            {
                "sentence": "In shapes understanding, a ball rolls while a box ______.",
                "options": ["slides", "flies", "melts", "floats"],
                "answer": "slides",
                "explain": "Learning Outcome #24 describes that a ball rolls and a box slides."
            },
            {
                "sentence": "In Class III vocabulary, an identified pair of opposites is day and ______.",
                "options": ["night", "sun", "noon", "light"],
                "answer": "night",
                "explain": "Learning Outcome #57 identifies opposites like ‘day/night’, ‘close/open’."
            },
            {
                "sentence": "Common phonetic blends in Class I include 'br' in brother and 'fr' in ______.",
                "options": ["frog", "fan", "hen", "rat"],
                "answer": "frog",
                "explain": "Learning Outcome #5 gives ‘brother’ and ‘frog’ as examples of ‘br’ and ‘fr’ blends."
            },
            {
                "sentence": "The three levels of government are local, state and ______.",
                "options": ["union", "global", "school", "city"],
                "answer": "union",
                "explain": "Learning Outcome #262 lists levels of government as local, state and union."
            },
            {
                "sentence": "The volume of a bucket is estimated to be about 20 times that of a ______.",
                "options": ["mug", "barrel", "tanker", "swimming pool"],
                "answer": "mug",
                "explain": "Learning Outcome #181 notes that the volume of a bucket is about 20 times that of a mug."
            },
            {
                "sentence": "For conservation and hygiene, students suggest ways to reduce, reuse and ______.",
                "options": ["recycle", "discard", "burn", "spill"],
                "answer": "recycle",
                "explain": "Learning Outcome #129 suggests ways for hygiene, reduce, reuse, recycle."
            }
        ]
    },
    {
        "id": "mg-true-false",
        "title": "Learning Outcomes Fact Check",
        "format": "True or False",
        "subject": "Integrated Curriculum",
        "time": "1 min",
        "instructions": "Decide whether each statement accurately reflects the facts and principles stated in the provided file.",
        "items": [
            {
                "statement": "In the learning outcomes, a ball is described as rolling and a box as sliding.",
                "answer": True,
                "explain": "True. Outcome #24 explicitly describes: 'a ball rolls, a box slides'."
            },
            {
                "statement": "The learning outcomes identify the Sun as a planet and the Earth as a star.",
                "answer": False,
                "explain": "False. Outcome #241 distinguishes Sun as star, Earth as planet, and Moon as satellite."
            },
            {
                "statement": "The Domestic Violence Act, RTI Act, and RTE Act are cited as examples of the law-making process.",
                "answer": True,
                "explain": "True. Outcome #435 explicitly lists these three Acts as examples of law-making."
            },
            {
                "statement": "Division facts are explained by equal grouping/sharing and repeated subtraction (such as 12 ÷ 3).",
                "answer": True,
                "explain": "True. Outcome #90 states that division is explained by equal grouping/sharing and repeated subtraction."
            },
            {
                "statement": "A finger, hand span, and footsteps are examples of uniform standard units of measurement like centimetres.",
                "answer": False,
                "explain": "False. Outcome #17 establishes that a finger, hand span, forearm length, and footsteps are non-uniform units."
            },
            {
                "statement": "Deficiency diseases are related to diet as a cause-and-effect relationship in Science.",
                "answer": True,
                "explain": "True. Outcome #231 states: relates processes and phenomena with causes (deficiency diseases with diet)."
            }
        ]
    },
    {
        "id": "mg-arrange-order",
        "title": "Curriculum Sequence Challenge",
        "format": "Arrange in Order",
        "subject": "EVS, Math & English",
        "time": "2 min",
        "instructions": "Put the steps, concepts, or events into the exact order established in the learning outcomes.",
        "rounds": [
            {
                "prompt": "Arrange the food supply journey from source to home (Outcome #120):",
                "steps": [
                    "Field (crops grown)",
                    "Mandi (market hub)",
                    "Home (kitchen & table)"
                ]
            },
            {
                "prompt": "Arrange the odd number pattern sequence in ascending order (Outcome #23):",
                "steps": [
                    "1",
                    "3",
                    "5",
                    "7"
                ]
            },
            {
                "prompt": "Arrange the levels of government starting from the grassroots (Outcome #262):",
                "steps": [
                    "Local Government",
                    "State Government",
                    "Union Government"
                ]
            },
            {
                "prompt": "Arrange the sentence transition linkers in order (Outcome #109):",
                "steps": [
                    "First",
                    "Next",
                    "Finally"
                ]
            }
        ]
    },
    {
        "id": "mg-quick-challenge",
        "title": "60-Second Knowledge Sprint",
        "format": "Quick Quiz Challenge",
        "subject": "Rapid Recall",
        "time": "1 min",
        "instructions": "Answer as many quick questions as you can before the 60-second countdown expires!",
        "seconds": 60,
        "questions": [
            {
                "q": "What physical movement is described for a ball in Outcome #24?",
                "options": ["Rolls", "Slides", "Flies", "Stretches"],
                "answer": 0,
                "explain": "Outcome #24 states: a ball rolls, a box slides."
            },
            {
                "q": "What physical movement is described for a box in Outcome #24?",
                "options": ["Slides", "Rolls", "Bounces", "Melts"],
                "answer": 0,
                "explain": "Outcome #24 states: a ball rolls, a box slides."
            },
            {
                "q": "Which blend is found in 'brother' according to Outcome #5?",
                "options": ["br", "fr", "pl", "st"],
                "answer": 0,
                "explain": "Outcome #5 lists blends like 'br' in brother."
            },
            {
                "q": "Which blend is found in 'frog' according to Outcome #5?",
                "options": ["fr", "br", "cl", "dr"],
                "answer": 0,
                "explain": "Outcome #5 lists blends like 'fr' in frog."
            },
            {
                "q": "The Sun is classified in the curriculum as a:",
                "options": ["Star", "Planet", "Satellite", "Comet"],
                "answer": 0,
                "explain": "Outcome #241 classifies the Sun as a star."
            },
            {
                "q": "The Earth is classified in the curriculum as a:",
                "options": ["Planet", "Star", "Satellite", "Galaxy"],
                "answer": 0,
                "explain": "Outcome #241 classifies the Earth as a planet."
            },
            {
                "q": "The Moon is classified in the curriculum as a:",
                "options": ["Satellite", "Star", "Planet", "Meteor"],
                "answer": 0,
                "explain": "Outcome #241 classifies the Moon as a satellite."
            },
            {
                "q": "What is the opposite of 'close' according to Outcome #57?",
                "options": ["open", "night", "near", "dark"],
                "answer": 0,
                "explain": "Outcome #57 lists opposites like ‘close/open’."
            }
        ]
    }
]

# Write to js/learning_outcomes_data.js
js_content = f"""// ============================================================================
// LEARNING OUTCOMES EDUCATIONAL DATASET & INTERACTIVE ACTIVITIES
// Source: Provided Learning Outcomes Dataset (MCBSubjectskillAreaOutcomeID 1 to 440)
// STRICT COMPLIANCE: Content extracted EXCLUSIVELY from the provided file.
// ============================================================================

window.LEARNING_OUTCOMES_DATA = {json.dumps(final_outcomes, indent=2, ensure_ascii=False)};

window.LTP_QUIZZES = {json.dumps(quizzes, indent=2, ensure_ascii=False)};

window.LTP_MINI_GAMES = {json.dumps(mini_games, indent=2, ensure_ascii=False)};
"""

with open('js/learning_outcomes_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Successfully generated js/learning_outcomes_data.js with {len(final_outcomes)} outcomes, {len(quizzes)} quizzes, and {len(mini_games)} mini-games!")
