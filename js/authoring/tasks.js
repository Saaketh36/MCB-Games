/* ====================================================
   TEACHER CREATE NEW TASK ENGINE
   ==================================================== */
const CUSTOM_TASKS_KEY = 'mcb_custom_tasks_v1';

function loadCustomTasks() {
    try {
        const raw = localStorage.getItem(CUSTOM_TASKS_KEY);
        return raw ? JSON.parse(raw) : [];
    } catch (e) {
        return [];
    }
}

function saveCustomTasks(tasks) {
    try {
        localStorage.setItem(CUSTOM_TASKS_KEY, JSON.stringify(tasks));
    } catch (e) { }
}

function loadCustomTasksIntoCatalog() {
    const saved = loadCustomTasks();
    saved.forEach(task => {
        if (!GamesCatalog.some(g => g.id === task.id)) {
            GamesCatalog.unshift(task);
        }
    });
}

let currentCreateTaskQuestions = [];
let currentAiIdeaOffset = 0;
let currentCreateTaskInteractiveConfig = null;
let currentCreateTaskGameType = 'auto';

function handleGameTypeSelectionChange(val) {
    currentCreateTaskGameType = val;
}

function clearCreatedInteractiveConfig() {
    currentCreateTaskInteractiveConfig = null;
    const previewCard = document.getElementById('aiBuiltGamePreviewCard');
    if (previewCard) previewCard.style.display = 'none';
    const gtSelect = document.getElementById('newTaskGameType');
    if (gtSelect) gtSelect.value = 'mcq';
    currentCreateTaskGameType = 'MCQ Quiz';
    showToastNotification("Interactive game removed. Reverted to standard quiz.");
}

function testPlayCreatedGame() {
    const title = document.getElementById('newTaskTitle')?.value?.trim() || 'Interactive Mini-Game Preview';
    const cls = document.getElementById('newTaskClass')?.value || AppState.selectedClass || 'IV';
    const subject = document.getElementById('newTaskSubject')?.value || 'Science';
    const skill = document.getElementById('newTaskSkillArea')?.value?.trim() || 'Curriculum Skill';

    if (!currentCreateTaskInteractiveConfig) {
        showToastNotification("No interactive game config found to test play.");
        return;
    }

    const tempGame = {
        id: 'PREVIEW-' + Date.now(),
        title: title,
        class: cls,
        subject: subject,
        skillArea: skill,
        gameType: currentCreateTaskGameType || 'Sort & Group',
        interactiveConfig: currentCreateTaskInteractiveConfig,
        questions: (currentCreateTaskQuestions && currentCreateTaskQuestions.length > 0)
            ? currentCreateTaskQuestions
            : [{
                prompt: `Review what you learned in ${title}!`,
                options: ['Core Concepts', 'Incorrect Distractor', 'Unrelated Fact', 'Random Noise'],
                answer: 0,
                explanation: `Review challenge for ${title}.`
            }]
    };

    AppState.activeMissionGame = tempGame;
    AppState.selectedStudent = { name: "Teacher Preview Mode", roll: 0 };
    launchQuestRunner();
}

