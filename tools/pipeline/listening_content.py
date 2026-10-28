"""
Listening passages and story-derived comprehension questions.

Every activity that is treated as a listening task gets a real spoken passage
plus three questions that can ONLY be answered by listening to / reading that
passage. This replaces the old generic "Attention students..." placeholder.

Each entry:
    "Activity Name": {
        "story": "...",                 # the passage read aloud
        "questions": [Q(stem, [4 options], correct_index, why), ...]
    }
"""

import json
import os
from collections import namedtuple


def Q(stem, options, correct, why):
    """Build one comprehension question and validate it."""
    assert len(options) == 4, f"need 4 options: {stem}"
    assert len(set(options)) == 4, f"duplicate options: {stem}"
    assert 0 <= correct < 4, f"bad correct index: {stem}"
    return {
        "question": stem,
        "options": list(options),
        "answer": options[correct],
        "explanation": why,
    }


LISTENING_STORIES = {

    # ------------------------------------------------------------- Class I
    "Letter Sound Safari": {
        "story": (
            "Ravi went to the zoo with his teacher. At the first enclosure he "
            "heard a long 'a' sound from a lion. Next, a butterfly showed him "
            "the word 'apple'. At the bird house a hen clucked and Ravi heard "
            "the short 'u' sound in 'sun'. Last, a monkey made him laugh with "
            "the sound in 'moon'."
        ),
        "questions": [
            Q("Which animal made the long 'a' sound?",
              ["A lion", "A hen", "A monkey", "A butterfly"], 0,
              "The passage says the lion gave a long 'a' sound."),
            Q("Which word was shown by the butterfly?",
              ["Apple", "Sun", "Moon", "Cat"], 0,
              "The butterfly showed the word 'apple'."),
            Q("Where did Ravi hear the short 'u' sound?",
              ["At the bird house", "At the first enclosure", "At the monkey cage",
               "At the entrance"], 0,
              "The hen at the bird house gave the short 'u' sound in 'sun'."),
        ],
    },

    "Listen & Do Adventure": {
        "instructions": [
            "Open your book to page five",
            "Draw a small blue star next to the heading",
            "Read the three sentences aloud",
            "Circle the picture of a red bus",
            "Close your book and wait for the bell",
        ],
        "story": (
            "Attention Class I! Please listen carefully. First, open your book to "
            "page five. Next, draw a small blue star next to the heading. Then "
            "read the three sentences aloud. After that, circle the picture of a "
            "red bus. Last, close your book and wait for the bell."
        ),
        "questions": [
            Q("What must you do first?",
              ["Open the book to page five", "Draw a blue star",
               "Read the sentences", "Circle the bus"], 0,
              "The passage begins with 'First, open your book to page five'."),
            Q("What colour is the star you must draw?",
              ["Red", "Blue", "Green", "Yellow"], 1,
              "The instruction says to draw a small blue star."),
            Q("Which picture must you circle?",
              ["A red bus", "A blue star", "A green leaf", "A yellow bell"], 0,
              "The passage says to circle the picture of a red bus."),
        ],
    },

    "Noun Basket Sort": {
        "story": (
            "Mother gave Meera three baskets. In the first basket she put a "
            "ball, a doll and a kite. In the second basket she put a spoon, a "
            "cup and a plate. In the third basket she put Delhi, her puppy and "
            "a flower. 'Now put every naming word in the right basket,' she said."
        ),
        "questions": [
            Q("Which basket holds the toys?",
              ["The first basket", "The second basket", "The third basket",
               "All three baskets"], 0,
              "The ball, doll and kite are toys and they are in the first basket."),
            Q("How many baskets does Meera have?",
              ["Two", "Three", "Four", "Five"], 1,
              "Mother gave Meera three baskets."),
            Q("Which of these is in the third basket?",
              ["A spoon", "A plate", "A flower", "A kite"], 2,
              "The third basket holds Delhi, the puppy and a flower."),
        ],
    },

    "Story Time Quiz": {
        "story": (
            "A tall tree stood near Nana's house. Every morning a small bird "
            "called Twee came to sing on its top branch. One day a storm broke "
            "the branch and Twee fell into the grass. Nana picked him up gently "
            "and kept him in a box near the window. The next morning Twee sang "
            "again, and this time a whole flock came to listen."
        ),
        "questions": [
            Q("What kind of animal was Twee?",
              ["A cat", "A bird", "A dog", "A fish"], 1,
              "The story says Twee was a small bird."),
            Q("Why did Twee fall?",
              ["A storm broke the branch", "He was flying too fast",
               "A cat chased him", "He was sleeping"], 0,
              "One day a storm broke the branch and Twee fell into the grass."),
            Q("Who looked after Twee?",
              ["Nana", "A farmer", "A shopkeeper", "Nobody"], 0,
              "Nana picked Twee up and kept him near the window."),
        ],
    },

    # ------------------------------------------------------------ Class II
    "Announcement Detective": {
        "story": (
            "Good morning, children. This is your school announcement. The "
            "science exhibition will be held in the back hall on Monday the "
            "twelfth of June. Please bring your model by eight o'clock in the "
            "morning. The lunch break will be thirty minutes longer on that day. "
            "Students who bring paper models must label them with their name and "
            "class. Thank you."
        ),
        "questions": [
            Q("Where will the science exhibition be held?",
              ["In the back hall", "In the playground", "In the library",
               "In the front hall"], 0,
              "The announcement says the back hall."),
            Q("By what time must the models be brought?",
              ["Eight o'clock", "Nine o'clock", "Ten o'clock", "Eleven o'clock"], 0,
              "Please bring your model by eight o'clock in the morning."),
            Q("What must students with paper models do?",
              ["Label them with name and class", "Paint them", "Break them",
               "Sell them"], 0,
              "Paper models must be labelled with the student's name and class."),
        ],
    },

    "Sound Detective": {
        "story": (
            "Anil closed his eyes and listened to his street. First he heard a "
            "bus hiss as it stopped near the corner. Then he heard a shopkeeper "
            "shouting 'Rupees twenty!' Next came a bicycle bell ringing twice. "
            "Finally he heard his mother calling him from the kitchen. Anil "
            "laughed and said, 'My street tells me a story every evening.'"
        ),
        "questions": [
            Q("What did Anil hear first?",
              ["A bicycle bell", "A bus hissing", "His mother calling",
               "The shopkeeper shouting"], 1,
              "First he heard a bus hiss as it stopped near the corner."),
            Q("How many times did the bicycle bell ring?",
              ["Once", "Twice", "Three times", "It did not ring"], 1,
              "The passage says a bicycle bell ringing twice."),
            Q("Who called Anil at the end?",
              ["His father", "His sister", "His mother", "His teacher"], 2,
              "Finally he heard his mother calling him from the kitchen."),
        ],
    },

    "Verb Action Sort": {
        "story": (
            "Every morning Sita does four things before the bus comes. First "
            "she folds her blanket and makes her bed. Next she brushes her "
            "teeth and washes her face. Then she drinks a glass of milk and "
            "eats one banana. Last of all she runs to the gate with her "
            "school bag. After school she writes her homework, packs her bag "
            "and waits for the bus."
        ),
        "questions": [
            Q("Which word tells what Sita does with the blanket?",
              ["Folds", "Blanket", "Morning", "Glass"], 0,
              "'Folds' is the action word in the sentence."),
            Q("Which of these is NOT something Sita does in the morning?",
              ["Drink milk", "Run to the gate", "Pack her bag",
               "Brush her teeth"], 2,
              "Packing her bag happens after school, not in the morning."),
            Q("What does Sita do after writing her homework?",
              ["She packs her bag", "She drinks milk", "She runs to the gate",
               "She folds her blanket"], 0,
              "After school she writes homework, packs her bag and waits."),
        ],
    },

    # ----------------------------------------------------------- Class III
    "Listen & Answer Challenge": {
        "story": (
            "The school fair opened at nine o'clock on Saturday. Reema and her "
            "brother reached the gate at nine fifteen, so they missed the "
            "dancing contest but saw the painting stall. Reema entered her "
            "painting of a peacock and won second prize. She received a "
            "geometry box and a chart of India. By four o'clock her painting was "
            "hung near the entrance for everyone to see."
        ),
        "questions": [
            Q("What time did the fair open?",
              ["Nine o'clock", "Nine fifteen", "Ten o'clock", "Four o'clock"], 0,
              "The school fair opened at nine o'clock on Saturday."),
            Q("Which event did Reema miss?",
              ["The painting stall", "The dancing contest", "The prize-giving",
               "The entrance display"], 1,
              "They arrived late and missed the dancing contest."),
            Q("What did Reema receive as her prize?",
              ["A geometry box", "A bicycle", "A painting set", "A book"], 0,
              "She received a geometry box and a chart of India."),
        ],
    },

    "Parts of Speech Sorter": {
        "story": (
            "The teacher wrote four words on the board: 'river', 'run', 'blue' "
            "and 'quickly'. She asked the children to name each word. Neha said "
            "'river' names a thing, so it is a noun. Imran said 'run' shows an "
            "action, so it is a verb. Meera said 'blue' describes the river, so "
            "it is an adjective. Then the teacher smiled and said 'quickly' "
            "tells how Imran runs, so it is an adverb."
        ),
        "questions": [
            Q("Which word is the adjective in the story?",
              ["River", "Run", "Blue", "Quickly"], 2,
              "Meera said 'blue' describes the river, so it is an adjective."),
            Q("What kind of word is 'quickly'?",
              ["A noun", "A verb", "An adjective", "An adverb"], 3,
              "The teacher said 'quickly' tells how Imran runs, so it is an adverb."),
            Q("Who said 'run' is a verb?",
              ["Neha", "Imran", "Meera", "The teacher"], 1,
              "Imran said 'run' shows an action, so it is a verb."),
        ],
    },

    # ------------------------------------------------------------ Class IV
    "Follow the Steps Race": {
        "instructions": [
            "Take a rectangular sheet of paper",
            "Fold it in half the long way",
            "Fold the top corners down to make a triangle",
            "Press the sides together to form a hull",
            "Fold the bottom points upwards on both sides",
            "Pull the two sides apart gently",
        ],
        "story": (
            "Here is how to make a paper boat. First take a rectangular sheet "
            "of paper and fold it in half the long way. Next fold the top "
            "corners down to make a triangle. Then open the paper slightly and "
            "press the sides together to form a hull. After that fold the "
            "bottom points upwards on both sides. Finally pull the two sides "
            "apart gently until the boat opens. Your boat is ready."
        ),
        "questions": [
            Q("What do you do first when making the boat?",
              ["Fold the top corners down", "Fold the paper in half the long way",
               "Pull the sides apart", "Fold the bottom points up"], 1,
              "First take a rectangular sheet and fold it in half the long way."),
            Q("When do you pull the sides apart?",
              ["First", "After folding the corners down",
               "Last of all", "Before folding in half"], 2,
              "Finally pull the two sides apart gently until the boat opens."),
            Q("What shape do you make by folding the top corners down?",
              ["A circle", "A triangle", "A square", "A star"], 1,
              "Fold the top corners down to make a triangle."),
        ],
    },

    "Listen & Type Challenge": {
        "story": (
            "Good morning everyone. Please write down these three sentences "
            "exactly as you hear them. Sentence one: The library opens at ten "
            "o'clock. Sentence two: Please return the books on Monday. Sentence "
            "three: The library is on the second floor, next to the reading "
            "room. When you finish, check every word before you hand in your "
            "answer sheet."
        ),
        "questions": [
            Q("At what time does the library open?",
              ["At nine o'clock", "At ten o'clock", "At eleven o'clock",
               "At two o'clock"], 1,
              "Sentence one says the library opens at ten o'clock."),
            Q("When must the books be returned?",
              ["On Monday", "On Tuesday", "On Friday", "Next month"], 0,
              "Sentence two says please return the books on Monday."),
            Q("Where is the library?",
              ["On the first floor", "On the second floor", "On the ground floor",
               "Near the gate"], 1,
              "Sentence three says the library is on the second floor."),
        ],
    },

    "Podcast Pop Quiz": {
        "story": (
            "Welcome to our school podcast. Today we visit Uncle Khan's honey "
            "farm. Uncle Khan keeps forty bee boxes beside a field of mustard "
            "flowers. He says bees collect nectar from the flowers and turn it "
            "into honey. In one season Uncle Khan collects about nine hundred "
            "jars of honey. He then packs the jars in straw and sends them to "
            "shops in the nearby town."
        ),
        "questions": [
            Q("How many bee boxes does Uncle Khan keep?",
              ["Fourteen", "Forty", "Four hundred", "Nine hundred"], 1,
              "The podcast says he keeps forty bee boxes."),
            Q("How much honey does he collect in one season?",
              ["About 400 jars", "About 900 jars", "About 90 jars",
               "About 40 jars"], 1,
              "In one season Uncle Khan collects about nine hundred jars."),
            Q("How are the jars packed for transport?",
              ["In straw", "In plastic bags", "In wooden boxes",
               "In cloth sacks"], 0,
              "He packs the jars in straw before sending them to shops."),
        ],
    },

    "Word Role Race": {
        "story": (
            "In the sentence 'The brave girl saved a small kitten', the words "
            "have different jobs. 'The' is an article. 'Brave' is an adjective "
            "because it describes the girl. 'Girl' is a noun because it names "
            "someone. 'Saved' is a verb because it shows an action. 'A' is an "
            "article again, 'small' is an adjective, 'kitten' is a noun, and "
            "the whole sentence tells us the girl performed an action."
        ),
        "questions": [
            Q("Which word is the verb in the sentence?",
              ["Brave", "Girl", "Saved", "Kitten"], 2,
              "'Saved' is a verb because it shows an action."),
            Q("How many nouns does the sentence contain?",
              ["One", "Two", "Three", "Four"], 1,
              "'Girl' and 'kitten' are the two nouns."),
            Q("What job does the word 'brave' do?",
              ["It names someone", "It shows an action", "It describes the girl",
               "It points to a thing"], 2,
              "'Brave' is an adjective because it describes the girl."),
        ],
    },

    # ------------------------------------------------------------- Class V
    "Mission Control Orders": {
        "instructions": [
            "Collect three empty bottles and two lids from the store room",
            "Carry them to the laboratory on the first floor",
            "Wash each bottle",
            "Let the bottles dry in the sun",
            "Label each bottle with your team number",
            "Report to the science teacher",
        ],
        "story": (
            "Attention team, this is mission control. Our mission begins at six "
            "o'clock. First, collect three empty bottles and two lids from the "
            "store room. Next, carry them to the laboratory on the first floor. "
            "Then wash each bottle and let it dry in the sun. After that, label "
            "each bottle with your team number. Finally, report to the science "
            "teacher. Do not begin without the gloves."
        ),
        "questions": [
            Q("What time does the mission begin?",
              ["At five o'clock", "At six o'clock", "At seven o'clock",
               "At eight o'clock"], 1,
              "Mission control says the mission begins at six o'clock."),
            Q("What must the team collect?",
              ["Three bottles and two lids", "Two bottles and three lids",
               "Six bottles", "Three lids only"], 0,
              "Collect three empty bottles and two lids from the store room."),
            Q("Where must the team go after collecting?",
              ["To the store room", "To the laboratory on the first floor",
               "To the playground", "To the office"], 1,
              "Next, carry them to the laboratory on the first floor."),
        ],
    },

    "Story Time Quiz - Class V": {
        "story": (
            "Harriet looked after her grandfather's garden every summer. One "
            "year the mango tree gave only four fruits. Harriet did not "
            "discourage. She watered the roots twice a week, spread compost "
            "around the tree and removed the weeds. The following summer the "
            "tree gave more than two hundred fruits. Her grandfather smiled and "
            "said the hardest work was the watering, not the picking."
        ),
        "questions": [
            Q("How many mangoes did the tree give before Harriet's care?",
              ["Four", "Twenty", "Two hundred", "One"], 0,
              "One year the mango tree gave only four fruits."),
            Q("What did Harriet spread around the tree?",
              ["Compost", "Sand", "Ash", "Salt"], 0,
              "She spread compost around the tree."),
            Q("What did her grandfather say was the hardest work?",
              ["Picking the mangoes", "The watering", "Removing weeds",
               "Planting the tree"], 1,
              "He said the hardest work was the watering, not the picking."),
        ],
    },

    # ------------------------------------------------------------ Class VI
    "Pronunciation Match-Up": {
        "story": (
            "Listen to these pairs of words. In 'record' used as a noun, the "
            "stress falls on the first syllable, so it sounds like 'RE cord'. In "
            "'record' used as a verb, the stress falls on the second syllable, "
            "so it sounds like 're CORD'. Similarly, 'present' is 'PRE sent' "
            "for a gift, but 'pre SENT' for a verb. Write down the word and say "
            "it twice, moving the stress each time."
        ),
        "questions": [
            Q("In 'record' meaning a noun, which syllable is stressed?",
              ["The first", "The second", "Both", "Neither"], 0,
              "The noun is stressed on the first syllable, like 'RE cord'."),
            Q("In 'present' meaning a gift, which syllable is stressed?",
              ["The first", "The second", "Both", "Neither"], 0,
              "A gift is 'PRE sent', stressed on the first syllable."),
            Q("How many different meanings does 'record' have in the passage?",
              ["One", "Two", "Three", "Four"], 1,
              "'Record' is shown as both a noun and a verb."),
        ],
    },

    "Simon Says Challenge – Class VI": {
        "story": (
            "Simon says: touch your nose. Simon says: clap three times. Simon "
            "says: stand on your left foot. Nobody says: jump three times. "
            "Simon says: spell your name quietly. Simon says: count backwards "
            "from ten to six. Nobody says: sit down. Simon says: raise your "
            "right hand."
        ),
        "questions": [
            Q("How many times must the players clap?",
              ["Two", "Three", "Four", "Ten"], 1,
              "Simon says clap three times."),
            Q("Which action has NOBODY says in front of it?",
              ["Touch your nose", "Jump three times", "Stand on your left foot",
               "Raise your right hand"], 1,
              "Nobody says: jump three times."),
            Q("From which number do the players count backwards?",
              ["From five", "From six", "From ten", "From twenty"], 2,
              "Count backwards from ten to six."),
        ],
    },

    "Sound Detective – Class VI": {
        "story": (
            "The science room was silent. Then a thin wire was stretched across "
            "a wooden box and a cup was fixed to its middle. Ravi plucked the "
            "wire and immediately the cup jumped. 'The wire is loose,' he said, "
            "so he tightened it by turning the peg one full turn. When he "
            "plucked again the cup jumped much higher. Then he added a thicker "
            "wire and the cup hardly moved at all."
        ),
        "questions": [
            Q("What did Ravi do first?",
              ["He tightened the peg", "He added a thicker wire",
               "He plucked the wire", "He fixed the cup"], 2,
              "Ravi plucked the wire and the cup jumped."),
            Q("What happened after he tightened the wire?",
              ["The cup stopped moving", "The cup jumped much higher",
               "The wire broke", "The cup fell down"], 1,
              "When he plucked again the cup jumped much higher."),
            Q("What happened when he added a thicker wire?",
              ["The cup jumped higher", "The cup hardly moved",
               "The cup broke", "The wire became longer"], 1,
              "With a thicker wire the cup hardly moved at all."),
        ],
    },

    # ----------------------------------------------------------- Class VII
    "Accent & Stress Spotter": {
        "story": (
            "In British English, the word 'schedule' is usually pronounced "
            "'SHED yool', while many Indian speakers say 'SKED yool'. Both are "
            "understood. In British English 'ask' is 'ASK', but in American "
            "English it is 'ASK'. Notice that the same two-syllable word "
            "'thirteen' changes its stress between British and Indian English. "
            "When you meet an unfamiliar word, say it aloud both ways and use "
            "the one you hear most often."
        ),
        "questions": [
            Q("Which pronunciation does British English usually give 'schedule'?",
              ["SKED yool", "SHED yool", "SKED yul", "SHED ule"], 1,
              "British English usually says 'SHED yool'."),
            Q("What do speakers do when they meet an unfamiliar word?",
              ["They guess silently", "They say it aloud both ways",
               "They write it once", "They avoid it"], 1,
              "Say it aloud both ways and use the one you hear most often."),
            Q("How many syllables does 'thirteen' have?",
              ["One", "Two", "Three", "Four"], 1,
              "'Thirteen' is described as a two-syllable word."),
        ],
    },

    "Announcement Detective – Class VII": {
        "story": (
            "Attention please. Platform number four will now be in use for the "
            "Rajdhani Express. The Rajdhani Express will depart from platform "
            "four at seven twenty-five in the evening. Coaches S seven and S "
            "eight will be attached at the rear. Passengers holding confirmed "
            "tickets should board now. The train will not wait for late "
            "passengers, so the last door will close five minutes before "
            "departure."
        ),
        "questions": [
            Q("From which platform will the Rajdhani Express depart?",
              ["Platform two", "Platform four", "Platform seven", "Platform eight"], 1,
              "The train will depart from platform four."),
            Q("At what time does the train depart?",
              ["7:25 in the morning", "7:25 in the evening", "6:25 in the evening",
               "5:25 in the evening"], 1,
              "It departs at seven twenty-five in the evening."),
            Q("Which coaches are attached at the rear?",
              ["S one and S two", "S seven and S eight", "S four and S five",
               "No coaches are mentioned"], 1,
              "Coaches S seven and S eight will be attached at the rear."),
        ],
    },

    "News Flash Listener": {
        "story": (
            "Good evening. In tonight's news, the state government has opened "
            "three new libraries in villages that had none. Each library will "
            "hold five thousand books. The government also says that the "
            "project to clean the river will begin next month, funded to the "
            "tune of four crore rupees. In sports, the district team won the "
            "final by twenty-two runs."
        ),
        "questions": [
            Q("How many new libraries were opened?",
              ["Three", "Four", "Five", "Six"], 0,
              "The news says three new libraries were opened."),
            Q("How much money is allocated for cleaning the river?",
              ["Three crore rupees", "Four crore rupees", "Five crore rupees",
               "Twenty-two crore rupees"], 1,
              "The river project is funded to the tune of four crore rupees."),
            Q("By how many runs did the district team win?",
              ["Twenty-two", "Thirty-two", "Twelve", "Twenty"], 0,
              "The district team won the final by twenty-two runs."),
        ],
    },

    # ---------------------------------------------------------- Class VIII
    "Follow the Steps Race – Class VIII": {
        "story": (
            "Here is the procedure for testing the pH of a sample. First label "
            "three clean test tubes A, B and C. Next pour five millilitres of "
            "distilled water into each tube. Then add one drop of universal "
            "indicator to tube A, two drops to tube B and three drops to tube "
            "C. After that swirl each tube gently and compare the colours with "
            "the chart. Finally record the matching colour and pH value for "
            "each tube in your notebook."
        ),
        "questions": [
            Q("How much distilled water is poured into each tube?",
              ["Two millilitres", "Three millilitres", "Five millilitres",
               "Ten millilitres"], 2,
              "Pour five millilitres of distilled water into each tube."),
            Q("How many drops of indicator go into tube B?",
              ["One drop", "Two drops", "Three drops", "Four drops"], 1,
              "Add two drops to tube B."),
            Q("What is done after swirling the tubes?",
              ["They are heated", "Colours are compared with the chart",
               "The water is poured out", "The tubes are labelled again"], 1,
              "Swirl gently and compare the colours with the chart."),
        ],
    },

    "Listen & Repeat Lab": {
        "instructions": [
            "Say each tongue twister slowly",
            "Say it again faster",
            "Record yourself the first time",
            "Record yourself the fifth time",
            "Compare the two recordings",
        ],
        "story": (
            "Let us practise tongue twisters. Say this one slowly, then faster: "
            "'She sells seashells by the seashore.' Now try: 'Red leather, "
            "yellow leather.' Finally say: 'A proper copper coffee pot.' Notice "
            "that in each sentence the repeated sounds use different mouth "
            "movements. Record yourself the first time and the fifth time, then "
            "compare the two recordings."
        ),
        "questions": [
            Q("Which tongue twister is given first?",
              ["Red leather, yellow leather",
               "She sells seashells by the seashore",
               "A proper copper coffee pot", "None of them"], 1,
              "Say this one first: she sells seashells by the seashore."),
            Q("How many recordings are compared?",
              ["Two", "Three", "Five", "Ten"], 0,
              "Record yourself the first time and the fifth time, then compare."),
            Q("What does the passage ask you to notice about repeated sounds?",
              ["They use different mouth movements", "They are always silent",
               "They must be written down", "They are unimportant"], 0,
              "The repeated sounds use different mouth movements."),
        ],
    },

    "Radio Ad Detective": {
        "story": (
            "You are listening to a radio advertisement. It says: 'Fresh "
            "coconut water straight from Kerala, delivered to your door in "
            "just two hours. Order before noon on Monday to get a free glass "
            "bottle. Dial 1800-222-333 now. The first one hundred callers each "
            "receive a twenty rupee discount.' The advertisement repeats three "
            "times before another programme begins."
        ),
        "questions": [
            Q("What is being advertised?",
              ["Coconut water", "Mineral water", "Soft drinks", "Milk"], 0,
              "The ad offers fresh coconut water from Kerala."),
            Q("What is the free gift for orders before noon on Monday?",
              ["A free glass bottle", "A free glass", "A discount coupon",
               "A free meal"], 0,
              "Order before noon on Monday to get a free glass bottle."),
            Q("How many callers receive a twenty rupee discount?",
              ["The first fifty", "The first one hundred", "The first two hundred",
               "Every caller"], 1,
              "The first one hundred callers each receive a twenty rupee discount."),
        ],
    },
}


