# -*- coding: utf-8 -*-
"""
Class III & IV Question Enhancements:
- Balanced option character lengths (within 10-20% ratio).
- Zero parentheses, brackets, or leaked calculation hints.
- High-quality, plausible, grade-appropriate distractors.
- Exact retention of correct answers at original answer index.
"""

ENHANCEMENTS_C3_C4 = {
    # 0: (LO-048, 1) Class III English - ans=1
    ("LO-048", 1): [
        "Put the receiver down suddenly on the table without speaking",
        "Thank you Uncle Vikram, I will give Dad the message. Goodbye!",
        "Tell the caller you are too busy right now and disconnect",
        "Ask the caller to ring back tomorrow and abruptly hang up"
    ],
    # 1: (LO-048, 2) Class III English - ans=0
    ("LO-048", 2): [
        "Could you please repeat the meeting time once more, Uncle?",
        "I cannot hear anything at all, so I will just hang up now.",
        "You are speaking far too quietly for anyone to understand.",
        "I will just write down whatever time I think sounds right."
    ],
    # 2: (LO-049, 0) Class III English - ans=3
    ("LO-049", 0): [
        "Splash water across the floor while washing faces",
        "Leave the water running while drying your fingers",
        "Wash muddy outdoor toys inside the drinking sink",
        "Turn off the tap tightly after washing your hands"
    ],
    # 3: (LO-049, 1) Class III English - ans=0
    ("LO-049", 1): [
        "To share important helpful reminders and exciting school news with everyone",
        "To decorate the room so students do not need to look at the blackboard",
        "To cover up cracks on the walls without having to paint them with color",
        "To display advertisements for outside shops and commercial toy products"
    ],
    # 4: (LO-049, 2) Class III English - ans=0
    ("LO-049", 2): [
        "Their borrowed storybooks to return to the shelf",
        "Their new coloring crayons for the drawing period",
        "A packed picnic lunch box to share with friends",
        "Their clean sports uniform for physical exercise"
    ],
    # 5: (LO-050, 0) Class III English - ans=1
    ("LO-050", 0): [
        "Speed up and skip ahead past the next three words",
        "Take a short, gentle pause before reading forward",
        "Raise your voice suddenly and shout the next word",
        "Stop reading immediately and close the storybook"
    ],
    # 6: (LO-050, 2) Class III English - ans=0
    ("LO-050", 2): [
        "Rise slightly at the end to show you are asking something",
        "Drop into a flat, steady whisper with no change in pitch",
        "Shout the final word as loud as you can to show surprise",
        "Speed up rapidly through the words without any hesitation"
    ],
    # 7: (LO-051, 1) Class III English - ans=0
    ("LO-051", 1): [
        "Children enjoying nature and observing birds from their treehouse",
        "A carpenter explaining how to cut wooden planks for garden sheds",
        "Neighborhood dogs learning how to climb tall branches safely",
        "Workers clearing fallen dry leaves and twigs from the city park"
    ],
    # 8: (LO-054, 0) Class III English - ans=0
    ("LO-054", 0): [
        "With a brisk, swooshing rush of flowing wind",
        "By spelling out each separate letter slowly",
        "In a silent whisper that nobody can hear at all",
        "With a short, sharp bark like an angry watchdog"
    ],
    # 9: (LO-054, 1) Class III English - ans=3
    ("LO-054", 1): [
        "Reading all lines quietly without opening your lips",
        "Standing completely still like an unmoving statue",
        "Skipping the rhyming words to finish the poem fast",
        "The expressive rising and falling melody of voice pitch"
    ],
    # 10: (LO-054, 2) Class III English - ans=1
    ("LO-054", 2): [
        "Turned backwards toward the curtain while whispering the words quietly",
        "Tall with confident posture, making friendly eye contact with listeners",
        "Slumped over looking down at shoe laces without glancing at the crowd",
        "Restlessly pacing and spinning around the stage without facing forward"
    ],
    # 11: (LO-056, 0) Class III English - ans=0
    ("LO-056", 0): [
        "Ravi swam five laps across the pool yesterday.",
        "Ravi is swimming five laps in the pool right now.",
        "Ravi will swim five laps in the pool on Saturday.",
        "Ravi swims five laps across the pool every morning."
    ],
    # 12: (LO-056, 1) Class III English - ans=3
    ("LO-056", 1): [
        "Maya was playing football every evening.",
        "Maya will play football tomorrow evening.",
        "Maya is playing football right now today.",
        "Maya played football yesterday evening."
    ],
    # 13: (LO-060, 2) Class III English - ans=2
    ("LO-060", 2): [
        "After the word bought so it reads Mom bought, apples",
        "At the very end of the sentence right after oranges",
        "Between the list items as apples, bananas, and oranges",
        "Between the subject and verb as Mom, bought the fruit"
    ],
    # 14: (LO-061, 0) Class III English - ans=2
    ("LO-061", 0): [
        "Flying colorful kites very high in the sky.",
        "Because tomorrow morning will be very sunny.",
        "The wind is perfect for flying kites today.",
        "Underneath the thick green grass by the pond."
    ],
    # 15: (LO-061, 1) Class III English - ans=3
    ("LO-061", 1): [
        "He carried an umbrella so that the hot sun was shining.",
        "Kabir took an umbrella although the sunny sky was clear.",
        "The bright blue umbrella was kept inside the school bag.",
        "He carried an umbrella because dark clouds filled the sky."
    ],
    # 16: (LO-062, 0) Class III English - ans=3
    ("LO-062", 0): [
        "The entrance tickets for the rides cost fifty rupees for each child.",
        "After eating delicious snacks, we walked slowly home in the evening.",
        "Sweet pink cotton candy is sold by vendors near the giant swing ride.",
        "Last Sunday, my family and I visited the lively neighborhood mela."
    ],
    # 17: (LO-062, 2) Class III English - ans=1
    ("LO-062", 2): [
        "My new walking shoes got quite dusty after standing near the ticket counter.",
        "Exhausted but smiling, we returned home with wonderful memories of the day.",
        "A tall Ferris wheel spins in large circles high above the festive grounds.",
        "Before entering the fairgrounds, we purchased four blue tokens at the gate."
    ],
    # 18: (LO-063, 1) Class III EVS - ans=2
    ("LO-063", 1): [
        "Thick curly fur growing all over their legs",
        "Sharp curved talons for catching tree prey",
        "Webbed feet with thin skin between the toes",
        "Heavy split hooves for running across rocks"
    ],
    # 19: (LO-064, 1) Class III EVS - ans=2
    ("LO-064", 1): [
        "Random decorative drawings added simply to fill up blank corner spaces",
        "Confidential teacher codes used strictly for grading classroom tests",
        "A map legend showing where important spots like reading corners sit",
        "Accidental pencil marks left on the sheet while measuring the floor"
    ],
    # 20: (LO-065, 2) Class III EVS - ans=0
    ("LO-065", 2): [
        "The sugar dissolves completely to form a clear sweet liquid",
        "The sugar crystals clump together and settle as hard pebbles",
        "The sugar floats on the surface like lightweight wood chips",
        "The warm water quickly freezes into solid sweet ice blocks"
    ],
    # 21: (LO-066, 1) Class III EVS - ans=1
    ("LO-066", 1): [
        "Because passing dark rain clouds physically block out different portions of the moon",
        "Because the Moon orbits Earth, changing how much of its sunlit surface faces us",
        "Because the Moon slowly shrinks and expands as the night air cools down and warms up",
        "Because bright stars slowly move across the moon and cover up its glowing edges"
    ],
    # 22: (LO-067, 0) Class III EVS - ans=0
    ("LO-067", 0): [
        "Family members share household chores and support each other warmly",
        "One single person is expected to carry out every task on their own",
        "Relatives avoid speaking to one another during difficult afternoons",
        "Everyone leaves home immediately so that no work needs to be done"
    ],
    # 23: (LO-067, 2) Class III EVS - ans=3
    ("LO-067", 2): [
        "The brand of school notebook you buy at the store",
        "The bright shade of plastic on your pencil box",
        "The type of sports shoes you wear to the ground",
        "Eye color, curly hair texture, or height features"
    ],
    # 24: (LO-068, 0) Class III EVS - ans=0
    ("LO-068", 0): [
        "They have no teeth yet and their gentle digestive system is still maturing",
        "They do not require any energy or nutrients during their first several months",
        "Their stomach can only process foods that have a bright white liquid color",
        "They naturally refuse solid food because they dislike chewing crunchy items"
    ],
    # 25: (LO-068, 1) Class III EVS - ans=0
    ("LO-068", 1): [
        "Water hydrates the body, helps digest food, and maintains vital organs",
        "Water is mainly needed by living creatures to wash their outer coats",
        "Animals only consume liquids when they want to cool down during winter",
        "Living organisms can easily survive without any fluids for many months"
    ],
    # 26: (LO-068, 2) Class III EVS - ans=3
    ("LO-068", 2): [
        "Skipping the washing step completely so that no household tap is turned on",
        "Leaving the sink tap running at full force while peeling all the vegetables",
        "Rinsing each single vegetable separately under an open gushing kitchen pipe",
        "Washing vegetables in a bowl and reusing that water for potted garden plants"
    ],
    # 27: (LO-070, 0) Class III EVS - ans=0
    ("LO-070", 0): [
        "To crack open hard nuts, tough seeds, and fruit rinds",
        "To probe deep into flower blossoms for sugary nectar",
        "To scoop up slippery fish from deep freshwater lakes",
        "To strain tiny pond insects and weeds from soft mud"
    ],
    # 28: (LO-071, 2) Class III EVS - ans=0
    ("LO-071", 2): [
        "By carrying items for them, listening to their memories, and offering caring support",
        "By playing noisy music in their bedroom while they are trying to take an afternoon nap",
        "By setting aside their eyeglasses and walking sticks without telling where they are",
        "By letting them manage heavy household chores alone while ignoring their daily needs"
    ],
    # 29: (LO-072, 2) Class III EVS - ans=0
    ("LO-072", 2): [
        "Their shapes help them adapt to local sunlight, climate, and moisture levels",
        "All plant leaves share the exact same outline regardless of their habitat",
        "Gardeners regularly trim every outdoor leaf using specialized hedge shears",
        "Leaves shift their physical patterns every few days to confuse caterpillars"
    ],
    # 30: (LO-073, 0) Class III EVS - ans=0
    ("LO-073", 0): [
        "To the hospital or neighborhood health clinic",
        "To the local post office counter for stamps",
        "To the playground swings in the public park",
        "To the ticket window at the cinema theater"
    ],
    # 31: (LO-073, 1) Class III EVS - ans=3
    ("LO-073", 1): [
        "Fixing flat bicycle tires and replacing broken chains for commuters",
        "Selling flight boarding passes and booking international hotel trips",
        "Pumping diesel fuel and motor oil into heavy transport vehicles",
        "Delivering letters, parcels, and savings services across the country"
    ],
    # 32: (LO-073, 2) Class III EVS - ans=3
    ("LO-073", 2): [
        "A brightly painted board indicating that the seats are kept for young toddlers",
        "A colorful advertisement symbol displaying an iced dessert or refreshment shop",
        "A standard route guidance marker pointing straight toward the driver compartment",
        "A pictorial sign showing an elderly traveler with a cane or an expectant mother"
    ],
    # 33: (LO-074, 1) Class III EVS - ans=3
    ("LO-074", 1): [
        "Discarded plastic scraps and synthetic foam sheets",
        "Piles of dry leaves burning inside closed rooms",
        "Open kerosene torches placed on wooden tables",
        "LPG piped gas stoves and electric induction units"
    ],
    # 34: (LO-075, 1) Class III EVS - ans=2
    ("LO-075", 1): [
        "Keep the feeling a secret and never talk about it with your parents or teachers",
        "Assume that you made a serious mistake and quietly blame yourself for the event",
        "Say a firm and loud no, move quickly to a safe spot, and inform a trusted adult",
        "Hide away silently under a blanket and hope that the problem disappears on its own"
    ],
    # 35: (LO-075, 2) Class III EVS - ans=3
    ("LO-075", 2): [
        "Only girls and women should be expected to prepare food and clean",
        "Daily household chores should be completely avoided by all children",
        "Boys ought to avoid helping around the kitchen or washing dishes",
        "Both boys and girls can equally learn and share household chores"
    ],
    # 36: (LO-076, 0) Class III EVS - ans=2
    ("LO-076", 0): [
        "Rules are created so that neither side can ever score any match points",
        "Rules give unfair privileges so one team can break rules without penalty",
        "Rules ensure fairness, prevent disputes, and keep all participants safe",
        "Rules make athletic activities slow, confusing, and dull for spectators"
    ],
    # 37: (LO-076, 1) Class III EVS - ans=2
    ("LO-076", 1): [
        "Argue heatedly with the match official and push other players off the game court",
        "Throw an angry tantrum on the grass, kick marker cones, and tear up the scorecard",
        "Accept the official call calmly, cheer from the sideline, and await your next turn",
        "Cross your arms stubbornly and refuse to leave the field until the call is changed"
    ],
    # 38: (LO-076, 2) Class III EVS - ans=3
    ("LO-076", 2): [
        "Sitting down on the court grass and refusing to run whenever you feel tired",
        "Demanding that you take every single shot yourself without passing to peers",
        "Blaming the defender or goalkeeper whenever the opposing side scores points",
        "Encouraging your partners, passing the ball, and celebrating team achievements"
    ],
    # 39: (LO-077, 0) Class III EVS - ans=0
    ("LO-077", 0): [
        "It provides cool, life-saving drinking water for thirsty birds and squirrels",
        "It makes the balcony tiles slippery so children do not run along the edges",
        "It serves as an outdoor cleaning basin for washing muddy gardening boots",
        "It helps collect stale rainwater to attract biting insects into the garden"
    ],
    # 40: (LO-077, 1) Class III EVS - ans=1
    ("LO-077", 1): [
        "Walk past them without speaking and leave them alone during recess play periods",
        "Keep access ramps clear and assist them warmly so they join all school activities",
        "Remind them that wheelchair users should avoid entering the library or laboratory",
        "Leave heavy school bags and desks piled up across the main corridor entry ramps"
    ],
    # 41: (LO-077, 2) Class III EVS - ans=2
    ("LO-077", 2): [
        "Set fire to the dry piles creating thick smoke that pollutes neighboring air",
        "Sweep all the leaves underneath parked school buses to hide them out of sight",
        "Collect them in a compost pit to produce rich natural fertilizer for plants",
        "Seal them inside large polythene bags and throw them into the nearby canal"
    ],
    # 42: (LO-078, 0) Class III Mathematics - ans=3
    ("LO-078", 0): [
        "Five small round dots arranged around a wide circle",
        "A single geometric star shape containing five points",
        "A closed square outline drawn with one center stroke",
        "Four vertical lines with one diagonal slash across"
    ],
    # 43: (LO-078, 2) Class III Mathematics - ans=0
    ("LO-078", 2): [
        "Bundling by fives makes it quick and easy to skip-count without confusion",
        "Because mathematical tally marks are never permitted to exceed four strokes",
        "Because standard classroom rulers only display measurements up to five units",
        "Because drawing more than five consecutive lines causes notebooks to tear"
    ],
    # 44: (LO-082, 2) Class III Mathematics - ans=3
    ("LO-082", 2): [
        "To hide the individual product prices from competing shopkeepers nearby",
        "Because shopkeepers are not allowed to calculate totals using mental math",
        "To fill out blank receipt sheets for extra handwriting practice during work",
        "So the customer can review every purchase and verify the total calculation"
    ],
    # 45: (LO-086, 2) Class III Mathematics - ans=1
    ("LO-086", 2): [
        "A large yellow school transport bus",
        "A small silver finger ring or stamp",
        "A full-grown adult African elephant",
        "A heavy sack of whole wheat grains"
    ],
    # 46: (LO-090, 1) Class III Mathematics - ans=3
    ("LO-090", 1): [
        "Add 3 repeatedly to 12 four times over",
        "Subtract 12 repeatedly until reaching 0",
        "Multiply 12 by 3 repeatedly four times",
        "Subtract 3 repeatedly until reaching 0"
    ],
    # 47: (LO-093, 1) Class III Mathematics - ans=1
    ("LO-093", 1): [
        "A single center point located inside the shape",
        "A straight line joining two opposite corners",
        "A curved boundary drawn along the outer border",
        "The flat wooden table surface below the polygon"
    ],
    # 48: (LO-094, 1) Class III Mathematics - ans=2
    ("LO-094", 1): [
        "Because circular tiles are far too heavy to lay flat across a room",
        "Because curved objects constantly roll away when placed on floors",
        "Because circular edges leave curved empty open gaps between tiles",
        "Because circular shapes are mathematically forbidden from touching"
    ],
    # 49: (LO-095, 1) Class III Mathematics - ans=0
    ("LO-095", 1): [
        "Connect dots along a straight path with a ruler",
        "Draw wavy looping arcs that touch every dot once",
        "Place a single dot without drawing connecting rays",
        "Dot grid marks are never allowed to be connected"
    ],
    # 50: (LO-097, 0) Class IV English - ans=2
    ("LO-097", 0): [
        "A solitary roaming male forest lion",
        "A flock of migratory hornbill birds",
        "The oldest and wisest female elephant",
        "The youngest playful baby elephant"
    ],
    # 51: (LO-097, 1) Class IV English - ans=0
    ("LO-097", 1): [
        "Using deep, low rumbles that vibrate through the ground",
        "By tapping rhythmic patterns on hollow fallen tree logs",
        "By whistling high-pitched tunes like migratory songbirds",
        "By waving branches and leaves high up in their trunks"
    ],
    # 52: (LO-097, 2) Class IV English - ans=0
    ("LO-097", 2): [
        "They are deeply caring, cooperative, and highly social herd animals",
        "They are unable to perceive sound vibrations or communicate at all",
        "They avoid helping other herd members and compete for food supplies",
        "They prefer living solitary lives in isolation without family units"
    ],
    # 53: (LO-099, 0) Class IV English - ans=3
    ("LO-099", 0): [
        "Smoky firewood burned in clay stoves",
        "Diesel fuel burned inside generators",
        "Coal furnaces heating boiler engines",
        "Solar power from rooftop solar panels"
    ],
    # 54: (LO-099, 2) Class IV English - ans=0
    ("LO-099", 2): [
        "To grab the reader's attention and summarize the main event instantly",
        "Because printed newspaper sentences are legally limited to five words",
        "To intentionally mislead readers about the real topic of the article",
        "Because printing presses lack enough metallic type for full sentences"
    ],
    # 55: (LO-100, 0) Class IV English - ans=0
    ("LO-100", 0): [
        "Speak with an energetic, sudden pause to show urgent attention",
        "Yawn slowly and drag out the vowel sound in a sleepy manner",
        "Laugh out loud before moving forward to the next sentence",
        "Mumble the word under his breath while glancing at the floor"
    ],
    # 56: (LO-100, 1) Class IV English - ans=2
    ("LO-100", 1): [
        "By whispering the final character name backwards",
        "With a flat, emotionless tone lacking inflection",
        "With a rising pitch that asks for Anita's answer",
        "By omitting the character name from the sentence"
    ],
    # 57: (LO-100, 2) Class IV English - ans=3
    ("LO-100", 2): [
        "Because school rules strictly forbid reading narrative paragraphs at a normal pace",
        "To stretch out the recitation time until the entire audience eventually falls asleep",
        "To intentionally confuse listeners about what each fictional character is doing",
        "It brings characters to life and helps listeners understand the story meaning easily"
    ],
    # 58: (LO-101, 1) Class IV English - ans=1
    ("LO-101", 1): [
        "The author's personal phone number and private home address",
        "Pronunciation guide, part of speech, and example sentences",
        "The current store market value of the printed paper pages",
        "A photographic portrait of every student enrolled in school"
    ],
    # 59: (LO-101, 2) Class IV English - ans=1
    ("LO-101", 2): [
        "They provide secret coded instructions meant exclusively for foreign spies",
        "They show the first and last word on that page to help you search quickly",
        "They list the personal names of the printing press technicians who set type",
        "They indicate which specific book sections the reader should skip entirely"
    ],
    # 60: (LO-102, 2) Class IV English - ans=2
    ("LO-102", 2): [
        "They automatically rewrite confusing plot endings without requiring extra reading",
        "They allow you to skip past difficult descriptive paragraphs during comprehension",
        "You can deduce the meaning of unfamiliar words using clues in neighboring sentences",
        "They prompt you to close the book whenever an unfamiliar difficult word appears"
    ],
    # 61: (LO-103, 0) Class IV English - ans=0
    ("LO-103", 0): [
        "Orange sparks danced into the dark sky while dry pine logs crackled in the cool night breeze.",
        "The scout leader stood beside the campsite boundary while blowing a loud metal whistle.",
        "We sat together near our green camping tents and ate warm roasted potatoes for dinner.",
        "Campfire logs are made of chopped forest wood and can produce smoke when burned outside."
    ],
    # 62: (LO-103, 1) Class IV English - ans=2
    ("LO-103", 1): [
        "Staring silently out the classroom window while waiting for the bell to ring",
        "Speaking continuously in a monotone mumble without making any natural pauses",
        "Speaking clearly, showing genuine excitement, and sequencing events in order",
        "Glancing down at your shoes while whispering barely audible words to yourself"
    ],
    # 63: (LO-103, 2) Class IV English - ans=2
    ("LO-103", 2): [
        "That marks the absolute end of the camping trip and I have nothing more to share.",
        "Our waterproof camping shelter was constructed with bright blue nylon canvas panels.",
        "As we packed our tents next morning, I looked forward to our next outdoor adventure.",
        "Green grass grows across forest camping clearings where visitors assemble in summer."
    ],
    # 64: (LO-104, 0) Class IV English - ans=2
    ("LO-104", 0): [
        "Air-conditioned indoor enclosures, metal cages, and processed domestic pet food",
        "Paving multi-lane highways and building concrete shopping malls across reserves",
        "Large connected forest corridors, clean water sources, and wildlife protection",
        "Domesticating wild predators so that they can live safely inside family houses"
    ],
    # 65: (LO-104, 1) Class IV English - ans=0
    ("LO-104", 1): [
        "Identifying the main ideas and key facts and stating them briefly in your own words",
        "Inventing an entirely fictional tale that replaces the factual points presented",
        "Transcribing every single cough, stumble, and unrelated comment the speaker uttered",
        "Ignoring the presentation entirely and writing about an unrelated personal hobby"
    ],
    # 66: (LO-104, 2) Class IV English - ans=1
    ("LO-104", 2): [
        "Because their presence in urban gardens helps shield municipal street trees from storm damage and pollution",
        "Protecting tiger habitats automatically safeguards thousands of plants, insects, and animals in that forest",
        "Because adult tigers carry large palm fronds over their cubs to shelter them from heavy monsoon downpours",
        "Because their orange and black striped coats resemble traditional umbrellas used in rural village markets"
    ],
    # 67: (LO-105, 1) Class IV English - ans=0
    ("LO-105", 1): [
        "The clear distinction between the sh and s sounds",
        "The subtle contrast between the hard c and g sounds",
        "The explosive contrast between the b and p sounds",
        "The humming transition between the m and n sounds"
    ],
    # 68: (LO-106, 0) Class IV English - ans=2
    ("LO-106", 0): [
        "Discard empty plastic bottles into local flowing river streams",
        "Fill an entire washing tub with fresh water to rinse one spoon",
        "Repair leaky taps quickly and harvest rainwater for home gardens",
        "Leave garden hoses running continuously across outdoor pavements"
    ],
    # 69: (LO-106, 1) Class IV English - ans=2
    ("LO-106", 1): [
        "Avoid brushing teeth altogether so that running water is never required",
        "Let the bathroom washbasin overflow until water spills into the hallway",
        "Turn off the tap while scrubbing teeth and use a small mug to rinse out",
        "Keep the tap valve running at maximum pressure throughout the routine"
    ],
    # 70: (LO-107, 0) Class IV English - ans=2
    ("LO-107", 0): [
        "Take whatever timber you want, as forests have no value",
        "I shall step aside so you can chop down every green bough",
        "A severed head is a small cost if it saves a living tree",
        "Fell this entire woodland grove to build royal palace halls"
    ],
    # 71: (LO-107, 1) Class IV English - ans=2
    ("LO-107", 1): [
        "They clutter the platform floor so actors cannot move around easily",
        "They provide decorative missiles to toss playfully toward spectators",
        "They help the audience visualize historical characters and the setting",
        "They eliminate any requirement for the student performers to speak out"
    ],
    # 72: (LO-107, 2) Class IV English - ans=3
    ("LO-107", 2): [
        "Ancient forests are troublesome obstacles that should be cleared for urbanization",
        "Only powerful monarchs have the authority to decide how natural habitats are managed",
        "Timber from rare trees should be gathered freely to build lavish decorative homes",
        "Communities have the power to protect trees and wildlife through unity and bravery"
    ],
    # 73: (LO-108, 0) Class IV English - ans=0
    ("LO-108", 0): [
        "A bubbling, flowing mountain brook",
        "A vintage steam railway locomotive",
        "A high-altitude passenger aircraft",
        "A motionless boulder upon the hill"
    ],
    # 74: (LO-108, 2) Class IV English - ans=3
    ("LO-108", 2): [
        "Recite as rapidly as possible without pausing for any natural breath breaks",
        "Whisper each phrase backwards while keeping your eyes shut upon the stage",
        "Pause after every single syllable for several seconds to break the rhythm",
        "Match the natural musical bounce and cadence of verses without any rush"
    ],
    # 75: (LO-109, 2) Class IV English - ans=2
    ("LO-109", 2): [
        "Because kitchen recipes are forbidden from containing ordinary action verbs",
        "They scramble the instructions so that readers cannot follow the procedure",
        "They guide the reader to carry out every step in the correct planned order",
        "They are merely filler terms meant to make instructional sentences longer"
    ],
    # 76: (LO-111, 1) Class IV English - ans=1
    ("LO-111", 1): [
        "Down words are spelled in reverse order, while Across words follow normal spelling",
        "Across words run horizontally along rows, while Down words read vertically downward",
        "Across clues represent numeric values, while Down clues exclusively describe colors",
        "Both terms refer to the exact same straight direction across the square grid lines"
    ],
    # 77: (LO-113, 1) Class IV English - ans=3
    ("LO-113", 1): [
        "A wishlist showing the purchase price of preferred gifts",
        "Confidential journal entries sharing your private secrets",
        "A specific description of the colorful shoes you will wear",
        "The date, starting time, venue location, and event purpose"
    ],
    # 78: (LO-114, 2) Class IV English - ans=0
    ("LO-114", 2): [
        "The pronoun I and specific proper names like India or the river Ganga",
        "Any descriptive adjective that contains more than six English letters",
        "Every action verb that appears near the middle of a completed clause",
        "Common spatial prepositions like inside, upon, beneath, or behind"
    ],
    # 79: (LO-115, 2) Class IV EVS - ans=2
    ("LO-115", 2): [
        "They absorb saline moisture directly from deep desert sand dunes through their split hooves",
        "They consume discarded metal containers to obtain mineral moisture during long expeditions",
        "They store fat in humps for energy, lose little water through sweat, and make very dry dung",
        "They conceal small natural reservoirs of groundwater inside specialized ear canal pouches"
    ],
    # 80: (LO-116, 1) Class IV EVS - ans=1
    ("LO-116", 1): [
        "By grinding the hard outer husk into sweet morning breakfast juice",
        "As an organic biodegradable hanging plant pot or bird drinking bowl",
        "By burning the shell inside a closed bedroom to provide indoor heat",
        "By tossing the tough dried shell directly into municipal sewer lines"
    ],
    # 81: (LO-116, 2) Class IV EVS - ans=0
    ("LO-116", 2): [
        "They are completely biodegradable, non-toxic, and safe for soil",
        "They cost tens of thousands of rupees to purchase at craft shops",
        "They create permanent stains that can never be washed off floors",
        "They undergo a chemical change that turns into plastic overnight"
    ],
    # 82: (LO-118, 0) Class IV EVS - ans=3
    ("LO-118", 0): [
        "Molten iron alloys and sheets of steel",
        "Granulated synthetic plastic pellets",
        "Crushed cement powder and gravel stone",
        "Fine moist clay and silt from riverbeds"
    ],
    # 83: (LO-118, 1) Class IV EVS - ans=2
    ("LO-118", 1): [
        "Because natural ice crystals spontaneously generate along the bottom of clay bowls",
        "Because traditional earthenware pots contain tiny electric cooling coils built in",
        "Water seeps through microscopic clay pores and evaporates, carrying heat away with it",
        "Because village matkas must be kept inside industrial freezer chambers overnight"
    ],
    # 84: (LO-118, 2) Class IV EVS - ans=1
    ("LO-118", 2): [
        "Carve personal initials onto ancient monument stone walls as a lasting memorial mark",
        "Record notes, sketch traditional tools, and interview experienced artisans politely",
        "Toss your notebook into the crowd and rely entirely on memory without writing details",
        "Run noisily past historical displays without observing artifacts or asking questions"
    ],
    # 85: (LO-119, 0) Class IV EVS - ans=1
    ("LO-119", 0): [
        "They remember visual landscape features by using extraordinarily sharp, camera-like compound eyesight",
        "They follow chemical scent trails called pheromones that traveling ants detect with their antennae",
        "They monitor subtle seismic shockwaves traveling through soil caused by the footsteps of leading workers",
        "They produce high-frequency buzzing calls using miniature vibrating wing membranes on their thorax"
    ],
    # 86: (LO-119, 2) Class IV EVS - ans=1
    ("LO-119", 2): [
        "To hoard massive stockpiles of harvested grain seeds safe from cold winter frosts",
        "To safeguard fragile eggs and chicks from monsoon rains and predators like snakes",
        "To capture passing flying insects inside the hanging hollow bottom entrance chute",
        "To provide a crowded communal dormitory where many unrelated bird families sleep"
    ],
    # 87: (LO-120, 0) Class IV EVS - ans=0
    ("LO-120", 0): [
        "Crop harvest, wholesale mandi, grain flour mill, dough kneading, hot roti",
        "Hot baked roti, seed planting in soil, flour grinding mill, wholesale mandi",
        "Grain flour mill, sowing wheat seeds, kitchen cooking, harvesting the crop",
        "Kneading wheat dough, crop harvesting, grain flour mill, local retail shop"
    ],
    # 88: (LO-120, 2) Class IV EVS - ans=2
    ("LO-120", 2): [
        "Because unprocessed wheat seeds can only sprout while stored inside hessian sacks",
        "To make the grain bundles heavier so farmers can charge higher prices at market",
        "To eliminate moisture so fungal mold, rot, and insects cannot spoil stored grains",
        "To ensure that individual cereal kernels transform into shiny golden metal coins"
    ],
    # 89: (LO-121, 0) Class IV EVS - ans=3
    ("LO-121", 0): [
        "By playing virtual textile designing video games on digital smartphones",
        "By purchasing finished machine garments from air-conditioned retail malls",
        "By memorizing complete jacquard patterns overnight in a brief morning dream",
        "By training for years under experienced family elders and master weavers"
    ],
    # 90: (LO-121, 2) Class IV EVS - ans=2
    ("LO-121", 2): [
        "To accelerate the closure of heritage weaving hamlets so rural families move to industrial factory jobs",
        "Because handcrafted textiles possess no artistic merit compared to mass-produced synthetic imports",
        "It preserves cultural heritage, sustains rural artisan livelihoods, and uses eco-friendly materials",
        "Because selling traditional handmade goods in urban marketplaces has been prohibited by national law"
    ],
    # 91: (LO-122, 0) Class IV EVS - ans=3
    ("LO-122", 0): [
        "A temporary flock of wild birds flying swiftly across the afternoon horizon",
        "A small random fracture running along the asphalt surface of a walking pavement",
        "A mythical cache of gold coins concealed deeply beneath neighborhood roadways",
        "A prominent, easily recognized building or natural feature that guides travelers"
    ],
    # 92: (LO-122, 2) Class IV EVS - ans=0
    ("LO-122", 2): [
        "A navigation landmark showing where to turn",
        "The ultimate terminal destination of the trip",
        "A permanent barricade preventing further travel",
        "An administrative classroom inside the school"
    ],
    # 93: (LO-124, 0) Class IV EVS - ans=3
    ("LO-124", 0): [
        "To flutter back and forth like cooling mechanical fans during humid tropical afternoons",
        "To store forest acorns and winter berries inside specialized outer ear flap cavities",
        "To generate aerodynamic lift so they can glide between high branches like wild birds",
        "To detect faint sounds of approaching predators from all directions without moving heads"
    ],
    # 94: (LO-124, 1) Class IV EVS - ans=0
    ("LO-124", 1): [
        "To stalk silently across ground without snapping twigs or making footsteps",
        "To slide smoothly down muddy hillside slopes while pursuing woodland prey",
        "To bounce vertically like elastic rubber balls to snatch high flying birds",
        "Because wild big cats feel uncomfortable when their skin contacts raw soil"
    ],
    # 95: (LO-125, 0) Class IV EVS - ans=2
    ("LO-125", 0): [
        "It creates confusion so that distant cousins and elders forget each other names and relations",
        "It requires family members to stay confined inside separate locked chambers without speaking",
        "It lets relatives share memories, celebrate cultural traditions, and nurture supportive bonds",
        "It compels household members to stop preparing meals and avoid sharing festive dining tables"
    ],
    # 96: (LO-125, 2) Class IV EVS - ans=1
    ("LO-125", 2): [
        "Because commercial moving trucks offer free transport services",
        "For better employment, educational schooling, or job transfers",
        "To isolate themselves permanently from contacting other people",
        "Because residential houses naturally vanish after twelve months"
    ],
    # 97: (LO-126, 0) Class IV EVS - ans=0
    ("LO-126", 0): [
        "Underground swollen taproots storing food nutrients",
        "Stout woody outer bark peeled from arboreal stems",
        "Broad green photosynthetic leaves collecting light",
        "Brightly pigmented flower petals attracting wasps"
    ],
    # 98: (LO-126, 1) Class IV EVS - ans=1
    ("LO-126", 1): [
        "Because diurnal blossoms never produce any aromatic fragrance at all",
        "To guide nocturnal pollinators like night-flying moths in the darkness",
        "To ward off every living garden visitor with harsh overwhelming smells",
        "To frighten woodland birds so they avoid perching near flowering stems"
    ],
    # 99: (LO-126, 2) Class IV EVS - ans=3
    ("LO-126", 2): [
        "Potato and onion",
        "Spinach and mint",
        "Ginger and turnip",
        "Tomato and pepper"
    ],
    # 100: (LO-127, 0) Class IV EVS - ans=0
    ("LO-127", 0): [
        "On foot, in bullock carts, on horses, and in wooden sailboats",
        "By riding rapid electric metro trains and underground subways",
        "By driving high-speed motorcars across paved highway networks",
        "By boarding commercial jet airliners and supersonic airplanes"
    ],
    # 101: (LO-127, 1) Class IV EVS - ans=1
    ("LO-127", 1): [
        "Compressed cardboard and paperboard",
        "Brass, copper, bronze, and red clay",
        "Thin synthetic polythene containers",
        "Molded lightweight styrofoam pieces"
    ],
    # 102: (LO-127, 2) Class IV EVS - ans=3
    ("LO-127", 2): [
        "People ceased corresponding and no longer exchange thoughts across distances",
        "Communities rely exclusively on hollow wooden signal drums sounded on hills",
        "Standard postal notes now require over a decade to reach neighboring towns",
        "To instant voice calls, video chats, and digital messages delivered in seconds"
    ],
    # 103: (LO-128, 0) Class IV EVS - ans=3
    ("LO-128", 0): [
        "Paying substantial tuition fees for private schooling",
        "Working regular daytime shifts inside local brick kilns",
        "Remaining isolated at home without textbooks or study",
        "Free and compulsory schooling in a neighborhood school"
    ],
    # 104: (LO-128, 1) Class IV EVS - ans=1
    ("LO-128", 1): [
        "It produces zero lasting physical or developmental consequences for growing youths",
        "It deprives children of their rights to play, learn in school, and develop safely",
        "Because children operate machinery far too swiftly for adult managers to supervise",
        "Because manufacturing facilities generally hold personal prejudice against youths"
    ],
    # 105: (LO-128, 2) Class IV EVS - ans=0
    ("LO-128", 2): [
        "With total equality, mutual respect, and equal opportunities to learn and lead",
        "By excluding students who converse in regional mother tongues from activities",
        "By giving unfair preference to boys over girls in sports arenas and classrooms",
        "By enforcing rigid stereotypes about which tasks girls should be allowed to do"
    ],
    # 106: (LO-129, 0) Class IV EVS - ans=1
    ("LO-129", 0): [
        "Collecting excess single-use polythene wrappers simply to accumulate extra trash",
        "Cutting down on the amount of unnecessary waste and disposable items we generate",
        "Discarding surplus cooked kitchen meals directly into flowing municipal rivers",
        "Purchasing multiple new plastic novelty toys each afternoon without real need"
    ],
    # 107: (LO-129, 1) Class IV EVS - ans=3
    ("LO-129", 1): [
        "Toss the empty glass container into an open roadside drainage gutter",
        "Shatter the brittle glass on the concrete surface of school grounds",
        "Toss the empty glass vessel into an open timber bonfire to burn down",
        "Wash it cleanly and use it to store pencils, sewing buttons, or seeds"
    ],
    # 108: (LO-129, 2) Class IV EVS - ans=3
    ("LO-129", 2): [
        "Power consumption generates zero noticeable influence on natural woodland environments",
        "Because unlit rooms physically expand in floor area whenever illumination is shut off",
        "To ensure that other household members are discouraged from stepping into that space",
        "Conserving power saves fossil fuels and lowers harmful emissions from thermal plants"
    ],
    # 109: (LO-132, 2) Class IV Mathematics - ans=0
    ("LO-132", 2): [
        "Fill it using a verified 1-litre bottle and count how many bottles it holds",
        "Stand across the hallway and visually assess the depth with your eyes shut",
        "Guess another random numeric capacity value without using any container",
        "Place the dry empty bucket on a weighing balance without adding any liquid"
    ],
    # 110: (LO-134, 1) Class IV Mathematics - ans=3
    ("LO-134", 1): [
        "1 hour and 45 minutes",
        "1 hour and 30 minutes",
        "1 hour and 05 minutes",
        "1 hour and 15 minutes"
    ],
    # 111: (LO-136, 2) Class IV Mathematics - ans=0
    ("LO-136", 2): [
        "3 meters and 50 centimeters",
        "35 meters and 0 centimeters",
        "30 meters and 5 centimeters",
        "0 meters and 35 centimeters"
    ],
    # 112: (LO-137, 2) Class IV Mathematics - ans=2
    ("LO-137", 2): [
        "12 apples per basket",
        "16 apples per basket",
        "10 apples per basket",
        "8 apples per basket"
    ],
    # 113: (LO-139, 2) Class IV Mathematics - ans=3
    ("LO-139", 2): [
        "The total weight of the object measured in gram units",
        "The count of individual equal pieces eaten or removed",
        "The mathematical multiplication factor for the fraction",
        "The total number of equal parts the whole is split into"
    ],
    # 114: (LO-141, 2) Class IV Mathematics - ans=2
    ("LO-141", 2): [
        "It increases by one place value by appending one zero",
        "It decreases in value by removing two terminal zeros",
        "It increases by two place values by appending two zeros",
        "Its numerical value remains completely unchanged at all"
    ],
    # 115: (LO-143, 0) Class IV Mathematics - ans=1
    ("LO-143", 0): [
        "The right-hand section is three times larger than the left-hand section",
        "Both halves are exact mirror reflections in shape, size, and alignment",
        "The opposite sides display entirely different geometric polygons and lines",
        "One half displays full motifs while the opposite side remains completely blank"
    ],
    # 116: (LO-144, 0) Class IV Mathematics - ans=3
    ("LO-144", 0): [
        "The outer circumference",
        "A straight chord segment",
        "The circular diameter line",
        "The center of the circle"
    ],
    # 117: (LO-144, 2) Class IV Mathematics - ans=3
    ("LO-144", 2): [
        "Diameter and radius have no geometric connection",
        "Diameter measures exactly half of radius length",
        "Diameter is equal to the radius of that circle",
        "Diameter is exactly twice the length of radius"
    ],
    # 118: (LO-146, 1) Class IV Mathematics - ans=0
    ("LO-146", 1): [
        "A triangle atop a rectangle",
        "A smooth continuous circle",
        "A single straight flat ray",
        "A winding curved line oval"
    ],
    # 119: (LO-146, 2) Class IV Mathematics - ans=1
    ("LO-146", 2): [
        "To make drafting architectural blueprints as complicated and slow as possible",
        "It shows exact dimensions from all angles so builders construct each face correctly",
        "Because modern engineering software is unable to render three-dimensional shapes",
        "To ensure that construction workers cannot tell what the interior layout looks like"
    ],
    # 120: (LO-147, 0) Class IV Mathematics - ans=0
    ("LO-147", 0): [
        "A symmetrical design where both sides mirror each other",
        "A completely dry sheet where all the wet paint vanished",
        "A printed photo image showing complex machinery shapes",
        "One side coated in paint while the opposite stays dry"
    ]
}

def apply_enhancements(games):
    applied = 0
    for g in games:
        gid = g['id']
        for q_idx, q in enumerate(g.get('questions', [])):
            key = (gid, q_idx)
            if key in ENHANCEMENTS_C3_C4:
                q['options'] = ENHANCEMENTS_C3_C4[key]
                applied += 1
    return applied