// ============================================================
// CLASS & SUBJECT DYNAMIC CURRICULUM IDEAS MAP
// ============================================================
const CurriculumIdeasMap = {
    "I": {
        "Mathematics": [
            { icon: "🔢", title: "Counting 1-20", prompt: "Counting real objects, forward and backward numbers up to 20", skill: "Counting & Number Sense", time: "3 min" },
            { icon: "➕", title: "Simple Addition", prompt: "Adding numbers up to 10 with pictures and counters", skill: "Addition within 10", time: "3 min" },
            { icon: "➖", title: "Take Away (Subtract)", prompt: "Subtracting numbers within 10 with visual objects", skill: "Basic Subtraction", time: "3 min" },
            { icon: "🔺", title: "Basic 2D Shapes", prompt: "Identifying circles, squares, triangles, and rectangles", skill: "Shapes & Space", time: "5 min" },
            { icon: "📏", title: "Longer & Shorter", prompt: "Comparing objects: longer vs shorter, heavier vs lighter", skill: "Measurement & Comparison", time: "3 min" },
            { icon: "🎯", title: "Fun Patterns", prompt: "Repeating visual color, animal, and shape sequences", skill: "Patterns & Sequences", time: "3 min" }
        ],
        "English": [
            { icon: "🔤", title: "Phonics & Sounds", prompt: "Beginning letter sounds, vowels (a, e, i, o, u) and consonants", skill: "Phonics & Sounds", time: "3 min" },
            { icon: "🐱", title: "Rhyming Words", prompt: "Simple 3-letter rhyming words like cat-hat, dog-log, sun-run", skill: "Rhyming Words", time: "3 min" },
            { icon: "🧸", title: "Naming Words (Nouns)", prompt: "Names of people, animals, everyday objects, and places", skill: "Naming Words / Nouns", time: "5 min" },
            { icon: "📖", title: "Sight Words", prompt: "High frequency early reading words: the, is, a, we, can, you", skill: "Sight Words", time: "3 min" },
            { icon: "↔️", title: "Opposite Words", prompt: "Simple opposites: big-small, hot-cold, up-down, happy-sad", skill: "Opposites / Antonyms", time: "3 min" }
        ],
        "EVS": [
            { icon: "🏡", title: "My Family & Home", prompt: "Family members, rooms in the house, and helping parents", skill: "Family & Home", time: "3 min" },
            { icon: "👀", title: "5 Senses", prompt: "Eyes see, ears hear, nose smells, tongue tastes, skin feels", skill: "Sense Organs", time: "5 min" },
            { icon: "🐾", title: "Animals & Sounds", prompt: "Farm animals, pets, and the sounds they make", skill: "Animal World", time: "3 min" },
            { icon: "🧼", title: "Clean Habits", prompt: "Handwashing, brushing teeth, and clean living habits", skill: "Health & Hygiene", time: "3 min" },
            { icon: "🍎", title: "Healthy Food", prompt: "Fruits, vegetables, drinking water, and avoiding junk food", skill: "Food & Health", time: "3 min" }
        ],
        "Science": [
            { icon: "☀️", title: "Day and Night", prompt: "The Sun in daytime, Moon and stars at night, daily routines", skill: "Day & Night Sky", time: "3 min" },
            { icon: "🌱", title: "Plants Around Us", prompt: "Leaves, flowers, trees, grass, and watering plants", skill: "Plants & Trees", time: "3 min" },
            { icon: "🌧️", title: "Weather & Rain", prompt: "Sunny, rainy, and windy days, using umbrellas and raincoats", skill: "Weather & Seasons", time: "3 min" },
            { icon: "🐶", title: "Living & Non-Living", prompt: "Living things grow and breathe; non-living things (toys, rocks)", skill: "Living vs Non-Living", time: "5 min" }
        ],
        "Social Science": [
            { icon: "🤝", title: "Good Manners", prompt: "Saying please, thank you, sorry, sharing toys and helping friends", skill: "Values & Manners", time: "3 min" },
            { icon: "🏫", title: "My School", prompt: "Classroom objects, school rules, and playground games", skill: "School & Community", time: "3 min" },
            { icon: "👮", title: "Community Helpers", prompt: "Doctors, teachers, police, firefighters, and postmen", skill: "Our Helpers", time: "5 min" }
        ]
    },
    "II": {
        "Mathematics": [
            { icon: "🔢", title: "2-Digit Place Value", prompt: "Tens and ones up to 99, expanded form and comparing numbers", skill: "Place Value & Numbers", time: "5 min" },
            { icon: "➕", title: "Addition with Carry", prompt: "2-digit addition with carry over and real-life shopping puzzles", skill: "2-Digit Addition", time: "5 min" },
            { icon: "➖", title: "Subtraction with Borrow", prompt: "2-digit subtraction with regrouping and word problems", skill: "2-Digit Subtraction", time: "5 min" },
            { icon: "🥤", title: "Capacity & Jugs", prompt: "Measuring liquids in litres (L) and millilitres (mL), pouring into jugs", skill: "Capacity & Litres", time: "5 min" },
            { icon: "⏰", title: "Telling the Clock", prompt: "Reading analog clock hours and half hours (o'clock, half past)", skill: "Time & Clock", time: "5 min" },
            { icon: "💰", title: "Coins & Currency", prompt: "Indian rupee notes and coins, making amounts to buy pencils and toys", skill: "Money & Currency", time: "5 min" }
        ],
        "English": [
            { icon: "🔤", title: "Singular & Plural", prompt: "One and many: adding -s, -es, and irregular plurals", skill: "Plurals & Nouns", time: "5 min" },
            { icon: "🏃", title: "Action Verbs", prompt: "Doing words: jump, swim, write, and play in sentences", skill: "Action Verbs", time: "5 min" },
            { icon: "🎨", title: "Describing Words", prompt: "Adjectives describing colors, sizes, shapes, and feelings", skill: "Describing Adjectives", time: "5 min" },
            { icon: "❓", title: "Sentence Punctuation", prompt: "Capital letters, full stops, and question marks", skill: "Punctuation", time: "5 min" }
        ],
        "EVS": [
            { icon: "🏠", title: "Types of Houses", prompt: "Kutcha houses, pucca houses, flats, stilt houses, and igloos", skill: "Shelter & Houses", time: "5 min" },
            { icon: "🚦", title: "Traffic & Road Safety", prompt: "Traffic lights (red, yellow, green), zebra crossings, walking safely", skill: "Safety & Traffic Rules", time: "5 min" },
            { icon: "🌦️", title: "Four Seasons", prompt: "Summer, Monsoon, Winter, Spring clothes, weather, and foods", skill: "Seasons & Weather", time: "5 min" },
            { icon: "💧", title: "Water and Its Uses", prompt: "Drinking, cooking, washing, saving water, and avoiding wastage", skill: "Water Conservation", time: "5 min" }
        ],
        "Science": [
            { icon: "🐾", title: "Animal Habitats", prompt: "Land, water, and desert animals: their homes, food, and young ones", skill: "Animal Habitats", time: "5 min" },
            { icon: "🌿", title: "Plant Uses", prompt: "Medicines, fruits, wood, cotton, and oxygen from plants", skill: "Uses of Plants", time: "5 min" },
            { icon: "💨", title: "Air & Wind", prompt: "Air occupies space, moving air is wind, pinwheels and kites", skill: "Air & Atmosphere", time: "5 min" }
        ],
        "Social Science": [
            { icon: "🎉", title: "Indian Festivals", prompt: "Diwali, Eid, Christmas, Holi, Gurpurab and national festivals", skill: "Culture & Festivals", time: "5 min" },
            { icon: "🇮🇳", title: "National Symbols", prompt: "Tiranga flag, tiger, peacock, lotus, and national anthem", skill: "National Symbols", time: "5 min" }
        ]
    },
    "III": {
        "Mathematics": [
            { icon: "🔢", title: "3-Digit Numbers", prompt: "Hundreds, tens, and units up to 999, number names and rounding", skill: "3-Digit Place Value", time: "5 min" },
            { icon: "✖️", title: "Multiplication Tables", prompt: "Times tables 2 to 9, repeated addition, and array word problems", skill: "Multiplication Facts", time: "5 min" },
            { icon: "➗", title: "Equal Sharing (Division)", prompt: "Dividing objects into equal groups, sharing marbles and sweets", skill: "Division Basics", time: "5 min" },
            { icon: "🍰", title: "Fractions Intro", prompt: "Halves (1/2), thirds (1/3), and quarters (1/4) of shapes", skill: "Fractions Basics", time: "5 min" },
            { icon: "⚖️", title: "Kilograms & Grams", prompt: "Converting kg to g, weighing groceries and balancing scales", skill: "Mass & Weight", time: "5 min" }
        ],
        "English": [
            { icon: "👤", title: "Pronouns", prompt: "Replacing repetitive nouns with he, she, it, they, we", skill: "Pronouns", time: "5 min" },
            { icon: "📍", title: "Prepositions of Place", prompt: "Position words: in, on, under, behind, in front of, between", skill: "Prepositions", time: "5 min" },
            { icon: "⚡", title: "Past Tense Verbs", prompt: "Regular past tense verbs (-ed) and irregular verbs (went, saw)", skill: "Past Tense", time: "5 min" },
            { icon: "💬", title: "Compound Words", prompt: "Joining words: rainbow, butterfly, jellyfish, sunflower", skill: "Word Building", time: "5 min" }
        ],
        "EVS": [
            { icon: "🌿", title: "Plant Parts & Leaves", prompt: "Roots, stem, leaves, flowers, leaf venation, photosynthesis", skill: "Plant Anatomy", time: "5 min" },
            { icon: "🐦", title: "Birds & Their Beaks", prompt: "Different types of beaks, claws, feathers, and nest building", skill: "Birds & Adaptations", time: "5 min" },
            { icon: "🚚", title: "Means of Transport", prompt: "Land, water, air travel, fuel used, and ancient vs modern vehicles", skill: "Transport & Travel", time: "5 min" },
            { icon: "💧", title: "Water Sources & Rain", prompt: "Rivers, wells, rainwater harvesting, filtration, and boiling", skill: "Water Resources", time: "5 min" }
        ],
        "Science": [
            { icon: "🫀", title: "Human Organ Systems", prompt: "Heart, lungs, stomach, brain, and how they keep us healthy", skill: "Human Organs", time: "5 min" },
            { icon: "🪨", title: "Solids, Liquids, Gases", prompt: "Three states of matter: ice, liquid water, steam properties", skill: "States of Matter", time: "5 min" },
            { icon: "🧲", title: "Fun with Magnets", prompt: "Attracting iron nails, North and South poles, magnetic toys", skill: "Magnetism Basics", time: "5 min" }
        ],
        "Social Science": [
            { icon: "🗺️", title: "Directions & Compass", prompt: "North, South, East, West, Sunrise direction, and map reading", skill: "Maps & Directions", time: "5 min" },
            { icon: "🏛️", title: "Our Heritage Monuments", prompt: "Taj Mahal, Red Fort, Qutub Minar, India Gate, and ancient temples", skill: "Indian Heritage", time: "5 min" }
        ]
    },
    "IV": {
        "Mathematics": [
            { icon: "🍕", title: "Fractions & Decimals", prompt: "Equivalent fractions, comparing fractions, and tenths/hundredths", skill: "Fractions & Decimals", time: "5 min" },
            { icon: "✖️", title: "Multi-Digit Multiplication", prompt: "Multiplying 2-digit by 2-digit numbers, mental math shortcuts", skill: "Multiplication Operations", time: "5 min" },
            { icon: "📐", title: "Perimeter & Area", prompt: "Measuring perimeter and area of rectangles and squares using grids", skill: "Perimeter & Area", time: "5 min" },
            { icon: "⏰", title: "Elapsed Time & 24h Clock", prompt: "Calculating start and end times, converting 12h to 24h railway time", skill: "Time Calculations", time: "5 min" },
            { icon: "📊", title: "Bar Charts & Pictographs", prompt: "Reading and drawing bar charts, interpreting tally marks and tables", skill: "Data & Graphing", time: "5 min" }
        ],
        "Science": [
            { icon: "⚡", title: "Electricity & Circuits", prompt: "Simple circuits, batteries, bulbs, switches, conductors and insulators", skill: "Electric Circuits", time: "5 min" },
            { icon: "🪐", title: "The Solar System", prompt: "8 planets in order, revolution, rotation, day/night, and Moon phases", skill: "Solar System & Space", time: "5 min" },
            { icon: "🧲", title: "Magnets & Poles", prompt: "Attraction, repulsion, magnetic field, and making an electromagnet", skill: "Magnetism", time: "5 min" },
            { icon: "💧", title: "The Water Cycle", prompt: "Evaporation, condensation, cloud formation, precipitation, and rain", skill: "Water Cycle & Weather", time: "5 min" },
            { icon: "🦷", title: "Teeth & Digestion", prompt: "Types of teeth (incisors, molars), plaque, and digestive organs", skill: "Human Digestion", time: "5 min" }
        ],
        "EVS": [
            { icon: "⚡", title: "Electricity at Home", prompt: "Safe use of electrical appliances, switches, and saving power", skill: "Energy in Daily Life", time: "5 min" },
            { icon: "💧", title: "Water Cycle & Clouds", prompt: "Evaporation, condensation, rain, and clean drinking water", skill: "Water Cycle", time: "5 min" },
            { icon: "🌳", title: "Forests & Wildlife", prompt: "Endangered animals, national parks, tiger conservation", skill: "Ecology & Wildlife", time: "5 min" },
            { icon: "🗑️", title: "Waste Management (3Rs)", prompt: "Reduce, Reuse, Recycle, biodegradable vs plastic waste", skill: "Environmental Care", time: "5 min" },
            { icon: "🌾", title: "From Seed to Plate", prompt: "Farming stages: ploughing, sowing, harvesting, and markets", skill: "Agriculture & Food", time: "5 min" }
        ],
        "English": [
            { icon: "🔤", title: "Adverbs of Manner (-ly)", prompt: "Identifying and using adverbs: swiftly, gracefully, loudly, carefully", skill: "Adverbs & Grammar", time: "5 min" },
            { icon: "🔗", title: "Conjunctions (Connectors)", prompt: "Joining sentences with and, but, because, although, or, so", skill: "Conjunctions", time: "5 min" },
            { icon: "📖", title: "Reading Comprehension", prompt: "Short passage inference, main idea, vocabulary in context, moral", skill: "Reading Comprehension", time: "10 min" },
            { icon: "🗣️", title: "Direct Speech & Quotes", prompt: "Using quotation marks, speaker dialogue, and punctuation", skill: "Punctuation & Dialogue", time: "5 min" }
        ],
        "Social Science": [
            { icon: "🗺️", title: "Physical Features of India", prompt: "Himalayas, Northern Plains, Thar Desert, Deccan Plateau, Coastal Plains", skill: "Geography of India", time: "5 min" },
            { icon: "🏛️", title: "Civic Life & Panchayat", prompt: "Gram Panchayat, Municipal Corporation, public services, and taxes", skill: "Civics & Governance", time: "5 min" }
        ]
    },
    "V": {
        "Mathematics": [
            { icon: "🔢", title: "Factors, Multiples & LCM/HCF", prompt: "Prime and composite numbers, divisibility tests, finding HCF and LCM", skill: "Factors & Multiples", time: "5 min" },
            { icon: "➗", title: "Decimals Operations", prompt: "Addition, subtraction, multiplication of decimals with money word problems", skill: "Decimals Operations", time: "5 min" },
            { icon: "📐", title: "Area & Volume of Shapes", prompt: "Area of rectangles and triangles, volume of cuboids in cubic cm", skill: "Area & Volume Mensuration", time: "10 min" },
            { icon: "📈", title: "Percentages & Fractions", prompt: "Converting fractions to percentages, discount and score percentage calculation", skill: "Percentages", time: "5 min" },
            { icon: "🧭", title: "Angles & Degrees", prompt: "Acute, right, obtuse, straight angles, measuring angles with protractor", skill: "Geometry & Angles", time: "5 min" }
        ],
        "Science": [
            { icon: "🌿", title: "Photosynthesis & Nutrition", prompt: "Chlorophyll, stomata, xylem, phloem, sunlight, and starch production", skill: "Plant Biology", time: "5 min" },
            { icon: "🦴", title: "Skeletal & Nervous System", prompt: "206 bones, ball-and-socket joint, spinal cord, sensory and motor nerves", skill: "Human Anatomy", time: "5 min" },
            { icon: "🦠", title: "Microbes & Food Preservation", prompt: "Bacteria, fungi, viruses, pasteurization, salting, canning, and pickling", skill: "Microbiology & Food", time: "5 min" },
            { icon: "🌪️", title: "Natural Disasters & Safety", prompt: "Earthquakes (Richter scale), tsunamis, cyclones, and disaster safety measures", skill: "Earth Science & Safety", time: "5 min" },
            { icon: "⚙️", title: "Simple Machines", prompt: "Six simple machines: lever (1st, 2nd, 3rd class), pulley, inclined plane", skill: "Physics & Mechanics", time: "5 min" }
        ],
        "English": [
            { icon: "✨", title: "Continuous & Perfect Tenses", prompt: "Present perfect (has/have seen) and past continuous (was running)", skill: "Advanced Verb Tenses", time: "5 min" },
            { icon: "🤝", title: "Subject-Verb Agreement", prompt: "Rules of singular/plural subject-verb pairing with tricky pronouns", skill: "Grammar & Syntax", time: "5 min" },
            { icon: "🎭", title: "Active & Passive Voice", prompt: "Converting active sentences to passive voice and identifying the agent", skill: "Active & Passive Voice", time: "5 min" },
            { icon: "📚", title: "Idioms & Metaphors", prompt: "Common idioms like 'piece of cake', 'break the ice', and similes/metaphors", skill: "Idioms & Figurative Language", time: "5 min" }
        ],
        "Social Science": [
            { icon: "🌍", title: "Continents & Latitudes", prompt: "7 continents, Equator, Prime Meridian, Tropics of Cancer and Capricorn", skill: "World Geography", time: "5 min" },
            { icon: "📜", title: "India's Freedom Movement", prompt: "Revolt of 1857, Non-Cooperation Movement, Dandi March, Independence 1947", skill: "Modern Indian History", time: "10 min" },
            { icon: "🗳️", title: "The United Nations", prompt: "UN aims, General Assembly, Security Council, UNESCO, UNICEF, and WHO", skill: "Global Organizations", time: "5 min" }
        ],
        "EVS": [
            { icon: "🔋", title: "Renewable Energy", prompt: "Solar panels, windmills, hydroelectric dams, and conserving fossil fuels", skill: "Clean Energy", time: "5 min" },
            { icon: "🌾", title: "Soil Layers & Conservation", prompt: "Topsoil, humus, subsoil, soil erosion, and terrace farming", skill: "Soil Science", time: "5 min" }
        ]
    },
    "VI": {
        "Mathematics": [
            { icon: "➕", title: "Integers & Number Line", prompt: "Negative integers, absolute values, adding and subtracting on number line", skill: "Integers", time: "5 min" },
            { icon: "🔣", title: "Intro to Algebra", prompt: "Variables, algebraic expressions, forming equations from word puzzles", skill: "Introductory Algebra", time: "5 min" },
            { icon: "⚖️", title: "Ratio & Proportions", prompt: "Simplifying ratios, checking proportion, unitary method in shopping", skill: "Ratio & Proportions", time: "5 min" },
            { icon: "📐", title: "Practical Geometry", prompt: "Drawing circles, line bisectors, perpendiculars, and angles with compass", skill: "Geometry & Constructions", time: "10 min" }
        ],
        "Science": [
            { icon: "🥗", title: "Nutrients & Deficiency Diseases", prompt: "Vitamins A, B, C, D, iron, iodine deficiencies (scurvy, rickets, goitre)", skill: "Food & Nutrition", time: "5 min" },
            { icon: "💡", title: "Light, Shadows & Reflections", prompt: "Pinhole camera, rectilinear propagation, transparent, translucent, opaque", skill: "Optics & Light", time: "5 min" },
            { icon: "🔌", title: "Electricity & Circuit Switches", prompt: "Components of electric cell, filament, open vs closed circuits, safety", skill: "Current Electricity", time: "5 min" },
            { icon: "🌱", title: "Plant Structure & Transpiration", prompt: "Taproots, fibrous roots, leaf venation, stomata and transpiration experiment", skill: "Botany & Plant Physiology", time: "5 min" }
        ],
        "English": [
            { icon: "📝", title: "Clauses & Complex Sentences", prompt: "Main clause, subordinate clause, relative pronouns (who, which, that)", skill: "Complex Sentence Structure", time: "5 min" },
            { icon: "💬", title: "Modal Auxiliaries", prompt: "Expressing permission, obligation, possibility (must, ought to, should, might)", skill: "Modal Verbs", time: "5 min" },
            { icon: "📖", title: "Critical Reading & Tone", prompt: "Identifying author perspective, factual vs opinion statements, summaries", skill: "Analytical Reading", time: "10 min" }
        ],
        "Social Science": [
            { icon: "🏛️", title: "Indus Valley Civilization", prompt: "Harappa, Mohenjo-Daro, Great Bath, town planning, granaries, and seals", skill: "Ancient History", time: "10 min" },
            { icon: "🗳️", title: "Democratic Government", prompt: "Universal adult franchise, equality, justice, resolving conflicts peacefully", skill: "Civics & Governance", time: "5 min" },
            { icon: "🪐", title: "Earth in the Solar System", prompt: "Asteroids, meteoroids, Earth's unique atmosphere, and Moon's surface", skill: "Physical Geography", time: "5 min" }
        ]
    },
    "VII": {
        "Mathematics": [
            { icon: "🔢", title: "Rational Numbers & Operations", prompt: "Arithmetic operations with positive and negative rational numbers", skill: "Rational Numbers", time: "10 min" },
            { icon: "📐", title: "Triangles & Pythagoras", prompt: "Angle sum property, exterior angle property, hypotenuse calculations", skill: "Triangles & Geometry", time: "10 min" },
            { icon: "⚡", title: "Exponents & Powers", prompt: "Laws of exponents: multiplying, dividing powers, standard scientific notation", skill: "Exponents & Algebra", time: "5 min" },
            { icon: "📊", title: "Mean, Median & Mode", prompt: "Calculating arithmetic mean, median, mode, and probability of outcomes", skill: "Statistics & Probability", time: "5 min" }
        ],
        "Science": [
            { icon: "🧪", title: "Acids, Bases & Salts", prompt: "Litmus, turmeric indicator, phenolphthalein, acid-base neutralisation salts", skill: "Chemistry: Acids & Bases", time: "5 min" },
            { icon: "🌡️", title: "Heat: Conduction & Convection", prompt: "Conduction in metals, convection currents in water/air, radiation from Sun", skill: "Thermal Physics", time: "5 min" },
            { icon: "⚡", title: "Electric Current & Magnets", prompt: "Electromagnets, electric bell mechanism, fuse wire safety and heating effect", skill: "Electromagnetism", time: "5 min" },
            { icon: "🫁", title: "Respiration in Organisms", prompt: "Aerobic vs anaerobic, human respiratory tract, breathing rate, diaphragm", skill: "Human Physiology", time: "5 min" }
        ],
        "English": [
            { icon: "🔄", title: "Reported Speech Mastery", prompt: "Direct to indirect speech rules for statements, questions, and commands", skill: "Indirect Speech", time: "5 min" },
            { icon: "✍️", title: "Formal Letters & Notices", prompt: "Format of letters to the editor/principal, notice writing with date and venue", skill: "Formal Writing", time: "10 min" }
        ],
        "Social Science": [
            { icon: "🏰", title: "The Mughal Empire", prompt: "Babur, Akbar's Din-i-Ilahi, Mansabdari system, architecture, and decline", skill: "Medieval Indian History", time: "10 min" },
            { icon: "🌍", title: "Atmosphere & Weather Systems", prompt: "Troposphere, stratosphere, air pressure belts, planetary winds, humidity", skill: "Atmospheric Geography", time: "5 min" }
        ]
    },
    "VIII": {
        "Mathematics": [
            { icon: "📐", title: "Linear Equations in 1 Variable", prompt: "Solving algebraic linear equations, cross-multiplication, and word problems", skill: "Linear Equations", time: "10 min" },
            { icon: "⬛", title: "Squares & Square Roots", prompt: "Finding square roots by prime factorisation and long division method", skill: "Squares & Square Roots", time: "10 min" },
            { icon: "📈", title: "Compound Interest & Profit/Loss", prompt: "Compounded annually vs half-yearly, calculating sales tax, GST, and profit %", skill: "Commercial Mathematics", time: "10 min" },
            { icon: "📦", title: "Mensuration: Cylinders & Prisms", prompt: "Total surface area, curved surface area, and volume of cylinders and cuboids", skill: "Mensuration 3D", time: "10 min" }
        ],
        "Science": [
            { icon: "⚡", title: "Force, Pressure & Friction", prompt: "Types of friction, atmospheric pressure, Pascal's principle, fluid resistance", skill: "Mechanics & Pressure", time: "5 min" },
            { icon: "🧬", title: "Cell Structure & Organelles", prompt: "Plant vs animal cell, cell wall, nucleus, mitochondria, chloroplasts", skill: "Cell Biology", time: "5 min" },
            { icon: "🦠", title: "Microorganisms: Friend & Foe", prompt: "Antibiotics, vaccines, nitrogen cycle, food poisoning, and fermentation", skill: "Microbiology", time: "5 min" },
            { icon: "🔥", title: "Combustion, Flame & Fuels", prompt: "Calorific value, zones of a candle flame, spontaneous and rapid combustion", skill: "Chemical Combustion", time: "5 min" },
            { icon: "🔭", title: "Stars, Constellations & Space", prompt: "Ursa Major, Orion, pole star, light years, artificial satellites and orbits", skill: "Astronomy & Space", time: "5 min" }
        ],
        "English": [
            { icon: "📚", title: "Conditional Clauses & Conjunctions", prompt: "First, second, third conditionals (If/Unless), complex coherence", skill: "Advanced Syntax", time: "5 min" },
            { icon: "✍️", title: "Argumentative Essays", prompt: "Writing structured argumentative essays with counter-arguments and evidence", skill: "Essay Writing", time: "10 min" }
        ],
        "Social Science": [
            { icon: "📜", title: "The Indian Constitution & Rights", prompt: "Fundamental Rights, Directive Principles, secularism, rule of law, judiciary", skill: "Civics & Constitution", time: "10 min" },
            { icon: "🌾", title: "Natural Resources & Agriculture", prompt: "Commercial farming, plantation agriculture, major food crops (rice, wheat), soil conservation", skill: "Economic Geography", time: "10 min" }
        ]
    }
};

