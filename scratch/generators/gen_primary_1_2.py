# -*- coding: utf-8 -*-
"""
Generator for Class I and Class II Educational Activities (Outcomes 1 - 47).
Pure child-centered learning tasks, zero curriculum meta-talk, realistic student distractors.
"""

PRIMARY_GAMES = {
    # ---------------- CLASS I (Outcomes 1 to 25) ----------------
    1: {
        "title": "Classroom Helpers: Follow the Teacher's Words! 🏫",
        "story": "Miss Anita's classroom is getting ready for morning story time. She gives two gentle instructions so everyone can hear and enjoy the book together.",
        "questions": [
            {
                "prompt": "Miss Anita says: 'Please shut the door to keep the hallway quiet.' What should you do?",
                "options": ["Walk to the classroom door and close it gently", "Push the classroom door wide open to hear the hallway", "Close your storybook quietly on your desk", "Sit quietly at your desk and open your school bag"],
                "answer": 0,
                "explanation": "Great listening! 'Shut the door' means walking to the door and closing it gently."
            },
            {
                "prompt": "Miss Anita smiles and says: 'Arjun, please bring me the storybook from the front table.' What should Arjun bring?",
                "options": ["The colorful storybook from the front table", "A box of crayons from his own desk", "His water bottle from the school bag", "A notebook from the bookshelf"],
                "answer": 0,
                "explanation": "Super job! The teacher specifically asked for the storybook from the front table."
            },
            {
                "prompt": "When the teacher asks the class to 'Raise your hand before speaking', what is the right action?",
                "options": ["Hold your hand up in the air and wait your turn", "Call out the answer immediately from your seat", "Stand up and walk to the blackboard", "Whisper the answer to the friend sitting beside you"],
                "answer": 0,
                "explanation": "Spot on! Raising your hand shows you are politely waiting for your turn to speak."
            }
        ]
    },
    2: {
        "title": "Drawing by Ear: The Sunny Park 🎨",
        "story": "Rohan is following an art guide on the radio. The speaker describes shapes step-by-step so Rohan can draw a sunny garden picture on his paper.",
        "questions": [
            {
                "prompt": "The guide says: 'Draw a big, bright circle in the top corner for the sun.' Which shape should Rohan draw?",
                "options": ["A round circle like a coin", "A pointy triangle like a party hat", "A flat square with four sharp corners", "A straight horizontal line across the page"],
                "answer": 0,
                "explanation": "Nice drawing! A round circle represents the glowing sun."
            },
            {
                "prompt": "Next, the voice says: 'Draw three straight rays shining down from the sun.' How many rays should Rohan draw?",
                "options": ["3 straight lines", "1 straight line only", "4 curved squiggles", "2 tiny dots"],
                "answer": 0,
                "explanation": "Exactly right! Counting three rays follows the spoken instruction perfectly."
            },
            {
                "prompt": "Why is it important to listen carefully before you start coloring your drawing?",
                "options": ["So you know which shapes and colors to draw in each step", "So you can turn off the radio guide immediately", "Because you are only allowed to use one dark pencil", "Because you should draw every shape as fast as possible without looking"],
                "answer": 0,
                "explanation": "Listening first helps you put the right colors and shapes in the right place!"
            }
        ]
    },
    3: {
        "title": "Friendly Greetings & Hello Smiles! 👋",
        "story": "Tara meets a new classmate named Kabir on the school bus. Kabir smiles and says, 'Hello! Good morning, how are you today?'",
        "questions": [
            {
                "prompt": "What is the polite and friendly English way for Tara to answer Kabir?",
                "options": ["'I am fine, thank you! How are you?'", "'Don't sit near my school bag!'", "'Give me your pencil right now!'", "'I will not talk to anyone today.'"],
                "answer": 0,
                "explanation": "Warm and polite! Saying 'I am fine, thank you!' is a lovely morning greeting."
            },
            {
                "prompt": "If a classmate cannot hear spoken words, how can you share a warm hello?",
                "options": ["By smiling and waving your hand in sign language", "By shouting louder into their ear", "By turning your back to them", "By closing your eyes tightly"],
                "answer": 0,
                "explanation": "Wonderful! Waving your hand and signing hello is an inclusive, friendly greeting."
            },
            {
                "prompt": "When someone shares their crayons with you, what magic words should you say?",
                "options": ["'Thank you very much!'", "'I wanted the whole box!'", "'Give me more colors!'", "'Mine are better!'"],
                "answer": 0,
                "explanation": "'Thank you' shows gratitude and kindness when someone shares."
            }
        ]
    },
    4: {
        "title": "Capital and Small Letter Safari 🦁",
        "story": "Leo the Lion is sorting wooden alphabet blocks into big parent letters (capitals) and little cub letters (small letters).",
        "questions": [
            {
                "prompt": "Which letter is the CAPITAL partner for the small letter 'b'?",
                "options": ["B", "d", "p", "q"],
                "answer": 0,
                "explanation": "Correct! 'B' is the capital form of small 'b'. Be careful not to confuse 'b' with 'd'!"
            },
            {
                "prompt": "Look at these four letters: [ M, T, a, R ]. Which one is a small (lowercase) letter?",
                "options": ["a", "M", "T", "R"],
                "answer": 0,
                "explanation": "Spot on! 'a' is a small letter, while M, T, and R are all tall capital letters."
            },
            {
                "prompt": "When writing your own name, how should the very first letter begin?",
                "options": ["With a Capital letter", "With a number", "With a small tiny dot only", "With a question mark"],
                "answer": 0,
                "explanation": "Great writing rule! Names always begin with a proud Capital letter."
            }
        ]
    },
    5: {
        "title": "The Blend Express: 'br' and 'fr'! 🚂",
        "story": "The Blend Train has two bouncy engine whistles: 'br-br-br' like a brown bear, and 'fr-fr-fr' like a jumping frog!",
        "questions": [
            {
                "prompt": "Which of these words starts with the 'fr' blend sound?",
                "options": ["Frog", "Book", "Tree", "Ship"],
                "answer": 0,
                "explanation": "Ribbit! 'Frog' begins with the smooth 'fr' sound: f-r-o-g."
            },
            {
                "prompt": "Which word starts with the 'br' sound, just like 'brown'?",
                "options": ["Brother", "Mother", "Sister", "Friend"],
                "answer": 0,
                "explanation": "Spot on! 'Brother' starts with 'br', making the 'br-uh-ther' sound."
            },
            {
                "prompt": "If you blend the sounds /b/ and /r/ together with 'ush', what helpful tool do you get?",
                "options": ["Brush", "Crush", "Rush", "Flush"],
                "answer": 0,
                "explanation": "Br + ush = Brush! You use a brush to paint or tidy your hair."
            }
        ]
    },
    6: {
        "title": "Alphabet Zoo: Letter Sounds A to Z 🐾",
        "story": "Zoya visits the petting zoo where each animal makes a fun letter sound. She listens carefully to match the letter to its starting phonics sound.",
        "questions": [
            {
                "prompt": "Which letter makes the bouncy /d/ sound at the beginning of 'Duck' and 'Dog'?",
                "options": ["D", "B", "T", "P"],
                "answer": 0,
                "explanation": "Super! The letter D makes the /d/ sound in duck, dog, and drum."
            },
            {
                "prompt": "What starting sound does the letter 'S' make in 'Sun', 'Snake', and 'Star'?",
                "options": ["A hissing /s/ sound like a gentle breeze", "A popping /b/ sound like a bubble", "A clicking /k/ sound like a clock", "A buzzing /m/ sound like humming"],
                "answer": 0,
                "explanation": "Sssss! 'S' makes the hissing /s/ sound."
            },
            {
                "prompt": "Which letter comes right between 'P' and 'R' in the alphabet song?",
                "options": ["Q", "O", "S", "M"],
                "answer": 0,
                "explanation": "Singing along: ... N, O, P, Q, R ... 'Q' comes right after P!"
            }
        ]
    },
    7: {
        "title": "Picture and Word Match-Up 🖼️",
        "story": "Ananya is playing a card game where she flips a picture card and finds the exact matching word label.",
        "questions": [
            {
                "prompt": "Ananya sees a picture of an orange fruit that grows juicy on a tree. Which word matches this picture?",
                "options": ["Mango", "Chair", "Shoe", "Pencil"],
                "answer": 0,
                "explanation": "Yum! The word 'Mango' matches the picture of the delicious sweet fruit."
            },
            {
                "prompt": "Which picture matches the word 'TREE'?",
                "options": ["A tall green plant with a wooden trunk and fluttering leaves", "A furry kitten drinking milk", "A flying kite in the sky", "A clock ticking on the wall"],
                "answer": 0,
                "explanation": "Spot on! A tree has a wooden trunk, green leaves, and branches."
            },
            {
                "prompt": "Look at the word: C-A-T. Which animal does this word name?",
                "options": ["A soft purring kitten with whiskers", "A swimming goldfish in a bowl", "A large elephant with a trunk", "A hopping green frog"],
                "answer": 0,
                "explanation": "Meow! C-A-T spells Cat, our purring whiskered friend!"
            }
        ]
    },
    8: {
        "title": "The Thirsty Crow's Clever Idea 🐦",
        "story": "Listen to the mini-story: 'A thirsty crow looked for water on a hot day. He found a tall jug with only a little water at the very bottom. He dropped small pebbles into the jug one by one until the water rose to the top!'",
        "questions": [
            {
                "prompt": "Why was the clever crow dropping pebbles into the tall jug?",
                "options": ["To make the water rise so he could drink it", "To break the glass jug into pieces", "To hide his pebbles from other birds", "To wash the dirty stones"],
                "answer": 0,
                "explanation": "Clever crow! As each stone dropped, the water level rose until he could reach it with his beak."
            },
            {
                "prompt": "How did the crow feel at the beginning of the story?",
                "options": ["Very thirsty on a hot day", "Full and ready to sleep", "Cold in deep winter snow", "Scared of a barking puppy"],
                "answer": 0,
                "explanation": "The story tells us the crow was looking everywhere for water because he was thirsty."
            },
            {
                "prompt": "What does this story teach us about solving problems?",
                "options": ["Using your brain and trying step-by-step can solve tricky problems", "Give up the second something looks hard", "Fly away and cry immediately", "Wait for someone else to do everything"],
                "answer": 0,
                "explanation": "The crow didn't give up; he used patience and pebbles to solve his problem!"
            }
        ]
    },
    9: {
        "title": "Tell Me About You! 🌟",
        "story": "During circle time, Kabir stands up proudly to introduce himself to his new friends in simple, clear English sentences.",
        "questions": [
            {
                "prompt": "Which sentence is the best way for Kabir to tell his friends his age?",
                "options": ["'I am six years old.'", "'My bag is blue.'", "'The bird is singing.'", "'Apples are red.'"],
                "answer": 0,
                "explanation": "'I am six years old' clearly tells Kabir's friends his age!"
            },
            {
                "prompt": "When describing a picture of your family having a picnic, what could you say?",
                "options": ["'We are sitting on the green grass eating sandwiches.'", "'A train runs on iron tracks.'", "'Zero is less than ten.'", "'Pencils are inside the desk.'"],
                "answer": 0,
                "explanation": "That describes the picnic scene directly and paints a happy picture!"
            },
            {
                "prompt": "Complete Kabir's sentence about his favorite sport: 'My favorite game to play is ________.'",
                "options": ["football with my brother", "a yellow pencil", "heavy rain outside", "a sleeping kitten"],
                "answer": 0,
                "explanation": "'Football' is a fun game you can play, completing the sentence nicely."
            }
        ]
    },
    10: {
        "title": "Story Detective: Sequence & Questions 🔍",
        "story": "Maya read a story: 'First, the little caterpillar hatched from an egg. Next, he ate green leaves and grew plump. Finally, he spun a cocoon and turned into a colorful butterfly!'",
        "questions": [
            {
                "prompt": "What happened FIRST in the caterpillar's story?",
                "options": ["He hatched from a tiny egg", "He flew away with bright butterfly wings", "He spun a silky cocoon", "He slept through the whole winter"],
                "answer": 0,
                "explanation": "The story tells us that first of all, the caterpillar hatched from an egg."
            },
            {
                "prompt": "Who is the main character in this little story?",
                "options": ["The growing caterpillar", "A barking puppy", "A soaring eagle", "A swimming turtle"],
                "answer": 0,
                "explanation": "The story follows the wonderful journey of the little caterpillar."
            },
            {
                "prompt": "What curious question could you ask about the story to learn more?",
                "options": ["'How long did the caterpillar sleep inside his cocoon?'", "'What color is my school bag?'", "'Can a chair dance?'", "'Why is math easy?'"],
                "answer": 0,
                "explanation": "Asking how long he stayed in the cocoon is a wonderful question about the story events!"
            }
        ]
    },
    11: {
        "title": "Action Rhyme Time: Hop and Clap! 🎵",
        "story": "The class is reciting the energetic nursery rhyme: 'Two little hands go clap, clap, clap! Two little feet go tap, tap, tap!'",
        "questions": [
            {
                "prompt": "When reciting 'Two little feet go tap, tap, tap!', what action should your feet do?",
                "options": ["Tap gently on the floor in rhythm", "Cover your ears with both hands", "Flap like bird wings in the air", "Close your eyes tightly"],
                "answer": 0,
                "explanation": "Tapping your feet in time with the rhyme brings the song to life!"
            },
            {
                "prompt": "Which word rhymes with 'HOP' in the poem: 'Little rabbit, do not stop, jump and ...'?",
                "options": ["Hop", "Run", "Sit", "Sing"],
                "answer": 0,
                "explanation": "'Hop' and 'stop' end with the matching -op sound, making a perfect rhyme!"
            },
            {
                "prompt": "Why do we use body actions and hand gestures while singing rhymes?",
                "options": ["It makes the rhyme fun to remember and helps us express the words", "Because we are not allowed to say any words", "So that we get tired and fall asleep", "Because rhymes cannot be spoken aloud"],
                "answer": 0,
                "explanation": "Actions make rhymes exciting, memorable, and full of musical energy!"
            }
        ]
    },
    12: {
        "title": "Grammar Garden: Nouns & Prepositions 🌸",
        "story": "Bunny is playing hide-and-seek in the garden. Look at where Bunny and the toys are placed!",
        "questions": [
            {
                "prompt": "Bunny is sitting resting his paws beneath a tall mango tree. Where is Bunny?",
                "options": ["UNDER the tree", "ON TOP OF the clouds", "INSIDE the bird's beak", "BEHIND the Sun"],
                "answer": 0,
                "explanation": "'Under' describes being beneath the branches of the shady tree."
            },
            {
                "prompt": "In the sentence 'The bright SUN warms the little BOY', which words are NOUNS (names of things or people)?",
                "options": ["Sun and Boy", "Warms and Bright", "The and Little", "And and The"],
                "answer": 0,
                "explanation": "'Sun' is a celestial object and 'Boy' is a person, making them naming words (nouns)."
            },
            {
                "prompt": "Choose the best preposition: 'The red apple is sitting ________ the wooden table.'",
                "options": ["ON", "UNDERNEATH the ocean", "THROUGH the keyhole", "BETWEEN the clouds"],
                "answer": 0,
                "explanation": "An apple sits ON the surface of a table."
            }
        ]
    },
    13: {
        "title": "Picture Vocabulary: In the Living Room 🛋️",
        "story": "Look closely at the cozy living room picture: there is a soft sofa, a ticking wall clock, a floor lamp, and a sleeping kitten on the rug.",
        "questions": [
            {
                "prompt": "Which object in the picture tells us what time of the day it is?",
                "options": ["The wall clock", "The soft cushion", "The wooden coffee table", "The window curtain"],
                "answer": 0,
                "explanation": "A clock has hands and numbers to show the exact time of day."
            },
            {
                "prompt": "What do we call the comfortable piece of furniture where three people can sit together?",
                "options": ["Sofa", "Plate", "Spoon", "Toothbrush"],
                "answer": 0,
                "explanation": "A sofa (or couch) is a cozy seat for family and guests."
            },
            {
                "prompt": "What familiar object provides bright light in the room when the sun sets?",
                "options": ["A lamp", "A pillow", "A blanket", "A teacup"],
                "answer": 0,
                "explanation": "A lamp shines light so you can read and see clearly in the evening."
            }
        ]
    },
    14: {
        "title": "Creative Scribbles & Story Drawings 🖍️",
        "story": "After hearing a lovely poem about rainbow rain, Nina takes her wax crayons to draw and scribble what she felt.",
        "questions": [
            {
                "prompt": "If the poem was about a rainy day, which shapes and colors would best show rain falling from clouds?",
                "options": ["Fluffy gray clouds with blue diagonal raindrops falling down", "A bright red fire truck on fire", "A giant yellow desert with no clouds", "Black scribble circles with no paper left"],
                "answer": 0,
                "explanation": "Drawing raindrops falling from clouds matches the poem's rainy theme beautifully."
            },
            {
                "prompt": "Why do artists first make light pencil scribbles and outlines before coloring?",
                "options": ["To plan where characters and shapes will go on the page", "To rip the paper before using paints", "Because you must always erase every single line", "So nobody can see what you are making"],
                "answer": 0,
                "explanation": "Light planning sketches help you decide where to place trees, animals, and houses!"
            },
            {
                "prompt": "What expression would you draw on a character's face if the poem says they received a surprise birthday puppy?",
                "options": ["A big, wide, cheerful smile", "An angry frown with tears", "A bored sleeping face", "No mouth at all"],
                "answer": 0,
                "explanation": "A surprise puppy brings pure joy, so a bright happy smile is perfect!"
            }
        ]
    },
    15: {
        "title": "Three-Letter Word Builders: CVC Words! 🧱",
        "story": "Sam has letter blocks [ F, H, R, A, N, T ]. He wants to slide them together to spell real, everyday words.",
        "questions": [
            {
                "prompt": "Which word spells the animal that lays eggs on the farm: H - E - N?",
                "options": ["Hen", "Hat", "Hop", "Hot"],
                "answer": 0,
                "explanation": "H-E-N spells Hen! A hen clucks and pecks on the farm."
            },
            {
                "prompt": "Combine the sounds /f/ + /a/ + /n/. What cool summer breeze machine does it spell?",
                "options": ["Fan", "Fat", "Fin", "Fun"],
                "answer": 0,
                "explanation": "F-A-N spells Fan! A fan spins to blow cool air on a warm day."
            },
            {
                "prompt": "Which rhyming word matches 'BAT' and 'CAT' and names a furry little squeaking animal?",
                "options": ["Rat", "Run", "Rug", "Red"],
                "answer": 0,
                "explanation": "R-A-T spells Rat, which rhymes with bat and cat!"
            }
        ]
    },
    16: {
        "title": "Fruit Basket Picture Chart 🍎🍌",
        "story": "Priya counted the fruits in the kitchen basket and drew pictures: 4 red apples, 6 yellow bananas, and 2 green pears.",
        "questions": [
            {
                "prompt": "Looking at Priya's fruit chart, which fruit is there the MOST of?",
                "options": ["Bananas (6)", "Apples (4)", "Pears (2)", "All are equal"],
                "answer": 0,
                "explanation": "Bananas have the highest count at 6, which is more than 4 or 2!"
            },
            {
                "prompt": "How many green pears did Priya find in the basket?",
                "options": ["2 pears", "4 pears", "6 pears", "8 pears"],
                "answer": 0,
                "explanation": "Priya counted exactly 2 green pears."
            },
            {
                "prompt": "How many apples and pears are there when you count them together (4 + 2)?",
                "options": ["6", "5", "7", "2"],
                "answer": 0,
                "explanation": "Counting 4 apples plus 2 pears gives 6 fruits in total!"
            }
        ]
    },
    17: {
        "title": "Handspans & Footsteps: Measuring Length 👣",
        "story": "Dev and Meera are measuring things in their room using their own bodies before they ever use a ruler!",
        "questions": [
            {
                "prompt": "Dev places his stretched hand across his math notebook from thumb to pinky. What is this body measure called?",
                "options": ["A hand span", "A footstep", "An arm length", "A finger nail"],
                "answer": 0,
                "explanation": "A hand span is the distance from the tip of your thumb to the tip of your little finger!"
            },
            {
                "prompt": "Meera walks heel-to-toe from her bed to the bedroom door and counts 8 steps. What did she measure?",
                "options": ["The distance across the room using footsteps", "The weight of her school shoes", "How hot the bedroom floor is", "The time it takes to brush her teeth"],
                "answer": 0,
                "explanation": "Footsteps measure the length or distance between two spots on the floor."
            },
            {
                "prompt": "Why might Dev count 6 hand spans across the desk while his teacher counts only 4 hand spans?",
                "options": ["Because the teacher's hands are bigger than Dev's little hands", "Because the desk shrunk while measuring", "Because Dev counted backwards", "Because hand spans cannot measure wood"],
                "answer": 0,
                "explanation": "Since adult hands are bigger, fewer hand spans are needed to cover the same desk!"
            }
        ]
    },
    18: {
        "title": "Toy Car Addition & Subtraction (1 to 20) 🚗",
        "story": "Rishi had 5 colorful toy cars on his carpet track. His uncle gifted him 4 new speed cars for his birthday.",
        "questions": [
            {
                "prompt": "How many toy cars does Rishi have altogether now? (5 + 4)",
                "options": ["9 cars", "8 cars", "1 car", "10 cars"],
                "answer": 0,
                "explanation": "5 + 4 = 9! Counting forward from 5: 6, 7, 8, 9."
            },
            {
                "prompt": "Later, Rishi shared 3 of his 9 cars with his sister Diya. How many cars does Rishi have left? (9 - 3)",
                "options": ["6 cars", "5 cars", "7 cars", "12 cars"],
                "answer": 0,
                "explanation": "9 take away 3 leaves 6 cars on Rishi's track."
            },
            {
                "prompt": "Which two numbers add up to make the number fact 8?",
                "options": ["4 + 4", "5 + 2", "3 + 3", "7 + 2"],
                "answer": 0,
                "explanation": "Double 4 is 8! (4 + 4 = 8)."
            }
        ]
    },
    19: {
        "title": "The Cookie Jar & The Magic of Zero! 🍪",
        "story": "Grandma baked 3 yummy chocolate chip cookies and placed them on a plate. Little puppy Bruno jumped up and ate all 3 cookies!",
        "questions": [
            {
                "prompt": "How many cookies are left on Grandma's plate now? (3 - 3)",
                "options": ["0 (Zero)", "1", "3", "6"],
                "answer": 0,
                "explanation": "When all 3 cookies are eaten, none are left. The number for 'none' is Zero (0)!"
            },
            {
                "prompt": "What does the numeral '0' tell us in counting?",
                "options": ["There are zero objects / nothing in the group", "There are ten objects", "It is the biggest number in the universe", "It means you have two pairs"],
                "answer": 0,
                "explanation": "Zero represents an empty set or having no items left."
            },
            {
                "prompt": "If you have 5 crayons in a tin and add 0 more crayons, how many crayons do you have?",
                "options": ["5 crayons", "0 crayons", "50 crayons", "4 crayons"],
                "answer": 0,
                "explanation": "Adding zero means adding nothing at all, so you still have your 5 crayons!"
            }
        ]
    },
    20: {
        "title": "Counting Star Balloons up to 20 🎈",
        "story": "At the school fair, a clown holds a bunch of shiny star balloons. Ali counts them one by one as they bob in the wind.",
        "questions": [
            {
                "prompt": "Ali counts: 11, 12, 13, 14, __. What number comes next?",
                "options": ["15 (fifteen)", "16", "10", "20"],
                "answer": 0,
                "explanation": "Counting in order: 11, 12, 13, 14, 15!"
            },
            {
                "prompt": "How do you write the number name for the numeral '18'?",
                "options": ["Eighteen", "Eighty", "Eighth", "Eleven"],
                "answer": 0,
                "explanation": "18 is spelled E-i-g-h-t-e-e-n."
            },
            {
                "prompt": "If you have 1 bundle of 10 pencils and 4 loose pencils, how many pencils do you have in total?",
                "options": ["14 pencils", "41 pencils", "10 pencils", "5 pencils"],
                "answer": 0,
                "explanation": "10 + 4 = 14! One ten and four ones make fourteen."
            }
        ]
    },
    21: {
        "title": "Number Detective: Writing Numerals to 99 🕵️",
        "story": "Detective Diya is reading house numbers on Sunshine Lane. She writes down the two-digit numbers in her notebook.",
        "questions": [
            {
                "prompt": "Which numeral represents the number 'Forty-Seven'?",
                "options": ["47", "74", "407", "14"],
                "answer": 0,
                "explanation": "Forty (4 tens) and seven (7 ones) is written as 47!"
            },
            {
                "prompt": "In the number 63, what does the digit '6' stand for?",
                "options": ["6 tens (which equals 60)", "6 ones (which equals 6)", "600", "Zero"],
                "answer": 0,
                "explanation": "In the tens place, 6 represents 6 groups of ten, or 60."
            },
            {
                "prompt": "Which number comes immediately before 80 when counting?",
                "options": ["79", "81", "70", "89"],
                "answer": 0,
                "explanation": "Counting up: 77, 78, 79, 80! 79 comes right before 80."
            }
        ]
    },
    22: {
        "title": "Who Has More? Comparing Numbers to 20 ⚖️",
        "story": "In the playground, Team Green has 12 players and Team Yellow has 15 players lined up for the relay race.",
        "questions": [
            {
                "prompt": "Which team has MORE players on the field?",
                "options": ["Team Yellow (15 players)", "Team Green (12 players)", "Both have the same", "Neither team has players"],
                "answer": 0,
                "explanation": "15 is greater than 12 (15 > 12), so Team Yellow has more players!"
            },
            {
                "prompt": "Which sign correctly compares 8 and 14: 8 [ ___ ] 14?",
                "options": ["< (8 is less than 14)", "> (8 is greater than 14)", "= (8 is equal to 14)", "+"],
                "answer": 0,
                "explanation": "The alligator mouth opens to the bigger number: 8 < 14."
            },
            {
                "prompt": "Look at these three numbers: [ 7, 19, 11 ]. Which one is the GREATEST?",
                "options": ["19", "11", "7", "1"],
                "answer": 0,
                "explanation": "19 is the largest number in this group."
            }
        ]
    },
    23: {
        "title": "Bead & Number Patterns: What Comes Next? 📿",
        "story": "Simran is threading a colorful necklace: Red bead, Blue bead, Red bead, Blue bead... She loves building patterns!",
        "questions": [
            {
                "prompt": "Look at Simran's color pattern: Red, Blue, Red, Blue, ___. Which bead comes next?",
                "options": ["Red bead", "Green bead", "Yellow bead", "Black bead"],
                "answer": 0,
                "explanation": "The repeating rule is Red, Blue! So after Blue comes Red."
            },
            {
                "prompt": "Find the next number in this skip-counting pattern: 2, 4, 6, 8, ___?",
                "options": ["10", "9", "12", "7"],
                "answer": 0,
                "explanation": "We are counting by 2s! 8 + 2 = 10."
            },
            {
                "prompt": "What is the missing number in this step-by-step pattern: 1, 3, 5, 7, ___?",
                "options": ["9", "8", "10", "11"],
                "answer": 0,
                "explanation": "Each number jumps up by 2 (odd numbers): 1, 3, 5, 7, 9!"
            }
        ]
    },
    24: {
        "title": "Rolling Balls and Sliding Boxes! ⚽📦",
        "story": "Arun built a smooth wooden ramp. He tests different objects from his toy box to see which ones roll and which ones slide.",
        "questions": [
            {
                "prompt": "When Arun places a round soccer ball on the ramp, what does it do?",
                "options": ["It rolls smoothly down the ramp", "It slides flat without spinning", "It stays frozen like a cube", "It breaks into squares"],
                "answer": 0,
                "explanation": "Round objects with curved surfaces like balls roll easily!"
            },
            {
                "prompt": "When Arun places a flat wooden pencil box on the ramp, what does it do?",
                "options": ["It slides down on its flat face", "It rolls like a wheel", "It bounces to the ceiling", "It turns into liquid"],
                "answer": 0,
                "explanation": "Objects with flat faces like boxes slide down smooth slopes."
            },
            {
                "prompt": "Which of these everyday objects can BOTH roll and slide?",
                "options": ["A round coin (rolls on its edge, slides on its flat face)", "A spiky jack toy", "A soft square pillow", "A flat piece of paper"],
                "answer": 0,
                "explanation": "A coin has a flat face to slide, and a round curved rim to roll!"
            }
        ]
    },
    25: {
        "title": "Shape Sorter: Sorting Toys by Size and Shape 🧸",
        "story": "Tina has a big toy bin with balls, building blocks, and toy plates. She wants to sort them into tidy groups.",
        "questions": [
            {
                "prompt": "Tina makes a group for all objects that have a ROUND shape. Which item belongs in this group?",
                "options": ["A bouncy tennis ball", "A rectangular book", "A square building block", "A triangular ruler"],
                "answer": 0,
                "explanation": "A tennis ball is completely round, matching the round group!"
            },
            {
                "prompt": "How did Tina sort these buttons: [ Tiny red button, Medium red button, Giant red button ]?",
                "options": ["By size (small, medium, large)", "By color only", "By their weight in kilograms", "By how loud they are"],
                "answer": 0,
                "explanation": "They are sorted from smallest to largest by size."
            },
            {
                "prompt": "If Tina wants to stack items into a tall, stable tower, which shapes are best to use?",
                "options": ["Blocks with flat square surfaces", "Round slippery marbles", "Pointy party hats", "Oval eggs"],
                "answer": 0,
                "explanation": "Flat surfaces rest securely on top of each other without rolling off!"
            }
        ]
    },

    # ---------------- CLASS II (Outcomes 26 to 47) ----------------
    26: {
        "title": "Art Studio: Follow Multi-Step Directions 🖌️",
        "story": "Teacher Maya announces an art challenge: 'Draw a tall green pine tree on the left, a cozy red roof house in the middle, and three flying birds in the sky.'",
        "questions": [
            {
                "prompt": "Where should you draw the cozy house according to Teacher Maya?",
                "options": ["In the middle of your drawing sheet", "Hidden on the back of the paper", "Underneath the desk", "In the top right corner"],
                "answer": 0,
                "explanation": "Teacher Maya clearly said: 'a cozy red roof house in the middle'!"
            },
            {
                "prompt": "How many flying birds should appear in the sky?",
                "options": ["3 flying birds", "1 sitting bird", "10 birds", "0 birds"],
                "answer": 0,
                "explanation": "The instructions asked for three flying birds in the sky."
            },
            {
                "prompt": "What color did Teacher Maya specify for the roof of the house?",
                "options": ["Red", "Purple", "Green", "Black"],
                "answer": 0,
                "explanation": "The instruction mentioned: 'a cozy red roof house'."
            }
        ]
    },
    27: {
        "title": "Courteous Conversations: Polite English Words 💬",
        "story": "Ravi bumps accidentally into his classmate Sara while rushing to line up for lunch.",
        "questions": [
            {
                "prompt": "What is the polite phrase Ravi should say to Sara immediately?",
                "options": ["'I am sorry! Are you alright?'", "'Get out of my way!'", "'You walked into me!'", "'Say nothing and run away'"],
                "answer": 0,
                "explanation": "Saying 'I am sorry!' shows empathy and polite manners."
            },
            {
                "prompt": "When someone asks you: 'How was your weekend?', what is a cheerful, polite response?",
                "options": ["'It was great, thank you! I went to the park. How was yours?'", "'Why are you asking me?'", "'No weekend for you!'", "'I don't remember anything.'"],
                "answer": 0,
                "explanation": "Sharing a polite sentence and asking in return makes a wonderful conversation!"
            },
            {
                "prompt": "When you want to borrow a blue crayon from your desk partner, how should you ask?",
                "options": ["'Please may I borrow your blue crayon?'", "'Hand over the blue crayon right now!'", "'I am taking your crayon!'", "'Give it here!'"],
                "answer": 0,
                "explanation": "Using 'Please may I...' is the polite, respectful way to ask."
            }
        ]
    },
    28: {
        "title": "Junior News Corner: The Baby Panda! 🐼",
        "story": "The teacher reads from the Children's World newspaper page: 'A tiny baby giant panda was born at the city zoo yesterday. He weighs only 100 grams and drinks warm milk every two hours!'",
        "questions": [
            {
                "prompt": "Which adorable baby animal was born at the city zoo according to the news text?",
                "options": ["A baby giant panda", "A baby tiger cub", "A baby blue whale", "A baby kangaroo"],
                "answer": 0,
                "explanation": "The newspaper snippet states: 'A tiny baby giant panda was born at the city zoo'."
            },
            {
                "prompt": "How often does the newborn panda drink warm milk?",
                "options": ["Every two hours", "Once a week", "Only on Sundays", "Once a year"],
                "answer": 0,
                "explanation": "The teacher read: 'drinks warm milk every two hours!'"
            },
            {
                "prompt": "What section of the newspaper shares stories especially written for young readers?",
                "options": ["The Children's Corner", "The stock market table", "The car advertisements", "The real estate classifieds"],
                "answer": 0,
                "explanation": "The Children's Corner features fun stories, comics, and kid news!"
            }
        ]
    },
    29: {
        "title": "Story Flow: The Brave Little Seed 🌱",
        "story": "Read the story: 'First, a little seed slept deep in the warm dark soil. Next, the gentle spring rain and sun helped a green shoot poke up into the air. Finally, it blossomed into a tall yellow sunflower!'",
        "questions": [
            {
                "prompt": "What happened right after the spring rain soaked the ground?",
                "options": ["A green shoot poked up into the air", "It turned back into an egg", "The seed flew into the clouds", "The sunflower lost all its petals"],
                "answer": 0,
                "explanation": "The story sequence says: 'Next, the gentle spring rain and sun helped a green shoot poke up'."
            },
            {
                "prompt": "What did the tiny seed finally become at the end of the story?",
                "options": ["A tall yellow sunflower", "A thorny cactus", "A leafy pine tree", "A mushroom"],
                "answer": 0,
                "explanation": "In the final event: 'Finally, it blossomed into a tall yellow sunflower!'"
            },
            {
                "prompt": "What was the very FIRST event in this story?",
                "options": ["The seed was sleeping deep in the dark soil", "The flower was harvested by a farmer", "The butterfly landed on the stem", "Leaves fell off in winter"],
                "answer": 0,
                "explanation": "The story began with the seed sleeping in the soil."
            }
        ]
    },
    30: {
        "title": "Poem Comprehension: The Flying Kite 🪁",
        "story": "Listen to the poem lines: 'Up in the blue sky, the red kite flies high! It dips and it dances, with the wind it romances!'",
        "questions": [
            {
                "prompt": "What color is the dancing kite described in the poem?",
                "options": ["Red", "Blue", "Black", "Brown"],
                "answer": 0,
                "explanation": "The poem specifically mentions: 'the red kite flies high!'"
            },
            {
                "prompt": "What helps the kite soar high and dance in the sky?",
                "options": ["The gentle blowing wind", "Heavy falling rain", "Thick dark mud", "A falling rock"],
                "answer": 0,
                "explanation": "Kites catch the air currents (wind) to rise and glide through the sky."
            },
            {
                "prompt": "Which word from the poem describes how the kite moves gracefully?",
                "options": ["Dances", "Sleeps", "Barks", "Sinks"],
                "answer": 0,
                "explanation": "The poem says: 'It dips and it dances'!"
            }
        ]
    },
    31: {
        "title": "Curious Questions About Story Characters 🦊",
        "story": "After reading a folk tale about a clever fox and a singing rooster, Varun wants to share his opinion and ask a good question.",
        "questions": [
            {
                "prompt": "Which of these is a thoughtful question to ask about the characters in the story?",
                "options": ["'Why did the clever rooster fly up to the high branch when he saw the fox?'", "'What is 5 plus 5?'", "'Is it raining outside right now?'", "'What color are my socks?'"],
                "answer": 0,
                "explanation": "Asking about the rooster's choice connects directly to character decisions in the story!"
            },
            {
                "prompt": "How can Varun express his personal opinion about the tale politely?",
                "options": ["'I liked the rooster because he stayed calm and outsmarted the fox.'", "'This book has paper pages.'", "'Characters are people or animals.'", "'I won't say anything.'"],
                "answer": 0,
                "explanation": "Sharing why you liked a character explains your personal opinion clearly."
            },
            {
                "prompt": "If you disagree with a classmate's opinion about a story, what is the best way to respond?",
                "options": ["'I see your point, but I felt the ending was surprising because...' ", "'You are wrong, stop talking!'", "'I am leaving the room!'", "'Nobody asked you.'"],
                "answer": 0,
                "explanation": "Polite discussions respect others' ideas while explaining your own thoughts."
            }
        ]
    },
    32: {
        "title": "Singing Rhymes: Twinkle Stars & Movement ⭐",
        "story": "The music teacher leads the class in singing: 'Twinkle, twinkle, little star, how I wonder what you are!' with expressive hand twinkling actions.",
        "questions": [
            {
                "prompt": "What action do children do with their hands when singing 'Twinkle, twinkle'?",
                "options": ["Open and close their fingers like sparkling stars", "Cover their knees with both hands", "Stomp their heavy shoes loudly", "Fold their arms tightly"],
                "answer": 0,
                "explanation": "Fluttering open and closed fingers looks just like glittering starlight!"
            },
            {
                "prompt": "In the song, where does the little star shine so bright?",
                "options": ["'Up above the world so high, like a diamond in the sky'", "'Underneath the carpet on the floor'", "'Inside the closed lunchbox'", "'Behind the kitchen sink'"],
                "answer": 0,
                "explanation": "The rhyme sings: 'Up above the world so high, like a diamond in the sky!'"
            },
            {
                "prompt": "Which two rhyming words end the lines in this famous nursery song?",
                "options": ["Star and Are", "Star and Moon", "Sky and High", "Both 'Star/Are' and 'Sky/High'"],
                "answer": 0,
                "explanation": "'Star' rhymes with 'Are', and 'High' rhymes with 'Sky'!"
            }
        ]
    },
    33: {
        "title": "Preposition Patrol: Before, Between, and After 🚦",
        "story": "Three animals line up at the water trough: Bunny is first, Deer is in the middle, and Fox is last.",
        "questions": [
            {
                "prompt": "Where is the Deer standing in the animal line?",
                "options": ["BETWEEN Bunny and Fox", "BEFORE the whole forest", "AFTER everyone in the world", "UNDER the deep water"],
                "answer": 0,
                "explanation": "'Between' means with an object or friend on either side. Deer is between Bunny and Fox!"
            },
            {
                "prompt": "Look at the order of the alphabet: A, B, C. Which letter comes BEFORE 'B'?",
                "options": ["A", "C", "D", "Z"],
                "answer": 0,
                "explanation": "'A' comes before 'B' in alphabet order."
            },
            {
                "prompt": "Complete the daily habit sentence: 'Wash your hands ________ you sit down to eat lunch.'",
                "options": ["BEFORE", "BETWEEN the bread slices", "BEHIND the refrigerator", "UNDER your chair"],
                "answer": 0,
                "explanation": "Washing hands BEFORE meals keeps germs away from your food!"
            }
        ]
    },
    34: {
        "title": "Pronoun Power: He, She, It, This & That 🦸",
        "story": "Rohan has a pet puppy. His sister Priya is playing with a frisbee in the garden.",
        "questions": [
            {
                "prompt": "Which pronoun correctly replaces 'Priya' in the sentence: 'Priya threw the frisbee'?",
                "options": ["She", "He", "It", "They"],
                "answer": 0,
                "explanation": "'She' is the pronoun used for a girl or woman (Priya)."
            },
            {
                "prompt": "Which pronoun replaces 'the fluffy puppy': 'The puppy is wagging its tail'?",
                "options": ["It", "He", "She", "These"],
                "answer": 0,
                "explanation": "'It' is used for an animal or an object."
            },
            {
                "prompt": "When pointing to a bright bird sitting far away on a high tree branch, which word do you use?",
                "options": ["THAT bird over there", "THIS bird in my hand", "THESE birds right here", "HERE bird"],
                "answer": 0,
                "explanation": "'That' refers to a single object or animal that is far away from you."
            }
        ]
    },
    35: {
        "title": "Describing Words: Colors, Shapes & Textures 🎈",
        "story": "Meena received a giant birthday surprise box wrapped in shiny paper with a silky ribbon.",
        "questions": [
            {
                "prompt": "Which word is an ADJECTIVE that tells the color and shape of the balloon inside: 'Meena blew up a ________ balloon'?",
                "options": ["round pink", "slowly quickly", "balloon string", "flew went"],
                "answer": 0,
                "explanation": "'Round' tells the shape and 'pink' tells the color—both are describing words (adjectives)!"
            },
            {
                "prompt": "Look at the sentence: 'The fluffy teddy bear felt soft and light.' What are the texture words?",
                "options": ["Fluffy and soft", "Teddy and bear", "Felt and and", "Light and toy"],
                "answer": 0,
                "explanation": "'Fluffy' and 'soft' describe how the teddy bear feels to touch."
            },
            {
                "prompt": "Which opposite pair describes the weight of a heavy boulder compared to a bird's feather?",
                "options": ["Heavy and Light", "Round and Square", "Pink and Blue", "Hot and Sweet"],
                "answer": 0,
                "explanation": "A boulder is heavy, while a feather is light!"
            }
        ]
    },
    36: {
        "title": "Poem Response: Write Your Words 📝",
        "story": "After reading a rhyming poem about buzzing bees in a sunflower field, children write their own short impressions in their notebooks.",
        "questions": [
            {
                "prompt": "Which short phrase makes a lovely response to the bee poem?",
                "options": ["'Sweet honey in the hive'", "'12 plus 15 is 27'", "'Trains run on tracks'", "'The door is locked'"],
                "answer": 0,
                "explanation": "'Sweet honey in the hive' connects directly to the busy bees and flowers!"
            },
            {
                "prompt": "If you want to write one sentence about how the poem made you feel, which is the best start?",
                "options": ["'The poem made me feel happy and cheerful.'", "'A noun is a naming word.'", "'Pencils have erasers.'", "'I have two shoes.'"],
                "answer": 0,
                "explanation": "This sentence clearly expresses your personal feeling about the poem."
            },
            {
                "prompt": "What should always come at the very end of your written sentence?",
                "options": ["A full stop (period)", "A comma in the middle", "A capital letter", "A blank blank space"],
                "answer": 0,
                "explanation": "A full stop (.) tells the reader that your complete thought has ended."
            }
        ]
    },
    37: {
        "title": "Sentence Architect: Spaces Between Words 📐",
        "story": "Aarav is learning to write tidy sentences in his four-line notebook. His teacher reminds him to leave a finger space between each word.",
        "questions": [
            {
                "prompt": "Which sentence is written correctly with clear finger spaces between words?",
                "options": ["The dog ran fast.", "Thedogranfast.", "The  dog   ran      fast .", "Thed ogranf ast."],
                "answer": 0,
                "explanation": "'The dog ran fast.' has neat, readable spaces between each separate word!"
            },
            {
                "prompt": "Why do we leave a small space between words when writing?",
                "options": ["So the reader can tell where one word ends and the next begins", "To waste space on the page", "Because letters do not like each other", "To make the writing impossible to read"],
                "answer": 0,
                "explanation": "Spaces make words easy and clear to read!"
            },
            {
                "prompt": "Which word is missing in this sentence: 'The birds ________ in the morning sky.'",
                "options": ["sing", "pencil", "heavy", "underneath"],
                "answer": 0,
                "explanation": "'Sing' is the action word (verb) that fits birds singing happily."
            }
        ]
    },
    38: {
        "title": "Vehicle Survey: Who Uses What? 🚲🚗",
        "story": "Samir and Angelina surveyed how their classmates travel to school. 10 children come by school bus, 6 walk on foot, and 4 ride bicycles.",
        "questions": [
            {
                "prompt": "Based on the collected survey data, how do the GREATEST number of children travel to school?",
                "options": ["By school bus (10 children)", "On foot (6 children)", "By bicycle (4 children)", "By airplane"],
                "answer": 0,
                "explanation": "10 is the largest number in the survey, so the school bus is used most!"
            },
            {
                "prompt": "How many MORE children walk on foot (6) than ride bicycles (4)?",
                "options": ["2 more children (6 - 4 = 2)", "10 more children", "1 more child", "0"],
                "answer": 0,
                "explanation": "6 minus 4 equals 2! 2 more children walk than bike."
            },
            {
                "prompt": "How many total children were surveyed across all three travel methods? (10 + 6 + 4)",
                "options": ["20 children", "16 children", "24 children", "14 children"],
                "answer": 0,
                "explanation": "10 + 6 + 4 = 20 total students in the survey!"
            }
        ]
    },
    39: {
        "title": "Cup & Bucket: Measuring Capacity 🪣",
        "story": "Tina is helping water the garden pots. She fills her little watering mug using a kitchen cup.",
        "questions": [
            {
                "prompt": "Tina finds that 4 small cups of water completely fill 1 mug. How many cups will she need to fill 2 identical mugs?",
                "options": ["8 cups (4 + 4 = 8)", "4 cups", "2 cups", "12 cups"],
                "answer": 0,
                "explanation": "Each mug needs 4 cups, so two mugs need 4 + 4 = 8 cups of water!"
            },
            {
                "prompt": "Which container holds the LARGEST capacity of liquid?",
                "options": ["A big garden bucket", "A medicine dropper", "A soup spoon", "A small teacup"],
                "answer": 0,
                "explanation": "A garden bucket can hold liters of water, far more than spoons or cups!"
            },
            {
                "prompt": "If a pencil is 7 paperclips long and an eraser is 2 paperclips long, how much longer is the pencil?",
                "options": ["5 paperclips longer (7 - 2 = 5)", "9 paperclips", "3 paperclips", "7 paperclips"],
                "answer": 0,
                "explanation": "7 - 2 = 5 paperclips longer."
            }
        ]
    },
    40: {
        "title": "Play Market: Counting Money up to ₹100 💰",
        "story": "Kunal is buying a toy train at the school play store that costs ₹75. He opens his play wallet with ₹50, ₹20, and ₹5 notes.",
        "questions": [
            {
                "prompt": "Which combination of play money notes exactly equals ₹75?",
                "options": ["One ₹50 note, one ₹20 note, and one ₹5 coin", "Three ₹10 notes and one ₹5 coin", "One ₹100 note with no change", "Two ₹20 notes only"],
                "answer": 0,
                "explanation": "50 + 20 + 5 = ₹75! Exactly what Kunal needs for the toy train."
            },
            {
                "prompt": "How many ₹10 play coins do you need to make ₹50?",
                "options": ["5 coins (10, 20, 30, 40, 50)", "2 coins", "10 coins", "50 coins"],
                "answer": 0,
                "explanation": "Five 10-rupee coins add up to ₹50!"
            },
            {
                "prompt": "If Kunal pays with a ₹100 note for a ₹60 book, how much change should the shopkeeper give back? (100 - 60)",
                "options": ["₹40", "₹30", "₹50", "₹10"],
                "answer": 0,
                "explanation": "100 minus 60 leaves ₹40 in change."
            }
        ]
    },
    41: {
        "title": "Calendar Fun: Days of the Week & Months 📅",
        "story": "Ritu loves looking at the classroom calendar to count down the days to Sports Day on Friday!",
        "questions": [
            {
                "prompt": "If today is Tuesday, which day will it be tomorrow?",
                "options": ["Wednesday", "Thursday", "Monday", "Sunday"],
                "answer": 0,
                "explanation": "The days go: Sunday, Monday, Tuesday, Wednesday! Wednesday is tomorrow."
            },
            {
                "prompt": "How many days are there in one complete week?",
                "options": ["7 days", "5 days", "10 days", "12 days"],
                "answer": 0,
                "explanation": "There are 7 days from Monday through Sunday in a full week."
            },
            {
                "prompt": "Which month comes right after July in the calendar year?",
                "options": ["August", "September", "June", "May"],
                "answer": 0,
                "explanation": "January, February, March, April, May, June, July, August! August comes after July."
            }
        ]
    },
    42: {
        "title": "Time Sequences: Hours, Days & Activities ⏰",
        "story": "Kabir thinks about how long different activities take in his daily life: sleeping at night, brushing teeth, and eating lunch.",
        "questions": [
            {
                "prompt": "Which daily activity takes the LONGEST amount of time?",
                "options": ["Sleeping through the night (8 to 9 hours)", "Brushing your teeth (2 minutes)", "Eating an apple (5 minutes)", "Tying your shoelaces (30 seconds)"],
                "answer": 0,
                "explanation": "A full night's restful sleep lasts about 8 to 9 hours, the longest duration!"
            },
            {
                "prompt": "Does a child typically spend a longer time at school or eating a meal?",
                "options": ["At school (about 6 hours)", "Eating a meal (about 20 minutes)", "Both take the exact same time", "Neither takes any time"],
                "answer": 0,
                "explanation": "A school day lasts around 6 hours, which is much longer than a 20-minute meal."
            },
            {
                "prompt": "What unit of time would you use to measure how long summer vacation lasts?",
                "options": ["Weeks or Months", "Seconds", "Minutes", "Hours only"],
                "answer": 0,
                "explanation": "A vacation spans several weeks or months on the calendar!"
            }
        ]
    },
    43: {
        "title": "Balance Scale: Heavier and Lighter ⚖️",
        "story": "Arjun has a simple two-pan balance scale in science class. He places a heavy melon in one pan and an apple in the other.",
        "questions": [
            {
                "prompt": "What happens to the pan holding the heavy watermelon?",
                "options": ["It sinks lower down because it has more weight", "It floats up into the ceiling", "It stays completely flat with the apple", "It disappears"],
                "answer": 0,
                "explanation": "The heavier side pushes down, making that pan sink lower!"
            },
            {
                "prompt": "Which of these two objects is LIGHTER: a plastic feather or a heavy metal lock?",
                "options": ["The plastic feather", "The heavy metal lock", "Both weigh the same as a car", "The lock is lighter"],
                "answer": 0,
                "explanation": "A feather is very light, while a metal lock is dense and heavy."
            },
            {
                "prompt": "When both pans of the balance scale stay exactly level at the same height, what does that tell you?",
                "options": ["Both sides have the exact same weight (equal)", "The left side is much heavier", "The right side is much heavier", "The scale is broken"],
                "answer": 0,
                "explanation": "When the pans balance level, the weights on both sides are equal!"
            }
        ]
    },
    44: {
        "title": "Two-Digit Math Adventures: Toy Shop Problems 🧸",
        "story": "Simran saved ₹34 in her piggy bank. Her grandmother gave her ₹25 more for helping in the flower garden.",
        "questions": [
            {
                "prompt": "How much money does Simran have now in total? (₹34 + ₹25)",
                "options": ["₹59", "₹51", "₹69", "₹49"],
                "answer": 0,
                "explanation": "Add the ones: 4 + 5 = 9. Add the tens: 3 + 2 = 5. Total = ₹59!"
            },
            {
                "prompt": "A baker had 48 muffins on his shelf. He sold 23 muffins in the morning. How many muffins are left? (48 - 23)",
                "options": ["25 muffins", "21 muffins", "35 muffins", "71 muffins"],
                "answer": 0,
                "explanation": "8 - 3 = 5 ones, and 4 - 2 = 2 tens. 48 - 23 = 25 muffins left!"
            },
            {
                "prompt": "There are 26 red kites and 13 blue kites in the park. How many kites are flying in all? (26 + 13)",
                "options": ["39 kites", "38 kites", "13 kites", "49 kites"],
                "answer": 0,
                "explanation": "26 + 13 = 39 kites flying in the sky!"
            }
        ]
    },
    45: {
        "title": "Place Value Champions: Greatest & Smallest (to 99) 🔢",
        "story": "Rohan has two digit cards: [ 3 ] and [ 8 ]. He wants to build two-digit numbers using these digits.",
        "questions": [
            {
                "prompt": "What is the GREATEST two-digit number Rohan can make using the digits 3 and 8 without repeating?",
                "options": ["83", "38", "88", "33"],
                "answer": 0,
                "explanation": "To make the greatest number, put the largest digit (8) in the tens place: 83!"
            },
            {
                "prompt": "What is the SMALLEST two-digit number you can form using the digits 2 and 7?",
                "options": ["27", "72", "22", "77"],
                "answer": 0,
                "explanation": "Put the smaller digit (2) in the tens place: 27!"
            },
            {
                "prompt": "In the number 94, how many tens and how many ones are there?",
                "options": ["9 tens and 4 ones", "4 tens and 9 ones", "94 tens", "0 tens and 94 ones"],
                "answer": 0,
                "explanation": "94 is made of 9 groups of ten (90) and 4 single ones (4)!"
            }
        ]
    },
    46: {
        "title": "Line Explorers: Straight, Slanted and Curved 📏",
        "story": "Ananya is drawing with a wooden ruler and a round drinking glass on a big sheet of cardboard.",
        "questions": [
            {
                "prompt": "When Ananya draws along the straight edge of her wooden ruler, what kind of line does she make?",
                "options": ["A straight line", "A curved wavy line", "A circle line", "A spiral line"],
                "answer": 0,
                "explanation": "Rulers create crisp, perfectly straight lines."
            },
            {
                "prompt": "When Ananya traces around the round rim of her glass, what kind of line does she make?",
                "options": ["A curved line", "A straight vertical line", "A sharp square line", "A zigzag straight line"],
                "answer": 0,
                "explanation": "The rim of a drinking glass produces a smooth, continuous curved line."
            },
            {
                "prompt": "What do we call a straight line that stands tall and straight up like a flagpole?",
                "options": ["A vertical line", "A horizontal line", "A slant line", "A curved loop"],
                "answer": 0,
                "explanation": "A line standing straight up and down is called a vertical line!"
            }
        ]
    },
    47: {
        "title": "3D Shape World: Cones, Cylinders, Spheres & Cuboids 🧊",
        "story": "Leo looks around his kitchen and school bag to spot 3D shapes: an ice cream cone, a soup can, a soccer ball, and a cereal box.",
        "questions": [
            {
                "prompt": "Which 3D shape is completely round like a basketball, with no flat faces or corners?",
                "options": ["Sphere", "Cube", "Cylinder", "Cone"],
                "answer": 0,
                "explanation": "A sphere is a perfectly round 3D solid, just like a ball!"
            },
            {
                "prompt": "What 3D shape does a soup tin or a soda can look like, with two flat circular ends and a curved side?",
                "options": ["Cylinder", "Cone", "Cuboid", "Pyramid"],
                "answer": 0,
                "explanation": "A cylinder has two parallel circular flat faces and a curved surface, just like a soup can."
            },
            {
                "prompt": "What 3D shape has a pointy tip at the top and a circular base, like a party hat or an ice cream treat?",
                "options": ["Cone", "Cuboid", "Sphere", "Cylinder"],
                "answer": 0,
                "explanation": "A party hat is shaped like a cone!"
            }
        ]
    }
}