def _load_audio_index():
    """Read audio/index.json produced by tools/make_audio.ps1 (optional)."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio", "index.json")
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return {}, None
    return data.get("stories", {}), data.get("voice")


AUDIO_INDEX, AUDIO_VOICE = _load_audio_index()

try:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "images", "index.json"), encoding="utf-8") as fh:
        IMAGE_ITEMS = json.load(fh).get("items", {})
except (OSError, ValueError):
    IMAGE_ITEMS = {}

for _name, _entry in LISTENING_STORIES.items():
    for _i, _q in enumerate(_entry["questions"]):
        _img = IMAGE_ITEMS.get(f"{_name}|||{_i}")
        if _img:
            _q["image"] = _img

for _name, _entry in LISTENING_STORIES.items():
    _slug = "".join(c if c.isalnum() else "-" for c in _name.lower())
    while "--" in _slug:
        _slug = _slug.replace("--", "-")
    _slug = _slug.strip("-")
    _meta = AUDIO_INDEX.get(_slug)
    if _meta and os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), _meta["file"].replace("/", os.sep))):
        _entry["audio"] = _meta["file"]
        _entry["audio_seconds"] = _meta.get("seconds", 0)
        _entry["audio_words"] = _meta.get("words", len(_entry["story"].split()))


def has_story(activity_name):
    return activity_name in LISTENING_STORIES


def get_story(activity_name):
    entry = LISTENING_STORIES.get(activity_name)
    if not entry:
        return None, []
    return entry["story"], entry["questions"]


def get_audio(activity_name):
    """Return the narration path for a listening activity, or None."""
    entry = LISTENING_STORIES.get(activity_name) or {}
    return entry.get("audio")