function applyCurriculumIdea(idea) {
    if (!idea) return;

    // 1. Populate AI Prompt
    const promptEl = document.getElementById('aiTaskPrompt');
    if (promptEl) {
        promptEl.value = `${idea.title}: ${idea.prompt}`;
    }

    // 2. Populate Task Details above
    const titleEl = document.getElementById('newTaskTitle');
    if (titleEl) {
        titleEl.value = `${idea.icon || '🎯'} ${idea.title}`;
    }

    const skillEl = document.getElementById('newTaskSkillArea');
    if (skillEl && idea.skill) {
        skillEl.value = idea.skill;
    }

    if (idea.time) {
        const timeSelect = document.getElementById('newTaskTime');
        if (timeSelect) {
            for (let i = 0; i < timeSelect.options.length; i++) {
                if (timeSelect.options[i].value === idea.time) {
                    timeSelect.selectedIndex = i;
                    break;
                }
            }
        }
    }

    const descEl = document.getElementById('newTaskDesc');
    if (descEl && !descEl.value.trim()) {
        descEl.value = `Master ${idea.title} by reading carefully and solving all interactive challenges!`;
    }

    // 3. Highlight the active idea button
    const allBtns = document.querySelectorAll('.ai-tag-btn[data-idea-title]');
    allBtns.forEach(b => {
        if (b.dataset.ideaTitle === idea.title) {
            b.classList.add('active');
        } else {
            b.classList.remove('active');
        }
    });

    const statusEl = document.getElementById('aiGenerationStatus');
    if (statusEl) statusEl.style.display = 'none';

    showToastNotification(`💡 Loaded idea: "${idea.title}". Click "Generate with AI" below!`);
}

function updateAiIdeaTags(resetOffset = false) {
    if (resetOffset) currentAiIdeaOffset = 0;

    const cls = document.getElementById('newTaskClass')?.value || AppState.selectedClass || 'IV';
    const sub = document.getElementById('newTaskSubject')?.value || 'Science';
    const labelEl = document.getElementById('aiIdeasTagLabel');
    const container = document.getElementById('aiDynamicIdeaButtons');
    if (!container) return;

    if (labelEl) {
        labelEl.innerHTML = `💡 Ideas for <strong>Class ${escapeHtml(cls)} (${escapeHtml(sub)})</strong>:`;
    }

    const classMap = CurriculumIdeasMap[cls] || CurriculumIdeasMap['IV'];
    let subjectIdeas = classMap[sub] || [];

    // If selected subject has no direct list (e.g. EVS in Class VII), fall back intelligently
    if (subjectIdeas.length === 0) {
        if (sub === 'EVS' && classMap['Science']) {
            subjectIdeas = classMap['Science'];
        } else if (sub === 'Science' && classMap['EVS']) {
            subjectIdeas = classMap['EVS'];
        } else {
            subjectIdeas = Object.values(classMap).flat();
        }
    }

    if (subjectIdeas.length === 0) {
        container.innerHTML = '<span style="font-size:12px; color:#64748b;">No preset ideas found. Type a prompt above!</span>';
        return;
    }

    const pageSize = 5;
    const startIdx = (currentAiIdeaOffset * pageSize) % subjectIdeas.length;
    const visibleIdeas = [];
    for (let i = 0; i < pageSize && i < subjectIdeas.length; i++) {
        visibleIdeas.push(subjectIdeas[(startIdx + i) % subjectIdeas.length]);
    }

    container.innerHTML = '';
    visibleIdeas.forEach(idea => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'ai-tag-btn';
        btn.dataset.ideaTitle = idea.title;
        btn.innerHTML = `${idea.icon || '💡'} ${escapeHtml(idea.title)}`;
        btn.title = `${idea.title} - ${idea.prompt}`;
        btn.onclick = () => applyCurriculumIdea(idea);
        container.appendChild(btn);
    });
}

function shuffleAiIdeas() {
    currentAiIdeaOffset++;
    updateAiIdeaTags(false);
}

function filterAiIdeaTags(searchVal) {
    const cls = document.getElementById('newTaskClass')?.value || AppState.selectedClass || 'IV';
    const sub = document.getElementById('newTaskSubject')?.value || 'Science';
    const container = document.getElementById('aiDynamicIdeaButtons');
    if (!container) return;

    const q = (searchVal || '').toLowerCase().trim();
    const classMap = CurriculumIdeasMap[cls] || CurriculumIdeasMap['IV'];
    const allClassIdeas = Object.values(classMap).flat();

    const matches = allClassIdeas.filter(idea =>
        idea.title.toLowerCase().includes(q) ||
        idea.prompt.toLowerCase().includes(q) ||
        (idea.skill && idea.skill.toLowerCase().includes(q))
    );

    if (matches.length === 0) {
        updateAiIdeaTags(false);
        return;
    }

    container.innerHTML = '';
    matches.slice(0, 6).forEach(idea => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'ai-tag-btn';
        btn.dataset.ideaTitle = idea.title;
        btn.innerHTML = `${idea.icon || '💡'} ${escapeHtml(idea.title)}`;
        btn.title = `${idea.title} - ${idea.prompt}`;
        btn.onclick = () => applyCurriculumIdea(idea);
        container.appendChild(btn);
    });
}

function syncCurriculumDefaultsForClass(cls, preferredSubject = null) {
    const classMap = CurriculumIdeasMap[cls] || CurriculumIdeasMap['IV'];
    const subSelect = document.getElementById('newTaskSubject');

    let currentSub = preferredSubject || (subSelect ? subSelect.value : 'Mathematics');

    // Adjust subject for primary vs upper grades
    if ((cls === 'I' || cls === 'II') && (currentSub === 'Science' || currentSub === 'Social Science')) {
        currentSub = 'EVS';
    } else if ((cls === 'VI' || cls === 'VII' || cls === 'VIII') && currentSub === 'EVS') {
        currentSub = 'Science';
    }

    if (subSelect) {
        for (let i = 0; i < subSelect.options.length; i++) {
            if (subSelect.options[i].value.toLowerCase() === currentSub.toLowerCase()) {
                subSelect.selectedIndex = i;
                break;
            }
        }
    }

    // Get the ideas for this class and subject
    let subjectIdeas = classMap[currentSub] || [];
    if (subjectIdeas.length === 0) {
        if (currentSub === 'EVS' && classMap['Science']) subjectIdeas = classMap['Science'];
        else if (currentSub === 'Science' && classMap['EVS']) subjectIdeas = classMap['EVS'];
        else subjectIdeas = Object.values(classMap).flat();
    }

    const defaultIdea = subjectIdeas[0];
    if (defaultIdea) {
        // 1. Task Title based upon the class & subject
        const titleEl = document.getElementById('newTaskTitle');
        if (titleEl) {
            titleEl.value = `${defaultIdea.icon || '🎯'} ${defaultIdea.title}`;
        }

        // 2. Skill Area / Topic based upon the class & subject
        const skillEl = document.getElementById('newTaskSkillArea');
        if (skillEl) {
            skillEl.value = defaultIdea.skill || defaultIdea.title;
        }

        // 3. Estimated Time
        if (defaultIdea.time) {
            const timeSelect = document.getElementById('newTaskTime');
            if (timeSelect) {
                for (let i = 0; i < timeSelect.options.length; i++) {
                    if (timeSelect.options[i].value === defaultIdea.time) {
                        timeSelect.selectedIndex = i;
                        break;
                    }
                }
            }
        }

        // 4. Instructions
        const descEl = document.getElementById('newTaskDesc');
        if (descEl) {
            if (cls === 'I' || cls === 'II') {
                descEl.value = `Look at each picture and question carefully and pick the matching answer! ⭐`;
            } else if (cls === 'III' || cls === 'IV' || cls === 'V') {
                descEl.value = `Read each challenge carefully, think step-by-step, and pick the best answer!`;
            } else {
                descEl.value = `Analyze each question, apply core principles of ${currentSub}, and choose the correct option.`;
            }
        }

        // 5. AI Prompt Box
        const promptEl = document.getElementById('aiTaskPrompt');
        if (promptEl) {
            promptEl.value = `${defaultIdea.title}: ${defaultIdea.prompt}`;
        }
    }

    // 6. Refresh the dynamic ideas tags and highlight the first one
    updateAiIdeaTags(true);

    const firstBtn = document.querySelector('.ai-tag-btn[data-idea-title]');
    if (firstBtn) firstBtn.classList.add('active');

    const statusEl = document.getElementById('aiGenerationStatus');
    if (statusEl) statusEl.style.display = 'none';

    if (typeof updateSkillAreaPickerContext === 'function') {
        updateSkillAreaPickerContext();
    }
}

