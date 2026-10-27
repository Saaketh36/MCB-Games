#!/usr/bin/env python3
"""
Authoritative 440-Activity 3D Diorama Thumbnail Generator for MyClassboard Games.
Synthesizes a unique, whimsical, kid-friendly 3D diorama thumbnail scene
and full AI generation prompt for every single one of the 440 activities
in the curriculum dataset (LO-001 to LO-440).

Strictly adheres to:
1. Deep metadata interpretation (Class, Subject, SkillArea, SubSkillArea, Title, LearningOutcome)
2. Content translation into thematic diorama scenes (no generic numbers/letters; tells student what they will learn)
3. Whimsical 3D floating green island aesthetic (shallow depth of field, tilt-shift, warm sunlight, friendly character faces)
4. UI layout constraints (clean, open gradient sky in upper-right corner for 'Assigned' / status badge)
5. User examples (Cup & Bucket, Play Market, Phonics/Letter Recognition, Environmental Sensitivity)
"""

import json
import re
import os
import sys

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, 'reconfigure'):
        stream.reconfigure(encoding='utf-8', errors='replace')

def clean_title(title):
    # Remove emojis and trailing whitespace
    clean = re.sub(r'[^\w\s\-,:;&\'\/()]+', '', title)
    return clean.strip()

def match_any(ctx, *patterns):
    """Word boundary matching helper that prevents substring collisions (e.g., 'rain' in 'training')."""
    for p in patterns:
        p_lower = p.lower()
        if " " in p_lower:
            if p_lower in ctx:
                return True
        else:
            pattern = r'\b' + re.escape(p_lower) + r'(s|es|ed|ing|er|ers)?\b'
            if re.search(pattern, ctx):
                return True
    return False

