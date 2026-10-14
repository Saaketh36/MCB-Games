with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ----------------------------------------------------
# 1. Update the table <thead>: Remove Action column and adjust widths
# ----------------------------------------------------
old_thead = """                <table class="curriculum-table">
                    <thead>
                        <tr>
                            <th style="width: 38%;">Activity & Categories</th>
                            <th style="width: 24%;">Completion Progress</th>
                            <th style="width: 24%;">Assigned Students</th>
                            <th style="width: 14%; text-align: right;">Action</th>
                        </tr>
                    </thead>
                    <tbody id="teacherTableBody">"""

new_thead = """                <table class="curriculum-table">
                    <thead>
                        <tr>
                            <th style="width: 44%;">Activity & Categories</th>
                            <th style="width: 28%;">Completion Progress</th>
                            <th style="width: 28%;">Assigned Students</th>
                        </tr>
                    </thead>
                    <tbody id="teacherTableBody">"""

if old_thead in html:
    html = html.replace(old_thead, new_thead)
    print("Updated <thead>: Action column removed and column widths adjusted!")
else:
    print("Warning: old_thead not matched exactly!")

# ----------------------------------------------------
# 2. Update empty state colspan: Change 4 to 3
# ----------------------------------------------------
old_empty = '<td colspan="4" style="text-align: center; padding: 48px 16px; background: #ffffff;">'
new_empty = '<td colspan="3" style="text-align: center; padding: 48px 16px; background: #ffffff;">'

if old_empty in html:
    html = html.replace(old_empty, new_empty)
    print("Updated empty state colspan from 4 to 3!")

# ----------------------------------------------------
# 3. In renderTeacherHub(): Add sorting (assigned first) & remove <td> Action column
# ----------------------------------------------------
old_filter_block = """            // Filter activities by Subject, Search query, and Status
            let filteredGames = classGames.filter(g => {
                if (AppState.teacherSubjectFilter !== 'all' && g.subject !== AppState.teacherSubjectFilter) return false;
                if (AppState.teacherStatusFilter === 'assigned' && !assignedGameIds.has(g.id)) return false;
                if (AppState.teacherSearchQuery) {
                    const q = AppState.teacherSearchQuery.toLowerCase();
                    const matchTitle = g.title && g.title.toLowerCase().includes(q);
                    const matchSub = g.subject && g.subject.toLowerCase().includes(q);
                    const matchSkill = g.skillArea && g.skillArea.toLowerCase().includes(q);
                    const matchAct = g.activity && g.activity.toLowerCase().includes(q);
                    if (!matchTitle && !matchSub && !matchSkill && !matchAct) return false;
                }
                return true;
            });"""

new_filter_block = """            // Filter activities by Subject, Search query, and Status
            let filteredGames = classGames.filter(g => {
                if (AppState.teacherSubjectFilter !== 'all' && g.subject !== AppState.teacherSubjectFilter) return false;
                if (AppState.teacherStatusFilter === 'assigned' && !assignedGameIds.has(g.id)) return false;
                if (AppState.teacherSearchQuery) {
                    const q = AppState.teacherSearchQuery.toLowerCase();
                    const matchTitle = g.title && g.title.toLowerCase().includes(q);
                    const matchSub = g.subject && g.subject.toLowerCase().includes(q);
                    const matchSkill = g.skillArea && g.skillArea.toLowerCase().includes(q);
                    const matchAct = g.activity && g.activity.toLowerCase().includes(q);
                    if (!matchTitle && !matchSub && !matchSkill && !matchAct) return false;
                }
                return true;
            });

            // Sort: Assigned activities first, not assigned later
            filteredGames.sort((a, b) => {
                const aAssigned = classAsgs.filter(asg => asg.gameId === a.id).length;
                const bAssigned = classAsgs.filter(asg => asg.gameId === b.id).length;
                const aHas = aAssigned > 0 ? 1 : 0;
                const bHas = bAssigned > 0 ? 1 : 0;

                if (bHas !== aHas) {
                    return bHas - aHas; // Assigned (1) comes before Unassigned (0)
                }
                if (bAssigned !== aAssigned) {
                    return bAssigned - aAssigned; // More assigned students first
                }
                return 0;
            });"""

if old_filter_block in html:
    html = html.replace(old_filter_block, new_filter_block)
    print("Added sorting: assigned activities first, unassigned later!")
else:
    print("Warning: old_filter_block not matched exactly!")

# Remove the Action <td> in table row
old_action_td = """                                <td style="text-align: right;">
                                    <div style="display: inline-flex; gap: 6px; align-items: center; justify-content: flex-end;">
                                        <button type="button" class="btn-tac-assign-sm" onclick="openAssignModalForGame('${g.id}')">
                                            + Assign
                                        </button>
                                        <button type="button" class="btn-tac-play-sm" onclick="openWhoIsPlaying('${g.id}')">
                                            ▶ Play
                                        </button>
                                    </div>
                                </td>"""

if old_action_td in html:
    html = html.replace(old_action_td, "")
    print("Removed Action column <td> from curriculum rows!")
else:
    print("Warning: old_action_td not matched exactly!")

# ----------------------------------------------------
# 4. In renderSplitViews(): also sort assigned first
# ----------------------------------------------------
old_split_games = """            const gamesToShow = splitFilter === 'assigned' ? assignedGames : classGames;"""
new_split_games = """            // Sort: Assigned activities first
            const sortedClassGames = [...classGames].sort((a, b) => {
                const aAssigned = classAsgs.filter(asg => asg.gameId === a.id).length;
                const bAssigned = classAsgs.filter(asg => asg.gameId === b.id).length;
                const aHas = aAssigned > 0 ? 1 : 0;
                const bHas = bAssigned > 0 ? 1 : 0;
                if (bHas !== aHas) return bHas - aHas;
                return bAssigned - aAssigned;
            });

            const gamesToShow = splitFilter === 'assigned' ? assignedGames : sortedClassGames;"""

if old_split_games in html:
    html = html.replace(old_split_games, new_split_games)
    print("Updated Split View to sort assigned first as well!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("ALL CHANGES COMPLETED!")