function openCreateTaskModal(focusAi = false) {
    const cls = AppState.selectedClass || 'IV';
    const clsSelect = document.getElementById('newTaskClass');
    if (clsSelect) clsSelect.value = cls;

    const currentSub = AppState.teacherSubjectFilter !== 'all' ? AppState.teacherSubjectFilter : (cls === 'I' || cls === 'II' ? 'Mathematics' : 'Science');

    document.getElementById('newTaskAssignNow').checked = true;
    toggleCreateTaskAssignList(true);

    renderCreateTaskStudentsList();

    // Default with 1 clean question block
    currentCreateTaskQuestions = [
        {
            prompt: '',
            options: ['', '', '', ''],
            answer: 0,
            explanation: ''
        }
    ];
    renderQuestionBlocks();

    // Sync Task Title, Subject, Skill Area, Time, and Prompt based upon the class itself!
    syncCurriculumDefaultsForClass(cls, currentSub);

    // Reset AI status & feedback
    const aiStatus = document.getElementById('aiGenerationStatus');
    if (aiStatus) {
        aiStatus.style.display = 'none';
        aiStatus.className = 'ai-status-strip';
        aiStatus.innerHTML = '';
    }

    // Reset Game Builder preview and inputs
    currentCreateTaskInteractiveConfig = null;
    currentCreateTaskGameType = 'auto';
    const previewCard = document.getElementById('aiBuiltGamePreviewCard');
    if (previewCard) previewCard.style.display = 'none';
    const gameTypeSelect = document.getElementById('newTaskGameType');
    if (gameTypeSelect) gameTypeSelect.value = 'auto';
    const condInput = document.getElementById('aiGameConditions');
    if (condInput) condInput.value = '';
    const infoInput = document.getElementById('aiGameInformation');
    if (infoInput) infoInput.value = '';

    document.getElementById('teacherCreateTaskModal').classList.add('active');

    if (focusAi) {
        setTimeout(() => {
            const promptEl = document.getElementById('aiTaskPrompt');
            if (promptEl) {
                promptEl.focus();
                promptEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }, 150);
    } else {
        setTimeout(() => {
            const titleEl = document.getElementById('newTaskTitle');
            if (titleEl) {
                titleEl.focus();
                titleEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }, 150);
    }
}

function setAiPrompt(promptText, subject) {
    const promptEl = document.getElementById('aiTaskPrompt');
    if (promptEl) {
        promptEl.value = promptText;
        promptEl.focus();
    }
    if (subject) {
        const subSelect = document.getElementById('newTaskSubject');
        if (subSelect) {
            for (let i = 0; i < subSelect.options.length; i++) {
                if (subSelect.options[i].value.toLowerCase() === subject.toLowerCase()) {
                    subSelect.selectedIndex = i;
                    break;
                }
            }
        }
    }
    const titleEl = document.getElementById('newTaskTitle');
    if (titleEl && !titleEl.value.trim()) {
        titleEl.value = promptText.split(':')[0].trim();
    }
    const statusEl = document.getElementById('aiGenerationStatus');
    if (statusEl) statusEl.style.display = 'none';
}

function showAiStatus(msg, type = 'info') {
    const statusEl = document.getElementById('aiGenerationStatus');
    if (!statusEl) return;
    statusEl.style.display = 'flex';
    statusEl.className = 'ai-status-strip ' + type;

    let iconHtml = 'ℹ️';
    if (type === 'loading') {
        iconHtml = '<span class="ai-spinner"></span>';
    } else if (type === 'success') {
        iconHtml = '✨';
    } else if (type === 'warning') {
        iconHtml = '⚠️';
    } else if (type === 'error') {
        iconHtml = '❌';
    }

    statusEl.innerHTML = `<span>${iconHtml}</span> <span>${escapeHtml(msg)}</span>`;
}

async function triggerAiTaskGeneration(forceRefresh = false, isGameBuilder = true) {
    const promptEl = document.getElementById('aiTaskPrompt');
    let prompt = (promptEl ? promptEl.value : '').trim();

    const cls = document.getElementById('newTaskClass')?.value || AppState.selectedClass || 'IV';
    const subject = document.getElementById('newTaskSubject')?.value || 'Science';
    const skillVal = document.getElementById('newTaskSkillArea')?.value?.trim();
    const numQuestions = parseInt(document.getElementById('aiNumQuestions')?.value || '3', 10);
    const difficulty = document.getElementById('aiDifficulty')?.value || 'Medium';

    const gameTypeSelect = document.getElementById('newTaskGameType');
    const gameType = gameTypeSelect ? gameTypeSelect.value : 'auto';

    const condInput = document.getElementById('aiGameConditions');
    const conditions = condInput ? condInput.value.trim() : '';

    const infoInput = document.getElementById('aiGameInformation');
    const information = infoInput ? infoInput.value.trim() : '';

    // If prompt is empty, use the Task Title, Skill Area, or Information
    if (!prompt) {
        const titleVal = document.getElementById('newTaskTitle')?.value?.trim();
        if (titleVal || skillVal) {
            prompt = [titleVal, skillVal].filter(Boolean).join(' - ');
            if (promptEl) promptEl.value = prompt;
        } else if (information) {
            prompt = information.split('\n')[0].substring(0, 50);
            if (promptEl) promptEl.value = prompt;
        }
    }

    if (!prompt) {
        showAiStatus('Please enter a Task Title above, or a topic prompt, or custom information below.', 'warning');
        const titleEl = document.getElementById('newTaskTitle');
        if (titleEl && !titleEl.value.trim()) {
            titleEl.focus();
        } else if (promptEl) {
            promptEl.focus();
        }
        return;
    }

    const btnGame = document.getElementById('btnBuildAiGame');
    const btnQuiz = document.getElementById('btnGenerateAiQuizOnly');
    const btnFresh = document.getElementById('btnGenerateAiFresh');
    const btnIcon = document.getElementById('aiBtnIcon');
    const btnText = document.getElementById('aiBtnText');
    const origGameText = btnText ? btnText.textContent : 'Build Small-Scale Game with AI';

    // Loading state
    if (btnGame) btnGame.disabled = true;
    if (btnQuiz) btnQuiz.disabled = true;
    if (btnFresh) btnFresh.disabled = true;
    if (btnIcon) btnIcon.innerHTML = '<span class="ai-spinner"></span>';
    if (btnText) btnText.textContent = isGameBuilder ? (forceRefresh ? 'Building Fresh Game...' : 'AI Agent Building Game...') : 'Designing Quiz...';

    const statusActionText = isGameBuilder
        ? `🤖 AI Game Developer Agent is architecting a tactile small-scale game for Class ${cls} ${subject} (${prompt})...`
        : `AI is checking question bank & designing ${numQuestions} ${difficulty.toLowerCase()} questions for Class ${cls} ${subject}...`;
    showAiStatus(statusActionText, 'loading');

    try {
        const response = await fetch('/api/ai/generate-task', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt: prompt,
                class: cls,
                subject: subject,
                topic: skillVal || prompt,
                game_type: gameType,
                conditions: conditions,
                information: information,
                num_questions: numQuestions,
                difficulty: difficulty,
                is_game_builder: isGameBuilder,
                force_refresh: forceRefresh
            })
        });

        const result = await response.json();

        if (!response.ok || (result.status !== 'success' && !result.success)) {
            throw new Error(result.message || result.error || 'Failed to generate task. Please try again.');
        }

        const task = result.task || (result.data ? result.data.task : null) || {};
        const questions = task.questions || (result.data ? result.data.questions : null) || [];

        populateCreateTaskForm(task, questions, subject);

        const isCached = result.cached || (result.provider && result.provider.includes('Question Bank Cache'));
        const providerName = result.provider || (result.data && result.data.source === 'gemini' ? 'Google Gemini AI' : 'AI Game Developer Agent');

        let statusMsg = '';
        if (task.interactiveConfig) {
            statusMsg = `🎮 AI Game Developer Agent built "${task.title || 'Game'}" with tactile ${task.gameType || 'Mini-Game'} engine & ${questions.length} questions via ${providerName}! Click "▶️ Test Play Game" below to try it!`;
        } else if (isCached) {
            statusMsg = `⚡ Served instantly from Question Bank Cache (0s)! "${task.title || 'Task'}" ready with ${questions.length} questions (${difficulty}).`;
        } else {
            statusMsg = `✨ Generated "${task.title || 'Task'}" with ${questions.length} questions (${difficulty}) via ${providerName}! Review and publish below.`;
        }

        showAiStatus(statusMsg, 'success');
        showToastNotification(`✨ AI Agent built "${task.title || 'Activity'}" successfully!`);

    } catch (err) {
        console.warn('Backend generation unreachable, attempting smart client-side curriculum fallback:', err);
        const clientTask = generateClientCurriculumTask(prompt, cls, subject, numQuestions, difficulty);
        if (clientTask) {
            populateCreateTaskForm(clientTask, clientTask.questions, subject);
            showAiStatus(`✨ Generated "${clientTask.title}" (${clientTask.questions.length} questions) via Built-in Curriculum Engine! Review and publish below.`, 'success');
            showToastNotification(`✨ Generated ${clientTask.questions.length} questions successfully!`);
        } else {
            showAiStatus(`⚠️ ${err.message || 'Generation failed. Please try again.'}`, 'error');
        }
    } finally {
        if (btnGame) btnGame.disabled = false;
        if (btnQuiz) btnQuiz.disabled = false;
        if (btnFresh) btnFresh.disabled = false;
        if (btnIcon) btnIcon.textContent = '🎮';
        if (btnText) btnText.textContent = origGameText;
    }
}

function populateCreateTaskForm(task, questions, subjectFallback = 'Science') {
    if (!task) return;

    // Save active interactive game configuration & type
    currentCreateTaskInteractiveConfig = task.interactiveConfig || null;
    currentCreateTaskGameType = task.gameType || (task.interactiveConfig ? 'Sort & Group' : 'MCQ Quiz');

    // 1. Populate Task Info
    const titleEl = document.getElementById('newTaskTitle');
    if (titleEl && task.title) {
        titleEl.value = task.title;
    }

    const detectedSubject = task.subject || subjectFallback;
    if (detectedSubject) {
        const subSelect = document.getElementById('newTaskSubject');
        if (subSelect) {
            for (let i = 0; i < subSelect.options.length; i++) {
                if (subSelect.options[i].value.toLowerCase() === detectedSubject.toLowerCase()) {
                    subSelect.selectedIndex = i;
                    break;
                }
            }
        }
    }

    const skill = task.skillArea || task.skill_area || task.topic;
    if (skill) {
        const skillEl = document.getElementById('newTaskSkillArea');
        if (skillEl) skillEl.value = skill;
    }

    // Sync Game Type Dropdown
    const gameTypeSelect = document.getElementById('newTaskGameType');
    if (gameTypeSelect) {
        const engine = (task.interactiveConfig && task.interactiveConfig.engine) ? task.interactiveConfig.engine : '';
        const gType = (task.gameType || '').toLowerCase();
        for (let i = 0; i < gameTypeSelect.options.length; i++) {
            const optVal = gameTypeSelect.options[i].value.toLowerCase();
            const optText = gameTypeSelect.options[i].text.toLowerCase();
            if (engine && (optVal === engine || optText.includes(engine))) {
                gameTypeSelect.selectedIndex = i;
                break;
            } else if (gType && (optVal.includes(gType) || optText.includes(gType))) {
                gameTypeSelect.selectedIndex = i;
                break;
            }
        }
    }

    const desc = task.desc || task.description;
    if (desc) {
        const descEl = document.getElementById('newTaskDesc');
        if (descEl) descEl.value = desc;
    }

    const timeVal = task.time || task.estimated_time;
    if (timeVal) {
        const timeSelect = document.getElementById('newTaskTime');
        if (timeSelect) {
            for (let i = 0; i < timeSelect.options.length; i++) {
                if (timeSelect.options[i].value.toLowerCase().includes(String(timeVal).toLowerCase())) {
                    timeSelect.selectedIndex = i;
                    break;
                }
            }
        }
    }

    // 2. Render Interactive Built Game Preview Card
    const previewCard = document.getElementById('aiBuiltGamePreviewCard');
    if (previewCard) {
        if (task.interactiveConfig) {
            previewCard.style.display = 'flex';
            const iconEl = document.getElementById('aiBuiltGameIcon');
            const titleEl = document.getElementById('aiBuiltGameTitle');
            const summaryEl = document.getElementById('aiBuiltGameSummary');
            const cfg = task.interactiveConfig;

            if (iconEl) iconEl.textContent = cfg.icon || '🎮';
            if (titleEl) titleEl.textContent = `🎮 Interactive ${task.gameType || 'Mini-Game'} Built: ${cfg.title || task.title}`;

            if (summaryEl) {
                let summary = `Tactile ${cfg.engine || 'interactive'} mini-game ready to test play!`;
                if (cfg.engine === 'bucket-sorter' && Array.isArray(cfg.buckets) && Array.isArray(cfg.items)) {
                    summary = `${cfg.buckets.length} Buckets (${cfg.buckets.map(b => b.label.replace(/⭐/g, '').trim()).join(', ')}) · ${cfg.items.length} cards to sort`;
                } else if (cfg.engine === 'pair-matcher' && Array.isArray(cfg.pairs)) {
                    summary = `${cfg.pairs.length} matching pairs challenge (connector arena)`;
                } else if (cfg.engine === 'word-train' && Array.isArray(cfg.rounds) && cfg.rounds[0]) {
                    summary = `${(cfg.rounds[0].words || []).length} sequential stages train challenge`;
                } else if (cfg.engine === 'word-scramble' && Array.isArray(cfg.rounds)) {
                    summary = `${cfg.rounds.length} vocabulary words letter arrange challenge`;
                } else if (cfg.engine === 'number-line-hopper') {
                    summary = 'Freddie Frog number line skip-counting challenge';
                } else if (cfg.engine === 'bubble-pop') {
                    summary = 'Fast-action target bubbles pop challenge';
                }
                summaryEl.textContent = summary;
            }
        } else {
            previewCard.style.display = 'none';
        }
    }

    // 3. Populate Questions
    const qList = questions || task.questions || [];
    if (Array.isArray(qList) && qList.length > 0) {
        currentCreateTaskQuestions = qList.map(q => ({
            prompt: q.prompt || q.question || '',
            options: (Array.isArray(q.options) && q.options.length >= 2)
                ? [q.options[0] || '', q.options[1] || '', q.options[2] || '', q.options[3] || '']
                : ['', '', '', ''],
            answer: (typeof q.answer === 'number' && q.answer >= 0 && q.answer < 4) ? q.answer : 0,
            explanation: q.explanation || '',
            visual_hint: q.visual_hint || '',
            svg_diagram: q.svg_diagram || ''
        }));
        renderQuestionBlocks();
    }

    // Smooth scroll to task details
    setTimeout(() => {
        const titleInput = document.getElementById('newTaskTitle');
        if (titleInput) {
            titleInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
            titleInput.focus();
        }
    }, 250);
}