def generate_diorama_scene(game):
    gid = game.get('id', '')
    oid = game.get('outcomeId', 0)
    cls = game.get('class', 'I')
    subj = game.get('subject', 'General')
    skill = game.get('skillArea', '')
    subskill = game.get('subSkillArea', '')
    raw_title = game.get('title', '')
    title = clean_title(raw_title)
    lo = game.get('learningOutcome', '')

    # Combine text for topic matching
    ctx = f"{skill} {subskill} {title} {lo}".lower()

    # Universal platform diorama base & lighting
    island_base = (
        "A charming floating miniature green island with rounded mossy turf, layered earthen cliff edges, "
        "scattered tiny white daisies, and soft morning dew"
    )
    camera_lighting = (
        "Isometric 3D diorama perspective, tilt-shift miniature camera, soft shallow depth of field, "
        "warm golden sunlight, gentle pastel ambient occlusion, high-end toy photography aesthetic, "
        "clean gradient sky in the upper-right corner"
    )

    # =========================================================================
    # 1. CANONICAL USER EXAMPLES & HIGH-PRIORITY SIGNATURE SCENES
    # =========================================================================

    # Example 1: Math - Capacity & Volume (Cup & Bucket)
    if "cup & bucket" in ctx or (subj == "Mathematics" and match_any(ctx, "capacity") and match_any(ctx, "cup", "bucket", "spoon", "non-standard")):
        scene_summary = "A whimsical water-measuring station with friendly plastic cups, buckets, and cheerful water droplets."
        hero_props = "various friendly translucent plastic cups, a bright yellow plastic bucket, and a miniature graduated measuring cylinder"
        characters = "a playful miniature hand character, happy water droplet figures with simple smiling faces, and a tiny character ruler"
        action = "a friendly miniature hand character gently pouring sparkling water between cups into a bucket, while smiling water droplets cheer and a tiny character ruler measures the water level"

    # Example 2: Math - Money & Market (Play Market)
    elif "play market" in ctx or (subj == "Mathematics" and match_any(ctx, "money") and match_any(ctx, "market", "note", "coin", "rupee", "stall")):
        scene_summary = "A bustling miniature market stall with friendly coin and bill characters being counted into coin purses."
        hero_props = "a striped canvas awning wooden market stall, tiny fruit crates filled with toy apples, and a vintage toy brass cash register"
        characters = "stylized friendly coin characters with cute faces and shoes, smiling paper bill figures, and cheerful velvet coin purse characters"
        action = "friendly coin and bill characters cheerfully hopping into open coin purses as a shopkeeper teddy bear tallies totals on an abacus"

    # Signature: The Blend Express (LO-005)
    elif "blend express" in ctx or "common blend" in ctx or (match_any(ctx, "blend") and match_any(ctx, "train", "express", "brother", "frog")):
        scene_summary = "A whimsical wooden toy steam train carrying friendly phonetic blend character pairs along scenic tracks."
        hero_props = "a pastel wooden toy train engine puffing fluffy cotton-wool smoke clouds, wooden railway tracks, and miniature signal flags"
        characters = "friendly 'br' (brown bear) and 'fr' (smiling frog) character duos sitting together in open wooden train cars"
        action = "the Blend Express train chugging merrily around a mossy curve while friendly blend characters wave happily from their carriages"

    # Example 3: English - Phonics & Letter Recognition (Storybook)
    elif subj == "English" and (match_any(ctx, "letter recognition", "phonics", "letter sound", "alphabet zoo") or "a-z" in ctx):
        scene_summary = "An open, friendly-looking miniature storybook with 3D character letters emerging and floating above."
        hero_props = "a giant open pop-up storybook with gilded edges resting on moss, wooden letter blocks, and miniature magnifying glasses"
        characters = "friendly 3D character letters with cute eyes and waving arms, and miniature character reading glasses with friendly smiles"
        action = "friendly 3D character letters joyfully emerging from the storybook pages and floating in mid-air, being warmly read by smiling character reading glasses"

    # Signature: The Thirsty Crow (LO-008)
    elif "thirsty crow" in ctx or "crow's clever idea" in ctx or ("crow" in ctx and "pebble" in ctx):
        scene_summary = "A picturesque garden scene depicting Aesop's clever crow dropping shiny pebbles into a vintage water pitcher."
        hero_props = "a clear vintage glass water jug, smooth rounded river pebbles in a small wooden crate, and a stone bird bath"
        characters = "a friendly crow character with bright curious eyes and a feather cap, smiling pebble characters, and happy water droplets"
        action = "the clever crow character dropping a smiling pebble into the glass jug, making the water level rise joyfully with happy droplet splashes"

    # Example 4: Science / EVS - Environment & Sensitivity (Community Garden)
    elif subj in ("Science", "EVS") and (match_any(ctx, "sensitivity", "conservation", "protect") or "planet protector" in ctx or "community garden" in ctx):
        scene_summary = "A child character tending to a miniature community garden with smiling plants and sunbeams."
        hero_props = "raised wooden garden beds with rich soil, a tiny wooden watering can, seedling pots, and a miniature wooden fence"
        characters = "a friendly child character in garden overalls, smiling potted plant characters with green leaves, and a cheerful round sunbeam character"
        action = "the child character gently watering healthy sprouts with a watering can as smiling plant characters thrive and a sunbeam beams warmth from above"

    # Signature: Master Artisans & Heritage Crafts (LO-121)
    elif match_any(ctx, "heritage craft", "master artisan", "potter", "weaver", "artisan", "handloom") or ("craft" in ctx and "livelihood" in ctx):
        scene_summary = "A traditional heritage craft workshop with a spinning pottery wheel, wooden handloom, and embroidery frames."
        hero_props = "a stone potter's wheel with wet clay, a wooden pit-loom strung with vibrant colorful threads, and hand-block stamps"
        characters = "a smiling master artisan badger shaping a clay pot, and a cheerful weaver bird threading colorful patterns"
        action = "the artisan badger gently shaping a smooth clay pot on the spinning wheel while nearby threads weave into radiant textiles"

    # =========================================================================
    # 2. SUBJECT-SCOPED DIORAMA SCENE MATCHERS
    # =========================================================================

    # -------------------------------------------------------------------------
    # A. ENGLISH
    # -------------------------------------------------------------------------
    elif subj == "English":
        # Listening Comprehension & Following Instructions
        if match_any(ctx, "listening", "instruction", "announcement", "listen", "audio", "classroom helper"):
            scene_summary = "A whimsical audio listening garden with a vintage brass gramophone bell, colorful headphones, and musical notes."
            hero_props = "a polished brass gramophone horn blooming among wildflowers, miniature wooden classroom desks, and oversized retro headphones"
            characters = "a smiling radio character with friendly eyes and antenna, dancing musical note figures, and an attentive puppy perking up its ears"
            action = "the cute radio character chiming clear musical tones while dancing note figures guide the puppy along a marked chalk path"

        # Speaking, Recitation, Skits & Drama
        elif match_any(ctx, "speaking", "recitation", "skit", "role play", "rhyme", "oral", "conversation", "poem", "speech"):
            scene_summary = "A miniature garden amphitheater with an open-air timber stage, footlights, and theatrical costume masks."
            hero_props = "a curved wooden stage platform, a vintage standing microphone draped in ivy, and tiny spotlight lanterns"
            characters = "a charismatic songbird character wearing a bow tie, smiling daisy flower spectators swaying in rhythm, and a friendly frog actor"
            action = "the songbird character standing proudly at the microphone delivering poetic lines with animated wings while the flowers cheer"

        # Reading Comprehension, Stories & Literature
        elif match_any(ctx, "reading", "story", "comprehension", "passage", "fluency", "read aloud", "fable", "book"):
            scene_summary = "A cozy treehouse library nestled in a bonsai oak tree with stacks of open pop-up storybooks."
            hero_props = "a miniature glowing lantern hanging from a branch, open pop-up books with castle turrets and sailboats, and a plush armchair"
            characters = "a scholarly owl librarian with round reading glasses, a curious rabbit reading an illustrated page, and living ribbon bookmarks"
            action = "the owl librarian turning giant illustrated pages as paper sailing ships and fairytale castle turrets emerge in miniature 3D"

        # Vocabulary, Synonyms & Antonyms
        elif match_any(ctx, "vocabulary", "synonym", "antonym", "word", "dictionary", "context clue"):
            scene_summary = "A whimsical lexicon garden featuring balance seesaws of opposites and twin floral arches of synonyms."
            hero_props = "a balance seesaw labeled 'Hot' and 'Cold' with matching props, an open illustrated dictionary pedestal, and magnifying loupes"
            characters = "a sunny firefly character ('Light') balancing opposite a sleepy owl character ('Dark'), and twin smiling blossom characters ('Glad' & 'Happy')"
            action = "the smiling synonym blossoms waving identical petal fans while opposite characters play harmoniously on the balance seesaw"

        # Grammar, Parts of Speech & Sentences
        elif match_any(ctx, "grammar", "parts of speech", "noun", "verb", "adjective", "adverb", "tense", "sentence", "preposition", "conjunction", "linker"):
            scene_summary = "A lively language mechanics workshop where colorful parts-of-speech blocks build sturdy sentence bridges."
            hero_props = "color-coded wooden word building blocks (blue nouns, red action verbs, yellow adjectives), and an illuminated word workbench"
            characters = "a smiling noun block with a tiny crown, an energetic verb block wearing rocket boots, and a friendly painter brush for adjectives"
            action = "the verb block with rocket boots propelling a blue noun block across a wooden gap, completing a glowing, grammatically sound sentence"

        # Writing, Punctuation & Creative Expression
        elif match_any(ctx, "writing", "punctuation", "quill", "author", "paragraph", "dictation", "creative writing", "mechanics"):
            scene_summary = "A charming scribe's sanctuary with a giant wooden fountain pen tower, ceramic inkpots, and jumping punctuation marks."
            hero_props = "a carved wooden fountain pen standing like a lighthouse, a ceramic inkwell bubbling with golden shimmer, and parchment scrolls"
            characters = "a friendly feather quill character with expressive cartoon eyes, and lively punctuation figures (smiling question mark & comma)"
            action = "the quill character gliding smoothly across a curling ribbon of parchment, accompanied by a leaping question mark that lands in place"

        else:
            scene_summary = f"A whimsical English language discovery garden themed around {title}."
            hero_props = "open storybook pathways, wooden word blocks, and miniature literary lanterns"
            characters = "friendly reading animal figures and smiling alphabet companions"
            action = f"the friendly characters discovering and demonstrating key language skills for {title}"

    # -------------------------------------------------------------------------
    # B. MATHEMATICS
    # -------------------------------------------------------------------------
    elif subj == "Mathematics":
        # Capacity & Volume
        if match_any(ctx, "capacity", "bucket", "millilitre", "litre", "volume", "jug"):
            scene_summary = "A whimsical water-measuring station with smiling droplet characters, clear graduated jugs, and cheerful buckets."
            hero_props = "translucent pastel plastic measuring cups, a miniature wooden water pump, and colorful graduated cylinders with glowing water levels"
            characters = "happy water droplet figures with simple cute faces, tiny character measuring spoons, and a cheerful miniature bucket character"
            action = "a friendly water droplet character joyfully pouring sparkling blue liquid from a cup into a clear bucket while a tiny character ruler measures the height"

        # Money, Commercial Math & Profit/Loss
        elif match_any(ctx, "money", "rupee", "price", "profit", "loss", "cost", "interest", "discount", "currency"):
            scene_summary = "A bustling miniature market stall with friendly coin and bill characters being counted into coin purses."
            hero_props = "a striped canvas awning wooden market booth, tiny fruit crates filled with toy apples, and a vintage toy brass cash register"
            characters = "friendly coin figures with smiling faces and tiny shoes, walking banknotes with cute eyes, and a cheerful velvet coin purse character"
            action = "smiling coin characters hopping into open coin purses as a cheerful shopkeeper bear figure tallies bills on an abacus"

        # Weight, Balance & Mass
        elif match_any(ctx, "weight", "balance", "kilogram", "heavy", "mass") or match_any(ctx, "gram"):
            scene_summary = "A playful weighing station featuring a vintage polished brass balance scale and friendly weight blocks."
            hero_props = "a polished brass pan balance scale on a wooden table, polished brass weight blocks, and tiny burlap sacks labeled '1 kg' and '500 g'"
            characters = "smiling brass weight characters with friendly faces, a round pumpkin character laughing on one balance pan, and a tiny character feather floating down"
            action = "a cheerful 1 kg weight block smiling on one balance pan while three cute apples balance it perfectly on the other"

        # Lines (Straight, Slanted, Curved)
        elif match_any(ctx, "line explorer", "straight and curved", "slant", "horizontal", "vertical") or (match_any(ctx, "line") and match_any(ctx, "straight", "curved", "orientation")):
            scene_summary = "A playful line drafting garden where straight, slanted, and curved wooden tracks guide rolling marbles."
            hero_props = "colorful straight wooden sticks, flexible bendy bamboo arcs, a smooth chalkboard slate with chalk lines, and a carpenter's level"
            characters = "a friendly smiling ruler character standing tall, a bendy tape measure character curling happily, and rolling wooden marble figures"
            action = "the ruler character guiding colorful straight and curved tracks across the island while cheerful marbles glide smoothly along them"

        # Length, Distance, Perimeter, Area & Mensuration
        elif match_any(ctx, "length", "distance", "metre", "centimetre", "ruler", "perimeter", "area", "mensuration", "surface area"):
            scene_summary = "A creative measuring garden where friendly ruler characters and tape measures explore miniature paths."
            hero_props = "a bright yellow wooden folding ruler, a soft cloth tape measure coiled like a path, and miniature wooden milestone posts"
            characters = "a friendly smiling caterpillar measuring tape crawling along a wooden fence, tiny smiling pencil characters, and a cheerful frog hopper"
            action = "a bendy yellow ruler character with cute eyes measuring the sides of a flower bed, giving a thumbs-up to a tiny snail"

        # 3D Shapes, Nets & Solids
        elif match_any(ctx, "3d shape", "net", "cube", "cuboid", "cylinder", "cone", "sphere", "solid", "visualisation"):
            scene_summary = "A creative paper-folding workshop where colorful pastel nets fold magically into 3D geometric solids."
            hero_props = "colorful origami paper nets unfolding into 3D cubes and pyramids, a wooden drafting compass, and giant glossy wooden geometric solids"
            characters = "smiling wooden cube and sphere characters with cute simple faces, a friendly triangle block waving, and a tiny protractor character"
            action = "a friendly cube character folding its pastel paper sides together while a cute sphere rolls joyfully down a wooden ramp"

        # 2D Shapes, Angles & Geometry
        elif match_any(ctx, "2d", "shape", "angle", "triangle", "quadrilateral", "polygon", "circle", "symmetry", "geometry", "construction"):
            scene_summary = "A colorful geometry playground with vibrant wooden tangrams, drafting compasses, and smiling geometric shapes."
            hero_props = "colorful wooden tangram tiles, an oversized drafting compass drawing chalk circles, and clear acrylic protractor arcs"
            characters = "smiling triangle, square, and circle wooden figures holding hands, and a friendly drafting compass character"
            action = "the drafting compass character smoothly drawing a perfect glowing circle around laughing triangle and square characters"

        # Fractions, Decimals, Percentages & Ratios
        elif match_any(ctx, "fraction", "decimal", "percentage", "ratio", "proportion", "half", "quarter", "unitary"):
            scene_summary = "A delightful bakery kitchen where delicious pies and fruit tarts demonstrate equal fractions."
            hero_props = "a wooden baking board, colorful fraction pie rings in halves, quarters and eighths, and a miniature baker's rolling pin"
            characters = "smiling slice characters with cute faces holding hands to form a complete round tart, and a happy chef hat character"
            action = "two matching half-pie slice characters joyfully snapping together like puzzle pieces on a pedestal to show a complete whole"

        # Time, Clocks & Calendar
        elif match_any(ctx, "time", "clock", "calendar", "hour", "minute", "day"):
            scene_summary = "A whimsical clockmaker's meadow with a giant friendly grandfather clock and cheerful calendar pages."
            hero_props = "a vintage turquoise alarm clock with ringing bells, a spinning miniature sundial, and a miniature wooden desk calendar"
            characters = "a smiling clock face character whose hands wave cheerfully, and animated calendar day tiles hopping along stepping stones"
            action = "the friendly clock character moving its hour and minute hands to chime while cheerful sunlight and moonbeams switch overhead"

        # Data Handling, Graphs, Pictographs & Tally Marks
        elif match_any(ctx, "data", "graph", "tally", "chart", "table", "pictograph", "mean", "median", "central tendency"):
            scene_summary = "A colorful data playground with rising wooden bar chart towers and cheerful tally stick fences."
            hero_props = "stacked colorful wooden counting blocks forming a 3D bar graph, a miniature chalkboard clipboard, and neat tally stick bundles"
            characters = "smiling wooden block characters stacked at different heights waving happily, and a cute owl figure holding a pointer stick"
            action = "stacked block characters celebrating as the tallest bar tower receives a tiny golden star flag at the top"

        # Probability & Chance
        elif match_any(ctx, "probability", "chance", "dice", "spinner"):
            scene_summary = "A whimsical probability pavilion with a rainbow spinning prize wheel and clear marble jars."
            hero_props = "a giant colorful segmented spinning prize wheel, a clear glass jar filled with red and blue marbles, and giant foam dice"
            characters = "a cheerful smiling die character showing dots, and a friendly carnival badger character turning the spinner"
            action = "the friendly badger spinning the rainbow wheel as smiling colored marble characters watch with excitement from their glass jar"

        # Algebra, Linear Equations & Variables
        elif match_any(ctx, "algebra", "linear equation", "variable", "identity", "expression"):
            scene_summary = "A mystical balance garden where equations are solved using seesaw balance scales and mystery gift boxes."
            hero_props = "a polished wooden balance beam scale, golden number token cubes, and glowing wrapped mystery boxes labeled 'x'"
            characters = "a smiling mystery gift box character labeled 'x', cheerful equal sign '=' characters, and a friendly wizard squirrel"
            action = "the wizard squirrel placing number token cubes on one side of the scale to balance the mystery 'x' box, unlocking a golden key"

        # Integers, Negative Numbers & Number Lines
        elif match_any(ctx, "integer", "negative", "number line"):
            scene_summary = "A dual-climate stepping-stone river representing positive sunny stones and cool snowy negative stones along a number line."
            hero_props = "a stone bridge path marked with numbers, a warm sunny bank on the positive side, and a frosty snowy bank on the negative side"
            characters = "a cheerful zero frog sitting at the center dividing point, hopping positive bee characters, and bundled-up negative penguin characters"
            action = "the zero frog character guiding a smiling counter along the numbered stones from negative frosty steps to positive sunny steps"

        # Exponents, Squares, Roots & Powers
        elif match_any(ctx, "exponent", "square root", "cube root", "square", "root") or match_any(ctx, "power"):
            scene_summary = "A crystalline geometric quarry where square tile mosaics and 3D cubic blocks demonstrate powers and roots."
            hero_props = "a pristine grid of square mosaic tiles forming perfect 3x3 and 4x4 squares, polished wooden cube blocks, and a brass square gauge"
            characters = "smiling mosaic tile figures locking into square grids, and a cheerful beaver builder inspecting square root measurements"
            action = "the beaver builder sliding four square tiles together to form a larger smiling square, celebrating the square root relationship"

        # Factors, Multiples & Divisibility
        elif match_any(ctx, "factor", "multiple", "divisib", "prime", "lcm", "hcf"):
            scene_summary = "A bustling fruit orchard where smiling apples and oranges are arranged into equal factor rows and baskets."
            hero_props = "wooden produce crates arranged in rectangular grid arrays, an abacus sorting rack, and chalkboard multiplication tables"
            characters = "cheerful smiling apple characters arranging themselves into neat factor rows of two, three, and six"
            action = "six smiling apples splitting harmoniously into two equal baskets of three, illustrating factors and multiples with joyful grins"

        # Patterns
        elif match_any(ctx, "pattern"):
            scene_summary = "A whimsical kaleidoscope path where repetitive geometric tiles and counting stones form enchanting patterns."
            hero_props = "a winding path of colorful repeating mosaic tiles, wooden pattern blocks, and a brass kaleidoscope lens"
            characters = "smiling tile characters marching in alternating AB-AB patterns, and a cheerful beetle inspector"
            action = "the beetle inspector placing the missing matching tile into the mosaic path to complete the colorful pattern"

        # Default Numbers, Operations & Place Value
        else:
            scene_summary = "A cheerful place-value construction workshop with golden bead towers and abacus stepping stones."
            hero_props = "a smooth wooden abacus with vibrant pastel beads, miniature place-value ten-block towers, and a wooden counting tree"
            characters = "friendly wooden bead characters with smiling faces, a cheerful squirrel counting acorn tokens into baskets, and a smiling piggy bank"
            action = "smiling bead characters marching in orderly columns of ones, tens, and hundreds across a cute wooden bridge"

    # -------------------------------------------------------------------------
    # C. SCIENCE & EVS
    # -------------------------------------------------------------------------
    elif subj in ("Science", "EVS"):
        # Chemical Equations, Reactions, Acids & Bases
        if match_any(ctx, "chemical equation", "acid", "base", "chemical", "reaction", "rust", "solution", "litmus", "corrosion"):
            scene_summary = "A friendly alchemy chemistry lab with bubbling pastel test tubes and glass Florence flasks."
            hero_props = "a miniature wooden test tube rack with colorful bubbling liquid tubes, a glass beaker, and strips of litmus paper"
            characters = "smiling bubble characters rising from a beaker, and a cheerful litmus paper strip turning from red to blue with a grin"
            action = "a cute glass flask bubbling with sparkling pink foam as friendly litmus characters celebrate a safe neutral pH"

        # Fluid Dynamics & Pressure
        elif match_any(ctx, "fluid dynamics", "hydrostatic", "fluid", "pressure", "manometer") or ("depth" in ctx and "liquid" in ctx):
            scene_summary = "A fluid dynamics exploration tank with clear graduated columns, floating pressure sensors, and water jets."
            hero_props = "a transparent acrylic water tank with height markers, U-tube manometer pressure gauges, and miniature brass taps"
            characters = "a friendly diver otter character with cute goggles, smiling water droplet figures, and a cheerful pressure needle"
            action = "the otter character measuring water pressure at different depths as lower taps shoot water jets further across the pool"

        # Electricity & Circuits
        elif match_any(ctx, "electric", "circuit", "battery", "bulb", "conductor", "electroscope", "switch"):
            scene_summary = "A sparkling electrical laboratory diorama with glowing filament bulbs and insulated copper wires."
            hero_props = "a giant translucent AA battery, an open knife switch with brass contacts, and a glowing retro Edison bulb"
            characters = "friendly glowing electron characters with smiling faces, a happy battery character giving a thumbs up, and a smiling lightbulb"
            action = "a smiling switch closing the circuit loop, making the friendly lightbulb character glow brilliantly with golden rays"

        # Magnetism & Magnetic Poles
        elif match_any(ctx, "magnet", "pole", "compass", "attract", "repel"):
            scene_summary = "A magnetic physics playground with red-and-blue horseshoe magnets and floating iron filings."
            hero_props = "a giant glossy red-and-blue horseshoe magnet with 'N' and 'S' poles, a brass pocket compass, and miniature steel paperclips"
            characters = "smiling horseshoe magnet character with magnetic energy waves, and cheerful paperclip characters clinging happily to the pole"
            action = "the horseshoe magnet character gently lifting smiling iron paperclips into an archway through magnetic force"

        # Light, Mirrors, Reflection & Prisms
        elif match_any(ctx, "light", "shadow", "mirror", "reflection", "lens", "prism", "spectrum"):
            scene_summary = "An optical wonder island with glass prisms casting brilliant rainbow beams across polished mirrors."
            hero_props = "a triangular glass optical prism, miniature adjustable brass mirrors on swivels, and a warm ray flashlight beam"
            characters = "a friendly flashlight character shining a bright beam, and dancing rainbow spectrum characters with cute smiling faces"
            action = "a clear beam entering a glass prism and fanning out into a vibrant 7-color rainbow across white card stands"

        # Cells, Microorganisms & Microscopy
        elif match_any(ctx, "cell", "microscope", "microorganism", "bacteria", "fungi", "slide", "organelle"):
            scene_summary = "A microscopic exploration station with a vintage brass microscope and an enlarged friendly plant cell model."
            hero_props = "a brass scientific microscope, prepared glass specimen slides, and an open cutaway 3D plant cell showing organelles"
            characters = "a smiling mitochondria powerhouse character with tiny sunglasses, and a friendly nucleus character waving from the center"
            action = "an explorer looking through a brass microscope at happy, glowing green chloroplast characters generating energy"

        # Sound, Acoustics & Vibrations
        elif match_any(ctx, "sound", "vibration", "ektara", "acoustic", "tuning fork", "loudness", "pitch"):
            scene_summary = "An acoustic sound laboratory where vibrating tuning forks and string instruments create gentle ripple waves."
            hero_props = "a polished steel tuning fork over a shallow water bowl, an Indian folk ektara one-string lute, and wooden acoustic drums"
            characters = "smiling ripple wave characters dancing through the air, and a musical cricket character strumming the ektara"
            action = "the cricket character striking the tuning fork, sending visible circular ripple rings across the water while cheerful soundwaves dance"

        # Heat, Temperature & Conduction
        elif match_any(ctx, "heat", "temperature", "thermometer", "conduction", "convection", "radiation"):
            scene_summary = "A thermal physics pavilion with a giant vintage glass thermometer and conduction metal bars."
            hero_props = "a clear glass thermometer filled with glowing red liquid, brass and iron conduction rods on stands, and miniature candle burners"
            characters = "a cheerful thermometer character with rising red liquid, and friendly heat aura figures with cozy smiles"
            action = "the thermometer character smiling as warm golden heat flows steadily along a brass rod, safely melting a row of wax tokens"

        # Plants, Leaves, Roots, Seeds & Photosynthesis
        elif match_any(ctx, "plant", "leaf", "root", "seed", "flower", "photosynthesis", "sprout"):
            scene_summary = "A lush botanical greenhouse diorama showing the secret root and leaf life of thriving plants."
            hero_props = "a transparent glass greenhouse dome, cross-section soil box showing roots, and a miniature watering can with silver droplets"
            characters = "smiling seed characters sprouting green shoots, a cheerful golden sunbeam character, and friendly earthworms with smiles"
            action = "a cheerful sunbeam character warming green leaves while smiling water droplets hydrate healthy roots beneath clear soil"

        # Animals, Birds, Habitats & Ecosystems
        elif match_any(ctx, "animal", "bird", "habitat", "ecosystem", "nest", "forest", "wildlife"):
            scene_summary = "A vibrant miniature wildlife sanctuary with diverse habitats from woodland nests to lily ponds."
            hero_props = "a miniature mossy hollow log, a woven bird's nest with speckled eggs, and a crystal-clear pebble stream"
            characters = "a friendly hedgehog with a curious face, a smiling bluebird perching on a twig, and a tiny frog on a lily pad"
            action = "forest animal characters sharing berries around a hollow log habitat while a friendly bluebird feeds its chicks"

        # Water, Rain, Water Cycle & Rivers
        elif match_any(ctx, "water", "rain", "river", "cycle", "ocean", "evaporation", "condensation"):
            scene_summary = "A miniature water cycle wonderland with fluffy rainclouds, flowing streams, and a sparkling reservoir."
            hero_props = "a miniature crystal waterfall flowing into a turquoise pond, a tiny water wheel turning, and a soft puffy cotton cloud"
            characters = "smiling raindrop characters parachuting down from a friendly cloud, and a cheerful sunbeam character evaporating water"
            action = "cute water droplet characters happily riding a water wheel and evaporating up toward a smiling, puffy white cloud"

        # Environment, Pollution, Recycling & Waste
        elif match_any(ctx, "environment", "pollution", "recycle", "waste", "nature", "garbage"):
            scene_summary = "An eco-friendly solar-powered community garden with color-coded recycling bins."
            hero_props = "miniature spinning wind turbine, a solar panel bench, colorful sorting bins (green, blue, yellow), and a seedling nursery"
            characters = "smiling recycling bin characters with open lids, a friendly child character planting a sapling, and smiling butterfly figures"
            action = "cheerful characters placing miniature paper and glass items into the smiling recycling bins under a clean blue sky"

        # Food, Cooking, Kitchen & Nutrition
        elif match_any(ctx, "food", "cook", "diet", "kitchen", "digest", "spice", "nutrition"):
            scene_summary = "A cheerful culinary kitchen island showcasing colorful food groups, healthy vegetables, and traditional spice jars."
            hero_props = "a wooden kitchen preparation island, ceramic spice jars, a balanced plate divided into food groups, and a simmering soup pot"
            characters = "smiling carrot and broccoli characters, a cheerful chef mouse with a wooden spoon, and fragrant steam swirl figures"
            action = "the chef mouse arranging colorful vegetable characters onto a balanced meal plate as savory steam swirls rise happily"

        # Human Body, Senses, Teeth & Hygiene
        elif match_any(ctx, "body", "sense", "teeth", "bone", "muscle", "hygiene"):
            scene_summary = "An anatomy discovery clinic featuring five-sense magnifying stations and friendly tooth-brushing models."
            hero_props = "a miniature wooden clinic examination desk, giant toothbrush and shiny tooth model, and interactive sense stations (eye, ear, hand)"
            characters = "a sparkling white tooth character smiling brightly, and friendly magnifying glass characters exploring the five senses"
            action = "a friendly toothbrush character polishing the smiling tooth model until it sparkles with clean golden gleams"

        # Family, Relationships, Neighborhood & Community
        elif match_any(ctx, "family", "relation", "grandparent", "shelter", "community", "mela", "neighborhood", "reunion"):
            scene_summary = "A warm village community courtyard celebrating family bonds, local shelters, and neighborhood traditions."
            hero_props = "a miniature tiled cottage with a welcoming wooden porch, family memory photo frames, and a festive colorful mela tent"
            characters = "friendly child, parent, and grandparent figures sharing stories on a bench, and a smiling family pet"
            action = "the grandparent figure sharing an illustrated storybook with the child on the porch while neighbors gather joyfully"

        else:
            scene_summary = f"A whimsical nature and science inquiry station exploring {title}."
            hero_props = "miniature scientific tools, glass beakers, and colorful discovery artifacts"
            characters = "curious student explorer characters and friendly nature companions"
            action = f"the characters exploring and demonstrating principles of {title} in an outdoor laboratory"

    # -------------------------------------------------------------------------
    # D. SOCIAL SCIENCE
    # -------------------------------------------------------------------------
    elif subj == "Social Science":
        # Public Goods, Regulations & Utilities (Water, Power, Roads)
        if match_any(ctx, "public good", "public facilities", "regulation", "economic justice") or ("water, power" in ctx):
            scene_summary = "A modern model civic town square with clean public water stations, solar streetlights, and public transit."
            hero_props = "a sparkling drinking water fountain pavilion, solar streetlights, a neat bus stop shelter, and an economic market square"
            characters = "smiling civic maintenance worker figures, cheerful commuter passengers, and a friendly bus driver"
            action = "commuters boarding a clean eco-friendly bus as fresh water flows reliably from public drinking taps in the town square"

        # Maps, Globes, Direction & Topography
        elif match_any(ctx, "map", "globe", "direction", "latitude", "longitude", "contour", "scale", "topograph"):
            scene_summary = "A cartographer's lookout island with a giant rotating globe, brass compass rose, and parchment contour maps."
            hero_props = "an antique brass mounted globe, a carved wooden directional signpost (N, S, E, W), and a relief topographic map model"
            characters = "a cheerful compass needle character pointing steadily north, and a friendly explorer fox with a tiny backpack"
            action = "the explorer fox tracing miniature contour mountain lines on a map while the friendly globe spins gently on its axis"

        # Earth, Solar System & Space
        elif match_any(ctx, "solar system", "planet", "earth", "space", "sun", "orbit"):
            scene_summary = "A breathtaking astronomy orrery diorama with polished brass orbital rings and rotating miniature planets."
            hero_props = "a mechanical brass clockwork orrery with concentric orbital rings, a glowing miniature sun orb, and a brass telescope"
            characters = "a smiling planet Earth character with blue oceans and green continents, and a friendly moon character orbiting close by"
            action = "the clockwork orrery turning smoothly as the smiling Earth and colorful planet spheres glide along their golden orbital tracks"

        # Landforms, Mountains, Rivers & Climate
        elif match_any(ctx, "landform", "mountain", "plateau", "river", "climate", "soil", "mineral", "resource", "plain", "desert"):
            scene_summary = "A dramatic geographic terrain diorama featuring snowcapped peaks, layered plateaus, and coastal plains."
            hero_props = "a miniature snowcapped mountain peak, a stepped red-laterite plateau, and a wind-vane weather station"
            characters = "a friendly mountain goat character smiling on a ledge, and cheerful cloud and sun figures indicating weather"
            action = "a gentle miniature river flowing from snowcapped mountain glaciers down through stepped plateaus to a green delta"

        # Agriculture & Farming
        elif match_any(ctx, "agriculture", "crop", "farming", "cultivat"):
            scene_summary = "A picturesque agrarian landscape with terraced emerald paddy fields, irrigation canals, and a granary."
            hero_props = "stepped green terrace fields, a miniature wooden tractor, water irrigation sluice gates, and golden sheaves of wheat"
            characters = "a friendly farmer character with a straw hat, smiling bullock cart figures, and cheerful songbirds in the field"
            action = "the farmer character opening an irrigation sluice to let fresh water nourish the terraced paddy fields under warm sunshine"

        # Ancient India, Harappan Civilization & Archaeology
        elif match_any(ctx, "harappa", "ancient", "archaeology", "indus", "ruin"):
            scene_summary = "An archaeological excavation site with terracotta Harappan brick walls and miniature artifact treasures."
            hero_props = "terracotta brick ruins with a miniature Great Bath pool, carved stone seals, antique pottery urns, and excavation brushes"
            characters = "a friendly archaeologist teddy character with a pith helmet and magnifying glass, and a smiling terracotta figurine"
            action = "the archaeologist dusting off a carved stone seal with a miniature brush next to ancient paved brick water channels"

        # Ashoka, Mauryan Empire, Inscriptions & Heritage
        elif match_any(ctx, "ashoka", "maurya", "pillar", "edict", "monument", "temple", "art, architecture"):
            scene_summary = "A majestic historical heritage monument with polished sandstone pillars, rock edicts, and carved stone archways."
            hero_props = "a polished Ashokan lion capital sandstone column, stone inscription tablets carved with Brahmi script, and temple gateway arches"
            characters = "a wise elder monk character with a scroll, and a friendly stone sculptor figure holding a wooden mallet"
            action = "the elder character admiring peaceful inscriptions on the polished stone pillar as golden sunlight illuminates the lion capital"

        # Medieval India, Mughals & Citadels
        elif match_any(ctx, "medieval", "mughal", "sultanate", "fort", "delhi"):
            scene_summary = "A medieval Indian royal citadel featuring red sandstone gateways, domed chhatris, and a vibrant trade bazaar."
            hero_props = "miniature red sandstone fortress battlements, elegant marble jali screens, ornate arched gateways, and silk canopies"
            characters = "a friendly royal courier pigeon character, and miniature merchant figures trading colorful silks and fragrant spices"
            action = "merchant figures exchanging spices and silks beneath elegant arched sandstone pavilions in the bustling citadel courtyard"

        # Colonial India, Freedom Movement & Charkha
        elif match_any(ctx, "colonial", "freedom", "modern india", "national movement", "british"):
            scene_summary = "A historic independence square featuring a traditional wooden charkha spinning wheel, parchment, and tricolor flags."
            hero_props = "a finely crafted wooden charkha spinning wheel with white cotton thread, historic printing presses, and tricolor bunting"
            characters = "a determined student character carrying a flag of unity, and friendly spinning spool characters turning smoothly"
            action = "the wooden charkha spinning wheel turning steadily as strands of white cotton weave into cloth symbolizing self-reliance"

        # Constitution, Parliament & Judiciary
        elif match_any(ctx, "constitution", "judiciary", "law", "right", "justice", "parliament", "court"):
            scene_summary = "A grand civic forum diorama featuring an illuminated Constitution volume, scales of justice, and a circular parliament rotunda."
            hero_props = "a grand marble circular parliament pavilion with classical pillars, a balance scale of justice, and a gilded open book"
            characters = "a dignified judge owl character holding a tiny gavel, and diverse student citizens holding hands in equality"
            action = "the judge owl character balancing the golden scales of fairness next to the illuminated Constitution as citizens celebrate justice"

        # Elections, Democracy & Local Governance (Gram Panchayats & Municipalities)
        elif match_any(ctx, "panchayat", "municipality", "governance", "government", "election", "vote", "democracy"):
            scene_summary = "A civic village square with a banyan tree assembly, ballot box, and miniature pillar of justice."
            hero_props = "a grand sandstone pillar of justice with scales, an open illuminated Constitution book, and a wooden ballot box"
            characters = "diverse friendly villager figures gathered peacefully under a grand banyan tree, and a smiling ballot character"
            action = "community characters raising hands in a democratic village meeting under the banyan tree next to a gleaming pillar of justice"

        # Diversity, Gender, Equality & Social Justice
        elif match_any(ctx, "diversity", "discrimination", "gender", "women", "mosaic", "empathy"):
            scene_summary = "A vibrant community harmony square where people of diverse cultures build an interlocking mosaic bridge of unity."
            hero_props = "a colorful mosaic bridge crossing a clear garden pond, cultural heritage flags, and round communal gathering benches"
            characters = "diverse friendly child and adult figures wearing regional Indian attire holding hands, and a dove of peace"
            action = "diverse community characters interlocking colorful mosaic bridge pieces together to create an open pathway of shared friendship"

        else:
            scene_summary = f"A historical and civic exploration diorama themed around {title}."
            hero_props = "miniature historic archives, scrolls, and cultural discovery artifacts"
            characters = "friendly citizen explorer figures and historical guide companions"
            action = f"the characters examining evidence and discovering key historical and civic insights for {title}"

    else:
        scene_summary = f"A whimsical learning adventure diorama exploring {title}."
        hero_props = f"miniature discovery apparatus and authentic learning artifacts for {skill}"
        characters = f"cheerful student explorer figures and friendly companions"
        action = f"the characters demonstrating the core principle of {title} in a playful setting"

    # Construct the final prompt string
    image_prompt = (
        f"A highly detailed, whimsical 3D diorama on a floating green island, {camera_lighting}. "
        f"Scene: {scene_summary} Main terrain: {island_base}. "
        f"Props and environment: {hero_props}. "
        f"Animated characters: {characters}. "
        f"Core action: {action}. "
        f"Composition: Beautifully centered isometric diorama with soft shallow depth of field. "
        f"Crucial layout constraint: Ensure the top-right corner features clear open gradient sky to accommodate a UI status badge overlay. "
        f"No generic numbers, no letters, no text, clean high-end 3D toy render style."
    )

    return {
        "id": gid,
        "outcomeId": oid,
        "class": cls,
        "subject": subj,
        "skillArea": skill,
        "subSkillArea": subskill,
        "title": raw_title,
        "cleanTitle": title,
        "learningOutcome": lo,
        "dioramaScene": {
            "summary": scene_summary,
            "islandBase": island_base,
            "heroProps": hero_props,
            "characters": characters,
            "action": action,
            "cameraLighting": camera_lighting
        },
        "imagePrompt": image_prompt
    }

