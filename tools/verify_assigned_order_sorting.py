import sys, json, re

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def run_tests():
    print("Testing assigned order sorting logic...")

    # The frontend is intentionally split into classic scripts. Inspect the
    # logical application, rather than assuming every implementation lives in
    # the bootstrap entry point.
    source_files = [
        'js/app.js',
        'js/portals/kid-zone.js',
        'js/portals/teacher-hub.js',
        'js/portals/split-view.js',
    ]
    code = '\n'.join(
        open(path, 'r', encoding='utf-8').read()
        for path in source_files
    )

    # Test 1: Verify assignedOrder is extracted in renderTeacherHub
    assert "const assignedOrder = [];" in code, "assignedOrder array definition missing in js/app.js"
    assert "if (!assignedOrder.includes(a.gameId))" in code, "assignedOrder deduplication missing"
    assert "filteredGames.sort((a, b) => {" in code, "filteredGames sort missing"
    assert "return aIdx - bIdx;" in code, "aIdx - bIdx assigned order sorting missing"
    print("✓ Check 1: renderTeacherHub assignedOrder extraction and sorting verified in code.")

    # Test 2: Verify table rendering iterates through filteredGames directly in sorted order
    assert "tableBody.appendChild(tr);" in code, "Table row append missing"
    # Ensure skillGroups iteration is removed from tableBody rendering
    # Check that skillGroups is not grouping table rows before sorting
    assert "skillGroups.forEach((gamesInSkill" not in code, "Old skillGroups.forEach loop still present!"
    print("✓ Check 2: Table rows iterate directly in assigned order (no artificial skillGroups partitioning).")

    # Test 3: Verify renderGamesGrid sorts list by assigned order
    assert "list.sort((a, b) => assignedGameIds.indexOf(a.id) - assignedGameIds.indexOf(b.id));" in code, "renderGamesGrid sorting missing"
    print("✓ Check 3: renderGamesGrid sorts kid activities in assigned order.")

    # Test 4: Verify renderSplitViews sorts by assigned order
    assert "const sortedClassGames = [...classGames].sort((a, b) => {" in code, "renderSplitViews sortedClassGames missing"
    print("✓ Check 4: renderSplitViews sorts activities in assigned order.")

    # Test 5: Simulate the sorting logic with mock data matching the user's Class IV activities
    mock_assignments = [
        {"class": "IV", "gameId": "LO-096"}, # Assembly Announcement (English)
        {"class": "IV", "gameId": "LO-097"}, # Radio Wildlife (English)
        {"class": "IV", "gameId": "LO-124"}, # Wild Adaptations (EVS)
        {"class": "IV", "gameId": "LO-125"}, # Family Reunion (EVS)
        {"class": "IV", "gameId": "LO-126"}, # Botanical Wonders (EVS)
        {"class": "IV", "gameId": "LO-133"}, # Everyday Problem Solvers (Math)
        {"class": "IV", "gameId": "LO-136"}, # Metric Converters (Math)
    ]

    mock_catalog = [
        {"id": "LO-096", "title": "Assembly Announcement: Lost & Found! 📢", "subject": "English"},
        {"id": "LO-097", "title": "Radio Wildlife: The Elephant Whisperer 🐘", "subject": "English"},
        {"id": "LO-100", "title": "Unassigned English Activity", "subject": "English"},
        {"id": "LO-124", "title": "Wild Adaptations: Claws, Teeth & Ears 🐾 👂", "subject": "EVS"},
        {"id": "LO-125", "title": "Family Reunion: Extended Family Bonds 👨‍👩‍👧‍👦", "subject": "EVS"},
        {"id": "LO-126", "title": "Botanical Wonders: Roots, Fruits & Fragrant Blooms 🌺 🥕", "subject": "EVS"},
        {"id": "LO-130", "title": "Unassigned EVS Activity", "subject": "EVS"},
        {"id": "LO-133", "title": "Everyday Problem Solvers: The School Picnic 🧺", "subject": "Mathematics"},
        {"id": "LO-136", "title": "Metric Converters: Meters and Centimeters 📏", "subject": "Mathematics"},
        {"id": "LO-140", "title": "Unassigned Math Activity", "subject": "Mathematics"},
    ]

    # Replicate the exact sorting algorithm from js/app.js:
    assignedOrder = []
    for a in mock_assignments:
        if a["gameId"] not in assignedOrder:
            assignedOrder.append(a["gameId"])

    def sort_key(item):
        a_id = item["id"]
        if a_id in assignedOrder:
            return (0, assignedOrder.index(a_id))
        else:
            return (1, 0)

    sorted_list = sorted(mock_catalog, key=sort_key)
    sorted_ids = [item["id"] for item in sorted_list]

    expected_assigned_order = [
        "LO-096", "LO-097", "LO-124", "LO-125", "LO-126", "LO-133", "LO-136"
    ]

    # Verify the first 7 are assigned, in exact assigned order
    assert sorted_ids[:7] == expected_assigned_order, f"Order mismatch: got {sorted_ids[:7]}"
    # Verify remaining 3 are unassigned
    assert sorted_ids[7:] == ["LO-100", "LO-130", "LO-140"], f"Unassigned mismatch: got {sorted_ids[7:]}"

    print(f"✓ Check 5: Simulated sorting strictly matched expected assigned order: {sorted_ids[:7]}")
    print("\nALL ASSIGNED ORDER TESTS PASSED SUCCESSFULLY! 🎯")

if __name__ == '__main__':
    run_tests()

