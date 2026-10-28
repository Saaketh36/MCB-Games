/* ====================================================
   NAVIGATION & VIEW SWITCHING
   ==================================================== */
function switchMainView(view) {
    if (view === 'learnThroughPlay') view = 'kid';
    AppState.currentView = view;

    const btnKid = document.getElementById('btnNavKid');
    const btnTeacher = document.getElementById('btnNavTeacher');
    const btnSplit = document.getElementById('btnNavSplit');
    if (btnKid) btnKid.classList.toggle('active', view === 'kid');
    if (btnTeacher) btnTeacher.classList.toggle('active', view === 'teacher');
    if (btnSplit) btnSplit.classList.toggle('active', view === 'split');

    const kidView = document.getElementById('kidZoneView');
    const teacherView = document.getElementById('teacherHubView');
    const splitView = document.getElementById('splitViewContainer');

    if (kidView) kidView.style.display = view === 'kid' ? 'block' : 'none';
    if (teacherView) teacherView.classList.toggle('active', view === 'teacher');
    if (splitView) splitView.classList.toggle('active', view === 'split');

    if (view === 'split') {
        renderSplitViews();
    } else if (view === 'teacher') {
        renderTeacherHub();
    } else {
        renderKidZone();
    }
}

function scrollToAdventures() {
    document.getElementById('adventuresSection').scrollIntoView({ behavior: 'smooth' });
}

/* ====================================================
   KID ZONE RENDERING & FILTERING
   ==================================================== */
function renderKidZone() {
    updateKidSubjectChips();
    updateKidStats();
    renderGamesGrid();
}

function updateKidStats() {
    const classAsgs = AppState.assignments.filter(a => a.class === AppState.selectedClass);
    const completed = classAsgs.filter(a => a.status === 'completed');

    let totalScore = 0;
    let totalMax = 0;
    completed.forEach(c => {
        totalScore += (c.score || 0);
        totalMax += (c.maxScore || 3);
    });

    const accuracy = totalMax > 0 ? Math.round((totalScore / totalMax) * 100) : (completed.length > 0 ? 100 : 0);

    const qEl = document.getElementById('kidStatQuests');
    if (qEl) qEl.textContent = completed.length;
    const sEl = document.getElementById('kidStatStars');
    if (sEl) sEl.textContent = totalScore;
    const aEl = document.getElementById('kidStatAccuracy');
    if (aEl) aEl.textContent = `${accuracy}%`;
    const bEl = document.getElementById('assignedCountBadge');
    const uniqueAssignedCount = [...new Set(classAsgs.map(a => a.gameId))].length;
    if (bEl) bEl.textContent = uniqueAssignedCount;
}