def build_all():
    catalog_path = 'full_games_catalog.json'
    print(f"Reading all activities from {catalog_path}...")
    with open(catalog_path, 'r', encoding='utf-8') as f:
        games = json.load(f)

    total_activities = len(games)
    print(f"Total activities loaded: {total_activities}")
    thumbnails_dataset = []

    for idx, game in enumerate(games):
        entry = generate_diorama_scene(game)
        gid = entry['id']
        jpg_path = os.path.join('images', 'thumbnails', f"{gid}.jpg")
        if os.path.exists(jpg_path):
            thumb_path = f"images/thumbnails/{gid}.jpg"
        else:
            thumb_path = f"images/thumbnails/{gid}.svg"
        entry['thumb'] = thumb_path
        thumbnails_dataset.append(entry)
        # Enrich the game record directly
        game['thumb'] = thumb_path
        game['dioramaScene'] = entry['dioramaScene']
        game['imagePrompt'] = entry['imagePrompt']

    # Ensure output directories exist
    os.makedirs('data', exist_ok=True)

    # 1. Save data/activity_card_thumbnails.json
    out_json = os.path.join('data', 'activity_card_thumbnails.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(thumbnails_dataset, f, indent=2, ensure_ascii=False)
    print(f" Generated full diorama thumbnail catalog: {out_json} ({len(thumbnails_dataset)} items)")

    # 2. Save data/activity_card_thumbnails.js
    out_js = os.path.join('data', 'activity_card_thumbnails.js')
    js_content = "// Authoritative 440-Activity 3D Diorama Card Thumbnail Dataset\n"
    js_content += "const ACTIVITY_CARD_THUMBNAILS = " + json.dumps(thumbnails_dataset, indent=2, ensure_ascii=False) + ";\n\n"
    js_content += "if (typeof window !== 'undefined') {\n"
    js_content += "    window.ACTIVITY_CARD_THUMBNAILS = ACTIVITY_CARD_THUMBNAILS;\n"
    js_content += "}\n"
    js_content += "if (typeof module !== 'undefined' && module.exports) {\n"
    js_content += "    module.exports = { ACTIVITY_CARD_THUMBNAILS };\n"
    js_content += "}\n"
    with open(out_js, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f" Generated JS bundle: {out_js}")

    # 3. Update full_games_catalog.json with the enriched diorama scenes
    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(games, f, indent=2, ensure_ascii=False)
    print(f" Updated {catalog_path} with diorama scenes")

    # 4. Sync full_games_catalog.js
    js_cat_path = 'full_games_catalog.js'
    js_cat_content = "// Authoritative Games Catalog derived STRICTLY from 'skillAreaOutcomes - Sheet1.pdf'\n"
    js_cat_content += "// Total Learning Outcomes / Activities: 440 (Classes I to VIII)\n"
    js_cat_content += "const FULL_GAMES_CATALOG = " + json.dumps(games, indent=2, ensure_ascii=False) + ";\n\n"
    js_cat_content += "if (typeof window !== 'undefined') {\n"
    js_cat_content += "    window.FULL_GAMES_CATALOG = FULL_GAMES_CATALOG;\n"
    js_cat_content += "    window.GamesCatalog = FULL_GAMES_CATALOG;\n"
    js_cat_content += "}\n"
    js_cat_content += "if (typeof module !== 'undefined' && module.exports) {\n"
    js_cat_content += "    module.exports = { FULL_GAMES_CATALOG };\n"
    js_cat_content += "}\n"
    with open(js_cat_path, 'w', encoding='utf-8') as f:
        f.write(js_cat_content)
    print(f" Synced {js_cat_path}")

    # Display representative samples from Class I to VIII
    print("\n" + "=" * 70)
    print("REPRESENTATIVE DIORAMA SCENE GENERATIONS ACROSS CLASSES I-VIII:")
    print("=" * 70)
    sample_indices = [
        0,    # LO-001 (English Class I)
        4,    # LO-005 (The Blend Express)
        7,    # LO-008 (The Thirsty Crow)
        38,   # LO-039 (Cup & Bucket)
        39,   # LO-040 (Play Market)
        45,   # LO-046 (Line Explorers)
        120,  # LO-121 (Heritage Crafts)
        128,  # LO-129 (Planet Protectors)
        210,  # LO-211 (Family Budget Analyst)
        260,  # LO-261 (Local Governance)
        310,  # LO-311 (Chemical Equations)
        410,  # LO-411 (Fluid Dynamics)
        439   # LO-440 (Public Goods & Regulations)
    ]
    for si in sample_indices:
        if si < len(thumbnails_dataset):
            d = thumbnails_dataset[si]
            print(f"\n[{d['id']}] Class {d['class']} | {d['subject']} | {d['title']}")
            print(f"  Skill > SubSkill: {d['skillArea']} > {d['subSkillArea']}")
            print(f"  Scene Summary   : {d['dioramaScene']['summary']}")
            print(f"  Hero Props      : {d['dioramaScene']['heroProps']}")
            print(f"  Characters      : {d['dioramaScene']['characters']}")
            print(f"  Action          : {d['dioramaScene']['action']}")
            print(f"  Prompt Preview  : {d['imagePrompt'][:140]}...")

if __name__ == '__main__':
    build_all()

