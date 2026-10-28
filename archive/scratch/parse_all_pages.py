# Parse all 15 pages of OCR text from the provided PDF file
import re, json

PAGES_TEXT = """
1 5 English Listening Following Instructions & Announcements Carries out simple instructions such as ‘Shut the door’, ‘Bring me the book’, and such others 2026-09-25 20:16:00 1
2 5 English Listening Following Instructions & Announcements Listens to instructions and draws a picture 2026-09-25 20:16:00 1
3 5 English Listening Listening Comprehension & Response Listens to English words, greetings, polite forms of expression, simple sentences, and responds in English or the home language or ‘signing’ (using sign language) 2026-09-25 20:16:00 1
4 5 English Reading Phonics & Letter Recognition Differentiates between small and capital letters in print or Braille 2026-09-25 20:16:00 1
5 5 English Reading Phonics & Letter Recognition Produces words with common blends like ‘br’, ‘fr’ like ‘brother’, ‘frog’ etc. 2026-09-25 20:16:00 1
6 5 English Reading Phonics & Letter Recognition Recognises letters and their sounds A–Z 2026-09-25 20:16:00 1
7 5 English Reading Word Recognition Associates words with pictures 2026-09-25 20:16:00 1
8 5 English Speaking Oral Expression & Narration Responds orally (in any language including sign language) to comprehension questions related to stories/poems 2026-09-25 20:16:00 1
9 5 English Speaking Oral Expression & Narration Talks about self/situations/pictures in English 2026-09-25 20:16:00 1
10 5 English Speaking Questioning Identifies characters and sequence of a story and asks questions about the story 2026-09-25 20:16:00 1
11 5 English Speaking Recitation & Performance Recites poems/rhymes with actions 2026-09-25 20:16:00 1
12 5 English Vocabulary & Grammar Parts of Speech Uses nouns such as ‘boy’, ‘sun’, and prepositions like ‘in’, ‘on’, ‘under’, etc. 2026-09-25 20:16:00 1
13 5 English Vocabulary & Grammar Vocbulary Names familiar objects seen in the pictures 2026-09-25 20:16:00 1
14 5 English Writing Pre-writing Draws, scribbles in response to poems and stories 2026-09-25 20:16:00 1
15 5 English Writing Word, Sentence & Paragraph Writing Writes simple words like fan, hen, rat etc. 2026-09-25 20:16:00 1
16 5 Mathematics Data Handling Data Collection & Interpretation Collects, records (using pictures/numerals) and interprets simple information by looking at visuals 2026-09-25 20:16:00 1
17 5 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Length & Distance Estimates and measures short lengths using non-uniform units like a finger, hand span, length of a forearm, footsteps, etc. 2026-09-25 20:16:00 1
18 5 Mathematics Numbers & Operations Addition & SubtractionApplies addition and subtraction of numbers 1 to 20 in daily life – constructs addition facts up to 9 using concrete objects; subtracts numbers using 1 to 9; solves day-to-day problems related to addition and subtraction of numbers up to 9 2026-09-25 20:16:00 1
19 5 Mathematics Numbers & Operations Number Sense & Place Value Develops the concept of zero 2026-09-25 20:16:00 1
20 5 Mathematics Numbers & Operations Number Sense & Place Value Recites number names and counts objects up to 20, concretely, pictorially and symbolically 2026-09-25 20:16:00 1
21 5 Mathematics Numbers & Operations Number Sense & Place Value Recognises numbers up to 99 and writes numerals 2026-09-25 20:16:00 1
22 5 Mathematics Numbers & Operations Number Sense & Place Value Works with numbers 1 to 20 – counts objects using numbers 1 to 9; compares numbers up to 20 (e.g., tells whether the number of girls or boys is more in the class) 2026-09-25 20:16:00 1
23 5 Mathematics Patterns Number Patterns Observes, extends and creates patterns of shapes and numbers (e.g., 1,2,3,4,5…; 1,3,5…; 2,4,6…) 2026-09-25 20:16:00 1
24 5 Mathematics Shapes & Spatial Understanding 3D Shapes & Nets Describes the physical features of various solids/shapes in her own language (e.g., a ball rolls, a box slides) 2026-09-25 20:16:00 1
25 5 Mathematics Shapes & Spatial Understanding Classification of ObjectsClassifies objects into groups based on a few physical attributes such as shape, size and other observable properties including rolling and sliding 2026-09-25 20:16:00 1
26 6 English Listening Following Instructions & Announcements Listens to instructions and draws a picture 2026-09-25 20:16:00 1
27 6 English Listening Listening Comprehension & Response Listens to English words, greetings, polite forms of expression, and responds in English/home language like ‘How are you?’, ‘I’m fine, thank you.’ etc. 2026-09-25 20:16:00 1
28 6 English Listening Listening Comprehension & Response Listens to short texts from children’s section of newspapers, read out by the teacher 2026-09-25 20:16:00 1
29 6 English Reading Reading ComprehensionIdentifies characters and sequence of events in a story 2026-09-25 20:16:00 1
30 6 English Reading Reading ComprehensionResponds to comprehension questions related to stories and poems, in home language or English or sign language, orally and in writing (phrases/short sentences) 2026-09-25 20:16:00 1
31 6 English Speaking Questioning Expresses verbally her or his opinion and asks questions about the characters, storyline, etc., in English or home language 2026-09-25 20:16:00 1
32 6 English Speaking Recitation & Performance Sings songs or rhymes with action 2026-09-25 20:16:00 1
33 6 English Vocabulary & Grammar Parts of Speech Uses prepositions like ‘before’, ‘between’ etc. 2026-09-25 20:16:00 1
34 6 English Vocabulary & Grammar Parts of Speech Uses pronouns related to gender like ‘his/her’, ‘he/she’, ‘it’ and other pronouns like ‘this/that’, ‘here/there’, ‘these/those’ etc. 2026-09-25 20:16:00 1
35 6 English Vocabulary & Grammar Parts of Speech Uses simple adjectives related to size, shape, colour, weight, texture such as ‘big’, ‘small’, ‘round’, ‘pink’, ‘red’, ‘heavy’, ‘light’, ‘soft’ etc. 2026-09-25 20:16:00 1
36 6 English Writing Pre-writing Draws or writes a few words or short sentences in response to poems and stories 2026-09-25 20:16:00 1
37 6 English Writing Word, Sentence & Paragraph Writing Composes and writes simple, short sentences with space between words 2026-09-25 20:16:00 1
38 6 Mathematics Data Handling Data Collection & Interpretation Draws inference based on the data collected (e.g., the number of vehicles used in Samir’s house is more than that in Angelina’s) 2026-09-25 20:16:00 1
39 6 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Capacity & Volume Estimates and measures length/distances and capacities of containers using uniform non-standard units like a rod/pencil, cup/spoon/bucket etc. 2026-09-25 20:16:00 1
40 6 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Money Represents an amount up to Rs. 100 using 3–4 notes and coins (of same/different denominations) of play money 2026-09-25 20:16:00 1
41 6 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Time & Calendar Identifies the days of the week and months of the year 2026-09-25 20:16:00 1
42 6 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Time & Calendar Sequences events according to their duration in terms of hours/days (e.g., does a child remain in school for a longer period than at home?) 2026-09-25 20:16:00 1
43 6 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Weight Compares objects as heavier/lighter than, using a simple balance 2026-09-25 20:16:00 1
44 6 Mathematics Numbers & Operations Addition & SubtractionSolves simple daily life problems/situations based on addition and subtraction of two digit numbers 2026-09-25 20:16:00 1
45 6 Mathematics Numbers & Operations Number Sense & Place Value Works with two digit numbers – reads and writes numerals up to 99; uses place value in writing and comparing two digit numbers; forms the greatest and smallest two digit numbers (with and without repetition of digits) 2026-09-25 20:16:00 1
46 6 Mathematics Shapes & Spatial Understanding 2D Shapes & Lines Distinguishes between straight and curved lines; draws/represents straight lines in various orientations (vertical, horizontal, slant) 2026-09-25 20:16:00 1
47 6 Mathematics Shapes & Spatial Understanding 3D Shapes & Nets Describes basic 3D and 2D shapes with their observable characteristics – identifies cuboid, cylinder, cone and sphere by their names 2026-09-25 20:16:00 1
48 7 English Listening Listening Comprehension & Response Responds appropriately to oral messages/telephonic communication 2026-09-25 20:16:00 1
49 7 English Reading Environmental Print & Information Reads printed scripts on the classroom walls: poems, posters, charts etc. 2026-09-25 20:16:00 1
50 7 English Reading Reading Aloud & Fluency Reads aloud with appropriate pronunciation and pause 2026-09-25 20:16:00 1
51 7 English Reading Reading ComprehensionReads small texts in English with comprehension i.e., identifies main idea, details and sequence and draws conclusions in English 2026-09-25 20:16:00 1
52 7 English Speaking Oral Expression & Narration Expresses orally her/his opinion/understanding about the story and characters in the story, in English/home language 2026-09-25 20:16:00 1
53 7 English Speaking Recitation & Performance Performs in events such as role play/skit in English with appropriate expressions 2026-09-25 20:16:00 1
54 7 English Speaking Recitation & Performance Recites poems individually/in groups with correct pronunciation and intonation 2026-09-25 20:16:00 1
55 7 English Vocabulary & Grammar Parts of Speech Uses a variety of nouns, pronouns, adjectives and prepositions in context as compared to previous class 2026-09-25 20:16:00 1
56 7 English Vocabulary & Grammar Tenses Distinguishes between simple past and simple present tenses 2026-09-25 20:16:00 1
57 7 English Vocabulary & Grammar Vocbulary Identifies opposites like ‘day/night’, ‘close/open’, and such others 2026-09-25 20:16:00 1
58 7 English Vocabulary & Grammar Vocbulary Uses vocabulary related to subjects like Maths, EVS, relevant to Class III 2026-09-25 20:16:00 1
59 7 English Writing Dictation Writes/types dictation of words/phrases/sentences 2026-09-25 20:16:00 1
60 7 English Writing Mechanics & Punctuation Uses punctuation such as question mark, full stop and capital letters appropriately 2026-09-25 20:16:00 1
61 7 English Writing Word, Sentence & Paragraph Writing Uses meaningful short sentences in English, orally and in writing 2026-09-25 20:16:00 1
62 7 English Writing Word, Sentence & Paragraph Writing Writes 5–6 sentences in English on personal experiences/events using verbal or visual clues 2026-09-25 20:16:00 1
63 7 EVS Classification & Grouping Grouping by Features & Properties Groups objects, birds, animals, features and activities according to differences/similarities using different senses (appearance, place of living, food, movement, likes/dislikes) 2026-09-25 20:16:00 1
64 7 EVS Creative ExpressionDrawings, Models & Maps Creates drawings, designs, motifs, models, top/front/side views of objects, simple maps (of classroom, sections of home/school) and slogans, poems, etc. 2026-09-25 20:16:00 1
65 7 EVS Estimation, Experimentation & Recording Estimation & VerificationGuesses properties, estimates quantities of materials/activities in daily life and verifies using symbols/non-standard units (hand spans, spoons/mugs, etc.) 2026-09-25 20:16:00 1
66 7 EVS Estimation, Experimentation & Recording Recording & Predicting Patterns Records observations, experiences, information on objects/activities/places visited in different ways and predicts patterns (e.g., shapes of moon, seasons) 2026-09-25 20:16:00 1
67 7 EVS Explanation & Understanding Relationships Family & Community Describes roles of family members, family influences (traits/features/habits/practices), and need for living together, through oral/written/other ways 2026-09-25 20:16:00 1
68 7 EVS Explanation & Understanding Relationships Food & Water Describes need of food for people of different age groups, animals and birds; availability of food and water and use of water at home and surroundings 2026-09-25 20:16:00 1
69 7 EVS Mapping & Spatial Skills Map Reading & Directions Identifies directions, location of objects/places in simple maps (of home/classroom/school) using signs/symbols/verbally 2026-09-25 20:16:00 1
70 7 EVS Observation & Identification Animals & Birds Identifies simple features (movement, places found/kept, eating habits, sounds) of animals and birds in the immediate surroundings 2026-09-25 20:16:00 1
71 7 EVS Observation & Identification Family & RelationshipsIdentifies relationships with and among family members 2026-09-25 20:16:00 1
72 7 EVS Observation & Identification Plants Identifies simple observable features (shape, colour, texture, aroma) of leaves, trunk and bark of plants in immediate surroundings 2026-09-25 20:16:00 1
73 7 EVS Observation & Identification Surroundings (Objects, Places & Activities) Identifies objects, signs (vessels, stoves, transport, means of communication, signboards), places (types of houses/shelters, bus stand, petrol pump) and activities (work people do, cooking processes) at home/school/neighbourhood 2026-09-25 20:16:00 1
74 7 EVS Past & Present (Change over Time) Continuity & Change Differentiates between objects and activities of present and past (at the time of the elders) – clothes, vessels, games played, work done by people 2026-09-25 20:16:00 1
75 7 EVS Values, Sensitivity & Opinion Opinion on Social IssuesVoices opinion on good/bad touch, gender stereotypes for tasks/play/food in family, misuse/wastage of food and water in family and school 2026-09-25 20:16:00 1
76 7 EVS Values, Sensitivity & Opinion Rules & Cooperation Observes rules in games (local, indoor, outdoor) and other collective tasks 2026-09-25 20:16:00 1
77 7 EVS Values, Sensitivity & Opinion Sensitivity, Hygiene & Conservation Shows sensitivity for plants, animals, the elderly, differently abled and diverse family set-ups in surroundings 2026-09-25 20:16:00 1
78 7 Mathematics Data Handling Data Representation (Tables & Graphs) Records data using tally marks, represents pictorially and draws conclusions 2026-09-25 20:16:00 1
79 7 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Capacity & Volume Compares the capacity of different containers in terms of non-standard units 2026-09-25 20:16:00 1
80 7 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Length & Distance Estimates and measures length and distance using standard units like centimetres or metres and identifies relationships 2026-09-25 20:16:00 1
81 7 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Money Adds and subtracts small amounts of money with or without regrouping 2026-09-25 20:16:00 1
82 7 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Money Makes rate charts and simple bills 2026-09-25 20:16:00 1
83 7 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Time & Calendar Identifies a particular day and date on a calendar 2026-09-25 20:16:00 1
84 7 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Time & Calendar Reads the time correctly to the hour using a clock/watch 2026-09-25 20:16:00 1
85 7 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Weight Adds and subtracts measures involving grams and kilograms in life situations 2026-09-25 20:16:00 1
86 7 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Weight Weighs objects using standard units – grams and kilograms – using a simple balance 2026-09-25 20:16:00 1
87 7 Mathematics Numbers & Operations Addition & SubtractionSolves simple daily life problems using addition and subtraction of three digit numbers with and without regrouping, sums not exceeding 999 2026-09-25 20:16:00 1
88 7 Mathematics Numbers & Operations Estimation & Problem Solving Analyses and applies an appropriate number operation in the situation/context 2026-09-25 20:16:00 1
89 7 Mathematics Numbers & Operations Multiplication & DivisionConstructs and uses the multiplication facts (tables) of 2, 3, 4, 5 and 10 in daily life situations 2026-09-25 20:16:00 1
90 7 Mathematics Numbers & Operations Multiplication & DivisionExplains the meaning of division facts by equal grouping/sharing and finds it by repeated subtraction (e.g., 12 ÷ 3) 2026-09-25 20:16:00 1
91 7 Mathematics Numbers & Operations Number Sense & Place Value Works with three digit numbers – reads and writes numbers up to 999 using place value; compares numbers up to 999 based on place value 2026-09-25 20:16:00 1
92 7 Mathematics Patterns Number Patterns Extends patterns in simple shapes and numbers 2026-09-25 20:16:00 1
93 7 Mathematics Shapes & Spatial Understanding 2D Shapes & Lines Describes 2D shapes by the number of sides, corners and diagonals 2026-09-25 20:16:00 1
94 7 Mathematics Shapes & Spatial Understanding 2D Shapes & Lines Fills a given region leaving no gaps using a tile of a given shape 2026-09-25 20:16:00 1
95 7 Mathematics Shapes & Spatial Understanding 2D Shapes & Lines Identifies and makes 2D shapes by paper folding, paper cutting on the dot grid, using straight lines etc. 2026-09-25 20:16:00 1
96 8 English Listening Following Instructions & Announcements Responds to simple instructions, announcements in English made in class/school 2026-09-25 20:16:00 1
97 8 English Listening Listening Comprehension & Response Responds verbally/in writing in English to questions based on day-to-day life experiences, an article, story or poem heard or read 2026-09-25 20:16:00 1
98 8 English Reading Environmental Print & Information Reads printed script on the classroom walls, notice board, in posters and in advertisements 2026-09-25 20:16:00 1
99 8 English Reading Environmental Print & Information Reads subtitles on TV, titles of books, news headlines, pamphlets and advertisements 2026-09-25 20:16:00 1
100 8 English Reading Reading Aloud & Fluency Uses punctuation marks appropriately in reading aloud with intonation and pauses such as question mark, comma and full stop 2026-09-25 20:16:00 1
101 8 English Reading Reference Skills Uses dictionary to find out spelling and meaning 2026-09-25 20:16:00 1
102 8 English Reading Vocabulary in Context Infers the meaning of unfamiliar words by reading them in context 2026-09-25 20:16:00 1
103 8 English Speaking Oral Expression & Narration Describes briefly, orally/in writing, events, places and/or personal experiences in English 2026-09-25 20:16:00 1
104 8 English Speaking Oral Expression & Narration Presents orally and in writing the highlights of a given written text/short speech/narration/video, film, pictures, photograph etc. 2026-09-25 20:16:00 1
105 8 English Speaking Oral Expression & Narration Shares riddles and tongue-twisters in English 2026-09-25 20:16:00 1
106 8 English Speaking Oral Expression & Narration Speaks briefly on a familiar issue like conservation of water and experiences of day-to-day life like a visit to a zoo or going to a mela 2026-09-25 20:16:00 1
107 8 English Speaking Recitation & Performance Enacts different roles in short skits 2026-09-25 20:16:00 1
108 8 English Speaking Recitation & Performance Recites poems with appropriate expressions and intonation 2026-09-25 20:16:00 1
109 8 English Vocabulary & Grammar Linkers & Connectors Uses linkers to indicate connections between words and sentences such as ‘First’, ‘Next’, etc. 2026-09-25 20:16:00 1
110 8 English Vocabulary & Grammar Parts of Speech Uses nouns, verbs, adjectives and prepositions in speech and writing 2026-09-25 20:16:00 1
111 8 English Vocabulary & Grammar Vocbulary Solves simple crossword puzzles, builds word chains, etc. 2026-09-25 20:16:00 1
112 8 English Writing Dictation Writes/types dictation of short paragraphs (7–8 sentences) 2026-09-25 20:16:00 1
113 8 English Writing Functional Writing Writes informal letters or messages with a sense of audience 2026-09-25 20:16:00 1
114 8 English Writing Mechanics & Punctuation Uses punctuation marks appropriately in writing such as question mark, comma, full stop and capital letters 2026-09-25 20:16:00 1
115 8 EVS Classification & Grouping Grouping by Features & Properties Groups animals, birds, plants, objects, waste material by observable features, instincts, uses and traits 2026-09-25 20:16:00 1
116 8 EVS Creative ExpressionDrawings, Models & Maps Creates collage, designs, models, rangolis, posters, albums, and simple maps (of school/neighbourhood, flow diagrams, etc.) using local/waste material 2026-09-25 20:16:00 1
117 8 EVS Estimation, Experimentation & Recording Estimation & VerificationGuesses properties/conditions of phenomena, estimates spatial quantities (distance, weight, time, duration) in standard/local units and verifies using simple tools/set-ups to establish cause and effect (evaporation, condensation, dissolution, absorption) 2026-09-25 20:16:00 1
118 8 EVS Estimation, Experimentation & Recording Recording & Predicting Patterns Records observations/experiences/information for objects, activities, phenomena, places visited (mela, festival, historical place) in different ways and predicts patterns 2026-09-25 20:16:00 1
119 8 EVS Explanation & Understanding Relationships Animal Behaviour & Family Change Explains herd/group behaviour in animals (ants, bees, elephants), birds (building nests), and changes in family (due to birth, marriage, transfer, etc.) 2026-09-25 20:16:00 1
120 8 EVS Explanation & Understanding Relationships Food & Water Explains the process of producing and procuring daily needs (food, water, clothes) from source to home (e.g., crops from field to mandi to home, water purification) 2026-09-25 20:16:00 1
121 8 EVS Explanation & Understanding Relationships Work & Livelihood Describes different skilled work (farming, construction, art/craft, etc.), their inheritance (from elders) and training (role of institutions) in daily life 2026-09-25 20:16:00 1
122 8 EVS Mapping & Spatial Skills Map Reading & Directions Identifies signs, location of objects/places and guides for directions with respect to a landmark in school/neighbourhood using maps etc. 2026-09-25 20:16:00 1
123 8 EVS Mapping & Spatial Skills Using Signs & Information Uses the information on signboards, posters, currency (notes/coins), railway ticket/time table 2026-09-25 20:16:00 1
124 8 EVS Observation & Identification Animals & Birds Identifies different features (beaks/teeth, claws, ears, hair, nests/shelters, etc.) of birds and animals 2026-09-25 20:16:00 1
125 8 EVS Observation & Identification Family & RelationshipsIdentifies relationship with and among family members in extended family 2026-09-25 20:16:00 1
126 8 EVS Observation & Identification Plants Identifies simple features (shape, colour, aroma, where they grow) of flowers, roots and fruits in immediate surroundings 2026-09-25 20:16:00 1
127 8 EVS Past & Present (Change over Time) Continuity & Change Differentiates between objects and activities of past and present (transport, currency, houses, materials, tools, skills – farming, construction, etc.) 2026-09-25 20:16:00 1
128 8 EVS Values, Sensitivity & Opinion Opinion on Social IssuesVoices opinion on issues observed/experienced in family/school/neighbourhood – stereotypes, discriminatory practices, child rights (schooling, child abuse, punishment, labour) 2026-09-25 20:16:00 1
129 8 EVS Values, Sensitivity & Opinion Sensitivity, Hygiene & Conservation Suggests ways for hygiene, reduce, reuse, recycle and takes care of living beings (plants, animals, the elderly, differently abled) and resources (food, water, public property) 2026-09-25 20:16:00 1
130 8 Mathematics Data Handling Data Representation (Tables & Graphs) Represents the collected information in tables and bar graphs and draws inferences from these 2026-09-25 20:16:00 1
131 8 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Area & Perimeter Explores the area and perimeter of simple geometrical shapes (triangle, rectangle, square) in terms of a given shape as a unit 2026-09-25 20:16:00 1
132 8 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Estimation & Verification of Measures Estimates the length of an object/distance between two locations, weight of objects, volume of liquid, etc., and verifies them by actual measurement 2026-09-25 20:16:00 1
133 8 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Problem Solving with Measures Solves problems involving daily life situations related to length, distance, weight, volume and time involving four basic arithmetic operations 2026-09-25 20:16:00 1
134 8 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Time & Calendar Calculates time intervals/duration of familiar daily life events using forward or backward counting/addition and subtraction 2026-09-25 20:16:00 1
135 8 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Time & Calendar Reads clock time in hours and minutes and expresses the time in a.m. and p.m.; relates 24 hr clock with 12 hr clock 2026-09-25 20:16:00 1
136 8 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Unit Conversion Converts metre into centimetre and vice versa 2026-09-25 20:16:00 1
137 8 Mathematics Numbers & Operations Estimation & Problem Solving Creates and solves simple real life situations/problems including money, length, mass and capacity by using the four operations 2026-09-25 20:16:00 1
138 8 Mathematics Numbers & Operations Fractions & Decimals Identifies half, one-fourth, three-fourths of a whole in a given picture, by paper folding and in a collection of objects 2026-09-25 20:16:00 1
139 8 Mathematics Numbers & Operations Fractions & Decimals Represents fractions as half, one-fourth and three-fourths using numbers/numerals; shows the equivalence of a fraction with other fractions 2026-09-25 20:16:00 1
140 8 Mathematics Numbers & Operations Multiplication & DivisionDivides a number by another using different methods – pictorially (by drawing dots), equal grouping or repeated subtraction, and using the inter-relationship between division and multiplication 2026-09-25 20:16:00 1
141 8 Mathematics Numbers & Operations Multiplication & DivisionMultiplies 2 and 3 digit numbers 2026-09-25 20:16:00 1
142 8 Mathematics Patterns Number Patterns Identifies the pattern in multiplication and division (up to multiples of 9) 2026-09-25 20:16:00 1
143 8 Mathematics Patterns Shape & Geometric Patterns Observes, identifies and extends geometrical patterns based on symmetry 2026-09-25 20:16:00 1
144 8 Mathematics Shapes & Spatial Understanding 2D Shapes & Lines Identifies the centre, radius and diameter of a circle 2026-09-25 20:16:00 1
145 8 Mathematics Shapes & Spatial Understanding 3D Shapes & Nets Finds out shapes that can be used for tiling; makes cubes/cuboids using given nets 2026-09-25 20:16:00 1
146 8 Mathematics Shapes & Spatial Understanding Spatial Views Draws top view, front view and side view of simple objects 2026-09-25 20:16:00 1
147 8 Mathematics Shapes & Spatial Understanding Symmetry Shows the concept of symmetry by reflection through paper folding/paper cutting, ink blots, etc. 2026-09-25 20:16:00 1
148 9 English Listening Following Instructions & Announcements Acts according to instructions given in English, in games/sports, such as ‘Hit the ball!’, ‘Throw the ring.’, ‘Run to the finish line!’ etc. 2026-09-25 20:16:00 1
149 9 English Listening Listening Comprehension & Response Answers coherently in written or oral form to questions in English based on day-to-day life experiences, unfamiliar story, poem heard or read 2026-09-25 20:16:00 1
150 9 English Reading Critical Reading Connects ideas that he/she has inferred, through reading and interaction, with his/her personal experiences 2026-09-25 20:16:00 1
151 9 English Reading Environmental Print & Information Reads print in the surroundings (advertisements, directions, names of places etc.), understands and answers queries 2026-09-25 20:16:00 1
152 9 English Reading Extensive Reading Reads independently English storybooks, news items/headlines, advertisements etc., talks about them, and composes short paragraphs 2026-09-25 20:16:00 1
153 9 English Reading Reading ComprehensionReads text with comprehension, locates details and sequence of events 2026-09-25 20:16:00 1
154 9 English Reading Reference Skills Uses the dictionary for reference 2026-09-25 20:16:00 1
155 9 English Speaking Conversation & Polite Expressions Conducts short interviews of people around him/her e.g. grandparents, teachers, school librarian, gardener etc. 2026-09-25 20:16:00 1
156 9 English Speaking Oral Expression & Narration Appreciates, verbally/in writing, the variety in food, dress, customs and festivals as read/heard in day-to-day life, in storybooks, narratives, videos, films etc. 2026-09-25 20:16:00 1
157 9 English Speaking Oral Expression & Narration Writes and speaks on peace, equality etc. suggesting personal views 2026-09-25 20:16:00 1
158 9 English Speaking Recitation & Performance Recites and shares English songs, poems, games, riddles, stories, tongue twisters etc. with peers and family members 2026-09-25 20:16:00 1
159 9 English Vocabulary & Grammar Grammar in Use Uses meaningful grammatically correct sentences to describe and narrate incidents and for framing questions 2026-09-25 20:16:00 1
160 9 English Vocabulary & Grammar Tenses Identifies kinds of nouns, adverbs; differentiates between simple past and simple present verbs 2026-09-25 20:16:00 1
161 9 English Vocabulary & Grammar Vocbulary Uses synonyms such as ‘big/large’, ‘shut/close’, and antonyms like ‘inside/outside’, ‘light/dark’ from clues in context 2026-09-25 20:16:00 1
162 9 English Writing Creative Writing Attempts to write creatively (stories, poems, posters, etc.) 2026-09-25 20:16:00 1
163 9 English Writing Creative Writing Writes a ‘mini biography’ and ‘mini autobiography’ 2026-09-25 20:16:00 1
164 9 English Writing Dictation Takes dictation for different purposes, such as lists, paragraphs, dialogues etc. 2026-09-25 20:16:00 1
165 9 English Writing Functional Writing Writes informal letters, messages and e-mails 2026-09-25 20:16:00 1
166 9 English Writing Word, Sentence & Paragraph Writing Writes paragraphs in English from verbal, visual clues, with appropriate punctuation marks and linkers 2026-09-25 20:16:00 1
167 9 EVS Classification & Grouping Grouping by Features & Properties Groups objects, materials, activities by features and properties such as shape, taste, colour, texture, sound, traits etc. 2026-09-25 20:16:00 1
168 9 EVS Creative ExpressionDrawings, Models & Maps Creates posters, designs, models, set-ups, local dishes, sketches, maps (of neighbourhood/places visited) using local/waste material and writes poems/slogans/travelogue etc. 2026-09-25 20:16:00 1
169 9 EVS Estimation, Experimentation & Recording Estimation & VerificationGuesses properties/conditions of phenomena, estimates spatial quantities (distance, area, volume, weight) and time in simple standard units and verifies using simple tools/set-ups (floating, sinking, mixing, evaporation, germination, spoilage) 2026-09-25 20:16:00 1
170 9 EVS Estimation, Experimentation & Recording Recording & Predicting Patterns Records observations, experiences and information in an organised manner (tables, sketches, bar graphs, pie charts) and predicts patterns to establish cause and effect 2026-09-25 20:16:00 1
171 9 EVS Explanation & Understanding Relationships Animals & Birds Explains the super senses and unusual features (sight, smell, hearing, sleep, sound, etc.) of animals and their responses to light, sound, food etc. 2026-09-25 20:16:00 1
172 9 EVS Explanation & Understanding Relationships Food & Water Explains the use of technology and the process of accessing basic needs (food, water etc.) in daily life (farm produce to kitchen, preservation techniques, storage and tracking of water source) 2026-09-25 20:16:00 1
173 9 EVS Explanation & Understanding Relationships Institutions Explains the role and functions of different institutions in daily life (Bank, Panchayat, cooperatives, police station, etc.) 2026-09-25 20:16:00 1
174 9 EVS Explanation & Understanding Relationships Interdependence in Nature Describes the interdependence among animals, plants and humans (livelihoods from animals, dispersal of seeds etc.) 2026-09-25 20:16:00 1
175 9 EVS Explanation & Understanding Relationships Terrain, Climate & Culture Establishes linkages among terrain, climate, resources (food, water, shelter, livelihood) and cultural life (e.g., life in hot/cold deserts) 2026-09-25 20:16:00 1
176 9 EVS Mapping & Spatial Skills Map Reading & Directions Identifies signs, directions, location of objects/landmarks of a locality/place visited in maps and predicts directions in context of positions at different places 2026-09-25 20:16:00 1
177 9 EVS Past & Present (Change over Time) Continuity & Change Traces changes in practices, customs, techniques of past and present through coins, paintings, monuments, museums and interacting with elders 2026-09-25 20:16:00 1
178 9 EVS Values, Sensitivity & Opinion Opinion on Social IssuesVoices opinions on issues observed/experienced and relates them to larger issues of society (discrimination, migration/displacement, exclusion, child rights) 2026-09-25 20:16:00 1
179 9 EVS Values, Sensitivity & Opinion Sensitivity, Hygiene & Conservation Suggests ways for hygiene, health, managing waste, disaster/emergency situations and protecting/saving resources (land, fuels, forests), and shows sensitivity for the disadvantaged/deprived 2026-09-25 20:16:00 1
180 9 Mathematics Data Handling Data Representation (Tables & Graphs) Collects data related to various daily life situations, represents it in tabular form and as bar graphs and interprets it 2026-09-25 20:16:00 1
181 9 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Estimation & Verification of Measures Estimates the volume of a solid body in known units (e.g., volume of a bucket is about 20 times that of a mug) 2026-09-25 20:16:00 1
182 9 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Problem Solving with Measures Applies the four fundamental arithmetic operations in solving problems involving money, length, mass, capacity and time intervals 2026-09-25 20:16:00 1
183 9 Mathematics Measurement (Length, Weight, Capacity, Time, Money) Unit Conversion Relates commonly used larger and smaller units of length, weight and volume and converts larger units to smaller units and vice versa 2026-09-25 20:16:00 1
184 9 Mathematics Numbers & Operations Estimation & Problem Solving Estimates sum, difference, product and quotient of numbers and verifies them using different strategies 2026-09-25 20:16:00 1
185 9 Mathematics Numbers & Operations Fractions & Decimals Expresses fractions like 1/2, 1/4, 1/5 in decimal notation and vice versa (e.g., in units of length and money); converts fractions into decimals and vice versa 2026-09-25 20:16:00 1
186 9 Mathematics Numbers & Operations Fractions & Decimals Finds the number corresponding to part of a collection; identifies and forms equivalent fractions of a given fraction 2026-09-25 20:16:00 1
187 9 Mathematics Numbers & Operations Multiplication & DivisionPerforms four basic arithmetic operations on numbers beyond 1000 by understanding place value; divides a number by another using standard algorithms 2026-09-25 20:16:00 1
188 9 Mathematics Numbers & Operations Number Sense & Place Value Reads and writes numbers bigger than 1000 being used in her/his surroundings 2026-09-25 20:16:00 1
189 9 Mathematics Patterns Number Patterns Identifies the pattern in triangular numbers and square numbers 2026-09-25 20:16:00 1
190 9 Mathematics Shapes & Spatial Understanding 3D Shapes & Nets Makes cube, cylinder and cone using nets designed for this purpose 2026-09-25 20:16:00 1
191 9 Mathematics Shapes & Spatial Understanding Angles Classifies angles into right angle, acute angle, obtuse angle and represents them by drawing and tracing 2026-09-25 20:16:00 1
192 9 Mathematics Shapes & Spatial Understanding Symmetry Identifies 2D shapes from the immediate environment that have rotation and reflection symmetry like alphabets and shapes 2026-09-25 20:16:00 1
193 10 English Listening Following Instructions & Announcements Responds to announcements and instructions made in class, school assembly, railway station and in other public places 2026-09-25 20:16:00 1
194 10 English Listening Language Lab Visits a language laboratory 2026-09-25 20:16:00 1
195 10 English Listening Listening Comprehension & Response Responds to oral messages, telephonic communication in English and communicates them in English or home language 2026-09-25 20:16:00 1
196 10 English Reading Environmental Print & Information Reads to seek information from notice board, newspaper, Internet, tables, charts, diagrams and maps etc. 2026-09-25 20:16:00 1
197 10 English Reading Reading ComprehensionReads a variety of texts in English/Braille and identifies main ideas, characters, sequence of ideas and events and relates with his/her personal experiences 2026-09-25 20:16:00 1
198 10 English Reading Reading ComprehensionResponds to a variety of questions on familiar and unfamiliar texts verbally and in writing 2026-09-25 20:16:00 1
199 10 English Reading Reference Skills Refers to dictionary to check meaning and spelling, and to suggested websites for information 2026-09-25 20:16:00 1
200 10 English Speaking Oral Expression & Narration Uses meaningful sentences to describe/narrate factual/imaginary situations in speech and writing 2026-09-25 20:16:00 1
201 10 English Speaking Recitation & Performance Participates in activities in English like role play, group discussion, debate, etc. 2026-09-25 20:16:00 1
202 10 English Speaking Recitation & Performance Recites and shares poems, songs, jokes, riddles, tongue twisters, etc. 2026-09-25 20:16:00 1
203 10 English Vocabulary & Grammar Grammar in Use Writes grammatically correct sentences for a variety of situations, using noun, pronoun, verb, adverb, determiners, etc. 2026-09-25 20:16:00 1
204 10 English Vocabulary & Grammar Vocbulary Uses synonyms, antonyms appropriately; deduces word meanings from clues in context while reading a variety of texts 2026-09-25 20:16:00 1
205 10 English Writing Creative Writing Writes a book review 2026-09-25 20:16:00 1
206 10 English Writing Dictation Writes words/phrases/simple sentences and short paragraphs as dictated by the teacher 2026-09-25 20:16:00 1
207 10 English Writing Functional Writing Writes messages, invitations, short paragraphs and letters (formal and informal) with a sense of audience 2026-09-25 20:16:00 1
208 10 English Writing Word, Sentence & Paragraph Writing Drafts, revises and writes short paragraphs based on verbal, print and visual clues 2026-09-25 20:16:00 1
209 10 English Writing Word, Sentence & Paragraph Writing Writes coherently with focus on appropriate beginning, middle and end in English/Braille 2026-09-25 20:16:00 1
210 10 Mathematics Algebra Variables & Algebraic Expressions Uses variables with different operations to generalise a given situation (e.g., perimeter of a rectangle with sides x units and 3 units is 2(x+3) units) 2026-09-25 20:16:00 1
211 10 Mathematics Data Handling Data Representation & Interpretation Arranges given/collected information (e.g., family expenditure over six months) in the form of table, pictograph and bar graph and interprets them 2026-09-25 20:16:00 1
212 10 Mathematics Geometry 3D Shapes & Visualisation Identifies 3D objects like sphere, cube, cuboid, cylinder, cone from the surroundings; describes and gives examples of edges, vertices and faces 2026-09-25 20:16:00 1
213 10 Mathematics Geometry Basic Geometrical IdeasDescribes geometrical ideas like line, line segment, open and closed figures, angle, triangle, quadrilateral, circle, etc., with examples in surroundings 2026-09-25 20:16:00 1
214 10 Mathematics Geometry Lines & Angles Demonstrates an understanding of angles – identifies examples in surroundings, classifies angles by measure, estimates measures using 45°, 90° and 180° as reference 2026-09-25 20:16:00 1
215 10 Mathematics Geometry Quadrilaterals Classifies quadrilaterals into different groups/types on the basis of their sides/angles 2026-09-25 20:16:00 1
216 10 Mathematics Geometry Symmetry Demonstrates an understanding of line symmetry – identifies and creates symmetrical 2D shapes 2026-09-25 20:16:00 1
217 10 Mathematics Geometry Triangles & CongruenceClassifies triangles on the basis of their angles and sides (scalene, isosceles, equilateral) 2026-09-25 20:16:00 1
218 10 Mathematics Mensuration Perimeter & Area Finds out the perimeter and area of rectangular objects in the surroundings like floor of the classroom, surfaces of a chalk box etc. 2026-09-25 20:16:00 1
219 10 Mathematics Number System Factors, Multiples & Divisibility Applies HCF or LCM in a particular situation 2026-09-25 20:16:00 1
220 10 Mathematics Number System Factors, Multiples & Divisibility Recognises and appreciates (through patterns) the broad classification of numbers as even, odd, prime, co-prime, etc. 2026-09-25 20:16:00 1
221 10 Mathematics Number System Fractions, Decimals & Rational Numbers Solves problems on daily life situations involving addition and subtraction of fractions/decimals 2026-09-25 20:16:00 1
222 10 Mathematics Number System Fractions, Decimals & Rational Numbers Uses fractions and decimals in different situations which involve money, length, temperature etc. 2026-09-25 20:16:00 1
223 10 Mathematics Number System Integers Solves problems involving addition and subtraction of integers 2026-09-25 20:16:00 1
224 10 Mathematics Number System Whole Numbers & Operations Solves problems involving large numbers by applying appropriate operations (addition, subtraction, multiplication and division) 2026-09-25 20:16:00 1
225 10 Mathematics Ratio, Proportion & Commercial Arithmetic Ratio & Proportion Compares quantities using ratios in different situations (e.g., ratio of girls to boys in a class is 3:2) 2026-09-25 20:16:00 1
226 10 Mathematics Ratio, Proportion & Commercial Arithmetic Unitary Method Uses unitary method in solving various word problems 2026-09-25 20:16:00 1
227 10 Science Classification Classification of Materials, Organisms & Processes Classifies materials, organisms and processes based on observable properties (soluble/insoluble; transparent/translucent/opaque; reversible/irreversible changes; herbs, shrubs, trees, creepers, climbers; biotic/abiotic; rectilinear, circular, periodic motion) 2026-09-25 20:16:00 1
228 10 Science Environmental Awareness, Creativity & Values Creativity Exhibits creativity in designing, planning, making use of available resources, etc. 2026-09-25 20:16:00 1
229 10 Science Environmental Awareness, Creativity & Values Environmental ProtectionMakes efforts to protect environment (minimising wastage of food, water, electricity; rainwater harvesting; care for plants) 2026-09-25 20:16:00 1
230 10 Science Environmental Awareness, Creativity & Values Scientific Values Exhibits values of honesty, objectivity, cooperation, freedom from fear and prejudices 2026-09-25 20:16:00 1
231 10 Science Explaining Processes & Cause-Effect Cause–Effect Relationships Relates processes and phenomena with causes (deficiency diseases with diet; adaptations with habitats; air quality with pollutants) 2026-09-25 20:16:00 1
232 10 Science Explaining Processes & Cause-Effect Explaining Processes & Phenomena Explains processes and phenomena (processing of plant fibres, movements in plants and animals, formation of shadows, reflection from plane mirror, composition of air, preparation of vermicompost) 2026-09-25 20:16:00 1
233 10 Science Identification & Differentiation Differentiation Differentiates materials and organisms (fibre and yarn; tap and fibrous roots; electrical conductors and insulators) on the basis of properties, structure and functions 2026-09-25 20:16:00 1
234 10 Science Identification & Differentiation Identification Identifies materials and organisms, such as plant fibres and flowers, on the basis of observable features (appearance, texture, function, aroma) 2026-09-25 20:16:00 1
235 10 Science Measurement, Recording & Representation Labelled Diagrams & Flow Charts Draws labelled diagrams/flow charts of organisms and processes (parts of flowers, joints, filtration, water cycle) 2026-09-25 20:16:00 1
236 10 Science Measurement, Recording & Representation Measurement & Calculation Measures physical quantities and expresses them in SI units (e.g., length) 2026-09-25 20:16:00 1
237 10 Science Models & Application in Daily Life Application of Concepts in Daily Life Applies learning of scientific concepts in day-to-day life (balanced diet, separating materials, season-appropriate fabrics, compass for directions, coping with heavy rain/drought) 2026-09-25 20:16:00 1
238 10 Science Models & Application in Daily Life Model Construction Constructs models using materials from surroundings and explains their working (pinhole camera, periscope, electric torch) 2026-09-25 20:16:00 1
239 10 Science Scientific Inquiry & Investigation Conducting Investigations Conducts simple investigations to seek answers to queries (e.g., nutrients in animal fodder; can all physical changes be reversed; does a freely suspended magnet align in a particular direction) 2026-09-25 20:16:00 1
240 10 Social Science Geography Earth & the Solar SystemDemonstrates day and night and seasons 2026-09-25 20:16:00 1
241 10 Social Science Geography Earth & the Solar SystemDistinguishes between stars, planets and satellites (Sun, Earth and Moon) 2026-09-25 20:16:00 1
242 10 Social Science Geography Earth & the Solar SystemExamines critically the superstitions related to eclipses 2026-09-25 20:16:00 1
243 10 Social Science Geography Earth & the Solar SystemRecognises that the earth is a unique celestial body due to existence of life, zones of the earth with special reference to biosphere 2026-09-25 20:16:00 1
244 10 Social Science Geography Maps, Globe & Diagrams Draws a neighbourhood map showing scale, direction and features using conventional symbols 2026-09-25 20:16:00 1
245 10 Social Science Geography Maps, Globe & Diagrams Identifies latitudes and longitudes (poles, equator, tropics), States/UTs of India and neighbouring countries on globe and world map 2026-09-25 20:16:00 1
246 10 Social Science Geography Maps, Globe & Diagrams Locates directions on a flat surface and continents and oceans on the world map 2026-09-25 20:16:00 1
247 10 Social Science Geography Maps, Globe & Diagrams Locates physical features of India (mountains, plateaus, plains, rivers, desert) on the map of India 2026-09-25 20:16:00 1
248 10 Social Science History Ancient India Explains broad developments during the ancient period (hunting–gathering, beginning of agriculture, first cities on the Indus) and relates developments in one place with another 2026-09-25 20:16:00 1
249 10 Social Science History Ancient India Lists significant contributions of important kingdoms and dynasties (Ashokan inscriptions, Gupta coins, Ratha temples by Pallavas) 2026-09-25 20:16:00 1
250 10 Social Science History Ancient India Locates important historical sites and places on an outline map of India 2026-09-25 20:16:00 1
251 10 Social Science History Ancient India Recognises distinctive features of early human cultures and explains their growth 2026-09-25 20:16:00 1
252 10 Social Science History Ancient India Synthesises information related to various historical developments 2026-09-25 20:16:00 1
253 10 Social Science History Art, Architecture & Culture Describes issues, events, personalities mentioned in literary works of the time 2026-09-25 20:16:00 1
254 10 Social Science History Art, Architecture & Culture Describes the implications of India’s contacts with regions outside India in religion, art, architecture, etc. 2026-09-25 20:16:00 1
255 10 Social Science History Art, Architecture & Culture Outlines India’s significant contributions in culture and science (astronomy, medicine, mathematics, knowledge of metals) 2026-09-25 20:16:00 1
256 10 Social Science History Religious Ideas & Movements Analyses basic ideas and values of various religions and systems of thought during the ancient period 2026-09-25 20:16:00 1
257 10 Social Science History Sources of History Identifies different types of sources (archaeological, literary etc.) and describes their use in reconstructing history of this period 2026-09-25 20:16:00 1
258 10 Social Science Social & Political Life (Civics & Economics) Diversity & Discrimination Describes various forms of human diversity around her/him and develops a healthy attitude towards diversity 2026-09-25 20:16:00 1
259 10 Social Science Social & Political Life (Civics & Economics) Diversity & Discrimination Differentiates between equality and inequality in various forms to treat them in a healthy way 2026-09-25 20:16:00 1
260 10 Social Science Social & Political Life (Civics & Economics) Diversity & Discrimination Recognises various forms of discrimination and understands the nature and sources of discrimination 2026-09-25 20:16:00 1
261 10 Social Science Social & Political Life (Civics & Economics) Government Describes the functioning of rural and urban local government bodies in sectors like health and education 2026-09-25 20:16:00 1
262 10 Social Science Social & Political Life (Civics & Economics) Government Describes the role of government, especially at the local level; identifies levels of government – local, state and union 2026-09-25 20:16:00 1
263 10 Social Science Social & Political Life (Civics & Economics) Markets, Economy & Public Facilities Describes factors responsible for availability of different occupations in rural and urban areas 2026-09-25 20:16:00 1
264 11 English Listening Following Instructions & Announcements Responds to different kinds of instructions, requests, directions in varied contexts viz. school, bank, railway station 2026-09-25 20:16:00 1
265 11 English Listening Language Lab Visits a language laboratory 2026-09-25 20:16:00 1
266 11 English Listening Media & Public ListeningSpeaks about excerpts, dialogues, skits, short films, news and debate on TV and radio, audio–video programmes on suggested websites 2026-09-25 20:16:00 1
267 11 English Reading Critical Reading Thinks critically, compares and contrasts characters, events, ideas, themes and relates them to life 2026-09-25 20:16:00 1
268 11 English Reading Environmental Print & Information Reads to seek information in print/online, notice board, signboards in public places, newspaper, hoardings etc. 2026-09-25 20:16:00 1
269 11 English Reading Extensive Reading Reads a variety of texts for pleasure e.g. adventure stories, science fiction, fairy tales, biography, autobiography, travelogue etc. (extensive reading) 2026-09-25 20:16:00 1
270 11 English Reading Reading ComprehensionAnswers questions orally and in writing on a variety of texts 2026-09-25 20:16:00 1
271 11 English Reading Reading ComprehensionIdentifies details, characters, main idea and sequence of ideas and events in textual/non-textual material 2026-09-25 20:16:00 1
272 11 English Reading Reading ComprehensionReads textual/non-textual materials in English/Braille with comprehension 2026-09-25 20:16:00 1
273 11 English Speaking Questioning Asks and responds to questions based on texts (from books or other resources) and out of curiosity 2026-09-25 20:16:00 1
274 11 English Speaking Recitation & Performance Engages in conversations in English with family, friends, and people from different professions such as shopkeeper, salesperson etc. using appropriate vocabulary 2026-09-25 20:16:00 1
275 11 English Speaking Recitation & Performance Participates in different activities in English such as role play, poetry recitation, skit, drama, debate, speech, elocution, declamation, quiz, etc. 2026-09-25 20:16:00 1
276 11 English Speaking Recitation & Performance Reads aloud stories and recites poems with appropriate pause, intonation and pronunciation 2026-09-25 20:16:00 1
277 11 English Vocabulary & Grammar Grammar in Use Uses appropriate grammatical forms in communication (e.g. noun, pronoun, verb, determiners, time and tense, passivisation, adjective, adverb, etc.) 2026-09-25 20:16:00 1
278 11 English Vocabulary & Grammar Vocbulary Infers the meaning of unfamiliar words by reading them in context 2026-09-25 20:16:00 1
279 11 English Vocabulary & Grammar Vocbulary Refers dictionary, thesaurus and encyclopedia to find meanings/spelling of words while reading and writing 2026-09-25 20:16:00 1
280 11 English Writing Creative Writing Writes a book review 2026-09-25 20:16:00 1
281 11 English Writing Creative Writing Writes descriptions/narratives showing sensitivity to gender, environment and appreciation of cultural diversity 2026-09-25 20:16:00 1
282 11 English Writing Creative Writing Writes dialogues from a story and story from dialogues 2026-09-25 20:16:00 1
283 11 English Writing Functional Writing Writes formal letters, personal diary, list, email, SMS, etc. 2026-09-25 20:16:00 1
284 11 English Writing Note Taking Takes notes while teacher teaches/from books/from online materials 2026-09-25 20:16:00 1
285 11 English Writing Word, Sentence & Paragraph Writing Organises sentences coherently in English/Braille with the help of verbal and visual clues and with a sense of audience 2026-09-25 20:16:00 1
286 11 Mathematics Algebra Linear Equations Represents daily life situations in the form of a simple equation and solves it 2026-09-25 20:16:00 1
287 11 Mathematics Algebra Variables & Algebraic Expressions Adds/subtracts algebraic expressions 2026-09-25 20:16:00 1
288 11 Mathematics Data Handling Data Representation & Interpretation Interprets data using bar graphs (e.g., electricity consumption in winter vs summer, runs scored in first 10 overs) 2026-09-25 20:16:00 1
289 11 Mathematics Data Handling Measures of Central Tendency Finds representative values for simple data from daily life contexts like mean, median and mode 2026-09-25 20:16:00 1
290 11 Mathematics Data Handling Probability & Chance Recognises variability in real life situations (e.g., heights of students) and uncertainty in happening of events like throwing a coin 2026-09-25 20:16:00 1
291 11 Mathematics Geometry Constructions Using ruler and compasses, constructs a line parallel to a given line from a point outside it, and triangles 2026-09-25 20:16:00 1
292 11 Mathematics Geometry Lines & Angles Classifies pairs of angles as linear, supplementary, complementary, adjacent and vertically opposite, and finds the value of one when the other is given 2026-09-25 20:16:00 1
293 11 Mathematics Geometry Lines & Angles Verifies the properties of pairs of angles formed when a transversal cuts two lines 2026-09-25 20:16:00 1
294 11 Mathematics Geometry Triangles & CongruenceExplains congruency of triangles on the basis of information given (SSS, SAS, ASA, RHS) 2026-09-25 20:16:00 1
295 11 Mathematics Geometry Triangles & CongruenceFinds unknown angle of a triangle when its two angles are known 2026-09-25 20:16:00 1
296 11 Mathematics Mensuration Perimeter & Area Calculates areas of the regions enclosed in a rectangle and a square 2026-09-25 20:16:00 1
297 11 Mathematics Mensuration Perimeter & Area Finds approximate area of closed shapes using unit square grid/graph sheet 2026-09-25 20:16:00 1
298 11 Mathematics Number System Exponents, Squares & Roots Uses exponential form of numbers to simplify problems involving multiplication and division of large numbers 2026-09-25 20:16:00 1
299 11 Mathematics Number System Fractions, Decimals & Rational Numbers Interprets the division and multiplication of fractions 2026-09-25 20:16:00 1
300 11 Mathematics Number System Fractions, Decimals & Rational Numbers Solves problems related to daily life situations involving rational numbers 2026-09-25 20:16:00 1
301 11 Mathematics Number System Fractions, Decimals & Rational Numbers Uses algorithms to multiply and divide fractions/decimals 2026-09-25 20:16:00 1
302 11 Mathematics Number System Integers Multiplies/divides two integers 2026-09-25 20:16:00 1
303 11 Mathematics Ratio, Proportion & Commercial Arithmetic Percentage, Profit & Loss, Interest Calculates profit/loss percent and rate percent in simple interest 2026-09-25 20:16:00 1
304 11 Mathematics Ratio, Proportion & Commercial Arithmetic Percentage, Profit & Loss, Interest Solves problems related to conversion of percentage to fraction and decimal and vice versa 2026-09-25 20:16:00 1
305 11 Mathematics Ratio, Proportion & Commercial Arithmetic Ratio & Proportion Distinguishes quantities that are in proportion (e.g., 15, 45, 40, 120) 2026-09-25 20:16:00 1
306 11 Science Classification Classification of Materials, Organisms & Processes Classifies materials and organisms based on properties/characteristics (plant and animal fibres; physical and chemical changes) 2026-09-25 20:16:00 1
307 11 Science Environmental Awareness, Creativity & Values Creativity Exhibits creativity in designing, planning, making use of available resources, etc. 2026-09-25 20:16:00 1
308 11 Science Environmental Awareness, Creativity & Values Environmental ProtectionMakes efforts to protect environment (sanitation in public places, minimising pollutants, planting trees, sensitising others on overconsumption) 2026-09-25 20:16:00 1
309 11 Science Environmental Awareness, Creativity & Values Scientific Values Exhibits values of honesty, objectivity, cooperation, freedom from fear and prejudices 2026-09-25 20:16:00 1
310 11 Science Explaining Processes & Cause-Effect Cause–Effect Relationships Relates processes and phenomena with causes (wind speed with air pressure; crops with soil types; depletion of water table with human activities) 2026-09-25 20:16:00 1
311 11 Science Explaining Processes & Cause-Effect Chemical Word Equations Writes word equations for chemical reactions (acid-base reactions, corrosion, photosynthesis, respiration) 2026-09-25 20:16:00 1
312 11 Science Explaining Processes & Cause-Effect Explaining Processes & Phenomena Explains processes and phenomena (processing of animal fibres, modes of heat transfer, organs and systems in humans and plants, heating and magnetic effects of electric current) 2026-09-25 20:16:00 1
313 11 Science Identification & Differentiation Differentiation Differentiates materials and organisms (digestion in different organisms; unisexual and bisexual flowers; conductors and insulators of heat; acidic, basic and neutral substances; images by mirrors and lenses) on the basis of properties, structure and function 2026-09-25 20:16:00 1
314 11 Science Identification & Differentiation Identification Identifies materials and organisms (animal fibres, types of teeth, mirrors and lenses) on the basis of observable features 2026-09-25 20:16:00 1
315 11 Science Measurement, Recording & Representation Graphs Plots and interprets graphs (e.g., distance–time graph) 2026-09-25 20:16:00 1
316 11 Science Measurement, Recording & Representation Labelled Diagrams & Flow Charts Draws labelled diagrams/flow charts (organ systems, electric circuits, experimental set-ups, life cycle of silk moth) 2026-09-25 20:16:00 1
317 11 Science Measurement, Recording & Representation Measurement & Calculation Measures and calculates temperature, pulse rate, speed of moving objects, time period of a simple pendulum, etc. 2026-09-25 20:16:00 1
318 11 Science Models & Application in Daily Life Application of Concepts in Daily Life Applies learning of scientific concepts in day-to-day life (dealing with acidity, testing and treating soil, preventing corrosion, vegetative propagation, connecting cells, disaster measures, treating polluted water) 2026-09-25 20:16:00 1
319 11 Science Models & Application in Daily Life History of Scientific Discoveries Discusses and appreciates stories of scientific discoveries 2026-09-25 20:16:00 1
320 11 Science Models & Application in Daily Life Model Construction Constructs models using materials from surroundings and explains their working (stethoscope, anemometer, electromagnet, Newton’s colour disc) 2026-09-25 20:16:00 1
321 11 Science Scientific Inquiry & Investigation Conducting Investigations Conducts simple investigations to seek answers to queries (flower extract as acid-base indicator; photosynthesis in non-green leaves; is white light composed of many colours) 2026-09-25 20:16:00 1
322 11 Social Science Geography Disasters & Management Explains preventive actions to be undertaken in the event of disasters (earthquake, floods, droughts) 2026-09-25 20:16:00 1
323 11 Social Science Geography Disasters & Management Reflects on the factors leading to disasters and calamities 2026-09-25 20:16:00 1
324 11 Social Science Geography Earth's Interior, Landforms & Atmosphere Describes formation of landforms due to various factors 2026-09-25 20:16:00 1
325 11 Social Science Geography Earth's Interior, Landforms & Atmosphere Explains composition and structure of the atmosphere 2026-09-25 20:16:00 1
326 11 Social Science Geography Earth's Interior, Landforms & Atmosphere Identifies major layers of the earth’s interior, rock types and layers of the atmosphere in a diagram 2026-09-25 20:16:00 1
327 11 Social Science Geography Environment & Natural Resources Analyses factors contributing to pollution in surroundings and lists measures to prevent it 2026-09-25 20:16:00 1
328 11 Social Science Geography Environment & Natural Resources Describes different components of the environment and the interrelationship between them 2026-09-25 20:16:00 1
329 11 Social Science Geography Environment & Natural Resources Reasons out factors leading to diversity in flora and fauna (climate, landforms) 2026-09-25 20:16:00 1
330 11 Social Science Geography Environment & Natural Resources Shows sensitivity to the need for conservation of natural resources – air, water, energy, flora and fauna 2026-09-25 20:16:00 1
331 11 Social Science Geography Human Geography & Development Analyses factors that impact development of specific regions 2026-09-25 20:16:00 1
332 11 Social Science Geography Human Geography & Development Draws interrelationship between climatic regions and life of people in different climatic regions of the world, including India 2026-09-25 20:16:00 1
333 11 Social Science Geography Maps, Globe & Diagrams Locates distribution and extent of different climatic regions on the world map or globe 2026-09-25 20:16:00 1
334 11 Social Science History Art, Architecture & Culture Describes distinctive developments in style and technology used for construction of temples, tombs and mosques 2026-09-25 20:16:00 1
335 11 Social Science History Medieval India Analyses administrative measures and strategies for military control adopted by different kingdoms (Khaljis, Tughluqs, Mughals) 2026-09-25 20:16:00 1
336 11 Social Science History Medieval India Analyses socio-political and economic changes during the medieval period 2026-09-25 20:16:00 1
337 11 Social Science History Medieval India Draws comparisons between policies of different rulers 2026-09-25 20:16:00 1
338 11 Social Science History Medieval India Explains the relationship between livelihood patterns and geographical conditions (tribes, nomadic pastoralists, banjaras) 2026-09-25 20:16:00 1
339 11 Social Science History Medieval India Relates key historical developments during the medieval period in one place with another 2026-09-25 20:16:00 1
340 11 Social Science History Religious Ideas & Movements Analyses factors which led to the emergence of new religious ideas and movements (bhakti and sufi) 2026-09-25 20:16:00 1
341 11 Social Science History Religious Ideas & Movements Draws inferences from poetry of bhakti and sufi saints about the existing social order 2026-09-25 20:16:00 1
342 11 Social Science History Sources of History Provides examples of sources used to study various periods in history 2026-09-25 20:16:00 1
343 11 Social Science Social & Political Life (Civics & Economics) Constitution, Rights & Laws Explains the significance of equality in democracy; distinguishes between political, economic and social equality 2026-09-25 20:16:00 1
344 11 Social Science Social & Political Life (Civics & Economics) Constitution, Rights & Laws Interprets social, political and economic issues in one’s own region with reference to the right to equality 2026-09-25 20:16:00 1
345 11 Social Science Social & Political Life (Civics & Economics) Elections & Constituencies Differentiates between local government and State government; describes the process of election to the legislative assembly 2026-09-25 20:16:00 1
346 11 Social Science Social & Political Life (Civics & Economics) Elections & Constituencies Locates one’s own constituency on the assembly constituency map of State/UT and names local MLA 2026-09-25 20:16:00 1
347 11 Social Science Social & Political Life (Civics & Economics) Gender Analyses causes and consequences of disadvantages faced by women; identifies women achievers and illustrates their contributions 2026-09-25 20:16:00 1
348 11 Social Science Social & Political Life (Civics & Economics) Markets, Economy & Public Facilities Differentiates between different kinds of markets; traces how goods travel through various market places 2026-09-25 20:16:00 1
349 11 Social Science Social & Political Life (Civics & Economics) Media & Advertising Explains the functioning of media with examples from newspapers; creates an advertisement 2026-09-25 20:16:00 1
350 12 English Listening Following Instructions & Announcements Responds to instructions and announcements in school and public places viz. railway station, market, airport, cinema hall, and acts accordingly 2026-09-25 20:16:00 1
351 12 English Listening Language Lab Visits a language laboratory 2026-09-25 20:16:00 1
352 12 English Listening Media & Public ListeningReads excerpts, dialogues, poems, commentaries of sports and games, speeches, news, debates on TV, radio and expresses opinions about them 2026-09-25 20:16:00 1
353 12 English Reading Critical Reading Interprets quotations, sayings and proverbs 2026-09-25 20:16:00 1
354 12 English Reading Critical Reading Reads, compares, contrasts, thinks critically and relates ideas to life 2026-09-25 20:16:00 1
355 12 English Reading Extensive Reading Reads a variety of texts for pleasure e.g. adventure stories, science fiction, fairy tales, non-fiction articles, narratives, travelogues, biographies, etc. (extensive reading) 2026-09-25 20:16:00 1
356 12 English Reading Reading ComprehensionIdentifies details, characters, main idea and sequence of ideas and events while reading 2026-09-25 20:16:00 1
357 12 English Reading Reading ComprehensionReads textual/non-textual materials in English/Braille with comprehension 2026-09-25 20:16:00 1
358 12 English Speaking Conversation & Polite Expressions Introduces guests in English, interviews people by asking questions based on the work they do 2026-09-25 20:16:00 1
359 12 English Speaking Conversation & Polite Expressions Uses formulaic/polite expressions to communicate such as ‘May I borrow your book?’, ‘I would like to differ’ etc. 2026-09-25 20:16:00 1
360 12 English Speaking Oral Expression & Narration Narrates stories (real or imaginary) and real life experiences in English 2026-09-25 20:16:00 1
361 12 English Speaking Oral Expression & Narration Speaks about objects/events in the class/school environment and outside surroundings 2026-09-25 20:16:00 1
362 12 English Speaking Oral Expression & Narration Speaks short prepared speech in morning assembly 2026-09-25 20:16:00 1
363 12 English Speaking Questioning Asks questions in different contexts and situations (based on the text/beyond the text/out of curiosity/while engaging in conversation) using appropriate vocabulary and accurate sentences 2026-09-25 20:16:00 1
364 12 English Speaking Recitation & Performance Engages in conversations in English with people from different professions such as bank staff, railway staff, etc. using appropriate vocabulary 2026-09-25 20:16:00 1
365 12 English Speaking Recitation & Performance Participates in different events such as role play, poetry recitation, skit, drama, debate, speech, elocution, declamation, quiz, etc. 2026-09-25 20:16:00 1
366 12 English Vocabulary & Grammar Grammar in Use Communicates accurately using appropriate grammatical forms (e.g., clauses, comparison of adjectives, time and tense, active/passive voice, reported speech etc.) 2026-09-25 20:16:00 1
367 12 English Vocabulary & Grammar Grammar in Use Participates in grammar games and kinaesthetic activities for language learning 2026-09-25 20:16:00 1
368 12 English Vocabulary & Grammar Vocbulary Infers the meaning of unfamiliar words by reading them in context 2026-09-25 20:16:00 1
369 12 English Vocabulary & Grammar Vocbulary Refers dictionary, thesaurus and encyclopedia as reference books for meaning and spelling while reading and writing 2026-09-25 20:16:00 1
370 12 English Writing Answer Writing Writes answers to textual/non-textual questions after comprehension/inference; draws character sketch, attempts extrapolative writing 2026-09-25 20:16:00 1
371 12 English Writing Creative Writing Develops a skit (dialogues from a story) and story from dialogues 2026-09-25 20:16:00 1
372 12 English Writing Creative Writing Writes a book review 2026-09-25 20:16:00 1
373 12 English Writing Functional Writing Prepares a write-up after seeking information in print/online, notice board, newspaper, etc. 2026-09-25 20:16:00 1
374 12 English Writing Functional Writing Writes email, messages, notice, formal letters, descriptions/narratives, personal diary, report, short personal/biographical experiences etc. 2026-09-25 20:16:00 1
375 12 English Writing Word, Sentence & Paragraph Writing Writes a coherent and meaningful paragraph through the process of drafting, revising, editing and finalising 2026-09-25 20:16:00 1
376 12 English Writing Word, Sentence & Paragraph Writing Writes short paragraphs coherently in English/Braille with a proper beginning, middle and end with appropriate punctuation marks 2026-09-25 20:16:00 1
377 12 Mathematics Algebra Algebraic Identities Uses various algebraic identities in solving problems of daily life 2026-09-25 20:16:00 1
378 12 Mathematics Algebra Variables & Algebraic Expressions Multiplies algebraic expressions (e.g., expands (2x-5)(3x²+7)) 2026-09-25 20:16:00 1
379 12 Mathematics Algebra Variables & Algebraic Expressions Solves puzzles and daily life problems using variables 2026-09-25 20:16:00 1
380 12 Mathematics Data Handling Data Representation & Interpretation Draws and interprets bar charts and pie charts 2026-09-25 20:16:00 1
381 12 Mathematics Data Handling Probability & Chance Makes hypotheses on chances of future events on the basis of earlier occurrences or available data (e.g., repeated throws of dice and coins) 2026-09-25 20:16:00 1
382 12 Mathematics Geometry 3D Shapes & Visualisation Represents 3D shapes on a plane surface such as sheet of paper, blackboard etc. 2026-09-25 20:16:00 1
383 12 Mathematics Geometry 3D Shapes & Visualisation Verifies Euler’s relation through pattern 2026-09-25 20:16:00 1
384 12 Mathematics Geometry Constructions Constructs different quadrilaterals using compasses and straight edge 2026-09-25 20:16:00 1
385 12 Mathematics Geometry Quadrilaterals Solves problems related to angles of a quadrilateral using angle sum property 2026-09-25 20:16:00 1
386 12 Mathematics Geometry Quadrilaterals Verifies properties of parallelograms and establishes the relationship between them through reasoning 2026-09-25 20:16:00 1
387 12 Mathematics Mensuration Perimeter & Area Estimates the area of shapes like trapezium and other polygons using square grid/graph sheet and verifies using formulas 2026-09-25 20:16:00 1
388 12 Mathematics Mensuration Perimeter & Area Finds the area of a polygon 2026-09-25 20:16:00 1
389 12 Mathematics Mensuration Surface Area & VolumeFinds surface area and volume of cuboidal and cylindrical objects 2026-09-25 20:16:00 1
390 12 Mathematics Number System Exponents, Squares & Roots Finds squares, cubes, square roots and cube roots of numbers using different methods 2026-09-25 20:16:00 1
391 12 Mathematics Number System Exponents, Squares & Roots Solves problems with integral exponents 2026-09-25 20:16:00 1
392 12 Mathematics Number System Factors, Multiples & Divisibility Proves divisibility rules of 2, 3, 4, 5, 6, 9 and 11 2026-09-25 20:16:00 1
393 12 Mathematics Number System Fractions, Decimals & Rational Numbers Finds out as many rational numbers as possible between two given rational numbers 2026-09-25 20:16:00 1
394 12 Mathematics Number System Fractions, Decimals & Rational Numbers Generalises properties of addition, subtraction, multiplication and division of rational numbers through patterns 2026-09-25 20:16:00 1
395 12 Mathematics Ratio, Proportion & Commercial Arithmetic Percentage, Profit & Loss, Interest Applies the concept of per cent in profit and loss situations to find discount, VAT and compound interest 2026-09-25 20:16:00 1
396 12 Mathematics Ratio, Proportion & Commercial Arithmetic Ratio & Proportion Solves problems based on direct and inverse proportions 2026-09-25 20:16:00 1
397 12 Science Classification Classification of Materials, Organisms & Processes Classifies materials and organisms based on properties/characteristics (metals and non-metals; kharif and rabi crops; useful and harmful microorganisms; sexual and asexual reproduction; celestial objects; exhaustible and inexhaustible resources) 2026-09-25 20:16:00 1
398 12 Science Environmental Awareness, Creativity & Values Creativity Exhibits creativity in designing, planning, making use of available resources, etc. 2026-09-25 20:16:00 1
399 12 Science Environmental Awareness, Creativity & Values Environmental ProtectionMakes efforts to protect environment (judicious use of resources, controlled use of fertilisers and pesticides, coping with environmental hazards) 2026-09-25 20:16:00 1
400 12 Science Environmental Awareness, Creativity & Values Scientific Values Exhibits values of honesty, objectivity, cooperation, freedom from fear and prejudices 2026-09-25 20:16:00 1
401 12 Science Explaining Processes & Cause-Effect Cause–Effect Relationships Relates processes and phenomena with causes (smog with air pollutants; deterioration of monuments with acid rain) 2026-09-25 20:16:00 1
402 12 Science Explaining Processes & Cause-Effect Chemical Word Equations Writes word equations for chemical reactions (reactions of metals and non-metals with air, water and acids) 2026-09-25 20:16:00 1
403 12 Science Explaining Processes & Cause-Effect Explaining Processes & Phenomena Explains processes and phenomena (reproduction in humans and animals, production and propagation of sound, chemical effects of electric current, multiple images, structure of flame) 2026-09-25 20:16:00 1
404 12 Science Identification & Differentiation Differentiation Differentiates materials and organisms (natural and human-made fibres; contact and non-contact forces; liquids as conductors and insulators; plant and animal cells; viviparous and oviparous animals) on the basis of properties, structure and functions 2026-09-25 20:16:00 1
405 12 Science Measurement, Recording & Representation Labelled Diagrams & Flow Charts Draws labelled diagrams/flow charts (structure of cell, eye, human reproductive organs, experimental set-ups) 2026-09-25 20:16:00 1
406 12 Science Measurement, Recording & Representation Measurement & Calculation Measures angles of incidence and reflection, etc. 2026-09-25 20:16:00 1
407 12 Science Measurement, Recording & Representation Microscopy & Slide Preparation Prepares slides of microorganisms, onion peel, human cheek cells, etc., and describes their microscopic features 2026-09-25 20:16:00 1
408 12 Science Models & Application in Daily Life Application of Concepts in Daily Life Applies learning of scientific concepts in day-to-day life (purifying water, segregating wastes, increasing crop production, using metals/non-metals, friction, challenging myths and taboos about adolescence) 2026-09-25 20:16:00 1
409 12 Science Models & Application in Daily Life History of Scientific Discoveries Discusses and appreciates stories of scientific discoveries 2026-09-25 20:16:00 1
410 12 Science Models & Application in Daily Life Model Construction Constructs models using materials from surroundings and explains their working (ektara, electroscope, fire extinguisher) 2026-09-25 20:16:00 1
411 12 Science Scientific Inquiry & Investigation Conducting Investigations Conducts simple investigations to seek answers to queries (conditions for combustion; salt and sugar in pickles; do liquids exert equal pressure at the same depth) 2026-09-25 20:16:00 1
412 12 Social Science Geography Agriculture & IndustriesAnalyses factors due to which some countries are known for production of major crops (wheat, rice, cotton, jute) and locates them on the world map 2026-09-25 20:16:00 1
413 12 Social Science Geography Agriculture & IndustriesClassifies different types of industries based on raw materials, size and ownership 2026-09-25 20:16:00 1
414 12 Social Science Geography Agriculture & IndustriesDescribes major crops, types of farming and agricultural practices in her/his own area/state 2026-09-25 20:16:00 1
415 12 Social Science Geography Agriculture & IndustriesDraws interrelationship between types of farming and development in different regions of the world 2026-09-25 20:16:00 1
416 12 Social Science Geography Disasters & Management Describes causes of forest fire, landslide, industrial disasters and their risk reduction measures 2026-09-25 20:16:00 1
417 12 Social Science Geography Environment & Natural Resources Analyses uneven distribution of natural and human-made resources on the earth 2026-09-25 20:16:00 1
418 12 Social Science Geography Environment & Natural Resources Justifies judicious use of natural resources such as water, soil, forest, etc. 2026-09-25 20:16:00 1
419 12 Social Science Geography Maps, Globe & Diagrams Draws bar diagrams to show population of different countries/India/states 2026-09-25 20:16:00 1
420 12 Social Science Geography Maps, Globe & Diagrams Interprets the world map for uneven distribution of population 2026-09-25 20:16:00 1
421 12 Social Science Geography Maps, Globe & Diagrams Locates distribution of important minerals (coal, mineral oil) on the world map 2026-09-25 20:16:00 1
422 12 Social Science History Art, Architecture & Culture Outlines major developments during the modern period in the field of arts 2026-09-25 20:16:00 1
423 12 Social Science History Colonial & Modern IndiaAnalyses issues related to caste, women, widow remarriage, child marriage, social reforms and colonial laws/policies on these issues 2026-09-25 20:16:00 1
424 12 Social Science History Colonial & Modern IndiaAnalyses significant developments in the process of nation building 2026-09-25 20:16:00 1
425 12 Social Science History Colonial & Modern IndiaAnalyses the decline of pre-existing urban centres and handicraft industries and development of new urban centres and industries during the colonial period 2026-09-25 20:16:00 1
426 12 Social Science History Colonial & Modern IndiaDescribes the forms of tribal societies in the 19th century and their relationship with the environment; explains colonial policies towards tribal communities 2026-09-25 20:16:00 1
427 12 Social Science History Colonial & Modern IndiaExplains differences in the impact of colonial agrarian policies in different regions (e.g., indigo rebellion) 2026-09-25 20:16:00 1
428 12 Social Science History Colonial & Modern IndiaExplains how the English East India Company became the most dominant power 2026-09-25 20:16:00 1
429 12 Social Science History Colonial & Modern IndiaExplains the institutionalisation of the new education system in India 2026-09-25 20:16:00 1
430 12 Social Science History Colonial & Modern IndiaExplains the origin, nature and spread of the revolt of 1857 and the lessons learned from it 2026-09-25 20:16:00 1
431 12 Social Science History Colonial & Modern IndiaOutlines the course of the Indian national movement from the 1870s till Independence 2026-09-25 20:16:00 1
432 12 Social Science History Sources of History Distinguishes the ‘modern period’ from the ‘medieval’ and ‘ancient’ periods through sources, nomenclature and broad developments 2026-09-25 20:16:00 1
433 12 Social Science Social & Political Life (Civics & Economics) Constitution, Rights & Laws Analyses causes and consequences of marginalisation faced by disadvantaged sections of one’s own region 2026-09-25 20:16:00 1
434 12 Social Science Social & Political Life (Civics & Economics) Constitution, Rights & Laws Describes the functioning of the judicial system in India citing landmark cases; demonstrates how to file an FIR 2026-09-25 20:16:00 1
435 12 Social Science Social & Political Life (Civics & Economics) Constitution, Rights & Laws Describes the process of making a law (e.g., Domestic Violence Act, RTI Act, RTE Act) 2026-09-25 20:16:00 1
436 12 Social Science Social & Political Life (Civics & Economics) Constitution, Rights & Laws Illustrates the Fundamental Rights and Fundamental Duties with examples; applies them to find out about their violation, protection and promotion (e.g., Child Rights) 2026-09-25 20:16:00 1
437 12 Social Science Social & Political Life (Civics & Economics) Constitution, Rights & Laws Interprets social and political issues in one’s own region with reference to the Constitution of India 2026-09-25 20:16:00 1
438 12 Social Science Social & Political Life (Civics & Economics) Elections & Constituencies Differentiates between State government and Union government; describes the process of election to the Lok Sabha 2026-09-25 20:16:00 1
439 12 Social Science Social & Political Life (Civics & Economics) Elections & Constituencies Locates one’s own constituency on the parliamentary constituency map of State/UT and names local MP 2026-09-25 20:16:00 1
440 12 Social Science Social & Political Life (Civics & Economics) Markets, Economy & Public Facilities Identifies the role of Government in providing public facilities (water, sanitation, road, electricity) and in regulating economic activities 2026-09-25 20:16:00 1
"""

CLASS_MAP = {
    5: "I",
    6: "II",
    7: "III",
    8: "IV",
    9: "V",
    10: "VI",
    11: "VII",
    12: "VIII"
}

SUBJECTS = [
    "English",
    "Mathematics",
    "EVS",
    "Science",
    "Social Science"
]

lines = [l.strip() for l in PAGES_TEXT.strip().split("\n") if l.strip()]
print(f"Total raw lines: {len(lines)}")

records = []
for line in lines:
    # Match id, masterclassId, subject
    m = re.match(r'^(\d+)\s+(\d+)\s+(English|Mathematics|EVS|Science|Social Science)\s+(.*?)\s+2026-09-25\s+\d{2}:\d{2}(?::\d{2})?\s+1$', line)
    if not m:
        # Check without date if slightly different
        print("MISMATCH LINE:", line)
        continue
    
    row_id = int(m.group(1))
    mc_id = int(m.group(2))
    subject = m.group(3)
    rest = m.group(4)
    
    records.append({
        "id": row_id,
        "masterclassId": mc_id,
        "class": CLASS_MAP.get(mc_id, "I"),
        "subject": subject,
        "raw_rest": rest
    })

print(f"Matched records: {len(records)}")
with open("scratch/parsed_sample.json", "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2)