function renderGamesGrid() {
    const grid = document.getElementById('gamesCardsGrid');
    if (!grid) return;
    grid.innerHTML = '';

    // Get all assigned game IDs in strict assigned order for the currently selected class
    const classAsgs = AppState.assignments.filter(a => a.class === AppState.selectedClass);
    const assignedGameIds = [];
    classAsgs.forEach(a => {
        if (!assignedGameIds.includes(a.gameId)) {
            assignedGameIds.push(a.gameId);
        }
    });

    let list = GamesCatalog.filter(g => {
        // Class filter
        if (g.class && g.class !== AppState.selectedClass) return false;

        // STRICTLY show only games that are assigned to this class!
        if (!assignedGameIds.includes(g.id)) return false;

        // Subject filter
        if (AppState.selectedSubject !== 'all' && g.subject !== AppState.selectedSubject) return false;
        // Skill Area filter
        if (AppState.selectedSkillArea !== 'all' && g.skillArea !== AppState.selectedSkillArea) return false;
        // Activity (sub-skill) filter
        if (AppState.selectedActivity !== 'all' && g.activity !== AppState.selectedActivity) return false;
        // Search query
        if (AppState.searchQuery) {
            const q = AppState.searchQuery.toLowerCase();
            const matchTitle = g.title && g.title.toLowerCase().includes(q);
            const matchDesc = g.desc && g.desc.toLowerCase().includes(q);
            const matchSkill = g.skillArea && g.skillArea.toLowerCase().includes(q);
            const matchAct = g.activity && g.activity.toLowerCase().includes(q);
            const matchTopic = g.topic && g.topic.toLowerCase().includes(q);
            if (!matchTitle && !matchDesc && !matchSkill && !matchAct && !matchTopic) return false;
        }
        return true;
    });

    // Sort strictly by the order in which activities were assigned
    list.sort((a, b) => assignedGameIds.indexOf(a.id) - assignedGameIds.indexOf(b.id));

    // Update adventure count badge & clear filters button
    const badge = document.getElementById('filteredGamesCountBadge');
    if (badge) badge.textContent = `Showing ${list.length} assigned activity${list.length === 1 ? '' : 'ies'}`;

    const clearBtn = document.getElementById('btnClearFilters');
    if (clearBtn) {
        const hasFilters = AppState.selectedSubject !== 'all' || AppState.selectedSkillArea !== 'all' || AppState.selectedActivity !== 'all' || AppState.searchQuery !== '';
        clearBtn.style.display = hasFilters ? 'inline-flex' : 'none';
    }

    const kidResetBtn = document.getElementById('btnKidResetAssignments');
    if (kidResetBtn) {
        const hasAssigned = AppState.assignments.some(a => a.class === AppState.selectedClass);
        kidResetBtn.style.display = hasAssigned ? 'inline-flex' : 'none';
    }

    if (list.length === 0) {
        const totalAssignedForClass = assignedGameIds.length;
        const hasFilters = AppState.selectedSubject !== 'all' || AppState.selectedSkillArea !== 'all' || AppState.selectedActivity !== 'all' || AppState.searchQuery !== '';
        grid.innerHTML = `
                    <div style="grid-column: 1 / -1; padding: 48px; text-align: center; background: #ffffff; border-radius: 24px; border: 1px solid #e2e8f0; box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);">
                        <div style="font-size: 44px; margin-bottom: 12px;">📋✨</div>
                        <h4 style="font-family: var(--font-heading); font-size: 22px; font-weight: 700; color: #1e1b4b; margin-bottom: 6px;">
                            ${totalAssignedForClass === 0 ? `No assigned activities for Class ${AppState.selectedClass} yet` : `No matching assigned activities found`}
                        </h4>
                        <p style="font-size: 15px; color: var(--text-muted); margin-bottom: 18px;">
                            ${totalAssignedForClass === 0 ? `Your teacher has not assigned any activities for Class ${AppState.selectedClass} yet. Check back soon!` : `Try picking a different subject chip or clear your search filter.`}
                        </p>
                        ${hasFilters ? `
                            <button type="button" class="btn-clear-filters" onclick="resetAllFilters()" style="margin: 0 auto;">
                                Reset all filters ↺
                            </button>
                        ` : ''}
                    </div>
                `;
        return;
    }

    list.forEach(game => {
        // Check assignments for this game
        const assignedForThis = AppState.assignments.filter(a => a.class === AppState.selectedClass && a.gameId === game.id);
        const totalAssigned = assignedForThis.length;
        const completedForThis = assignedForThis.filter(a => a.status === 'completed');
        const compCount = completedForThis.length;
        const allCompleted = totalAssigned > 0 && compCount === totalAssigned;
        const hasPending = totalAssigned > 0 && compCount < totalAssigned;

        const card = document.createElement('div');
        card.className = `game-card ${allCompleted ? 'game-card-all-completed' : ''}`;
        card.innerHTML = `
                    <div class="game-thumb-wrap" style="height: 135px;">
                        <img src="${game.thumb}" alt="${game.title}" class="game-thumb-img" onerror="if(!this.src.endsWith('.svg')){this.src='images/thumbnails/${game.id}.svg';}">
                        <span class="subject-badge-pill ${game.badgeClass}">${game.subject}</span>
                        ${game.isCustom ? '<span class="tac-badge tac-badge-custom" style="position: absolute; top: 10px; right: 10px; z-index: 3; box-shadow: 0 2px 8px rgba(0,0,0,0.12);">⭐ Custom</span>' : ''}
                        ${allCompleted
                ? '<span class="game-status-pill completed-pill" style="background: rgba(16, 185, 129, 0.95); color: #ffffff; border: 1px solid #059669;"><span>✓</span> Completed</span>'
                : (compCount > 0
                    ? `<span class="game-status-pill" style="background: rgba(16, 185, 129, 0.92); color: #ffffff;"><span>✓</span> ${compCount}/${totalAssigned} Done</span>`
                    : (totalAssigned > 0 ? '<span class="game-status-pill" style="background: rgba(254, 243, 199, 0.95); color: #b45309;"><span>⏳</span> Assigned</span>' : ''))
            }
                    </div>
                    <div class="game-info-body" style="padding: 14px 16px;">
                        <div class="game-simple-tags">
                            ${(window.Class2Games && window.Class2Games.isClass2Interactive(game)) ? '<span class="simple-tag mini-game-tag">🎮 Mini-Game</span>' : ''}
                            <span class="simple-tag">${game.skillArea || 'General'}</span>
                        </div>
                        <h3 class="game-title" style="font-size: 16px; margin-bottom: 8px;">${game.title}</h3>

                        ${totalAssigned > 0 ? `
                        <div class="game-assigned-summary">
                            <span class="assigned-dot" style="${allCompleted ? 'background: #10b981;' : ''}"></span>
                            <span>${totalAssigned} assigned</span>
                            ${compCount > 0 ? `<span class="assigned-comp-check">(${compCount} done ✓)</span>` : ''}
                        </div>
                        ` : ''}

                        ${allCompleted ? `
                        <button type="button" class="btn-play-action played-all-done" style="margin-top: auto; padding: 9px 14px; font-size: 13px;" onclick="openWhoIsPlaying('${game.id}')">
                            <span>✓</span> Completed (All Students Done)
                        </button>
                        ` : (hasPending ? `
                        <button type="button" class="btn-play-action" style="margin-top: auto; padding: 9px 14px; font-size: 13px;" onclick="openWhoIsPlaying('${game.id}')">
                            <span>${(window.Class2Games && window.Class2Games.isClass2Interactive(game)) ? '🎮' : '▶'}</span> Play Activity (${totalAssigned - compCount} pending)
                        </button>
                        ` : `
                        <button type="button" class="btn-play-action" style="margin-top: auto; padding: 9px 14px; font-size: 13px;" onclick="openWhoIsPlaying('${game.id}')">
                            <span>${(window.Class2Games && window.Class2Games.isClass2Interactive(game)) ? '🎮' : '▶'}</span> Play Activity 🚀
                        </button>
                        `)}
                    </div>
                `;
        grid.appendChild(card);
    });
}

