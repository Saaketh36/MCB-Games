// Authoritative Curriculum Data derived strictly from 'skillAreaOutcomes - Sheet1.pdf'
// Total Learning Outcomes: 440 across Classes I to VIII
(function (root) {
  const SUBJECT_CODE = { 'English': 'ENG', 'Mathematics': 'MAT', 'EVS': 'EVS', 'Science': 'SCI', 'Social Science': 'SOC' };
  const RAW = `
@I
!English
Listening|Following Instructions & Announcements|Classroom Instructions: 'Shut the Door' & 'Bring the Book'|MCQ Quiz
Listening|Following Instructions & Announcements|Listen to Instructions & Draw a Picture|MCQ Quiz
Listening|Listening Comprehension & Response|Greetings & Polite Responses (English and Signing)|MCQ Quiz
Reading|Phonics & Letter Recognition|Small & Capital Letters (Print and Braille)|MCQ Quiz
Reading|Phonics & Letter Recognition|Phonics Blends: 'br' and 'fr' ('brother', 'frog')|MCQ Quiz
Reading|Phonics & Letter Recognition|Alphabet Sounds & Letter Recognition A-Z|MCQ Quiz
Reading|Word Recognition|Word Recognition & Picture Association|MCQ Quiz
Speaking|Oral Expression & Narration|Speaking Studio: Oral Expression & Narration (LO #8)|MCQ Quiz
Speaking|Oral Expression & Narration|Speaking Studio: Oral Expression & Narration (LO #9)|MCQ Quiz
Speaking|Questioning|Speaking Studio: Questioning (LO #10)|MCQ Quiz
Speaking|Recitation & Performance|Speaking Studio: Recitation & Performance (LO #11)|MCQ Quiz
Vocabulary & Grammar|Parts of Speech|Parts of Speech: Nouns ('boy', 'sun') & Prepositions ('in', 'on', 'under')|MCQ Quiz
Vocabulary & Grammar|Vocabulary|Grammar & Vocabulary Studio: Vocabulary (LO #13)|MCQ Quiz
Writing|Pre-writing|Pre-Writing: Drawing & Scribbling to Stories|MCQ Quiz
Writing|Word, Sentence & Paragraph Writing|Simple Word Writing ('fan', 'hen', 'rat')|MCQ Quiz
!Mathematics
Data Handling|Data Collection & Interpretation|Data Handling: Data Collection & Interpretation (LO #16)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Length & Distance|Non-Uniform Units: Hand Span, Forearm & Footsteps|MCQ Quiz
Numbers & Operations|Addition & Subtraction|Addition & Subtraction within 20 and up to 9|MCQ Quiz
Numbers & Operations|Number Sense & Place Value|Understanding the Concept of Zero|MCQ Quiz
Numbers & Operations|Number Sense & Place Value|Numbers & Operations: Number Sense & Place Value (LO #20)|MCQ Quiz
Numbers & Operations|Number Sense & Place Value|Numbers & Operations: Number Sense & Place Value (LO #21)|MCQ Quiz
Numbers & Operations|Number Sense & Place Value|Numbers & Operations: Number Sense & Place Value (LO #22)|MCQ Quiz
Patterns|Number Patterns|Patterns: Number Patterns (LO #23)|MCQ Quiz
Shapes & Spatial Understanding|3D Shapes & Nets|Physical Features of Shapes: A Ball Rolls, a Box Slides|MCQ Quiz
Shapes & Spatial Understanding|Classification of Objects|Shapes & Spatial Understanding: Classification of Objects (LO #25)|MCQ Quiz
@II
!English
Listening|Following Instructions & Announcements|Follow Audio Instructions to Draw|MCQ Quiz
Listening|Listening Comprehension & Response|Polite Conversations: 'How are you?'|MCQ Quiz
Listening|Listening Comprehension & Response|Children's Newspaper Section Read-Aloud|MCQ Quiz
Reading|Reading Comprehension|Reading Studio: Reading Comprehension (LO #29)|MCQ Quiz
Reading|Reading Comprehension|Reading Studio: Reading Comprehension (LO #30)|MCQ Quiz
Speaking|Questioning|Speaking Studio: Questioning (LO #31)|MCQ Quiz
Speaking|Recitation & Performance|Speaking Studio: Recitation & Performance (LO #32)|MCQ Quiz
Vocabulary & Grammar|Parts of Speech|Prepositions of Place & Order: 'before', 'between'|MCQ Quiz
Vocabulary & Grammar|Parts of Speech|Pronouns: Gender ('he/she', 'his/her') & Demonstratives ('this/that')|MCQ Quiz
Vocabulary & Grammar|Parts of Speech|Adjectives: Size, Shape, Colour & Texture ('big', 'pink', 'soft')|MCQ Quiz
Writing|Pre-writing|Writing Studio: Pre-writing (LO #36)|MCQ Quiz
Writing|Word, Sentence & Paragraph Writing|Writing Studio: Word, Sentence & Paragraph Writing (LO #37)|MCQ Quiz
!Mathematics
Data Handling|Data Collection & Interpretation|Data Handling: Data Collection & Interpretation (LO #38)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Capacity & Volume|Measurement (Length, Weight, Capacity, Time, Money): Capacity & Volume (LO #39)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Money|Measurement (Length, Weight, Capacity, Time, Money): Money (LO #40)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Time & Calendar|Measurement (Length, Weight, Capacity, Time, Money): Time & Calendar (LO #41)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Time & Calendar|Measurement (Length, Weight, Capacity, Time, Money): Time & Calendar (LO #42)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Weight|Measurement (Length, Weight, Capacity, Time, Money): Weight (LO #43)|MCQ Quiz
Numbers & Operations|Addition & Subtraction|Numbers & Operations: Addition & Subtraction (LO #44)|MCQ Quiz
Numbers & Operations|Number Sense & Place Value|Numbers & Operations: Number Sense & Place Value (LO #45)|MCQ Quiz
Shapes & Spatial Understanding|2D Shapes & Lines|Shapes & Spatial Understanding: 2D Shapes & Lines (LO #46)|MCQ Quiz
Shapes & Spatial Understanding|3D Shapes & Nets|Shapes & Spatial Understanding: 3D Shapes & Nets (LO #47)|MCQ Quiz
@III
!English
Listening|Listening Comprehension & Response|Oral Messages & Telephonic Communication|MCQ Quiz
Reading|Environmental Print & Information|Reading Studio: Environmental Print & Information (LO #49)|MCQ Quiz
Reading|Reading Aloud & Fluency|Reading Studio: Reading Aloud & Fluency (LO #50)|MCQ Quiz
Reading|Reading Comprehension|Reading Studio: Reading Comprehension (LO #51)|MCQ Quiz
Speaking|Oral Expression & Narration|Speaking Studio: Oral Expression & Narration (LO #52)|MCQ Quiz
Speaking|Recitation & Performance|Speaking Studio: Recitation & Performance (LO #53)|MCQ Quiz
Speaking|Recitation & Performance|Speaking Studio: Recitation & Performance (LO #54)|MCQ Quiz
Vocabulary & Grammar|Parts of Speech|Grammar & Vocabulary Studio: Parts of Speech (LO #55)|MCQ Quiz
Vocabulary & Grammar|Tenses|Grammar & Vocabulary Studio: Tenses (LO #56)|MCQ Quiz
Vocabulary & Grammar|Vocabulary|Opposites (Antonyms): 'day/night', 'close/open'|MCQ Quiz
Vocabulary & Grammar|Vocabulary|Grammar & Vocabulary Studio: Vocabulary (LO #58)|MCQ Quiz
Writing|Dictation|Writing Studio: Dictation (LO #59)|MCQ Quiz
Writing|Mechanics & Punctuation|Punctuation & Mechanics (Class III)|MCQ Quiz
Writing|Word, Sentence & Paragraph Writing|Writing Studio: Word, Sentence & Paragraph Writing (LO #61)|MCQ Quiz
Writing|Word, Sentence & Paragraph Writing|Writing Studio: Word, Sentence & Paragraph Writing (LO #62)|MCQ Quiz
!EVS
Classification & Grouping|Grouping by Features & Properties|EVS Studio: Grouping by Features & Properties (LO #63)|MCQ Quiz
Creative Expression|Drawings, Models & Maps|EVS Studio: Drawings, Models & Maps (LO #64)|MCQ Quiz
Estimation, Experimentation & Recording|Estimation & Verification|EVS Studio: Estimation & Verification (LO #65)|MCQ Quiz
Estimation, Experimentation & Recording|Recording & Predicting Patterns|EVS Studio: Recording & Predicting Patterns (LO #66)|MCQ Quiz
Explanation & Understanding Relationships|Family & Community|EVS Studio: Family & Community (LO #67)|MCQ Quiz
Explanation & Understanding Relationships|Food & Water|EVS Studio: Food & Water (LO #68)|MCQ Quiz
Mapping & Spatial Skills|Map Reading & Directions|EVS Studio: Map Reading & Directions (LO #69)|MCQ Quiz
Observation & Identification|Animals & Birds|EVS Studio: Animals & Birds (LO #70)|MCQ Quiz
Observation & Identification|Family & Relationships|EVS Studio: Family & Relationships (LO #71)|MCQ Quiz
Observation & Identification|Plants|EVS Studio: Plants (LO #72)|MCQ Quiz
Observation & Identification|Surroundings (Objects, Places & Activities)|EVS Studio: Surroundings (Objects, Places & Activities) (LO #73)|MCQ Quiz
Past & Present (Change over Time)|Continuity & Change|EVS Studio: Continuity & Change (LO #74)|MCQ Quiz
Values, Sensitivity & Opinion|Opinion on Social Issues|EVS Studio: Opinion on Social Issues (LO #75)|MCQ Quiz
Values, Sensitivity & Opinion|Rules & Cooperation|EVS Studio: Rules & Cooperation (LO #76)|MCQ Quiz
Values, Sensitivity & Opinion|Sensitivity, Hygiene & Conservation|EVS Studio: Sensitivity, Hygiene & Conservation (LO #77)|MCQ Quiz
!Mathematics
Data Handling|Data Representation (Tables & Graphs)|Data Handling: Data Representation (Tables & Graphs) (LO #78)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Capacity & Volume|Measurement (Length, Weight, Capacity, Time, Money): Capacity & Volume (LO #79)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Length & Distance|Measurement (Length, Weight, Capacity, Time, Money): Length & Distance (LO #80)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Money|Measurement (Length, Weight, Capacity, Time, Money): Money (LO #81)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Money|Measurement (Length, Weight, Capacity, Time, Money): Money (LO #82)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Time & Calendar|Measurement (Length, Weight, Capacity, Time, Money): Time & Calendar (LO #83)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Time & Calendar|Measurement (Length, Weight, Capacity, Time, Money): Time & Calendar (LO #84)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Weight|Measurement (Length, Weight, Capacity, Time, Money): Weight (LO #85)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Weight|Measurement (Length, Weight, Capacity, Time, Money): Weight (LO #86)|MCQ Quiz
Numbers & Operations|Addition & Subtraction|Numbers & Operations: Addition & Subtraction (LO #87)|MCQ Quiz
Numbers & Operations|Estimation & Problem Solving|Numbers & Operations: Estimation & Problem Solving (LO #88)|MCQ Quiz
Numbers & Operations|Multiplication & Division|Numbers & Operations: Multiplication & Division (LO #89)|MCQ Quiz
Numbers & Operations|Multiplication & Division|Division by Equal Sharing & Repeated Subtraction ('12 ÷ 3')|MCQ Quiz
Numbers & Operations|Number Sense & Place Value|Numbers & Operations: Number Sense & Place Value (LO #91)|MCQ Quiz
Patterns|Number Patterns|Patterns: Number Patterns (LO #92)|MCQ Quiz
Shapes & Spatial Understanding|2D Shapes & Lines|Shapes & Spatial Understanding: 2D Shapes & Lines (LO #93)|MCQ Quiz
Shapes & Spatial Understanding|2D Shapes & Lines|Shapes & Spatial Understanding: 2D Shapes & Lines (LO #94)|MCQ Quiz
Shapes & Spatial Understanding|2D Shapes & Lines|Shapes & Spatial Understanding: 2D Shapes & Lines (LO #95)|MCQ Quiz
@IV
!English
Listening|Following Instructions & Announcements|School Announcements & Instructions|MCQ Quiz
Listening|Listening Comprehension & Response|Listening Comprehension & Public Broadcast (LO #97)|MCQ Quiz
Reading|Environmental Print & Information|Reading Studio: Environmental Print & Information (LO #98)|MCQ Quiz
Reading|Environmental Print & Information|Reading Studio: Environmental Print & Information (LO #99)|MCQ Quiz
Reading|Reading Aloud & Fluency|Reading Studio: Reading Aloud & Fluency (LO #100)|MCQ Quiz
Reading|Reference Skills|Reference Skills: Dictionary, Thesaurus & Encyclopedia (Class IV)|MCQ Quiz
Reading|Vocabulary in Context|Reading Studio: Vocabulary in Context (LO #102)|MCQ Quiz
Speaking|Oral Expression & Narration|Speaking Studio: Oral Expression & Narration (LO #103)|MCQ Quiz
Speaking|Oral Expression & Narration|Speaking Studio: Oral Expression & Narration (LO #104)|MCQ Quiz
Speaking|Oral Expression & Narration|Speaking Studio: Oral Expression & Narration (LO #105)|MCQ Quiz
Speaking|Oral Expression & Narration|Speaking Studio: Oral Expression & Narration (LO #106)|MCQ Quiz
Speaking|Recitation & Performance|Speaking Studio: Recitation & Performance (LO #107)|MCQ Quiz
Speaking|Recitation & Performance|Speaking Studio: Recitation & Performance (LO #108)|MCQ Quiz
Vocabulary & Grammar|Linkers & Connectors|Discourse Linkers & Connectors: 'First', 'Next'|Sequence Order
Vocabulary & Grammar|Parts of Speech|Grammar & Vocabulary Studio: Parts of Speech (LO #110)|MCQ Quiz
Vocabulary & Grammar|Vocabulary|Grammar & Vocabulary Studio: Vocabulary (LO #111)|MCQ Quiz
Writing|Dictation|Writing Studio: Dictation (LO #112)|MCQ Quiz
Writing|Functional Writing|Writing Studio: Functional Writing (LO #113)|MCQ Quiz
Writing|Mechanics & Punctuation|Punctuation & Mechanics (Class IV)|MCQ Quiz
!EVS
Classification & Grouping|Grouping by Features & Properties|EVS Studio: Grouping by Features & Properties (LO #115)|MCQ Quiz
Creative Expression|Drawings, Models & Maps|EVS Studio: Drawings, Models & Maps (LO #116)|MCQ Quiz
Estimation, Experimentation & Recording|Estimation & Verification|EVS Studio: Estimation & Verification (LO #117)|MCQ Quiz
Estimation, Experimentation & Recording|Recording & Predicting Patterns|EVS Studio: Recording & Predicting Patterns (LO #118)|MCQ Quiz
Explanation & Understanding Relationships|Animal Behaviour & Family Change|Animal Herd Behavior: Ants, Bees & Elephants|MCQ Quiz
Explanation & Understanding Relationships|Food & Water|Food Supply Journey: Field to Mandi to Home|Sequence Order
Explanation & Understanding Relationships|Work & Livelihood|EVS Studio: Work & Livelihood (LO #121)|MCQ Quiz
Mapping & Spatial Skills|Map Reading & Directions|EVS Studio: Map Reading & Directions (LO #122)|MCQ Quiz
Mapping & Spatial Skills|Using Signs & Information|EVS Studio: Using Signs & Information (LO #123)|MCQ Quiz
Observation & Identification|Animals & Birds|EVS Studio: Animals & Birds (LO #124)|MCQ Quiz
Observation & Identification|Family & Relationships|EVS Studio: Family & Relationships (LO #125)|MCQ Quiz
Observation & Identification|Plants|EVS Studio: Plants (LO #126)|MCQ Quiz
Past & Present (Change over Time)|Continuity & Change|EVS Studio: Continuity & Change (LO #127)|MCQ Quiz
Values, Sensitivity & Opinion|Opinion on Social Issues|EVS Studio: Opinion on Social Issues (LO #128)|MCQ Quiz
Values, Sensitivity & Opinion|Sensitivity, Hygiene & Conservation|EVS Studio: Sensitivity, Hygiene & Conservation (LO #129)|MCQ Quiz
!Mathematics
Data Handling|Data Representation (Tables & Graphs)|Data Handling: Data Representation (Tables & Graphs) (LO #130)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Area & Perimeter|Measurement (Length, Weight, Capacity, Time, Money): Area & Perimeter (LO #131)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Estimation & Verification of Measures|Measurement (Length, Weight, Capacity, Time, Money): Estimation & Verification of Measures (LO #132)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Problem Solving with Measures|Measurement (Length, Weight, Capacity, Time, Money): Problem Solving with Measures (LO #133)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Time & Calendar|Measurement (Length, Weight, Capacity, Time, Money): Time & Calendar (LO #134)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Time & Calendar|Measurement (Length, Weight, Capacity, Time, Money): Time & Calendar (LO #135)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Unit Conversion|Measurement (Length, Weight, Capacity, Time, Money): Unit Conversion (LO #136)|MCQ Quiz
Numbers & Operations|Estimation & Problem Solving|Numbers & Operations: Estimation & Problem Solving (LO #137)|MCQ Quiz
Numbers & Operations|Fractions & Decimals|Numbers & Operations: Fractions & Decimals (LO #138)|MCQ Quiz
Numbers & Operations|Fractions & Decimals|Numbers & Operations: Fractions & Decimals (LO #139)|MCQ Quiz
Numbers & Operations|Multiplication & Division|Numbers & Operations: Multiplication & Division (LO #140)|MCQ Quiz
Numbers & Operations|Multiplication & Division|Numbers & Operations: Multiplication & Division (LO #141)|MCQ Quiz
Patterns|Number Patterns|Patterns: Number Patterns (LO #142)|MCQ Quiz
Patterns|Shape & Geometric Patterns|Patterns: Shape & Geometric Patterns (LO #143)|MCQ Quiz
Shapes & Spatial Understanding|2D Shapes & Lines|Shapes & Spatial Understanding: 2D Shapes & Lines (LO #144)|MCQ Quiz
Shapes & Spatial Understanding|3D Shapes & Nets|Shapes & Spatial Understanding: 3D Shapes & Nets (LO #145)|MCQ Quiz
Shapes & Spatial Understanding|Spatial Views|Shapes & Spatial Understanding: Spatial Views (LO #146)|MCQ Quiz
Shapes & Spatial Understanding|Symmetry|Shapes & Spatial Understanding: Symmetry (LO #147)|MCQ Quiz
@V
!English
Listening|Following Instructions & Announcements|Sports Field Instructions: 'Hit the ball!' & 'Run!'|MCQ Quiz
Listening|Listening Comprehension & Response|Listening Comprehension & Public Broadcast (LO #149)|MCQ Quiz
Reading|Critical Reading|Reading Studio: Critical Reading (LO #150)|MCQ Quiz
Reading|Environmental Print & Information|Reading Studio: Environmental Print & Information (LO #151)|MCQ Quiz
Reading|Extensive Reading|Reading Studio: Extensive Reading (LO #152)|MCQ Quiz
Reading|Reading Comprehension|Reading Studio: Reading Comprehension (LO #153)|MCQ Quiz
Reading|Reference Skills|Reference Skills: Dictionary, Thesaurus & Encyclopedia (Class V)|MCQ Quiz
Speaking|Conversation & Polite Expressions|Speaking Studio: Conversation & Polite Expressions (LO #155)|MCQ Quiz
Speaking|Oral Expression & Narration|Speaking Studio: Oral Expression & Narration (LO #156)|MCQ Quiz
Speaking|Oral Expression & Narration|Speaking Studio: Oral Expression & Narration (LO #157)|MCQ Quiz
Speaking|Recitation & Performance|Speaking Studio: Recitation & Performance (LO #158)|MCQ Quiz
Vocabulary & Grammar|Grammar in Use|Grammar & Vocabulary Studio: Grammar in Use (LO #159)|MCQ Quiz
Vocabulary & Grammar|Tenses|Grammar & Vocabulary Studio: Tenses (LO #160)|MCQ Quiz
Vocabulary & Grammar|Vocabulary|Synonyms & Antonyms in Context ('big/large', 'inside/outside')|MCQ Quiz
Writing|Creative Writing|Writing Studio: Creative Writing (LO #162)|MCQ Quiz
Writing|Creative Writing|Creative Writing: Mini Biography & Autobiography|MCQ Quiz
Writing|Dictation|Writing Studio: Dictation (LO #164)|MCQ Quiz
Writing|Functional Writing|Writing Studio: Functional Writing (LO #165)|MCQ Quiz
Writing|Word, Sentence & Paragraph Writing|Writing Studio: Word, Sentence & Paragraph Writing (LO #166)|MCQ Quiz
!EVS
Classification & Grouping|Grouping by Features & Properties|EVS Studio: Grouping by Features & Properties (LO #167)|MCQ Quiz
Creative Expression|Drawings, Models & Maps|EVS Studio: Drawings, Models & Maps (LO #168)|MCQ Quiz
Estimation, Experimentation & Recording|Estimation & Verification|EVS Studio: Estimation & Verification (LO #169)|MCQ Quiz
Estimation, Experimentation & Recording|Recording & Predicting Patterns|EVS Studio: Recording & Predicting Patterns (LO #170)|MCQ Quiz
Explanation & Understanding Relationships|Animals & Birds|EVS Studio: Animals & Birds (LO #171)|MCQ Quiz
Explanation & Understanding Relationships|Food & Water|EVS Studio: Food & Water (LO #172)|MCQ Quiz
Explanation & Understanding Relationships|Institutions|EVS Studio: Institutions (LO #173)|MCQ Quiz
Explanation & Understanding Relationships|Interdependence in Nature|EVS Studio: Interdependence in Nature (LO #174)|MCQ Quiz
Explanation & Understanding Relationships|Terrain, Climate & Culture|EVS Studio: Terrain, Climate & Culture (LO #175)|MCQ Quiz
Mapping & Spatial Skills|Map Reading & Directions|EVS Studio: Map Reading & Directions (LO #176)|MCQ Quiz
Past & Present (Change over Time)|Continuity & Change|EVS Studio: Continuity & Change (LO #177)|MCQ Quiz
Values, Sensitivity & Opinion|Opinion on Social Issues|EVS Studio: Opinion on Social Issues (LO #178)|MCQ Quiz
Values, Sensitivity & Opinion|Sensitivity, Hygiene & Conservation|EVS Studio: Sensitivity, Hygiene & Conservation (LO #179)|MCQ Quiz
!Mathematics
Data Handling|Data Representation (Tables & Graphs)|Data Handling: Data Representation (Tables & Graphs) (LO #180)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Estimation & Verification of Measures|Measurement (Length, Weight, Capacity, Time, Money): Estimation & Verification of Measures (LO #181)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Problem Solving with Measures|Measurement (Length, Weight, Capacity, Time, Money): Problem Solving with Measures (LO #182)|MCQ Quiz
Measurement (Length, Weight, Capacity, Time, Money)|Unit Conversion|Measurement (Length, Weight, Capacity, Time, Money): Unit Conversion (LO #183)|MCQ Quiz
Numbers & Operations|Estimation & Problem Solving|Numbers & Operations: Estimation & Problem Solving (LO #184)|MCQ Quiz
Numbers & Operations|Fractions & Decimals|Numbers & Operations: Fractions & Decimals (LO #185)|MCQ Quiz
Numbers & Operations|Fractions & Decimals|Numbers & Operations: Fractions & Decimals (LO #186)|MCQ Quiz
Numbers & Operations|Multiplication & Division|Numbers & Operations: Multiplication & Division (LO #187)|MCQ Quiz
Numbers & Operations|Number Sense & Place Value|Numbers & Operations: Number Sense & Place Value (LO #188)|MCQ Quiz
Patterns|Number Patterns|Patterns: Number Patterns (LO #189)|MCQ Quiz
Shapes & Spatial Understanding|3D Shapes & Nets|Shapes & Spatial Understanding: 3D Shapes & Nets (LO #190)|MCQ Quiz
Shapes & Spatial Understanding|Angles|Shapes & Spatial Understanding: Angles (LO #191)|MCQ Quiz
Shapes & Spatial Understanding|Symmetry|Shapes & Spatial Understanding: Symmetry (LO #192)|MCQ Quiz
@VI
!English
Listening|Following Instructions & Announcements|Public Announcements: Railway Station & Assembly|MCQ Quiz
Listening|Language Lab|Language Laboratory Session (Class VI)|MCQ Quiz
Listening|Listening Comprehension & Response|Listening Comprehension & Public Broadcast (LO #195)|MCQ Quiz
Reading|Environmental Print & Information|Reading Studio: Environmental Print & Information (LO #196)|MCQ Quiz
Reading|Reading Comprehension|Reading Studio: Reading Comprehension (LO #197)|MCQ Quiz
Reading|Reading Comprehension|Reading Studio: Reading Comprehension (LO #198)|MCQ Quiz
Reading|Reference Skills|Reference Skills: Dictionary, Thesaurus & Encyclopedia (Class VI)|MCQ Quiz
Speaking|Oral Expression & Narration|Speaking Studio: Oral Expression & Narration (LO #200)|MCQ Quiz
Speaking|Recitation & Performance|Speaking Studio: Recitation & Performance (LO #201)|MCQ Quiz
Speaking|Recitation & Performance|Speaking Studio: Recitation & Performance (LO #202)|MCQ Quiz
Vocabulary & Grammar|Grammar in Use|Grammar & Vocabulary Studio: Grammar in Use (LO #203)|MCQ Quiz
Vocabulary & Grammar|Vocabulary|Grammar & Vocabulary Studio: Vocabulary (LO #204)|MCQ Quiz
Writing|Creative Writing|Creative Writing: Book Review (Class VI)|MCQ Quiz
Writing|Dictation|Writing Studio: Dictation (LO #206)|MCQ Quiz
Writing|Functional Writing|Writing Studio: Functional Writing (LO #207)|MCQ Quiz
Writing|Word, Sentence & Paragraph Writing|Writing Studio: Word, Sentence & Paragraph Writing (LO #208)|MCQ Quiz
Writing|Word, Sentence & Paragraph Writing|Writing Studio: Word, Sentence & Paragraph Writing (LO #209)|MCQ Quiz
!Mathematics
Algebra|Variables & Algebraic Expressions|Algebra: Variables & Generalised Perimeter ('2(x+3)')|MCQ Quiz
Data Handling|Data Representation & Interpretation|Data Handling: Data Representation & Interpretation (LO #211)|MCQ Quiz
Geometry|3D Shapes & Visualisation|Geometry: 3D Shapes & Visualisation (LO #212)|MCQ Quiz
Geometry|Basic Geometrical Ideas|Geometry: Basic Geometrical Ideas (LO #213)|MCQ Quiz
Geometry|Lines & Angles|Geometry: Lines & Angles (LO #214)|MCQ Quiz
Geometry|Quadrilaterals|Geometry: Quadrilaterals (LO #215)|MCQ Quiz
Geometry|Symmetry|Geometry: Symmetry (LO #216)|MCQ Quiz
Geometry|Triangles & Congruence|Geometry: Triangles & Congruence (LO #217)|MCQ Quiz
Mensuration|Perimeter & Area|Mensuration: Perimeter & Area (LO #218)|MCQ Quiz
Number System|Factors, Multiples & Divisibility|Number System: Factors, Multiples & Divisibility (LO #219)|MCQ Quiz
Number System|Factors, Multiples & Divisibility|Number System: Factors, Multiples & Divisibility (LO #220)|MCQ Quiz
Number System|Fractions, Decimals & Rational Numbers|Number System: Fractions, Decimals & Rational Numbers (LO #221)|MCQ Quiz
Number System|Fractions, Decimals & Rational Numbers|Number System: Fractions, Decimals & Rational Numbers (LO #222)|MCQ Quiz
Number System|Integers|Number System: Integers (LO #223)|MCQ Quiz
Number System|Whole Numbers & Operations|Number System: Whole Numbers & Operations (LO #224)|MCQ Quiz
Ratio, Proportion & Commercial Arithmetic|Ratio & Proportion|Ratio, Proportion & Commercial Arithmetic: Ratio & Proportion (LO #225)|MCQ Quiz
Ratio, Proportion & Commercial Arithmetic|Unitary Method|Ratio, Proportion & Commercial Arithmetic: Unitary Method (LO #226)|MCQ Quiz
!Science
Classification|Classification of Materials, Organisms & Processes|Classification of Matter & Motion (Biotic/Abiotic, Rectilinear/Circular)|MCQ Quiz
Environmental Awareness, Creativity & Values|Creativity|Science Studio: Creativity (LO #228)|MCQ Quiz
Environmental Awareness, Creativity & Values|Environmental Protection|Science Studio: Environmental Protection (LO #229)|MCQ Quiz
Environmental Awareness, Creativity & Values|Scientific Values|Science Studio: Scientific Values (LO #230)|MCQ Quiz
Explaining Processes & Cause-Effect|General|Science Studio: General (LO #231)|MCQ Quiz
Explaining Processes & Cause-Effect|Explaining Processes & Phenomena|Science Studio: Explaining Processes & Phenomena (LO #232)|MCQ Quiz
Identification & Differentiation|Differentiation|Science Studio: Differentiation (LO #233)|MCQ Quiz
Identification & Differentiation|Identification|Science Studio: Identification (LO #234)|MCQ Quiz
Measurement, Recording & Representation|Labelled Diagrams & Flow Charts|Science Studio: Labelled Diagrams & Flow Charts (LO #235)|MCQ Quiz
Measurement, Recording & Representation|Measurement & Calculation|Science Studio: Measurement & Calculation (LO #236)|MCQ Quiz
Models & Application in Daily Life|Application of Concepts in Daily Life|Science Studio: Application of Concepts in Daily Life (LO #237)|MCQ Quiz
Models & Application in Daily Life|Model Construction|Science Studio: Model Construction (LO #238)|MCQ Quiz
Scientific Inquiry & Investigation|Conducting Investigations|Science Studio: Conducting Investigations (LO #239)|MCQ Quiz
!Social Science
Geography|Earth & the Solar System|Earth's Rotation & Revolution: Day, Night and Seasons|MCQ Quiz
Geography|Earth & the Solar System|Celestial Bodies: Sun, Earth and Moon|MCQ Quiz
Geography|Earth & the Solar System|Understanding Eclipses & Scientific Evidence|MCQ Quiz
Geography|Earth & the Solar System|Earth: A Unique Planet & The Biosphere|MCQ Quiz
Geography|Maps, Globe & Diagrams|Geography: Maps, Globe & Diagrams (LO #244)|MCQ Quiz
Geography|Maps, Globe & Diagrams|Grid Lines: Latitudes, Longitudes, Poles & Tropics|MCQ Quiz
Geography|Maps, Globe & Diagrams|Continents and Oceans on the World Map|MCQ Quiz
Geography|Maps, Globe & Diagrams|Major Physical Features of India|MCQ Quiz
History|Ancient India|Ancient India: Harappan Civilization & First Cities|MCQ Quiz
History|Ancient India|Ancient Dynasties: Mauryas, Guptas and Pallavas|MCQ Quiz
History|Ancient India|History: Ancient India (LO #250)|MCQ Quiz
History|Ancient India|History: Ancient India (LO #251)|MCQ Quiz
History|Ancient India|History: Ancient India (LO #252)|MCQ Quiz
History|Art, Architecture & Culture|History: Art, Architecture & Culture (LO #253)|MCQ Quiz
History|Art, Architecture & Culture|History: Art, Architecture & Culture (LO #254)|MCQ Quiz
History|Art, Architecture & Culture|History: Art, Architecture & Culture (LO #255)|MCQ Quiz
History|Religious Ideas & Movements|History: Religious Ideas & Movements (LO #256)|MCQ Quiz
History|Sources of History|History: Sources of History (LO #257)|MCQ Quiz
Social & Political Life (Civics & Economics)|Diversity & Discrimination|Civics: Diversity & Discrimination (LO #258)|MCQ Quiz
Social & Political Life (Civics & Economics)|Diversity & Discrimination|Equality & Inequality: Understanding Everyday Differences|MCQ Quiz
Social & Political Life (Civics & Economics)|Diversity & Discrimination|Diversity & Combating Discrimination: Identifying Sources|MCQ Quiz
Social & Political Life (Civics & Economics)|Government|Civics: Government (LO #261)|MCQ Quiz
Social & Political Life (Civics & Economics)|Government|Three Levels of Government: Local, State & Union|MCQ Quiz
Social & Political Life (Civics & Economics)|Markets, Economy & Public Facilities|Civics: Markets, Economy & Public Facilities (LO #263)|MCQ Quiz
@VII
!English
Listening|Following Instructions & Announcements|Listening Comprehension & Public Broadcast (LO #264)|MCQ Quiz
Listening|Language Lab|Language Laboratory Session (Class VII)|MCQ Quiz
Listening|Media & Public Listening|Listening Comprehension & Public Broadcast (LO #266)|MCQ Quiz
Reading|Critical Reading|Reading Studio: Critical Reading (LO #267)|MCQ Quiz
Reading|Environmental Print & Information|Reading Studio: Environmental Print & Information (LO #268)|MCQ Quiz
Reading|Extensive Reading|Reading Studio: Extensive Reading (LO #269)|MCQ Quiz
Reading|Reading Comprehension|Reading Studio: Reading Comprehension (LO #270)|MCQ Quiz
Reading|Reading Comprehension|Reading Studio: Reading Comprehension (LO #271)|MCQ Quiz
Reading|Reading Comprehension|Reading Studio: Reading Comprehension (LO #272)|MCQ Quiz
Speaking|Questioning|Speaking Studio: Questioning (LO #273)|MCQ Quiz
Speaking|Recitation & Performance|Speaking Studio: Recitation & Performance (LO #274)|MCQ Quiz
Speaking|Recitation & Performance|Speaking Studio: Recitation & Performance (LO #275)|MCQ Quiz
Speaking|Recitation & Performance|Speaking Studio: Recitation & Performance (LO #276)|MCQ Quiz
Vocabulary & Grammar|Grammar in Use|Grammar & Vocabulary Studio: Grammar in Use (LO #277)|MCQ Quiz
Vocabulary & Grammar|Vocabulary|Grammar & Vocabulary Studio: Vocabulary (LO #278)|MCQ Quiz
Vocabulary & Grammar|Vocabulary|Grammar & Vocabulary Studio: Vocabulary (LO #279)|MCQ Quiz
Writing|Creative Writing|Creative Writing: Book Review (Class VII)|MCQ Quiz
Writing|Creative Writing|Writing Studio: Creative Writing (LO #281)|MCQ Quiz
Writing|Creative Writing|Writing Studio: Creative Writing (LO #282)|MCQ Quiz
Writing|Functional Writing|Writing Studio: Functional Writing (LO #283)|MCQ Quiz
Writing|Note Taking|Writing Studio: Note Taking (LO #284)|MCQ Quiz
Writing|Word, Sentence & Paragraph Writing|Writing Studio: Word, Sentence & Paragraph Writing (LO #285)|MCQ Quiz
!Mathematics
Algebra|Linear Equations|Algebra: Linear Equations (LO #286)|MCQ Quiz
Algebra|Variables & Algebraic Expressions|Algebra: Variables & Algebraic Expressions (LO #287)|MCQ Quiz
Data Handling|Data Representation & Interpretation|Data Handling: Data Representation & Interpretation (LO #288)|MCQ Quiz
Data Handling|Measures of Central Tendency|Data Handling: Measures of Central Tendency (LO #289)|MCQ Quiz
Data Handling|Probability & Chance|Data Handling: Probability & Chance (LO #290)|MCQ Quiz
Geometry|Constructions|Geometry: Constructions (LO #291)|MCQ Quiz
Geometry|Lines & Angles|Geometry: Lines & Angles (LO #292)|MCQ Quiz
Geometry|Lines & Angles|Geometry: Lines & Angles (LO #293)|MCQ Quiz
Geometry|Triangles & Congruence|Geometry: Triangles & Congruence (LO #294)|MCQ Quiz
Geometry|Triangles & Congruence|Geometry: Triangles & Congruence (LO #295)|MCQ Quiz
Mensuration|Perimeter & Area|Mensuration: Perimeter & Area (LO #296)|MCQ Quiz
Mensuration|Perimeter & Area|Mensuration: Perimeter & Area (LO #297)|MCQ Quiz
Number System|Exponents, Squares & Roots|Number System: Exponents, Squares & Roots (LO #298)|MCQ Quiz
Number System|Fractions, Decimals & Rational Numbers|Number System: Fractions, Decimals & Rational Numbers (LO #299)|MCQ Quiz
Number System|Fractions, Decimals & Rational Numbers|Number System: Fractions, Decimals & Rational Numbers (LO #300)|MCQ Quiz
Number System|Fractions, Decimals & Rational Numbers|Number System: Fractions, Decimals & Rational Numbers (LO #301)|MCQ Quiz
Number System|Integers|Number System: Integers (LO #302)|MCQ Quiz
Ratio, Proportion & Commercial Arithmetic|Percentage, Profit & Loss, Interest|Ratio, Proportion & Commercial Arithmetic: Percentage, Profit & Loss, Interest (LO #303)|MCQ Quiz
Ratio, Proportion & Commercial Arithmetic|Percentage, Profit & Loss, Interest|Ratio, Proportion & Commercial Arithmetic: Percentage, Profit & Loss, Interest (LO #304)|MCQ Quiz
Ratio, Proportion & Commercial Arithmetic|Ratio & Proportion|Ratio & Proportion: Proportional Quantities (15, 45, 40, 120)|MCQ Quiz
!Science
Classification|Classification of Materials, Organisms & Processes|Science Studio: Classification of Materials, Organisms & Processes (LO #306)|MCQ Quiz
Environmental Awareness, Creativity & Values|Creativity|Science Studio: Creativity (LO #307)|MCQ Quiz
Environmental Awareness, Creativity & Values|Environmental Protection|Science Studio: Environmental Protection (LO #308)|MCQ Quiz
Environmental Awareness, Creativity & Values|Scientific Values|Science Studio: Scientific Values (LO #309)|MCQ Quiz
Explaining Processes & Cause-Effect|General|Science Studio: General (LO #310)|MCQ Quiz
Explaining Processes & Cause-Effect|Chemical Word Equations|Science Studio: Chemical Word Equations (LO #311)|MCQ Quiz
Explaining Processes & Cause-Effect|Explaining Processes & Phenomena|Science Studio: Explaining Processes & Phenomena (LO #312)|MCQ Quiz
Identification & Differentiation|Differentiation|Science Studio: Differentiation (LO #313)|MCQ Quiz
Identification & Differentiation|Identification|Science Studio: Identification (LO #314)|MCQ Quiz
Measurement, Recording & Representation|Graphs|Science Studio: Graphs (LO #315)|MCQ Quiz
Measurement, Recording & Representation|Labelled Diagrams & Flow Charts|Science Studio: Labelled Diagrams & Flow Charts (LO #316)|MCQ Quiz
Measurement, Recording & Representation|Measurement & Calculation|Science Studio: Measurement & Calculation (LO #317)|MCQ Quiz
Models & Application in Daily Life|Application of Concepts in Daily Life|Science Studio: Application of Concepts in Daily Life (LO #318)|MCQ Quiz
Models & Application in Daily Life|History of Scientific Discoveries|Science Studio: History of Scientific Discoveries (LO #319)|MCQ Quiz
Models & Application in Daily Life|Model Construction|Surrounding Models: Stethoscope, Anemometer & Newton's Disc|MCQ Quiz
Scientific Inquiry & Investigation|Conducting Investigations|Scientific Investigation: Flower Extract as Acid-Base Indicator|MCQ Quiz
!Social Science
Geography|Disasters & Management|Disaster Preparedness: Preventive Actions for Floods & Earthquakes|MCQ Quiz
Geography|Disasters & Management|Environmental Calamities: Factors Leading to Disasters|MCQ Quiz
Geography|Earth's Interior, Landforms & Atmosphere|Geography: Earth's Interior, Landforms & Atmosphere (LO #324)|MCQ Quiz
Geography|Earth's Interior, Landforms & Atmosphere|Composition and Structure of the Atmosphere|MCQ Quiz
Geography|Earth's Interior, Landforms & Atmosphere|Layers of Earth's Interior & Rock Types|MCQ Quiz
Geography|Environment & Natural Resources|Geography: Environment & Natural Resources (LO #327)|MCQ Quiz
Geography|Environment & Natural Resources|Geography: Environment & Natural Resources (LO #328)|MCQ Quiz
Geography|Environment & Natural Resources|Geography: Environment & Natural Resources (LO #329)|MCQ Quiz
Geography|Environment & Natural Resources|Geography: Environment & Natural Resources (LO #330)|MCQ Quiz
Geography|Human Geography & Development|Geography: Human Geography & Development (LO #331)|MCQ Quiz
Geography|Human Geography & Development|Geography: Human Geography & Development (LO #332)|MCQ Quiz
Geography|Maps, Globe & Diagrams|Geography: Maps, Globe & Diagrams (LO #333)|MCQ Quiz
History|Art, Architecture & Culture|History: Art, Architecture & Culture (LO #334)|MCQ Quiz
History|Medieval India|Medieval India: Administrative Measures of Khaljis & Tughlaqs|MCQ Quiz
History|Medieval India|Medieval India: Socio-Political & Economic Transformations|MCQ Quiz
History|Medieval India|History: Medieval India (LO #337)|MCQ Quiz
History|Medieval India|History: Medieval India (LO #338)|MCQ Quiz
History|Medieval India|Medieval India: Comparative Regional Developments|MCQ Quiz
History|Religious Ideas & Movements|Bhakti & Sufi Movements: Emergence of New Religious Ideas|MCQ Quiz
History|Religious Ideas & Movements|Bhakti & Sufi Traditions: Inferences from Devotional Poetry|MCQ Quiz
History|Sources of History|History: Sources of History (LO #342)|MCQ Quiz
Social & Political Life (Civics & Economics)|Constitution, Rights & Laws|Democratic Equality: Political, Economic & Social Dimensions|MCQ Quiz
Social & Political Life (Civics & Economics)|Constitution, Rights & Laws|Right to Equality: Regional Social & Economic Issues|MCQ Quiz
Social & Political Life (Civics & Economics)|Elections & Constituencies|Civics: Elections & Constituencies (LO #345)|MCQ Quiz
Social & Political Life (Civics & Economics)|Elections & Constituencies|Civics: Elections & Constituencies (LO #346)|MCQ Quiz
Social & Political Life (Civics & Economics)|Gender|Civics: Gender (LO #347)|MCQ Quiz
Social & Political Life (Civics & Economics)|Markets, Economy & Public Facilities|Civics: Markets, Economy & Public Facilities (LO #348)|MCQ Quiz
Social & Political Life (Civics & Economics)|Media & Advertising|Role of Media: News Reporting & Creating Advertisements|MCQ Quiz
@VIII
!English
Listening|Following Instructions & Announcements|Listening Comprehension & Public Broadcast (LO #350)|MCQ Quiz
Listening|Language Lab|Language Laboratory Session (Class VIII)|MCQ Quiz
Listening|Media & Public Listening|Listening Comprehension & Public Broadcast (LO #352)|MCQ Quiz
Reading|Critical Reading|Reading Studio: Critical Reading (LO #353)|MCQ Quiz
Reading|Critical Reading|Reading Studio: Critical Reading (LO #354)|MCQ Quiz
Reading|Extensive Reading|Reading Studio: Extensive Reading (LO #355)|MCQ Quiz
Reading|Reading Comprehension|Reading Studio: Reading Comprehension (LO #356)|MCQ Quiz
Reading|Reading Comprehension|Reading Studio: Reading Comprehension (LO #357)|MCQ Quiz
Speaking|Conversation & Polite Expressions|Speaking Studio: Conversation & Polite Expressions (LO #358)|MCQ Quiz
Speaking|Conversation & Polite Expressions|Speaking Studio: Conversation & Polite Expressions (LO #359)|MCQ Quiz
Speaking|Oral Expression & Narration|Speaking Studio: Oral Expression & Narration (LO #360)|MCQ Quiz
Speaking|Oral Expression & Narration|Speaking Studio: Oral Expression & Narration (LO #361)|MCQ Quiz
Speaking|Oral Expression & Narration|Speaking Studio: Oral Expression & Narration (LO #362)|MCQ Quiz
Speaking|Questioning|Speaking Studio: Questioning (LO #363)|MCQ Quiz
Speaking|Recitation & Performance|Speaking Studio: Recitation & Performance (LO #364)|MCQ Quiz
Speaking|Recitation & Performance|Speaking Studio: Recitation & Performance (LO #365)|MCQ Quiz
Vocabulary & Grammar|Grammar in Use|Grammar & Vocabulary Studio: Grammar in Use (LO #366)|MCQ Quiz
Vocabulary & Grammar|Grammar in Use|Grammar & Vocabulary Studio: Grammar in Use (LO #367)|MCQ Quiz
Vocabulary & Grammar|Vocabulary|Grammar & Vocabulary Studio: Vocabulary (LO #368)|MCQ Quiz
Vocabulary & Grammar|Vocabulary|Grammar & Vocabulary Studio: Vocabulary (LO #369)|MCQ Quiz
Writing|Answer Writing|Writing Studio: Answer Writing (LO #370)|MCQ Quiz
Writing|Creative Writing|Writing Studio: Creative Writing (LO #371)|MCQ Quiz
Writing|Creative Writing|Creative Writing: Book Review (Class VIII)|MCQ Quiz
Writing|Functional Writing|Writing Studio: Functional Writing (LO #373)|MCQ Quiz
Writing|Functional Writing|Writing Studio: Functional Writing (LO #374)|MCQ Quiz
Writing|Word, Sentence & Paragraph Writing|The Writing Process: Drafting, Revising, Editing & Finalising|Sequence Order
Writing|Word, Sentence & Paragraph Writing|Writing Studio: Word, Sentence & Paragraph Writing (LO #376)|MCQ Quiz
!Mathematics
Algebra|Algebraic Identities|Algebra: Algebraic Identities (LO #377)|MCQ Quiz
Algebra|Variables & Algebraic Expressions|Algebra: Variables & Algebraic Expressions (LO #378)|MCQ Quiz
Algebra|Variables & Algebraic Expressions|Algebra: Variables & Algebraic Expressions (LO #379)|MCQ Quiz
Data Handling|Data Representation & Interpretation|Data Handling: Data Representation & Interpretation (LO #380)|MCQ Quiz
Data Handling|Probability & Chance|Data Handling: Probability & Chance (LO #381)|MCQ Quiz
Geometry|3D Shapes & Visualisation|Geometry: 3D Shapes & Visualisation (LO #382)|MCQ Quiz
Geometry|3D Shapes & Visualisation|Euler's Relation for Polyhedra (F + V - E = 2)|MCQ Quiz
Geometry|Constructions|Geometry: Constructions (LO #384)|MCQ Quiz
Geometry|Quadrilaterals|Geometry: Quadrilaterals (LO #385)|MCQ Quiz
Geometry|Quadrilaterals|Geometry: Quadrilaterals (LO #386)|MCQ Quiz
Mensuration|Perimeter & Area|Mensuration: Perimeter & Area (LO #387)|MCQ Quiz
Mensuration|Perimeter & Area|Mensuration: Perimeter & Area (LO #388)|MCQ Quiz
Mensuration|Surface Area & Volume|Mensuration: Surface Area & Volume (LO #389)|MCQ Quiz
Number System|Exponents, Squares & Roots|Number System: Exponents, Squares & Roots (LO #390)|MCQ Quiz
Number System|Exponents, Squares & Roots|Number System: Exponents, Squares & Roots (LO #391)|MCQ Quiz
Number System|Factors, Multiples & Divisibility|Number System: Factors, Multiples & Divisibility (LO #392)|MCQ Quiz
Number System|Fractions, Decimals & Rational Numbers|Number System: Fractions, Decimals & Rational Numbers (LO #393)|MCQ Quiz
Number System|Fractions, Decimals & Rational Numbers|Number System: Fractions, Decimals & Rational Numbers (LO #394)|MCQ Quiz
Ratio, Proportion & Commercial Arithmetic|Percentage, Profit & Loss, Interest|Ratio, Proportion & Commercial Arithmetic: Percentage, Profit & Loss, Interest (LO #395)|MCQ Quiz
Ratio, Proportion & Commercial Arithmetic|Ratio & Proportion|Ratio, Proportion & Commercial Arithmetic: Ratio & Proportion (LO #396)|MCQ Quiz
!Science
Classification|Classification of Materials, Organisms & Processes|Science Studio: Classification of Materials, Organisms & Processes (LO #397)|MCQ Quiz
Environmental Awareness, Creativity & Values|Creativity|Science Studio: Creativity (LO #398)|MCQ Quiz
Environmental Awareness, Creativity & Values|Environmental Protection|Science Studio: Environmental Protection (LO #399)|MCQ Quiz
Environmental Awareness, Creativity & Values|Scientific Values|Science Studio: Scientific Values (LO #400)|MCQ Quiz
Explaining Processes & Cause-Effect|General|Science Studio: General (LO #401)|MCQ Quiz
Explaining Processes & Cause-Effect|Chemical Word Equations|Science Studio: Chemical Word Equations (LO #402)|MCQ Quiz
Explaining Processes & Cause-Effect|Explaining Processes & Phenomena|Science Studio: Explaining Processes & Phenomena (LO #403)|MCQ Quiz
Identification & Differentiation|Differentiation|Science Studio: Differentiation (LO #404)|MCQ Quiz
Measurement, Recording & Representation|Labelled Diagrams & Flow Charts|Science Studio: Labelled Diagrams & Flow Charts (LO #405)|MCQ Quiz
Measurement, Recording & Representation|Measurement & Calculation|Science Studio: Measurement & Calculation (LO #406)|MCQ Quiz
Measurement, Recording & Representation|Microscopy & Slide Preparation|Science Studio: Microscopy & Slide Preparation (LO #407)|MCQ Quiz
Models & Application in Daily Life|Application of Concepts in Daily Life|Science Studio: Application of Concepts in Daily Life (LO #408)|MCQ Quiz
Models & Application in Daily Life|History of Scientific Discoveries|Science Studio: History of Scientific Discoveries (LO #409)|MCQ Quiz
Models & Application in Daily Life|Model Construction|Science Studio: Model Construction (LO #410)|MCQ Quiz
Scientific Inquiry & Investigation|Conducting Investigations|Science Studio: Conducting Investigations (LO #411)|MCQ Quiz
!Social Science
Geography|Agriculture & Industries|Global Agricultural Production: Wheat, Rice, Cotton & Jute|MCQ Quiz
Geography|Agriculture & Industries|Geography: Agriculture & Industries (LO #413)|MCQ Quiz
Geography|Agriculture & Industries|Regional Agriculture: Farming Types & Local Crop Practices|MCQ Quiz
Geography|Agriculture & Industries|Geography: Agriculture & Industries (LO #415)|MCQ Quiz
Geography|Disasters & Management|Industrial Disasters & Landslides: Risk Reduction Measures|MCQ Quiz
Geography|Environment & Natural Resources|Geography: Environment & Natural Resources (LO #417)|MCQ Quiz
Geography|Environment & Natural Resources|Geography: Environment & Natural Resources (LO #418)|MCQ Quiz
Geography|Maps, Globe & Diagrams|Geography: Maps, Globe & Diagrams (LO #419)|MCQ Quiz
Geography|Maps, Globe & Diagrams|Geography: Maps, Globe & Diagrams (LO #420)|MCQ Quiz
Geography|Maps, Globe & Diagrams|Geography: Maps, Globe & Diagrams (LO #421)|MCQ Quiz
History|Art, Architecture & Culture|History: Art, Architecture & Culture (LO #422)|MCQ Quiz
History|Colonial & Modern India|History: Colonial & Modern India (LO #423)|MCQ Quiz
History|Colonial & Modern India|History: Colonial & Modern India (LO #424)|MCQ Quiz
History|Colonial & Modern India|Colonial & Modern India: Decline and Rise of Urban Centres|MCQ Quiz
History|Colonial & Modern India|History: Colonial & Modern India (LO #426)|MCQ Quiz
History|Colonial & Modern India|History: Colonial & Modern India (LO #427)|MCQ Quiz
History|Colonial & Modern India|History: Colonial & Modern India (LO #428)|MCQ Quiz
History|Colonial & Modern India|History: Colonial & Modern India (LO #429)|MCQ Quiz
History|Colonial & Modern India|The Revolt of 1857: Origins, Spread & Impact|MCQ Quiz
History|Colonial & Modern India|Indian National Movement: 1870s to 1947|Sequence Order
History|Sources of History|Historical Periods: Distinguishing Modern, Medieval & Ancient|MCQ Quiz
Social & Political Life (Civics & Economics)|Constitution, Rights & Laws|Civics: Constitution, Rights & Laws (LO #433)|MCQ Quiz
Social & Political Life (Civics & Economics)|Constitution, Rights & Laws|The Judicial System & How to File an FIR|MCQ Quiz
Social & Political Life (Civics & Economics)|Constitution, Rights & Laws|How Laws are Made: RTI Act, RTE Act & Domestic Violence Act|MCQ Quiz
Social & Political Life (Civics & Economics)|Constitution, Rights & Laws|Civics: Constitution, Rights & Laws (LO #436)|MCQ Quiz
Social & Political Life (Civics & Economics)|Constitution, Rights & Laws|Civics: Constitution, Rights & Laws (LO #437)|MCQ Quiz
Social & Political Life (Civics & Economics)|Elections & Constituencies|Civics: Elections & Constituencies (LO #438)|MCQ Quiz
Social & Political Life (Civics & Economics)|Elections & Constituencies|Civics: Elections & Constituencies (LO #439)|MCQ Quiz
Social & Political Life (Civics & Economics)|Markets, Economy & Public Facilities|Civics: Markets, Economy & Public Facilities (LO #440)|MCQ Quiz
`;

  const ACTIVITIES = [];
  const CURRICULUM_DATA = {};
  let cls = '', subject = '';
  const counters = {};

  RAW.split('\n').forEach(function (line) {
    line = line.trim();
    if (!line) return;
    if (line[0] === '@') { cls = line.slice(1); CURRICULUM_DATA[cls] = {}; return; }
    if (line[0] === '!') { subject = line.slice(1); CURRICULUM_DATA[cls][subject] = {}; return; }
    const p = line.split('|');
    const skill = p[0];
    const sub = p[1], name = p[2], type = p[3];
    const ck = cls + '-' + (SUBJECT_CODE[subject] || 'GEN');
    counters[ck] = (counters[ck] || 0) + 1;
    const id = ck + '-' + String(counters[ck]).padStart(2, '0');
    const act = { id: id, class: cls, subject: subject, skill: skill, subSkill: sub, name: name, type: type, file: 'play.html' };
    ACTIVITIES.push(act);
    const key = skill + ' – ' + sub;
    (CURRICULUM_DATA[cls][subject][key] = CURRICULUM_DATA[cls][subject][key] || []).push(act);
  });

  function getActivity(id) { return ACTIVITIES.find(function (a) { return a.id === id; }); }

  root.ACTIVITIES = ACTIVITIES;
  root.CURRICULUM_DATA = CURRICULUM_DATA;
  root.getActivity = getActivity;
  if (typeof module !== 'undefined' && module.exports) module.exports = { ACTIVITIES, CURRICULUM_DATA, getActivity };
})(typeof window !== 'undefined' ? window : globalThis);
