function resolveGameFile(gameName, skill, className) {
    const byName = {
        'Listen & Do Adventure': 'listen_do_adventure.html',
        'Story Time Quiz': 'story_time_quiz_game.html',
        'Cell Organelles Matcher': 'cell_organelles_matcher.html',
        'Cell Structure Game': 'cell_structure_game.html'
    };
    if (byName[gameName]) return byName[gameName];

    // skill -> { class: file, '*': default file }
    const bySkill = {
        'Listening': {'*': 'listen_do_adventure.html'},
        'Reading': {'I': 'story_time_quiz_game.html', '*': 'reading_comprehension_2.html'},
        'Writing': {'I': 'letter_formation.html', '*': 'writing_practice_2.html'},
        'Speaking': {'I': 'pronunciation_game.html', '*': 'speaking_practice_2.html'},
        'Numbers': {'*': 'count_and_match.html'},
        'Addition': {'*': 'simple_addition.html'},
        'Subtraction': {'*': 'subtraction_basics.html'},
        'Shapes': {'*': 'shape_sorter.html'},
        'Multiplication': {'*': 'multiplication_table.html'},
        'Division': {'*': 'division_basics.html'},
        'Measurement': {'*': 'measurement_quiz.html'},
        'Fractions': {'*': 'fraction_basics.html'},
        'Decimals': {'*': 'decimal_identifier.html'},
        'Geometry': {'*': 'geometry_game.html'},
        'Data': {'*': 'data_collector.html'},
        'Algebra': {'*': 'algebra_basics.html'},
        'Statistics': {'*': 'statistics_quiz.html'},
        'Probability': {'*': 'probability_game.html'},
        'Ratios': {'*': 'ratio_game.html'},
        'Percentages': {'*': 'percentage_calculator.html'},
        'Calculus': {'*': 'calculus_basics.html'},
        'Life Skills': {'*': 'life_skills_quiz.html'},
        'Nature': {'*': 'nature_explorer.html'},
        'Safety': {'*': 'safety_rules_quiz.html'},
        'Weather': {'*': 'weather_quiz.html'},
        'Environment': {'*': 'environment_game.html'},
        'Plants': {'*': 'plant_parts_quiz.html'},
        'Animals': {'*': 'animal_matcher.html'},
        'Ecosystems': {'*': 'ecosystem_simulator.html'},
        'Body': {'*': 'body_systems_quiz.html'},
        'Matter': {'*': 'matter_states_quiz.html'},
        'Forces': {'*': 'forces_game.html'},
        'Life Cycles': {'*': 'life_cycles_quiz.html'},
        'Cells': {'*': 'cell_structure_game.html'},
        'Reproduction': {'*': 'reproduction_quiz.html'},
        'Ecology': {'*': 'ecology_game.html'},
        'Physics': {'VIII': 'advanced_physics.html', '*': 'physics_quiz.html'},
        'Chemistry': {'VIII': 'advanced_chemistry.html', '*': 'chemistry_game.html'},
        'Biology': {'VIII': 'advanced_biology.html', '*': 'biology_quiz.html'}
    };
    const entry = bySkill[skill];
    if (!entry) return null;
    return entry[className] || entry['*'];
}