/* Dynamic Cascading Filters for Skill Area & Activity */
function updateSkillAreaOptions() {
    const select = document.getElementById('filterSkillAreaSelect');
    if (!select) return;

    const currentClassGames = GamesCatalog.filter(g => {
        if (g.class && g.class !== AppState.selectedClass) return false;
        if (AppState.selectedSubject !== 'all' && g.subject !== AppState.selectedSubject) return false;
        return true;
    });

    const uniqueSkillAreas = Array.from(new Set(currentClassGames.map(g => g.skillArea).filter(Boolean))).sort();

    if (AppState.selectedSkillArea !== 'all' && !uniqueSkillAreas.includes(AppState.selectedSkillArea)) {
        AppState.selectedSkillArea = 'all';
    }

    select.innerHTML = '<option value="all">🎯 All Skill Areas</option>';
    uniqueSkillAreas.forEach(sa => {
        const opt = document.createElement('option');
        opt.value = sa;
        opt.textContent = sa;
        if (AppState.selectedSkillArea === sa) opt.selected = true;
        select.appendChild(opt);
    });

    updateActivityOptions();
}

function updateActivityOptions() {
    const select = document.getElementById('filterActivitySelect');
    if (!select) return;

    const matchingGames = GamesCatalog.filter(g => {
        if (g.class && g.class !== AppState.selectedClass) return false;
        if (AppState.selectedSubject !== 'all' && g.subject !== AppState.selectedSubject) return false;
        if (AppState.selectedSkillArea !== 'all' && g.skillArea !== AppState.selectedSkillArea) return false;
        return true;
    });

    const uniqueActivities = Array.from(new Set(matchingGames.map(g => g.activity).filter(Boolean))).sort();

    if (AppState.selectedActivity !== 'all' && !uniqueActivities.includes(AppState.selectedActivity)) {
        AppState.selectedActivity = 'all';
    }

    select.innerHTML = '<option value="all">⚡ All Activities</option>';
    uniqueActivities.forEach(act => {
        const opt = document.createElement('option');
        opt.value = act;
        opt.textContent = act;
        if (AppState.selectedActivity === act) opt.selected = true;
        select.appendChild(opt);
    });
}

