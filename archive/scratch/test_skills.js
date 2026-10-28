const CLASS_CURRICULUM_SUBJECTS = {
    "I": ["English", "Mathematics"],
    "II": ["English", "Mathematics"],
    "III": ["English", "Mathematics", "EVS"],
    "IV": ["English", "Mathematics", "EVS"],
    "V": ["English", "Mathematics", "EVS"],
    "VI": ["English", "Mathematics", "Science", "Social Science"],
    "VII": ["English", "Mathematics", "Science", "Social Science"],
    "VIII": ["English", "Mathematics", "Science", "Social Science"]
};

const CurriculumIdeasMap = {
    "I": {
        "English": [
            { icon: "🔤", title: "Phonics & Sounds", prompt: "Beginning letter sounds, vowels (a, e, i, o, u) and consonants", skill: "Phonics & Sounds", time: "3 min" },
            { icon: "🐱", title: "Rhyming Words", prompt: "Simple 3-letter rhyming words like cat-hat, dog-log, sun-run", skill: "Rhyming Words", time: "3 min" },
            { icon: "🧸", title: "Naming Words (Nouns)", prompt: "Names of people, animals, everyday objects, and places", skill: "Naming Words / Nouns", time: "5 min" },
            { icon: "📖", title: "Sight Words", prompt: "High frequency early reading words: the, is, a, we, can, you", skill: "Sight Words", time: "3 min" },
            { icon: "↔️", title: "Opposite Words", prompt: "Simple opposites: big-small, hot-cold, up-down, happy-sad", skill: "Opposites / Antonyms", time: "3 min" }
        ],
        "Mathematics": [
            { icon: "🔢", title: "Counting 1-20", prompt: "Counting real objects, forward and backward numbers up to 20", skill: "Counting & Number Sense", time: "3 min" },
            { icon: "➕", title: "Simple Addition", prompt: "Adding numbers up to 10 with pictures and counters", skill: "Addition within 10", time: "3 min" },
            { icon: "➖", title: "Take Away (Subtract)", prompt: "Subtracting numbers within 10 with visual objects", skill: "Basic Subtraction", time: "3 min" },
            { icon: "🔺", title: "Basic 2D Shapes", prompt: "Identifying circles, squares, triangles, and rectangles", skill: "Shapes & Space", time: "5 min" },
            { icon: "📏", title: "Longer & Shorter", prompt: "Comparing objects: longer vs shorter, heavier vs lighter", skill: "Measurement & Comparison", time: "3 min" },
            { icon: "🎯", title: "Fun Patterns", prompt: "Repeating visual color, animal, and shape sequences", skill: "Patterns & Sequences", time: "3 min" }
        ]
    },
    "II": {
        "English": [
            { icon: "🔤", title: "Singular & Plural", prompt: "One and many: adding -s, -es, and irregular plurals", skill: "Plurals & Nouns", time: "5 min" },
            { icon: "🏃", title: "Action Verbs", prompt: "Doing words: jump, swim, write, and play in sentences", skill: "Action Verbs", time: "5 min" },
            { icon: "🎨", title: "Describing Words", prompt: "Adjectives describing colors, sizes, shapes, and feelings", skill: "Describing Adjectives", time: "5 min" },
            { icon: "❓", title: "Sentence Punctuation", prompt: "Capital letters, full stops, and question marks", skill: "Punctuation", time: "5 min" }
        ],
        "Mathematics": [
            { icon: "🔢", title: "2-Digit Place Value", prompt: "Tens and ones up to 99, expanded form and comparing numbers", skill: "Place Value & Numbers", time: "5 min" },
            { icon: "➕", title: "Addition with Carry", prompt: "2-digit addition with carry over and real-life shopping puzzles", skill: "2-Digit Addition", time: "5 min" },
            { icon: "➖", title: "Subtraction with Borrow", prompt: "2-digit subtraction with regrouping and word problems", skill: "2-Digit Subtraction", time: "5 min" },
            { icon: "🥤", title: "Capacity & Jugs", prompt: "Measuring liquids in litres (L) and millilitres (mL), pouring into jugs", skill: "Capacity & Litres", time: "5 min" },
            { icon: "⏰", title: "Telling the Clock", prompt: "Reading analog clock hours and half hours (o'clock, half past)", skill: "Time & Clock", time: "5 min" },
            { icon: "💰", title: "Coins & Currency", prompt: "Indian rupee notes and coins, making amounts to buy pencils and toys", skill: "Money & Currency", time: "5 min" }
        ]
    },
    "III": {
        "English": [
            { icon: "👤", title: "Pronouns", prompt: "Replacing repetitive nouns with he, she, it, they, we", skill: "Pronouns", time: "5 min" },
            { icon: "📍", title: "Prepositions of Place", prompt: "Position words: in, on, under, behind, in front of, between", skill: "Prepositions", time: "5 min" },
            { icon: "⚡", title: "Past Tense Verbs", prompt: "Regular past tense verbs (-ed) and irregular verbs (went, saw)", skill: "Past Tense", time: "5 min" },
            { icon: "💬", title: "Compound Words", prompt: "Joining words: rainbow, butterfly, jellyfish, sunflower", skill: "Word Building", time: "5 min" }
        ],
        "Mathematics": [
            { icon: "🔢", title: "3-Digit Numbers", prompt: "Hundreds, tens, and units up to 999, number names and rounding", skill: "3-Digit Place Value", time: "5 min" },
            { icon: "✖️", title: "Multiplication Tables", prompt: "Times tables 2 to 9, repeated addition, and array word problems", skill: "Multiplication Facts", time: "5 min" },
            { icon: "➗", title: "Equal Sharing (Division)", prompt: "Dividing objects into equal groups, sharing marbles and sweets", skill: "Division Basics", time: "5 min" },
            { icon: "🍰", title: "Fractions Intro", prompt: "Halves (1/2), thirds (1/3), and quarters (1/4) of shapes", skill: "Fractions Basics", time: "5 min" },
            { icon: "⚖️", title: "Kilograms & Grams", prompt: "Converting kg to g, weighing groceries and balancing scales", skill: "Mass & Weight", time: "5 min" }
        ],
        "EVS": [
            { icon: "🌿", title: "Plant Parts & Leaves", prompt: "Roots, stem, leaves, flowers, leaf venation, photosynthesis", skill: "Plant Anatomy", time: "5 min" },
            { icon: "🐦", title: "Birds & Their Beaks", prompt: "Different types of beaks, claws, feathers, and nest building", skill: "Birds & Adaptations", time: "5 min" },
            { icon: "🚚", title: "Means of Transport", prompt: "Land, water, air travel, fuel used, and ancient vs modern vehicles", skill: "Transport & Travel", time: "5 min" },
            { icon: "💧", title: "Water Sources & Rain", prompt: "Rivers, wells, rainwater harvesting, filtration, and boiling", skill: "Water Resources", time: "5 min" },
            { icon: "🫀", title: "Human Organ Systems", prompt: "Heart, lungs, stomach, brain, and how they keep us healthy", skill: "Human Organs", time: "5 min" },
            { icon: "🪨", title: "Solids, Liquids, Gases", prompt: "Three states of matter: ice, liquid water, steam properties", skill: "States of Matter", time: "5 min" },
            { icon: "🧲", title: "Fun with Magnets", prompt: "Attracting iron nails, North and South poles, magnetic toys", skill: "Magnetism Basics", time: "5 min" },
            { icon: "🗺️", title: "Directions & Compass", prompt: "North, South, East, West, Sunrise direction, and map reading", skill: "Maps & Directions", time: "5 min" },
            { icon: "🏛️", title: "Our Heritage Monuments", prompt: "Taj Mahal, Red Fort, Qutub Minar, India Gate, and ancient temples", skill: "Indian Heritage", time: "5 min" }
        ]
    },
    "IV": {
        "English": [
            { icon: "🔤", title: "Adverbs of Manner (-ly)", prompt: "Identifying and using adverbs: swiftly, gracefully, loudly, carefully", skill: "Adverbs & Grammar", time: "5 min" },
            { icon: "🔗", title: "Conjunctions (Connectors)", prompt: "Joining sentences with and, but, because, although, or, so", skill: "Conjunctions", time: "5 min" },
            { icon: "📖", title: "Reading Comprehension", prompt: "Short passage inference, main idea, vocabulary in context, moral", skill: "Reading Comprehension", time: "10 min" },
            { icon: "🗣️", title: "Direct Speech & Quotes", prompt: "Using quotation marks, speaker dialogue, and punctuation", skill: "Punctuation & Dialogue", time: "5 min" }
        ],
        "Mathematics": [
            { icon: "🍕", title: "Fractions & Decimals", prompt: "Equivalent fractions, comparing fractions, and tenths/hundredths", skill: "Fractions & Decimals", time: "5 min" },
            { icon: "✖️", title: "Multi-Digit Multiplication", prompt: "Multiplying 2-digit by 2-digit numbers, mental math shortcuts", skill: "Multiplication Operations", time: "5 min" },
            { icon: "📐", title: "Perimeter & Area", prompt: "Measuring perimeter and area of rectangles and squares using grids", skill: "Perimeter & Area", time: "5 min" },
            { icon: "⏰", title: "Elapsed Time & 24h Clock", prompt: "Calculating start and end times, converting 12h to 24h railway time", skill: "Time Calculations", time: "5 min" },
            { icon: "📊", title: "Bar Charts & Pictographs", prompt: "Reading and drawing bar charts, interpreting tally marks and tables", skill: "Data & Graphing", time: "5 min" }
        ],
        "EVS": [
            { icon: "⚡", title: "Electricity & Circuits", prompt: "Simple circuits, batteries, bulbs, switches, conductors and insulators", skill: "Electric Circuits", time: "5 min" },
            { icon: "🪐", title: "The Solar System", prompt: "8 planets in order, revolution, rotation, day/night, and Moon phases", skill: "Solar System & Space", time: "5 min" },
            { icon: "🧲", title: "Magnets & Poles", prompt: "Attraction, repulsion, magnetic field, and making an electromagnet", skill: "Magnetism", time: "5 min" },
            { icon: "💧", title: "Water Cycle & Clouds", prompt: "Evaporation, condensation, rain, and clean drinking water", skill: "Water Cycle", time: "5 min" },
            { icon: "🦷", title: "Teeth & Digestion", prompt: "Types of teeth (incisors, molars), plaque, and digestive organs", skill: "Human Digestion", time: "5 min" },
            { icon: "🌳", title: "Forests & Wildlife", prompt: "Endangered animals, national parks, tiger conservation", skill: "Ecology & Wildlife", time: "5 min" },
            { icon: "🗑️", title: "Waste Management (3Rs)", prompt: "Reduce, Reuse, Recycle, biodegradable vs plastic waste", skill: "Environmental Care", time: "5 min" },
            { icon: "🌾", title: "From Seed to Plate", prompt: "Farming stages: ploughing, sowing, harvesting, and markets", skill: "Agriculture & Food", time: "5 min" },
            { icon: "🗺️", title: "Physical Features of India", prompt: "Himalayas, Northern Plains, Thar Desert, Deccan Plateau, Coastal Plains", skill: "Geography of India", time: "5 min" },
            { icon: "🏛️", title: "Civic Life & Panchayat", prompt: "Gram Panchayat, Municipal Corporation, public services, and taxes", skill: "Civics & Governance", time: "5 min" }
        ]
    },
    "V": {
        "English": [
            { icon: "✨", title: "Continuous & Perfect Tenses", prompt: "Present perfect (has/have seen) and past continuous (was running)", skill: "Advanced Verb Tenses", time: "5 min" },
            { icon: "🤝", title: "Subject-Verb Agreement", prompt: "Rules of singular/plural subject-verb pairing with tricky pronouns", skill: "Grammar & Syntax", time: "5 min" },
            { icon: "🎭", title: "Active & Passive Voice", prompt: "Converting active sentences to passive voice and identifying the agent", skill: "Active & Passive Voice", time: "5 min" },
            { icon: "📚", title: "Idioms & Metaphors", prompt: "Common idioms like 'piece of cake', 'break the ice', and similes/metaphors", skill: "Idioms & Figurative Language", time: "5 min" }
        ],
        "Mathematics": [
            { icon: "🔢", title: "Factors, Multiples & LCM/HCF", prompt: "Prime and composite numbers, divisibility tests, finding HCF and LCM", skill: "Factors & Multiples", time: "5 min" },
            { icon: "➗", title: "Decimals Operations", prompt: "Addition, subtraction, multiplication of decimals with money word problems", skill: "Decimals Operations", time: "5 min" },
            { icon: "📐", title: "Area & Volume of Shapes", prompt: "Area of rectangles and triangles, volume of cuboids in cubic cm", skill: "Area & Volume Mensuration", time: "10 min" },
            { icon: "📈", title: "Percentages & Fractions", prompt: "Converting fractions to percentages, discount and score percentage calculation", skill: "Percentages", time: "5 min" },
            { icon: "🧭", title: "Angles & Degrees", prompt: "Acute, right, obtuse, straight angles, measuring angles with protractor", skill: "Geometry & Angles", time: "5 min" }
        ],
        "EVS": [
            { icon: "🌿", title: "Photosynthesis & Nutrition", prompt: "Chlorophyll, stomata, xylem, phloem, sunlight, and starch production", skill: "Plant Biology", time: "5 min" },
            { icon: "🦴", title: "Skeletal & Nervous System", prompt: "206 bones, ball-and-socket joint, spinal cord, sensory and motor nerves", skill: "Human Anatomy", time: "5 min" },
            { icon: "🦠", title: "Microbes & Food Preservation", prompt: "Bacteria, fungi, viruses, pasteurization, salting, canning, and pickling", skill: "Microbiology & Food", time: "5 min" },
            { icon: "🌪️", title: "Natural Disasters & Safety", prompt: "Earthquakes (Richter scale), tsunamis, cyclones, and disaster safety measures", skill: "Earth Science & Safety", time: "5 min" },
            { icon: "⚙️", title: "Simple Machines", prompt: "Six simple machines: lever (1st, 2nd, 3rd class), pulley, inclined plane", skill: "Physics & Mechanics", time: "5 min" },
            { icon: "🔋", title: "Renewable Energy", prompt: "Solar panels, windmills, hydroelectric dams, and conserving fossil fuels", skill: "Clean Energy", time: "5 min" },
            { icon: "🌾", title: "Soil Layers & Conservation", prompt: "Topsoil, humus, subsoil, soil erosion, and terrace farming", skill: "Soil Science", time: "5 min" },
            { icon: "🌍", title: "Continents & Latitudes", prompt: "7 continents, Equator, Prime Meridian, Tropics of Cancer and Capricorn", skill: "World Geography", time: "5 min" },
            { icon: "📜", title: "India's Freedom Movement", prompt: "Revolt of 1857, Non-Cooperation Movement, Dandi March, Independence 1947", skill: "Modern Indian History", time: "10 min" }
        ]
    }
};

const fs = require('fs');
const catalog = JSON.parse(fs.readFileSync('full_games_catalog.json', 'utf8'));

Object.keys(CLASS_CURRICULUM_SUBJECTS).forEach(cls => {
    const subs = CLASS_CURRICULUM_SUBJECTS[cls];
    console.log(`Class ${cls} Curriculum Subjects:`, subs);
    subs.forEach(sub => {
        const ideas = CurriculumIdeasMap[cls]?.[sub] || [];
        const games = catalog.filter(g => g.class === cls && g.subject.toLowerCase() === sub.toLowerCase());
        console.log(`   ${sub}: ${ideas.length} ideas, ${games.length} catalog games`);
    });
});
