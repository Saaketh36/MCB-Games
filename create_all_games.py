import json
import os

# All games data with questions
games_content = {
    "pronunciation_game.html": {
        "title": "🎤 Pronunciation Game",
        "class": "I",
        "skill": "Speaking",
        "questions": [
            {"text": "How do you pronounce 'Apple'?", "options": ["Ap-ul", "Ay-pul", "App-le", "A-ple"], "correct": "Ap-ul"},
            {"text": "How do you pronounce 'Elephant'?", "options": ["El-uh-funt", "E-le-phant", "El-fant", "E-phant"], "correct": "El-uh-funt"},
            {"text": "How do you pronounce 'Orange'?", "options": ["Or-anj", "O-range", "Or-ing", "Ar-anj"], "correct": "Or-anj"},
            {"text": "How do you pronounce 'Water'?", "options": ["Wa-ter", "Wau-tar", "Wa-tar", "Wa-tur"], "correct": "Wa-ter"},
            {"text": "How do you pronounce 'Flower'?", "options": ["Flow-ur", "Flo-wer", "Flour", "Fl-wer"], "correct": "Flow-ur"}
        ]
    },
    "count_and_match.html": {
        "title": "🔢 Count & Match",
        "class": "I",
        "skill": "Numbers",
        "questions": [
            {"text": "How many apples are there: 🍎🍎🍎?", "options": ["2", "3", "4", "5"], "correct": "3"},
            {"text": "Match 5 with:", "options": ["●●●●", "●●●●●", "●●●●●●", "●●"], "correct": "●●●●●"},
            {"text": "Count: 🌟🌟🌟🌟🌟🌟", "options": ["5", "6", "7", "8"], "correct": "6"},
            {"text": "Which number is bigger? 7 or 4?", "options": ["4", "7", "Same", "Neither"], "correct": "7"},
            {"text": "Count fingers: ✋", "options": ["3", "4", "5", "6"], "correct": "5"}
        ]
    },
    "simple_addition.html": {
        "title": "➕ Simple Addition",
        "class": "I",
        "skill": "Addition",
        "questions": [
            {"text": "1 + 1 = ?", "options": ["1", "2", "3", "4"], "correct": "2"},
            {"text": "2 + 2 = ?", "options": ["2", "3", "4", "5"], "correct": "4"},
            {"text": "3 + 1 = ?", "options": ["2", "3", "4", "5"], "correct": "4"},
            {"text": "2 + 3 = ?", "options": ["3", "4", "5", "6"], "correct": "5"},
            {"text": "4 + 1 = ?", "options": ["3", "4", "5", "6"], "correct": "5"}
        ]
    },
    "shape_sorter.html": {
        "title": "⬜ Shape Sorter",
        "class": "I",
        "skill": "Shapes",
        "questions": [
            {"text": "Which is a circle?", "options": ["●", "■", "▲", "◊"], "correct": "●"},
            {"text": "Which is a square?", "options": ["●", "■", "▲", "◊"], "correct": "■"},
            {"text": "Which is a triangle?", "options": ["●", "■", "▲", "◊"], "correct": "▲"},
            {"text": "Which shape has 4 sides?", "options": ["Circle", "Triangle", "Square", "Line"], "correct": "Square"},
            {"text": "Which has 3 sides?", "options": ["Square", "Triangle", "Circle", "Pentagon"], "correct": "Triangle"}
        ]
    },
    "subtraction_basics.html": {
        "title": "➖ Subtraction Basics",
        "class": "I",
        "skill": "Subtraction",
        "questions": [
            {"text": "5 - 2 = ?", "options": ["2", "3", "4", "5"], "correct": "3"},
            {"text": "4 - 1 = ?", "options": ["2", "3", "4", "5"], "correct": "3"},
            {"text": "3 - 2 = ?", "options": ["1", "2", "3", "4"], "correct": "1"},
            {"text": "6 - 3 = ?", "options": ["2", "3", "4", "5"], "correct": "3"},
            {"text": "5 - 1 = ?", "options": ["3", "4", "5", "6"], "correct": "4"}
        ]
    },
    "life_skills_quiz.html": {
        "title": "🧼 Life Skills Quiz",
        "class": "I",
        "skill": "Life Skills",
        "questions": [
            {"text": "When should you wash your hands?", "options": ["Before eating", "After playing", "Both", "Never"], "correct": "Both"},
            {"text": "How do you greet someone?", "options": ["Say hello", "Wave", "Smile", "All of above"], "correct": "All of above"},
            {"text": "What should you do before sleep?", "options": ["Brush teeth", "Change clothes", "Both", "Play"], "correct": "Both"},
            {"text": "How do you say sorry?", "options": ["Say 'Sorry'", "Nod head", "Smile", "Walk away"], "correct": "Say 'Sorry'"},
            {"text": "What's good behavior?", "options": ["Sharing", "Listening", "Helping", "All"], "correct": "All"}
        ]
    },
    "nature_explorer.html": {
        "title": "🌿 Nature Explorer",
        "class": "I",
        "skill": "Nature",
        "questions": [
            {"text": "What grows on trees?", "options": ["Leaves", "Flowers", "Fruits", "All"], "correct": "All"},
            {"text": "Which animal flies?", "options": ["Dog", "Bird", "Fish", "Cow"], "correct": "Bird"},
            {"text": "What comes after rain?", "options": ["Snow", "Rainbow", "Wind", "Night"], "correct": "Rainbow"},
            {"text": "Where do fish live?", "options": ["Land", "Water", "Air", "Trees"], "correct": "Water"},
            {"text": "What is the sun?", "options": ["Star", "Planet", "Moon", "Cloud"], "correct": "Star"}
        ]
    },
    "safety_rules_quiz.html": {
        "title": "🚗 Safety Rules Quiz",
        "class": "I",
        "skill": "Safety",
        "questions": [
            {"text": "What color means stop?", "options": ["Yellow", "Green", "Red", "Blue"], "correct": "Red"},
            {"text": "Should you talk to strangers?", "options": ["Yes", "No", "Sometimes", "Always"], "correct": "No"},
            {"text": "What should you do at traffic light?", "options": ["Run", "Walk", "Wait", "Jump"], "correct": "Wait"},
            {"text": "Is fire safe to touch?", "options": ["Yes", "No", "Sometimes", "Always safe"], "correct": "No"},
            {"text": "Should you hold hand while crossing?", "options": ["No", "Yes", "Maybe", "Never"], "correct": "Yes"}
        ]
    },
    "multiplication_table.html": {
        "title": "⏱️ Times Table Game",
        "class": "II",
        "skill": "Multiplication",
        "questions": [
            {"text": "2 × 3 = ?", "options": ["5", "6", "7", "8"], "correct": "6"},
            {"text": "3 × 4 = ?", "options": ["10", "11", "12", "13"], "correct": "12"},
            {"text": "5 × 2 = ?", "options": ["8", "9", "10", "11"], "correct": "10"},
            {"text": "4 × 3 = ?", "options": ["10", "11", "12", "13"], "correct": "12"},
            {"text": "2 × 5 = ?", "options": ["8", "9", "10", "11"], "correct": "10"}
        ]
    },
    "division_basics.html": {
        "title": "➗ Division Basics",
        "class": "II",
        "skill": "Division",
        "questions": [
            {"text": "6 ÷ 2 = ?", "options": ["2", "3", "4", "5"], "correct": "3"},
            {"text": "8 ÷ 2 = ?", "options": ["2", "3", "4", "5"], "correct": "4"},
            {"text": "10 ÷ 5 = ?", "options": ["1", "2", "3", "4"], "correct": "2"},
            {"text": "12 ÷ 3 = ?", "options": ["2", "3", "4", "5"], "correct": "4"},
            {"text": "15 ÷ 3 = ?", "options": ["3", "4", "5", "6"], "correct": "5"}
        ]
    },
    "measurement_quiz.html": {
        "title": "📏 Measurement Quiz",
        "class": "II",
        "skill": "Measurement",
        "questions": [
            {"text": "Which is longest?", "options": ["Pencil", "Stick", "Finger", "Paper"], "correct": "Stick"},
            {"text": "How many centimeters in a meter?", "options": ["10", "50", "100", "1000"], "correct": "100"},
            {"text": "Which is heaviest?", "options": ["Feather", "Rock", "Paper", "Leaf"], "correct": "Rock"},
            {"text": "Which holds more water?", "options": ["Cup", "Bottle", "Bucket", "Spoon"], "correct": "Bucket"},
            {"text": "How many minutes in an hour?", "options": ["30", "60", "120", "12"], "correct": "60"}
        ]
    },
    "weather_quiz.html": {
        "title": "☀️ Weather Quiz",
        "class": "II",
        "skill": "Weather",
        "questions": [
            {"text": "What weather brings rain?", "options": ["Sunny", "Cloudy", "Clear", "Windy"], "correct": "Cloudy"},
            {"text": "When is it cold?", "options": ["Day", "Night", "Summer", "Noon"], "correct": "Night"},
            {"text": "What causes rainbow?", "options": ["Rain & Sun", "Wind", "Snow", "Cloud"], "correct": "Rain & Sun"},
            {"text": "Which is hottest season?", "options": ["Winter", "Summer", "Fall", "Spring"], "correct": "Summer"},
            {"text": "What comes from snow?", "options": ["Rain", "Ice", "Wind", "Cloud"], "correct": "Ice"}
        ]
    },
    "environment_game.html": {
        "title": "🌍 Environment Game",
        "class": "II",
        "skill": "Environment",
        "questions": [
            {"text": "What should we recycle?", "options": ["Plastic", "Paper", "Both", "None"], "correct": "Both"},
            {"text": "How to save water?", "options": ["Close tap", "Short shower", "Both", "None"], "correct": "Both"},
            {"text": "What pollutes air?", "options": ["Car smoke", "Factory", "Both", "Rain"], "correct": "Both"},
            {"text": "Best transport?", "options": ["Car", "Bus", "Bike", "Plane"], "correct": "Bus"},
            {"text": "What helps plants?", "options": ["Water", "Sun", "Both", "Wind"], "correct": "Both"}
        ]
    },
    "reading_comprehension_2.html": {
        "title": "📖 Reading Comprehension II",
        "class": "II",
        "skill": "Reading",
        "questions": [
            {"text": "What helps you understand?", "options": ["Reading", "Listening", "Both", "Neither"], "correct": "Both"},
            {"text": "Best time to read?", "options": ["Morning", "Evening", "Anytime quiet", "Never"], "correct": "Anytime quiet"},
            {"text": "What is a book?", "options": ["Paper", "Words", "Both", "Pictures"], "correct": "Both"},
            {"text": "How to remember story?", "options": ["Read again", "Think", "Both", "Skip"], "correct": "Both"},
            {"text": "Where do we read?", "options": ["Library", "Home", "Both", "Outside"], "correct": "Both"}
        ]
    },
    "writing_practice_2.html": {
        "title": "✍️ Writing Practice II",
        "class": "II",
        "skill": "Writing",
        "questions": [
            {"text": "What helps writing?", "options": ["Pen", "Paper", "Both", "None"], "correct": "Both"},
            {"text": "How to improve?", "options": ["Practice", "Read", "Both", "Play"], "correct": "Both"},
            {"text": "What's a sentence?", "options": ["Words", "Idea", "Both", "Letter"], "correct": "Both"},
            {"text": "When to write?", "options": ["Morning", "Evening", "Anytime", "Never"], "correct": "Anytime"},
            {"text": "Why write neatly?", "options": ["Look good", "Easy to read", "Both", "No reason"], "correct": "Both"}
        ]
    },
    "speaking_practice_2.html": {
        "title": "🗣️ Speaking Practice II",
        "class": "II",
        "skill": "Speaking",
        "questions": [
            {"text": "How to speak clearly?", "options": ["Loud", "Slow", "Both", "Fast"], "correct": "Both"},
            {"text": "When speaking, look at?", "options": ["Ground", "Listener", "Wall", "Up"], "correct": "Listener"},
            {"text": "What helps confidence?", "options": ["Practice", "Listen", "Both", "Hide"], "correct": "Both"},
            {"text": "How to start speaking?", "options": ["Jump", "Breathe", "Shout", "Whisper"], "correct": "Breathe"},
            {"text": "Good speaking is?", "options": ["Loud", "Clear", "Both", "Soft"], "correct": "Both"}
        ]
    },
    "fraction_basics.html": {
        "title": "🥧 Fraction Basics",
        "class": "III",
        "skill": "Fractions",
        "questions": [
            {"text": "What is 1/2?", "options": ["One third", "Half", "Quarter", "Whole"], "correct": "Half"},
            {"text": "What is 1/4?", "options": ["Half", "Third", "Quarter", "Whole"], "correct": "Quarter"},
            {"text": "2/2 equals?", "options": ["Half", "1", "2", "Quarter"], "correct": "1"},
            {"text": "1/3 is?", "options": ["Half", "Quarter", "One third", "Whole"], "correct": "One third"},
            {"text": "Which is bigger: 1/2 or 1/4?", "options": ["1/4", "1/2", "Same", "Neither"], "correct": "1/2"}
        ]
    },
    "plant_parts_quiz.html": {
        "title": "🌱 Plant Parts Quiz",
        "class": "III",
        "skill": "Plants",
        "questions": [
            {"text": "What do roots do?", "options": ["Make leaves", "Hold water", "Make flowers", "Both B&C"], "correct": "Both B&C"},
            {"text": "What is green in plants?", "options": ["Root", "Stem", "Leaf", "Flower"], "correct": "Leaf"},
            {"text": "What absorbs water?", "options": ["Leaf", "Stem", "Root", "Flower"], "correct": "Root"},
            {"text": "What carries water?", "options": ["Leaf", "Stem", "Flower", "Seed"], "correct": "Stem"},
            {"text": "Where are seeds?", "options": ["Root", "Stem", "Leaf", "Flower"], "correct": "Flower"}
        ]
    },
    "animal_matcher.html": {
        "title": "🦁 Animal Matcher",
        "class": "III",
        "skill": "Animals",
        "questions": [
            {"text": "Where do fish live?", "options": ["Land", "Air", "Water", "Tree"], "correct": "Water"},
            {"text": "Where do birds live?", "options": ["Water", "Ground", "Air", "Underground"], "correct": "Air"},
            {"text": "Which is farm animal?", "options": ["Lion", "Cow", "Tiger", "Bear"], "correct": "Cow"},
            {"text": "Which animal flies?", "options": ["Bat", "Cow", "Fish", "Turtle"], "correct": "Bat"},
            {"text": "Which is wild animal?", "options": ["Dog", "Cat", "Tiger", "Rabbit"], "correct": "Tiger"}
        ]
    },
    "decimal_identifier.html": {
        "title": "🔢 Decimal Identifier",
        "class": "IV",
        "skill": "Decimals",
        "questions": [
            {"text": "What is 0.5?", "options": ["One", "Half", "Quarter", "Double"], "correct": "Half"},
            {"text": "0.25 equals?", "options": ["Half", "Quarter", "Third", "Whole"], "correct": "Quarter"},
            {"text": "1.5 means?", "options": ["One half", "One and half", "One third", "One quarter"], "correct": "One and half"},
            {"text": "0.1 is?", "options": ["One tenth", "One half", "Half", "Quarter"], "correct": "One tenth"},
            {"text": "2.5 equals?", "options": ["Two", "Two and half", "Three", "Five"], "correct": "Two and half"}
        ]
    },
    "geometry_game.html": {
        "title": "📐 Geometry Game",
        "class": "IV",
        "skill": "Geometry",
        "questions": [
            {"text": "How many sides has square?", "options": ["3", "4", "5", "6"], "correct": "4"},
            {"text": "How many sides pentagon?", "options": ["4", "5", "6", "7"], "correct": "5"},
            {"text": "What is angle?", "options": ["Side", "Corner", "Edge", "Line"], "correct": "Corner"},
            {"text": "Right angle is?", "options": ["45°", "60°", "90°", "180°"], "correct": "90°"},
            {"text": "Circle has?", "options": ["0 sides", "1 side", "Infinite", "2 sides"], "correct": "0 sides"}
        ]
    },
    "data_collector.html": {
        "title": "📊 Data Collector",
        "class": "IV",
        "skill": "Data",
        "questions": [
            {"text": "What is data?", "options": ["Numbers", "Facts", "Both", "Pictures"], "correct": "Both"},
            {"text": "How to show data?", "options": ["Chart", "Graph", "Both", "Text"], "correct": "Both"},
            {"text": "Bar graph shows?", "options": ["Amounts", "Patterns", "Both", "Colors"], "correct": "Both"},
            {"text": "Pie chart shows?", "options": ["Parts", "Whole", "Both", "Time"], "correct": "Both"},
            {"text": "Why collect data?", "options": ["Understand", "Decide", "Both", "Fun"], "correct": "Both"}
        ]
    },
    "ecosystem_simulator.html": {
        "title": "🌲 Ecosystem Simulator",
        "class": "IV",
        "skill": "Ecosystems",
        "questions": [
            {"text": "What is ecosystem?", "options": ["Animals", "Plants", "Environment", "All"], "correct": "All"},
            {"text": "Food chain starts with?", "options": ["Animal", "Plant", "Sun", "Soil"], "correct": "Sun"},
            {"text": "Predator eats?", "options": ["Plant", "Animal", "Both", "Dirt"], "correct": "Animal"},
            {"text": "What needs sun?", "options": ["Animal", "Plant", "Water", "Soil"], "correct": "Plant"},
            {"text": "Decomposer breaks down?", "options": ["Rocks", "Dead matter", "Water", "Air"], "correct": "Dead matter"}
        ]
    },
    "body_systems_quiz.html": {
        "title": "💪 Body Systems Quiz",
        "class": "IV",
        "skill": "Body",
        "questions": [
            {"text": "Heart pumps?", "options": ["Air", "Blood", "Food", "Water"], "correct": "Blood"},
            {"text": "Lungs help with?", "options": ["Eating", "Breathing", "Seeing", "Hearing"], "correct": "Breathing"},
            {"text": "Brain controls?", "options": ["Heart", "Movement", "Both", "Digestion"], "correct": "Both"},
            {"text": "Bones do what?", "options": ["Move", "Support", "Both", "Digest"], "correct": "Both"},
            {"text": "Stomach breaks down?", "options": ["Water", "Food", "Air", "Bones"], "correct": "Food"}
        ]
    },
    "percentage_calculator.html": {
        "title": "📈 Percentage Calculator",
        "class": "V",
        "skill": "Percentages",
        "questions": [
            {"text": "What is 50%?", "options": ["Quarter", "Half", "Third", "Whole"], "correct": "Half"},
            {"text": "100% means?", "options": ["Half", "Whole", "Double", "Nothing"], "correct": "Whole"},
            {"text": "25% is?", "options": ["Half", "Quarter", "Third", "Whole"], "correct": "Quarter"},
            {"text": "75% of 100?", "options": ["25", "50", "75", "100"], "correct": "75"},
            {"text": "10% of 50?", "options": ["5", "10", "15", "50"], "correct": "5"}
        ]
    },
    "algebra_basics.html": {
        "title": "📐 Algebra Basics",
        "class": "V",
        "skill": "Algebra",
        "questions": [
            {"text": "x + 5 = 10, x = ?", "options": ["3", "4", "5", "6"], "correct": "5"},
            {"text": "2x = 8, x = ?", "options": ["2", "3", "4", "5"], "correct": "4"},
            {"text": "x - 3 = 7, x = ?", "options": ["9", "10", "11", "12"], "correct": "10"},
            {"text": "x + 2 = 5, x = ?", "options": ["2", "3", "4", "5"], "correct": "3"},
            {"text": "3x = 12, x = ?", "options": ["2", "3", "4", "5"], "correct": "4"}
        ]
    },
    "matter_states_quiz.html": {
        "title": "❄️ Matter States Quiz",
        "class": "V",
        "skill": "Matter",
        "questions": [
            {"text": "Solid is?", "options": ["Shapeless", "Fixed shape", "Flows", "Evaporates"], "correct": "Fixed shape"},
            {"text": "Liquid flows because?", "options": ["No shape", "Heavy", "Cold", "Empty"], "correct": "No shape"},
            {"text": "Gas becomes liquid?", "options": ["Heating", "Cooling", "Mixing", "Freezing"], "correct": "Cooling"},
            {"text": "Water freezes at?", "options": ["0°C", "25°C", "50°C", "100°C"], "correct": "0°C"},
            {"text": "Water boils at?", "options": ["0°C", "25°C", "50°C", "100°C"], "correct": "100°C"}
        ]
    },
    "forces_game.html": {
        "title": "⚡ Forces Game",
        "class": "V",
        "skill": "Forces",
        "questions": [
            {"text": "Force can make things?", "options": ["Move", "Stop", "Both", "Float"], "correct": "Both"},
            {"text": "Gravity pulls?", "options": ["Up", "Down", "Right", "Left"], "correct": "Down"},
            {"text": "Friction makes things?", "options": ["Faster", "Slower", "Stop", "Slide"], "correct": "Slower"},
            {"text": "Push and pull are?", "options": ["Gravity", "Forces", "Motion", "Energy"], "correct": "Forces"},
            {"text": "Magnetic force attracts?", "options": ["Wood", "Metal", "Plastic", "Paper"], "correct": "Metal"}
        ]
    },
    "life_cycles_quiz.html": {
        "title": "🔄 Life Cycles Quiz",
        "class": "V",
        "skill": "Life Cycles",
        "questions": [
            {"text": "Butterfly cycle starts as?", "options": ["Butterfly", "Caterpillar", "Egg", "Cocoon"], "correct": "Egg"},
            {"text": "Frog starts as?", "options": ["Tadpole", "Adult", "Egg", "Larva"], "correct": "Egg"},
            {"text": "Plant grows from?", "options": ["Leaf", "Seed", "Root", "Flower"], "correct": "Seed"},
            {"text": "Caterpillar becomes?", "options": ["Moth", "Butterfly", "Both", "Fly"], "correct": "Both"},
            {"text": "Life cycle has how many stages?", "options": ["2", "3", "4", "5"], "correct": "4"}
        ]
    },
    "ratio_game.html": {
        "title": "⚖️ Ratio Game",
        "class": "VI",
        "skill": "Ratios",
        "questions": [
            {"text": "2:4 simplified is?", "options": ["1:2", "1:4", "2:2", "4:2"], "correct": "1:2"},
            {"text": "If 1:3, then 2:?", "options": ["3", "4", "5", "6"], "correct": "6"},
            {"text": "3:6 equals?", "options": ["1:2", "1:3", "2:3", "3:3"], "correct": "1:2"},
            {"text": "Ratio compares?", "options": ["Size", "Amount", "Both", "Color"], "correct": "Both"},
            {"text": "1:2:3 total parts?", "options": ["3", "4", "5", "6"], "correct": "6"}
        ]
    },
    "statistics_quiz.html": {
        "title": "📊 Statistics Quiz",
        "class": "VI",
        "skill": "Statistics",
        "questions": [
            {"text": "Mean is?", "options": ["Middle", "Average", "Most", "Least"], "correct": "Average"},
            {"text": "Median is?", "options": ["Average", "Middle value", "Most common", "Highest"], "correct": "Middle value"},
            {"text": "Mode is?", "options": ["Average", "Middle", "Most common", "Least"], "correct": "Most common"},
            {"text": "Range is?", "options": ["Highest-Lowest", "Middle", "Average", "Mode"], "correct": "Highest-Lowest"},
            {"text": "Data means?", "options": ["Numbers", "Facts", "Both", "Ideas"], "correct": "Both"}
        ]
    },
    "cell_structure_game.html": {
        "title": "🔬 Cell Structure Game",
        "class": "VI",
        "skill": "Cells",
        "questions": [
            {"text": "Cell nucleus contains?", "options": ["Water", "DNA", "Energy", "Protein"], "correct": "DNA"},
            {"text": "Mitochondria makes?", "options": ["Food", "Energy", "Protein", "Waste"], "correct": "Energy"},
            {"text": "Cell membrane does?", "options": ["Makes protein", "Controls entry", "Stores water", "Produces energy"], "correct": "Controls entry"},
            {"text": "Chloroplast found in?", "options": ["Animals", "Plants", "Both", "Bacteria"], "correct": "Plants"},
            {"text": "Ribosome makes?", "options": ["Energy", "DNA", "Protein", "Fat"], "correct": "Protein"}
        ]
    },
    "reproduction_quiz.html": {
        "title": "🌸 Reproduction Quiz",
        "class": "VI",
        "skill": "Reproduction",
        "questions": [
            {"text": "Sexual reproduction needs?", "options": ["One parent", "Two parents", "Three", "Many"], "correct": "Two parents"},
            {"text": "Asexual makes copies?", "options": ["Different", "Same", "Smaller", "Larger"], "correct": "Same"},
            {"text": "Flower part for reproduction?", "options": ["Leaf", "Stem", "Stamen & Pistil", "Root"], "correct": "Stamen & Pistil"},
            {"text": "Pollination happens when?", "options": ["Rain", "Pollen transfers", "Wind", "Sun"], "correct": "Pollen transfers"},
            {"text": "Seed grows into?", "options": ["Flower", "Plant", "Tree", "Both B&C"], "correct": "Both B&C"}
        ]
    },
    "ecology_game.html": {
        "title": "🌍 Ecology Game",
        "class": "VI",
        "skill": "Ecology",
        "questions": [
            {"text": "Ecology studies?", "options": ["Organisms", "Environment", "Both", "Plants only"], "correct": "Both"},
            {"text": "Biome is?", "options": ["Forest", "Climate zone", "Both", "Desert"], "correct": "Both"},
            {"text": "Symbiosis is?", "options": ["Predator-prey", "Organism interaction", "Competition", "Mutation"], "correct": "Organism interaction"},
            {"text": "Conservation means?", "options": ["Destroy", "Protect", "Change", "Move"], "correct": "Protect"},
            {"text": "Biodiversity is?", "options": ["Many species", "Few species", "Same species", "No species"], "correct": "Many species"}
        ]
    },
    "physics_quiz.html": {
        "title": "⚡ Physics Quiz",
        "class": "VII",
        "skill": "Physics",
        "questions": [
            {"text": "Speed measures?", "options": ["Distance", "Time", "Distance/Time", "Power"], "correct": "Distance/Time"},
            {"text": "Velocity includes?", "options": ["Speed", "Direction", "Both", "Mass"], "correct": "Both"},
            {"text": "Acceleration is?", "options": ["Speed change", "Direction", "Both", "Distance"], "correct": "Both"},
            {"text": "Newton's law #1?", "options": ["F=ma", "Action=Reaction", "Inertia", "Energy"], "correct": "Inertia"},
            {"text": "Energy can't be?", "options": ["Changed", "Created/destroyed", "Transferred", "Stored"], "correct": "Created/destroyed"}
        ]
    },
    "chemistry_game.html": {
        "title": "⚗️ Chemistry Game",
        "class": "VII",
        "skill": "Chemistry",
        "questions": [
            {"text": "Atom contains?", "options": ["Nucleus", "Electrons", "Both", "Nothing"], "correct": "Both"},
            {"text": "Molecule is?", "options": ["One atom", "Atoms bonded", "Element", "Gas"], "correct": "Atoms bonded"},
            {"text": "Chemical reaction?", "options": ["No change", "New substance", "State change", "Movement"], "correct": "New substance"},
            {"text": "Acid pH is?", "options": ["7", "Above 7", "Below 7", "14"], "correct": "Below 7"},
            {"text": "Base pH is?", "options": ["7", "Above 7", "Below 7", "0"], "correct": "Above 7"}
        ]
    },
    "biology_quiz.html": {
        "title": "🧬 Biology Quiz",
        "class": "VII",
        "skill": "Biology",
        "questions": [
            {"text": "DNA contains?", "options": ["Proteins", "Genes", "Both", "Water"], "correct": "Genes"},
            {"text": "Photosynthesis makes?", "options": ["Energy", "Food", "Both", "Waste"], "correct": "Both"},
            {"text": "Respiration releases?", "options": ["Oxygen", "Energy", "Carbon", "Nitrogen"], "correct": "Energy"},
            {"text": "Evolution is?", "options": ["Change over time", "Development", "Growth", "Adaptation"], "correct": "Change over time"},
            {"text": "Natural selection favors?", "options": ["Weak", "Adapted", "Different", "Old"], "correct": "Adapted"}
        ]
    },
    "probability_game.html": {
        "title": "🎲 Probability Game",
        "class": "VII",
        "skill": "Probability",
        "questions": [
            {"text": "Probability ranges?", "options": ["0-10", "0-1", "1-100", "-1 to 1"], "correct": "0-1"},
            {"text": "Certain event probability?", "options": ["0", "0.5", "1", "2"], "correct": "1"},
            {"text": "Impossible probability?", "options": ["0", "0.5", "1", "-1"], "correct": "0"},
            {"text": "Fair coin P(heads)?", "options": ["0.25", "0.5", "0.75", "1"], "correct": "0.5"},
            {"text": "If 3 red, 2 blue?", "options": ["P(red)=0.6", "P(red)=0.4", "P(red)=0.5", "Equal"], "correct": "P(red)=0.6"}
        ]
    },
    "calculus_basics.html": {
        "title": "📈 Calculus Basics",
        "class": "VIII",
        "skill": "Calculus",
        "questions": [
            {"text": "Derivative measures?", "options": ["Area", "Rate of change", "Sum", "Product"], "correct": "Rate of change"},
            {"text": "Integral opposite of?", "options": ["Derivative", "Sum", "Division", "Multiplication"], "correct": "Derivative"},
            {"text": "Limit is?", "options": ["Maximum", "Approaching value", "Boundary", "End"], "correct": "Approaching value"},
            {"text": "Slope means?", "options": ["Height", "Rise/Run", "Distance", "Angle"], "correct": "Rise/Run"},
            {"text": "Curve analysis studies?", "options": ["Shape", "Behavior", "Both", "Color"], "correct": "Both"}
        ]
    },
    "advanced_physics.html": {
        "title": "🔬 Advanced Physics",
        "class": "VIII",
        "skill": "Physics",
        "questions": [
            {"text": "Quantum mechanics studies?", "options": ["Large objects", "Atoms/particles", "Planets", "Stars"], "correct": "Atoms/particles"},
            {"text": "Relativity by?", "options": ["Newton", "Einstein", "Galileo", "Kepler"], "correct": "Einstein"},
            {"text": "Wave-particle duality?", "options": ["Contradiction", "Nature of light", "Myth", "Impossible"], "correct": "Nature of light"},
            {"text": "Planck constant relates?", "options": ["Time", "Energy to frequency", "Mass", "Speed"], "correct": "Energy to frequency"},
            {"text": "Black hole has?", "options": ["Light", "Escape velocity > c", "Radiation", "Movement"], "correct": "Escape velocity > c"}
        ]
    },
    "advanced_chemistry.html": {
        "title": "⚛️ Advanced Chemistry",
        "class": "VIII",
        "skill": "Chemistry",
        "questions": [
            {"text": "Organic chemistry studies?", "options": ["Metals", "Carbon compounds", "Minerals", "Salts"], "correct": "Carbon compounds"},
            {"text": "Electrochemistry involves?", "options": ["Heat", "Electrons", "Light", "Sound"], "correct": "Electrons"},
            {"text": "Catalyst does?", "options": ["Slows reaction", "Speeds reaction", "Stops reaction", "Reverses reaction"], "correct": "Speeds reaction"},
            {"text": "Equilibrium means?", "options": ["Stopped", "Balanced", "Maximum", "Minimum"], "correct": "Balanced"},
            {"text": "Isotope differs in?", "options": ["Protons", "Electrons", "Neutrons", "All"], "correct": "Neutrons"}
        ]
    },
    "advanced_biology.html": {
        "title": "🧬 Advanced Biology",
        "class": "VIII",
        "skill": "Biology",
        "questions": [
            {"text": "Genetics studies?", "options": ["Traits", "Inheritance", "Both", "Evolution"], "correct": "Both"},
            {"text": "Allele is?", "options": ["Gene", "Gene variant", "Chromosome", "Protein"], "correct": "Gene variant"},
            {"text": "Dominant trait?", "options": ["Hidden", "Expressed", "Rare", "New"], "correct": "Expressed"},
            {"text": "Mutation causes?", "options": ["Growth", "Variation", "Death", "Movement"], "correct": "Variation"},
            {"text": "Mitosis produces?", "options": ["Variation", "Identical cells", "Different cells", "Gametes"], "correct": "Identical cells"}
        ]
    }
}