function handleSkillAreaFilterChange(val) {
    AppState.selectedSkillArea = val;
    updateActivityOptions();
    renderGamesGrid();
}

function handleActivityFilterChange(val) {
    AppState.selectedActivity = val;
    renderGamesGrid();
}

function resetAllFilters() {
    AppState.selectedSubject = 'all';
    AppState.selectedSkillArea = 'all';
    AppState.selectedActivity = 'all';
    AppState.searchQuery = '';
    const searchInput = document.getElementById('gameSearchInput');
    if (searchInput) searchInput.value = '';
    document.querySelectorAll('.chip-btn').forEach((b, idx) => {
        b.classList.toggle('active', idx === 0);
    });
    updateSkillAreaOptions();
    renderGamesGrid();
}

function handleClassFilterChange(cls) {
    AppState.selectedClass = cls;
    AppState.selectedSkillArea = 'all';
    AppState.selectedActivity = 'all';
    const tSel = document.getElementById('teacherClassSelect');
    if (tSel) tSel.value = cls;
    const kSel = document.getElementById('kidClassSelect');
    if (kSel) kSel.value = cls;

    const kLbl = document.getElementById('kidCurrentClassLabel');
    if (kLbl) kLbl.textContent = cls;
    const tLbl = document.getElementById('teacherCurrentClassLabel');
    if (tLbl) tLbl.textContent = cls;

    document.querySelectorAll('#teacherClassPills .teacher-class-pill, #kidClassPills .teacher-class-pill').forEach(btn => {
        btn.classList.toggle('active', btn.textContent.trim() === `Class ${cls}`);
    });

    updateSkillAreaOptions();
    renderKidZone();
    renderTeacherHub();
    if (AppState.currentView === 'split') {
        renderSplitViews();
    }
}