function generateClientCurriculumTask(prompt, cls, subject, numQuestions, difficulty) {
    const p = (prompt || '').toLowerCase();
    let title = `${prompt} Explorer`;
    let skill = `${prompt} Concepts`;
    let detectedSubject = subject || 'Science';
    let desc = `Interactive learning quest on ${prompt} for Class ${cls}.`;
    let questions = [];

    if (p.includes('phonic') || p.includes('sound') || p.includes('rhym') || (cls === 'I' && subject === 'English')) {
        title = '🔤 Phonics & Letter Sounds Explorer';
        skill = 'Phonics & Sounds';
        detectedSubject = 'English';
        desc = 'Learn letter sounds, vowels, and rhyming words with fun picture challenges!';
        questions = [
            {
                prompt: 'Which letter makes the starting sound in the word "Apple"?',
                options: ['Letter A (Ah)', 'Letter B (Buh)', 'Letter C (Kuh)', 'Letter D (Duh)'],
                answer: 0,
                explanation: 'Apple starts with the short vowel "A" sound (/æ/).',
                visual_hint: '🍎 A is for Apple!'
            },
            {
                prompt: 'Which of the following words rhymes with "Cat"?',
                options: ['Hat', 'Dog', 'Sun', 'Cup'],
                answer: 0,
                explanation: 'Cat and Hat have the same ending sound (-at).',
                visual_hint: '🐱 Cat wearing a Hat!'
            },
            {
                prompt: 'Which of these letters is a vowel?',
                options: ['Letter E', 'Letter B', 'Letter T', 'Letter M'],
                answer: 0,
                explanation: 'The five English vowels are A, E, I, O, and U.',
                visual_hint: '⭐ Vowels are A, E, I, O, U!'
            },
            {
                prompt: 'What sound does the letter "S" make, like in "Sun"?',
                options: ['/s/ like a hissing snake', '/b/ like a bouncing ball', '/m/ like humming', '/p/ like popping'],
                answer: 0,
                explanation: 'The letter S makes the hissing /s/ sound as in Sun, Star, and Snake.',
                visual_hint: '☀️ S is for Sun!'
            },
            {
                prompt: 'Which word is the opposite of "Big"?',
                options: ['Small', 'Tall', 'Fast', 'Hot'],
                answer: 0,
                explanation: 'Small is the direct opposite of Big.',
                visual_hint: '🐘 Big elephant vs 🐭 Small mouse.'
            }
        ];
    } else if (p.includes('count') || p.includes('number') || (cls === 'I' && subject === 'Mathematics')) {
        title = '🔢 Fun with Numbers & Counting 1-20';
        skill = 'Counting & Number Sense';
        detectedSubject = 'Mathematics';
        desc = 'Count colorful objects, find missing numbers, and practice simple addition!';
        questions = [
            {
                prompt: 'How many fingers do we have on two hands together?',
                options: ['10 fingers', '5 fingers', '8 fingers', '12 fingers'],
                answer: 0,
                explanation: 'We have 5 fingers on each hand, making 5 + 5 = 10 fingers in total.',
                visual_hint: '🖐️ 5 on left + 🖐️ 5 on right = 10!'
            },
            {
                prompt: 'What number comes immediately after 6?',
                options: ['7', '5', '8', '9'],
                answer: 0,
                explanation: 'Counting forward: 1, 2, 3, 4, 5, 6, 7!',
                visual_hint: '🔢 6 comes before 7.'
            },
            {
                prompt: 'If you have 3 red balloons and get 2 more, how many balloons do you have in all?',
                options: ['5 balloons', '4 balloons', '6 balloons', '3 balloons'],
                answer: 0,
                explanation: '3 + 2 = 5 balloons.',
                visual_hint: '🎈 3 balloons + 🎈🎈 2 balloons = 5!'
            },
            {
                prompt: 'Which number is smaller: 4 or 9?',
                options: ['4 is smaller', '9 is smaller', 'Both are equal', 'Neither'],
                answer: 0,
                explanation: '4 comes before 9 on the number line, so 4 is smaller.',
                visual_hint: '📉 4 is fewer than 9.'
            },
            {
                prompt: 'Which shape has 3 straight sides and 3 corners?',
                options: ['Triangle', 'Circle', 'Square', 'Rectangle'],
                answer: 0,
                explanation: 'A triangle is a 3-sided shape with 3 corners.',
                visual_hint: '🔺 Triangle has 3 sides.'
            }
        ];
    } else if (p.includes('sense') || (cls === 'I' && subject === 'EVS')) {
        title = '👀 5 Senses & My Body Adventure';
        skill = 'Sense Organs & Hygiene';
        detectedSubject = 'EVS';
        desc = 'Discover the 5 senses and learn how to take care of our body!';
        questions = [
            {
                prompt: 'Which sense organ helps us see bright colors and read storybooks?',
                options: ['Our Eyes', 'Our Ears', 'Our Nose', 'Our Tongue'],
                answer: 0,
                explanation: 'Eyes provide the sense of sight so we can see the world around us.',
                visual_hint: '👀 Eyes help us see!'
            },
            {
                prompt: 'What should we do before eating food to keep away germs?',
                options: ['Wash hands with soap and water', 'Skip washing', 'Rub hands on clothes', 'Sleep first'],
                answer: 0,
                explanation: 'Washing hands with soap kills germs and prevents sickness.',
                visual_hint: '🧼 Clean hands protect against germs!'
            },
            {
                prompt: 'Which sense organ helps us listen to birds singing and music?',
                options: ['Our Ears', 'Our Nose', 'Our Tongue', 'Our Skin'],
                answer: 0,
                explanation: 'Ears provide the sense of hearing.',
                visual_hint: '👂 Ears help us hear!'
            }
        ];
    } else if (p.includes('electric') || p.includes('circuit') || p.includes('batter') || p.includes('switch')) {
        title = '⚡ Electricity & Circuit Quest';
        skill = 'Electricity & Circuits';
        detectedSubject = (cls === 'I' || cls === 'II' || cls === 'III' || cls === 'IV' || cls === 'V') ? 'EVS' : 'Science';
        desc = 'Explore how electric circuits, batteries, switches, and conductors power our daily devices!';
        questions = [
            {
                prompt: 'What do we call the complete, unbroken loop that electricity flows through?',
                options: ['A straight line', 'An electric circuit', 'A water pipe', 'A battery box'],
                answer: 1,
                explanation: 'An electric circuit is an unbroken conductive loop that allows electricity to flow and power devices.',
                visual_hint: '🔋 A circuit needs an unbroken loop from battery to bulb!'
            },
            {
                prompt: 'Which of the following materials is a good conductor of electricity?',
                options: ['Copper wire', 'Rubber band', 'Plastic ruler', 'Dry wood'],
                answer: 0,
                explanation: 'Copper is a metal with free electrons that easily conducts electrical current.',
                visual_hint: '🔌 Metals like copper conduct electricity, while rubber and plastics act as insulators.'
            },
            {
                prompt: 'What happens in a circuit when an electric switch is turned OFF?',
                options: ['The bulb glows brighter', 'The circuit opens and stops current', 'The battery recharges', 'More electricity flows'],
                answer: 1,
                explanation: 'Turning a switch OFF creates an air gap, opening the circuit and stopping the electric current.',
                visual_hint: '💡 A switch safely opens (stops) or closes (starts) the electric path.'
            },
            {
                prompt: 'Which component provides the electrical energy in a portable flashlight?',
                options: ['The glass lens', 'The dry cell battery', 'The plastic handle', 'The screw cap'],
                answer: 1,
                explanation: 'The dry cell battery converts chemical energy into electrical energy to light up the torch bulb.',
                visual_hint: '🔋 Batteries store chemical energy to produce electrical voltage.'
            },
            {
                prompt: 'Why must we never touch electric switches with wet hands?',
                options: ['Water breaks the plastic', 'Water conducts electricity and can shock', 'Water cools the switch', 'It drains the battery'],
                answer: 1,
                explanation: 'Normal water contains dissolved minerals making it a conductor, which can cause severe electric shocks.',
                visual_hint: '⚠️ Always keep hands completely dry before operating electrical appliances!'
            }
        ];
    } else if (p.includes('solar') || p.includes('planet') || p.includes('space') || p.includes('sun') || p.includes('orbit')) {
        title = '🪐 Solar System Cosmic Quest';
        skill = 'Planets & Solar System';
        detectedSubject = 'Science';
        desc = 'Embark on an astronomical journey exploring the Sun, Moon, Earth, and orbiting planets!';
        questions = [
            {
                prompt: 'Which celestial body sits at the very center of our Solar System?',
                options: ['The Moon', 'The Sun', 'Earth', 'Jupiter'],
                answer: 1,
                explanation: 'The Sun is the massive central star of our Solar System around which all planets orbit.',
                visual_hint: '☀️ The Sun provides the gravitational anchor and light for all planets.'
            },
            {
                prompt: 'Which planet in our Solar System is famously known as the "Red Planet"?',
                options: ['Venus', 'Mars', 'Jupiter', 'Mercury'],
                answer: 1,
                explanation: 'Mars appears red because of iron oxide (rust) present across its surface dust.',
                visual_hint: '🔴 Mars has a reddish appearance due to iron-rich rocks and soil.'
            },
            {
                prompt: 'How long does Earth take to make one complete revolution around the Sun?',
                options: ['24 hours', '30 days', '365 1/4 days (1 year)', '10 years'],
                answer: 2,
                explanation: 'One complete revolution of Earth around the Sun takes approximately 365.25 days (1 year).',
                visual_hint: '🌍 One year equals one full revolution around the Sun.'
            },
            {
                prompt: 'Which is the largest planet in our Solar System?',
                options: ['Saturn', 'Jupiter', 'Neptune', 'Earth'],
                answer: 1,
                explanation: 'Jupiter is the largest planet, over 1,300 times larger in volume than Earth.',
                visual_hint: '🪐 Jupiter is a massive gas giant with famous storm bands.'
            },
            {
                prompt: 'What causes the daily cycle of day and night on Earth?',
                options: ['The Sun moving up and down', 'Earth spinning on its own axis', 'The Moon blocking the Sun', 'Clouds passing by'],
                answer: 1,
                explanation: 'Earth rotates on its axis once every 24 hours, bringing parts into sunlight (day) and away (night).',
                visual_hint: '🔄 Earth spins once on its axis every 24 hours.'
            }
        ];
    } else if (p.includes('magnet') || p.includes('pole')) {
        title = '🧲 Magnetic Force Challenge';
        skill = 'Magnets & Magnetic Poles';
        detectedSubject = 'Science';
        desc = 'Investigate magnetic poles, attraction, repulsion, and magnetic materials!';
        questions = [
            {
                prompt: 'What happens when two North (N) poles of two magnets are brought close?',
                options: ['They stick firmly', 'They repel (push apart)', 'They melt', 'They lose charge'],
                answer: 1,
                explanation: 'Like poles (North-North or South-South) always repel each other.',
                visual_hint: '🧲 Like magnetic poles repel; opposite poles attract!'
            },
            {
                prompt: 'Which of the following materials is strongly attracted by a magnet?',
                options: ['Plastic straw', 'Iron nail', 'Wooden toothpick', 'Glass marble'],
                answer: 1,
                explanation: 'Iron is a ferromagnetic material that is strongly attracted to magnets.',
                visual_hint: '📎 Magnets attract iron, nickel, and steel.'
            },
            {
                prompt: 'Which direction does a freely suspended magnetic compass needle naturally align?',
                options: ['East-West', 'North-South', 'Random direction', 'Towards the Sun'],
                answer: 1,
                explanation: 'Earth behaves like a giant magnet, aligning magnetic compass needles along the North-South axis.',
                visual_hint: '🧭 Compass needles point along Earth’s magnetic North-South poles.'
            }
        ];
    } else if (p.includes('fraction') || p.includes('decimal') || p.includes('ratio')) {
        title = '🍕 Fraction & Division Mastery';
        skill = 'Fractions & Parts of a Whole';
        detectedSubject = 'Mathematics';
        desc = 'Understand halves, quarters, numerators, and denominators through fun real-world sharing!';
        questions = [
            {
                prompt: 'If a pizza is divided into 4 equal slices and you eat 1 slice, what fraction was eaten?',
                options: ['1/2', '1/4', '3/4', '4/1'],
                answer: 1,
                explanation: '1 slice out of 4 equal parts equals the fraction 1/4 (one quarter).',
                visual_hint: '🍕 1 slice out of 4 equal slices = 1/4 of the pizza.'
            },
            {
                prompt: 'What is 1/2 of 10 chocolates?',
                options: ['2 chocolates', '5 chocolates', '4 chocolates', '8 chocolates'],
                answer: 1,
                explanation: 'Half of 10 is 10 ÷ 2 = 5 chocolates.',
                visual_hint: '🍫 Dividing 10 into 2 equal halves gives 5 in each group.'
            },
            {
                prompt: 'In the fraction 3/5, what does the bottom number (5) represent?',
                options: ['The slices eaten', 'The total number of equal parts', 'The number of plates', 'The extra pieces'],
                answer: 1,
                explanation: 'The denominator (bottom number) always tells the total number of equal parts the whole was divided into.',
                visual_hint: '📊 Denominator = total parts; Numerator = parts selected.'
            },
            {
                prompt: 'Which of the following fractions is equivalent to 1/2?',
                options: ['2/4', '1/3', '3/5', '1/4'],
                answer: 0,
                explanation: '2/4 simplifies to 1/2 when dividing numerator and denominator by 2.',
                visual_hint: '🍰 2 fourths equals exactly 1 half.'
            }
        ];
    } else if (p.includes('plant') || p.includes('leaf') || p.includes('root') || p.includes('photosynth')) {
        title = '🌿 Plant Life & Photosynthesis';
        skill = 'Plant Parts & Functions';
        detectedSubject = 'Science';
        desc = 'Learn about roots, stems, leaves, flowers, and how green plants make food with sunlight!';
        questions = [
            {
                prompt: 'Which part of a plant absorbs water and minerals from the soil?',
                options: ['The flowers', 'The roots', 'The leaves', 'The fruit'],
                answer: 1,
                explanation: 'Roots anchor the plant and absorb essential water and dissolved minerals from the soil.',
                visual_hint: '🌱 Underground roots draw moisture and minerals upward.'
            },
            {
                prompt: 'What is the green pigment in plant leaves that captures sunlight called?',
                options: ['Chlorophyll', 'Oxygen', 'Stomata', 'Glucose'],
                answer: 0,
                explanation: 'Chlorophyll gives leaves their green colour and traps solar energy for photosynthesis.',
                visual_hint: '🍃 Chlorophyll absorbs sunlight to produce plant sugars.'
            },
            {
                prompt: 'What vital gas do plants release into the air during photosynthesis?',
                options: ['Carbon dioxide', 'Oxygen', 'Nitrogen', 'Methane'],
                answer: 1,
                explanation: 'During photosynthesis, plants take in carbon dioxide and release life-giving oxygen.',
                visual_hint: '💨 Green plants produce oxygen that humans and animals breathe.'
            }
        ];
    } else if (p.includes('water') && (p.includes('cycle') || p.includes('rain') || p.includes('evaporat'))) {
        title = '💧 Water Cycle Explorer';
        skill = 'Water Cycle & Weather';
        detectedSubject = 'EVS';
        desc = 'Trace how water evaporates into the sky, condenses into clouds, and falls as rainfall!';
        questions = [
            {
                prompt: 'What process turns liquid water into invisible water vapour when heated by the Sun?',
                options: ['Freezing', 'Evaporation', 'Precipitation', 'Condensation'],
                answer: 1,
                explanation: 'Evaporation happens when the Sun heats water in oceans and lakes, turning it into gas vapour.',
                visual_hint: '☀️ Sun warmth turns surface water into rising vapour (evaporation).'
            },
            {
                prompt: 'What are white floating clouds in the sky made of?',
                options: ['White smoke', 'Cotton wool', 'Billions of tiny water droplets', 'Dry air'],
                answer: 2,
                explanation: 'Clouds form when rising water vapour cools and condenses into billions of microscopic liquid droplets.',
                visual_hint: '☁️ Condensed water droplets cluster together to form clouds.'
            },
            {
                prompt: 'When water droplets in clouds become too heavy and fall to the ground, it is called:',
                options: ['Evaporation', 'Precipitation (Rain)', 'Filtration', 'Transpiration'],
                answer: 1,
                explanation: 'Precipitation occurs when cloud water droplets combine and fall as rain, hail, or snow.',
                visual_hint: '🌧️ Rain falling from heavy clouds is precipitation.'
            }
        ];
    } else if (p.includes('gramm') || p.includes('verb') || p.includes('noun') || p.includes('tense')) {
        title = '🔤 English Grammar Detective';
        skill = 'Grammar & Parts of Speech';
        detectedSubject = 'English';
        desc = 'Master action verbs, naming words, adjectives, and clear sentence structure!';
        questions = [
            {
                prompt: 'Which word in the sentence is an action verb: "The quick puppy jumped over the fence"?',
                options: ['Puppy', 'Jumped', 'Fence', 'Quick'],
                answer: 1,
                explanation: '"Jumped" expresses the physical action performed by the puppy.',
                visual_hint: '🏃 Verbs describe actions, states, or occurrences.'
            },
            {
                prompt: 'What is the simple past tense of the verb "go"?',
                options: ['Goed', 'Went', 'Going', 'Gone'],
                answer: 1,
                explanation: '"Go" is an irregular verb whose simple past form is "went".',
                visual_hint: '📅 Today I go; yesterday I went.'
            },
            {
                prompt: 'Which word is an adjective that describes a noun: "Aarav wore a bright red sweater"?',
                options: ['Aarav', 'Bright', 'Wore', 'Sweater'],
                answer: 1,
                explanation: '"Bright" (and "red") are adjectives describing the appearance of the sweater.',
                visual_hint: '🎨 Adjectives describe the quality, colour, or size of nouns.'
            }
        ];
    } else {
        questions = [
            {
                prompt: `Which of the following is the key concept in ${prompt}?`,
                options: ['Understanding core principles', 'Ignoring classroom rules', 'Memorizing without meaning', 'Guessing answers'],
                answer: 0,
                explanation: `Learning ${prompt} requires understanding the underlying core principles and applying them.`,
                visual_hint: `🎯 Focus on fundamental concepts in ${prompt}.`
            },
            {
                prompt: `Why is learning about ${prompt} important in our daily lives?`,
                options: ['It has no practical use', 'It helps us understand the world around us', 'It is only for tests', 'It replaces school'],
                answer: 1,
                explanation: `Studying ${prompt} equips students to solve real-world problems and understand how things work.`,
                visual_hint: `💡 Real-world applications make learning memorable.`
            },
            {
                prompt: `Which habit helps a student master ${prompt} most effectively?`,
                options: ['Practicing problems step-by-step', 'Skipping practice', 'Rushing through questions', 'Waiting until exams'],
                answer: 0,
                explanation: 'Consistent step-by-step practice builds deep conceptual mastery and confidence.',
                visual_hint: '📚 Regular practice leads to success.'
            }
        ];
    }

    return {
        title: title,
        subject: detectedSubject,
        class: cls,
        skillArea: skill,
        topic: skill,
        desc: desc,
        time: '5 min',
        questions: questions.slice(0, Math.min(numQuestions, questions.length))
    };
}

