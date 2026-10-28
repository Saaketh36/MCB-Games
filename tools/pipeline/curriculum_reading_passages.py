"""
Pre-curated, curriculum-aligned English Reading Comprehension Passages & Questions
for MyClassboard Games Platform (Classes I to VIII).
Topics cover Nature, Animals, Science, Inventions, Adventures, Moral Stories, and Biographies.
Includes:
- Passage title, topic, genre, estimated reading time, reading level
- Paragraphs
- Interactive vocabulary glossaries (word, definition, example)
- Comprehension questions (MCQ + Short Typed with text evidence clues)
"""

READING_PASSAGES = {
    "II-ENG-05": {
        "title": "Story Detective",
        "class": "II",
        "subject": "English",
        "skillArea": "Reading",
        "activity": "Reading Comprehension",
        "gameType": "Reading Comprehension",
        "passage": {
            "title": "The Little Beaver Who Wanted to Fly",
            "topic": "Animals & Perseverance",
            "genre": "Story",
            "readingLevel": "Class II",
            "estimatedTime": "3 min",
            "content": [
                "Barnaby was a little brown beaver with soft fur and a wide flat tail. He lived by the Sparkling River with his family. While all the other young beavers loved cutting wood and building wooden dams, Barnaby spent his afternoons gazing up at the bright blue sky.",
                "Barnaby watched Pippa the swallow glide through the clouds. 'I want to fly up there!' Barnaby announced proudly to the forest animals.",
                "The older beavers chuckled softly. 'Beavers swim, Barnaby. They do not fly!' But Barnaby did not give up. He climbed a tall grassy mound, spread his front paws wide, and jumped. Whoosh—splash! He landed right into the cool river water.",
                "Pippa swooped down and perched gently on a willow branch. 'You may not have feathers, Barnaby, but you can build something with wings!' That gave Barnaby a brilliant idea. Using smooth willow twigs and large green leaves, he crafted a light pair of gliders. With a brave leap into the river breeze, he sailed across the pond for three whole seconds before safely splashing down. The river animals cheered!"
            ],
            "vocabulary": [
                {
                    "word": "gazing",
                    "definition": "Looking at something steadily and with wonder or curiosity.",
                    "example": "Barnaby was gazing at the fluffy clouds."
                },
                {
                    "word": "glide",
                    "definition": "To move smoothly, quietly, and continuously through the air.",
                    "example": "Swallows glide gracefully above the lake."
                },
                {
                    "word": "crafted",
                    "definition": "Made or created something skillfully with your hands.",
                    "example": "He crafted a sturdy birdhouse from cedar wood."
                },
                {
                    "word": "brilliant",
                    "definition": "Very bright, clever, or impressive.",
                    "example": "Maya came up with a brilliant plan to solve the puzzle."
                }
            ]
        },
        "questions": [
            {
                "id": 1,
                "type": "mcq",
                "prompt": "Where did Barnaby the beaver live?",
                "options": [
                    "In a rocky mountain cave",
                    "By the Sparkling River",
                    "On top of an oak tree",
                    "In a desert oasis"
                ],
                "answer": 1,
                "evidenceParagraph": 0,
                "explanation": "Paragraph 1 explicitly tells us: 'He lived by the Sparkling River with his family.'"
            },
            {
                "id": 2,
                "type": "mcq",
                "prompt": "What did the older beavers say when Barnaby said he wanted to fly?",
                "options": [
                    "Beavers swim, they do not fly",
                    "You need to eat more green leaves",
                    "Ask Pippa to give you some feathers",
                    "Climb the highest pine tree first"
                ],
                "answer": 0,
                "evidenceParagraph": 2,
                "explanation": "In Paragraph 3, the older beavers chuckled: 'Beavers swim, Barnaby. They do not fly!'"
            },
            {
                "id": 3,
                "type": "mcq",
                "prompt": "What does the word 'glide' mean in Paragraph 2?",
                "options": [
                    "To swim deep underwater",
                    "To move smoothly through the air",
                    "To build a heavy dam",
                    "To hide beneath the mud"
                ],
                "answer": 1,
                "evidenceParagraph": 1,
                "explanation": "'Glide' describes moving smoothly and quietly through the air without flapping."
            },
            {
                "id": 4,
                "type": "typed",
                "prompt": "What natural materials did Barnaby use to craft his glider wings?",
                "answer": "willow twigs and green leaves",
                "keywords": ["twigs", "leaves"],
                "evidenceParagraph": 3,
                "explanation": "Paragraph 4 explains: 'Using smooth willow twigs and large green leaves, he crafted a light pair of gliders.'"
            },
            {
                "id": 5,
                "type": "typed",
                "prompt": "How many seconds did Barnaby sail across the pond before splashing down?",
                "answer": "three seconds",
                "keywords": ["three", "3"],
                "evidenceParagraph": 3,
                "explanation": "Paragraph 4 states that Barnaby 'sailed across the pond for three whole seconds'."
            }
        ]
    },

    "III-ENG-05": {
        "title": "Read & Reveal",
        "class": "III",
        "subject": "English",
        "skillArea": "Reading",
        "activity": "Reading Comprehension",
        "gameType": "Reading Comprehension",
        "passage": {
            "title": "The Secret Dance of the Honeybee",
            "topic": "Insects & Nature Communication",
            "genre": "Science Essay",
            "readingLevel": "Class III",
            "estimatedTime": "3 min",
            "content": [
                "Honeybees are among the hardest working creatures on planet Earth. A single worker bee visits hundreds of flowers each day to collect golden nectar and powdery pollen. But how does a bee tell thousands of hive mates where the sweetest blossoms are located?",
                "The answer is astonishing: bees communicate through dance! When a scout bee finds a rich flower patch, she flies back inside the dark hive and begins performing the famous 'waggle dance' on the honeycomb.",
                "If flowers are close to the hive, within fifty meters, she runs in a simple circle. But if flowers are far away, she runs in a figure-eight pattern while shaking her abdomen quickly from side to side.",
                "The angle of her dance points in the exact direction of the flowers relative to the sun. The length of the waggle tells the other bees the exact distance! Scientists call this nature's GPS. Because of this clever dance, the hive never runs out of honey."
            ],
            "vocabulary": [
                {
                    "word": "astonishing",
                    "definition": "Extremely surprising or amazing.",
                    "example": "It is astonishing how bees remember landmarks."
                },
                {
                    "word": "nectar",
                    "definition": "A sweet liquid produced by flowers to attract pollinators.",
                    "example": "Bees sip sugary nectar to make honey."
                },
                {
                    "word": "abdomen",
                    "definition": "The rear or back section of an insect's three-part body.",
                    "example": "The scout bee waggled her abdomen vigorously."
                },
                {
                    "word": "relative",
                    "definition": "Considered in relation or proportion to something else.",
                    "example": "The scout dances relative to the sun's position."
                }
            ]
        },
        "questions": [
            {
                "id": 1,
                "type": "mcq",
                "prompt": "How do scout bees communicate the location of flowers to their hive mates?",
                "options": [
                    "By buzzing loudly in three tones",
                    "By performing a special waggle dance",
                    "By leaving scent trails on flower stems",
                    "By tapping their legs against tree bark"
                ],
                "answer": 1,
                "evidenceParagraph": 1,
                "explanation": "Paragraph 2 states: 'The answer is astonishing: bees communicate through dance!' performing the 'waggle dance'."
            },
            {
                "id": 2,
                "type": "mcq",
                "prompt": "What dance does a bee do when the flowers are close, within fifty meters?",
                "options": [
                    "A figure-eight waggle",
                    "A simple circle dance",
                    "A backward hop",
                    "A stationary vibration"
                ],
                "answer": 1,
                "evidenceParagraph": 2,
                "explanation": "Paragraph 3 explains: 'If flowers are close to the hive, within fifty meters, she runs in a simple circle.'"
            },
            {
                "id": 3,
                "type": "mcq",
                "prompt": "What does the angle of the bee's dance tell other bees?",
                "options": [
                    "The temperature of the air",
                    "The exact direction of the flowers relative to the sun",
                    "How many raindrops are falling",
                    "The color of the flower petals"
                ],
                "answer": 1,
                "evidenceParagraph": 3,
                "explanation": "Paragraph 4 explains: 'The angle of her dance points in the exact direction of the flowers relative to the sun.'"
            },
            {
                "id": 4,
                "type": "typed",
                "prompt": "What does the length or duration of the bee's waggle tell the other bees?",
                "answer": "the distance to the flowers",
                "keywords": ["distance"],
                "evidenceParagraph": 3,
                "explanation": "Paragraph 4 confirms: 'The length of the waggle tells the other bees the exact distance!'"
            },
            {
                "id": 5,
                "type": "typed",
                "prompt": "What two things does a worker bee collect from flowers each day?",
                "answer": "nectar and pollen",
                "keywords": ["nectar", "pollen"],
                "evidenceParagraph": 0,
                "explanation": "Paragraph 1 mentions collecting 'golden nectar and powdery pollen'."
            }
        ]
    },

    "V-ENG-07": {
        "title": "Passage Pursuit",
        "class": "V",
        "subject": "English",
        "skillArea": "Reading",
        "activity": "Reading Comprehension",
        "gameType": "Reading Comprehension",
        "passage": {
            "title": "Voyage to Mars: Journey of the Red Planet Rover",
            "topic": "Space Exploration & Robotics",
            "genre": "Informational Essay",
            "readingLevel": "Class V",
            "estimatedTime": "4 min",
            "content": [
                "Mars, known as the Red Planet due to iron oxide rust covering its dusty surface, has fascinated astronomers for centuries. Sending humans across millions of kilometers of vacuum is still a gigantic engineering challenge. Therefore, space agencies rely on robotic explorers called rovers to scout the terrain.",
                "Rovers are car-sized robotic laboratories equipped with high-resolution cameras, laser spectrometers, drill arms, and solar panels or nuclear batteries. They withstand freezing nights where temperatures plummet below minus eighty degrees Celsius.",
                "In 2021, the Perseverance rover landed inside Jezero Crater—an ancient lake basin that dried up billions of years ago. Perseverance carries a miniature robotic helicopter named Ingenuity. Engineers wondered if rotor blades could spin fast enough in Mars's thin atmosphere, which is only one percent as dense as Earth's.",
                "Against all odds, Ingenuity completed over seventy successful flights! It flew ahead of the rover, photographing ridges and boulder fields to map safe paths. Meanwhile, Perseverance drilled core samples from ancient rocks to search for microscopic signs of past microbial life. These robotic pioneers prove that curiosity and perseverance can conquer distant worlds."
            ],
            "vocabulary": [
                {
                    "word": "spectrometer",
                    "definition": "A scientific instrument used to examine the composition of rocks and gases by analyzing light.",
                    "example": "The rover's spectrometer analyzed the chemical makeup of red sand."
                },
                {
                    "word": "plummet",
                    "definition": "To fall or drop straight down at high speed.",
                    "example": "Martian temperatures plummet rapidly after twilight."
                },
                {
                    "word": "microbial",
                    "definition": "Relating to or caused by microscopic organisms like bacteria.",
                    "example": "Scientists look for ancient microbial fossils in the mudstone."
                },
                {
                    "word": "perseverance",
                    "definition": "Continued effort to do or achieve something despite difficulties or delay.",
                    "example": "Her perseverance in learning coding earned her top honors."
                }
            ]
        },
        "questions": [
            {
                "id": 1,
                "type": "mcq",
                "prompt": "Why does Mars appear red to astronomers?",
                "options": [
                    "Because of red volcanic lava",
                    "Due to iron oxide rust on its surface",
                    "Because of red vegetation and forests",
                    "Due to thick red clouds of steam"
                ],
                "answer": 1,
                "evidenceParagraph": 0,
                "explanation": "Paragraph 1 mentions Mars is 'known as the Red Planet due to iron oxide rust covering its dusty surface'."
            },
            {
                "id": 2,
                "type": "mcq",
                "prompt": "Where did the Perseverance rover land on Mars in 2021?",
                "options": [
                    "Olympus Mons Volcano",
                    "Jezero Crater",
                    "Gale Crater",
                    "Valles Marineris Canyon"
                ],
                "answer": 1,
                "evidenceParagraph": 2,
                "explanation": "Paragraph 3 states: 'In 2021, the Perseverance rover landed inside Jezero Crater—an ancient lake basin'."
            },
            {
                "id": 3,
                "type": "mcq",
                "prompt": "Why was flying a helicopter on Mars such a difficult challenge?",
                "options": [
                    "Mars has zero gravity",
                    "Mars's atmosphere is only one percent as dense as Earth's",
                    "The helicopter had no radio signal",
                    "High winds break all propellers"
                ],
                "answer": 1,
                "evidenceParagraph": 2,
                "explanation": "Paragraph 3 notes: 'atmosphere, which is only one percent as dense as Earth's'."
            },
            {
                "id": 4,
                "type": "typed",
                "prompt": "What is the name of the miniature robotic helicopter carried by Perseverance?",
                "answer": "Ingenuity",
                "keywords": ["ingenuity"],
                "evidenceParagraph": 2,
                "explanation": "Paragraph 3 specifies: 'Perseverance carries a miniature robotic helicopter named Ingenuity.'"
            },
            {
                "id": 5,
                "type": "typed",
                "prompt": "What does Perseverance search for when drilling rock core samples?",
                "answer": "microscopic signs of past microbial life",
                "keywords": ["life", "microbial"],
                "evidenceParagraph": 3,
                "explanation": "Paragraph 4 explains: 'drilled core samples from ancient rocks to search for microscopic signs of past microbial life.'"
            }
        ]
    },

    "VI-ENG-06": {
        "title": "Comprehension Quest",
        "class": "VI",
        "subject": "English",
        "skillArea": "Reading",
        "activity": "Reading Comprehension",
        "gameType": "Reading Comprehension",
        "passage": {
            "title": "The Living Root Bridges of Meghalaya",
            "topic": "Nature & Indigenous Engineering",
            "genre": "Informational Essay",
            "readingLevel": "Class VI",
            "estimatedTime": "4 min",
            "content": [
                "Deep in the mist-shrouded subtropical rainforests of Meghalaya in Northeast India lies one of the world's most astonishing wonders of indigenous bio-engineering: the living root bridges, locally known as 'Jingkieng Jri'.",
                "The Khasi and Jaintia tribes live in valleys that receive some of the highest annual rainfall on Earth. During the monsoon, roaring rivers swell with violent torrents, snapping ordinary bamboo or timber bridges like toothpicks. Rather than fighting nature, the Khasi people collaborated with it.",
                "Along riverbanks grows the Ficus elastica, the Indian rubber tree. This tree produces thick, flexible aerial roots that sprout from its trunk. Elders hollow out betel nut trunks, place them horizontally across the chasm, and guide the young pliable roots through the hollow tubes. Over fifteen to twenty years, the roots reach the opposite bank, take firm root in the soil, and fuse together.",
                "Unlike modern concrete or steel bridges that weaken with age and rust in the humid dampness, living root bridges grow stronger every single year! As the living tree matures, the roots thicken into stout timber cables capable of holding over fifty people simultaneously. Some bridges in Cherrapunji are more than five hundred years old, serving as living proof of ecological harmony."
            ],
            "vocabulary": [
                {
                    "word": "indigenous",
                    "definition": "Originating or occurring naturally in a particular place; native to a local culture.",
                    "example": "Indigenous knowledge helped the tribe survive in rainforest conditions."
                },
                {
                    "word": "pliable",
                    "definition": "Easily bent, flexible, and supple without breaking.",
                    "example": "Young rubber tree roots are pliable enough to be braided by hand."
                },
                {
                    "word": "chasm",
                    "definition": "A deep fissure or gap in the earth, rock, or valley floor.",
                    "example": "The bridge spans across a misty mountain chasm."
                },
                {
                    "word": "ecological",
                    "definition": "Relating to the relation of living organisms to one another and to their physical surroundings.",
                    "example": "The root bridges represent sustainable ecological design."
                }
            ]
        },
        "questions": [
            {
                "id": 1,
                "type": "mcq",
                "prompt": "What is the local Khasi name for the living root bridges of Meghalaya?",
                "options": [
                    "Jingkieng Jri",
                    "Cherrapunji Setu",
                    "Ficus Pulam",
                    "Jaintia Dwaar"
                ],
                "answer": 0,
                "evidenceParagraph": 0,
                "explanation": "Paragraph 1 mentions the bridges are 'locally known as Jingkieng Jri'."
            },
            {
                "id": 2,
                "type": "mcq",
                "prompt": "Which species of tree is trained to create these living bridges?",
                "options": [
                    "Banyan tree (Ficus benghalensis)",
                    "Indian rubber tree (Ficus elastica)",
                    "Teak wood tree (Tectona grandis)",
                    "Neem tree (Azadirachta indica)"
                ],
                "answer": 1,
                "evidenceParagraph": 2,
                "explanation": "Paragraph 3 notes: 'Along riverbanks grows the Ficus elastica, the Indian rubber tree.'"
            },
            {
                "id": 3,
                "type": "mcq",
                "prompt": "How do living root bridges compare to modern concrete or steel bridges over time?",
                "options": [
                    "Root bridges rot away within ten years",
                    "Root bridges grow stronger each year instead of rusting",
                    "Root bridges can only hold one child at a time",
                    "Root bridges require chemical paint every monsoon"
                ],
                "answer": 1,
                "evidenceParagraph": 3,
                "explanation": "Paragraph 4 explains: 'Unlike modern concrete or steel bridges that weaken with age and rust... living root bridges grow stronger every single year!'"
            },
            {
                "id": 4,
                "type": "typed",
                "prompt": "Approximately how many years does it take for a young living root bridge to grow and become usable?",
                "answer": "fifteen to twenty years",
                "keywords": ["15", "20", "fifteen", "twenty"],
                "evidenceParagraph": 2,
                "explanation": "Paragraph 3 states: 'Over fifteen to twenty years, the roots reach the opposite bank, take firm root in the soil, and fuse together.'"
            },
            {
                "id": 5,
                "type": "typed",
                "prompt": "What hollow tubes do Khasi elders use to guide the pliable tree roots across the river?",
                "answer": "betel nut trunks",
                "keywords": ["betel", "nut", "trunks"],
                "evidenceParagraph": 2,
                "explanation": "Paragraph 3 mentions: 'Elders hollow out betel nut trunks, place them horizontally across the chasm, and guide the young pliable roots'."
            }
        ]
    },

    "VII-ENG-06": {
        "title": "Inference Investigator",
        "class": "VII",
        "subject": "English",
        "skillArea": "Reading",
        "activity": "Reading Comprehension",
        "gameType": "Reading Comprehension",
        "passage": {
            "title": "Dr. APJ Abdul Kalam: The Missile Man and People's President",
            "topic": "Biography & Inspiring Lives",
            "genre": "Biographical Essay",
            "readingLevel": "Class VII",
            "estimatedTime": "5 min",
            "content": [
                "Avul Pakir Jainulabdeen Abdul Kalam was born in 1931 into a humble Tamil Muslim family in the pilgrimage town of Rameswaram, Tamil Nadu. His father was a boat owner who ferried Hindu pilgrims, while his mother was a devoted homemaker. To support his family during tough financial times, young Kalam woke up before dawn to distribute newspapers around town before heading off to school.",
                "Kalam possessed an insatiable hunger for mathematics and physics. After graduating in aerospace engineering from the Madras Institute of Technology, he joined the Defense Research and Development Organisation (DRDO) and later the Indian Space Research Organisation (ISRO). At ISRO, he served as the project director of India's first satellite launch vehicle, SLV-III, which successfully deployed the Rohini satellite into orbit in 1980.",
                "His visionary leadership subsequently led to the indigenous development of vital strategic missiles including Agni and Prithvi, earning him the affectionate title 'The Missile Man of India'. Yet, despite wielding monumental scientific influence, Dr. Kalam remained legendary for his austere simplicity, vegetarian diet, and love for Tamil poetry and the veena.",
                "In 2002, Kalam was elected the 11th President of India, winning overwhelming bipartisan support. Uniquely accessible, he opened the gates of Rashtrapati Bhavan to students, farmers, and underprivileged children, becoming known as the 'People's President'. Until his very last breath while delivering a lecture to students at IIM Shillong in 2015, Dr. Kalam championed a single lifelong message: 'Dream, dream, dream. Dreams transform into thoughts, and thoughts result in action.'"
            ],
            "vocabulary": [
                {
                    "word": "insatiable",
                    "definition": "Impossible to satisfy; having an unquenchable desire.",
                    "example": "He had an insatiable curiosity about how jet engines operate."
                },
                {
                    "word": "austere",
                    "definition": "Severe or strict in manner; extremely simple and plain without luxury.",
                    "example": "Despite his high office, he lived an austere life with few possessions."
                },
                {
                    "word": "bipartisan",
                    "definition": "Involving the agreement or cooperation of two political parties.",
                    "example": "The education bill passed with strong bipartisan approval."
                },
                {
                    "word": "accessible",
                    "definition": "Friendly and easy to talk to, approach, or reach.",
                    "example": "The President was admired for being genuinely accessible to ordinary citizens."
                }
            ]
        },
        "questions": [
            {
                "id": 1,
                "type": "mcq",
                "prompt": "What job did young Abdul Kalam do before school to support his family in Rameswaram?",
                "options": [
                    "Helped repair fishing boats",
                    "Distributed morning newspapers",
                    "Sold tea at the railway station",
                    "Carried luggage at the temple"
                ],
                "answer": 1,
                "evidenceParagraph": 0,
                "explanation": "Paragraph 1 states: 'young Kalam woke up before dawn to distribute newspapers around town before heading off to school.'"
            },
            {
                "id": 2,
                "type": "mcq",
                "prompt": "What major national milestone did Kalam accomplish as project director at ISRO in 1980?",
                "options": [
                    "Launched India's first mission to Mars",
                    "Successfully deployed Rohini satellite via SLV-III",
                    "Constructed the Vikram Sarabhai Space Centre",
                    "Designed India's first nuclear submarine"
                ],
                "answer": 1,
                "evidenceParagraph": 1,
                "explanation": "Paragraph 2 states: 'project director of India's first satellite launch vehicle, SLV-III, which successfully deployed the Rohini satellite into orbit in 1980.'"
            },
            {
                "id": 3,
                "type": "mcq",
                "prompt": "Why was Dr. Kalam widely remembered as the 'People's President' during his term?",
                "options": [
                    "He gave speeches exclusively on radio",
                    "He opened Rashtrapati Bhavan to students and underprivileged children",
                    "He lowered national taxes by royal decree",
                    "He traveled to every Indian village in an airplane"
                ],
                "answer": 1,
                "evidenceParagraph": 3,
                "explanation": "Paragraph 4 explains: 'Uniquely accessible, he opened the gates of Rashtrapati Bhavan to students, farmers, and underprivileged children, becoming known as the People's President.'"
            },
            {
                "id": 4,
                "type": "typed",
                "prompt": "What musical string instrument was Dr. Kalam known to play with deep passion?",
                "answer": "veena",
                "keywords": ["veena"],
                "evidenceParagraph": 2,
                "explanation": "Paragraph 3 notes his 'love for Tamil poetry and the veena'."
            },
            {
                "id": 5,
                "type": "typed",
                "prompt": "Complete Dr. Kalam's famous inspiring motto: 'Dreams transform into thoughts, and thoughts result in _____.'",
                "answer": "action",
                "keywords": ["action"],
                "evidenceParagraph": 3,
                "explanation": "Paragraph 4 concludes: 'Dreams transform into thoughts, and thoughts result in action.'"
            }
        ]
    },

    "VIII-ENG-09": {
        "title": "Reading Rally",
        "class": "VIII",
        "subject": "English",
        "skillArea": "Reading",
        "activity": "Reading Comprehension",
        "gameType": "Reading Comprehension",
        "passage": {
            "title": "The Mariana Trench: Journey into the Oceanic Abyss",
            "topic": "Oceanography & Extreme Science",
            "genre": "Scientific Essay",
            "readingLevel": "Class VIII",
            "estimatedTime": "5 min",
            "content": [
                "Beneath the sunlit waves of the western Pacific Ocean lies the most extreme frontier on Earth: the Mariana Trench. Formed by tectonic subduction where the massive Pacific plate slides underneath the smaller Mariana plate, this crescent-shaped crescent trench plunges nearly eleven kilometers down to the Challenger Deep.",
                "To grasp this astonishing depth, consider this: if Mount Everest, Earth's tallest peak, were placed at the base of the trench, its summit would still be submerged under more than two thousand meters of icy seawater. At the bottom, perpetual darkness reigns, with water temperatures hovering barely above freezing at one to four degrees Celsius.",
                "More daunting than cold or darkness is hydrostatic pressure. At eleven thousand meters depth, the weight of the water column exerts crushing pressure exceeding one thousand times atmospheric pressure at sea level—equivalent to balancing eight tons of weight on a single postage stamp! Ordinary submarines would be crushed in milliseconds.",
                "Remarkably, life does not merely endure here; it flourishes. Deep-sea submersibles have documented bizarre xenophyophores (giant single-celled organisms), translucent snailfish with flexible skulls, and amphipods containing unique anti-freezing proteins. These creatures survive without sunlight, feeding on organic 'marine snow' and chemosynthetic bacteria. Exploring the Mariana Trench proves that life adapts to the most unimaginable frontiers in the universe."
            ],
            "vocabulary": [
                {
                    "word": "subduction",
                    "definition": "The geological process where one tectonic plate moves under another tectonic plate and sinks into the mantle.",
                    "example": "Tectonic subduction created deep oceanic trenches and volcanic island arcs."
                },
                {
                    "word": "hydrostatic",
                    "definition": "Relating to the pressure exerted by a fluid at rest due to gravity.",
                    "example": "Deep-sea robots require titanium hulls to withstand hydrostatic force."
                },
                {
                    "word": "translucent",
                    "definition": "Allowing light, but not detailed shapes, to pass through; semi-transparent.",
                    "example": "The snailfish has a translucent body through which you can see its organs."
                },
                {
                    "word": "chemosynthetic",
                    "definition": "Relating to the biological conversion of chemical compounds into organic matter without sunlight.",
                    "example": "Chemosynthetic bacteria thrive near hydrothermal mineral vents."
                }
            ]
        },
        "questions": [
            {
                "id": 1,
                "type": "mcq",
                "prompt": "What geological process formed the Mariana Trench in the western Pacific Ocean?",
                "options": [
                    "A massive asteroid collision",
                    "Tectonic subduction between the Pacific and Mariana plates",
                    "Underwater volcanic eruptions building a caldera",
                    "Rapid glacial melting during the last Ice Age"
                ],
                "answer": 1,
                "evidenceParagraph": 0,
                "explanation": "Paragraph 1 explains: 'Formed by tectonic subduction where the massive Pacific plate slides underneath the smaller Mariana plate'."
            },
            {
                "id": 2,
                "type": "mcq",
                "prompt": "What would happen if Mount Everest were dropped into the Mariana Trench?",
                "options": [
                    "Its peak would stick out 1,000 meters into the air",
                    "Its peak would level exactly with the water surface",
                    "Its peak would still be submerged under more than two thousand meters of water",
                    "It would displace the entire ocean"
                ],
                "answer": 2,
                "evidenceParagraph": 1,
                "explanation": "Paragraph 2 states: 'if Mount Everest... were placed at the base of the trench, its summit would still be submerged under more than two thousand meters of icy seawater.'"
            },
            {
                "id": 3,
                "type": "mcq",
                "prompt": "How intense is the hydrostatic pressure at the bottom of the Challenger Deep?",
                "options": [
                    "About the same as a swimming pool",
                    "Ten times sea level pressure",
                    "Exceeding 1,000 times atmospheric pressure at sea level",
                    "Zero pressure because of the vacuum"
                ],
                "answer": 2,
                "evidenceParagraph": 2,
                "explanation": "Paragraph 3 notes: 'crushing pressure exceeding one thousand times atmospheric pressure at sea level—equivalent to balancing eight tons of weight on a single postage stamp!'"
            },
            {
                "id": 4,
                "type": "typed",
                "prompt": "What name is given to the falling organic debris from upper ocean layers that deep-sea animals feed on?",
                "answer": "marine snow",
                "keywords": ["marine", "snow"],
                "evidenceParagraph": 3,
                "explanation": "Paragraph 4 states that creatures feed on 'organic marine snow and chemosynthetic bacteria'."
            },
            {
                "id": 5,
                "type": "typed",
                "prompt": "What is the deepest known point of the Mariana Trench called?",
                "answer": "Challenger Deep",
                "keywords": ["challenger", "deep"],
                "evidenceParagraph": 0,
                "explanation": "Paragraph 1 mentions the trench 'plunges nearly eleven kilometers down to the Challenger Deep.'"
            }
        ]
    }
}