function filterBySubject(sub, btn) {
    AppState.selectedSubject = sub;
    AppState.selectedSkillArea = 'all';
    AppState.selectedActivity = 'all';
    document.querySelectorAll('#kidSubjectChips .chip-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    updateSkillAreaOptions();
    renderGamesGrid();
}

function handleGameSearch(val) {
    AppState.searchQuery = (val || '').trim();
    renderGamesGrid();
}

function setKidSubTab(tab = 'assigned') {
    AppState.kidSubTab = 'assigned';
    const tabAsg = document.getElementById('tabMyAssignments');
    if (tabAsg) tabAsg.classList.add('active');
    renderGamesGrid();
}

/* ====================================================
   "WHO'S PLAYING?" SELECTION MODAL
   ==================================================== */
function openWhoIsPlaying(gameId) {
    const game = GamesCatalog.find(g => g.id === gameId);
    if (!game) return;

    AppState.activeMissionGame = game;
    AppState.selectedStudent = null;

    document.getElementById('whoModalSubtitle').textContent = `Choose your name for ${game.title} • Class ${AppState.selectedClass}`;
    document.getElementById('whoStudentSearch').value = '';
    document.getElementById('btnStartSelectedChallenge').disabled = true;

    renderWhoRoster();
    document.getElementById('whoIsPlayingModal').classList.add('active');
}

function closeWhoModal() {
    document.getElementById('whoIsPlayingModal').classList.remove('active');
}

function renderWhoRoster(filterText = '') {
    const container = document.getElementById('whoStudentsGrid');
    container.innerHTML = '';

    const game = AppState.activeMissionGame;
    if (!game) return;

    // Get students assigned to this specific game in the selected class
    const assignedList = AppState.assignments
        .filter(a => a.class === AppState.selectedClass && a.gameId === game.id);

    if (assignedList.length === 0) {
        container.innerHTML = `
                    <div style="grid-column: 1 / -1; text-align: center; padding: 28px 16px; background: #f8fafc; border: 1.5px dashed #cbd5e1; border-radius: 18px;">
                        <div style="font-size: 34px; margin-bottom: 8px;">📋✨</div>
                        <h4 style="font-family: var(--font-heading); font-size: 17px; color: #1e1b4b; margin-bottom: 6px;">No students assigned yet</h4>
                        <p style="font-size: 13.5px; color: var(--text-muted); margin-bottom: 16px;">This activity has not been assigned to any students in Class ${AppState.selectedClass} yet.</p>
                        <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
                            <button type="button" class="btn-quest-ctrl" style="padding: 9px 20px; font-size: 13px; background: #ede9fe; color: #6d28d9; border-color: #ddd6fe;" onclick="startQuickPractice('${game.id}')">
                                <span>🎮</span> Quick Practice / Preview
                            </button>
                        </div>
                    </div>
                `;
        document.getElementById('btnStartSelectedChallenge').disabled = true;
        return;
    }

    const allCompleted = assignedList.length > 0 && assignedList.every(a => a.status === 'completed');

    if (allCompleted) {
        const banner = document.createElement('div');
        banner.style.cssText = 'grid-column: 1 / -1; padding: 18px 20px; background: #ecfdf5; border: 2px solid #a7f3d0; border-radius: 16px; text-align: center; margin-bottom: 10px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.1);';
        banner.innerHTML = `
                    <div style="font-size: 34px; margin-bottom: 6px;">🎉🏆</div>
                    <h4 style="font-family: var(--font-heading); font-size: 17.5px; color: #065f46; font-weight: 800; margin-bottom: 4px;">Activity Completed by All Assigned Students!</h4>
                    <p style="font-size: 13.5px; color: #047857; margin: 0; line-height: 1.4;">
                        Every assigned student has successfully finished this activity. Students do not need to do this task again. Excellent work! 🌟
                    </p>
                `;
        container.appendChild(banner);

        const startBtn = document.getElementById('btnStartSelectedChallenge');
        if (startBtn) {
            startBtn.disabled = true;
            startBtn.innerHTML = '<span>✓</span> All Assigned Students Finished';
        }
    }

    const colors = [
        { bg: '#ede9fe', text: '#7c3aed' },
        { bg: '#ffe4e6', text: '#e11d48' },
        { bg: '#dcfce7', text: '#15803d' },
        { bg: '#fef3c7', text: '#d97706' },
        { bg: '#e0f2fe', text: '#0284c7' }
    ];

    const filtered = assignedList.filter(a => !filterText || a.student.toLowerCase().includes(filterText.toLowerCase()));

    if (filtered.length === 0) {
        container.innerHTML = `
                    <div style="grid-column: 1 / -1; text-align: center; padding: 18px; color: var(--text-muted); font-size: 13.5px;">
                        No assigned students match "${filterText}"
                    </div>
                `;
        return;
    }

    filtered.forEach((asg, idx) => {
        const initials = asg.student.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase();
        const col = colors[idx % colors.length];
        const isCompleted = asg.status === 'completed';

        const card = document.createElement('div');
        card.className = `who-student-card ${isCompleted ? 'completed-locked' : ''}`;

        if (isCompleted) {
            card.onclick = () => {
                showToastNotification(`${asg.student} has already completed this activity (Score: ${asg.score || 3}/${asg.maxScore || 3} ⭐)! Great job! No need to do it again. 🎉`);
            };
        } else {
            card.onclick = () => selectStudentForMission({ name: asg.student, roll: asg.roll }, card);
        }

        card.innerHTML = `
                    <div class="who-avatar-badge" style="background: ${isCompleted ? '#dcfce7' : col.bg}; color: ${isCompleted ? '#15803d' : col.text};">
                        ${isCompleted ? '✓' : initials}
                    </div>
                    <div style="flex: 1;">
                        <div style="font-size: 14.5px; font-weight: 700; color: #0f172a;">${asg.student}</div>
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 3px; gap: 8px;">
                            <span style="font-size: 11.5px; color: var(--text-muted);">Roll #${asg.roll}</span>
                            <span style="font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 999px; ${isCompleted ? 'background: #dcfce7; color: #15803d; border: 1px solid #86efac;' : 'background: #fef3c7; color: #b45309; border: 1px solid #fde68a;'}">
                                ${isCompleted ? `✓ Done (${asg.score || 3}/${asg.maxScore || 3} ⭐)` : 'Ready to play! 🚀'}
                            </span>
                        </div>
                        ${isCompleted ? `
                        <div style="font-size: 11px; color: #15803d; font-weight: 600; margin-top: 4px;">
                            ✓ Task completed • No need to redo
                        </div>
                        ` : ''}
                    </div>
                `;
        container.appendChild(card);
    });
}

function filterWhoRoster(val) {
    renderWhoRoster(val);
}

function selectStudentForMission(student, cardElem) {
    if (!student || !AppState.activeMissionGame) return;

    // Prevent selecting students who already completed the task
    const asg = AppState.assignments.find(a =>
        a.class === AppState.selectedClass &&
        a.gameId === AppState.activeMissionGame.id &&
        a.student === student.name
    );
    if (asg && asg.status === 'completed') {
        showToastNotification(`${student.name} has already completed this activity! No need to do it again. 🎉`);
        return;
    }

    AppState.selectedStudent = student;
    document.querySelectorAll('.who-student-card').forEach(c => c.classList.remove('selected'));
    cardElem.classList.add('selected');

    const startBtn = document.getElementById('btnStartSelectedChallenge');
    if (startBtn) {
        startBtn.disabled = false;
        startBtn.innerHTML = `<span>🚀</span> Start Challenge for ${student.name}`;
    }
}

function startSelectedMission() {
    if (!AppState.selectedStudent || !AppState.activeMissionGame) return;

    // Guard against completed student re-taking
    const asg = AppState.assignments.find(a =>
        a.class === AppState.selectedClass &&
        a.gameId === AppState.activeMissionGame.id &&
        a.student === AppState.selectedStudent.name
    );
    if (asg && asg.status === 'completed') {
        showToastNotification(`${AppState.selectedStudent.name} has already completed this activity! No need to do it again.`);
        return;
    }

    closeWhoModal();
    launchQuestRunner();
}

function startQuickPractice(gameId) {
    const game = GamesCatalog.find(g => g.id === gameId);
    if (!game) return;
    closeWhoModal();
    AppState.activeMissionGame = game;
    AppState.selectedStudent = { name: "Guest Explorer", roll: 101 };
    launchQuestRunner();
}

function previewActivity(gameId) {
    const game = GamesCatalog.find(g => g.id === gameId);
    if (!game) return;
    AppState.activeMissionGame = game;
    AppState.selectedStudent = { name: "Teacher Preview Mode", roll: 0 };
    launchQuestRunner();
}