# Template HTML with placeholder for title, class, skill, and questions
html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Class {class_num}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        .header {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        }}
        .header h1 {{
            color: #667eea;
            font-size: 32px;
            margin-bottom: 10px;
        }}
        .header-info {{
            color: #666;
            font-size: 14px;
            margin-bottom: 15px;
        }}
        .progress-info {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 15px;
        }}
        .progress-bar {{
            flex: 1;
            height: 10px;
            background: #e0e0e0;
            border-radius: 10px;
            margin: 0 20px;
            overflow: hidden;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            width: 0%;
            transition: width 0.3s ease;
        }}
        .game-card {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
        }}
        .question-container {{
            margin-bottom: 30px;
        }}
        .question-number {{
            color: #667eea;
            font-weight: bold;
            margin-bottom: 10px;
            font-size: 14px;
        }}
        .question-text {{
            color: #333;
            font-size: 18px;
            font-weight: 500;
            margin-bottom: 20px;
        }}
        .options {{
            display: grid;
            gap: 12px;
        }}
        .option {{
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            background: white;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }}
        .option:hover {{
            border-color: #667eea;
            background: #f0f4ff;
        }}
        .option.disabled {{
            cursor: not-allowed;
            opacity: 0.7;
        }}
        .feedback-box {{
            margin-top: 20px;
            padding: 20px;
            border-radius: 10px;
            display: none;
            animation: slideIn 0.5s ease;
        }}
        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateY(10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        .feedback-box.show {{
            display: block;
        }}
        .feedback-box.correct {{
            background: #d4edda;
            border-left: 5px solid #28a745;
            color: #155724;
        }}
        .feedback-box.wrong {{
            background: #f8d7da;
            border-left: 5px solid #dc3545;
            color: #721c24;
        }}
        .feedback-content {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        .feedback-emoji {{
            font-size: 50px;
            min-width: 50px;
        }}
        .feedback-text {{
            flex: 1;
        }}
        .feedback-status {{
            font-size: 20px;
            font-weight: bold;
        }}
        .feedback-score {{
            font-size: 16px;
            margin-top: 8px;
            font-weight: bold;
        }}
        .nav-buttons {{
            display: flex;
            gap: 10px;
            margin-top: 30px;
        }}
        .btn {{
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
            flex: 1;
        }}
        .btn:hover:not(:disabled) {{
            transform: scale(1.05);
        }}
        .btn:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        .btn-next {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }}
        .results-screen {{
            display: none;
        }}
        .results-screen.show {{
            display: block;
        }}
        .final-results {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 40px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 20px;
        }}
        .final-score-display {{
            font-size: 80px;
            font-weight: bold;
            margin: 20px 0;
        }}
        .final-percentage {{
            font-size: 32px;
            margin: 15px 0;
        }}
        .performance-message {{
            font-size: 24px;
            font-weight: bold;
            margin: 15px 0;
        }}
        .stars {{
            font-size: 40px;
            margin: 15px 0;
        }}
        .results-summary {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .summary-row {{
            display: flex;
            justify-content: space-between;
            padding: 15px;
            border-bottom: 1px solid #eee;
            font-size: 16px;
        }}
        .summary-row.correct {{
            background: #d4edda;
            border-radius: 5px;
            margin-bottom: 10px;
        }}
        .summary-row.wrong {{
            background: #f8d7da;
            border-radius: 5px;
            margin-bottom: 10px;
        }}
        .answer-details {{
            background: white;
            border-radius: 10px;
        }}
        .answer-item {{
            border-bottom: 1px solid #eee;
            padding: 15px;
        }}
        .answer-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-weight: bold;
        }}
        .answer-status {{
            font-size: 24px;
        }}
        .answer-question {{
            color: #333;
            margin-bottom: 10px;
        }}
        .answer-given {{
            color: #666;
            font-size: 14px;
            margin-bottom: 8px;
        }}
        .answer-correct {{
            color: #28a745;
            font-size: 14px;
            font-weight: bold;
        }}
        .answer-points {{
            color: #667eea;
            font-size: 14px;
            font-weight: bold;
        }}
        .restart-btn {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div id="gameScreen">
            <div class="header">
                <h1 id="gameTitle">{title}</h1>
                <p class="header-info" id="gameInfo">Class {class_num} · Skill: {skill}</p>
                <div class="progress-info">
                    <span id="questionCounter">Question 1/5</span>
                    <div class="progress-bar">
                        <div class="progress-fill" id="progressFill"></div>
                    </div>
                    <span id="scoreCounter">Score: 0/50</span>
                </div>
            </div>

            <div class="game-card">
                <div class="question-container">
                    <div class="question-number" id="questionNum">Question 1/5</div>
                    <div class="question-text" id="questionText"></div>
                    <div class="options" id="optionsContainer"></div>

                    <div class="feedback-box" id="feedbackBox">
                        <div class="feedback-content">
                            <div class="feedback-emoji" id="feedbackEmoji"></div>
                            <div class="feedback-text">
                                <div class="feedback-status" id="feedbackStatus"></div>
                                <div class="feedback-score" id="feedbackScore"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="nav-buttons">
                    <button class="btn btn-next" id="nextBtn" onclick="goToNextQuestion()" disabled>
                        Next Question →
                    </button>
                </div>
            </div>
        </div>

        <div id="resultsScreen" class="results-screen">
            <div class="header">
                <h1>🎉 Quiz Complete!</h1>
            </div>

            <div class="game-card">
                <div class="final-results" id="finalResults"></div>

                <div class="results-summary">
                    <div class="summary-row correct">
                        <span>✅ Correct Answers</span>
                        <span id="correctCount">0/5</span>
                    </div>
                    <div class="summary-row wrong">
                        <span>❌ Wrong Answers</span>
                        <span id="wrongCount">0/5</span>
                    </div>
                    <div class="summary-row" style="background: #e3f2fd;">
                        <span>📊 Total Score</span>
                        <span id="totalScore">0/50</span>
                    </div>
                </div>

                <h3 style="margin: 20px 0 15px 0; color: #333;">📋 Answer Review</h3>
                <div class="answer-details" id="answerDetails"></div>

                <button class="restart-btn" onclick="location.reload()">Take Quiz Again</button>
            </div>
        </div>
    </div>

    <script>
        const gameConfig = {{
            title: "{title}",
            class: "{class_num}",
            skill: "{skill}",
            totalPoints: 50,
            pointsPerQuestion: 10
        }};

        const quizData = {{
            questions: {questions_json}
        }};

        let currentQuestion = 0;
        let userAnswers = {{}};
        let scores = {{}};
        let totalScore = 0;

        function initGame() {{
            document.getElementById('gameTitle').textContent = gameConfig.title;
            document.getElementById('gameInfo').textContent =
                `Class ${{gameConfig.class}} · Skill: ${{gameConfig.skill}}`;
            loadQuestion();
        }}

        function loadQuestion() {{
            const q = quizData.questions[currentQuestion];

            document.getElementById('questionText').textContent = q.text;
            document.getElementById('questionNum').textContent =
                `Question ${{currentQuestion + 1}}/${{quizData.questions.length}}`;
            document.getElementById('questionCounter').textContent =
                `Question ${{currentQuestion + 1}}/${{quizData.questions.length}}`;

            const progress = ((currentQuestion + 1) / quizData.questions.length) * 100;
            document.getElementById('progressFill').style.width = progress + '%';

            const container = document.getElementById('optionsContainer');
            container.innerHTML = '';

            q.options.forEach(option => {{
                const optionDiv = document.createElement('div');
                optionDiv.className = 'option';
                optionDiv.textContent = option;
                optionDiv.onclick = () => selectAnswer(option, q.id, q.correct, q.points);
                container.appendChild(optionDiv);
            }});

            document.getElementById('feedbackBox').classList.remove('show', 'correct', 'wrong');
            document.getElementById('nextBtn').disabled = true;
        }}

        function selectAnswer(option, questionId, correctAnswer, points) {{
            userAnswers[questionId] = option;
            const isCorrect = option === correctAnswer;

            document.querySelectorAll('.option').forEach(el => {{
                el.classList.add('disabled');
                el.style.pointerEvents = 'none';
            }});

            showFeedback(isCorrect, points);
            scores[questionId] = isCorrect ? points : 0;
            document.getElementById('nextBtn').disabled = false;
        }}

        function showFeedback(isCorrect, points) {{
            const feedbackBox = document.getElementById('feedbackBox');
            const feedbackEmoji = document.getElementById('feedbackEmoji');
            const feedbackStatus = document.getElementById('feedbackStatus');
            const feedbackScore = document.getElementById('feedbackScore');

            feedbackBox.classList.add('show');

            if (isCorrect) {{
                feedbackBox.classList.add('correct');
                feedbackBox.classList.remove('wrong');
                feedbackEmoji.textContent = '👏';
                feedbackStatus.textContent = '✅ CORRECT!';
                feedbackScore.textContent = `Score: +${{points}} points`;
            }} else {{
                feedbackBox.classList.add('wrong');
                feedbackBox.classList.remove('correct');
                feedbackEmoji.textContent = '❌';
                feedbackStatus.textContent = '❌ WRONG';
                feedbackScore.textContent = `Score: 0 points`;
            }}

            totalScore = Object.values(scores).reduce((a, b) => a + b, 0);
            document.getElementById('scoreCounter').textContent = `Score: ${{totalScore}}/${{gameConfig.totalPoints}}`;
        }}

        function goToNextQuestion() {{
            currentQuestion++;

            if (currentQuestion < quizData.questions.length) {{
                loadQuestion();
            }} else {{
                showResults();
            }}
        }}

        function showResults() {{
            document.getElementById('gameScreen').style.display = 'none';
            document.getElementById('resultsScreen').classList.add('show');

            const correctCount = Object.values(scores).filter(s => s > 0).length;
            const totalQuestions = quizData.questions.length;
            const percentage = (totalScore / gameConfig.totalPoints) * 100;

            let emoji = '', stars = '', message = '';

            if (percentage >= 80) {{
                emoji = '🎉';
                stars = '⭐⭐⭐⭐⭐';
                message = 'Excellent! Outstanding performance!';
            }} else if (percentage >= 60) {{
                emoji = '👏';
                stars = '⭐⭐⭐⭐';
                message = 'Great job! Good performance!';
            }} else if (percentage >= 40) {{
                emoji = '👍';
                stars = '⭐⭐⭐';
                message = 'Good effort! Keep practicing!';
            }} else {{
                emoji = '💪';
                stars = '⭐⭐';
                message = 'Keep trying! You can do better!';
            }}

            document.getElementById('finalResults').innerHTML = `
                <div style="font-size: 60px; margin-bottom: 15px;">${{emoji}}</div>
                <div class="final-score-display">${{totalScore}}/${{gameConfig.totalPoints}}</div>
                <div class="final-percentage">${{percentage.toFixed(1)}}%</div>
                <div class="performance-message">${{message}}</div>
                <div class="stars">${{stars}}</div>
            `;

            document.getElementById('correctCount').textContent = `${{correctCount}}/${{totalQuestions}}`;
            document.getElementById('wrongCount').textContent = `${{totalQuestions - correctCount}}/${{totalQuestions}}`;
            document.getElementById('totalScore').textContent = `${{totalScore}}/${{gameConfig.totalPoints}}`;

            const answerDetails = document.getElementById('answerDetails');
            answerDetails.innerHTML = '';

            quizData.questions.forEach((q, index) => {{
                const userAnswer = userAnswers[q.id];
                const isCorrect = userAnswer === q.correct;
                const earnedPoints = scores[q.id];

                const item = document.createElement('div');
                item.className = 'answer-item';
                item.innerHTML = `
                    <div class="answer-header">
                        <span>Question ${{index + 1}}</span>
                        <span class="answer-status">${{isCorrect ? '✅' : '❌'}}</span>
                    </div>
                    <div class="answer-question">${{q.text}}</div>
                    <div class="answer-given">Your Answer: <strong>${{userAnswer}}</strong></div>
                    ${{!isCorrect ? `<div class="answer-correct">Correct Answer: ${{q.correct}}</div>` : ''}}
                    <div class="answer-points">Score: ${{earnedPoints}}/10 points</div>
                `;

                answerDetails.appendChild(item);
            }});
        }}

        initGame();
    </script>
</body>
</html>
'''

# Create all game files
base_path = r'C:\Users\Charitha Sadineni\OneDrive\Desktop\Games'
os.chdir(base_path)

for filename, game_info in games_content.items():
    # Convert questions to JSON format
    questions_json = json.dumps(
        [{"id": i+1, "text": q["text"], "options": q["options"], "correct": q["correct"], "points": 10}
         for i, q in enumerate(game_info["questions"])],
        indent=12
    )

    # Generate HTML
    html_content = html_template.format(
        title=game_info["title"],
        class_num=game_info["class"],
        skill=game_info["skill"],
        questions_json=questions_json
    )

    # Write file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Created: {filename}")

print(f"\n🎉 All games created successfully!")
print(f"Total: {len(games_content)} game files")
