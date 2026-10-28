import json
import re

with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

# Dictionary of all Sequence Order and Context-needing activities
enrichment_map = {
    "I-ENG-08": {
        "instructions": [
            "Hold your pencil gently between your thumb and index finger.",
            "Place the pencil tip at the starting green dot on the worksheet.",
            "Follow the dotted line slowly and steadily from left to right.",
            "Keep your hand steady and do not lift the pencil off the paper.",
            "Stop smoothly when you reach the red finish star."
        ],
        "story": "Welcome to Trace the Pattern Path! Hold your pencil gently, place it on the starting green dot, follow the line smoothly, and stop at the finish star.",
        "audio_script": "Welcome to Trace the Pattern Path! Hold your pencil gently, place it on the starting green dot, follow the line smoothly, and stop at the finish star."
    },
    "I-MAT-06": {
        "instructions": [
            "Look at the shapes on the train wagons: Circle, Square, Circle, Square.",
            "Say the pattern aloud to discover the repetition rule.",
            "Predict which shape must come next to continue the pattern.",
            "Select the matching shape wagon to complete the sequence.",
            "Check that the pattern repeats smoothly from front to back."
        ],
        "story": "The Pattern Train is ready to roll! Look at the repeating shapes on the wagons: Circle, Square, Circle, Square. Which shape comes next?",
        "audio_script": "The Pattern Train is ready to roll! Look at the repeating shapes on the wagons: Circle, Square, Circle, Square. Which shape comes next?"
    },
    "II-ENG-06": {
        "instructions": [
            "Start at the top margin of your four-line handwriting guide.",
            "Draw three straight vertical strokes down to the base line.",
            "Draw two gentle upward curves like rolling ocean waves.",
            "Connect the straight strokes and curves to form neat letters.",
            "Leave a clear finger space before starting the next word."
        ],
        "story": "Time for Line and Curve Fun! Start at the top line, draw your straight strokes, curve gracefully at the base, and keep even spacing.",
        "audio_script": "Time for Line and Curve Fun! Start at the top line, draw your straight strokes, curve gracefully at the base, and keep even spacing."
    },
    "III-MAT-11": {
        "instructions": [
            "Start on the number line at zero.",
            "Count forward by hops of 5: 0, 5, 10, 15, 20.",
            "Identify the missing number in the skip counting sequence.",
            "Confirm that every jump has exactly the same distance.",
            "Land on the target star to complete the number path."
        ],
        "story": "Hop along the number line with Skip Counting Hop! Jump forward by equal steps of five: 5, 10, 15, 20! Find the missing number in the jump.",
        "audio_script": "Hop along the number line with Skip Counting Hop! Jump forward by equal steps of five: 5, 10, 15, 20! Find the missing number in the jump."
    },
    "III-EVS-08": {
        "instructions": [
            "Step 1 - Long ago: Students studied on slates using chalk and read under oil lamps.",
            "Step 2 - Years later: Schools introduced printed paper notebooks and wooden benches.",
            "Step 3 - Growing up: Classrooms featured large blackboards and library book collections.",
            "Step 4 - Recent years: Classrooms adopted digital smartboards and computer lessons.",
            "Step 5 - Today: Modern students learn with interactive digital tablets and e-learning portals."
        ],
        "story": "Explore the Then & Now Timeline! Long ago, students wrote on slates under oil lamps. Later came paper notebooks and wooden desks, followed by blackboards, smartboards, and now modern tablets.",
        "audio_script": "Explore the Then & Now Timeline! Long ago, students wrote on slates under oil lamps. Later came paper notebooks and wooden desks, followed by blackboards, smartboards, and now modern tablets."
    },
    "III-EVS-10": {
        "instructions": [
            "Step 1: Check the morning sky for bright sun, scattered clouds, or grey overcast.",
            "Step 2: Measure outdoor temperature in the shade using a thermometer.",
            "Step 3: Observe wind direction and strength using a paper windsock.",
            "Step 4: Record your weather observations in your weekly weather diary.",
            "Step 5: Predict afternoon rainfall based on cloud thickness and wind changes."
        ],
        "story": "Become a Weather Tracker Predictor! Check the morning sky, check the thermometer in the shade, watch the wind direction, record your findings, and predict the afternoon weather.",
        "audio_script": "Become a Weather Tracker Predictor! Check the morning sky, check the thermometer in the shade, watch the wind direction, record your findings, and predict the afternoon weather."
    },
    "IV-MAT-13": {
        "instructions": [
            "Step 1: Write down the consecutive numbers in the pattern row.",
            "Step 2: Calculate the difference between consecutive numbers by subtraction.",
            "Step 3: Verify whether the difference is constant (+4, +8) or multiplying (*2).",
            "Step 4: Apply the pattern rule to determine the missing mystery number.",
            "Step 5: Verify the sequence by testing the next subsequent number."
        ],
        "story": "Number Pattern Finder challenge! Look at the sequence of numbers, find the difference between them, discover the hidden rule, and find the next number.",
        "audio_script": "Number Pattern Finder challenge! Look at the sequence of numbers, find the difference between them, discover the hidden rule, and find the next number."
    },
    "IV-MAT-14": {
        "instructions": [
            "Step 1: Observe the repeating geometric sequence: Triangle, Diamond, Hexagon.",
            "Step 2: Check for orientation changes, such as rotation by 90 degrees.",
            "Step 3: Identify the core repeating block of shapes in the parade.",
            "Step 4: Select the shape that matches the next position in the sequence.",
            "Step 5: Check that both color and geometric orientation match the rule."
        ],
        "story": "Welcome to the Shape Pattern Parade! Watch the geometric figures marching by: Triangle, Diamond, Hexagon. Follow the rhythm and pick the shape that comes next.",
        "audio_script": "Welcome to the Shape Pattern Parade! Watch the geometric figures marching by: Triangle, Diamond, Hexagon. Follow the rhythm and pick the shape that comes next."
    },
    "IV-EVS-08": {
        "instructions": [
            "Step 1 - Past: Drawing fresh drinking water from community wells using buckets and ropes.",
            "Step 2 - Past: Installing cast-iron community hand pumps in neighborhood squares.",
            "Step 3 - Present: Piped treated municipal tap water delivered straight to kitchen sinks.",
            "Step 4 - Present: Installing multi-stage RO and UV purifiers inside homes.",
            "Step 5 - Future: Smart rainwater harvesting systems and automated solar water pumps."
        ],
        "story": "Changing Times Sorter reveals how water access evolved over generations: from well buckets to hand pumps, municipal piped water, modern filters, and solar rainwater harvesting.",
        "audio_script": "Changing Times Sorter reveals how water access evolved over generations: from well buckets to hand pumps, municipal piped water, modern filters, and solar rainwater harvesting."
    },
    "IV-EVS-10": {
        "instructions": [
            "Step 1: Select a tree shadow or flagpole to observe daily.",
            "Step 2: Measure the shadow's length every day at exactly 12:00 noon.",
            "Step 3: Record the date, time, and exact measurement in your observation diary.",
            "Step 4: Plot the recorded lengths on a grid chart to reveal patterns.",
            "Step 5: Use seasonal sun angles to predict next month's shadow length."
        ],
        "story": "In Pattern Diary, record how shadows change. Measure the shadow at solar noon every day, log your data in a table, and see how the Earth's orbit shifts shadow lengths.",
        "audio_script": "In Pattern Diary, record how shadows change. Measure the shadow at solar noon every day, log your data in a table, and see how the Earth's orbit shifts shadow lengths."
    },
    "V-MAT-11": {
        "instructions": [
            "Step 1: Examine the input and output pairs in the number table.",
            "Step 2: Test multiplication: check if multiplying input by a factor gives the output.",
            "Step 3: Check for addition or subtraction adjustments to find the complete rule.",
            "Step 4: Formulate the mathematical equation relating input x to output y.",
            "Step 5: Calculate the mystery output for the target number using your rule."
        ],
        "story": "Can you crack the code in What's the Rule? Look at the input numbers and their outputs. Find the multiplying and adding rule to find the missing answer.",
        "audio_script": "Can you crack the code in What's the Rule? Look at the input numbers and their outputs. Find the multiplying and adding rule to find the missing answer."
    },
    "V-EVS-03": {
        "instructions": [
            "Step 1 - Sun & Producers: Green plants absorb sunlight to produce food via photosynthesis.",
            "Step 2 - Primary Consumer: Grasshoppers and caterpillars feed directly on plant leaves.",
            "Step 3 - Secondary Consumer: Frogs and small insect-eating birds consume the herbivores.",
            "Step 4 - Tertiary Consumer: Snakes and hawks hunt smaller animals in the ecosystem.",
            "Step 5 - Decomposers: Fungi and bacteria break down organic matter, enriching soil nutrients."
        ],
        "story": "Food Chain Builder: Follow energy flow in nature! Sunlight fuels the green plants, grasshoppers eat the plants, frogs eat the grasshoppers, snakes eat the frogs, and fungi recycle nutrients.",
        "audio_script": "Food Chain Builder: Follow energy flow in nature! Sunlight fuels the green plants, grasshoppers eat the plants, frogs eat the grasshoppers, snakes eat the frogs, and fungi recycle nutrients."
    },
    "V-EVS-07": {
        "instructions": [
            "Stage 1: Traditional bullock carts, pack horses, and wooden sailboats.",
            "Stage 2: Advent of steam engines, coal railways, and postal mail routes.",
            "Stage 3: Motor cars, propeller planes, and nationwide telegraph wires.",
            "Stage 4: Jet passenger aircraft, interstate highways, and landline telephones.",
            "Stage 5: High-speed electric bullet trains, satellites, and mobile fiber networks."
        ],
        "story": "Past to Present Journey traces the evolution of transport and communication: from bullock carts and sailboats to steam locomotives, motorcars, jet airliners, and high-speed electric trains.",
        "audio_script": "Past to Present Journey traces the evolution of transport and communication: from bullock carts and sailboats to steam locomotives, motorcars, jet airliners, and high-speed electric trains."
    },
    "V-EVS-09": {
        "instructions": [
            "Step 1: Measure atmospheric pressure using a laboratory barometer.",
            "Step 2: Record temperature, humidity, and wind speed over three consecutive mornings.",
            "Step 3: Analyze barometric trends: dropping pressure signals incoming storm clouds.",
            "Step 4: Check regional satellite weather maps for approaching rain systems.",
            "Step 5: Formulate the 24-hour weather forecast based on recorded data trends."
        ],
        "story": "Predict the Next Day: Track the weather like a meteorologist! Check atmospheric pressure, temperature, humidity, and wind trends to forecast tomorrow's weather.",
        "audio_script": "Predict the Next Day: Track the weather like a meteorologist! Check atmospheric pressure, temperature, humidity, and wind trends to forecast tomorrow's weather."
    },
    "VI-SCI-04": {
        "instructions": [
            "Step 1: State the scientific question and formulate a testable hypothesis.",
            "Step 2: Assemble equipment: test tubes, stand, measuring cylinder, and timer.",
            "Step 3: Conduct the controlled experiment and observe visible changes carefully.",
            "Step 4: Record measurements immediately in an organized observation table.",
            "Step 5: Repeat the trial three times, calculate averages, and draw conclusions."
        ],
        "story": "Welcome to Experiment Steps Order. In any scientific investigation, first state your hypothesis, assemble the apparatus, conduct the trial, record data in a table, and repeat to ensure accuracy.",
        "audio_script": "Welcome to Experiment Steps Order. In any scientific investigation, first state your hypothesis, assemble the apparatus, conduct the trial, record data in a table, and repeat to ensure accuracy."
    },
    "VI-SCI-06": {
        "instructions": [
            "Step 1 - Evaporation: Solar heat warms water in oceans and lakes, turning it into invisible vapor.",
            "Step 2 - Transpiration: Trees and plants release water vapor into the air through leaf stomata.",
            "Step 3 - Condensation: Rising water vapor cools at high altitude, forming tiny cloud droplets.",
            "Step 4 - Precipitation: Droplets combine until heavy enough to fall as rain, sleet, or snow.",
            "Step 5 - Collection & Runoff: Water collects in streams and rivers, flowing back to oceans."
        ],
        "story": "Process Order Puzzle: The Great Water Cycle! Solar heat drives evaporation and transpiration. Rising vapor condenses into clouds, precipitates as rain, and returns to the sea.",
        "audio_script": "Process Order Puzzle: The Great Water Cycle! Solar heat drives evaporation and transpiration. Rising vapor condenses into clouds, precipitates as rain, and returns to the sea."
    },
    "VI-SCI-09": {
        "instructions": [
            "Step 1: Identify the scientific principle to demonstrate with your model.",
            "Step 2: Create a scaled blueprint with labeled dimensions and required materials.",
            "Step 3: Cut and assemble recyclable materials safely according to the blueprint.",
            "Step 4: Test the model's function and check structural stability.",
            "Step 5: Calibrate moving parts and prepare an explanation of its working principle."
        ],
        "story": "Build-a-Model Plan: An engineer's step-by-step guide. Identify the scientific concept, draft a blueprint, build the prototype carefully, test its function, and refine the design.",
        "audio_script": "Build-a-Model Plan: An engineer's step-by-step guide. Identify the scientific concept, draft a blueprint, build the prototype carefully, test its function, and refine the design."
    },
    "VI-SOC-04": {
        "instructions": [
            "Era 1 (c. 2600 BCE): Harappan Civilization thrives with brick cities, drainage, and trade.",
            "Era 2 (c. 1500 BCE): Early Vedic Period marked by the composition of the Rigveda hymns.",
            "Era 3 (c. 600 BCE): Rise of the 16 Mahajanapadas and teachings of Gautama Buddha and Mahavira.",
            "Era 4 (c. 321 - 185 BCE): Mauryan Empire unites India under Chandragupta and Emperor Ashoka.",
            "Era 5 (c. 320 - 550 CE): Gupta Dynasty Golden Age brings classical science, astronomy, and art."
        ],
        "story": "Ancient India Timeline Run takes you across the ages: from the Indus Valley cities to the Vedic Age, Mahajanapadas, the great Mauryan Empire, and the Gupta Golden Age.",
        "audio_script": "Ancient India Timeline Run takes you across the ages: from the Indus Valley cities to the Vedic Age, Mahajanapadas, the great Mauryan Empire, and the Gupta Golden Age."
    },
    "VII-MAT-10": {
        "instructions": [
            "Step 1: Draw a straight base line segment AB using a sharp pencil and ruler.",
            "Step 2: Set compass to required radius, place needle on A, and swing a wide arc above AB.",
            "Step 3: Without altering radius, place compass needle on B and cut the first arc at point C.",
            "Step 4: Use ruler to draw straight line segments from A to C and B to C.",
            "Step 5: Verify the triangle's side lengths and angle measures with a protractor."
        ],
        "story": "Construction Steps Builder: To construct a triangle, first draw base AB with a ruler. Swing an arc from A, cut it with an arc from B to find vertex C, and connect with straight lines.",
        "audio_script": "Construction Steps Builder: To construct a triangle, first draw base AB with a ruler. Swing an arc from A, cut it with an arc from B to find vertex C, and connect with straight lines."
    },
    "VII-SCI-04": {
        "instructions": [
            "Step 1: Choose the single independent variable you want to investigate.",
            "Step 2: Identify and fix all control variables: same container, same soil, same water volume.",
            "Step 3: Set up identical test groups and change only the independent variable in the test group.",
            "Step 4: Measure the dependent variable accurately at regular time intervals.",
            "Step 5: Compare results against the untreated control group to draw valid conclusions."
        ],
        "story": "Fair Test Detective: In a fair test, you change only ONE variable at a time while keeping every other factor constant. Measure accurately and compare with your control group.",
        "audio_script": "Fair Test Detective: In a fair test, you change only ONE variable at a time while keeping every other factor constant. Measure accurately and compare with your control group."
    },
    "VII-SCI-06": {
        "instructions": [
            "Stage 1 - Evaporation: Solar heat converts liquid water in oceans and soils into water vapor.",
            "Stage 2 - Transpiration: Forest vegetation releases water vapor into the air through stomata.",
            "Stage 3 - Condensation: Ascending vapor cools and condenses around dust particles, forming clouds.",
            "Stage 4 - Precipitation: Cloud droplets grow heavy and fall back to Earth as rain or snow.",
            "Stage 5 - Infiltration & Runoff: Water seeps into groundwater aquifers and streams return to the sea."
        ],
        "story": "Water Cycle Story: Solar radiation evaporates surface water. Transpiration adds moisture. Rising air cools into clouds, precipitation brings rain, and runoff cycles water back.",
        "audio_script": "Water Cycle Story: Solar radiation evaporates surface water. Transpiration adds moisture. Rising air cools into clouds, precipitation brings rain, and runoff cycles water back."
    },
    "VII-SCI-11": {
        "instructions": [
            "Step 1: Choose the scientific organ or system to model (e.g. human lung mechanism).",
            "Step 2: Fit a Y-shaped glass tube into a bell jar using an airtight rubber stopper.",
            "Step 3: Secure two rubber balloons to the branching arms of the Y-tube inside the jar.",
            "Step 4: Stretch a flexible rubber sheet across the open bottom of the jar to act as the diaphragm.",
            "Step 5: Pull the rubber diaphragm downwards to observe balloons inflate with atmospheric air."
        ],
        "story": "Model Maker Blueprint: Learn how the lung model works! A Y-tube holds two balloon lungs inside a bell jar. Pulling down the bottom rubber diaphragm inflates the balloons instantly.",
        "audio_script": "Model Maker Blueprint: Learn how the lung model works! A Y-tube holds two balloon lungs inside a bell jar. Pulling down the bottom rubber diaphragm inflates the balloons instantly."
    },
    "VII-SOC-01": {
        "instructions": [
            "Layer 1 - Crust: The outermost solid rock shell (5 to 70 km thick) beneath continents and oceans.",
            "Layer 2 - Lithosphere: Rigid upper mantle and crust divided into dynamic tectonic plates.",
            "Layer 3 - Mantle: Dense semi-solid silicate rock extending 2900 km deep with slow convection currents.",
            "Layer 4 - Outer Core: Liquid iron and nickel layer (2200 km thick) generating Earth's magnetic field.",
            "Layer 5 - Inner Core: Extremely dense solid iron-nickel sphere at Earth's center under massive pressure."
        ],
        "story": "Earth Layers Explorer takes you deep beneath our feet: from the continental crust, down through the mantle, across the liquid outer core, to the blazing solid inner core.",
        "audio_script": "Earth Layers Explorer takes you deep beneath our feet: from the continental crust, down through the mantle, across the liquid outer core, to the blazing solid inner core."
    },
    "VII-SOC-07": {
        "instructions": [
            "Era 1 (9th - 13th c.): The Chola Empire commands South India with naval expeditions and temple architecture.",
            "Era 2 (1206 - 1526 CE): The Delhi Sultanate unites northern trade and builds monuments in Delhi.",
            "Era 3 (1336 - 1646 CE): The Vijayanagara Empire prospers in the Deccan with grand capital at Hampi.",
            "Era 4 (1526 CE): Babur defeats Ibrahim Lodi at the First Battle of Panipat to found the Mughal Empire.",
            "Era 5 (1556 - 1605 CE): Akbar expands and stabilizes the empire through administrative and cultural synthesis."
        ],
        "story": "Medieval Dynasties Timeline journeys through India's medieval history: the Chola naval supremacy, Delhi Sultanate, grand Vijayanagara at Hampi, and the Mughal Golden Age under Akbar.",
        "audio_script": "Medieval Dynasties Timeline journeys through India's medieval history: the Chola naval supremacy, Delhi Sultanate, grand Vijayanagara at Hampi, and the Mughal Golden Age under Akbar."
    },
    "VIII-MAT-10": {
        "instructions": [
            "Step 1: Draw the given angle ABC with straight edges meeting at vertex B.",
            "Step 2: Place compass point at B and draw an arc cutting arms BA and BC at points P and Q.",
            "Step 3: From point P, draw an arc in the interior of the angle with radius greater than half PQ.",
            "Step 4: With the same radius, draw an intersecting arc from point Q, meeting at point R.",
            "Step 5: Draw a straight ray from vertex B through point R to bisect the angle into two equal halves."
        ],
        "story": "Compass and Ruler Order Game: To bisect an angle, swing an arc across both arms from vertex B. Then draw intersecting arcs from those points, and draw ray BR straight through the intersection.",
        "audio_script": "Compass and Ruler Order Game: To bisect an angle, swing an arc across both arms from vertex B. Then draw intersecting arcs from those points, and draw ray BR straight through the intersection."
    },
    "VIII-SCI-03": {
        "instructions": [
            "Step 1: State the hypothesis and research question with clear cause and effect.",
            "Step 2: Choose one single independent variable to test across your experimental groups.",
            "Step 3: Maintain all control variables strictly identical: temperature, volume, lighting, and time.",
            "Step 4: Measure the dependent variable using calibrated, sensitive lab instruments.",
            "Step 5: Compare data against the control trial to determine statistical significance."
        ],
        "story": "Variable Controller: Master scientific inquiry! Formulate a clear hypothesis, manipulate one single variable, control all other conditions, and measure your dependent variable with precision.",
        "audio_script": "Variable Controller: Master scientific inquiry! Formulate a clear hypothesis, manipulate one single variable, control all other conditions, and measure your dependent variable with precision."
    },
    "VIII-SCI-05": {
        "instructions": [
            "Step 1: Observe the phenomenon: shiny iron nails exposed to moist air develop brown flaky rust.",
            "Step 2: Identify chemical reactants: Iron atoms (Fe) react with dissolved oxygen (O₂) and water (H₂O).",
            "Step 3: Explain reaction mechanism: Slow oxidation reaction produces hydrated iron(III) oxide.",
            "Step 4: Test protective barriers: Apply oil, paint, or zinc galvanization to block oxygen contact.",
            "Step 5: Formulate scientific conclusion: Corrosion requires both oxygen and water simultaneously."
        ],
        "story": "Phenomena Explainer: Why does iron rust? Iron metal reacts with oxygen and water in the air to produce hydrated iron oxide. Coating iron with paint or zinc halts the reaction.",
        "audio_script": "Phenomena Explainer: Why does iron rust? Iron metal reacts with oxygen and water in the air to produce hydrated iron oxide. Coating iron with paint or zinc halts the reaction."
    },
    "VIII-SCI-08": {
        "instructions": [
            "Step 1: Clean a glass slide and coverslip thoroughly with soft lens paper.",
            "Step 2: Place a single drop of distilled water or dilute safranin stain in the center of the slide.",
            "Step 3: Use forceps to peel a transparent layer of onion epidermis and spread it flat in the drop.",
            "Step 4: Touch coverslip edge at 45 degrees and lower gently with a needle to avoid trapping air bubbles.",
            "Step 5: Blot excess liquid from coverslip edges with filter paper before mounting on the stage."
        ],
        "story": "Slide Prep Step Order: Prepare a temporary microscope slide! Clean the slide, add a stain drop, place the thin peel, lower the coverslip gently with a needle to avoid bubbles, and blot excess liquid.",
        "audio_script": "Slide Prep Step Order: Prepare a temporary microscope slide! Clean the slide, add a stain drop, place the thin peel, lower the coverslip gently with a needle to avoid bubbles, and blot excess liquid."
    },
    "VIII-SCI-10": {
        "instructions": [
            "Step 1: Identify structural challenge: Construct an earthquake-resistant model building.",
            "Step 2: Design blueprint with cross-bracing diagonals and a broad, low-center-of-gravity base.",
            "Step 3: Fabricate building frames using flexible joints to absorb seismic shear forces.",
            "Step 4: Place the model on an oscillation shake table and test against horizontal tremors.",
            "Step 5: Reinforce weak junction nodes to ensure maximum stability under vibration."
        ],
        "story": "Model Engineer Challenge: Design an earthquake-resistant tower! Draft a blueprint with triangular cross-bracing, assemble flexible shock-absorbing joints, and shake-test for structural integrity.",
        "audio_script": "Model Engineer Challenge: Design an earthquake-resistant tower! Draft a blueprint with triangular cross-bracing, assemble flexible shock-absorbing joints, and shake-test for structural integrity."
    },
    "VIII-SOC-06": {
        "instructions": [
            "Epoch 1 (1857): The First War of Independence unites soldiers, rulers, and peasants across India.",
            "Epoch 2 (1885): Foundation of the Indian National Congress in Bombay to voice national rights.",
            "Epoch 3 (1920 - 1922): Mahatma Gandhi leads the nationwide Non-Cooperation Movement.",
            "Epoch 4 (1930): The Salt March to Dandi initiates the Civil Disobedience Movement.",
            "Epoch 5 (1942 - 1947): The Quit India Movement launches the final struggle, leading to Independence."
        ],
        "story": "Freedom Struggle Timeline commemorates India's journey to freedom: the Revolt of 1857, the founding of the Congress in 1885, Non-Cooperation, the historic Dandi Salt March, and Quit India in 1942.",
        "audio_script": "Freedom Struggle Timeline commemorates India's journey to freedom: the Revolt of 1857, the founding of the Congress in 1885, Non-Cooperation, the historic Dandi Salt March, and Quit India in 1942."
    }
}

updated_count = 0
for g in catalog:
    gid = g.get('id')
    if gid in enrichment_map:
        info = enrichment_map[gid]
        for k, v in info.items():
            g[k] = v
        updated_count += 1

print(f"Updated {updated_count} games in catalog with instructions, stories, and audio scripts.")

with open('full_games_catalog.json', 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)

with open('full_games_catalog.js', 'w', encoding='utf-8') as f:
    f.write('const FULL_GAMES_CATALOG = ' + json.dumps(catalog, indent=2, ensure_ascii=False) + ';\n')
    f.write('if (typeof module !== "undefined" && module.exports) {\n    module.exports = FULL_GAMES_CATALOG;\n}\n')

print("Saved full_games_catalog.json and full_games_catalog.js successfully.")