async function checkAiStatus() {
    try {
        const res = await fetch('/api/ai/status');
        if (!res.ok) return;
        const status = await res.json();
        const badge = document.getElementById('aiModelBadge');
        if (badge && status) {
            if (status.active_engine === 'gemini' && status.has_gemini_key) {
                badge.textContent = 'Google Gemini AI 🟢';
                badge.title = 'Live Google Gemini AI Connected';
            } else {
                badge.textContent = 'Smart AI Engine ⚡';
                badge.title = 'Built-in Curriculum AI Generator Active';
            }
        }
    } catch (e) { }
}

/* ====================================================
   SKILL AREA / TOPIC POPUP DROPDOWN LOGIC
   ==================================================== */
function getSkillIconForSubjectAndGame(subject, gameType) {
    const gt = (gameType || '').toLowerCase();
    if (gt.includes('sort')) return '🧺';
    if (gt.includes('sequence') || gt.includes('order')) return '🚂';
    if (gt.includes('match') || gt.includes('pair')) return '🔗';
    if (gt.includes('word') || gt.includes('scramble')) return '🧩';
    if (gt.includes('line') || gt.includes('hop')) return '🐸';
    if (gt.includes('bubble') || gt.includes('pop')) return '🫧';
    if (gt.includes('quiz') || gt.includes('mcq')) return '📝';

    const sub = (subject || '').toLowerCase();
    if (sub.includes('math')) return '🔢';
    if (sub.includes('sci')) return '🔬';
    if (sub.includes('eng')) return '📖';
    if (sub.includes('evs')) return '🌿';
    if (sub.includes('social')) return '🏛️';
    return '🎯';
}

function getGameTypeBadgeClass(gameType) {
    const gt = (gameType || '').toLowerCase();
    if (gt.includes('sort')) return 'badge-sort';
    if (gt.includes('sequence') || gt.includes('order')) return 'badge-sequence';
    if (gt.includes('match') || gt.includes('pair')) return 'badge-match';
    if (gt.includes('quiz') || gt.includes('mcq')) return 'badge-mcq';
    return 'badge-other';
}

function getAvailableSkillsForCategory(cls, subject) {
    const cClean = (cls || 'IV').replace(/^Class\s*/i, '').trim();
    const subName = (subject || 'Science').trim();
    const subNorm = subName.toLowerCase();

    const chapterTopics = [];
    const catalogSkills = [];
    const seenSkills = new Set();

    // 1. Curriculum Chapter Topics (from CurriculumIdeasMap)
    const classMap = (typeof CurriculumIdeasMap !== 'undefined') ? (CurriculumIdeasMap[cClean] || CurriculumIdeasMap['IV'] || {}) : {};
    let subjectIdeas = classMap[subName] || [];
    if (!subjectIdeas || subjectIdeas.length === 0) {
        for (const k of Object.keys(classMap)) {
            if (k.toLowerCase() === subNorm) {
                subjectIdeas = classMap[k];
                break;
            }
        }
    }

    if (subjectIdeas && subjectIdeas.length > 0) {
        subjectIdeas.forEach(idea => {
            const skillName = idea.skill || idea.title;
            if (!seenSkills.has(skillName.toLowerCase())) {
                seenSkills.add(skillName.toLowerCase());
                chapterTopics.push({
                    skill: skillName,
                    title: idea.title,
                    activity: idea.prompt,
                    icon: idea.icon || getSkillIconForSubjectAndGame(subName, ''),
                    gameType: 'auto',
                    time: idea.time || '5 min',
                    prompt: idea.prompt,
                    type: 'topic'
                });
            }
        });
    }

    // 2. Syllabus Skill Areas & Activities (from FULL_GAMES_CATALOG)
    const catalog = (typeof FULL_GAMES_CATALOG !== 'undefined') ? FULL_GAMES_CATALOG : (window.FULL_GAMES_CATALOG || []);
    const seenCatalog = new Set();

    catalog.forEach(item => {
        const itemClass = (item.class || '').replace(/^Class\s*/i, '').trim();
        const itemSub = (item.subject || '').trim().toLowerCase();

        if (itemClass === cClean && itemSub === subNorm) {
            const skillName = (item.skillArea || item.topic || item.title || '').trim().replace(/[\uFFFD\u2013\u2014]/g, '-');
            const activityName = (item.activity || item.topic || '').trim().replace(/[\uFFFD\u2013\u2014]/g, '-');
            const actTitle = (item.title || activityName).trim();
            const key = `${skillName}:::${activityName}`.toLowerCase();

            if (!seenCatalog.has(key)) {
                seenCatalog.add(key);
                catalogSkills.push({
                    skill: skillName,
                    title: actTitle,
                    activity: activityName,
                    gameType: item.gameType || 'MCQ Quiz',
                    icon: getSkillIconForSubjectAndGame(subName, item.gameType),
                    desc: item.desc || '',
                    type: 'competency'
                });
            }
        }
    });

    return {
        chapterTopics,
        catalogSkills,
        totalCount: chapterTopics.length + catalogSkills.length
    };
}

function updateSkillAreaPickerContext() {
    const clsSelect = document.getElementById('newTaskClass');
    const subSelect = document.getElementById('newTaskSubject');
    const cls = clsSelect ? clsSelect.value : (AppState.selectedClass || 'IV');
    const sub = subSelect ? subSelect.value : 'Science';

    const { chapterTopics, catalogSkills, totalCount } = getAvailableSkillsForCategory(cls, sub);

    const countBadge = document.getElementById('skillPickerCountBadge');
    if (countBadge) countBadge.textContent = `${totalCount}`;

    const categoryText = document.getElementById('skillPickerCategoryText');
    if (categoryText) categoryText.textContent = `${sub} • Class ${cls}`;

    const availCount = document.getElementById('skillPickerAvailableCount');
    if (availCount) availCount.textContent = `${totalCount} Skills Available`;

    const dropdown = document.getElementById('skillAreaPickerDropdown');
    if (dropdown && dropdown.style.display !== 'none') {
        const searchInput = document.getElementById('skillPickerSearchInput');
        renderSkillPickerList(searchInput ? searchInput.value : '');
    }
}

function openSkillAreaPicker(event) {
    if (event) {
        event.stopPropagation();
    }
    const dropdown = document.getElementById('skillAreaPickerDropdown');
    if (!dropdown) return;

    dropdown.style.display = 'flex';
    updateSkillAreaPickerContext();

    const searchInput = document.getElementById('skillPickerSearchInput');
    if (searchInput) {
        searchInput.value = '';
    }
    renderSkillPickerList('');

    setTimeout(() => {
        const activeItem = dropdown.querySelector('.skill-picker-item.active');
        if (activeItem) {
            activeItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }, 60);
}

function closeSkillAreaPicker() {
    const dropdown = document.getElementById('skillAreaPickerDropdown');
    if (dropdown) dropdown.style.display = 'none';
}

function toggleSkillAreaPicker(event) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    const dropdown = document.getElementById('skillAreaPickerDropdown');
    if (!dropdown) return;
    if (dropdown.style.display === 'none' || !dropdown.style.display) {
        openSkillAreaPicker();
    } else {
        closeSkillAreaPicker();
    }
}

function filterSkillAreaPicker(query) {
    renderSkillPickerList(query);
}

