// Source: "Skill_Areas - Subskill area.pdf"
// Row format:  Skill Area | Sub-Skill Area | Activity Name | Game Type
// "@X" starts a class, "!Subject" starts a subject. Skill tokens in CAPS are expanded below.

(function (root) {
  const SKILL = {
    NO: 'Numbers & Operations',
    SH: 'Shapes & Spatial Understanding',
    MEAS: 'Measurement (Length, Weight, Capacity, Time, Money)',
    OI: 'Observation & Identification',
    EUR: 'Explanation & Understanding Relationships',
    CG: 'Classification & Grouping',
    PP: 'Past & Present (Change over Time)',
    EER: 'Estimation, Experimentation & Recording',
    MS: 'Mapping & Spatial Skills',
    CE: 'Creative Expression',
    VSO: 'Values, Sensitivity & Opinion',
    VG: 'Vocabulary & Grammar',
    NS: 'Number System',
    RPCA: 'Ratio, Proportion & Commercial Arithmetic',
    ID: 'Identification & Differentiation',
    SII: 'Scientific Inquiry & Investigation',
    EPCE: 'Explaining Processes & Cause-Effect',
    MRR: 'Measurement, Recording & Representation',
    MADL: 'Models & Application in Daily Life',
    EACV: 'Environmental Awareness, Creativity & Values',
    SPL: 'Social & Political Life (Civics & Economics)'
  };

  const SUBJECT_CODE = { 'English': 'ENG', 'Mathematics': 'MAT', 'EVS': 'EVS', 'Science': 'SCI', 'Social Science': 'SOC' };

  const RAW = `
@I
!English
Listening|Following Instructions & Announcements|Listen & Do Adventure|Sequence Order
Listening|Listening Comprehension & Response|Story Time Quiz|MCQ Quiz
Speaking|Recitation & Performance|Rhyme Gap Fill|Fill in the Blank
Speaking|Oral Expression & Narration|Picture Story Teller|Story Builder
Speaking|Questioning|Question Word Match|Match Pairs
Reading|Word Recognition|Sight Word Memory Match|Memory Match
Reading|Phonics & Letter Recognition|Letter Sound Safari|Match Pairs
Writing|Pre-writing|Trace the Pattern Path|Sequence Order
Writing|Word, Sentence & Paragraph Writing|Word Builder|Word Scramble
VG|Vocabulary|Picture Word Hunt|Guess the Word
VG|Parts of Speech|Noun Basket Sort|Sort & Group
!Mathematics
NO|Number Sense & Place Value|Place Value Tower|MCQ Quiz
NO|Addition & Subtraction|Add & Subtract Sprint|Timed Challenge
SH|Classification of Objects|Odd One Out Zoo|Odd One Out
SH|3D Shapes & Nets|Solid Shape Safari|Match Pairs
MEAS|Length & Distance|Ruler Race|MCQ Quiz
Patterns|Number Patterns|Pattern Train|Sequence Order
Data Handling|Data Collection & Interpretation|Tally Marks Survey|MCQ Quiz

@II
!English
Listening|Listening Comprehension & Response|Sound Detective|MCQ Quiz
Listening|Following Instructions & Announcements|Announcement Detective|Sequence Order
Speaking|Recitation & Performance|Poem Performer|Fill in the Blank
Speaking|Questioning|Ask Me Anything Quiz|Match Pairs
Reading|Reading Comprehension|Story Detective|MCQ Quiz
Writing|Pre-writing|Line & Curve Fun|Sequence Order
Writing|Word, Sentence & Paragraph Writing|Sentence Scramble|Word Scramble
VG|Parts of Speech|Verb Action Sort|Sort & Group
!Mathematics
NO|Number Sense & Place Value|Digit Detective|MCQ Quiz
NO|Addition & Subtraction|Number Line Hopper|Timed Challenge
SH|3D Shapes & Nets|Net Builder Puzzle|Match Pairs
SH|2D Shapes & Lines|Shape Sides Sorter|MCQ Quiz
MEAS|Money|Shopkeeper Change Maker|Typing Answer
MEAS|Capacity & Volume|Fill the Jug Challenge|MCQ Quiz
MEAS|Weight|Heavy or Light Balance|MCQ Quiz
MEAS|Time & Calendar|Clock Reader Challenge|MCQ Quiz
Data Handling|Data Collection & Interpretation|Class Survey Counter|MCQ Quiz

@III
!English
Listening|Listening Comprehension & Response|Listen & Answer Challenge|MCQ Quiz
Speaking|Recitation & Performance|Poetry Stage Star|Fill in the Blank
Speaking|Oral Expression & Narration|Story Chain Builder|Story Builder
Reading|Reading Aloud & Fluency|Speed Reader Sprint|Timed Challenge
Reading|Reading Comprehension|Read & Reveal|MCQ Quiz
Reading|Environmental Print & Information|Sign & Label Detective|MCQ Quiz
Writing|Dictation|Spell It Right Dictation|Typing Answer
Writing|Word, Sentence & Paragraph Writing|Paragraph Puzzle|Word Scramble
Writing|Mechanics & Punctuation|Capital & Full Stop Fix-It|Fill in the Blank
VG|Parts of Speech|Parts of Speech Sorter|Sort & Group
VG|Tenses|Past Present Future Race|Fill in the Blank
VG|Vocabulary|Word Wizard Hangman|Guess the Word
!Mathematics
NO|Number Sense & Place Value|Number Expander Race|MCQ Quiz
NO|Addition & Subtraction|Carry & Borrow Challenge|Timed Challenge
NO|Multiplication & Division|Times Table Rocket|Timed Challenge
NO|Estimation & Problem Solving|Guess & Check Jar|MCQ Quiz
SH|2D Shapes & Lines|Line Type Hunter|MCQ Quiz
MEAS|Money|Rupee Market Game|Typing Answer
MEAS|Length & Distance|Near & Far Measure Quest|MCQ Quiz
MEAS|Weight|Kilo & Gram Market|MCQ Quiz
MEAS|Capacity & Volume|Litre Lab|MCQ Quiz
MEAS|Time & Calendar|Calendar Detective|MCQ Quiz
Patterns|Number Patterns|Skip Counting Hop|Sequence Order
Data Handling|Data Representation (Tables & Graphs)|Bar Graph Builder|MCQ Quiz
!EVS
OI|Plants|Plant Parts Match|Match Pairs
OI|Animals & Birds|Animal Homes Match|Match Pairs
OI|Family & Relationships|Family Tree Builder|Match Pairs
OI|Surroundings (Objects, Places & Activities)|My Neighbourhood Explorer|Odd One Out
EUR|Food & Water|Healthy Plate Builder|Sort & Group
EUR|Family & Community|Community Helpers Quiz|MCQ Quiz
CG|Grouping by Features & Properties|Feature Sorting Safari|Sort & Group
PP|Continuity & Change|Then & Now Timeline|Sequence Order
EER|Estimation & Verification|Guess & Check Challenge|MCQ Quiz
EER|Recording & Predicting Patterns|Weather Tracker Predictor|Sequence Order
MS|Map Reading & Directions|Treasure Map Directions|MCQ Quiz
CE|Drawings, Models & Maps|Design My Map|Story Builder
VSO|Rules & Cooperation|Team Rules Scenarios|MCQ Quiz
VSO|Opinion on Social Issues|Speak Up Debate Cards|MCQ Quiz
VSO|Sensitivity, Hygiene & Conservation|Clean & Care Hero|MCQ Quiz

@IV
!English
Listening|Following Instructions & Announcements|Follow the Steps Race|Sequence Order
Listening|Listening Comprehension & Response|Podcast Pop Quiz|MCQ Quiz
Speaking|Recitation & Performance|Verse Voice Challenge|Fill in the Blank
Speaking|Oral Expression & Narration|Tell-It-Your-Way Adventure|Story Builder
Reading|Environmental Print & Information|Notice Board Reader|MCQ Quiz
Reading|Vocabulary in Context|Guess the Meaning Clue Hunt|MCQ Quiz
Reading|Reference Skills|Dictionary ABC Race|Sort & Group
Reading|Reading Aloud & Fluency|Fluent Reader Race|Timed Challenge
Writing|Dictation|Listen & Type Challenge|Typing Answer
Writing|Mechanics & Punctuation|Punctuation Police|Fill in the Blank
Writing|Functional Writing|Letter & Notice Builder|Fill in the Blank
VG|Vocabulary|Synonym Showdown|Guess the Word
VG|Linkers & Connectors|Connector Bridge Builder|Fill in the Blank
VG|Parts of Speech|Word Role Race|Sort & Group
!Mathematics
NO|Multiplication & Division|Multiply Maze|Timed Challenge
NO|Estimation & Problem Solving|Word Problem Detective|MCQ Quiz
NO|Fractions & Decimals|Pizza Slice Fractions|Match Pairs
SH|2D Shapes & Lines|Polygon Parade|MCQ Quiz
SH|3D Shapes & Nets|Shape Net Match|Match Pairs
SH|Symmetry|Mirror Image Match|MCQ Quiz
SH|Spatial Views|Top Side Front View Puzzle|MCQ Quiz
MEAS|Area & Perimeter|Garden Fence Planner|Typing Answer
MEAS|Unit Conversion|Unit Converter Quest|Match Pairs
MEAS|Estimation & Verification of Measures|Estimate then Measure Challenge|MCQ Quiz
MEAS|Problem Solving with Measures|Measure Mystery Word Problems|Typing Answer
MEAS|Time & Calendar|Time Traveller Timetable|MCQ Quiz
Patterns|Number Patterns|Number Pattern Finder|Sequence Order
Patterns|Shape & Geometric Patterns|Shape Pattern Parade|Sequence Order
Data Handling|Data Representation (Tables & Graphs)|Pictograph Detective|MCQ Quiz
!EVS
OI|Plants|Leaf & Tree Spotter|Match Pairs
OI|Animals & Birds|Bird & Beak Detective|Match Pairs
OI|Family & Relationships|Relationship Riddles|Match Pairs
EUR|Animal Behaviour & Family Change|Animal Behaviour Detective|MCQ Quiz
EUR|Work & Livelihood|Who Does What Job?|Match Pairs
EUR|Food & Water|Water Source Sorter|Sort & Group
CG|Grouping by Features & Properties|Group It Right|Sort & Group
PP|Continuity & Change|Changing Times Sorter|Sequence Order
EER|Estimation & Verification|Estimate Then Test|MCQ Quiz
EER|Recording & Predicting Patterns|Pattern Diary|Sequence Order
MS|Map Reading & Directions|Compass Navigator|MCQ Quiz
MS|Using Signs & Information|Sign Spotter|MCQ Quiz
CE|Drawings, Models & Maps|Model Maker Plan|Story Builder
VSO|Opinion on Social Issues|My Opinion Matters|MCQ Quiz
VSO|Sensitivity, Hygiene & Conservation|Hygiene Habits Challenge|MCQ Quiz

@V
!English
Listening|Listening Comprehension & Response|Story Time Quiz – Class V|MCQ Quiz
Listening|Following Instructions & Announcements|Mission Control Orders|Sequence Order
Speaking|Recitation & Performance|Recital Rehearsal|Fill in the Blank
Speaking|Conversation & Polite Expressions|Polite Words Role Play|Story Builder
Speaking|Oral Expression & Narration|Speaker's Spotlight|Story Builder
Reading|Extensive Reading|Book Explorer Quiz|MCQ Quiz
Reading|Reading Comprehension|Passage Pursuit|MCQ Quiz
Reading|Critical Reading|Fact or Opinion Judge|MCQ Quiz
Reading|Reference Skills|Index & Contents Finder|Sort & Group
Reading|Environmental Print & Information|Ad & Poster Decoder|MCQ Quiz
Writing|Dictation|Dictation Dash|Typing Answer
Writing|Word, Sentence & Paragraph Writing|Sentence Architect|Word Scramble
Writing|Creative Writing|Story Starter Spinner|Story Builder
Writing|Functional Writing|Email Maker|Fill in the Blank
VG|Grammar in Use|Grammar Gym|Fill in the Blank
VG|Vocabulary|Word Detective|Guess the Word
VG|Tenses|Tense Time Machine|Fill in the Blank
!Mathematics
NO|Number Sense & Place Value|Big Number Builder|MCQ Quiz
NO|Multiplication & Division|Division Dash|Timed Challenge
NO|Estimation & Problem Solving|Estimate It Fast|MCQ Quiz
NO|Fractions & Decimals|Decimal Dash|Match Pairs
SH|Angles|Angle Sniper|MCQ Quiz
SH|Symmetry|Fold & Flip|MCQ Quiz
SH|3D Shapes & Nets|Cube & Cuboid Challenge|Match Pairs
MEAS|Unit Conversion|Measurement Converter Race|Match Pairs
MEAS|Estimation & Verification of Measures|Guess the Measure Quest|MCQ Quiz
MEAS|Problem Solving with Measures|Real-Life Measures Missions|Typing Answer
Patterns|Number Patterns|What's the Rule? Challenge|Sequence Order
Data Handling|Data Representation (Tables & Graphs)|Table Reader Race|MCQ Quiz
!EVS
EUR|Animals & Birds|Animal Adaptations Quiz|Match Pairs
EUR|Food & Water|Food Journey Quiz|Sort & Group
EUR|Interdependence in Nature|Food Chain Builder|Sequence Order
EUR|Institutions|Institution Match-Up|Match Pairs
EUR|Terrain, Climate & Culture|Terrain & Culture Explorer|Match Pairs
CG|Grouping by Features & Properties|Property Sorter|Sort & Group
PP|Continuity & Change|Past to Present Journey|Sequence Order
EER|Estimation & Verification|Predict & Prove|MCQ Quiz
EER|Recording & Predicting Patterns|Predict the Next Day|Sequence Order
MS|Map Reading & Directions|Route Finder|MCQ Quiz
CE|Drawings, Models & Maps|Draw & Describe|Story Builder
VSO|Opinion on Social Issues|Agree or Disagree Arena|MCQ Quiz
VSO|Sensitivity, Hygiene & Conservation|Save Water Save Energy|MCQ Quiz

@VI
!English
Listening|Listening Comprehension & Response|Sound Detective – Class VI|MCQ Quiz
Listening|Following Instructions & Announcements|Simon Says Challenge – Class VI|Sequence Order
Listening|Language Lab|Pronunciation Match-Up|Typing Answer
Speaking|Recitation & Performance|Rhyme Gap Fill – Class VI|Fill in the Blank
Speaking|Oral Expression & Narration|Picture Story Teller – Class VI|Story Builder
Reading|Reading Comprehension|Comprehension Quest|MCQ Quiz
Reading|Environmental Print & Information|Timetable Treasure Hunt|MCQ Quiz
Reading|Reference Skills|Reference Hunt|Sort & Group
Writing|Dictation|Dictation Derby|Typing Answer
Writing|Word, Sentence & Paragraph Writing|Paragraph Planner|Word Scramble
Writing|Functional Writing|Form Filling Challenge|Fill in the Blank
Writing|Creative Writing|Poem Maker Lab|Story Builder
VG|Vocabulary|Antonym Arena|Guess the Word
VG|Grammar in Use|Error Hunter|Fill in the Blank
!Mathematics
NS|Whole Numbers & Operations|Big Number Bank|Timed Challenge
NS|Factors, Multiples & Divisibility|Factor Finder|Typing Answer
NS|Integers|Number Line Elevator|MCQ Quiz
NS|Fractions, Decimals & Rational Numbers|Fraction Match|Match Pairs
Algebra|Variables & Algebraic Expressions|Mystery Box Algebra|Typing Answer
RPCA|Ratio & Proportion|Recipe Ratio Chef|MCQ Quiz
RPCA|Unitary Method|Price Per Item Shopper|Typing Answer
Geometry|Basic Geometrical Ideas|Point Line Plane Match|Match Pairs
Geometry|Lines & Angles|Angle Pair Detective|MCQ Quiz
Geometry|Symmetry|Symmetry Spotter|MCQ Quiz
Geometry|Triangles & Congruence|Triangle Types Sort|MCQ Quiz
Geometry|Quadrilaterals|Quadrilateral Family Tree|Sort & Group
Geometry|3D Shapes & Visualisation|Faces Edges Vertices Count|MCQ Quiz
Mensuration|Perimeter & Area|Floor Tiler|Typing Answer
Data Handling|Data Representation & Interpretation|Graph Story Reader|MCQ Quiz
!Science
ID|Identification|Mystery Object Identifier|MCQ Quiz
ID|Differentiation|Spot the Difference Lab|Sort & Group
Classification|Classification of Materials, Organisms & Processes|Material Sorting Lab|Sort & Group
SII|Conducting Investigations|Experiment Steps Order|Sequence Order
EPCE|Cause–Effect Relationships|Cause & Effect Match|Match Pairs
EPCE|Explaining Processes & Phenomena|Process Order Puzzle|Sequence Order
MRR|Measurement & Calculation|Lab Measure & Calculate|Typing Answer
MRR|Labelled Diagrams & Flow Charts|Label the Diagram|Match Pairs
MADL|Model Construction|Build-a-Model Plan|Sequence Order
MADL|Application of Concepts in Daily Life|Science in My Day|MCQ Quiz
EACV|Environmental Protection|Eco Hero Choices|MCQ Quiz
EACV|Creativity|Invent-It Challenge|Story Builder
EACV|Scientific Values|Honest Scientist Dilemmas|MCQ Quiz
!Social Science
Geography|Earth & the Solar System|Planet Explorer Quiz|MCQ Quiz
Geography|Maps, Globe & Diagrams|Map Symbols Treasure Hunt|Match Pairs
History|Sources of History|Primary vs Secondary Source Sort|Sort & Group
History|Ancient India|Ancient India Timeline Run|Sequence Order
History|Art, Architecture & Culture|Monument Match-Up|Match Pairs
History|Religious Ideas & Movements|Ideas & Thinkers Quiz|MCQ Quiz
SPL|Diversity & Discrimination|Unity in Diversity Scenarios|MCQ Quiz
SPL|Government|Who Does What in Government|MCQ Quiz
SPL|Markets, Economy & Public Facilities|Market Chain Explorer|Sort & Group

@VII
!English
Listening|Following Instructions & Announcements|Announcement Detective – Class VII|Sequence Order
Listening|Media & Public Listening|News Flash Listener|MCQ Quiz
Listening|Language Lab|Accent & Stress Spotter|Typing Answer
Speaking|Recitation & Performance|Poem Performer – Class VII|Fill in the Blank
Speaking|Questioning|Question Master|Match Pairs
Reading|Reading Comprehension|Inference Investigator|MCQ Quiz
Reading|Critical Reading|Author's Purpose Detective|MCQ Quiz
Reading|Environmental Print & Information|Menu & Brochure Reader|MCQ Quiz
Reading|Extensive Reading|Reading Log Challenge|MCQ Quiz
Writing|Note Taking|Key Point Catcher|Fill in the Blank
Writing|Word, Sentence & Paragraph Writing|Paragraph Polisher|Word Scramble
Writing|Functional Writing|Message Writer|Fill in the Blank
Writing|Creative Writing|Story Dice Challenge|Story Builder
VG|Vocabulary|Word Power Quiz|Guess the Word
VG|Grammar in Use|Grammar Escape Room|Fill in the Blank
!Mathematics
NS|Integers|Temperature Integer Game|MCQ Quiz
NS|Fractions, Decimals & Rational Numbers|Rational Number Line Race|Match Pairs
NS|Exponents, Squares & Roots|Power Up Exponents|Typing Answer
Algebra|Linear Equations|Balance Scale Equation Solver|Typing Answer
Algebra|Variables & Algebraic Expressions|Expression Builder|Typing Answer
RPCA|Ratio & Proportion|Proportion Puzzle|MCQ Quiz
RPCA|Percentage, Profit & Loss, Interest|Sale Season Shopkeeper|Typing Answer
Geometry|Lines & Angles|Parallel Lines Puzzle|MCQ Quiz
Geometry|Triangles & Congruence|Congruence Court|MCQ Quiz
Geometry|Constructions|Construction Steps Builder|Sequence Order
Mensuration|Perimeter & Area|Perimeter & Area Architect|Typing Answer
Data Handling|Measures of Central Tendency|Mean Median Mode Machine|Typing Answer
Data Handling|Probability & Chance|Dice & Coin Chance Lab|MCQ Quiz
Data Handling|Data Representation & Interpretation|Chart Analyst|MCQ Quiz
!Science
ID|Identification|Lab Equipment ID|MCQ Quiz
ID|Differentiation|Living vs Non-Living Sorter|Sort & Group
Classification|Classification of Materials, Organisms & Processes|Organism Classifier|Sort & Group
SII|Conducting Investigations|Fair Test Detective|Sequence Order
EPCE|Cause–Effect Relationships|Chain Reaction Builder|Match Pairs
EPCE|Explaining Processes & Phenomena|Water Cycle Story|Sequence Order
EPCE|Chemical Word Equations|Word Equation Builder|Fill in the Blank
MRR|Measurement & Calculation|Science Calculator Challenge|Typing Answer
MRR|Labelled Diagrams & Flow Charts|Flow Chart Builder|Match Pairs
MRR|Graphs|Science Graph Reader|MCQ Quiz
MADL|Model Construction|Model Maker Blueprint|Sequence Order
MADL|History of Scientific Discoveries|Scientist & Discovery Match|Match Pairs
MADL|Application of Concepts in Daily Life|Everyday Science Scenarios|MCQ Quiz
EACV|Environmental Protection|Green Choices Challenge|MCQ Quiz
EACV|Creativity|Science Inventor Lab|Story Builder
EACV|Scientific Values|Scientist's Code Quiz|MCQ Quiz
!Social Science
Geography|Earth's Interior, Landforms & Atmosphere|Earth Layers Explorer|Sequence Order
Geography|Maps, Globe & Diagrams|Latitude & Longitude Locator|Match Pairs
Geography|Disasters & Management|Disaster Safety Drill|MCQ Quiz
Geography|Environment & Natural Resources|Renewable vs Non-Renewable Sort|Sort & Group
Geography|Human Geography & Development|Settlements & Development Quiz|MCQ Quiz
History|Sources of History|History Detective Sources|Sort & Group
History|Medieval India|Medieval Dynasties Timeline|Sequence Order
History|Art, Architecture & Culture|Heritage Trail Quiz|Match Pairs
History|Religious Ideas & Movements|Bhakti & Reform Movement Match|MCQ Quiz
SPL|Constitution, Rights & Laws|Rights & Duties Court|MCQ Quiz
SPL|Elections & Constituencies|Election Day Simulator|Story Builder
SPL|Gender|Equal Opportunities Scenarios|MCQ Quiz
SPL|Media & Advertising|Ad Detective|MCQ Quiz
SPL|Markets, Economy & Public Facilities|Public Facility Planner|Sort & Group

@VIII
!English
Listening|Following Instructions & Announcements|Follow the Steps Race – Class VIII|Sequence Order
Listening|Media & Public Listening|Radio Ad Detective|MCQ Quiz
Listening|Language Lab|Listen & Repeat Lab|Typing Answer
Speaking|Conversation & Polite Expressions|Greeting Dialogue Game|Story Builder
Speaking|Recitation & Performance|Poetry Stage Star – Class VIII|Fill in the Blank
Speaking|Oral Expression & Narration|Story Chain Builder – Class VIII|Story Builder
Speaking|Questioning|Interview Challenge|Match Pairs
Reading|Critical Reading|Spot the Bias|MCQ Quiz
Reading|Reading Comprehension|Reading Rally|MCQ Quiz
Reading|Extensive Reading|Library Quest|MCQ Quiz
Writing|Functional Writing|Letter & Notice Builder – Class VIII|Fill in the Blank
Writing|Word, Sentence & Paragraph Writing|Writing Workshop|Word Scramble
Writing|Answer Writing|Answer Builder Challenge|Typing Answer
Writing|Creative Writing|Create-a-Character Tale|Story Builder
VG|Grammar in Use|Sentence Fixer|Fill in the Blank
VG|Vocabulary|Vocabulary Vault|Guess the Word
!Mathematics
NS|Fractions, Decimals & Rational Numbers|Decimal Duel|Match Pairs
NS|Factors, Multiples & Divisibility|HCF-LCM Showdown|Typing Answer
NS|Exponents, Squares & Roots|Perfect Square Hunter|Typing Answer
Algebra|Variables & Algebraic Expressions|Variable Value Challenge|Typing Answer
Algebra|Algebraic Identities|Identity Match-Up|Match Pairs
RPCA|Percentage, Profit & Loss, Interest|Profit or Loss Trader|Typing Answer
RPCA|Ratio & Proportion|Ratio Rescue|MCQ Quiz
Geometry|Quadrilaterals|Quad Property Sorter|Sort & Group
Geometry|3D Shapes & Visualisation|3D Visualiser Challenge|MCQ Quiz
Geometry|Constructions|Compass & Ruler Order Game|Sequence Order
Mensuration|Perimeter & Area|Land Plot Planner|Typing Answer
Mensuration|Surface Area & Volume|Box Wrapper Surface Area|Typing Answer
Data Handling|Data Representation & Interpretation|Data Dashboard Detective|MCQ Quiz
Data Handling|Probability & Chance|Probability Predictor|MCQ Quiz
!Science
ID|Differentiation|Physical vs Chemical Change Sorter|Sort & Group
Classification|Classification of Materials, Organisms & Processes|Kingdom Sorting Challenge|Sort & Group
SII|Conducting Investigations|Variable Controller|Sequence Order
EPCE|Cause–Effect Relationships|Why Does It Happen?|Match Pairs
EPCE|Explaining Processes & Phenomena|Phenomena Explainer|Sequence Order
EPCE|Chemical Word Equations|Reaction Recipe Match|Fill in the Blank
MRR|Measurement & Calculation|Measure It Right|Typing Answer
MRR|Microscopy & Slide Preparation|Slide Prep Step Order|Sequence Order
MRR|Labelled Diagrams & Flow Charts|Diagram Detective|Match Pairs
MADL|Model Construction|Model Engineer Challenge|Sequence Order
MADL|Application of Concepts in Daily Life|Real-Life Science Challenge|MCQ Quiz
MADL|History of Scientific Discoveries|Discovery Timeline Challenge|Match Pairs
EACV|Environmental Protection|Save the Planet Decision Maker|MCQ Quiz
EACV|Creativity|Creative Solution Studio|Story Builder
EACV|Scientific Values|Curious & Careful Challenge|MCQ Quiz
!Social Science
Geography|Agriculture & Industries|Farm to Factory Match|Match Pairs
Geography|Maps, Globe & Diagrams|Globe Navigator|Match Pairs
Geography|Disasters & Management|Emergency Response Planner|MCQ Quiz
Geography|Environment & Natural Resources|Resource Manager|Sort & Group
History|Sources of History|Evidence Explorer|Sort & Group
History|Colonial & Modern India|Freedom Struggle Timeline|Sequence Order
History|Art, Architecture & Culture|Architecture Explorer|Match Pairs
SPL|Constitution, Rights & Laws|Constitution Quest|MCQ Quiz
SPL|Elections & Constituencies|Vote & Count Challenge|Story Builder
SPL|Markets, Economy & Public Facilities|Economy Explorer|Sort & Group
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
    const skill = SKILL[p[0]] || p[0];
    const sub = p[1], name = p[2], type = p[3];
    const ck = cls + '-' + SUBJECT_CODE[subject];
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