function renderSkillPickerList(filterText = '') {
    const listEl = document.getElementById('skillPickerList');
    if (!listEl) return;

    const clsSelect = document.getElementById('newTaskClass');
    const subSelect = document.getElementById('newTaskSubject');
    const cls = clsSelect ? clsSelect.value : (AppState.selectedClass || 'IV');
    const sub = subSelect ? subSelect.value : 'Science';

    const { chapterTopics, catalogSkills } = getAvailableSkillsForCategory(cls, sub);
    const currentSkillVal = (document.getElementById('newTaskSkillArea')?.value || '').trim().toLowerCase();
    const q = (filterText || '').trim().toLowerCase();

    const filterItem = (item) => {
        if (!q) return true;
        const matchSkill = (item.skill || '').toLowerCase().includes(q);
        const matchTitle = (item.title || '').toLowerCase().includes(q);
        const matchAct = (item.activity || '').toLowerCase().includes(q);
        const matchGt = (item.gameType || '').toLowerCase().includes(q);
        return matchSkill || matchTitle || matchAct || matchGt;
    };

    const filteredTopics = chapterTopics.filter(filterItem);
    const filteredCatalog = catalogSkills.filter(filterItem);

    if (filteredTopics.length === 0 && filteredCatalog.length === 0) {
        listEl.innerHTML = `
                    <div class="skill-picker-empty">
                        <div style="font-size: 20px; margin-bottom: 4px;">🔍</div>
                        <div>No skills match <strong>"${escapeHtml(filterText)}"</strong> for Class ${cls} ${sub}.</div>
                        ${filterText ? `
                            <button type="button" class="skill-picker-custom-btn" onclick="selectSkillFromPicker('${escapeHtml(filterText).replace(/'/g, "\\'")}', 'auto', '', '')">
                                <span>✍️</span> Use "${escapeHtml(filterText)}" as topic
                            </button>
                        ` : ''}
                    </div>
                `;
        return;
    }

    let html = '';

    // Section 1: Core Curriculum Topics
    if (filteredTopics.length > 0) {
        html += `
                    <div class="skill-picker-section-title">
                        <span>🎯 Chapter &amp; Curriculum Modules</span>
                        <span>${filteredTopics.length}</span>
                    </div>
                `;
        filteredTopics.forEach(item => {
            const isActive = currentSkillVal === item.skill.toLowerCase() || currentSkillVal === item.title.toLowerCase();
            const escapedSkill = escapeHtml(item.skill).replace(/'/g, "\\'");
            const escapedGt = escapeHtml(item.gameType || 'auto').replace(/'/g, "\\'");
            const escapedTitle = escapeHtml(item.title).replace(/'/g, "\\'");
            const escapedPrompt = escapeHtml(item.prompt || '').replace(/'/g, "\\'");

            html += `
                        <div class="skill-picker-item ${isActive ? 'active' : ''}"
                            onclick="selectSkillFromPicker('${escapedSkill}', '${escapedGt}', '${escapedTitle}', '${escapedPrompt}')"
                            title="${escapeHtml(item.skill)}: ${escapeHtml(item.activity)}">
                            <div class="skill-item-left">
                                <div class="skill-item-title-row">
                                    <span class="skill-item-icon">${item.icon || '🎯'}</span>
                                    <span class="skill-item-name">${highlightMatch(escapeHtml(item.skill), q)}</span>
                                </div>
                                <div class="skill-item-sub">${highlightMatch(escapeHtml(item.title + ' • ' + item.activity), q)}</div>
                            </div>
                            <span class="skill-item-badge badge-other">📖 Topic</span>
                            ${isActive ? '<span class="skill-item-check">✓</span>' : ''}
                        </div>
                    `;
        });
    }

    // Section 2: Syllabus Competencies & Interactive Activities
    if (filteredCatalog.length > 0) {
        html += `
                    <div class="skill-picker-section-title" style="margin-top: 8px;">
                        <span>⚡ Curriculum Competencies &amp; Activities</span>
                        <span>${filteredCatalog.length}</span>
                    </div>
                `;
        filteredCatalog.forEach(item => {
            const isActive = currentSkillVal === item.skill.toLowerCase() || currentSkillVal === item.title.toLowerCase();
            const badgeClass = getGameTypeBadgeClass(item.gameType);
            const escapedSkill = escapeHtml(item.skill).replace(/'/g, "\\'");
            const escapedGt = escapeHtml(item.gameType || 'mcq').replace(/'/g, "\\'");
            const escapedTitle = escapeHtml(item.title).replace(/'/g, "\\'");
            const escapedDesc = escapeHtml(item.desc || item.activity || '').replace(/'/g, "\\'");

            html += `
                        <div class="skill-picker-item ${isActive ? 'active' : ''}"
                            onclick="selectSkillFromPicker('${escapedSkill}', '${escapedGt}', '${escapedTitle}', '${escapedDesc}')"
                            title="${escapeHtml(item.skill)} - ${escapeHtml(item.activity)} (${escapeHtml(item.gameType)})">
                            <div class="skill-item-left">
                                <div class="skill-item-title-row">
                                    <span class="skill-item-icon">${item.icon || '⚡'}</span>
                                    <span class="skill-item-name">${highlightMatch(escapeHtml(item.skill), q)}</span>
                                </div>
                                <div class="skill-item-sub">${highlightMatch(escapeHtml(item.activity ? item.activity + ' • ' + item.title : item.title), q)}</div>
                            </div>
                            <span class="skill-item-badge ${badgeClass}">${item.gameType}</span>
                            ${isActive ? '<span class="skill-item-check">✓</span>' : ''}
                        </div>
                    `;
        });
    }

    listEl.innerHTML = html;
}

function highlightMatch(text, query) {
    if (!query) return text;
    const idx = text.toLowerCase().indexOf(query.toLowerCase());
    if (idx === -1) return text;
    const before = text.slice(0, idx);
    const match = text.slice(idx, idx + query.length);
    const after = text.slice(idx + query.length);
    return `${before}<mark style="background: #fef08a; padding: 0 2px; border-radius: 2px;">${match}</mark>${after}`;
}

function selectSkillFromPicker(skillName, gameType, title, promptHint) {
    const skillInput = document.getElementById('newTaskSkillArea');
    if (skillInput) {
        skillInput.value = skillName;
    }

    // Sync Game Type if provided
    if (gameType && gameType !== 'auto') {
        const gtSelect = document.getElementById('newTaskGameType');
        if (gtSelect) {
            const gtMap = {
                'sort & group': 'sort-and-group',
                'match pairs': 'match-pairs',
                'sequence order': 'sequence-order',
                'word scramble': 'word-scramble',
                'number line hopper': 'number-line-hopper',
                'bubble pop': 'bubble-pop',
                'mcq quiz': 'mcq',
                'mcq': 'mcq'
            };
            const mappedVal = gtMap[gameType.toLowerCase()];
            if (mappedVal) {
                gtSelect.value = mappedVal;
            }
        }
    }

    // Suggest title if empty or default
    if (title) {
        const titleEl = document.getElementById('newTaskTitle');
        if (titleEl && (!titleEl.value || titleEl.value.startsWith('🎯') || titleEl.value.startsWith('💡'))) {
            titleEl.value = `🎯 ${title}`;
        }
    }

    // Update AI Prompt with topic context if empty or default
    if (promptHint) {
        const promptEl = document.getElementById('aiTaskPrompt');
        if (promptEl) {
            promptEl.value = `${title || skillName}: ${promptHint}`;
        }
    }

    // Trigger AI idea tags update
    handleCreateTaskTopicInput(skillName);

    // Close popup
    closeSkillAreaPicker();
}

// Global dismiss on click outside
document.addEventListener('click', function (e) {
    const container = document.getElementById('skillPickerContainer');
    const dropdown = document.getElementById('skillAreaPickerDropdown');
    if (dropdown && dropdown.style.display !== 'none') {
        if (container && !container.contains(e.target)) {
            closeSkillAreaPicker();
        }
    }
});

// Global dismiss on Esc
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
        closeSkillAreaPicker();
    }
});

function closeCreateTaskModal() {
    closeSkillAreaPicker();
    document.getElementById('teacherCreateTaskModal').classList.remove('active');
}

function handleCreateTaskClassChange(cls) {
    renderCreateTaskStudentsList();
    syncCurriculumDefaultsForClass(cls);
}

function handleCreateTaskSubjectChange(sub) {
    const cls = document.getElementById('newTaskClass')?.value || AppState.selectedClass || 'IV';
    syncCurriculumDefaultsForClass(cls, sub);
}

function handleCreateTaskTopicInput(val) {
    if (!val || val.trim().length < 2) {
        updateAiIdeaTags(false);
    } else {
        filterAiIdeaTags(val);
    }
}

function renderCreateTaskStudentsList() {
    const cls = document.getElementById('newTaskClass').value;
    const container = document.getElementById('newTaskStudentsList');
    if (!container) return;
    container.innerHTML = '';

    const roster = StudentRosters[cls] || [];
    roster.forEach(s => {
        const label = document.createElement('label');
        label.className = 'student-check-row';
        label.innerHTML = `
                    <input type="checkbox" name="createTaskStudentCheck" value="${s.roll}" data-name="${s.name}" checked>
                    <span>${s.name} (Roll #${s.roll})</span>
                `;
        container.appendChild(label);
    });
}

function toggleCreateTaskSelectAll() {
    const boxes = document.querySelectorAll('input[name="createTaskStudentCheck"]');
    const anyUnchecked = Array.from(boxes).some(b => !b.checked);
    boxes.forEach(b => b.checked = anyUnchecked);
}

function toggleCreateTaskAssignList(checked) {
    const cont = document.getElementById('createTaskStudentsContainer');
    const btn = document.getElementById('newTaskToggleAllBtn');
    if (cont) cont.style.display = checked ? 'block' : 'none';
    if (btn) btn.style.display = checked ? 'inline-block' : 'none';
}

function renderQuestionBlocks() {
    const container = document.getElementById('createTaskQuestionsList');
    const badge = document.getElementById('questionCountBadge');
    if (!container) return;
    container.innerHTML = '';
    if (badge) badge.textContent = currentCreateTaskQuestions.length;

    currentCreateTaskQuestions.forEach((q, qIdx) => {
        const block = document.createElement('div');
        block.className = 'q-block';
        block.innerHTML = `
                    <div class="q-header">
                        <span class="q-num-badge">Question ${qIdx + 1}</span>
                        ${currentCreateTaskQuestions.length > 1 ? `
                            <button type="button" class="btn-remove-q" onclick="removeQuestionBlock(${qIdx})">✕ Remove</button>
                        ` : ''}
                    </div>
                    ${q.visual_hint ? `
                        <div style="font-size: 12px; color: #4338ca; background: #eef2ff; border-radius: 8px; padding: 5px 10px; margin-bottom: 8px; font-weight: 600; display: inline-flex; align-items: center; gap: 6px;">
                            <span>💡 Clue:</span> ${escapeHtml(cleanVisualHint(q.visual_hint))}
                        </div>
                    ` : ''}
                    ${q.svg_diagram ? `
                        <div style="max-height: 80px; overflow: hidden; margin-bottom: 8px; border-radius: 10px; border: 1.5px dashed #cbd5e1; padding: 4px; display: flex; justify-content: center; background: #f8fafc;">
                            ${q.svg_diagram}
                        </div>
                    ` : ''}
                    <div style="margin-bottom: 10px;">
                        <input type="text" class="assign-input q-prompt-input" data-qidx="${qIdx}" placeholder="Enter question prompt..." value="${escapeHtml(q.prompt)}">
                    </div>
                    <div style="font-size: 11.5px; font-weight: 700; color: #475569; margin-bottom: 6px;">
                        Options (select the radio button for the correct choice):
                    </div>
                    <div class="q-options-grid">
                        ${[0, 1, 2, 3].map(optIdx => `
                            <div class="q-opt-wrap ${q.answer === optIdx ? 'correct' : ''}">
                                <input type="radio" name="q_correct_${qIdx}" value="${optIdx}" ${q.answer === optIdx ? 'checked' : ''} onchange="setQuestionCorrectAnswer(${qIdx}, ${optIdx})">
                                <input type="text" class="assign-input q-opt-input" style="padding: 6px 10px; font-size: 12.5px;" data-qidx="${qIdx}" data-optidx="${optIdx}" placeholder="Option ${String.fromCharCode(65 + optIdx)}" value="${escapeHtml(q.options[optIdx] || '')}">
                            </div>
                        `).join('')}
                    </div>
                    <div style="margin-top: 8px;">
                        <input type="text" class="assign-input q-exp-input" style="padding: 6px 10px; font-size: 12px; background: #f8fafc;" data-qidx="${qIdx}" placeholder="Explanation/Hint for student after answering (optional)..." value="${escapeHtml(q.explanation || '')}">
                    </div>
                `;
        container.appendChild(block);
    });

    container.querySelectorAll('.q-prompt-input').forEach(inp => {
        inp.addEventListener('input', (e) => {
            const idx = parseInt(e.target.dataset.qidx, 10);
            if (currentCreateTaskQuestions[idx]) currentCreateTaskQuestions[idx].prompt = e.target.value;
        });
    });
    container.querySelectorAll('.q-opt-input').forEach(inp => {
        inp.addEventListener('input', (e) => {
            const qIdx = parseInt(e.target.dataset.qidx, 10);
            const optIdx = parseInt(e.target.dataset.optidx, 10);
            if (currentCreateTaskQuestions[qIdx]) {
                if (!currentCreateTaskQuestions[qIdx].options) currentCreateTaskQuestions[qIdx].options = [];
                currentCreateTaskQuestions[qIdx].options[optIdx] = e.target.value;
            }
        });
    });
    container.querySelectorAll('.q-exp-input').forEach(inp => {
        inp.addEventListener('input', (e) => {
            const idx = parseInt(e.target.dataset.qidx, 10);
            if (currentCreateTaskQuestions[idx]) currentCreateTaskQuestions[idx].explanation = e.target.value;
        });
    });
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function addNewQuestionBlock() {
    currentCreateTaskQuestions.push({
        prompt: '',
        options: ['', '', '', ''],
        answer: 0,
        explanation: ''
    });
    renderQuestionBlocks();
}

function removeQuestionBlock(idx) {
    if (currentCreateTaskQuestions.length <= 1) return;
    currentCreateTaskQuestions.splice(idx, 1);
    renderQuestionBlocks();
}

function setQuestionCorrectAnswer(qIdx, optIdx) {
    if (currentCreateTaskQuestions[qIdx]) {
        currentCreateTaskQuestions[qIdx].answer = optIdx;
        renderQuestionBlocks();
    }
}

function fillSampleQuestion() {
    const sub = document.getElementById('newTaskSubject').value;
    const cls = document.getElementById('newTaskClass').value;

    let sampleTitle = `Class ${cls} ${sub} Review Challenge`;
    let samplePrompt = "What is the primary source of energy for Planet Earth?";
    let sampleOpts = ["The Sun", "The Moon", "The Wind", "Ocean Tides"];
    let sampleAns = 0;
    let sampleExp = "The Sun radiates light and heat, powering photosynthesis and weather on Earth.";
    let sampleSkill = "Solar Energy & Earth";

    if (sub === 'Mathematics') {
        sampleTitle = `Class ${cls} Multiplication & Mental Math`;
        samplePrompt = "What is 12 multiplied by 8?";
        sampleOpts = ["86", "92", "96", "104"];
        sampleAns = 2;
        sampleExp = "12 × 8 = 96.";
        sampleSkill = "Multiplication & Operations";
    } else if (sub === 'English') {
        sampleTitle = `Class ${cls} Vocabulary & Grammar Sprint`;
        samplePrompt = "Which word is an antonym (opposite) of 'Ancient'?";
        sampleOpts = ["Old", "Historic", "Modern", "Dusty"];
        sampleAns = 2;
        sampleExp = "'Modern' refers to present times, opposite of 'ancient'.";
        sampleSkill = "Vocabulary & Antonyms";
    }

    document.getElementById('newTaskTitle').value = sampleTitle;
    document.getElementById('newTaskSkillArea').value = sampleSkill;
    document.getElementById('newTaskDesc').value = `Solve each challenge carefully to earn 3 stars!`;

    currentCreateTaskQuestions = [
        {
            prompt: samplePrompt,
            options: sampleOpts,
            answer: sampleAns,
            explanation: sampleExp
        }
    ];
    renderQuestionBlocks();
    showToastNotification("🎲 Filled with sample questions!");
}

function submitCreateTask() {
    const title = document.getElementById('newTaskTitle').value.trim();
    if (!title) {
        alert('Please enter a Task Title.');
        document.getElementById('newTaskTitle').focus();
        return;
    }

    const cls = document.getElementById('newTaskClass').value;
    const subject = document.getElementById('newTaskSubject').value;
    const skillArea = document.getElementById('newTaskSkillArea').value.trim() || 'General Curriculum';
    const timeEst = document.getElementById('newTaskTime').value;
    const desc = document.getElementById('newTaskDesc').value.trim() || `Teacher created activity for Class ${cls} ${subject}.`;

    const validQuestions = [];
    for (let i = 0; i < currentCreateTaskQuestions.length; i++) {
        const q = currentCreateTaskQuestions[i];
        const prompt = (q.prompt || '').trim();
        const opts = (q.options || []).map(o => String(o || '').trim()).filter(Boolean);

        if (!prompt && opts.length === 0) continue;

        if (!prompt) {
            alert(`Question ${i + 1} is missing a prompt.`);
            return;
        }
        if (opts.length < 2) {
            alert(`Question ${i + 1} needs at least 2 options.`);
            return;
        }

        const finalOpts = [q.options[0] || 'Option A', q.options[1] || 'Option B', q.options[2] || 'Option C', q.options[3] || 'Option D'];
        const ans = (typeof q.answer === 'number' && q.answer >= 0 && q.answer < finalOpts.length) ? q.answer : 0;
        const exp = (q.explanation || '').trim() || `Correct answer: ${finalOpts[ans]}`;

        validQuestions.push({
            prompt: prompt,
            options: finalOpts,
            answer: ans,
            explanation: exp,
            visual_hint: q.visual_hint || '',
            svg_diagram: q.svg_diagram || ''
        });
    }

    if (validQuestions.length === 0) {
        if (currentCreateTaskInteractiveConfig) {
            validQuestions.push({
                prompt: `Great work completing the ${title} mini-game! What did you explore in this challenge?`,
                options: [skillArea, "Unrelated trivia", "Random guessing", "Extra score"],
                answer: 0,
                explanation: `This mini-game was designed to reinforce key concepts in ${skillArea}!`,
                visual_hint: 'Mini-Game Synthesis Check',
                svg_diagram: ''
            });
        } else {
            alert('Please add at least 1 question to this task or build an interactive mini-game with AI.');
            return;
        }
    }

    let thumb = 'images/game_english.jpg';
    let badgeClass = 'badge-eng';
    if (subject === 'Mathematics') {
        thumb = 'images/game_math.jpg';
        badgeClass = 'badge-math';
    } else if (subject === 'EVS' || subject === 'Science' || subject === 'Social Science') {
        thumb = 'images/game_science.jpg';
        badgeClass = 'badge-evs';
    }

    const chosenGameType = (currentCreateTaskGameType && currentCreateTaskGameType !== 'auto')
        ? currentCreateTaskGameType
        : (document.getElementById('newTaskGameType')?.value || (currentCreateTaskInteractiveConfig ? 'Sort & Group' : 'MCQ Quiz'));
    const finalGameType = chosenGameType === 'auto'
        ? (currentCreateTaskInteractiveConfig?.engine === 'bucket-sorter' ? 'Sort & Group' :
            currentCreateTaskInteractiveConfig?.engine === 'pair-matcher' ? 'Match Pairs' :
                currentCreateTaskInteractiveConfig?.engine === 'word-train' ? 'Sequence Order' :
                    currentCreateTaskInteractiveConfig?.engine === 'word-scramble' ? 'Word Scramble' :
                        currentCreateTaskInteractiveConfig?.engine === 'number-line-hopper' ? 'Math Hop' :
                            currentCreateTaskInteractiveConfig?.engine === 'bubble-pop' ? 'Fast Tapper' : 'Sort & Group')
        : chosenGameType;

    const conditionsVal = document.getElementById('aiGameConditions')?.value?.trim() || '';
    const informationVal = document.getElementById('aiGameInformation')?.value?.trim() || '';

    const taskId = 'CUSTOM-' + Date.now();
    const newTask = {
        id: taskId,
        title: title,
        class: cls,
        subject: subject,
        skillArea: skillArea,
        activity: finalGameType,
        gameType: finalGameType,
        interactiveConfig: currentCreateTaskInteractiveConfig || null,
        conditions: conditionsVal,
        information: informationVal,
        thumb: thumb,
        badgeClass: badgeClass,
        desc: desc,
        time: timeEst,
        stars: '3 stars',
        topic: skillArea,
        isCustom: true,
        createdDate: new Date().toISOString(),
        questions: validQuestions
    };

    let customTasks = loadCustomTasks();
    customTasks.unshift(newTask);
    saveCustomTasks(customTasks);

    GamesCatalog.unshift(newTask);

    const assignNow = document.getElementById('newTaskAssignNow').checked;
    let assignedCount = 0;
    if (assignNow) {
        const checkedBoxes = document.querySelectorAll('input[name="createTaskStudentCheck"]:checked');
        checkedBoxes.forEach(cb => {
            const roll = parseInt(cb.value, 10);
            const name = cb.dataset.name;
            const alreadyAssigned = AppState.assignments.some(a =>
                a.class === cls && a.gameId === taskId && a.student === name
            );
            if (!alreadyAssigned) {
                AppState.assignments.push({
                    class: cls,
                    subject: subject,
                    gameId: taskId,
                    gameTitle: title,
                    student: name,
                    roll: roll,
                    status: 'pending',
                    assignedDate: new Date().toISOString(),
                    score: null
                });
                assignedCount++;
            }
        });
        saveAssignments();
    }

    AppState.selectedClass = cls;

    updateSkillAreaOptions();
    updateKidStats();
    renderGamesGrid();
    renderTeacherHub();
    if (typeof renderSplitViews === 'function') renderSplitViews();

    closeCreateTaskModal();
    const assignMsg = assignedCount > 0 ? ` and assigned to ${assignedCount} students!` : '!';
    showToastNotification(`🎉 Custom task "${title}" created${assignMsg}`);
}

function openDeleteTaskModal() {
    renderDeleteTasksModalList();
    const modal = document.getElementById('teacherDeleteTaskModal');
    if (modal) modal.classList.add('active');
}

function closeDeleteTaskModal() {
    const modal = document.getElementById('teacherDeleteTaskModal');
    if (modal) modal.classList.remove('active');
}

function renderDeleteTasksModalList() {
    const container = document.getElementById('deleteTasksModalList');
    if (!container) return;

    // Get all custom tasks from catalog and storage
    const customTasks = GamesCatalog.filter(g => g.isCustom);

    if (customTasks.length === 0) {
        container.innerHTML = `
                    <div style="text-align: center; padding: 42px 16px; background: #f8fafc; border: 1.5px dashed #cbd5e1; border-radius: 16px;">
                        <div style="font-size: 40px; margin-bottom: 8px;">📋</div>
                        <h4 style="font-family: var(--font-heading); font-size: 17px; color: #1e1b4b; margin-bottom: 6px;">No custom tasks found</h4>
                        <p style="color: var(--text-muted); font-size: 13.5px; margin: 0 0 16px;">You haven't created any custom tasks yet.</p>
                        <button type="button" class="btn-create-task-modal" style="margin: 0 auto;" onclick="closeDeleteTaskModal(); openCreateTaskModal();">
                            <span>✨</span> Create New Activity
                        </button>
                    </div>
                `;
        return;
    }

    container.innerHTML = customTasks.map(t => {
        const qCount = (t.questions || []).length;
        const cls = t.class || 'All';
        const sub = t.subject || 'General';
        const skill = t.skillArea || 'Custom Skill';
        const escapedTitle = (t.title || 'Untitled Task').replace(/'/g, "\\'");

        return `
                    <div style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 14px; padding: 14px 16px; display: flex; align-items: center; justify-content: space-between; gap: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
                        <div style="display: flex; flex-direction: column; gap: 4px; flex: 1; min-width: 0;">
                            <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
                                <span style="font-family: var(--font-heading); font-size: 11px; font-weight: 700; background: #f1f5f9; color: #475569; padding: 2px 8px; border-radius: 6px;">Class ${cls}</span>
                                <span class="tac-badge tac-badge-subject ${t.badgeClass || ''}" style="font-size: 10.5px; padding: 2px 8px;">${sub}</span>
                                <span class="tac-badge tac-badge-skill" style="font-size: 10.5px; padding: 2px 8px;">🎯 ${skill}</span>
                                <span style="font-size: 11px; color: #64748b; font-weight: 600;">• ${qCount} question${qCount === 1 ? '' : 's'}</span>
                            </div>
                            <h4 style="font-family: var(--font-heading); font-size: 15.5px; font-weight: 700; color: #0f172a; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${t.title}">
                                ${t.title}
                            </h4>
                        </div>
                        <button type="button" class="btn-delete-tasks-top" style="padding: 7px 14px; font-size: 12px; flex: none;" onclick="executeDeleteCustomTask('${t.id}', '${escapedTitle}')">
                            <span>🗑️</span> Delete
                        </button>
                    </div>
                `;
    }).join('');
}

function executeDeleteCustomTask(taskId, taskTitle) {
    // Delete from GamesCatalog
    const catIdx = GamesCatalog.findIndex(g => g.id === taskId);
    if (catIdx !== -1) {
        GamesCatalog.splice(catIdx, 1);
    }

    // Delete from localStorage
    let customTasks = loadCustomTasks();
    customTasks = customTasks.filter(t => t.id !== taskId);
    saveCustomTasks(customTasks);

    // Clean up related assignments
    AppState.assignments = AppState.assignments.filter(a => a.gameId !== taskId);
    saveAssignments();

    // Refresh app state
    updateSkillAreaOptions();
    updateKidStats();
    renderGamesGrid();
    renderTeacherHub();
    if (typeof renderSplitViews === 'function') renderSplitViews();

    // Refresh delete modal list
    renderDeleteTasksModalList();

    showToastNotification(`🗑️ Custom task "${taskTitle}" deleted.`);
}

// Backward compatibility alias
function deleteCustomTask(taskId) {
    const task = GamesCatalog.find(g => g.id === taskId);
    const title = task ? task.title : 'this task';
    executeDeleteCustomTask(taskId, title);
}

