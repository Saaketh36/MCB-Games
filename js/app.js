/* ====================================================
   CURRICULUM ROSTER & GAME DATA
   ==================================================== */
const StudentRosters = {
    "I": [
        { roll: 101, name: "Aarav Sharma" },
        { roll: 102, name: "Ananya Verma" },
        { roll: 103, name: "Ishaan Gupta" },
        { roll: 104, name: "Kavya Nair" },
        { roll: 105, name: "Rohan Mehra" }
    ],
    "II": [
        { roll: 201, name: "Aditya Rao" },
        { roll: 202, name: "Diya Pillai" },
        { roll: 203, name: "Manish Joshi" },
        { roll: 204, name: "Riya Sen" },
        { roll: 205, name: "Vivaan Malhotra" }
    ],
    "III": [
        { roll: 301, name: "Aryan Saxena" },
        { roll: 302, name: "Ira Singhania" },
        { roll: 303, name: "Kabir Das" },
        { roll: 304, name: "Meera Iyer" },
        { roll: 305, name: "Reyansh Bhatt" }
    ],
    "IV": [
        { roll: 401, name: "Aarav Sharma" },
        { roll: 402, name: "Ananya Reddy" },
        { roll: 403, name: "Arjun Patel" },
        { roll: 404, name: "Diya Rao" },
        { roll: 405, name: "Ishaan Kumar" },
        { roll: 406, name: "Meera Nair" },
        { roll: 407, name: "Rohan Gupta" },
        { roll: 408, name: "Saanvi Reddy" },
        { roll: 409, name: "Vihaan Shah" },
        { roll: 410, name: "Zoya Khan" }
    ],
    "V": [
        { roll: 501, name: "Armaan Malik" },
        { roll: 502, name: "Devika Menon" },
        { roll: 503, name: "Karan Johar" },
        { roll: 504, name: "Pooja Hegde" },
        { roll: 505, name: "Siddharth Roy" }
    ],
    "VI": [
        { roll: 601, name: "Abhinav Bindra" },
        { roll: 602, name: "Fatima Sana" },
        { roll: 603, name: "Gautam Gambhir" },
        { roll: 604, name: "Harmanpreet Kaur" },
        { roll: 605, name: "Jasprit Bumrah" }
    ],
    "VII": [
        { roll: 701, name: "Alia Bhatt" },
        { roll: 702, name: "Deepika Padukone" },
        { roll: 703, name: "Ranbir Kapoor" },
        { roll: 704, name: "Ranveer Singh" },
        { roll: 705, name: "Varun Dhawan" }
    ],
    "VIII": [
        { roll: 801, name: "Anushka Sharma" },
        { roll: 802, name: "KL Rahul" },
        { roll: 803, name: "Rohit Sharma" },
        { roll: 804, name: "Smriti Mandhana" },
        { roll: 805, name: "Virat Kohli" }
    ]
};

const GamesCatalog = (typeof FULL_GAMES_CATALOG !== 'undefined' && Array.isArray(FULL_GAMES_CATALOG) && FULL_GAMES_CATALOG.length > 0)
    ? FULL_GAMES_CATALOG
    : (typeof window !== 'undefined' && window.GamesCatalog && window.GamesCatalog.length > 0)
        ? window.GamesCatalog
        : [];

/* ====================================================
   CENTRALIZED STATE MANAGEMENT
   ==================================================== */
const AppState = {
    currentView: 'kid', // 'kid' | 'teacher' | 'split'
    selectedClass: 'IV',
    selectedSubject: 'all',
    selectedSkillArea: 'all',
    selectedActivity: 'all',
    searchQuery: '',
    kidSubTab: 'assigned', // Enforce assigned activities only
    teacherSubjectFilter: 'all',
    teacherSearchQuery: '',
    teacherLayoutMode: 'table', // 'table' | 'grid'
    teacherStatusFilter: 'all', // 'all' | 'assigned'
    splitTeacherFilter: 'assigned', // 'assigned' | 'all'
    assignments: [],
    activeMissionGame: null,
    selectedStudent: null,
    missionStep: 0,
    missionAnswers: {}
};

// Persistent Assignment Storage (Strict user-driven assignments only: NO auto-seeding)
const STORAGE_KEY = 'mcb_assignments_v8';

function loadSavedAssignments() {
    try {
        // Clear any legacy test keys so stale test assignments never linger
        ['mcb_assignments', 'mcb_assignments_v1', 'mcb_assignments_v2', 'mcb_assignments_v3', 'mcb_assignments_v4', 'mcb_assignments_v5', 'mcb_assignments_v6', 'mcb_assignments_v7', 'assignments'].forEach(k => {
            try { localStorage.removeItem(k); } catch (e) { }
        });

        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
            AppState.assignments = JSON.parse(stored);
            if (!Array.isArray(AppState.assignments)) {
                AppState.assignments = [];
            }
        } else {
            AppState.assignments = [];
        }
    } catch (e) {
        AppState.assignments = [];
    }
}

function saveAssignments() {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(AppState.assignments));
    } catch (e) {
        console.error(e);
    }
}

function promptResetAssignments() {
    const modal = document.getElementById('resetConfirmModal');
    if (modal) {
        const classBtnLabel = document.getElementById('resetModalClassBtnLabel');
        if (classBtnLabel) classBtnLabel.textContent = `Class ${AppState.selectedClass}`;
        modal.classList.add('active');
        modal.style.display = 'flex';
    }
}

function closeResetModal() {
    const modal = document.getElementById('resetConfirmModal');
    if (modal) {
        modal.classList.remove('active');
        modal.style.display = 'none';
    }
}

function clearAllAssignments() {
    AppState.assignments = [];
    try {
        ['mcb_assignments', 'mcb_assignments_v1', 'mcb_assignments_v2', 'mcb_assignments_v3', 'mcb_assignments_v4', 'mcb_assignments_v5', 'mcb_assignments_v6', 'mcb_assignments_v7', 'mcb_assignments_v8', 'assignments'].forEach(k => {
            try { localStorage.removeItem(k); } catch (e) { }
        });
    } catch (e) { }
    saveAssignments();
    closeResetModal();
    renderTeacherHub();
    renderKidZone();
    if (AppState.currentView === 'split') {
        renderSplitViews();
    }
    showToastNotification("✨ All assignments for all classes reset to 0!");
}

function clearClassAssignments() {
    const cls = AppState.selectedClass;
    AppState.assignments = AppState.assignments.filter(a => a.class !== cls);
    saveAssignments();
    closeResetModal();
    renderTeacherHub();
    renderKidZone();
    if (AppState.currentView === 'split') {
        renderSplitViews();
    }
    showToastNotification(`✨ All assignments for Class ${cls} reset to 0!`);
}

function unassignActivity(gameId) {
    const cls = AppState.selectedClass;
    AppState.assignments = AppState.assignments.filter(a => !(a.class === cls && a.gameId === gameId));
    saveAssignments();
    renderTeacherHub();
    renderKidZone();
    if (AppState.currentView === 'split') {
        renderSplitViews();
    }
    showToastNotification("Activity unassigned successfully! ✨");
}

function toggleStudentAssignment(gameId, studentName, roll) {
    const cls = AppState.selectedClass;
    const game = GamesCatalog.find(g => g.id === gameId);
    if (!game) return;

    const existingIndex = AppState.assignments.findIndex(a =>
        a.class === cls && a.gameId === gameId && a.student === studentName
    );

    if (existingIndex >= 0) {
        const existing = AppState.assignments[existingIndex];
        if (existing.status === 'completed') {
            showToastNotification(`${studentName} has already completed this activity (Score: ${existing.score || 3}/${existing.maxScore || 3} ⭐)! Progress is preserved. ✨`);
            return;
        }
        AppState.assignments.splice(existingIndex, 1);
        saveAssignments();
        renderTeacherHub();
        renderKidZone();
        if (AppState.currentView === 'split') renderSplitViews();
        showToastNotification(`Unassigned ${studentName} from "${game.title}"`);
    } else {
        AppState.assignments.push({
            id: "asg-" + Date.now() + "-" + Math.random().toString(36).substr(2, 4),
            class: cls,
            subject: game.subject,
            skillArea: game.skillArea || '',
            activity: game.activity || '',
            gameId: game.id,
            gameTitle: game.title,
            student: studentName,
            roll: roll,
            status: 'pending',
            score: null,
            assignedDate: new Date().toISOString()
        });
        saveAssignments();
        renderTeacherHub();
        renderKidZone();
        if (AppState.currentView === 'split') renderSplitViews();
        showToastNotification(`Assigned "${game.title}" to ${studentName}! 🚀`);
    }
}

function assignAllStudentsToGame(gameId) {
    const cls = AppState.selectedClass;
    const game = GamesCatalog.find(g => g.id === gameId);
    if (!game) return;

    const roster = StudentRosters[cls] || [];
    let addedCount = 0;

    roster.forEach(st => {
        const alreadyAssigned = AppState.assignments.some(a =>
            a.class === cls && a.gameId === gameId && a.student === st.name
        );
        if (!alreadyAssigned) {
            AppState.assignments.push({
                id: "asg-" + Date.now() + "-" + Math.random().toString(36).substr(2, 4),
                class: cls,
                subject: game.subject,
                skillArea: game.skillArea || '',
                activity: game.activity || '',
                gameId: game.id,
                gameTitle: game.title,
                student: st.name,
                roll: st.roll,
                status: 'pending',
                score: null,
                assignedDate: new Date().toISOString()
            });
            addedCount++;
        }
    });

    saveAssignments();
    renderTeacherHub();
    renderKidZone();
    if (AppState.currentView === 'split') renderSplitViews();
    showToastNotification(`Assigned "${game.title}" to all ${roster.length} students in Class ${cls}! 👥✨`);
}

function showToastNotification(msg) {
    let toast = document.getElementById('mcbToastNotification');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'mcbToastNotification';
        toast.style.cssText = `
                    position: fixed;
                    bottom: 28px;
                    left: 50%;
                    transform: translateX(-50%) translateY(100px);
                    background: #1e1b4b;
                    color: #ffffff;
                    padding: 12px 24px;
                    border-radius: 999px;
                    font-family: var(--font-heading);
                    font-size: 14px;
                    font-weight: 700;
                    box-shadow: 0 12px 32px rgba(15, 23, 42, 0.4);
                    border: 1px solid #334155;
                    z-index: 99999;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    transition: transform 0.28s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.28s;
                    opacity: 0;
                    pointer-events: none;
                `;
        document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.style.opacity = '1';
    toast.style.transform = 'translateX(-50%) translateY(0)';
    if (window._mcbToastTimer) clearTimeout(window._mcbToastTimer);
    window._mcbToastTimer = setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(-50%) translateY(100px)';
    }, 3000);
}

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

    // Get all assigned game IDs for the currently selected class
    const assignedGameIds = AppState.assignments
        .filter(a => a.class === AppState.selectedClass)
        .map(a => a.gameId);

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

/* ====================================================
   QUEST RUNNER (QUESTION UI ENGINE)
   ==================================================== */
function toggleQuestFullscreen() {
    const card = document.getElementById('questRunnerCard');
    if (!card) return;
    const isFull = card.classList.toggle('is-fullscreen');
    const btn = document.getElementById('btnQuestFullscreen');
    if (btn) {
        btn.innerHTML = isFull ? '<span>🗗</span> Exit Fullscreen' : '<span>⛶</span> Fullscreen';
    }
}

function launchQuestRunner() {
    AppState.missionStep = 0;
    AppState.missionAnswers = {};
    isContextAudioPlaying = false;
    isSequencePracticeOpen = false;
    isContextBodyCollapsed = false;

    const game = AppState.activeMissionGame;
    if (game) {
        const titleEl = document.getElementById('questGameHeaderTitle');
        if (titleEl) titleEl.textContent = game.title;
        const badgeEl = document.getElementById('questGameSubjectBadge');
        if (badgeEl) {
            badgeEl.textContent = `${game.subject} • Class ${game.class || AppState.selectedClass}`;
            badgeEl.className = `tac-badge tac-badge-subject ${game.badgeClass || ''}`;
        }
        const playerEl = document.getElementById('questActivePlayerName');
        if (playerEl && AppState.selectedStudent) {
            if (AppState.selectedStudent.name === "Teacher Preview Mode") {
                playerEl.textContent = "👩‍🏫 Teacher Preview Mode";
            } else {
                playerEl.textContent = `${AppState.selectedStudent.name} (Roll #${AppState.selectedStudent.roll})`;
            }
        }
        const skillTag = document.getElementById('questPromptSkillTag');
        if (skillTag) skillTag.textContent = `🎯 ${game.skillArea || 'Core Skill'}`;
        const actTag = document.getElementById('questPromptActTag');
        if (actTag) actTag.textContent = `⚡ ${game.activity || 'Activity'}`;
    }

    document.getElementById('questActiveRunner').style.display = 'block';
    document.getElementById('questCelebrationRunner').style.display = 'none';

    renderQuestStep();
    document.getElementById('questRunnerModal').classList.add('active');
}

function closeQuestRunner() {
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    isContextAudioPlaying = false;
    isSequencePracticeOpen = false;
    const audioBtn = document.getElementById('btnContextAudioPlay');
    if (audioBtn) audioBtn.classList.remove('is-playing');
    if (typeof ReadingStudio !== 'undefined') {
        ReadingStudio.stopSpeech();
        ReadingStudio.hideVocabPopover();
    }
    const card = document.getElementById('questRunnerCard');
    if (card) card.classList.remove('quest-reading-mode');
    const studio = document.getElementById('questReadingStudioContainer');
    if (studio) studio.style.display = 'none';
    const c2 = document.getElementById('c2InteractiveGameContainer');
    if (c2) c2.innerHTML = '';
    document.getElementById('questRunnerModal').classList.remove('active');
    renderKidZone();
    renderTeacherHub();
    if (AppState.currentView === 'split') {
        renderSplitViews();
    }
}

// Web Audio API Sound Synthesizer for Kids Quest
const QuestAudio = {
    enabled: true,
    ctx: null,
    getCtx() {
        if (!this.ctx) {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            if (AudioCtx) this.ctx = new AudioCtx();
        }
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
        return this.ctx;
    },
    playClick() {
        if (!this.enabled) return;
        try {
            const ctx = this.getCtx();
            if (!ctx) return;
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(587.33, ctx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.1);
            gain.gain.setValueAtTime(0.18, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.12);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start();
            osc.stop(ctx.currentTime + 0.13);
        } catch (e) { }
    },
    playNav() {
        if (!this.enabled) return;
        try {
            const ctx = this.getCtx();
            if (!ctx) return;
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(440, ctx.currentTime);
            gain.gain.setValueAtTime(0.12, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.09);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start();
            osc.stop(ctx.currentTime + 0.1);
        } catch (e) { }
    },
    playFanfare() {
        if (!this.enabled) return;
        try {
            const ctx = this.getCtx();
            if (!ctx) return;
            const notes = [523.25, 659.25, 783.99, 1046.5];
            notes.forEach((freq, idx) => {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.value = freq;
                const start = ctx.currentTime + (idx * 0.12);
                gain.gain.setValueAtTime(0.15, start);
                gain.gain.exponentialRampToValueAtTime(0.001, start + 0.35);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(start);
                osc.stop(start + 0.36);
            });
        } catch (e) { }
    }
};

function toggleQuestSound() {
    QuestAudio.enabled = !QuestAudio.enabled;
    const icon = document.getElementById('questSoundIcon');
    if (icon) icon.textContent = QuestAudio.enabled ? '🔊' : '🔇';
    showToastNotification(QuestAudio.enabled ? 'Sound effects enabled! 🔊' : 'Sound effects muted 🔇');
}

function launchQuestConfetti() {
    const canvas = document.getElementById('questConfettiCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    canvas.width = canvas.parentElement.clientWidth || window.innerWidth;
    canvas.height = canvas.parentElement.clientHeight || window.innerHeight;

    const colors = ['#f59e0b', '#ec4899', '#6366f1', '#10b981', '#3b82f6', '#8b5cf6'];
    const particles = [];
    for (let i = 0; i < 70; i++) {
        particles.push({
            x: canvas.width / 2,
            y: canvas.height / 3,
            vx: (Math.random() - 0.5) * 14,
            vy: (Math.random() - 0.8) * 14,
            size: Math.random() * 8 + 4,
            color: colors[Math.floor(Math.random() * colors.length)],
            rotation: Math.random() * 360,
            vRot: (Math.random() - 0.5) * 10,
            opacity: 1
        });
    }

    let frames = 0;
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        let alive = false;
        particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;
            p.vy += 0.35;
            p.rotation += p.vRot;
            p.opacity -= 0.012;
            if (p.opacity > 0) {
                alive = true;
                ctx.save();
                ctx.translate(p.x, p.y);
                ctx.rotate((p.rotation * Math.PI) / 180);
                ctx.fillStyle = p.color;
                ctx.globalAlpha = Math.max(0, p.opacity);
                ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.6);
                ctx.restore();
            }
        });
        frames++;
        if (alive && frames < 120) {
            requestAnimationFrame(animate);
        } else {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
    }
    requestAnimationFrame(animate);
}

/* ====================================================
   ENGLISH READING COMPREHENSION STUDIO CONTROLLER
   Side-by-side passage reader, audio TTS, vocabulary
   tooltips, and evidence highlighting
   ==================================================== */
function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}

function isAnswerCorrect(q, userAns) {
    if (!q || userAns === undefined || userAns === null) return false;
    if (q.type === 'typed') {
        const str = String(userAns).trim().toLowerCase();
        if (!str) return false;
        const expected = String(q.answer).trim().toLowerCase();
        if (str === expected || str.includes(expected) || expected.includes(str)) return true;
        if (q.keywords && Array.isArray(q.keywords)) {
            const hits = q.keywords.filter(kw => str.includes(kw.toLowerCase()));
            return hits.length >= 1;
        }
        return false;
    }
    return userAns === q.answer;
}

const ReadingStudio = {
    currentPassage: null,
    fontSize: 17,
    synth: window.speechSynthesis,
    isSpeaking: false,
    popoverEl: null,

    init(passage, containerEl) {
        this.currentPassage = passage;
        this.stopSpeech();
        this.hideVocabPopover();
        this.renderPassage(containerEl);
    },

    stopSpeech() {
        if (this.synth) {
            this.synth.cancel();
        }
        this.isSpeaking = false;
        const btn = document.getElementById('btnReadingTTS');
        if (btn) {
            btn.classList.remove('is-speaking');
            btn.innerHTML = '<span>▶</span> Read Aloud';
        }
        const paras = document.querySelectorAll('.passage-paragraph');
        paras.forEach(p => p.classList.remove('is-speaking-para'));
    },

    toggleSpeech() {
        if (!this.synth || !this.currentPassage) return;
        if (this.isSpeaking) {
            this.stopSpeech();
            return;
        }

        this.stopSpeech();
        const fullText = this.currentPassage.content.join('. ');
        const utter = new SpeechSynthesisUtterance(fullText);
        utter.rate = 0.92;
        utter.pitch = 1.02;

        const btn = document.getElementById('btnReadingTTS');
        if (btn) {
            btn.classList.add('is-speaking');
            btn.innerHTML = '<span>⏹</span> Stop Audio';
        }
        this.isSpeaking = true;

        utter.onend = () => {
            this.stopSpeech();
        };
        utter.onerror = () => {
            this.stopSpeech();
        };

        this.synth.speak(utter);
    },

    adjustFontSize(delta) {
        this.fontSize = Math.min(24, Math.max(14, this.fontSize + delta));
        const txtEl = document.getElementById('passageTextContainer');
        if (txtEl) {
            txtEl.style.fontSize = `${this.fontSize}px`;
        }
    },

    highlightEvidence(paraIdx) {
        const paras = document.querySelectorAll('.passage-paragraph');
        paras.forEach(p => p.classList.remove('is-evidence-target'));

        const target = document.getElementById(`passagePara-${paraIdx}`);
        if (target) {
            target.classList.add('is-evidence-target');
            target.scrollIntoView({ behavior: 'smooth', block: 'center' });
            setTimeout(() => {
                target.classList.remove('is-evidence-target');
            }, 3500);
        }
    },

    showVocabPopover(word, def, example, targetEl) {
        this.hideVocabPopover();
        const pop = document.createElement('div');
        pop.className = 'vocab-popover-card';
        pop.id = 'activeVocabPopover';
        pop.innerHTML = `
                    <div class="vocab-popover-word">
                        <span>📖 ${word}</span>
                        <button type="button" style="background:none; border:none; color:#f8fafc; cursor:pointer; font-size:14px;" onclick="ReadingStudio.hideVocabPopover()">✕</button>
                    </div>
                    <div class="vocab-popover-def">${def}</div>
                    ${example ? `<div class="vocab-popover-example">"${example}"</div>` : ''}
                `;
        document.body.appendChild(pop);

        const rect = targetEl.getBoundingClientRect();
        const top = rect.bottom + window.scrollY + 8;
        const left = Math.min(window.innerWidth - 330, Math.max(10, rect.left + window.scrollX - 20));
        pop.style.top = `${top}px`;
        pop.style.left = `${left}px`;
        this.popoverEl = pop;
    },

    hideVocabPopover() {
        const old = document.getElementById('activeVocabPopover');
        if (old) old.remove();
        this.popoverEl = null;
    },

    renderPassage(container) {
        if (!this.currentPassage) return;
        const p = this.currentPassage;

        const vocabMap = {};
        if (p.vocabulary && Array.isArray(p.vocabulary)) {
            p.vocabulary.forEach(v => {
                vocabMap[v.word.toLowerCase()] = v;
            });
        }

        let parasHtml = '';
        p.content.forEach((paraText, pIdx) => {
            let processed = paraText;
            Object.keys(vocabMap).forEach(w => {
                const regex = new RegExp(`\\b(${w})\\b`, 'gi');
                processed = processed.replace(regex, (match) => {
                    return `<span class="vocab-word-highlight" data-word="${match}" onclick="ReadingStudio.onVocabClick(event, '${w}')">${match}</span>`;
                });
            });

            parasHtml += `
                        <div class="passage-paragraph" id="passagePara-${pIdx}">
                            <span class="passage-para-badge">¶ ${pIdx + 1}</span>
                            ${processed}
                        </div>
                    `;
        });

        container.innerHTML = `
                    <div class="passage-meta-header">
                        <div class="passage-meta-tags">
                            <span class="passage-badge passage-badge-topic">🏷️ ${p.topic || 'Reading'}</span>
                            <span class="passage-badge passage-badge-genre">📚 ${p.genre || 'Story / Essay'}</span>
                            <span class="passage-badge passage-badge-time">⏱️ ${p.estimatedTime || '3 min read'}</span>
                        </div>
                        <h3 class="passage-title">${p.title}</h3>
                    </div>

                    <div class="reading-toolbar">
                        <div class="reading-audio-controls">
                            <button type="button" class="btn-reading-tts" id="btnReadingTTS" onclick="ReadingStudio.toggleSpeech()">
                                <span>▶</span> Read Aloud
                            </button>
                        </div>
                        <div class="reading-font-controls">
                            <span class="font-ctrl-label">Text Size:</span>
                            <button type="button" class="btn-font-size" onclick="ReadingStudio.adjustFontSize(-2)" title="Smaller text">A-</button>
                            <button type="button" class="btn-font-size" onclick="ReadingStudio.adjustFontSize(2)" title="Larger text">A+</button>
                        </div>
                    </div>

                    <div class="passage-text-container" id="passageTextContainer" style="font-size: ${this.fontSize}px;">
                        ${parasHtml}
                    </div>
                `;
    },

    onVocabClick(e, wordKey) {
        e.stopPropagation();
        if (!this.currentPassage || !this.currentPassage.vocabulary) return;
        const item = this.currentPassage.vocabulary.find(v => v.word.toLowerCase() === wordKey.toLowerCase());
        if (item) {
            this.showVocabPopover(item.word, item.definition, item.example || '', e.target);
        }
    }
};

// Global dismiss for vocab popover
document.addEventListener('click', (e) => {
    if (!e.target.closest('.vocab-popover-card') && !e.target.closest('.vocab-word-highlight')) {
        ReadingStudio.hideVocabPopover();
    }
});

function cleanQuestionPrompt(text) {
    if (!text || typeof text !== 'string') return text || '';
    return text.replace(/^\s*\[Class\s+[^\]]+\]\s*/i, '').trim();
}

function selectReadingMCQAnswer(idx) {
    QuestAudio.playClick();
    AppState.missionAnswers[AppState.missionStep] = idx;
    renderQuestStep();
}

function submitTypedReadingAnswer() {
    const inp = document.getElementById('readingTypedInput');
    if (!inp) return;
    const text = inp.value.trim();
    if (!text) {
        showToastNotification("Please type your response based on the text! ✍️");
        return;
    }
    QuestAudio.playClick();
    AppState.missionAnswers[AppState.missionStep] = text;
    renderQuestStep();
}

function renderReadingStudioStep(game) {
    const pPane = document.getElementById('questReadingPassagePane');
    const qPane = document.getElementById('questReadingQuizPane');
    if (!pPane || !qPane) return;

    if (!pPane.hasChildNodes() || ReadingStudio.currentPassage !== game.passage) {
        ReadingStudio.init(game.passage, pPane);
    }

    const qList = game.questions;
    const total = qList.length;
    const q = qList[AppState.missionStep];
    const userAns = AppState.missionAnswers[AppState.missionStep];
    const isAnswered = userAns !== undefined && userAns !== null && String(userAns).trim().length > 0;

    let stepperHtml = '<div class="quest-stepper-row" style="margin-bottom: 12px;">';
    qList.forEach((_, sIdx) => {
        const isCurrent = sIdx === AppState.missionStep;
        const answered = AppState.missionAnswers[sIdx] !== undefined;
        stepperHtml += `<div class="quest-step-pill ${isCurrent ? 'active' : ''} ${answered ? 'answered' : ''}" onclick="QuestAudio.playNav(); AppState.missionStep = ${sIdx}; renderQuestStep();">Q${sIdx + 1} ${answered ? '✓' : ''}</div>`;
    });
    stepperHtml += '</div>';

    const isTyped = q.type === 'typed';
    const typeLabel = isTyped ? '✍️ Short Answer' : '🎯 Multiple Choice';

    const clueBtn = q.evidenceParagraph !== undefined
        ? `<button type="button" class="btn-show-evidence" onclick="ReadingStudio.highlightEvidence(${q.evidenceParagraph})">🔍 Find in Text (¶ ${q.evidenceParagraph + 1})</button>`
        : '';

    let answerHtml = '';
    if (isTyped) {
        const val = userAns || '';
        let fbHtml = '';
        if (isAnswered) {
            const ok = isAnswerCorrect(q, userAns);
            fbHtml = `<div class="typed-feedback-box ${ok ? 'correct' : 'wrong'}">
                        ${ok ? '✅ Excellent text evidence!' : '💡 Expected answer: ' + q.answer}
                        ${q.explanation ? '<br><span style="font-weight:400; font-size:12.5px;">' + q.explanation + '</span>' : ''}
                    </div>`;
        }

        answerHtml = `
                    <div class="reading-typed-container">
                        <input type="text" id="readingTypedInput" class="reading-typed-input" placeholder="Type your answer based on the passage..." value="${escapeHtml(val)}" ${isAnswered ? '' : 'autofocus'}>
                        <div class="reading-typed-actions">
                            <button type="button" class="btn-typed-submit" id="btnSubmitTyped" onclick="submitTypedReadingAnswer()">
                                ${isAnswered ? 'Update Answer' : 'Check Answer ✓'}
                            </button>
                        </div>
                        ${fbHtml}
                    </div>
                `;
    } else {
        const keys = ['A', 'B', 'C', 'D'];
        const badgeClasses = ['badge-a', 'badge-b', 'badge-c', 'badge-d'];
        answerHtml = '<div class="quest-choices-grid" style="grid-template-columns: 1fr; gap: 10px; margin-top: 14px;">';
        (q.options || []).forEach((optText, optIdx) => {
            const isSelected = userAns === optIdx;
            answerHtml += `
                        <button type="button" class="quest-choice-btn ${isSelected ? 'selected' : ''}" onclick="selectReadingMCQAnswer(${optIdx})">
                            <div class="choice-main-content">
                                <span class="choice-key-badge ${badgeClasses[optIdx % 4]}">${keys[optIdx % 4]}</span>
                                <span style="line-height: 1.4;">${optText}</span>
                            </div>
                            <div class="choice-check-indicator">✓</div>
                        </button>
                    `;
        });
        answerHtml += '</div>';

        if (isAnswered && q.explanation) {
            const ok = userAns === q.answer;
            answerHtml += `
                        <div class="typed-feedback-box ${ok ? 'correct' : 'wrong'}" style="margin-top: 14px;">
                            ${ok ? '✅ Correct!' : '❌ Incorrect.'} <span style="font-weight:400; font-size:12.5px;">${q.explanation}</span>
                        </div>
                    `;
        }
    }

    const answeredCount = Object.keys(AppState.missionAnswers).length;
    const pct = Math.round((answeredCount / total) * 100);

    qPane.innerHTML = `
                <div>
                    ${stepperHtml}

                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <div style="font-family: var(--font-heading); font-size: 13px; font-weight: 800; color: #6d28d9;">
                            Question ${AppState.missionStep + 1} of ${total}
                        </div>
                        <div style="font-size: 12.5px; font-weight: 800; color: #b45309;">
                            ${pct}% Complete ⭐
                        </div>
                    </div>

                    <div class="quest-progress-track" style="margin-bottom: 14px;">
                        <div class="quest-progress-fill" style="width: ${(AppState.missionStep + 1) / total * 100}%;"></div>
                    </div>

                    <div class="reading-question-card">
                        <div class="reading-question-header">
                            <span class="reading-type-badge">${typeLabel}</span>
                            ${clueBtn}
                        </div>
                        <h3 class="reading-question-title">${cleanQuestionPrompt(q.prompt)}</h3>
                        ${answerHtml}
                    </div>
                </div>

                <div class="quest-footer-bar" style="margin-top: 16px;">
                    <button type="button" class="btn-quest-back" onclick="navigateQuest(-1)" style="visibility: ${AppState.missionStep > 0 ? 'visible' : 'hidden'}">
                        <span>←</span> Previous
                    </button>
                    <div class="quest-footer-hint" style="font-size: 12px;">
                        <span>💡</span> Hint: Check the left pane for details!
                    </div>
                    <button type="button" class="btn-quest-next-step" onclick="navigateQuest(1)">
                        ${AppState.missionStep === total - 1 ? 'Submit Challenge 🚀' : 'Next question →'}
                    </button>
                </div>
            `;

    if (isTyped) {
        const inp = document.getElementById('readingTypedInput');
        if (inp) {
            inp.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') submitTypedReadingAnswer();
            });
        }
    }
}

function renderQuestStep() {
    const game = AppState.activeMissionGame;
    if (!game) return;

    const c2Container = document.getElementById('c2InteractiveGameContainer');
    const studioContainer = document.getElementById('questReadingStudioContainer');
    const card = document.getElementById('questRunnerCard');
    const standardElements = [
        document.getElementById('questStepperRow'),
        document.getElementById('questStepCounter') ? document.getElementById('questStepCounter').parentElement : null,
        document.querySelector('.quest-progress-track'),
        document.querySelector('.quest-prompt-card'),
        document.getElementById('questChoicesGrid'),
        document.querySelector('.quest-footer-bar')
    ];

    // Direct-manipulation Tactile Mini-Game for Class 2
    if (window.Class2Games && window.Class2Games.isClass2Interactive(game)) {
        if (card) card.classList.remove('quest-reading-mode');
        if (studioContainer) studioContainer.style.display = 'none';
        standardElements.forEach(el => { if (el) el.style.display = 'none'; });
        if (c2Container) {
            c2Container.style.display = 'block';
            window.Class2Games.render(c2Container, game, (result) => {
                AppState.missionAnswers = {};
                const qCount = (game.questions && game.questions.length) || result.total || 3;
                for (let i = 0; i < qCount; i++) {
                    if (i < result.score) {
                        AppState.missionAnswers[i] = (game.questions && game.questions[i]) ? game.questions[i].answer : 0;
                    } else {
                        const cor = (game.questions && game.questions[i]) ? game.questions[i].answer : 0;
                        AppState.missionAnswers[i] = (cor + 1) % 4;
                    }
                }
                finishQuestAndShowReview();
            });
        }
        return;
    }

    // Side-by-Side Reading Comprehension Studio
    const isReadingStudio = !!(game.passage && game.passage.content);
    if (isReadingStudio) {
        if (card) card.classList.add('quest-reading-mode');
        standardElements.forEach(el => { if (el) el.style.display = 'none'; });
        if (c2Container) c2Container.style.display = 'none';
        if (studioContainer) studioContainer.style.display = 'block';

        renderReadingStudioStep(game);
        return;
    } else {
        if (card) card.classList.remove('quest-reading-mode');
        if (studioContainer) studioContainer.style.display = 'none';
    }

    // Standard MCQ / Visual Diagram Quest Runner
    if (c2Container) c2Container.style.display = 'none';
    standardElements.forEach(el => { if (el) el.style.display = ''; });

    // Dedicated Context / Spoken Passage / Lab Procedure & Steps Studio
    renderQuestContext(game);

    const qList = game.questions;
    const total = qList.length;
    const q = qList[AppState.missionStep];

    // Render Stepper Row
    const stepper = document.getElementById('questStepperRow');
    if (stepper) {
        stepper.innerHTML = '';
        qList.forEach((_, sIdx) => {
            const isCurrent = sIdx === AppState.missionStep;
            const isAnswered = AppState.missionAnswers[sIdx] !== undefined;
            const pill = document.createElement('div');
            pill.className = `quest-step-pill ${isCurrent ? 'active' : ''} ${isAnswered ? 'answered' : ''}`;
            pill.innerHTML = `Q${sIdx + 1} ${isAnswered ? '✓' : ''}`;
            pill.onclick = () => {
                QuestAudio.playNav();
                AppState.missionStep = sIdx;
                renderQuestStep();
            };
            stepper.appendChild(pill);
        });
    }

    document.getElementById('questStepCounter').textContent = `Question ${AppState.missionStep + 1} of ${total}`;
    const answeredCount = Object.keys(AppState.missionAnswers).length;
    const pct = Math.round((answeredCount / total) * 100);
    document.getElementById('questProgressFill').style.width = `${pct}%`;
    const pctLabel = document.getElementById('questPercentLabel');
    if (pctLabel) pctLabel.textContent = `${pct}% Complete (${answeredCount}/${total} Answered) ⭐`;

    const tips = [
        "Take your time. Curiosity is your superpower! 🚀",
        "Read carefully and trust your instincts! ⭐",
        "You are doing awesome, keep going! 🌟",
        "Every question makes you smarter! 💡"
    ];
    const tipEl = document.getElementById('questFooterTip');
    if (tipEl) tipEl.innerHTML = `<span>💡</span> ${tips[AppState.missionStep % tips.length]}`;

    // Update Skill Area & Activity Tags
    const skillTag = document.getElementById('questPromptSkillTag');
    const actTag = document.getElementById('questPromptActTag');
    if (skillTag) {
        skillTag.textContent = `🎯 ${game.subject || ''} • ${game.skillArea || ''}`;
    }
    if (actTag) {
        actTag.style.display = 'inline-flex';
        actTag.textContent = `⚡ ${game.gameType || 'Activity'}`;

        // Color-code activity badge based on gameType
        if (game.gameType === 'Sequence Order') {
            actTag.style.cssText = 'background:#ecfdf5; color:#065f46; border:1px solid #a7f3d0; font-size:11px; font-weight:800; border-radius:999px; padding:3px 10px; display:inline-flex;';
        } else if (game.gameType === 'Fill in the Blank') {
            actTag.style.cssText = 'background:#fffbeb; color:#92400e; border:1px solid #fde68a; font-size:11px; font-weight:800; border-radius:999px; padding:3px 10px; display:inline-flex;';
        } else if (game.gameType === 'Match Pairs') {
            actTag.style.cssText = 'background:#eff6ff; color:#1e40af; border:1px solid #bfdbfe; font-size:11px; font-weight:800; border-radius:999px; padding:3px 10px; display:inline-flex;';
        } else if (game.gameType === 'Sort & Group') {
            actTag.style.cssText = 'background:#fdf2f8; color:#9d174d; border:1px solid #fbcfe8; font-size:11px; font-weight:800; border-radius:999px; padding:3px 10px; display:inline-flex;';
        } else if (game.gameType === 'Word Scramble') {
            actTag.style.cssText = 'background:#f5f3ff; color:#5b21b6; border:1px solid #ddd6fe; font-size:11px; font-weight:800; border-radius:999px; padding:3px 10px; display:inline-flex;';
        } else {
            actTag.style.cssText = 'background:#ede9fe; color:#5b21b6; border:1px solid #c4b5fd; font-size:11px; font-weight:800; border-radius:999px; padding:3px 10px; display:inline-flex;';
        }
    }

    // Clean & format question prompt (Highlight blanks for Fill in the Blank)
    let rawPrompt = cleanQuestionPrompt(q.prompt);
    if (game.gameType === 'Fill in the Blank' || rawPrompt.includes('_____')) {
        document.getElementById('questPromptTitle').innerHTML = rawPrompt.replace(/_{3,}/g, '<span class="fitb-blank">[ ________ ]</span>');
    } else {
        document.getElementById('questPromptTitle').textContent = rawPrompt;
    }

    // Multi-Modal Visual Clue & Diagram Rendering
    const visualCont = document.getElementById('questVisualContainer');
    const diagBox = document.getElementById('questDiagramBox');
    const cluePill = document.getElementById('questCluePill');

    if (visualCont && diagBox && cluePill) {
        const hasSvg = q.svg_diagram && q.svg_diagram.includes('<svg');
        const hasClue = q.visual_hint && q.visual_hint.trim().length > 0;

        if (hasSvg || hasClue) {
            visualCont.style.display = 'flex';
            if (hasSvg) {
                diagBox.innerHTML = q.svg_diagram;
                diagBox.style.display = 'flex';
            } else {
                diagBox.innerHTML = '';
                diagBox.style.display = 'none';
            }

            if (hasClue) {
                cluePill.textContent = q.visual_hint;
                cluePill.style.display = 'inline-flex';
            } else {
                cluePill.textContent = '';
                cluePill.style.display = 'none';
            }
        } else {
            visualCont.style.display = 'none';
        }
    }

    const grid = document.getElementById('questChoicesGrid');
    grid.innerHTML = '';

    const isTypedInput = q.type === 'typed' || (game.gameType === 'Typing Answer' && (!q.options || q.options.length <= 1));

    if (isTypedInput) {
        const userAns = AppState.missionAnswers[AppState.missionStep] || '';
        const isAnswered = String(userAns).trim().length > 0;
        grid.style.gridTemplateColumns = '1fr';
        grid.innerHTML = `
                    <div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 14px; padding: 18px 20px;">
                        <label style="display: block; font-family: var(--font-heading); font-size: 13px; font-weight: 700; color: #475569; margin-bottom: 8px;">
                            ✍️ Type your response below:
                        </label>
                        <div style="display: flex; gap: 10px;">
                            <input type="text" id="standardTypedInput" value="${escapeHtml(userAns)}" placeholder="Type your answer here..." style="flex: 1; padding: 12px 16px; border: 2px solid #e2e8f0; border-radius: 10px; font-size: 15px; outline: none; font-family: var(--font-body);" ${isAnswered ? '' : 'autofocus'}>
                            <button type="button" class="btn-typed-submit" id="btnSubmitStandardTyped" onclick="submitStandardTypedAnswer()" style="background: #4f46e5; color: #ffffff; border: none; border-radius: 10px; padding: 12px 20px; font-weight: 700; cursor: pointer;">
                                ${isAnswered ? 'Update ✓' : 'Save Answer ✓'}
                            </button>
                        </div>
                    </div>
                `;
        const inp = document.getElementById('standardTypedInput');
        if (inp) {
            inp.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') submitStandardTypedAnswer();
            });
        }
    } else {
        grid.style.gridTemplateColumns = '';
        const keys = ['A', 'B', 'C', 'D'];
        const badgeClasses = ['badge-a', 'badge-b', 'badge-c', 'badge-d'];

        (q.options || []).forEach((optText, idx) => {
            const isSelected = AppState.missionAnswers[AppState.missionStep] === idx;
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = `quest-choice-btn ${isSelected ? 'selected' : ''}`;
            btn.onclick = () => {
                QuestAudio.playClick();
                AppState.missionAnswers[AppState.missionStep] = idx;
                renderQuestStep();
            };

            btn.innerHTML = `
                        <div class="choice-main-content">
                            <span class="choice-key-badge ${badgeClasses[idx % 4]}">${keys[idx % 4]}</span>
                            <span style="line-height: 1.4;">${optText}</span>
                        </div>
                        <div class="choice-check-indicator">✓</div>
                    `;
            grid.appendChild(btn);
        });
    }

    document.getElementById('btnQuestPrev').style.visibility = AppState.missionStep > 0 ? 'visible' : 'hidden';
    document.getElementById('btnQuestNext').innerHTML = AppState.missionStep === total - 1
        ? 'Submit Challenge <span>🚀</span>'
        : 'Next question <span>→</span>';
}

function submitStandardTypedAnswer() {
    const inp = document.getElementById('standardTypedInput');
    if (!inp) return;
    const text = inp.value.trim();
    if (!text) {
        showToastNotification("Please type your answer! ✍️");
        return;
    }
    QuestAudio.playClick();
    AppState.missionAnswers[AppState.missionStep] = text;
    renderQuestStep();
}

/* ====================================================
   QUEST CONTEXT STUDIO & AUDIO PLAYBACK ENGINE
   Handles spoken scripts, lab procedure steps, and
   interactive sequence ordering practice.
   ==================================================== */
let activeContextAudioUtterance = null;
let isContextAudioPlaying = false;
let isContextBodyCollapsed = false;
let isSequencePracticeOpen = false;
let currentShuffledSteps = [];

function renderQuestContext(game) {
    const ctxCard = document.getElementById('questContextCard');
    if (!ctxCard) return;

    const hasInstructions = Array.isArray(game.instructions) && game.instructions.length > 0;
    const hasAudioScript = !!(game.audio_script && game.audio_script.trim().length > 0);
    const hasStory = !!(game.story && game.story.trim().length > 0);
    const hasContext = hasInstructions || hasAudioScript || hasStory || game.skillArea === 'Listening';

    if (!hasContext) {
        ctxCard.style.display = 'none';
        return;
    }

    ctxCard.style.display = 'block';

    const ctxIcon = document.getElementById('questContextIcon');
    const ctxTitle = document.getElementById('questContextTitle');
    const ctxSubtitle = document.getElementById('questContextSubtitle');
    const ctxPill = document.getElementById('questContextPill');
    const stepsList = document.getElementById('questStepsList');
    const narrativeBox = document.getElementById('questNarrativeBox');
    const practiceBtn = document.getElementById('btnContextPracticeSeq');
    const seqInteractiveBox = document.getElementById('questSeqInteractiveBox');

    // Icon & Pill Badges
    if (game.skillArea === 'Listening') {
        ctxIcon.textContent = '🎧';
        ctxPill.textContent = 'Listening Studio';
        ctxPill.style.background = '#ede9fe';
        ctxPill.style.color = '#5b21b6';
    } else if (game.gameType === 'Sequence Order') {
        ctxIcon.textContent = game.subject === 'Science' ? '🔬' : (game.subject === 'Social Science' ? '⏳' : '🔢');
        ctxPill.textContent = 'Sequence Order';
        ctxPill.style.background = '#ecfdf5';
        ctxPill.style.color = '#065f46';
    } else {
        ctxIcon.textContent = '📋';
        ctxPill.textContent = game.gameType || 'Context';
    }

    // Title & Subtitle
    if (hasInstructions) {
        if (game.subject === 'Science') {
            ctxTitle.textContent = '🔬 Laboratory Procedure & Steps';
            ctxSubtitle.textContent = 'Follow the numbered procedure steps to answer this quest accurately';
        } else if (game.subject === 'Social Science') {
            ctxTitle.textContent = '⏳ Historical Timeline & Sequence';
            ctxSubtitle.textContent = 'Follow the chronological sequence of events to solve this challenge';
        } else {
            ctxTitle.textContent = '📋 Step-by-Step Instructions';
            ctxSubtitle.textContent = 'Follow the sequence of instructions below to answer this quest';
        }
    } else {
        ctxTitle.textContent = game.skillArea === 'Listening' ? '🎧 Spoken Audio Script & Passage' : '📖 Story & Background Context';
        ctxSubtitle.textContent = 'Listen carefully to the audio narration or read along below';
    }

    // Steps vs Narrative
    if (hasInstructions) {
        stepsList.style.display = 'flex';
        narrativeBox.style.display = 'none';
        stepsList.innerHTML = '';

        game.instructions.forEach((stepText, idx) => {
            const stepItem = document.createElement('div');
            stepItem.className = 'quest-step-item';

            // Highlight step if current question refers to this step
            const currentQ = (game.questions && game.questions[AppState.missionStep]) ? game.questions[AppState.missionStep] : null;
            const qPrompt = currentQ ? currentQ.prompt.toLowerCase() : '';

            const stepMatch = (idx === 0 && (qPrompt.includes('first') || qPrompt.includes('step 1') || qPrompt.includes('label three'))) ||
                (idx === 1 && (qPrompt.includes('second') || qPrompt.includes('step 2') || qPrompt.includes('distilled water'))) ||
                (idx === 2 && (qPrompt.includes('third') || qPrompt.includes('step 3') || qPrompt.includes('indicator') || qPrompt.includes('tube b'))) ||
                (idx === 3 && (qPrompt.includes('fourth') || qPrompt.includes('step 4') || qPrompt.includes('swirl') || qPrompt.includes('after swirling'))) ||
                (idx === 4 && (qPrompt.includes('fifth') || qPrompt.includes('step 5') || qPrompt.includes('final') || qPrompt.includes('last') || qPrompt.includes('record')));

            if (stepMatch) {
                stepItem.classList.add('is-highlighted');
            }

            const prefix = (game.subject === 'Social Science' && (stepText.startsWith('Era') || stepText.startsWith('Epoch') || stepText.startsWith('Period')))
                ? 'Timeline ' + (idx + 1)
                : 'Step ' + (idx + 1);

            stepItem.innerHTML = `
                        <span class="step-num-pill">${prefix}</span>
                        <span class="step-item-text">${escapeHtml(stepText)}</span>
                    `;
            stepsList.appendChild(stepItem);
        });

        if (practiceBtn) {
            practiceBtn.style.display = (game.gameType === 'Sequence Order') ? 'inline-flex' : 'none';
        }
    } else {
        stepsList.style.display = 'none';
        narrativeBox.style.display = 'block';
        narrativeBox.innerHTML = `
                    <div style="font-style: italic; color: #475569; margin-bottom: 6px; font-size: 12px; font-weight: 700;">
                        ${game.skillArea === 'Listening' ? '🎙️ Spoken Passage:' : '📜 Context:'}
                    </div>
                    <div>${escapeHtml(game.audio_script || game.story)}</div>
                `;
        if (practiceBtn) practiceBtn.style.display = 'none';
    }

    if (seqInteractiveBox && !isSequencePracticeOpen) {
        seqInteractiveBox.style.display = 'none';
    }
}

function toggleContextAudio() {
    const game = AppState.activeMissionGame;
    if (!game) return;

    const btn = document.getElementById('btnContextAudioPlay');
    const icon = document.getElementById('contextAudioBtnIcon');
    const label = document.getElementById('contextAudioBtnLabel');

    if (isContextAudioPlaying) {
        if ('speechSynthesis' in window) window.speechSynthesis.cancel();
        isContextAudioPlaying = false;
        if (btn) btn.classList.remove('is-playing');
        if (icon) icon.textContent = '▶';
        if (label) label.textContent = 'Listen to Audio';
        return;
    }

    const textToSpeak = game.audio_script || (game.instructions ? game.instructions.join('. ') : '') || game.story;
    if (!textToSpeak) {
        showToastNotification("No audio narration available for this activity.");
        return;
    }

    if (!('speechSynthesis' in window)) {
        showToastNotification("Speech synthesis is not supported in this browser.");
        return;
    }

    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(textToSpeak);
    utter.rate = 0.90;
    utter.pitch = 1.05;

    const voices = window.speechSynthesis.getVoices();
    const enVoice = voices.find(v => v.lang.startsWith('en-IN')) || voices.find(v => v.lang.startsWith('en'));
    if (enVoice) utter.voice = enVoice;

    utter.onstart = () => {
        isContextAudioPlaying = true;
        if (btn) btn.classList.add('is-playing');
        if (icon) icon.textContent = '⏹';
        if (label) label.textContent = 'Stop Audio';
    };

    utter.onend = () => {
        isContextAudioPlaying = false;
        if (btn) btn.classList.remove('is-playing');
        if (icon) icon.textContent = '▶';
        if (label) label.textContent = 'Listen to Audio';
    };

    utter.onerror = () => {
        isContextAudioPlaying = false;
        if (btn) btn.classList.remove('is-playing');
        if (icon) icon.textContent = '▶';
        if (label) label.textContent = 'Listen to Audio';
    };

    activeContextAudioUtterance = utter;
    window.speechSynthesis.speak(utter);
}

function toggleContextBody() {
    const body = document.getElementById('questContextBody');
    const label = document.getElementById('contextToggleLabel');
    if (!body) return;
    isContextBodyCollapsed = !isContextBodyCollapsed;
    body.style.display = isContextBodyCollapsed ? 'none' : 'block';
    if (label) label.textContent = isContextBodyCollapsed ? 'Show Details' : 'Hide Details';
}

function toggleSequenceOrderPractice() {
    const game = AppState.activeMissionGame;
    if (!game || !game.instructions || game.instructions.length === 0) return;

    const box = document.getElementById('questSeqInteractiveBox');
    if (!box) return;

    isSequencePracticeOpen = !isSequencePracticeOpen;
    if (!isSequencePracticeOpen) {
        box.style.display = 'none';
        return;
    }

    box.style.display = 'block';
    // Shuffle steps
    currentShuffledSteps = game.instructions.map((text, originalIndex) => ({
        text,
        originalIndex
    })).sort(() => Math.random() - 0.5);

    renderSequenceOrderPractice(game);
}

function renderSequenceOrderPractice(game) {
    const box = document.getElementById('questSeqInteractiveBox');
    if (!box) return;

    const isAllCorrect = currentShuffledSteps.every((item, idx) => item.originalIndex === idx);

    let html = `
                <div class="seq-practice-head">
                    <div class="seq-practice-title">🔄 Step Re-ordering Practice: Arrange the steps in the correct order (1 to ${currentShuffledSteps.length})</div>
                    <button type="button" class="btn-context-toggle" onclick="toggleSequenceOrderPractice()">Close ✕</button>
                </div>
                <div class="seq-slots-list">
            `;

    currentShuffledSteps.forEach((item, idx) => {
        const isCorrectSlot = item.originalIndex === idx;
        html += `
                    <div class="seq-draggable-step ${isCorrectSlot ? 'is-correct-slot' : ''}">
                        <div style="display: flex; align-items: center; gap: 10px; flex: 1;">
                            <span class="step-num-pill" style="${isCorrectSlot ? 'background:#10b981;' : ''}">Slot ${idx + 1} ${isCorrectSlot ? '✓' : ''}</span>
                            <span style="font-size: 13.5px; font-weight: 500; color: #1e293b; line-height: 1.4;">${escapeHtml(item.text)}</span>
                        </div>
                        <div class="seq-step-arrows">
                            <button type="button" class="btn-seq-move" onclick="moveSequenceStep(${idx}, -1)" ${idx === 0 ? 'disabled style=\"opacity:0.3; cursor:default;\"' : ''} title=\"Move up\">▲</button>
                            <button type="button" class="btn-seq-move" onclick="moveSequenceStep(${idx}, 1)" ${idx === currentShuffledSteps.length - 1 ? 'disabled style=\"opacity:0.3; cursor:default;\"' : ''} title=\"Move down\">▼</button>
                        </div>
                    </div>
                `;
    });

    html += `</div>`;

    if (isAllCorrect) {
        html += `
                    <div style="margin-top: 12px; background: #ecfdf5; border: 1.5px solid #a7f3d0; border-radius: 10px; padding: 10px 14px; color: #065f46; font-weight: 700; font-size: 13.5px; text-align: center;">
                        🎉 Outstanding! You arranged all steps in perfect order!
                    </div>
                `;
        QuestAudio.playCorrect();
    }

    box.innerHTML = html;
}

function moveSequenceStep(index, direction) {
    const targetIndex = index + direction;
    if (targetIndex < 0 || targetIndex >= currentShuffledSteps.length) return;
    const temp = currentShuffledSteps[index];
    currentShuffledSteps[index] = currentShuffledSteps[targetIndex];
    currentShuffledSteps[targetIndex] = temp;
    QuestAudio.playClick();
    renderSequenceOrderPractice(AppState.activeMissionGame);
}

function navigateQuest(delta) {
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    isContextAudioPlaying = false;
    const audioBtn = document.getElementById('btnContextAudioPlay');
    if (audioBtn) audioBtn.classList.remove('is-playing');
    const icon = document.getElementById('contextAudioBtnIcon');
    if (icon) icon.textContent = '▶';
    const label = document.getElementById('contextAudioBtnLabel');
    if (label) label.textContent = 'Listen to Audio';

    const total = AppState.activeMissionGame.questions.length;
    const next = AppState.missionStep + delta;

    if (next >= total) {
        finishQuestAndShowReview();
    } else if (next >= 0) {
        AppState.missionStep = next;
        renderQuestStep();
    }
}

function speakCurrentQuestPrompt() {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const game = AppState.activeMissionGame;
    const q = game && game.questions ? game.questions[AppState.missionStep] : null;
    if (!q) return;

    let textToSpeak = cleanQuestionPrompt(q.prompt);
    textToSpeak = textToSpeak.replace(/_{2,}/g, 'blank');

    if (q.options && q.options.length > 0) {
        textToSpeak += '. Option A: ' + q.options[0] + '. Option B: ' + q.options[1];
        if (q.options[2]) textToSpeak += '. Option C: ' + q.options[2];
        if (q.options[3]) textToSpeak += '. Option D: ' + q.options[3];
    }

    const utter = new SpeechSynthesisUtterance(textToSpeak);
    utter.rate = 0.95;
    utter.pitch = 1.05;
    window.speechSynthesis.speak(utter);
}

function retakeCurrentQuest() {
    showToastNotification("Activity completed! You do not need to do this task again. 🎉");
    closeQuestRunner();
}

/* ====================================================
   FINISH QUEST & POST-TEST ANSWER REVIEW
   ==================================================== */
function finishQuestAndShowReview() {
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    QuestAudio.playFanfare();
    launchQuestConfetti();

    const game = AppState.activeMissionGame;
    const qList = game.questions;
    const total = qList.length;

    let correct = 0;
    qList.forEach((q, idx) => {
        if (isAnswerCorrect(q, AppState.missionAnswers[idx])) correct++;
    });

    const wrong = total - correct;
    const pct = Math.round((correct / total) * 100);

    // Save completed state to assignments (only if not in Teacher Preview Mode)
    if (AppState.selectedStudent && AppState.selectedStudent.name !== "Teacher Preview Mode") {
        let existing = AppState.assignments.find(a =>
            a.class === AppState.selectedClass &&
            a.gameId === game.id &&
            a.student === AppState.selectedStudent.name
        );

        if (existing) {
            existing.status = 'completed';
            existing.score = correct;
            existing.maxScore = total;
        } else {
            AppState.assignments.push({
                id: "asg-" + Date.now(),
                class: AppState.selectedClass,
                subject: game.subject,
                skillArea: game.skillArea || '',
                activity: game.activity || '',
                gameId: game.id,
                gameTitle: game.title,
                student: AppState.selectedStudent.name,
                roll: AppState.selectedStudent.roll,
                status: 'completed',
                score: correct,
                maxScore: total
            });
        }
        saveAssignments();
    }
    renderKidZone();
    renderTeacherHub();
    if (AppState.currentView === 'split') {
        renderSplitViews();
    }

    // Populate Review Header
    const trophyEl = document.getElementById('celebTrophyEmoji');
    const titleEl = document.getElementById('celebMainTitle');
    const subEl = document.getElementById('celebSubTitle');
    const isTeacherPreview = AppState.selectedStudent && AppState.selectedStudent.name === "Teacher Preview Mode";
    const celebNotice = document.getElementById('celebCompletedNotice');
    if (celebNotice) {
        celebNotice.style.display = isTeacherPreview ? 'none' : 'inline-flex';
    }

    if (isTeacherPreview) {
        trophyEl.textContent = '👁️';
        titleEl.textContent = 'PREVIEW COMPLETED';
        subEl.textContent = `Teacher Preview for ${game.title}. Questions and answers evaluated successfully!`;
    } else if (pct === 100) {
        trophyEl.textContent = '🌟';
        titleEl.textContent = 'PERFECT SCORE! 🏆';
        subEl.textContent = `Amazing work, ${AppState.selectedStudent.name}! You scored 100% on ${game.title}!`;
    } else if (pct >= 65) {
        trophyEl.textContent = '🎉';
        titleEl.textContent = 'GREAT JOB! ⭐';
        subEl.textContent = `Well done, ${AppState.selectedStudent.name}! Here is your answer review:`;
    } else {
        trophyEl.textContent = '💪';
        titleEl.textContent = 'NICE EFFORT! 🚀';
        subEl.textContent = `Good try, ${AppState.selectedStudent.name}! Check the explanations below to learn more!`;
    }

    document.getElementById('reviewScoreText').textContent = `${correct} / ${total}`;
    document.getElementById('reviewAccuracyText').textContent = `${pct}%`;
    document.getElementById('reviewCorrectText').textContent = `${correct}`;
    document.getElementById('reviewWrongText').textContent = `${wrong}`;

    // Populate Detailed Question Review Cards
    const reviewList = document.getElementById('reviewAnswersList');
    reviewList.innerHTML = '';

    qList.forEach((q, idx) => {
        const userChoice = AppState.missionAnswers[idx];
        const isAnswered = userChoice !== undefined && userChoice !== null && String(userChoice).trim().length > 0;
        const isCorrect = isAnswered && isAnswerCorrect(q, userChoice);
        const userText = isAnswered
            ? (q.type === 'typed' ? escapeHtml(String(userChoice)) : (q.options ? q.options[userChoice] : String(userChoice)))
            : 'Not answered';
        const correctText = q.type === 'typed' ? q.answer : (q.options ? q.options[q.answer] : q.answer);

        const card = document.createElement('div');
        card.className = `review-q-card ${isCorrect ? 'is-correct' : 'is-wrong'}`;

        card.innerHTML = `
                    <div class="review-card-head">
                        <div style="flex: 1;">
                            <span style="font-size: 11px; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">Question ${idx + 1}</span>
                            <div class="review-q-prompt-text">${cleanQuestionPrompt(q.prompt)}</div>
                        </div>
                        <span class="review-badge-status ${isCorrect ? 'badge-ans-correct' : 'badge-ans-wrong'}">
                            ${isCorrect ? '✓ Correct (+1 ⭐)' : (isAnswered ? '✗ Incorrect' : '⚠️ Unanswered')}
                        </span>
                    </div>

                    <div class="review-pills-row">
                        <div class="ans-pill ${isCorrect ? 'ans-pill-user-correct' : 'ans-pill-user'}">
                            <strong>Your Answer:</strong> ${userText}
                        </div>
                        ${!isCorrect ? `
                        <div class="ans-pill ans-pill-solution">
                            <strong>Correct Solution:</strong> ${correctText}
                        </div>
                        ` : ''}
                    </div>

                    ${q.explanation ? `
                    <div class="review-exp-box">
                        <span>💡</span>
                        <div><strong>Why?</strong> ${q.explanation}</div>
                    </div>
                    ` : ''}

                    ${q.visual_hint ? `
                    <div style="font-size: 12.5px; color: #4338ca; background: #eef2ff; border-radius: 8px; padding: 6px 12px; margin-top: 8px; font-weight: 600; display: inline-flex; align-items: center; gap: 6px;">
                        <span>🎨 Visual Clue:</span> ${escapeHtml(q.visual_hint)}
                    </div>
                    ` : ''}
                `;
        reviewList.appendChild(card);
    });

    document.getElementById('questActiveRunner').style.display = 'none';
    document.getElementById('questCelebrationRunner').style.display = 'block';
}

/* ====================================================
   TEACHER HUB & CLASS-SPECIFIC ACTIVITIES & PROGRESS BOARD
   ==================================================== */
function renderTeacherHub() {
    const cls = AppState.selectedClass;
    const roster = StudentRosters[cls] || [];

    // Update labels
    const lbl = document.getElementById('teacherCurrentClassLabel');
    if (lbl) lbl.textContent = cls;

    // Sync class dropdown
    const sel = document.getElementById('teacherClassSelect');
    if (sel) sel.value = cls;

    // Sync class selector pills
    document.querySelectorAll('#teacherClassPills .teacher-class-pill').forEach(btn => {
        const btnText = btn.textContent.trim();
        btn.classList.toggle('active', btnText === `Class ${cls}`);
    });

    // Update Subject Filter Chips to ONLY show subjects with activities in this class
    updateTeacherSubjectChips();

    // Get all activities for this class
    const classGames = GamesCatalog.filter(g => g.class === cls);

    // Get assignments for this class
    const classAsgs = AppState.assignments.filter(a => a.class === cls);
    const assignedGameIds = new Set(classAsgs.map(a => a.gameId));
    const completedAsgs = classAsgs.filter(a => a.status === 'completed');
    const pendingAsgs = classAsgs.filter(a => a.status === 'pending');

    // Update Metrics
    const statAssigned = document.getElementById('teacherStatAssignedActivities');
    if (statAssigned) statAssigned.textContent = assignedGameIds.size;
    const statComp = document.getElementById('teacherStatCompleted');
    if (statComp) statComp.textContent = completedAsgs.length;
    const statPend = document.getElementById('teacherStatPending');
    if (statPend) statPend.textContent = pendingAsgs.length;

    // Filter activities by Subject, Search query, and Status
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

    // Group filtered games by Skill Area in order
    const skillGroups = new Map();
    filteredGames.forEach(g => {
        const skill = (g.skillArea || 'Other Topics').trim();
        if (!skillGroups.has(skill)) {
            skillGroups.set(skill, []);
        }
        skillGroups.get(skill).push(g);
    });

    // Within each skill group, sort assigned games first
    skillGroups.forEach((gamesList) => {
        gamesList.sort((a, b) => {
            const aAssigned = classAsgs.filter(asg => asg.gameId === a.id).length;
            const bAssigned = classAsgs.filter(asg => asg.gameId === b.id).length;
            const aHas = aAssigned > 0 ? 1 : 0;
            const bHas = bAssigned > 0 ? 1 : 0;
            if (bHas !== aHas) return bHas - aHas;
            if (bAssigned !== aAssigned) return bAssigned - aAssigned;
            return 0;
        });
    });

    const badgeCount = document.getElementById('teacherBadgeAssignedCount');
    if (badgeCount) badgeCount.textContent = `${filteredGames.length} activities`;

    const mode = AppState.teacherLayoutMode || 'table';
    const tableContainer = document.getElementById('teacherTableContainer');
    const tableBody = document.getElementById('teacherTableBody');
    const grid = document.getElementById('teacherActivitiesGrid');

    if (mode === 'table') {
        if (tableContainer) tableContainer.style.display = 'block';
        if (grid) grid.style.display = 'none';

        if (tableBody) {
            tableBody.innerHTML = '';
            if (filteredGames.length === 0) {
                tableBody.innerHTML = `
                            <tr>
                                <td colspan="3" style="text-align: center; padding: 48px 16px; background: #ffffff;">
                                    <div style="font-size: 38px; margin-bottom: 8px;">📚✨</div>
                                    <h4 style="font-family: var(--font-heading); font-size: 19px; color: #1e1b4b; margin-bottom: 6px;">No activities match this filter</h4>
                                    <p style="color: var(--text-muted); font-size: 13.5px; margin-bottom: 16px;">Try switching to 'All Activities' or selecting a different subject.</p>
                                    <button type="button" class="btn-clear-filters" onclick="resetTeacherFilters()" style="margin: 0 auto;">Reset filters ↺</button>
                                </td>
                            </tr>
                        `;
            } else {
                const isSpecificSubject = AppState.teacherSubjectFilter !== 'all';

                skillGroups.forEach((gamesInSkill, skillName) => {
                    const hasAnyAssignedInSkill = gamesInSkill.some(g => classAsgs.some(a => a.gameId === g.id));
                    // Skill Area Header Row (Order of Skill Area, stated once, NOT on every game!)
                    const headerTr = document.createElement('tr');
                    headerTr.className = 'curriculum-skill-header-row';
                    headerTr.innerHTML = `
                                <td colspan="3">
                                    <div class="skill-header-content">
                                        <div class="skill-header-left">
                                            <span class="skill-header-icon-badge">🎯</span>
                                            <span class="skill-header-title">${skillName}</span>
                                            <span class="skill-header-count">${gamesInSkill.length} ${gamesInSkill.length === 1 ? 'activity' : 'activities'}</span>
                                        </div>
                                        <div class="skill-header-right">
                                            ${hasAnyAssignedInSkill ? `
                                            <button type="button" class="btn-clear-skill-heading" onclick="unassignSkill('${escapeHtml(skillName)}', '${cls}')" title="Unassign all activities in ${escapeHtml(skillName)} from Class ${cls}">
                                                ✕ Clear Skill
                                            </button>
                                            ` : ''}
                                        </div>
                                    </div>
                                </td>
                            `;
                    tableBody.appendChild(headerTr);

                    // Games under this Skill Area
                    gamesInSkill.forEach(g => {
                        const assigned = classAsgs.filter(a => a.gameId === g.id);
                        const totalAssigned = assigned.length;
                        const completed = assigned.filter(a => a.status === 'completed');
                        const compCount = completed.length;
                        const pct = totalAssigned > 0 ? Math.round((compCount / totalAssigned) * 100) : 0;
                        const isAssigned = totalAssigned > 0;

                        const tr = document.createElement('tr');
                        tr.className = `curriculum-row ${isAssigned ? 'is-assigned' : ''}`;
                        tr.innerHTML = `
                                    <td>
                                        <div class="curriculum-title-wrap">
                                            ${!isSpecificSubject ? `<span class="tac-badge tac-badge-subject ${g.badgeClass || ''}">${g.subject}</span>` : ''}
                                            ${g.isCustom ? '<span class="tac-badge tac-badge-custom">⭐ Custom</span>' : ''}
                                            ${(window.Class2Games && window.Class2Games.isClass2Interactive(g)) ? '<span class="tac-badge tac-badge-mini">🎮 Mini-Game</span>' : ''}
                                            <span class="curriculum-title" title="${escapeHtml(g.title)}">${g.title}</span>
                                            <button type="button" class="btn-tac-preview-sm" style="margin-left: auto; flex-shrink: 0;" onclick="previewActivity('${g.id}')" title="Preview activity before assigning">👁️ Preview</button>
                                        </div>
                                    </td>
                                    <td>
                                        <div class="curriculum-progress-wrap">
                                            ${isAssigned ? `
                                            <div class="curriculum-progress-label">
                                                <span class="curriculum-pct ${pct === 100 ? 'done' : 'in-prog'}">
                                                    <strong>${compCount}/${totalAssigned}</strong> completed
                                                </span>
                                                <span class="curriculum-pct-badge ${pct === 100 ? 'done' : ''}">${pct}%</span>
                                            </div>
                                            <div class="tac-progress-bar">
                                                <div class="tac-progress-fill ${pct === 100 ? 'full' : ''}" style="width: ${pct}%;"></div>
                                            </div>
                                            ` : `
                                            <span class="curriculum-empty-dash">—</span>
                                            `}
                                        </div>
                                    </td>
                                    <td>
                                        <div class="curriculum-students-cell">
                                            ${isAssigned ? `
                                            <div class="tac-students-wrap">
                                                ${assigned.map(a => `
                                                    <span class="tac-chip ${a.status === 'completed' ? 'completed' : 'pending'}" title="${a.student} (Roll #${a.roll}) • ${a.status === 'completed' ? `Score: ${a.score || 3}/${a.maxScore || 3} ⭐` : 'Pending'}">
                                                        <span>${a.status === 'completed' ? '✓' : '⏳'}</span>
                                                        <span>${a.student}</span>
                                                        ${a.status === 'completed' && a.score !== undefined && a.score !== null ? `<span class="tac-chip-score">⭐ ${a.score}/${a.maxScore || 3}</span>` : ''}
                                                    </span>
                                                `).join('')}
                                            </div>
                                            ` : `
                                            <span class="curriculum-empty-dash">—</span>
                                            `}
                                        </div>
                                    </td>
                                `;
                        tableBody.appendChild(tr);
                    });
                });
            }
        }
    } else {
        // Grid Mode
        if (tableContainer) tableContainer.style.display = 'none';
        if (grid) {
            grid.style.display = 'grid';
            grid.innerHTML = '';

            if (filteredGames.length === 0) {
                grid.innerHTML = `
                            <div style="grid-column: 1 / -1; text-align: center; padding: 48px; background: #ffffff; border-radius: 20px; border: 1.5px dashed #cbd5e1;">
                                <div style="font-size: 38px; margin-bottom: 8px;">📚✨</div>
                                <h4 style="font-family: var(--font-heading); font-size: 20px; color: #1e1b4b; margin-bottom: 6px;">No activities match this filter</h4>
                                <p style="color: var(--text-muted); font-size: 14px; margin-bottom: 16px;">Try selecting 'All subjects' or resetting your search query.</p>
                                <button type="button" class="btn-clear-filters" onclick="resetTeacherFilters()" style="margin: 0 auto;">Reset filters ↺</button>
                            </div>
                        `;
            } else {
                const isSpecificSubject = AppState.teacherSubjectFilter !== 'all';

                skillGroups.forEach((gamesInSkill, skillName) => {
                    const hasAnyAssignedInSkill = gamesInSkill.some(g => classAsgs.some(a => a.gameId === g.id));
                    // Section Banner for Skill Area in Grid
                    const banner = document.createElement('div');
                    banner.style.cssText = 'grid-column: 1 / -1; margin-top: 14px; margin-bottom: 6px; padding: 10px 16px; background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 12px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;';
                    banner.innerHTML = `
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <span style="font-size: 16px;">🎯</span>
                                    <span style="font-family: var(--font-heading); font-size: 15px; font-weight: 800; color: #1e1b4b;">${skillName}</span>
                                </div>
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <span style="background: #ede9fe; color: #5b21b6; font-family: var(--font-heading); font-weight: 700; font-size: 11.5px; padding: 2px 10px; border-radius: 999px; border: 1px solid #ddd6fe;">
                                        ${gamesInSkill.length} ${gamesInSkill.length === 1 ? 'activity' : 'activities'}
                                    </span>
                                    <button type="button" class="btn-assign-skill-heading" onclick="openAssignModalForSkill('${escapeHtml(skillName)}')" title="Assign activities in ${escapeHtml(skillName)}">
                                        <svg class="assign-icon-dotted" width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                                            <circle cx="8" cy="8" r="6.5" stroke-dasharray="2.2 2.2"/>
                                            <line x1="8" y1="5" x2="8" y2="11"/>
                                            <line x1="5" y1="8" x2="11" y2="8"/>
                                        </svg>
                                        <span>Assign</span>
                                    </button>
                                    ${hasAnyAssignedInSkill ? `
                                    <button type="button" class="btn-clear-assignments-sm" style="padding: 4px 10px; font-size: 11.5px; border-radius: 6px;" title="Unassign all activities in ${escapeHtml(skillName)} from Class ${cls}" onclick="unassignSkill('${escapeHtml(skillName)}', '${cls}')">
                                        ✕ Clear Skill
                                    </button>
                                    ` : ''}
                                </div>
                            `;
                    grid.appendChild(banner);

                    gamesInSkill.forEach(g => {
                        const assigned = classAsgs.filter(a => a.gameId === g.id);
                        const totalAssigned = assigned.length;
                        const completed = assigned.filter(a => a.status === 'completed');
                        const compCount = completed.length;
                        const pct = totalAssigned > 0 ? Math.round((compCount / totalAssigned) * 100) : 0;
                        const isAssigned = totalAssigned > 0;

                        const card = document.createElement('div');
                        card.className = `teacher-activity-card ${isAssigned ? 'is-assigned' : ''}`;

                        card.innerHTML = `
                                    <div style="margin-bottom: 10px;">
                                        <div class="tac-badges" style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                                            ${!isSpecificSubject ? `<span class="tac-badge tac-badge-subject ${g.badgeClass || ''}">${g.subject}</span>` : ''}
                                            ${g.isCustom ? '<span class="tac-badge tac-badge-custom">⭐ Custom</span>' : ''}
                                            ${(window.Class2Games && window.Class2Games.isClass2Interactive(g)) ? '<span class="tac-badge" style="background:#fdf2f8; color:#be185d; border:1px solid #fbcfe8; font-size:10.5px; font-weight:800; border-radius:999px; padding:2px 7px;">🎮 Mini-Game</span>' : ''}
                                            <h4 class="tac-title" style="font-size: 15.5px; margin: 0; display: inline-block;">${g.title}</h4>
                                        </div>
                                    </div>

                                    <div class="tac-progress-wrap" style="padding: 8px 12px; margin-bottom: 10px;">
                                        <div class="tac-progress-header" style="margin-bottom: 4px; font-size: 11.5px;">
                                            <span class="tac-progress-label">Completion:</span>
                                            <span class="tac-progress-metric ${pct === 100 ? 'completed' : (!isAssigned ? 'unassigned' : '')}">
                                                ${isAssigned
                                ? `<strong>${compCount}/${totalAssigned}</strong> (${pct}%)`
                                : 'Not assigned (0%)'}
                                            </span>
                                        </div>
                                        <div class="tac-progress-bar" style="height: 7px;">
                                            <div class="tac-progress-fill ${pct === 100 ? 'full' : ''}" style="width: ${pct}%;"></div>
                                        </div>
                                    </div>

                                    <div class="tac-students-wrap" style="margin-bottom: 10px;">
                                        <div class="tac-students-label" style="font-size: 11px; margin-bottom: 4px; display: flex; justify-content: space-between; align-items: center;">
                                            <span>Assigned Students (${totalAssigned})</span>
                                            ${isAssigned ? `<span style="font-weight: 700; color: ${pct === 100 ? '#15803d' : '#b45309'};">${pct === 100 ? '✓ Done' : `${compCount}/${totalAssigned} Done`}</span>` : ''}
                                        </div>
                                        <div class="tac-student-chips" style="display: flex; flex-wrap: wrap; gap: 4px;">
                                            ${isAssigned
                                ? assigned.map(a => `
                                                    <span class="tac-chip ${a.status === 'completed' ? 'completed' : 'pending'}" style="font-size: 11px; padding: 2px 8px;">
                                                        ${a.status === 'completed' ? `✓ ${a.student}` : `⏳ ${a.student}`}
                                                        ${a.status === 'completed' ? `<span class="tac-chip-stars" style="font-size: 10px;">⭐ ${a.score || 3}/3</span>` : ''}
                                                    </span>
                                                `).join('')
                                : `<span style="color: #94a3b8; font-size: 12px; font-weight: 500;">—</span>`
                            }
                                        </div>
                                    </div>

                                    <div class="tac-footer" style="padding-top: 8px; display: flex; gap: 6px; justify-content: flex-end;">
                                        <button type="button" class="btn-tac-preview" style="padding: 7px 14px; font-size: 12px; width: 100%; justify-content: center; gap: 6px;" onclick="previewActivity('${g.id}')" title="Preview this activity before assigning">
                                            <span>👁️</span> Preview Activity
                                        </button>
                                    </div>
                                `;

                        grid.appendChild(card);
                    });
                });
            }
        }
    }
}

function handleTeacherClassChange(cls) {
    handleClassFilterChange(cls);
}

function updateTeacherSubjectChips() {
    const container = document.getElementById('teacherSubjectChips');
    if (!container) return;

    const cls = AppState.selectedClass;
    const classGames = GamesCatalog.filter(g => g.class === cls);

    // Only subjects that actually have activities in this class
    const presentSubjects = Array.from(new Set(classGames.map(g => g.subject).filter(Boolean)));

    const subjectOrder = ['Mathematics', 'English', 'EVS', 'Science', 'Social Science'];
    presentSubjects.sort((a, b) => {
        const idxA = subjectOrder.indexOf(a);
        const idxB = subjectOrder.indexOf(b);
        return (idxA !== -1 ? idxA : 99) - (idxB !== -1 ? idxB : 99);
    });

    // If selected filter is not present in this class, reset to 'all'
    if (AppState.teacherSubjectFilter !== 'all' && !presentSubjects.includes(AppState.teacherSubjectFilter)) {
        AppState.teacherSubjectFilter = 'all';
    }

    const subjectMeta = {
        'Mathematics': { label: 'Math', dot: 'chip-dot-math' },
        'English': { label: 'English', dot: 'chip-dot-eng' },
        'EVS': { label: 'EVS', dot: 'chip-dot-evs' },
        'Science': { label: 'Science', dot: 'chip-dot-sci' },
        'Social Science': { label: 'Social', dot: 'chip-dot-soc' }
    };

    container.innerHTML = '';

    // 'All' button
    const allBtn = document.createElement('button');
    allBtn.type = 'button';
    allBtn.className = `chip-btn ${AppState.teacherSubjectFilter === 'all' ? 'active' : ''}`;
    allBtn.textContent = 'All';
    allBtn.onclick = function () { filterTeacherSubject('all', this); };
    container.appendChild(allBtn);

    // Dynamically add ONLY subjects that have activities in this class
    presentSubjects.forEach(sub => {
        const meta = subjectMeta[sub] || { label: sub, dot: 'chip-dot-math' };
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = `chip-btn ${AppState.teacherSubjectFilter === sub ? 'active' : ''}`;
        btn.innerHTML = `<span class="chip-dot ${meta.dot}"></span> ${meta.label}`;
        btn.onclick = function () { filterTeacherSubject(sub, this); };
        container.appendChild(btn);
    });
}

function updateKidSubjectChips() {
    const container = document.getElementById('kidSubjectChips');
    if (!container) return;

    const cls = AppState.selectedClass;
    const classGames = GamesCatalog.filter(g => g.class === cls);
    const presentSubjects = Array.from(new Set(classGames.map(g => g.subject).filter(Boolean)));

    const subjectOrder = ['Mathematics', 'English', 'EVS', 'Science', 'Social Science'];
    presentSubjects.sort((a, b) => {
        const idxA = subjectOrder.indexOf(a);
        const idxB = subjectOrder.indexOf(b);
        return (idxA !== -1 ? idxA : 99) - (idxB !== -1 ? idxB : 99);
    });

    if (AppState.selectedSubject !== 'all' && !presentSubjects.includes(AppState.selectedSubject)) {
        AppState.selectedSubject = 'all';
    }

    const subjectMeta = {
        'Mathematics': { label: 'Math', dot: 'chip-dot-math' },
        'English': { label: 'English', dot: 'chip-dot-eng' },
        'EVS': { label: 'EVS', dot: 'chip-dot-evs' },
        'Science': { label: 'Science', dot: 'chip-dot-sci' },
        'Social Science': { label: 'Social', dot: 'chip-dot-soc' }
    };

    container.innerHTML = '';

    const allBtn = document.createElement('button');
    allBtn.type = 'button';
    allBtn.className = `chip-btn ${AppState.selectedSubject === 'all' ? 'active' : ''}`;
    allBtn.textContent = 'All';
    allBtn.onclick = function () { filterBySubject('all', this); };
    container.appendChild(allBtn);

    presentSubjects.forEach(sub => {
        const meta = subjectMeta[sub] || { label: sub, dot: 'chip-dot-math' };
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = `chip-btn ${AppState.selectedSubject === sub ? 'active' : ''}`;
        btn.innerHTML = `<span class="chip-dot ${meta.dot}"></span> ${meta.label}`;
        btn.onclick = function () { filterBySubject(sub, this); };
        container.appendChild(btn);
    });
}

function filterTeacherSubject(sub, btn) {
    AppState.teacherSubjectFilter = sub;
    renderTeacherHub();
}

function filterTeacherActivities(val) {
    AppState.teacherSearchQuery = (val || '').trim();
    renderTeacherHub();
}

function filterTeacherStatus(status, btn) {
    AppState.teacherStatusFilter = status;
    const btnAll = document.getElementById('btnTeacherStatusAll');
    const btnAsg = document.getElementById('btnTeacherStatusAssigned');
    if (btnAll) btnAll.classList.toggle('active', status === 'all');
    if (btnAsg) btnAsg.classList.toggle('active', status === 'assigned');
    renderTeacherHub();
}

function setTeacherLayoutMode(mode, btn) {
    AppState.teacherLayoutMode = mode;
    document.querySelectorAll('.view-mode-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    renderTeacherHub();
}

function resetTeacherFilters() {
    AppState.teacherSubjectFilter = 'all';
    AppState.teacherSearchQuery = '';
    AppState.teacherStatusFilter = 'all';
    const input = document.getElementById('teacherSearchInput');
    if (input) input.value = '';
    const btnAll = document.getElementById('btnTeacherStatusAll');
    const btnAsg = document.getElementById('btnTeacherStatusAssigned');
    if (btnAll) btnAll.classList.add('active');
    if (btnAsg) btnAsg.classList.remove('active');
    renderTeacherHub();
}

/* ====================================================
   ASSIGN MODAL LOGIC (CASCADING CLASS -> SUBJECT -> SKILL -> ACTIVITY)
   ==================================================== */
/* ====================================================
   ASSIGN MODAL LOGIC (ASSIGN BY SKILL AREA)
   ==================================================== */
function openAssignModal() {
    document.getElementById('modalAssignClass').value = AppState.selectedClass;
    updateModalSubjectOptions(AppState.teacherSubjectFilter !== 'all' ? AppState.teacherSubjectFilter : undefined);
    renderAssignStudentsList();
    document.getElementById('teacherAssignModal').classList.add('active');
}

function openAssignModalForSkill(skillName) {
    document.getElementById('modalAssignClass').value = AppState.selectedClass;
    renderAssignStudentsList();

    const cls = AppState.selectedClass;
    const matchingGame = GamesCatalog.find(g => (g.class === cls || !g.class) && g.skillArea === skillName);
    const sub = matchingGame ? matchingGame.subject : (AppState.teacherSubjectFilter !== 'all' ? AppState.teacherSubjectFilter : undefined);

    updateModalSubjectOptions(sub, skillName);
    document.getElementById('teacherAssignModal').classList.add('active');
}

// Backward compatibility fallback
function openAssignModalForGame(gameId) {
    const game = GamesCatalog.find(g => g.id === gameId);
    if (game && game.skillArea) {
        openAssignModalForSkill(game.skillArea);
    } else {
        openAssignModal();
    }
}

function closeAssignModal() {
    document.getElementById('teacherAssignModal').classList.remove('active');
}

function handleModalClassChange(cls) {
    renderAssignStudentsList();
    updateModalSubjectOptions();
}

function updateModalSubjectOptions(preferredSubject, preferredSkill) {
    const cls = document.getElementById('modalAssignClass').value;
    const subSelect = document.getElementById('modalAssignSubject');
    if (!subSelect) return;

    const classGames = GamesCatalog.filter(g => g.class === cls);
    const presentSubjects = Array.from(new Set(classGames.map(g => g.subject).filter(Boolean)));
    const subjectOrder = ['Mathematics', 'English', 'EVS', 'Science', 'Social Science'];
    presentSubjects.sort((a, b) => {
        const idxA = subjectOrder.indexOf(a);
        const idxB = subjectOrder.indexOf(b);
        return (idxA !== -1 ? idxA : 99) - (idxB !== -1 ? idxB : 99);
    });

    const currentVal = preferredSubject !== undefined ? preferredSubject : subSelect.value;

    subSelect.innerHTML = '';
    presentSubjects.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s;
        opt.textContent = s;
        subSelect.appendChild(opt);
    });

    if (currentVal && currentVal !== 'all' && presentSubjects.includes(currentVal)) {
        subSelect.value = currentVal;
    } else if (presentSubjects.length > 0) {
        subSelect.value = presentSubjects[0];
    } else {
        subSelect.value = '';
    }

    updateModalSkillAreaOptions(preferredSkill);
}

function handleModalSubjectChange(sub) {
    updateModalSkillAreaOptions();
}

function handleModalSkillAreaChange(sa) {
    updateModalSkillActivitiesPreview();
}

function updateModalSkillAreaOptions(preferredSkill) {
    const cls = document.getElementById('modalAssignClass').value;
    const sub = document.getElementById('modalAssignSubject').value;
    const saSelect = document.getElementById('modalAssignSkillArea');
    if (!saSelect) return;

    const games = GamesCatalog.filter(g => {
        if (g.class && g.class !== cls) return false;
        if (sub !== 'all' && g.subject !== sub) return false;
        return true;
    });

    const uniqueSkills = Array.from(new Set(games.map(g => g.skillArea).filter(Boolean))).sort();
    saSelect.innerHTML = '';

    if (uniqueSkills.length === 0) {
        saSelect.innerHTML = '<option value="">No skill areas available</option>';
    } else {
        uniqueSkills.forEach(s => {
            const count = games.filter(g => g.skillArea === s).length;
            const opt = document.createElement('option');
            opt.value = s;
            opt.textContent = `🎯 ${s} (${count} ${count === 1 ? 'activity' : 'activities'})`;
            saSelect.appendChild(opt);
        });
    }

    if (preferredSkill && uniqueSkills.includes(preferredSkill)) {
        saSelect.value = preferredSkill;
    } else if (uniqueSkills.length > 0) {
        saSelect.value = uniqueSkills[0];
    }

    updateModalSkillActivitiesPreview();
}

function updateModalSkillActivitiesPreview() {
    const cls = document.getElementById('modalAssignClass').value;
    const sub = document.getElementById('modalAssignSubject').value;
    const saSelect = document.getElementById('modalAssignSkillArea');
    const sa = saSelect ? saSelect.value : '';
    const previewBox = document.getElementById('modalSkillActivitiesPreview');
    const listEl = document.getElementById('modalSkillActivitiesList');
    const countEl = document.getElementById('modalSkillActivityCount');

    if (!sa || !previewBox || !listEl) {
        if (previewBox) previewBox.style.display = 'none';
        return;
    }

    const gamesInSkill = GamesCatalog.filter(g => {
        if (g.class && g.class !== cls) return false;
        if (sub !== 'all' && g.subject !== sub) return false;
        return g.skillArea === sa;
    });

    if (gamesInSkill.length === 0) {
        previewBox.style.display = 'none';
        return;
    }

    previewBox.style.display = 'block';
    if (countEl) countEl.textContent = gamesInSkill.length;

    listEl.innerHTML = gamesInSkill.map((g, idx) => `
                <label class="student-check-row" style="display: flex; align-items: center; justify-content: space-between; gap: 10px;">
                    <div style="display: flex; align-items: center; gap: 10px; min-width: 0; flex: 1;">
                        <input type="checkbox" name="assignActivityCheck" value="${g.id}" checked>
                        <span style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${escapeHtml(g.title)}</span>
                    </div>
                    <button type="button" class="btn-tac-preview-sm" onclick="event.preventDefault(); event.stopPropagation(); previewActivity('${g.id}')" title="Preview activity before assigning" style="flex: none; display: inline-flex; align-items: center; gap: 4px;">
                        <span>👁️</span> Preview
                    </button>
                </label>
            `).join('');
}

function toggleAssignActivitiesSelectAll() {
    const boxes = document.querySelectorAll('input[name="assignActivityCheck"]');
    const anyUnchecked = Array.from(boxes).some(b => !b.checked);
    boxes.forEach(b => b.checked = anyUnchecked);
}

function renderAssignStudentsList() {
    const cls = document.getElementById('modalAssignClass').value;
    const container = document.getElementById('modalAssignStudentsList');
    container.innerHTML = '';

    const roster = StudentRosters[cls] || [];
    roster.forEach(s => {
        const label = document.createElement('label');
        label.className = 'student-check-row';
        label.innerHTML = `
                    <input type="checkbox" name="assignStudentCheck" value="${s.roll}" data-name="${s.name}" checked>
                    <span>${s.name} (Roll #${s.roll})</span>
                `;
        container.appendChild(label);
    });
}

function toggleAssignSelectAll() {
    const boxes = document.querySelectorAll('input[name="assignStudentCheck"]');
    const anyUnchecked = Array.from(boxes).some(b => !b.checked);
    boxes.forEach(b => b.checked = anyUnchecked);
}

function submitModalAssignment() {
    const cls = document.getElementById('modalAssignClass').value;
    const sub = document.getElementById('modalAssignSubject').value;
    const sa = document.getElementById('modalAssignSkillArea').value;

    if (!sa) {
        alert('Please select a skill area.');
        return;
    }

    const checkedActivityBoxes = Array.from(document.querySelectorAll('input[name="assignActivityCheck"]:checked'));
    if (checkedActivityBoxes.length === 0) {
        alert('Please select at least one activity to assign.');
        return;
    }

    const selectedGameIds = new Set(checkedActivityBoxes.map(b => b.value));
    const selectedGames = GamesCatalog.filter(g => selectedGameIds.has(g.id));

    const checkedStudentBoxes = Array.from(document.querySelectorAll('input[name="assignStudentCheck"]:checked'));
    if (checkedStudentBoxes.length === 0) {
        alert('Please select at least one student to assign.');
        return;
    }

    checkedStudentBoxes.forEach(box => {
        const roll = parseInt(box.value, 10);
        const name = box.dataset.name;

        selectedGames.forEach(game => {
            // Avoid duplicate pending assignment
            const exists = AppState.assignments.some(a => a.class === cls && a.gameId === game.id && a.student === name);
            if (!exists) {
                AppState.assignments.push({
                    id: "asg-" + Date.now() + "-" + roll + "-" + Math.random().toString(36).substr(2, 4),
                    class: cls,
                    subject: game.subject || sub,
                    skillArea: game.skillArea || sa,
                    activity: game.activity || '',
                    gameId: game.id,
                    gameTitle: game.title,
                    student: name,
                    roll: roll,
                    status: 'pending'
                });
            }
        });
    });

    saveAssignments();
    closeAssignModal();
    renderTeacherHub();
    renderKidZone();
    if (AppState.currentView === 'split') {
        renderSplitViews();
    }
}

function unassignSkill(skillName, cls) {
    const targetClass = cls || AppState.selectedClass;
    const gamesInSkill = GamesCatalog.filter(g => (g.class === targetClass || !g.class) && g.skillArea === skillName);
    const gameIds = new Set(gamesInSkill.map(g => g.id));
    AppState.assignments = AppState.assignments.filter(a => !(a.class === targetClass && gameIds.has(a.gameId)));
    saveAssignments();
    renderTeacherHub();
    renderKidZone();
    if (AppState.currentView === 'split') {
        renderSplitViews();
    }
}

/* ====================================================
   SPLIT VIEW RENDERING (SYNCHRONIZED TEACHER HUB & STUDENT ZONE)
   ==================================================== */
function toggleSplitTeacherFilter(filter) {
    AppState.splitTeacherFilter = filter;
    renderSplitViews();
}

function renderSplitViews() {
    const tCol = document.getElementById('splitTeacherContent');
    const kCol = document.getElementById('splitKidContent');
    const cls = AppState.selectedClass;
    const roster = StudentRosters[cls] || [];

    const classGames = GamesCatalog.filter(g => g.class === cls);
    const classAsgs = AppState.assignments.filter(a => a.class === cls);
    const assignedGameIds = Array.from(new Set(classAsgs.map(a => a.gameId)));
    const assignedGames = classGames.filter(g => assignedGameIds.includes(g.id));
    const splitFilter = AppState.splitTeacherFilter || 'assigned';

    // Sort: Assigned activities first
    const sortedClassGames = [...classGames].sort((a, b) => {
        const aAssigned = classAsgs.filter(asg => asg.gameId === a.id).length;
        const bAssigned = classAsgs.filter(asg => asg.gameId === b.id).length;
        const aHas = aAssigned > 0 ? 1 : 0;
        const bHas = bAssigned > 0 ? 1 : 0;
        if (bHas !== aHas) return bHas - aHas;
        return bAssigned - aAssigned;
    });

    const gamesToShow = splitFilter === 'assigned' ? assignedGames : sortedClassGames;

    // Populate Teacher Side
    tCol.innerHTML = `
                <div style="margin-bottom: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <div>
                            <h3 style="font-family: var(--font-heading); font-size: 18.5px; font-weight: 700; color: #1e1b4b; margin: 0;">🎓 Class ${cls} Teacher Hub</h3>
                            <div style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">Track completion & assignments</div>
                        </div>
                    </div>

                    <!-- Quick Class Picker in Split View -->
                    <div style="display: flex; gap: 5px; overflow-x: auto; padding-bottom: 6px; margin-bottom: 10px;">
                        ${['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII'].map(c => `
                            <button type="button" class="teacher-class-pill ${c === cls ? 'active' : ''}" style="padding: 4px 10px; font-size: 11.5px;" onclick="handleClassFilterChange('${c}')">Class ${c}</button>
                        `).join('')}
                    </div>

                    <!-- Filter Toggle (Assigned Only vs All) -->
                    <div class="tab-toggles tab-toggles-sm" style="margin-bottom: 12px;">
                        <button type="button" class="tab-btn ${splitFilter === 'assigned' ? 'active' : ''}" onclick="toggleSplitTeacherFilter('assigned')">
                            📖 Assigned Only (${assignedGames.length})
                        </button>
                        <button type="button" class="tab-btn ${splitFilter === 'all' ? 'active' : ''}" onclick="toggleSplitTeacherFilter('all')">
                            All Curriculum (${classGames.length})
                        </button>
                    </div>
                </div>

                <!-- Teacher Activities List -->
                <div style="display: flex; flex-direction: column; gap: 10px;">
                    ${gamesToShow.length === 0 ? `
                        <div style="text-align: center; padding: 36px 16px; background: #ffffff; border: 1.5px dashed #cbd5e1; border-radius: 16px;">
                            <div style="font-size: 32px; margin-bottom: 6px;">📋✨</div>
                            <h4 style="font-family: var(--font-heading); font-size: 16px; color: #1e1b4b; margin-bottom: 4px;">No activities assigned yet for Class ${cls}</h4>
                            <p style="font-size: 12.5px; color: var(--text-muted); margin-bottom: 12px;">Assign activities by skill in Teacher Hub, or switch to 'All Curriculum' above to view all ${classGames.length} activities.</p>
                            <button type="button" class="btn-clear-filters" style="margin: 0 auto;" onclick="toggleSplitTeacherFilter('all')">View All Curriculum</button>
                        </div>
                    ` : gamesToShow.map(g => {
        const assigned = classAsgs.filter(a => a.gameId === g.id);
        const totalAssigned = assigned.length;
        const completed = assigned.filter(a => a.status === 'completed');
        const compCount = completed.length;
        const pct = totalAssigned > 0 ? Math.round((compCount / totalAssigned) * 100) : 0;
        const isAssigned = totalAssigned > 0;

        const isSpecificSubject = AppState.teacherSubjectFilter && AppState.teacherSubjectFilter !== 'all';

        return `
                            <div style="background: #ffffff; border: 1px solid ${isAssigned ? '#818cf8' : '#e2e8f0'}; border-radius: 14px; padding: 12px 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
                                <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; margin-bottom: 6px;">
                                    <div>
                                        <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap; margin-bottom: 4px;">
                                            ${!isSpecificSubject ? `<span class="tac-badge tac-badge-subject ${g.badgeClass || ''}" style="font-size: 10px; padding: 2px 7px;">${g.subject}</span>` : ''}
                                            ${g.isCustom ? '<span class="tac-badge tac-badge-custom" style="font-size: 10px; padding: 2px 7px;">⭐ Custom</span>' : ''}
                                            <span class="tac-badge tac-badge-skill" style="font-size: 10px; padding: 2px 7px;">🎯 ${g.skillArea || 'Skill'}</span>
                                            <h5 style="font-family: var(--font-heading); font-size: 14px; font-weight: 700; color: #0f172a; margin: 0; display: inline;">${g.title}</h5>
                                        </div>
                                    </div>
                                    <div style="display: flex; gap: 4px; align-items: center; flex: none;">
                                        <button type="button" class="btn-tac-preview-sm" style="font-size: 11px; padding: 4px 10px;" onclick="previewActivity('${g.id}')" title="Preview activity before assigning">👁️ Preview</button>
                                    </div>
                                </div>

                                <!-- Progress bar -->
                                <div style="margin: 6px 0; background: #f8fafc; padding: 5px 8px; border-radius: 8px; border: 1px solid #e2e8f0;">
                                    <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 3px;">
                                        <span style="color: #64748b; font-weight: 600;">Completion:</span>
                                        <span style="font-weight: 700; color: ${pct === 100 ? '#15803d' : '#0f172a'};">
                                            ${isAssigned ? `${compCount}/${totalAssigned} (${pct}%)` : 'Not assigned'}
                                        </span>
                                    </div>
                                    <div style="height: 6px; background: #e2e8f0; border-radius: 999px; overflow: hidden;">
                                        <div style="height: 100%; border-radius: 999px; width: ${pct}%; background: ${pct === 100 ? '#10b981' : 'linear-gradient(90deg, #f59e0b, #10b981)'};"></div>
                                    </div>
                                </div>

                                <!-- Student Names & Status -->
                                <div style="display: flex; flex-wrap: wrap; gap: 4px; align-items: center; margin-top: 6px;">
                                    <span style="font-size: 10.5px; color: #64748b; font-weight: 700;">Students:</span>
                                    ${isAssigned
                ? assigned.map(a => `
                                            <span class="tac-chip ${a.status === 'completed' ? 'completed' : 'pending'}" style="font-size: 10px; padding: 2px 7px;">
                                                ${a.status === 'completed' ? `✓ ${a.student}` : `⏳ ${a.student}`}
                                            </span>
                                        `).join('')
                : `<span style="font-size: 11px; color: #94a3b8; font-weight: 500;">—</span>`
            }
                                </div>
                            </div>
                        `;
    }).join('')}
                </div>
            `;

    // Populate Kid Side (Assigned Activities)
    kCol.innerHTML = `
                <div style="margin-bottom: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <div>
                            <h3 style="font-family: var(--font-heading); font-size: 18.5px; font-weight: 700; color: #1e1b4b; margin: 0;">🎒 Class ${cls} Student Zone</h3>
                            <div style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">Assigned quests for your class</div>
                        </div>
                        <span class="tab-counter-badge" style="background: #ede9fe; color: #6d28d9;">${assignedGames.length} active quests</span>
                    </div>
                </div>

                <div style="display: flex; flex-direction: column; gap: 12px;">
                    ${assignedGames.length === 0 ? `
                        <div style="text-align: center; padding: 36px 16px; background: #f8fafc; border: 1.5px dashed #cbd5e1; border-radius: 16px;">
                            <div style="font-size: 36px; margin-bottom: 8px;">🎒✨</div>
                            <h4 style="font-family: var(--font-heading); font-size: 16.5px; color: #1e1b4b; margin-bottom: 4px;">No assigned activities for Class ${cls}</h4>
                            <p style="font-size: 12.5px; color: var(--text-muted); margin-bottom: 6px;">Activities assigned by your teacher in Teacher Hub will appear here!</p>
                        </div>
                    ` : assignedGames.map(game => {
        const assignedSts = classAsgs.filter(a => a.gameId === game.id);
        const isDone = assignedSts.some(a => a.status === 'completed');

        return `
                            <div class="game-card" style="box-shadow: 0 4px 14px rgba(0,0,0,0.05); border-radius: 16px; overflow: hidden;">
                                <div class="game-thumb-wrap" style="height: 110px;">
                                    <img src="${game.thumb}" alt="${game.title}" class="game-thumb-img" onerror="if(!this.src.endsWith('.svg')){this.src='images/thumbnails/${game.id}.svg';}">
                                    <span class="subject-badge-pill ${game.badgeClass}">${game.subject}</span>
                                    ${isDone ? '<span class="game-status-pill"><span>✓</span> Progress Active</span>' : ''}
                                </div>
                                <div class="game-info-body" style="padding: 14px;">
                                    <div class="game-category-tags" style="margin-bottom: 6px;">
                                        <span class="skill-tag-pill" style="font-size: 10px;">🎯 ${game.skillArea}</span>
                                        <span class="activity-tag-pill" style="font-size: 10px;">⚡ ${game.activity}</span>
                                    </div>
                                    <h4 style="font-family: var(--font-heading); font-size: 16px; font-weight: 700; color: #1e1b4b; margin-bottom: 4px;">${game.title}</h4>
                                    <p style="font-size: 12px; color: var(--text-muted); line-height: 1.35; margin-bottom: 8px;">${game.desc}</p>
                                    
                                    <!-- Assigned Students summary -->
                                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 5px 8px; margin-bottom: 10px; font-size: 11px; color: #4338ca; font-weight: 700;">
                                        👥 Assigned: ${assignedSts.map(a => `${a.student}${a.status === 'completed' ? ' (✓)' : ''}`).join(', ')}
                                    </div>

                                    <button type="button" class="btn-play-action" style="padding: 8px 14px; font-size: 13px;" onclick="openWhoIsPlaying('${game.id}')">
                                        <span>▶</span> Play Activity 🚀
                                    </button>
                                </div>
                            </div>
                        `;
    }).join('')}
                </div>
            `;
}


/* ====================================================
   TEACHER CREATE NEW TASK ENGINE
   ==================================================== */
const CUSTOM_TASKS_KEY = 'mcb_custom_tasks_v1';

function loadCustomTasks() {
    try {
        const raw = localStorage.getItem(CUSTOM_TASKS_KEY);
        return raw ? JSON.parse(raw) : [];
    } catch (e) {
        return [];
    }
}

function saveCustomTasks(tasks) {
    try {
        localStorage.setItem(CUSTOM_TASKS_KEY, JSON.stringify(tasks));
    } catch (e) { }
}

function loadCustomTasksIntoCatalog() {
    const saved = loadCustomTasks();
    saved.forEach(task => {
        if (!GamesCatalog.some(g => g.id === task.id)) {
            GamesCatalog.unshift(task);
        }
    });
}

let currentCreateTaskQuestions = [];
let currentAiIdeaOffset = 0;
let currentCreateTaskInteractiveConfig = null;
let currentCreateTaskGameType = 'auto';

function handleGameTypeSelectionChange(val) {
    currentCreateTaskGameType = val;
}

function clearCreatedInteractiveConfig() {
    currentCreateTaskInteractiveConfig = null;
    const previewCard = document.getElementById('aiBuiltGamePreviewCard');
    if (previewCard) previewCard.style.display = 'none';
    const gtSelect = document.getElementById('newTaskGameType');
    if (gtSelect) gtSelect.value = 'mcq';
    currentCreateTaskGameType = 'MCQ Quiz';
    showToastNotification("Interactive game removed. Reverted to standard quiz.");
}

function testPlayCreatedGame() {
    const title = document.getElementById('newTaskTitle')?.value?.trim() || 'Interactive Mini-Game Preview';
    const cls = document.getElementById('newTaskClass')?.value || AppState.selectedClass || 'IV';
    const subject = document.getElementById('newTaskSubject')?.value || 'Science';
    const skill = document.getElementById('newTaskSkillArea')?.value?.trim() || 'Curriculum Skill';

    if (!currentCreateTaskInteractiveConfig) {
        showToastNotification("No interactive game config found to test play.");
        return;
    }

    const tempGame = {
        id: 'PREVIEW-' + Date.now(),
        title: title,
        class: cls,
        subject: subject,
        skillArea: skill,
        gameType: currentCreateTaskGameType || 'Sort & Group',
        interactiveConfig: currentCreateTaskInteractiveConfig,
        questions: (currentCreateTaskQuestions && currentCreateTaskQuestions.length > 0)
            ? currentCreateTaskQuestions
            : [{
                prompt: `Review what you learned in ${title}!`,
                options: ['Core Concepts', 'Incorrect Distractor', 'Unrelated Fact', 'Random Noise'],
                answer: 0,
                explanation: `Review challenge for ${title}.`
            }]
    };

    AppState.activeMissionGame = tempGame;
    AppState.selectedStudent = { name: "Teacher Preview Mode", roll: 0 };
    launchQuestRunner();
}

// ============================================================
// CLASS & SUBJECT DYNAMIC CURRICULUM IDEAS MAP
// ============================================================
const CurriculumIdeasMap = {
    "I": {
        "Mathematics": [
            { icon: "🔢", title: "Counting 1-20", prompt: "Counting real objects, forward and backward numbers up to 20", skill: "Counting & Number Sense", time: "3 min" },
            { icon: "➕", title: "Simple Addition", prompt: "Adding numbers up to 10 with pictures and counters", skill: "Addition within 10", time: "3 min" },
            { icon: "➖", title: "Take Away (Subtract)", prompt: "Subtracting numbers within 10 with visual objects", skill: "Basic Subtraction", time: "3 min" },
            { icon: "🔺", title: "Basic 2D Shapes", prompt: "Identifying circles, squares, triangles, and rectangles", skill: "Shapes & Space", time: "5 min" },
            { icon: "📏", title: "Longer & Shorter", prompt: "Comparing objects: longer vs shorter, heavier vs lighter", skill: "Measurement & Comparison", time: "3 min" },
            { icon: "🎯", title: "Fun Patterns", prompt: "Repeating visual color, animal, and shape sequences", skill: "Patterns & Sequences", time: "3 min" }
        ],
        "English": [
            { icon: "🔤", title: "Phonics & Sounds", prompt: "Beginning letter sounds, vowels (a, e, i, o, u) and consonants", skill: "Phonics & Sounds", time: "3 min" },
            { icon: "🐱", title: "Rhyming Words", prompt: "Simple 3-letter rhyming words like cat-hat, dog-log, sun-run", skill: "Rhyming Words", time: "3 min" },
            { icon: "🧸", title: "Naming Words (Nouns)", prompt: "Names of people, animals, everyday objects, and places", skill: "Naming Words / Nouns", time: "5 min" },
            { icon: "📖", title: "Sight Words", prompt: "High frequency early reading words: the, is, a, we, can, you", skill: "Sight Words", time: "3 min" },
            { icon: "↔️", title: "Opposite Words", prompt: "Simple opposites: big-small, hot-cold, up-down, happy-sad", skill: "Opposites / Antonyms", time: "3 min" }
        ],
        "EVS": [
            { icon: "🏡", title: "My Family & Home", prompt: "Family members, rooms in the house, and helping parents", skill: "Family & Home", time: "3 min" },
            { icon: "👀", title: "5 Senses", prompt: "Eyes see, ears hear, nose smells, tongue tastes, skin feels", skill: "Sense Organs", time: "5 min" },
            { icon: "🐾", title: "Animals & Sounds", prompt: "Farm animals, pets, and the sounds they make", skill: "Animal World", time: "3 min" },
            { icon: "🧼", title: "Clean Habits", prompt: "Handwashing, brushing teeth, and clean living habits", skill: "Health & Hygiene", time: "3 min" },
            { icon: "🍎", title: "Healthy Food", prompt: "Fruits, vegetables, drinking water, and avoiding junk food", skill: "Food & Health", time: "3 min" }
        ],
        "Science": [
            { icon: "☀️", title: "Day and Night", prompt: "The Sun in daytime, Moon and stars at night, daily routines", skill: "Day & Night Sky", time: "3 min" },
            { icon: "🌱", title: "Plants Around Us", prompt: "Leaves, flowers, trees, grass, and watering plants", skill: "Plants & Trees", time: "3 min" },
            { icon: "🌧️", title: "Weather & Rain", prompt: "Sunny, rainy, and windy days, using umbrellas and raincoats", skill: "Weather & Seasons", time: "3 min" },
            { icon: "🐶", title: "Living & Non-Living", prompt: "Living things grow and breathe; non-living things (toys, rocks)", skill: "Living vs Non-Living", time: "5 min" }
        ],
        "Social Science": [
            { icon: "🤝", title: "Good Manners", prompt: "Saying please, thank you, sorry, sharing toys and helping friends", skill: "Values & Manners", time: "3 min" },
            { icon: "🏫", title: "My School", prompt: "Classroom objects, school rules, and playground games", skill: "School & Community", time: "3 min" },
            { icon: "👮", title: "Community Helpers", prompt: "Doctors, teachers, police, firefighters, and postmen", skill: "Our Helpers", time: "5 min" }
        ]
    },
    "II": {
        "Mathematics": [
            { icon: "🔢", title: "2-Digit Place Value", prompt: "Tens and ones up to 99, expanded form and comparing numbers", skill: "Place Value & Numbers", time: "5 min" },
            { icon: "➕", title: "Addition with Carry", prompt: "2-digit addition with carry over and real-life shopping puzzles", skill: "2-Digit Addition", time: "5 min" },
            { icon: "➖", title: "Subtraction with Borrow", prompt: "2-digit subtraction with regrouping and word problems", skill: "2-Digit Subtraction", time: "5 min" },
            { icon: "🥤", title: "Capacity & Jugs", prompt: "Measuring liquids in litres (L) and millilitres (mL), pouring into jugs", skill: "Capacity & Litres", time: "5 min" },
            { icon: "⏰", title: "Telling the Clock", prompt: "Reading analog clock hours and half hours (o'clock, half past)", skill: "Time & Clock", time: "5 min" },
            { icon: "💰", title: "Coins & Currency", prompt: "Indian rupee notes and coins, making amounts to buy pencils and toys", skill: "Money & Currency", time: "5 min" }
        ],
        "English": [
            { icon: "🔤", title: "Singular & Plural", prompt: "One and many: adding -s, -es, and irregular plurals", skill: "Plurals & Nouns", time: "5 min" },
            { icon: "🏃", title: "Action Verbs", prompt: "Doing words: jump, swim, write, and play in sentences", skill: "Action Verbs", time: "5 min" },
            { icon: "🎨", title: "Describing Words", prompt: "Adjectives describing colors, sizes, shapes, and feelings", skill: "Describing Adjectives", time: "5 min" },
            { icon: "❓", title: "Sentence Punctuation", prompt: "Capital letters, full stops, and question marks", skill: "Punctuation", time: "5 min" }
        ],
        "EVS": [
            { icon: "🏠", title: "Types of Houses", prompt: "Kutcha houses, pucca houses, flats, stilt houses, and igloos", skill: "Shelter & Houses", time: "5 min" },
            { icon: "🚦", title: "Traffic & Road Safety", prompt: "Traffic lights (red, yellow, green), zebra crossings, walking safely", skill: "Safety & Traffic Rules", time: "5 min" },
            { icon: "🌦️", title: "Four Seasons", prompt: "Summer, Monsoon, Winter, Spring clothes, weather, and foods", skill: "Seasons & Weather", time: "5 min" },
            { icon: "💧", title: "Water and Its Uses", prompt: "Drinking, cooking, washing, saving water, and avoiding wastage", skill: "Water Conservation", time: "5 min" }
        ],
        "Science": [
            { icon: "🐾", title: "Animal Habitats", prompt: "Land, water, and desert animals: their homes, food, and young ones", skill: "Animal Habitats", time: "5 min" },
            { icon: "🌿", title: "Plant Uses", prompt: "Medicines, fruits, wood, cotton, and oxygen from plants", skill: "Uses of Plants", time: "5 min" },
            { icon: "💨", title: "Air & Wind", prompt: "Air occupies space, moving air is wind, pinwheels and kites", skill: "Air & Atmosphere", time: "5 min" }
        ],
        "Social Science": [
            { icon: "🎉", title: "Indian Festivals", prompt: "Diwali, Eid, Christmas, Holi, Gurpurab and national festivals", skill: "Culture & Festivals", time: "5 min" },
            { icon: "🇮🇳", title: "National Symbols", prompt: "Tiranga flag, tiger, peacock, lotus, and national anthem", skill: "National Symbols", time: "5 min" }
        ]
    },
    "III": {
        "Mathematics": [
            { icon: "🔢", title: "3-Digit Numbers", prompt: "Hundreds, tens, and units up to 999, number names and rounding", skill: "3-Digit Place Value", time: "5 min" },
            { icon: "✖️", title: "Multiplication Tables", prompt: "Times tables 2 to 9, repeated addition, and array word problems", skill: "Multiplication Facts", time: "5 min" },
            { icon: "➗", title: "Equal Sharing (Division)", prompt: "Dividing objects into equal groups, sharing marbles and sweets", skill: "Division Basics", time: "5 min" },
            { icon: "🍰", title: "Fractions Intro", prompt: "Halves (1/2), thirds (1/3), and quarters (1/4) of shapes", skill: "Fractions Basics", time: "5 min" },
            { icon: "⚖️", title: "Kilograms & Grams", prompt: "Converting kg to g, weighing groceries and balancing scales", skill: "Mass & Weight", time: "5 min" }
        ],
        "English": [
            { icon: "👤", title: "Pronouns", prompt: "Replacing repetitive nouns with he, she, it, they, we", skill: "Pronouns", time: "5 min" },
            { icon: "📍", title: "Prepositions of Place", prompt: "Position words: in, on, under, behind, in front of, between", skill: "Prepositions", time: "5 min" },
            { icon: "⚡", title: "Past Tense Verbs", prompt: "Regular past tense verbs (-ed) and irregular verbs (went, saw)", skill: "Past Tense", time: "5 min" },
            { icon: "💬", title: "Compound Words", prompt: "Joining words: rainbow, butterfly, jellyfish, sunflower", skill: "Word Building", time: "5 min" }
        ],
        "EVS": [
            { icon: "🌿", title: "Plant Parts & Leaves", prompt: "Roots, stem, leaves, flowers, leaf venation, photosynthesis", skill: "Plant Anatomy", time: "5 min" },
            { icon: "🐦", title: "Birds & Their Beaks", prompt: "Different types of beaks, claws, feathers, and nest building", skill: "Birds & Adaptations", time: "5 min" },
            { icon: "🚚", title: "Means of Transport", prompt: "Land, water, air travel, fuel used, and ancient vs modern vehicles", skill: "Transport & Travel", time: "5 min" },
            { icon: "💧", title: "Water Sources & Rain", prompt: "Rivers, wells, rainwater harvesting, filtration, and boiling", skill: "Water Resources", time: "5 min" }
        ],
        "Science": [
            { icon: "🫀", title: "Human Organ Systems", prompt: "Heart, lungs, stomach, brain, and how they keep us healthy", skill: "Human Organs", time: "5 min" },
            { icon: "🪨", title: "Solids, Liquids, Gases", prompt: "Three states of matter: ice, liquid water, steam properties", skill: "States of Matter", time: "5 min" },
            { icon: "🧲", title: "Fun with Magnets", prompt: "Attracting iron nails, North and South poles, magnetic toys", skill: "Magnetism Basics", time: "5 min" }
        ],
        "Social Science": [
            { icon: "🗺️", title: "Directions & Compass", prompt: "North, South, East, West, Sunrise direction, and map reading", skill: "Maps & Directions", time: "5 min" },
            { icon: "🏛️", title: "Our Heritage Monuments", prompt: "Taj Mahal, Red Fort, Qutub Minar, India Gate, and ancient temples", skill: "Indian Heritage", time: "5 min" }
        ]
    },
    "IV": {
        "Mathematics": [
            { icon: "🍕", title: "Fractions & Decimals", prompt: "Equivalent fractions, comparing fractions, and tenths/hundredths", skill: "Fractions & Decimals", time: "5 min" },
            { icon: "✖️", title: "Multi-Digit Multiplication", prompt: "Multiplying 2-digit by 2-digit numbers, mental math shortcuts", skill: "Multiplication Operations", time: "5 min" },
            { icon: "📐", title: "Perimeter & Area", prompt: "Measuring perimeter and area of rectangles and squares using grids", skill: "Perimeter & Area", time: "5 min" },
            { icon: "⏰", title: "Elapsed Time & 24h Clock", prompt: "Calculating start and end times, converting 12h to 24h railway time", skill: "Time Calculations", time: "5 min" },
            { icon: "📊", title: "Bar Charts & Pictographs", prompt: "Reading and drawing bar charts, interpreting tally marks and tables", skill: "Data & Graphing", time: "5 min" }
        ],
        "Science": [
            { icon: "⚡", title: "Electricity & Circuits", prompt: "Simple circuits, batteries, bulbs, switches, conductors and insulators", skill: "Electric Circuits", time: "5 min" },
            { icon: "🪐", title: "The Solar System", prompt: "8 planets in order, revolution, rotation, day/night, and Moon phases", skill: "Solar System & Space", time: "5 min" },
            { icon: "🧲", title: "Magnets & Poles", prompt: "Attraction, repulsion, magnetic field, and making an electromagnet", skill: "Magnetism", time: "5 min" },
            { icon: "💧", title: "The Water Cycle", prompt: "Evaporation, condensation, cloud formation, precipitation, and rain", skill: "Water Cycle & Weather", time: "5 min" },
            { icon: "🦷", title: "Teeth & Digestion", prompt: "Types of teeth (incisors, molars), plaque, and digestive organs", skill: "Human Digestion", time: "5 min" }
        ],
        "EVS": [
            { icon: "⚡", title: "Electricity at Home", prompt: "Safe use of electrical appliances, switches, and saving power", skill: "Energy in Daily Life", time: "5 min" },
            { icon: "💧", title: "Water Cycle & Clouds", prompt: "Evaporation, condensation, rain, and clean drinking water", skill: "Water Cycle", time: "5 min" },
            { icon: "🌳", title: "Forests & Wildlife", prompt: "Endangered animals, national parks, tiger conservation", skill: "Ecology & Wildlife", time: "5 min" },
            { icon: "🗑️", title: "Waste Management (3Rs)", prompt: "Reduce, Reuse, Recycle, biodegradable vs plastic waste", skill: "Environmental Care", time: "5 min" },
            { icon: "🌾", title: "From Seed to Plate", prompt: "Farming stages: ploughing, sowing, harvesting, and markets", skill: "Agriculture & Food", time: "5 min" }
        ],
        "English": [
            { icon: "🔤", title: "Adverbs of Manner (-ly)", prompt: "Identifying and using adverbs: swiftly, gracefully, loudly, carefully", skill: "Adverbs & Grammar", time: "5 min" },
            { icon: "🔗", title: "Conjunctions (Connectors)", prompt: "Joining sentences with and, but, because, although, or, so", skill: "Conjunctions", time: "5 min" },
            { icon: "📖", title: "Reading Comprehension", prompt: "Short passage inference, main idea, vocabulary in context, moral", skill: "Reading Comprehension", time: "10 min" },
            { icon: "🗣️", title: "Direct Speech & Quotes", prompt: "Using quotation marks, speaker dialogue, and punctuation", skill: "Punctuation & Dialogue", time: "5 min" }
        ],
        "Social Science": [
            { icon: "🗺️", title: "Physical Features of India", prompt: "Himalayas, Northern Plains, Thar Desert, Deccan Plateau, Coastal Plains", skill: "Geography of India", time: "5 min" },
            { icon: "🏛️", title: "Civic Life & Panchayat", prompt: "Gram Panchayat, Municipal Corporation, public services, and taxes", skill: "Civics & Governance", time: "5 min" }
        ]
    },
    "V": {
        "Mathematics": [
            { icon: "🔢", title: "Factors, Multiples & LCM/HCF", prompt: "Prime and composite numbers, divisibility tests, finding HCF and LCM", skill: "Factors & Multiples", time: "5 min" },
            { icon: "➗", title: "Decimals Operations", prompt: "Addition, subtraction, multiplication of decimals with money word problems", skill: "Decimals Operations", time: "5 min" },
            { icon: "📐", title: "Area & Volume of Shapes", prompt: "Area of rectangles and triangles, volume of cuboids in cubic cm", skill: "Area & Volume Mensuration", time: "10 min" },
            { icon: "📈", title: "Percentages & Fractions", prompt: "Converting fractions to percentages, discount and score percentage calculation", skill: "Percentages", time: "5 min" },
            { icon: "🧭", title: "Angles & Degrees", prompt: "Acute, right, obtuse, straight angles, measuring angles with protractor", skill: "Geometry & Angles", time: "5 min" }
        ],
        "Science": [
            { icon: "🌿", title: "Photosynthesis & Nutrition", prompt: "Chlorophyll, stomata, xylem, phloem, sunlight, and starch production", skill: "Plant Biology", time: "5 min" },
            { icon: "🦴", title: "Skeletal & Nervous System", prompt: "206 bones, ball-and-socket joint, spinal cord, sensory and motor nerves", skill: "Human Anatomy", time: "5 min" },
            { icon: "🦠", title: "Microbes & Food Preservation", prompt: "Bacteria, fungi, viruses, pasteurization, salting, canning, and pickling", skill: "Microbiology & Food", time: "5 min" },
            { icon: "🌪️", title: "Natural Disasters & Safety", prompt: "Earthquakes (Richter scale), tsunamis, cyclones, and disaster safety measures", skill: "Earth Science & Safety", time: "5 min" },
            { icon: "⚙️", title: "Simple Machines", prompt: "Six simple machines: lever (1st, 2nd, 3rd class), pulley, inclined plane", skill: "Physics & Mechanics", time: "5 min" }
        ],
        "English": [
            { icon: "✨", title: "Continuous & Perfect Tenses", prompt: "Present perfect (has/have seen) and past continuous (was running)", skill: "Advanced Verb Tenses", time: "5 min" },
            { icon: "🤝", title: "Subject-Verb Agreement", prompt: "Rules of singular/plural subject-verb pairing with tricky pronouns", skill: "Grammar & Syntax", time: "5 min" },
            { icon: "🎭", title: "Active & Passive Voice", prompt: "Converting active sentences to passive voice and identifying the agent", skill: "Active & Passive Voice", time: "5 min" },
            { icon: "📚", title: "Idioms & Metaphors", prompt: "Common idioms like 'piece of cake', 'break the ice', and similes/metaphors", skill: "Idioms & Figurative Language", time: "5 min" }
        ],
        "Social Science": [
            { icon: "🌍", title: "Continents & Latitudes", prompt: "7 continents, Equator, Prime Meridian, Tropics of Cancer and Capricorn", skill: "World Geography", time: "5 min" },
            { icon: "📜", title: "India's Freedom Movement", prompt: "Revolt of 1857, Non-Cooperation Movement, Dandi March, Independence 1947", skill: "Modern Indian History", time: "10 min" },
            { icon: "🗳️", title: "The United Nations", prompt: "UN aims, General Assembly, Security Council, UNESCO, UNICEF, and WHO", skill: "Global Organizations", time: "5 min" }
        ],
        "EVS": [
            { icon: "🔋", title: "Renewable Energy", prompt: "Solar panels, windmills, hydroelectric dams, and conserving fossil fuels", skill: "Clean Energy", time: "5 min" },
            { icon: "🌾", title: "Soil Layers & Conservation", prompt: "Topsoil, humus, subsoil, soil erosion, and terrace farming", skill: "Soil Science", time: "5 min" }
        ]
    },
    "VI": {
        "Mathematics": [
            { icon: "➕", title: "Integers & Number Line", prompt: "Negative integers, absolute values, adding and subtracting on number line", skill: "Integers", time: "5 min" },
            { icon: "🔣", title: "Intro to Algebra", prompt: "Variables, algebraic expressions, forming equations from word puzzles", skill: "Introductory Algebra", time: "5 min" },
            { icon: "⚖️", title: "Ratio & Proportions", prompt: "Simplifying ratios, checking proportion, unitary method in shopping", skill: "Ratio & Proportions", time: "5 min" },
            { icon: "📐", title: "Practical Geometry", prompt: "Drawing circles, line bisectors, perpendiculars, and angles with compass", skill: "Geometry & Constructions", time: "10 min" }
        ],
        "Science": [
            { icon: "🥗", title: "Nutrients & Deficiency Diseases", prompt: "Vitamins A, B, C, D, iron, iodine deficiencies (scurvy, rickets, goitre)", skill: "Food & Nutrition", time: "5 min" },
            { icon: "💡", title: "Light, Shadows & Reflections", prompt: "Pinhole camera, rectilinear propagation, transparent, translucent, opaque", skill: "Optics & Light", time: "5 min" },
            { icon: "🔌", title: "Electricity & Circuit Switches", prompt: "Components of electric cell, filament, open vs closed circuits, safety", skill: "Current Electricity", time: "5 min" },
            { icon: "🌱", title: "Plant Structure & Transpiration", prompt: "Taproots, fibrous roots, leaf venation, stomata and transpiration experiment", skill: "Botany & Plant Physiology", time: "5 min" }
        ],
        "English": [
            { icon: "📝", title: "Clauses & Complex Sentences", prompt: "Main clause, subordinate clause, relative pronouns (who, which, that)", skill: "Complex Sentence Structure", time: "5 min" },
            { icon: "💬", title: "Modal Auxiliaries", prompt: "Expressing permission, obligation, possibility (must, ought to, should, might)", skill: "Modal Verbs", time: "5 min" },
            { icon: "📖", title: "Critical Reading & Tone", prompt: "Identifying author perspective, factual vs opinion statements, summaries", skill: "Analytical Reading", time: "10 min" }
        ],
        "Social Science": [
            { icon: "🏛️", title: "Indus Valley Civilization", prompt: "Harappa, Mohenjo-Daro, Great Bath, town planning, granaries, and seals", skill: "Ancient History", time: "10 min" },
            { icon: "🗳️", title: "Democratic Government", prompt: "Universal adult franchise, equality, justice, resolving conflicts peacefully", skill: "Civics & Governance", time: "5 min" },
            { icon: "🪐", title: "Earth in the Solar System", prompt: "Asteroids, meteoroids, Earth's unique atmosphere, and Moon's surface", skill: "Physical Geography", time: "5 min" }
        ]
    },
    "VII": {
        "Mathematics": [
            { icon: "🔢", title: "Rational Numbers & Operations", prompt: "Arithmetic operations with positive and negative rational numbers", skill: "Rational Numbers", time: "10 min" },
            { icon: "📐", title: "Triangles & Pythagoras", prompt: "Angle sum property, exterior angle property, hypotenuse calculations", skill: "Triangles & Geometry", time: "10 min" },
            { icon: "⚡", title: "Exponents & Powers", prompt: "Laws of exponents: multiplying, dividing powers, standard scientific notation", skill: "Exponents & Algebra", time: "5 min" },
            { icon: "📊", title: "Mean, Median & Mode", prompt: "Calculating arithmetic mean, median, mode, and probability of outcomes", skill: "Statistics & Probability", time: "5 min" }
        ],
        "Science": [
            { icon: "🧪", title: "Acids, Bases & Salts", prompt: "Litmus, turmeric indicator, phenolphthalein, acid-base neutralisation salts", skill: "Chemistry: Acids & Bases", time: "5 min" },
            { icon: "🌡️", title: "Heat: Conduction & Convection", prompt: "Conduction in metals, convection currents in water/air, radiation from Sun", skill: "Thermal Physics", time: "5 min" },
            { icon: "⚡", title: "Electric Current & Magnets", prompt: "Electromagnets, electric bell mechanism, fuse wire safety and heating effect", skill: "Electromagnetism", time: "5 min" },
            { icon: "🫁", title: "Respiration in Organisms", prompt: "Aerobic vs anaerobic, human respiratory tract, breathing rate, diaphragm", skill: "Human Physiology", time: "5 min" }
        ],
        "English": [
            { icon: "🔄", title: "Reported Speech Mastery", prompt: "Direct to indirect speech rules for statements, questions, and commands", skill: "Indirect Speech", time: "5 min" },
            { icon: "✍️", title: "Formal Letters & Notices", prompt: "Format of letters to the editor/principal, notice writing with date and venue", skill: "Formal Writing", time: "10 min" }
        ],
        "Social Science": [
            { icon: "🏰", title: "The Mughal Empire", prompt: "Babur, Akbar's Din-i-Ilahi, Mansabdari system, architecture, and decline", skill: "Medieval Indian History", time: "10 min" },
            { icon: "🌍", title: "Atmosphere & Weather Systems", prompt: "Troposphere, stratosphere, air pressure belts, planetary winds, humidity", skill: "Atmospheric Geography", time: "5 min" }
        ]
    },
    "VIII": {
        "Mathematics": [
            { icon: "📐", title: "Linear Equations in 1 Variable", prompt: "Solving algebraic linear equations, cross-multiplication, and word problems", skill: "Linear Equations", time: "10 min" },
            { icon: "⬛", title: "Squares & Square Roots", prompt: "Finding square roots by prime factorisation and long division method", skill: "Squares & Square Roots", time: "10 min" },
            { icon: "📈", title: "Compound Interest & Profit/Loss", prompt: "Compounded annually vs half-yearly, calculating sales tax, GST, and profit %", skill: "Commercial Mathematics", time: "10 min" },
            { icon: "📦", title: "Mensuration: Cylinders & Prisms", prompt: "Total surface area, curved surface area, and volume of cylinders and cuboids", skill: "Mensuration 3D", time: "10 min" }
        ],
        "Science": [
            { icon: "⚡", title: "Force, Pressure & Friction", prompt: "Types of friction, atmospheric pressure, Pascal's principle, fluid resistance", skill: "Mechanics & Pressure", time: "5 min" },
            { icon: "🧬", title: "Cell Structure & Organelles", prompt: "Plant vs animal cell, cell wall, nucleus, mitochondria, chloroplasts", skill: "Cell Biology", time: "5 min" },
            { icon: "🦠", title: "Microorganisms: Friend & Foe", prompt: "Antibiotics, vaccines, nitrogen cycle, food poisoning, and fermentation", skill: "Microbiology", time: "5 min" },
            { icon: "🔥", title: "Combustion, Flame & Fuels", prompt: "Calorific value, zones of a candle flame, spontaneous and rapid combustion", skill: "Chemical Combustion", time: "5 min" },
            { icon: "🔭", title: "Stars, Constellations & Space", prompt: "Ursa Major, Orion, pole star, light years, artificial satellites and orbits", skill: "Astronomy & Space", time: "5 min" }
        ],
        "English": [
            { icon: "📚", title: "Conditional Clauses & Conjunctions", prompt: "First, second, third conditionals (If/Unless), complex coherence", skill: "Advanced Syntax", time: "5 min" },
            { icon: "✍️", title: "Argumentative Essays", prompt: "Writing structured argumentative essays with counter-arguments and evidence", skill: "Essay Writing", time: "10 min" }
        ],
        "Social Science": [
            { icon: "📜", title: "The Indian Constitution & Rights", prompt: "Fundamental Rights, Directive Principles, secularism, rule of law, judiciary", skill: "Civics & Constitution", time: "10 min" },
            { icon: "🌾", title: "Natural Resources & Agriculture", prompt: "Commercial farming, plantation agriculture, major food crops (rice, wheat), soil conservation", skill: "Economic Geography", time: "10 min" }
        ]
    }
};

function applyCurriculumIdea(idea) {
    if (!idea) return;

    // 1. Populate AI Prompt
    const promptEl = document.getElementById('aiTaskPrompt');
    if (promptEl) {
        promptEl.value = `${idea.title}: ${idea.prompt}`;
    }

    // 2. Populate Task Details above
    const titleEl = document.getElementById('newTaskTitle');
    if (titleEl) {
        titleEl.value = `${idea.icon || '🎯'} ${idea.title}`;
    }

    const skillEl = document.getElementById('newTaskSkillArea');
    if (skillEl && idea.skill) {
        skillEl.value = idea.skill;
    }

    if (idea.time) {
        const timeSelect = document.getElementById('newTaskTime');
        if (timeSelect) {
            for (let i = 0; i < timeSelect.options.length; i++) {
                if (timeSelect.options[i].value === idea.time) {
                    timeSelect.selectedIndex = i;
                    break;
                }
            }
        }
    }

    const descEl = document.getElementById('newTaskDesc');
    if (descEl && !descEl.value.trim()) {
        descEl.value = `Master ${idea.title} by reading carefully and solving all interactive challenges!`;
    }

    // 3. Highlight the active idea button
    const allBtns = document.querySelectorAll('.ai-tag-btn[data-idea-title]');
    allBtns.forEach(b => {
        if (b.dataset.ideaTitle === idea.title) {
            b.classList.add('active');
        } else {
            b.classList.remove('active');
        }
    });

    const statusEl = document.getElementById('aiGenerationStatus');
    if (statusEl) statusEl.style.display = 'none';

    showToastNotification(`💡 Loaded idea: "${idea.title}". Click "Generate with AI" below!`);
}

function updateAiIdeaTags(resetOffset = false) {
    if (resetOffset) currentAiIdeaOffset = 0;

    const cls = document.getElementById('newTaskClass')?.value || AppState.selectedClass || 'IV';
    const sub = document.getElementById('newTaskSubject')?.value || 'Science';
    const labelEl = document.getElementById('aiIdeasTagLabel');
    const container = document.getElementById('aiDynamicIdeaButtons');
    if (!container) return;

    if (labelEl) {
        labelEl.innerHTML = `💡 Ideas for <strong>Class ${escapeHtml(cls)} (${escapeHtml(sub)})</strong>:`;
    }

    const classMap = CurriculumIdeasMap[cls] || CurriculumIdeasMap['IV'];
    let subjectIdeas = classMap[sub] || [];

    // If selected subject has no direct list (e.g. EVS in Class VII), fall back intelligently
    if (subjectIdeas.length === 0) {
        if (sub === 'EVS' && classMap['Science']) {
            subjectIdeas = classMap['Science'];
        } else if (sub === 'Science' && classMap['EVS']) {
            subjectIdeas = classMap['EVS'];
        } else {
            subjectIdeas = Object.values(classMap).flat();
        }
    }

    if (subjectIdeas.length === 0) {
        container.innerHTML = '<span style="font-size:12px; color:#64748b;">No preset ideas found. Type a prompt above!</span>';
        return;
    }

    const pageSize = 5;
    const startIdx = (currentAiIdeaOffset * pageSize) % subjectIdeas.length;
    const visibleIdeas = [];
    for (let i = 0; i < pageSize && i < subjectIdeas.length; i++) {
        visibleIdeas.push(subjectIdeas[(startIdx + i) % subjectIdeas.length]);
    }

    container.innerHTML = '';
    visibleIdeas.forEach(idea => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'ai-tag-btn';
        btn.dataset.ideaTitle = idea.title;
        btn.innerHTML = `${idea.icon || '💡'} ${escapeHtml(idea.title)}`;
        btn.title = `${idea.title} - ${idea.prompt}`;
        btn.onclick = () => applyCurriculumIdea(idea);
        container.appendChild(btn);
    });
}

function shuffleAiIdeas() {
    currentAiIdeaOffset++;
    updateAiIdeaTags(false);
}

function filterAiIdeaTags(searchVal) {
    const cls = document.getElementById('newTaskClass')?.value || AppState.selectedClass || 'IV';
    const sub = document.getElementById('newTaskSubject')?.value || 'Science';
    const container = document.getElementById('aiDynamicIdeaButtons');
    if (!container) return;

    const q = (searchVal || '').toLowerCase().trim();
    const classMap = CurriculumIdeasMap[cls] || CurriculumIdeasMap['IV'];
    const allClassIdeas = Object.values(classMap).flat();

    const matches = allClassIdeas.filter(idea =>
        idea.title.toLowerCase().includes(q) ||
        idea.prompt.toLowerCase().includes(q) ||
        (idea.skill && idea.skill.toLowerCase().includes(q))
    );

    if (matches.length === 0) {
        updateAiIdeaTags(false);
        return;
    }

    container.innerHTML = '';
    matches.slice(0, 6).forEach(idea => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'ai-tag-btn';
        btn.dataset.ideaTitle = idea.title;
        btn.innerHTML = `${idea.icon || '💡'} ${escapeHtml(idea.title)}`;
        btn.title = `${idea.title} - ${idea.prompt}`;
        btn.onclick = () => applyCurriculumIdea(idea);
        container.appendChild(btn);
    });
}

function syncCurriculumDefaultsForClass(cls, preferredSubject = null) {
    const classMap = CurriculumIdeasMap[cls] || CurriculumIdeasMap['IV'];
    const subSelect = document.getElementById('newTaskSubject');

    let currentSub = preferredSubject || (subSelect ? subSelect.value : 'Mathematics');

    // Adjust subject for primary vs upper grades
    if ((cls === 'I' || cls === 'II') && (currentSub === 'Science' || currentSub === 'Social Science')) {
        currentSub = 'EVS';
    } else if ((cls === 'VI' || cls === 'VII' || cls === 'VIII') && currentSub === 'EVS') {
        currentSub = 'Science';
    }

    if (subSelect) {
        for (let i = 0; i < subSelect.options.length; i++) {
            if (subSelect.options[i].value.toLowerCase() === currentSub.toLowerCase()) {
                subSelect.selectedIndex = i;
                break;
            }
        }
    }

    // Get the ideas for this class and subject
    let subjectIdeas = classMap[currentSub] || [];
    if (subjectIdeas.length === 0) {
        if (currentSub === 'EVS' && classMap['Science']) subjectIdeas = classMap['Science'];
        else if (currentSub === 'Science' && classMap['EVS']) subjectIdeas = classMap['EVS'];
        else subjectIdeas = Object.values(classMap).flat();
    }

    const defaultIdea = subjectIdeas[0];
    if (defaultIdea) {
        // 1. Task Title based upon the class & subject
        const titleEl = document.getElementById('newTaskTitle');
        if (titleEl) {
            titleEl.value = `${defaultIdea.icon || '🎯'} ${defaultIdea.title}`;
        }

        // 2. Skill Area / Topic based upon the class & subject
        const skillEl = document.getElementById('newTaskSkillArea');
        if (skillEl) {
            skillEl.value = defaultIdea.skill || defaultIdea.title;
        }

        // 3. Estimated Time
        if (defaultIdea.time) {
            const timeSelect = document.getElementById('newTaskTime');
            if (timeSelect) {
                for (let i = 0; i < timeSelect.options.length; i++) {
                    if (timeSelect.options[i].value === defaultIdea.time) {
                        timeSelect.selectedIndex = i;
                        break;
                    }
                }
            }
        }

        // 4. Instructions
        const descEl = document.getElementById('newTaskDesc');
        if (descEl) {
            if (cls === 'I' || cls === 'II') {
                descEl.value = `Look at each picture and question carefully and pick the matching answer! ⭐`;
            } else if (cls === 'III' || cls === 'IV' || cls === 'V') {
                descEl.value = `Read each challenge carefully, think step-by-step, and pick the best answer!`;
            } else {
                descEl.value = `Analyze each question, apply core principles of ${currentSub}, and choose the correct option.`;
            }
        }

        // 5. AI Prompt Box
        const promptEl = document.getElementById('aiTaskPrompt');
        if (promptEl) {
            promptEl.value = `${defaultIdea.title}: ${defaultIdea.prompt}`;
        }
    }

    // 6. Refresh the dynamic ideas tags and highlight the first one
    updateAiIdeaTags(true);

    const firstBtn = document.querySelector('.ai-tag-btn[data-idea-title]');
    if (firstBtn) firstBtn.classList.add('active');

    const statusEl = document.getElementById('aiGenerationStatus');
    if (statusEl) statusEl.style.display = 'none';

    if (typeof updateSkillAreaPickerContext === 'function') {
        updateSkillAreaPickerContext();
    }
}

function openCreateTaskModal(focusAi = false) {
    const cls = AppState.selectedClass || 'IV';
    const clsSelect = document.getElementById('newTaskClass');
    if (clsSelect) clsSelect.value = cls;

    const currentSub = AppState.teacherSubjectFilter !== 'all' ? AppState.teacherSubjectFilter : (cls === 'I' || cls === 'II' ? 'Mathematics' : 'Science');

    document.getElementById('newTaskAssignNow').checked = true;
    toggleCreateTaskAssignList(true);

    renderCreateTaskStudentsList();

    // Default with 1 clean question block
    currentCreateTaskQuestions = [
        {
            prompt: '',
            options: ['', '', '', ''],
            answer: 0,
            explanation: ''
        }
    ];
    renderQuestionBlocks();

    // Sync Task Title, Subject, Skill Area, Time, and Prompt based upon the class itself!
    syncCurriculumDefaultsForClass(cls, currentSub);

    // Reset AI status & feedback
    const aiStatus = document.getElementById('aiGenerationStatus');
    if (aiStatus) {
        aiStatus.style.display = 'none';
        aiStatus.className = 'ai-status-strip';
        aiStatus.innerHTML = '';
    }

    // Reset Game Builder preview and inputs
    currentCreateTaskInteractiveConfig = null;
    currentCreateTaskGameType = 'auto';
    const previewCard = document.getElementById('aiBuiltGamePreviewCard');
    if (previewCard) previewCard.style.display = 'none';
    const gameTypeSelect = document.getElementById('newTaskGameType');
    if (gameTypeSelect) gameTypeSelect.value = 'auto';
    const condInput = document.getElementById('aiGameConditions');
    if (condInput) condInput.value = '';
    const infoInput = document.getElementById('aiGameInformation');
    if (infoInput) infoInput.value = '';

    document.getElementById('teacherCreateTaskModal').classList.add('active');

    if (focusAi) {
        setTimeout(() => {
            const promptEl = document.getElementById('aiTaskPrompt');
            if (promptEl) {
                promptEl.focus();
                promptEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }, 150);
    } else {
        setTimeout(() => {
            const titleEl = document.getElementById('newTaskTitle');
            if (titleEl) {
                titleEl.focus();
                titleEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }, 150);
    }
}

function setAiPrompt(promptText, subject) {
    const promptEl = document.getElementById('aiTaskPrompt');
    if (promptEl) {
        promptEl.value = promptText;
        promptEl.focus();
    }
    if (subject) {
        const subSelect = document.getElementById('newTaskSubject');
        if (subSelect) {
            for (let i = 0; i < subSelect.options.length; i++) {
                if (subSelect.options[i].value.toLowerCase() === subject.toLowerCase()) {
                    subSelect.selectedIndex = i;
                    break;
                }
            }
        }
    }
    const titleEl = document.getElementById('newTaskTitle');
    if (titleEl && !titleEl.value.trim()) {
        titleEl.value = promptText.split(':')[0].trim();
    }
    const statusEl = document.getElementById('aiGenerationStatus');
    if (statusEl) statusEl.style.display = 'none';
}

function showAiStatus(msg, type = 'info') {
    const statusEl = document.getElementById('aiGenerationStatus');
    if (!statusEl) return;
    statusEl.style.display = 'flex';
    statusEl.className = 'ai-status-strip ' + type;

    let iconHtml = 'ℹ️';
    if (type === 'loading') {
        iconHtml = '<span class="ai-spinner"></span>';
    } else if (type === 'success') {
        iconHtml = '✨';
    } else if (type === 'warning') {
        iconHtml = '⚠️';
    } else if (type === 'error') {
        iconHtml = '❌';
    }

    statusEl.innerHTML = `<span>${iconHtml}</span> <span>${escapeHtml(msg)}</span>`;
}

async function triggerAiTaskGeneration(forceRefresh = false, isGameBuilder = true) {
    const promptEl = document.getElementById('aiTaskPrompt');
    let prompt = (promptEl ? promptEl.value : '').trim();

    const cls = document.getElementById('newTaskClass')?.value || AppState.selectedClass || 'IV';
    const subject = document.getElementById('newTaskSubject')?.value || 'Science';
    const skillVal = document.getElementById('newTaskSkillArea')?.value?.trim();
    const numQuestions = parseInt(document.getElementById('aiNumQuestions')?.value || '3', 10);
    const difficulty = document.getElementById('aiDifficulty')?.value || 'Medium';

    const gameTypeSelect = document.getElementById('newTaskGameType');
    const gameType = gameTypeSelect ? gameTypeSelect.value : 'auto';

    const condInput = document.getElementById('aiGameConditions');
    const conditions = condInput ? condInput.value.trim() : '';

    const infoInput = document.getElementById('aiGameInformation');
    const information = infoInput ? infoInput.value.trim() : '';

    // If prompt is empty, use the Task Title, Skill Area, or Information
    if (!prompt) {
        const titleVal = document.getElementById('newTaskTitle')?.value?.trim();
        if (titleVal || skillVal) {
            prompt = [titleVal, skillVal].filter(Boolean).join(' - ');
            if (promptEl) promptEl.value = prompt;
        } else if (information) {
            prompt = information.split('\n')[0].substring(0, 50);
            if (promptEl) promptEl.value = prompt;
        }
    }

    if (!prompt) {
        showAiStatus('Please enter a Task Title above, or a topic prompt, or custom information below.', 'warning');
        const titleEl = document.getElementById('newTaskTitle');
        if (titleEl && !titleEl.value.trim()) {
            titleEl.focus();
        } else if (promptEl) {
            promptEl.focus();
        }
        return;
    }

    const btnGame = document.getElementById('btnBuildAiGame');
    const btnQuiz = document.getElementById('btnGenerateAiQuizOnly');
    const btnFresh = document.getElementById('btnGenerateAiFresh');
    const btnIcon = document.getElementById('aiBtnIcon');
    const btnText = document.getElementById('aiBtnText');
    const origGameText = btnText ? btnText.textContent : 'Build Small-Scale Game with AI';

    // Loading state
    if (btnGame) btnGame.disabled = true;
    if (btnQuiz) btnQuiz.disabled = true;
    if (btnFresh) btnFresh.disabled = true;
    if (btnIcon) btnIcon.innerHTML = '<span class="ai-spinner"></span>';
    if (btnText) btnText.textContent = isGameBuilder ? (forceRefresh ? 'Building Fresh Game...' : 'AI Agent Building Game...') : 'Designing Quiz...';

    const statusActionText = isGameBuilder
        ? `🤖 AI Game Developer Agent is architecting a tactile small-scale game for Class ${cls} ${subject} (${prompt})...`
        : `AI is checking question bank & designing ${numQuestions} ${difficulty.toLowerCase()} questions for Class ${cls} ${subject}...`;
    showAiStatus(statusActionText, 'loading');

    try {
        const response = await fetch('/api/ai/generate-task', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt: prompt,
                class: cls,
                subject: subject,
                topic: skillVal || prompt,
                game_type: gameType,
                conditions: conditions,
                information: information,
                num_questions: numQuestions,
                difficulty: difficulty,
                is_game_builder: isGameBuilder,
                force_refresh: forceRefresh
            })
        });

        const result = await response.json();

        if (!response.ok || (result.status !== 'success' && !result.success)) {
            throw new Error(result.message || result.error || 'Failed to generate task. Please try again.');
        }

        const task = result.task || (result.data ? result.data.task : null) || {};
        const questions = task.questions || (result.data ? result.data.questions : null) || [];

        populateCreateTaskForm(task, questions, subject);

        const isCached = result.cached || (result.provider && result.provider.includes('Question Bank Cache'));
        const providerName = result.provider || (result.data && result.data.source === 'gemini' ? 'Google Gemini AI' : 'AI Game Developer Agent');

        let statusMsg = '';
        if (task.interactiveConfig) {
            statusMsg = `🎮 AI Game Developer Agent built "${task.title || 'Game'}" with tactile ${task.gameType || 'Mini-Game'} engine & ${questions.length} questions via ${providerName}! Click "▶️ Test Play Game" below to try it!`;
        } else if (isCached) {
            statusMsg = `⚡ Served instantly from Question Bank Cache (0s)! "${task.title || 'Task'}" ready with ${questions.length} questions (${difficulty}).`;
        } else {
            statusMsg = `✨ Generated "${task.title || 'Task'}" with ${questions.length} questions (${difficulty}) via ${providerName}! Review and publish below.`;
        }

        showAiStatus(statusMsg, 'success');
        showToastNotification(`✨ AI Agent built "${task.title || 'Activity'}" successfully!`);

    } catch (err) {
        console.warn('Backend generation unreachable, attempting smart client-side curriculum fallback:', err);
        const clientTask = generateClientCurriculumTask(prompt, cls, subject, numQuestions, difficulty);
        if (clientTask) {
            populateCreateTaskForm(clientTask, clientTask.questions, subject);
            showAiStatus(`✨ Generated "${clientTask.title}" (${clientTask.questions.length} questions) via Built-in Curriculum Engine! Review and publish below.`, 'success');
            showToastNotification(`✨ Generated ${clientTask.questions.length} questions successfully!`);
        } else {
            showAiStatus(`⚠️ ${err.message || 'Generation failed. Please try again.'}`, 'error');
        }
    } finally {
        if (btnGame) btnGame.disabled = false;
        if (btnQuiz) btnQuiz.disabled = false;
        if (btnFresh) btnFresh.disabled = false;
        if (btnIcon) btnIcon.textContent = '🎮';
        if (btnText) btnText.textContent = origGameText;
    }
}

function populateCreateTaskForm(task, questions, subjectFallback = 'Science') {
    if (!task) return;

    // Save active interactive game configuration & type
    currentCreateTaskInteractiveConfig = task.interactiveConfig || null;
    currentCreateTaskGameType = task.gameType || (task.interactiveConfig ? 'Sort & Group' : 'MCQ Quiz');

    // 1. Populate Task Info
    const titleEl = document.getElementById('newTaskTitle');
    if (titleEl && task.title) {
        titleEl.value = task.title;
    }

    const detectedSubject = task.subject || subjectFallback;
    if (detectedSubject) {
        const subSelect = document.getElementById('newTaskSubject');
        if (subSelect) {
            for (let i = 0; i < subSelect.options.length; i++) {
                if (subSelect.options[i].value.toLowerCase() === detectedSubject.toLowerCase()) {
                    subSelect.selectedIndex = i;
                    break;
                }
            }
        }
    }

    const skill = task.skillArea || task.skill_area || task.topic;
    if (skill) {
        const skillEl = document.getElementById('newTaskSkillArea');
        if (skillEl) skillEl.value = skill;
    }

    // Sync Game Type Dropdown
    const gameTypeSelect = document.getElementById('newTaskGameType');
    if (gameTypeSelect) {
        const engine = (task.interactiveConfig && task.interactiveConfig.engine) ? task.interactiveConfig.engine : '';
        const gType = (task.gameType || '').toLowerCase();
        for (let i = 0; i < gameTypeSelect.options.length; i++) {
            const optVal = gameTypeSelect.options[i].value.toLowerCase();
            const optText = gameTypeSelect.options[i].text.toLowerCase();
            if (engine && (optVal === engine || optText.includes(engine))) {
                gameTypeSelect.selectedIndex = i;
                break;
            } else if (gType && (optVal.includes(gType) || optText.includes(gType))) {
                gameTypeSelect.selectedIndex = i;
                break;
            }
        }
    }

    const desc = task.desc || task.description;
    if (desc) {
        const descEl = document.getElementById('newTaskDesc');
        if (descEl) descEl.value = desc;
    }

    const timeVal = task.time || task.estimated_time;
    if (timeVal) {
        const timeSelect = document.getElementById('newTaskTime');
        if (timeSelect) {
            for (let i = 0; i < timeSelect.options.length; i++) {
                if (timeSelect.options[i].value.toLowerCase().includes(String(timeVal).toLowerCase())) {
                    timeSelect.selectedIndex = i;
                    break;
                }
            }
        }
    }

    // 2. Render Interactive Built Game Preview Card
    const previewCard = document.getElementById('aiBuiltGamePreviewCard');
    if (previewCard) {
        if (task.interactiveConfig) {
            previewCard.style.display = 'flex';
            const iconEl = document.getElementById('aiBuiltGameIcon');
            const titleEl = document.getElementById('aiBuiltGameTitle');
            const summaryEl = document.getElementById('aiBuiltGameSummary');
            const cfg = task.interactiveConfig;

            if (iconEl) iconEl.textContent = cfg.icon || '🎮';
            if (titleEl) titleEl.textContent = `🎮 Interactive ${task.gameType || 'Mini-Game'} Built: ${cfg.title || task.title}`;

            if (summaryEl) {
                let summary = `Tactile ${cfg.engine || 'interactive'} mini-game ready to test play!`;
                if (cfg.engine === 'bucket-sorter' && Array.isArray(cfg.buckets) && Array.isArray(cfg.items)) {
                    summary = `${cfg.buckets.length} Buckets (${cfg.buckets.map(b => b.label.replace(/⭐/g, '').trim()).join(', ')}) · ${cfg.items.length} cards to sort`;
                } else if (cfg.engine === 'pair-matcher' && Array.isArray(cfg.pairs)) {
                    summary = `${cfg.pairs.length} matching pairs challenge (connector arena)`;
                } else if (cfg.engine === 'word-train' && Array.isArray(cfg.rounds) && cfg.rounds[0]) {
                    summary = `${(cfg.rounds[0].words || []).length} sequential stages train challenge`;
                } else if (cfg.engine === 'word-scramble' && Array.isArray(cfg.rounds)) {
                    summary = `${cfg.rounds.length} vocabulary words letter arrange challenge`;
                } else if (cfg.engine === 'number-line-hopper') {
                    summary = 'Freddie Frog number line skip-counting challenge';
                } else if (cfg.engine === 'bubble-pop') {
                    summary = 'Fast-action target bubbles pop challenge';
                }
                summaryEl.textContent = summary;
            }
        } else {
            previewCard.style.display = 'none';
        }
    }

    // 3. Populate Questions
    const qList = questions || task.questions || [];
    if (Array.isArray(qList) && qList.length > 0) {
        currentCreateTaskQuestions = qList.map(q => ({
            prompt: q.prompt || q.question || '',
            options: (Array.isArray(q.options) && q.options.length >= 2)
                ? [q.options[0] || '', q.options[1] || '', q.options[2] || '', q.options[3] || '']
                : ['', '', '', ''],
            answer: (typeof q.answer === 'number' && q.answer >= 0 && q.answer < 4) ? q.answer : 0,
            explanation: q.explanation || '',
            visual_hint: q.visual_hint || '',
            svg_diagram: q.svg_diagram || ''
        }));
        renderQuestionBlocks();
    }

    // Smooth scroll to task details
    setTimeout(() => {
        const titleInput = document.getElementById('newTaskTitle');
        if (titleInput) {
            titleInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
            titleInput.focus();
        }
    }, 250);
}

function generateClientCurriculumTask(prompt, cls, subject, numQuestions, difficulty) {
    const p = (prompt || '').toLowerCase();
    let title = `${prompt} Explorer`;
    let skill = `${prompt} Concepts`;
    let detectedSubject = subject || 'Science';
    let desc = `Interactive learning quest on ${prompt} for Class ${cls}.`;
    let questions = [];

    if (p.includes('phonic') || p.includes('sound') || p.includes('rhym') || (cls === 'I' && subject === 'English')) {
        title = '🔤 Phonics & Letter Sounds Explorer';
        skill = 'Phonics & Sounds';
        detectedSubject = 'English';
        desc = 'Learn letter sounds, vowels, and rhyming words with fun picture challenges!';
        questions = [
            {
                prompt: 'Which letter makes the starting sound in the word "Apple"?',
                options: ['Letter A (Ah)', 'Letter B (Buh)', 'Letter C (Kuh)', 'Letter D (Duh)'],
                answer: 0,
                explanation: 'Apple starts with the short vowel "A" sound (/æ/).',
                visual_hint: '🍎 A is for Apple!'
            },
            {
                prompt: 'Which of the following words rhymes with "Cat"?',
                options: ['Hat', 'Dog', 'Sun', 'Cup'],
                answer: 0,
                explanation: 'Cat and Hat have the same ending sound (-at).',
                visual_hint: '🐱 Cat wearing a Hat!'
            },
            {
                prompt: 'Which of these letters is a vowel?',
                options: ['Letter E', 'Letter B', 'Letter T', 'Letter M'],
                answer: 0,
                explanation: 'The five English vowels are A, E, I, O, and U.',
                visual_hint: '⭐ Vowels are A, E, I, O, U!'
            },
            {
                prompt: 'What sound does the letter "S" make, like in "Sun"?',
                options: ['/s/ like a hissing snake', '/b/ like a bouncing ball', '/m/ like humming', '/p/ like popping'],
                answer: 0,
                explanation: 'The letter S makes the hissing /s/ sound as in Sun, Star, and Snake.',
                visual_hint: '☀️ S is for Sun!'
            },
            {
                prompt: 'Which word is the opposite of "Big"?',
                options: ['Small', 'Tall', 'Fast', 'Hot'],
                answer: 0,
                explanation: 'Small is the direct opposite of Big.',
                visual_hint: '🐘 Big elephant vs 🐭 Small mouse.'
            }
        ];
    } else if (p.includes('count') || p.includes('number') || (cls === 'I' && subject === 'Mathematics')) {
        title = '🔢 Fun with Numbers & Counting 1-20';
        skill = 'Counting & Number Sense';
        detectedSubject = 'Mathematics';
        desc = 'Count colorful objects, find missing numbers, and practice simple addition!';
        questions = [
            {
                prompt: 'How many fingers do we have on two hands together?',
                options: ['10 fingers', '5 fingers', '8 fingers', '12 fingers'],
                answer: 0,
                explanation: 'We have 5 fingers on each hand, making 5 + 5 = 10 fingers in total.',
                visual_hint: '🖐️ 5 on left + 🖐️ 5 on right = 10!'
            },
            {
                prompt: 'What number comes immediately after 6?',
                options: ['7', '5', '8', '9'],
                answer: 0,
                explanation: 'Counting forward: 1, 2, 3, 4, 5, 6, 7!',
                visual_hint: '🔢 6 comes before 7.'
            },
            {
                prompt: 'If you have 3 red balloons and get 2 more, how many balloons do you have in all?',
                options: ['5 balloons', '4 balloons', '6 balloons', '3 balloons'],
                answer: 0,
                explanation: '3 + 2 = 5 balloons.',
                visual_hint: '🎈 3 balloons + 🎈🎈 2 balloons = 5!'
            },
            {
                prompt: 'Which number is smaller: 4 or 9?',
                options: ['4 is smaller', '9 is smaller', 'Both are equal', 'Neither'],
                answer: 0,
                explanation: '4 comes before 9 on the number line, so 4 is smaller.',
                visual_hint: '📉 4 is fewer than 9.'
            },
            {
                prompt: 'Which shape has 3 straight sides and 3 corners?',
                options: ['Triangle', 'Circle', 'Square', 'Rectangle'],
                answer: 0,
                explanation: 'A triangle is a 3-sided shape with 3 corners.',
                visual_hint: '🔺 Triangle has 3 sides.'
            }
        ];
    } else if (p.includes('sense') || (cls === 'I' && subject === 'EVS')) {
        title = '👀 5 Senses & My Body Adventure';
        skill = 'Sense Organs & Hygiene';
        detectedSubject = 'EVS';
        desc = 'Discover the 5 senses and learn how to take care of our body!';
        questions = [
            {
                prompt: 'Which sense organ helps us see bright colors and read storybooks?',
                options: ['Our Eyes', 'Our Ears', 'Our Nose', 'Our Tongue'],
                answer: 0,
                explanation: 'Eyes provide the sense of sight so we can see the world around us.',
                visual_hint: '👀 Eyes help us see!'
            },
            {
                prompt: 'What should we do before eating food to keep away germs?',
                options: ['Wash hands with soap and water', 'Skip washing', 'Rub hands on clothes', 'Sleep first'],
                answer: 0,
                explanation: 'Washing hands with soap kills germs and prevents sickness.',
                visual_hint: '🧼 Clean hands protect against germs!'
            },
            {
                prompt: 'Which sense organ helps us listen to birds singing and music?',
                options: ['Our Ears', 'Our Nose', 'Our Tongue', 'Our Skin'],
                answer: 0,
                explanation: 'Ears provide the sense of hearing.',
                visual_hint: '👂 Ears help us hear!'
            }
        ];
    } else if (p.includes('electric') || p.includes('circuit') || p.includes('batter') || p.includes('switch')) {
        title = '⚡ Electricity & Circuit Quest';
        skill = 'Electricity & Circuits';
        detectedSubject = (cls === 'I' || cls === 'II' || cls === 'III' || cls === 'IV' || cls === 'V') ? 'EVS' : 'Science';
        desc = 'Explore how electric circuits, batteries, switches, and conductors power our daily devices!';
        questions = [
            {
                prompt: 'What do we call the complete, unbroken loop that electricity flows through?',
                options: ['A straight line', 'An electric circuit', 'A water pipe', 'A battery box'],
                answer: 1,
                explanation: 'An electric circuit is an unbroken conductive loop that allows electricity to flow and power devices.',
                visual_hint: '🔋 A circuit needs an unbroken loop from battery to bulb!'
            },
            {
                prompt: 'Which of the following materials is a good conductor of electricity?',
                options: ['Copper wire', 'Rubber band', 'Plastic ruler', 'Dry wood'],
                answer: 0,
                explanation: 'Copper is a metal with free electrons that easily conducts electrical current.',
                visual_hint: '🔌 Metals like copper conduct electricity, while rubber and plastics act as insulators.'
            },
            {
                prompt: 'What happens in a circuit when an electric switch is turned OFF?',
                options: ['The bulb glows brighter', 'The circuit opens and stops current', 'The battery recharges', 'More electricity flows'],
                answer: 1,
                explanation: 'Turning a switch OFF creates an air gap, opening the circuit and stopping the electric current.',
                visual_hint: '💡 A switch safely opens (stops) or closes (starts) the electric path.'
            },
            {
                prompt: 'Which component provides the electrical energy in a portable flashlight?',
                options: ['The glass lens', 'The dry cell battery', 'The plastic handle', 'The screw cap'],
                answer: 1,
                explanation: 'The dry cell battery converts chemical energy into electrical energy to light up the torch bulb.',
                visual_hint: '🔋 Batteries store chemical energy to produce electrical voltage.'
            },
            {
                prompt: 'Why must we never touch electric switches with wet hands?',
                options: ['Water breaks the plastic', 'Water conducts electricity and can shock', 'Water cools the switch', 'It drains the battery'],
                answer: 1,
                explanation: 'Normal water contains dissolved minerals making it a conductor, which can cause severe electric shocks.',
                visual_hint: '⚠️ Always keep hands completely dry before operating electrical appliances!'
            }
        ];
    } else if (p.includes('solar') || p.includes('planet') || p.includes('space') || p.includes('sun') || p.includes('orbit')) {
        title = '🪐 Solar System Cosmic Quest';
        skill = 'Planets & Solar System';
        detectedSubject = 'Science';
        desc = 'Embark on an astronomical journey exploring the Sun, Moon, Earth, and orbiting planets!';
        questions = [
            {
                prompt: 'Which celestial body sits at the very center of our Solar System?',
                options: ['The Moon', 'The Sun', 'Earth', 'Jupiter'],
                answer: 1,
                explanation: 'The Sun is the massive central star of our Solar System around which all planets orbit.',
                visual_hint: '☀️ The Sun provides the gravitational anchor and light for all planets.'
            },
            {
                prompt: 'Which planet in our Solar System is famously known as the "Red Planet"?',
                options: ['Venus', 'Mars', 'Jupiter', 'Mercury'],
                answer: 1,
                explanation: 'Mars appears red because of iron oxide (rust) present across its surface dust.',
                visual_hint: '🔴 Mars has a reddish appearance due to iron-rich rocks and soil.'
            },
            {
                prompt: 'How long does Earth take to make one complete revolution around the Sun?',
                options: ['24 hours', '30 days', '365 1/4 days (1 year)', '10 years'],
                answer: 2,
                explanation: 'One complete revolution of Earth around the Sun takes approximately 365.25 days (1 year).',
                visual_hint: '🌍 One year equals one full revolution around the Sun.'
            },
            {
                prompt: 'Which is the largest planet in our Solar System?',
                options: ['Saturn', 'Jupiter', 'Neptune', 'Earth'],
                answer: 1,
                explanation: 'Jupiter is the largest planet, over 1,300 times larger in volume than Earth.',
                visual_hint: '🪐 Jupiter is a massive gas giant with famous storm bands.'
            },
            {
                prompt: 'What causes the daily cycle of day and night on Earth?',
                options: ['The Sun moving up and down', 'Earth spinning on its own axis', 'The Moon blocking the Sun', 'Clouds passing by'],
                answer: 1,
                explanation: 'Earth rotates on its axis once every 24 hours, bringing parts into sunlight (day) and away (night).',
                visual_hint: '🔄 Earth spins once on its axis every 24 hours.'
            }
        ];
    } else if (p.includes('magnet') || p.includes('pole')) {
        title = '🧲 Magnetic Force Challenge';
        skill = 'Magnets & Magnetic Poles';
        detectedSubject = 'Science';
        desc = 'Investigate magnetic poles, attraction, repulsion, and magnetic materials!';
        questions = [
            {
                prompt: 'What happens when two North (N) poles of two magnets are brought close?',
                options: ['They stick firmly', 'They repel (push apart)', 'They melt', 'They lose charge'],
                answer: 1,
                explanation: 'Like poles (North-North or South-South) always repel each other.',
                visual_hint: '🧲 Like magnetic poles repel; opposite poles attract!'
            },
            {
                prompt: 'Which of the following materials is strongly attracted by a magnet?',
                options: ['Plastic straw', 'Iron nail', 'Wooden toothpick', 'Glass marble'],
                answer: 1,
                explanation: 'Iron is a ferromagnetic material that is strongly attracted to magnets.',
                visual_hint: '📎 Magnets attract iron, nickel, and steel.'
            },
            {
                prompt: 'Which direction does a freely suspended magnetic compass needle naturally align?',
                options: ['East-West', 'North-South', 'Random direction', 'Towards the Sun'],
                answer: 1,
                explanation: 'Earth behaves like a giant magnet, aligning magnetic compass needles along the North-South axis.',
                visual_hint: '🧭 Compass needles point along Earth’s magnetic North-South poles.'
            }
        ];
    } else if (p.includes('fraction') || p.includes('decimal') || p.includes('ratio')) {
        title = '🍕 Fraction & Division Mastery';
        skill = 'Fractions & Parts of a Whole';
        detectedSubject = 'Mathematics';
        desc = 'Understand halves, quarters, numerators, and denominators through fun real-world sharing!';
        questions = [
            {
                prompt: 'If a pizza is divided into 4 equal slices and you eat 1 slice, what fraction was eaten?',
                options: ['1/2', '1/4', '3/4', '4/1'],
                answer: 1,
                explanation: '1 slice out of 4 equal parts equals the fraction 1/4 (one quarter).',
                visual_hint: '🍕 1 slice out of 4 equal slices = 1/4 of the pizza.'
            },
            {
                prompt: 'What is 1/2 of 10 chocolates?',
                options: ['2 chocolates', '5 chocolates', '4 chocolates', '8 chocolates'],
                answer: 1,
                explanation: 'Half of 10 is 10 ÷ 2 = 5 chocolates.',
                visual_hint: '🍫 Dividing 10 into 2 equal halves gives 5 in each group.'
            },
            {
                prompt: 'In the fraction 3/5, what does the bottom number (5) represent?',
                options: ['The slices eaten', 'The total number of equal parts', 'The number of plates', 'The extra pieces'],
                answer: 1,
                explanation: 'The denominator (bottom number) always tells the total number of equal parts the whole was divided into.',
                visual_hint: '📊 Denominator = total parts; Numerator = parts selected.'
            },
            {
                prompt: 'Which of the following fractions is equivalent to 1/2?',
                options: ['2/4', '1/3', '3/5', '1/4'],
                answer: 0,
                explanation: '2/4 simplifies to 1/2 when dividing numerator and denominator by 2.',
                visual_hint: '🍰 2 fourths equals exactly 1 half.'
            }
        ];
    } else if (p.includes('plant') || p.includes('leaf') || p.includes('root') || p.includes('photosynth')) {
        title = '🌿 Plant Life & Photosynthesis';
        skill = 'Plant Parts & Functions';
        detectedSubject = 'Science';
        desc = 'Learn about roots, stems, leaves, flowers, and how green plants make food with sunlight!';
        questions = [
            {
                prompt: 'Which part of a plant absorbs water and minerals from the soil?',
                options: ['The flowers', 'The roots', 'The leaves', 'The fruit'],
                answer: 1,
                explanation: 'Roots anchor the plant and absorb essential water and dissolved minerals from the soil.',
                visual_hint: '🌱 Underground roots draw moisture and minerals upward.'
            },
            {
                prompt: 'What is the green pigment in plant leaves that captures sunlight called?',
                options: ['Chlorophyll', 'Oxygen', 'Stomata', 'Glucose'],
                answer: 0,
                explanation: 'Chlorophyll gives leaves their green colour and traps solar energy for photosynthesis.',
                visual_hint: '🍃 Chlorophyll absorbs sunlight to produce plant sugars.'
            },
            {
                prompt: 'What vital gas do plants release into the air during photosynthesis?',
                options: ['Carbon dioxide', 'Oxygen', 'Nitrogen', 'Methane'],
                answer: 1,
                explanation: 'During photosynthesis, plants take in carbon dioxide and release life-giving oxygen.',
                visual_hint: '💨 Green plants produce oxygen that humans and animals breathe.'
            }
        ];
    } else if (p.includes('water') && (p.includes('cycle') || p.includes('rain') || p.includes('evaporat'))) {
        title = '💧 Water Cycle Explorer';
        skill = 'Water Cycle & Weather';
        detectedSubject = 'EVS';
        desc = 'Trace how water evaporates into the sky, condenses into clouds, and falls as rainfall!';
        questions = [
            {
                prompt: 'What process turns liquid water into invisible water vapour when heated by the Sun?',
                options: ['Freezing', 'Evaporation', 'Precipitation', 'Condensation'],
                answer: 1,
                explanation: 'Evaporation happens when the Sun heats water in oceans and lakes, turning it into gas vapour.',
                visual_hint: '☀️ Sun warmth turns surface water into rising vapour (evaporation).'
            },
            {
                prompt: 'What are white floating clouds in the sky made of?',
                options: ['White smoke', 'Cotton wool', 'Billions of tiny water droplets', 'Dry air'],
                answer: 2,
                explanation: 'Clouds form when rising water vapour cools and condenses into billions of microscopic liquid droplets.',
                visual_hint: '☁️ Condensed water droplets cluster together to form clouds.'
            },
            {
                prompt: 'When water droplets in clouds become too heavy and fall to the ground, it is called:',
                options: ['Evaporation', 'Precipitation (Rain)', 'Filtration', 'Transpiration'],
                answer: 1,
                explanation: 'Precipitation occurs when cloud water droplets combine and fall as rain, hail, or snow.',
                visual_hint: '🌧️ Rain falling from heavy clouds is precipitation.'
            }
        ];
    } else if (p.includes('gramm') || p.includes('verb') || p.includes('noun') || p.includes('tense')) {
        title = '🔤 English Grammar Detective';
        skill = 'Grammar & Parts of Speech';
        detectedSubject = 'English';
        desc = 'Master action verbs, naming words, adjectives, and clear sentence structure!';
        questions = [
            {
                prompt: 'Which word in the sentence is an action verb: "The quick puppy jumped over the fence"?',
                options: ['Puppy', 'Jumped', 'Fence', 'Quick'],
                answer: 1,
                explanation: '"Jumped" expresses the physical action performed by the puppy.',
                visual_hint: '🏃 Verbs describe actions, states, or occurrences.'
            },
            {
                prompt: 'What is the simple past tense of the verb "go"?',
                options: ['Goed', 'Went', 'Going', 'Gone'],
                answer: 1,
                explanation: '"Go" is an irregular verb whose simple past form is "went".',
                visual_hint: '📅 Today I go; yesterday I went.'
            },
            {
                prompt: 'Which word is an adjective that describes a noun: "Aarav wore a bright red sweater"?',
                options: ['Aarav', 'Bright', 'Wore', 'Sweater'],
                answer: 1,
                explanation: '"Bright" (and "red") are adjectives describing the appearance of the sweater.',
                visual_hint: '🎨 Adjectives describe the quality, colour, or size of nouns.'
            }
        ];
    } else {
        questions = [
            {
                prompt: `Which of the following is the key concept in ${prompt}?`,
                options: ['Understanding core principles', 'Ignoring classroom rules', 'Memorizing without meaning', 'Guessing answers'],
                answer: 0,
                explanation: `Learning ${prompt} requires understanding the underlying core principles and applying them.`,
                visual_hint: `🎯 Focus on fundamental concepts in ${prompt}.`
            },
            {
                prompt: `Why is learning about ${prompt} important in our daily lives?`,
                options: ['It has no practical use', 'It helps us understand the world around us', 'It is only for tests', 'It replaces school'],
                answer: 1,
                explanation: `Studying ${prompt} equips students to solve real-world problems and understand how things work.`,
                visual_hint: `💡 Real-world applications make learning memorable.`
            },
            {
                prompt: `Which habit helps a student master ${prompt} most effectively?`,
                options: ['Practicing problems step-by-step', 'Skipping practice', 'Rushing through questions', 'Waiting until exams'],
                answer: 0,
                explanation: 'Consistent step-by-step practice builds deep conceptual mastery and confidence.',
                visual_hint: '📚 Regular practice leads to success.'
            }
        ];
    }

    return {
        title: title,
        subject: detectedSubject,
        class: cls,
        skillArea: skill,
        topic: skill,
        desc: desc,
        time: '5 min',
        questions: questions.slice(0, Math.min(numQuestions, questions.length))
    };
}

async function checkAiStatus() {
    try {
        const res = await fetch('/api/ai/status');
        if (!res.ok) return;
        const status = await res.json();
        const badge = document.getElementById('aiModelBadge');
        if (badge && status) {
            if (status.active_engine === 'gemini' && status.has_gemini_key) {
                badge.textContent = 'Google Gemini AI 🟢';
                badge.title = 'Live Google Gemini AI Connected';
            } else {
                badge.textContent = 'Smart AI Engine ⚡';
                badge.title = 'Built-in Curriculum AI Generator Active';
            }
        }
    } catch (e) { }
}

/* ====================================================
   SKILL AREA / TOPIC POPUP DROPDOWN LOGIC
   ==================================================== */
function getSkillIconForSubjectAndGame(subject, gameType) {
    const gt = (gameType || '').toLowerCase();
    if (gt.includes('sort')) return '🧺';
    if (gt.includes('sequence') || gt.includes('order')) return '🚂';
    if (gt.includes('match') || gt.includes('pair')) return '🔗';
    if (gt.includes('word') || gt.includes('scramble')) return '🧩';
    if (gt.includes('line') || gt.includes('hop')) return '🐸';
    if (gt.includes('bubble') || gt.includes('pop')) return '🫧';
    if (gt.includes('quiz') || gt.includes('mcq')) return '📝';

    const sub = (subject || '').toLowerCase();
    if (sub.includes('math')) return '🔢';
    if (sub.includes('sci')) return '🔬';
    if (sub.includes('eng')) return '📖';
    if (sub.includes('evs')) return '🌿';
    if (sub.includes('social')) return '🏛️';
    return '🎯';
}

function getGameTypeBadgeClass(gameType) {
    const gt = (gameType || '').toLowerCase();
    if (gt.includes('sort')) return 'badge-sort';
    if (gt.includes('sequence') || gt.includes('order')) return 'badge-sequence';
    if (gt.includes('match') || gt.includes('pair')) return 'badge-match';
    if (gt.includes('quiz') || gt.includes('mcq')) return 'badge-mcq';
    return 'badge-other';
}

function getAvailableSkillsForCategory(cls, subject) {
    const cClean = (cls || 'IV').replace(/^Class\s*/i, '').trim();
    const subName = (subject || 'Science').trim();
    const subNorm = subName.toLowerCase();

    const chapterTopics = [];
    const catalogSkills = [];
    const seenSkills = new Set();

    // 1. Curriculum Chapter Topics (from CurriculumIdeasMap)
    const classMap = (typeof CurriculumIdeasMap !== 'undefined') ? (CurriculumIdeasMap[cClean] || CurriculumIdeasMap['IV'] || {}) : {};
    let subjectIdeas = classMap[subName] || [];
    if (!subjectIdeas || subjectIdeas.length === 0) {
        for (const k of Object.keys(classMap)) {
            if (k.toLowerCase() === subNorm) {
                subjectIdeas = classMap[k];
                break;
            }
        }
    }

    if (subjectIdeas && subjectIdeas.length > 0) {
        subjectIdeas.forEach(idea => {
            const skillName = idea.skill || idea.title;
            if (!seenSkills.has(skillName.toLowerCase())) {
                seenSkills.add(skillName.toLowerCase());
                chapterTopics.push({
                    skill: skillName,
                    title: idea.title,
                    activity: idea.prompt,
                    icon: idea.icon || getSkillIconForSubjectAndGame(subName, ''),
                    gameType: 'auto',
                    time: idea.time || '5 min',
                    prompt: idea.prompt,
                    type: 'topic'
                });
            }
        });
    }

    // 2. Syllabus Skill Areas & Activities (from FULL_GAMES_CATALOG)
    const catalog = (typeof FULL_GAMES_CATALOG !== 'undefined') ? FULL_GAMES_CATALOG : (window.FULL_GAMES_CATALOG || []);
    const seenCatalog = new Set();

    catalog.forEach(item => {
        const itemClass = (item.class || '').replace(/^Class\s*/i, '').trim();
        const itemSub = (item.subject || '').trim().toLowerCase();

        if (itemClass === cClean && itemSub === subNorm) {
            const skillName = (item.skillArea || item.topic || item.title || '').trim().replace(/[\uFFFD\u2013\u2014]/g, '-');
            const activityName = (item.activity || item.topic || '').trim().replace(/[\uFFFD\u2013\u2014]/g, '-');
            const actTitle = (item.title || activityName).trim();
            const key = `${skillName}:::${activityName}`.toLowerCase();

            if (!seenCatalog.has(key)) {
                seenCatalog.add(key);
                catalogSkills.push({
                    skill: skillName,
                    title: actTitle,
                    activity: activityName,
                    gameType: item.gameType || 'MCQ Quiz',
                    icon: getSkillIconForSubjectAndGame(subName, item.gameType),
                    desc: item.desc || '',
                    type: 'competency'
                });
            }
        }
    });

    return {
        chapterTopics,
        catalogSkills,
        totalCount: chapterTopics.length + catalogSkills.length
    };
}

function updateSkillAreaPickerContext() {
    const clsSelect = document.getElementById('newTaskClass');
    const subSelect = document.getElementById('newTaskSubject');
    const cls = clsSelect ? clsSelect.value : (AppState.selectedClass || 'IV');
    const sub = subSelect ? subSelect.value : 'Science';

    const { chapterTopics, catalogSkills, totalCount } = getAvailableSkillsForCategory(cls, sub);

    const countBadge = document.getElementById('skillPickerCountBadge');
    if (countBadge) countBadge.textContent = `${totalCount}`;

    const categoryText = document.getElementById('skillPickerCategoryText');
    if (categoryText) categoryText.textContent = `${sub} • Class ${cls}`;

    const availCount = document.getElementById('skillPickerAvailableCount');
    if (availCount) availCount.textContent = `${totalCount} Skills Available`;

    const dropdown = document.getElementById('skillAreaPickerDropdown');
    if (dropdown && dropdown.style.display !== 'none') {
        const searchInput = document.getElementById('skillPickerSearchInput');
        renderSkillPickerList(searchInput ? searchInput.value : '');
    }
}

function openSkillAreaPicker(event) {
    if (event) {
        event.stopPropagation();
    }
    const dropdown = document.getElementById('skillAreaPickerDropdown');
    if (!dropdown) return;

    dropdown.style.display = 'flex';
    updateSkillAreaPickerContext();

    const searchInput = document.getElementById('skillPickerSearchInput');
    if (searchInput) {
        searchInput.value = '';
    }
    renderSkillPickerList('');

    setTimeout(() => {
        const activeItem = dropdown.querySelector('.skill-picker-item.active');
        if (activeItem) {
            activeItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }, 60);
}

function closeSkillAreaPicker() {
    const dropdown = document.getElementById('skillAreaPickerDropdown');
    if (dropdown) dropdown.style.display = 'none';
}

function toggleSkillAreaPicker(event) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    const dropdown = document.getElementById('skillAreaPickerDropdown');
    if (!dropdown) return;
    if (dropdown.style.display === 'none' || !dropdown.style.display) {
        openSkillAreaPicker();
    } else {
        closeSkillAreaPicker();
    }
}

function filterSkillAreaPicker(query) {
    renderSkillPickerList(query);
}

function renderSkillPickerList(filterText = '') {
    const listEl = document.getElementById('skillPickerList');
    if (!listEl) return;

    const clsSelect = document.getElementById('newTaskClass');
    const subSelect = document.getElementById('newTaskSubject');
    const cls = clsSelect ? clsSelect.value : (AppState.selectedClass || 'IV');
    const sub = subSelect ? subSelect.value : 'Science';

    const { chapterTopics, catalogSkills } = getAvailableSkillsForCategory(cls, sub);
    const currentSkillVal = (document.getElementById('newTaskSkillArea')?.value || '').trim().toLowerCase();
    const q = (filterText || '').trim().toLowerCase();

    const filterItem = (item) => {
        if (!q) return true;
        const matchSkill = (item.skill || '').toLowerCase().includes(q);
        const matchTitle = (item.title || '').toLowerCase().includes(q);
        const matchAct = (item.activity || '').toLowerCase().includes(q);
        const matchGt = (item.gameType || '').toLowerCase().includes(q);
        return matchSkill || matchTitle || matchAct || matchGt;
    };

    const filteredTopics = chapterTopics.filter(filterItem);
    const filteredCatalog = catalogSkills.filter(filterItem);

    if (filteredTopics.length === 0 && filteredCatalog.length === 0) {
        listEl.innerHTML = `
                    <div class="skill-picker-empty">
                        <div style="font-size: 20px; margin-bottom: 4px;">🔍</div>
                        <div>No skills match <strong>"${escapeHtml(filterText)}"</strong> for Class ${cls} ${sub}.</div>
                        ${filterText ? `
                            <button type="button" class="skill-picker-custom-btn" onclick="selectSkillFromPicker('${escapeHtml(filterText).replace(/'/g, "\\'")}', 'auto', '', '')">
                                <span>✍️</span> Use "${escapeHtml(filterText)}" as topic
                            </button>
                        ` : ''}
                    </div>
                `;
        return;
    }

    let html = '';

    // Section 1: Core Curriculum Topics
    if (filteredTopics.length > 0) {
        html += `
                    <div class="skill-picker-section-title">
                        <span>🎯 Chapter &amp; Curriculum Modules</span>
                        <span>${filteredTopics.length}</span>
                    </div>
                `;
        filteredTopics.forEach(item => {
            const isActive = currentSkillVal === item.skill.toLowerCase() || currentSkillVal === item.title.toLowerCase();
            const escapedSkill = escapeHtml(item.skill).replace(/'/g, "\\'");
            const escapedGt = escapeHtml(item.gameType || 'auto').replace(/'/g, "\\'");
            const escapedTitle = escapeHtml(item.title).replace(/'/g, "\\'");
            const escapedPrompt = escapeHtml(item.prompt || '').replace(/'/g, "\\'");

            html += `
                        <div class="skill-picker-item ${isActive ? 'active' : ''}"
                            onclick="selectSkillFromPicker('${escapedSkill}', '${escapedGt}', '${escapedTitle}', '${escapedPrompt}')"
                            title="${escapeHtml(item.skill)}: ${escapeHtml(item.activity)}">
                            <div class="skill-item-left">
                                <div class="skill-item-title-row">
                                    <span class="skill-item-icon">${item.icon || '🎯'}</span>
                                    <span class="skill-item-name">${highlightMatch(escapeHtml(item.skill), q)}</span>
                                </div>
                                <div class="skill-item-sub">${highlightMatch(escapeHtml(item.title + ' • ' + item.activity), q)}</div>
                            </div>
                            <span class="skill-item-badge badge-other">📖 Topic</span>
                            ${isActive ? '<span class="skill-item-check">✓</span>' : ''}
                        </div>
                    `;
        });
    }

    // Section 2: Syllabus Competencies & Interactive Activities
    if (filteredCatalog.length > 0) {
        html += `
                    <div class="skill-picker-section-title" style="margin-top: 8px;">
                        <span>⚡ Curriculum Competencies &amp; Activities</span>
                        <span>${filteredCatalog.length}</span>
                    </div>
                `;
        filteredCatalog.forEach(item => {
            const isActive = currentSkillVal === item.skill.toLowerCase() || currentSkillVal === item.title.toLowerCase();
            const badgeClass = getGameTypeBadgeClass(item.gameType);
            const escapedSkill = escapeHtml(item.skill).replace(/'/g, "\\'");
            const escapedGt = escapeHtml(item.gameType || 'mcq').replace(/'/g, "\\'");
            const escapedTitle = escapeHtml(item.title).replace(/'/g, "\\'");
            const escapedDesc = escapeHtml(item.desc || item.activity || '').replace(/'/g, "\\'");

            html += `
                        <div class="skill-picker-item ${isActive ? 'active' : ''}"
                            onclick="selectSkillFromPicker('${escapedSkill}', '${escapedGt}', '${escapedTitle}', '${escapedDesc}')"
                            title="${escapeHtml(item.skill)} - ${escapeHtml(item.activity)} (${escapeHtml(item.gameType)})">
                            <div class="skill-item-left">
                                <div class="skill-item-title-row">
                                    <span class="skill-item-icon">${item.icon || '⚡'}</span>
                                    <span class="skill-item-name">${highlightMatch(escapeHtml(item.skill), q)}</span>
                                </div>
                                <div class="skill-item-sub">${highlightMatch(escapeHtml(item.activity ? item.activity + ' • ' + item.title : item.title), q)}</div>
                            </div>
                            <span class="skill-item-badge ${badgeClass}">${item.gameType}</span>
                            ${isActive ? '<span class="skill-item-check">✓</span>' : ''}
                        </div>
                    `;
        });
    }

    listEl.innerHTML = html;
}

function highlightMatch(text, query) {
    if (!query) return text;
    const idx = text.toLowerCase().indexOf(query.toLowerCase());
    if (idx === -1) return text;
    const before = text.slice(0, idx);
    const match = text.slice(idx, idx + query.length);
    const after = text.slice(idx + query.length);
    return `${before}<mark style="background: #fef08a; padding: 0 2px; border-radius: 2px;">${match}</mark>${after}`;
}

function selectSkillFromPicker(skillName, gameType, title, promptHint) {
    const skillInput = document.getElementById('newTaskSkillArea');
    if (skillInput) {
        skillInput.value = skillName;
    }

    // Sync Game Type if provided
    if (gameType && gameType !== 'auto') {
        const gtSelect = document.getElementById('newTaskGameType');
        if (gtSelect) {
            const gtMap = {
                'sort & group': 'sort-and-group',
                'match pairs': 'match-pairs',
                'sequence order': 'sequence-order',
                'word scramble': 'word-scramble',
                'number line hopper': 'number-line-hopper',
                'bubble pop': 'bubble-pop',
                'mcq quiz': 'mcq',
                'mcq': 'mcq'
            };
            const mappedVal = gtMap[gameType.toLowerCase()];
            if (mappedVal) {
                gtSelect.value = mappedVal;
            }
        }
    }

    // Suggest title if empty or default
    if (title) {
        const titleEl = document.getElementById('newTaskTitle');
        if (titleEl && (!titleEl.value || titleEl.value.startsWith('🎯') || titleEl.value.startsWith('💡'))) {
            titleEl.value = `🎯 ${title}`;
        }
    }

    // Update AI Prompt with topic context if empty or default
    if (promptHint) {
        const promptEl = document.getElementById('aiTaskPrompt');
        if (promptEl) {
            promptEl.value = `${title || skillName}: ${promptHint}`;
        }
    }

    // Trigger AI idea tags update
    handleCreateTaskTopicInput(skillName);

    // Close popup
    closeSkillAreaPicker();
}

// Global dismiss on click outside
document.addEventListener('click', function (e) {
    const container = document.getElementById('skillPickerContainer');
    const dropdown = document.getElementById('skillAreaPickerDropdown');
    if (dropdown && dropdown.style.display !== 'none') {
        if (container && !container.contains(e.target)) {
            closeSkillAreaPicker();
        }
    }
});

// Global dismiss on Esc
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
        closeSkillAreaPicker();
    }
});

function closeCreateTaskModal() {
    closeSkillAreaPicker();
    document.getElementById('teacherCreateTaskModal').classList.remove('active');
}

function handleCreateTaskClassChange(cls) {
    renderCreateTaskStudentsList();
    syncCurriculumDefaultsForClass(cls);
}

function handleCreateTaskSubjectChange(sub) {
    const cls = document.getElementById('newTaskClass')?.value || AppState.selectedClass || 'IV';
    syncCurriculumDefaultsForClass(cls, sub);
}

function handleCreateTaskTopicInput(val) {
    if (!val || val.trim().length < 2) {
        updateAiIdeaTags(false);
    } else {
        filterAiIdeaTags(val);
    }
}

function renderCreateTaskStudentsList() {
    const cls = document.getElementById('newTaskClass').value;
    const container = document.getElementById('newTaskStudentsList');
    if (!container) return;
    container.innerHTML = '';

    const roster = StudentRosters[cls] || [];
    roster.forEach(s => {
        const label = document.createElement('label');
        label.className = 'student-check-row';
        label.innerHTML = `
                    <input type="checkbox" name="createTaskStudentCheck" value="${s.roll}" data-name="${s.name}" checked>
                    <span>${s.name} (Roll #${s.roll})</span>
                `;
        container.appendChild(label);
    });
}

function toggleCreateTaskSelectAll() {
    const boxes = document.querySelectorAll('input[name="createTaskStudentCheck"]');
    const anyUnchecked = Array.from(boxes).some(b => !b.checked);
    boxes.forEach(b => b.checked = anyUnchecked);
}

function toggleCreateTaskAssignList(checked) {
    const cont = document.getElementById('createTaskStudentsContainer');
    const btn = document.getElementById('newTaskToggleAllBtn');
    if (cont) cont.style.display = checked ? 'block' : 'none';
    if (btn) btn.style.display = checked ? 'inline-block' : 'none';
}

function renderQuestionBlocks() {
    const container = document.getElementById('createTaskQuestionsList');
    const badge = document.getElementById('questionCountBadge');
    if (!container) return;
    container.innerHTML = '';
    if (badge) badge.textContent = currentCreateTaskQuestions.length;

    currentCreateTaskQuestions.forEach((q, qIdx) => {
        const block = document.createElement('div');
        block.className = 'q-block';
        block.innerHTML = `
                    <div class="q-header">
                        <span class="q-num-badge">Question ${qIdx + 1}</span>
                        ${currentCreateTaskQuestions.length > 1 ? `
                            <button type="button" class="btn-remove-q" onclick="removeQuestionBlock(${qIdx})">✕ Remove</button>
                        ` : ''}
                    </div>
                    ${q.visual_hint ? `
                        <div style="font-size: 12px; color: #4338ca; background: #eef2ff; border-radius: 8px; padding: 5px 10px; margin-bottom: 8px; font-weight: 600; display: inline-flex; align-items: center; gap: 6px;">
                            <span>💡 Clue:</span> ${escapeHtml(q.visual_hint)}
                        </div>
                    ` : ''}
                    ${q.svg_diagram ? `
                        <div style="max-height: 80px; overflow: hidden; margin-bottom: 8px; border-radius: 10px; border: 1.5px dashed #cbd5e1; padding: 4px; display: flex; justify-content: center; background: #f8fafc;">
                            ${q.svg_diagram}
                        </div>
                    ` : ''}
                    <div style="margin-bottom: 10px;">
                        <input type="text" class="assign-input q-prompt-input" data-qidx="${qIdx}" placeholder="Enter question prompt..." value="${escapeHtml(q.prompt)}">
                    </div>
                    <div style="font-size: 11.5px; font-weight: 700; color: #475569; margin-bottom: 6px;">
                        Options (select the radio button for the correct choice):
                    </div>
                    <div class="q-options-grid">
                        ${[0, 1, 2, 3].map(optIdx => `
                            <div class="q-opt-wrap ${q.answer === optIdx ? 'correct' : ''}">
                                <input type="radio" name="q_correct_${qIdx}" value="${optIdx}" ${q.answer === optIdx ? 'checked' : ''} onchange="setQuestionCorrectAnswer(${qIdx}, ${optIdx})">
                                <input type="text" class="assign-input q-opt-input" style="padding: 6px 10px; font-size: 12.5px;" data-qidx="${qIdx}" data-optidx="${optIdx}" placeholder="Option ${String.fromCharCode(65 + optIdx)}" value="${escapeHtml(q.options[optIdx] || '')}">
                            </div>
                        `).join('')}
                    </div>
                    <div style="margin-top: 8px;">
                        <input type="text" class="assign-input q-exp-input" style="padding: 6px 10px; font-size: 12px; background: #f8fafc;" data-qidx="${qIdx}" placeholder="Explanation/Hint for student after answering (optional)..." value="${escapeHtml(q.explanation || '')}">
                    </div>
                `;
        container.appendChild(block);
    });

    container.querySelectorAll('.q-prompt-input').forEach(inp => {
        inp.addEventListener('input', (e) => {
            const idx = parseInt(e.target.dataset.qidx, 10);
            if (currentCreateTaskQuestions[idx]) currentCreateTaskQuestions[idx].prompt = e.target.value;
        });
    });
    container.querySelectorAll('.q-opt-input').forEach(inp => {
        inp.addEventListener('input', (e) => {
            const qIdx = parseInt(e.target.dataset.qidx, 10);
            const optIdx = parseInt(e.target.dataset.optidx, 10);
            if (currentCreateTaskQuestions[qIdx]) {
                if (!currentCreateTaskQuestions[qIdx].options) currentCreateTaskQuestions[qIdx].options = [];
                currentCreateTaskQuestions[qIdx].options[optIdx] = e.target.value;
            }
        });
    });
    container.querySelectorAll('.q-exp-input').forEach(inp => {
        inp.addEventListener('input', (e) => {
            const idx = parseInt(e.target.dataset.qidx, 10);
            if (currentCreateTaskQuestions[idx]) currentCreateTaskQuestions[idx].explanation = e.target.value;
        });
    });
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function addNewQuestionBlock() {
    currentCreateTaskQuestions.push({
        prompt: '',
        options: ['', '', '', ''],
        answer: 0,
        explanation: ''
    });
    renderQuestionBlocks();
}

function removeQuestionBlock(idx) {
    if (currentCreateTaskQuestions.length <= 1) return;
    currentCreateTaskQuestions.splice(idx, 1);
    renderQuestionBlocks();
}

function setQuestionCorrectAnswer(qIdx, optIdx) {
    if (currentCreateTaskQuestions[qIdx]) {
        currentCreateTaskQuestions[qIdx].answer = optIdx;
        renderQuestionBlocks();
    }
}

function fillSampleQuestion() {
    const sub = document.getElementById('newTaskSubject').value;
    const cls = document.getElementById('newTaskClass').value;

    let sampleTitle = `Class ${cls} ${sub} Review Challenge`;
    let samplePrompt = "What is the primary source of energy for Planet Earth?";
    let sampleOpts = ["The Sun", "The Moon", "The Wind", "Ocean Tides"];
    let sampleAns = 0;
    let sampleExp = "The Sun radiates light and heat, powering photosynthesis and weather on Earth.";
    let sampleSkill = "Solar Energy & Earth";

    if (sub === 'Mathematics') {
        sampleTitle = `Class ${cls} Multiplication & Mental Math`;
        samplePrompt = "What is 12 multiplied by 8?";
        sampleOpts = ["86", "92", "96", "104"];
        sampleAns = 2;
        sampleExp = "12 × 8 = 96.";
        sampleSkill = "Multiplication & Operations";
    } else if (sub === 'English') {
        sampleTitle = `Class ${cls} Vocabulary & Grammar Sprint`;
        samplePrompt = "Which word is an antonym (opposite) of 'Ancient'?";
        sampleOpts = ["Old", "Historic", "Modern", "Dusty"];
        sampleAns = 2;
        sampleExp = "'Modern' refers to present times, opposite of 'ancient'.";
        sampleSkill = "Vocabulary & Antonyms";
    }

    document.getElementById('newTaskTitle').value = sampleTitle;
    document.getElementById('newTaskSkillArea').value = sampleSkill;
    document.getElementById('newTaskDesc').value = `Solve each challenge carefully to earn 3 stars!`;

    currentCreateTaskQuestions = [
        {
            prompt: samplePrompt,
            options: sampleOpts,
            answer: sampleAns,
            explanation: sampleExp
        }
    ];
    renderQuestionBlocks();
    showToastNotification("🎲 Filled with sample questions!");
}

function submitCreateTask() {
    const title = document.getElementById('newTaskTitle').value.trim();
    if (!title) {
        alert('Please enter a Task Title.');
        document.getElementById('newTaskTitle').focus();
        return;
    }

    const cls = document.getElementById('newTaskClass').value;
    const subject = document.getElementById('newTaskSubject').value;
    const skillArea = document.getElementById('newTaskSkillArea').value.trim() || 'General Curriculum';
    const timeEst = document.getElementById('newTaskTime').value;
    const desc = document.getElementById('newTaskDesc').value.trim() || `Teacher created activity for Class ${cls} ${subject}.`;

    const validQuestions = [];
    for (let i = 0; i < currentCreateTaskQuestions.length; i++) {
        const q = currentCreateTaskQuestions[i];
        const prompt = (q.prompt || '').trim();
        const opts = (q.options || []).map(o => String(o || '').trim()).filter(Boolean);

        if (!prompt && opts.length === 0) continue;

        if (!prompt) {
            alert(`Question ${i + 1} is missing a prompt.`);
            return;
        }
        if (opts.length < 2) {
            alert(`Question ${i + 1} needs at least 2 options.`);
            return;
        }

        const finalOpts = [q.options[0] || 'Option A', q.options[1] || 'Option B', q.options[2] || 'Option C', q.options[3] || 'Option D'];
        const ans = (typeof q.answer === 'number' && q.answer >= 0 && q.answer < finalOpts.length) ? q.answer : 0;
        const exp = (q.explanation || '').trim() || `Correct answer: ${finalOpts[ans]}`;

        validQuestions.push({
            prompt: prompt,
            options: finalOpts,
            answer: ans,
            explanation: exp,
            visual_hint: q.visual_hint || '',
            svg_diagram: q.svg_diagram || ''
        });
    }

    if (validQuestions.length === 0) {
        if (currentCreateTaskInteractiveConfig) {
            validQuestions.push({
                prompt: `Great work completing the ${title} mini-game! What did you explore in this challenge?`,
                options: [skillArea, "Unrelated trivia", "Random guessing", "Extra score"],
                answer: 0,
                explanation: `This mini-game was designed to reinforce key concepts in ${skillArea}!`,
                visual_hint: 'Mini-Game Synthesis Check',
                svg_diagram: ''
            });
        } else {
            alert('Please add at least 1 question to this task or build an interactive mini-game with AI.');
            return;
        }
    }

    let thumb = 'images/game_english.jpg';
    let badgeClass = 'badge-eng';
    if (subject === 'Mathematics') {
        thumb = 'images/game_math.jpg';
        badgeClass = 'badge-math';
    } else if (subject === 'EVS' || subject === 'Science' || subject === 'Social Science') {
        thumb = 'images/game_science.jpg';
        badgeClass = 'badge-evs';
    }

    const chosenGameType = (currentCreateTaskGameType && currentCreateTaskGameType !== 'auto')
        ? currentCreateTaskGameType
        : (document.getElementById('newTaskGameType')?.value || (currentCreateTaskInteractiveConfig ? 'Sort & Group' : 'MCQ Quiz'));
    const finalGameType = chosenGameType === 'auto'
        ? (currentCreateTaskInteractiveConfig?.engine === 'bucket-sorter' ? 'Sort & Group' :
            currentCreateTaskInteractiveConfig?.engine === 'pair-matcher' ? 'Match Pairs' :
                currentCreateTaskInteractiveConfig?.engine === 'word-train' ? 'Sequence Order' :
                    currentCreateTaskInteractiveConfig?.engine === 'word-scramble' ? 'Word Scramble' :
                        currentCreateTaskInteractiveConfig?.engine === 'number-line-hopper' ? 'Math Hop' :
                            currentCreateTaskInteractiveConfig?.engine === 'bubble-pop' ? 'Fast Tapper' : 'Sort & Group')
        : chosenGameType;

    const conditionsVal = document.getElementById('aiGameConditions')?.value?.trim() || '';
    const informationVal = document.getElementById('aiGameInformation')?.value?.trim() || '';

    const taskId = 'CUSTOM-' + Date.now();
    const newTask = {
        id: taskId,
        title: title,
        class: cls,
        subject: subject,
        skillArea: skillArea,
        activity: finalGameType,
        gameType: finalGameType,
        interactiveConfig: currentCreateTaskInteractiveConfig || null,
        conditions: conditionsVal,
        information: informationVal,
        thumb: thumb,
        badgeClass: badgeClass,
        desc: desc,
        time: timeEst,
        stars: '3 stars',
        topic: skillArea,
        isCustom: true,
        createdDate: new Date().toISOString(),
        questions: validQuestions
    };

    let customTasks = loadCustomTasks();
    customTasks.unshift(newTask);
    saveCustomTasks(customTasks);

    GamesCatalog.unshift(newTask);

    const assignNow = document.getElementById('newTaskAssignNow').checked;
    let assignedCount = 0;
    if (assignNow) {
        const checkedBoxes = document.querySelectorAll('input[name="createTaskStudentCheck"]:checked');
        checkedBoxes.forEach(cb => {
            const roll = parseInt(cb.value, 10);
            const name = cb.dataset.name;
            const alreadyAssigned = AppState.assignments.some(a =>
                a.class === cls && a.gameId === taskId && a.student === name
            );
            if (!alreadyAssigned) {
                AppState.assignments.push({
                    class: cls,
                    subject: subject,
                    gameId: taskId,
                    gameTitle: title,
                    student: name,
                    roll: roll,
                    status: 'pending',
                    assignedDate: new Date().toISOString(),
                    score: null
                });
                assignedCount++;
            }
        });
        saveAssignments();
    }

    AppState.selectedClass = cls;

    updateSkillAreaOptions();
    updateKidStats();
    renderGamesGrid();
    renderTeacherHub();
    if (typeof renderSplitViews === 'function') renderSplitViews();

    closeCreateTaskModal();
    const assignMsg = assignedCount > 0 ? ` and assigned to ${assignedCount} students!` : '!';
    showToastNotification(`🎉 Custom task "${title}" created${assignMsg}`);
}

function openDeleteTaskModal() {
    renderDeleteTasksModalList();
    const modal = document.getElementById('teacherDeleteTaskModal');
    if (modal) modal.classList.add('active');
}

function closeDeleteTaskModal() {
    const modal = document.getElementById('teacherDeleteTaskModal');
    if (modal) modal.classList.remove('active');
}

function renderDeleteTasksModalList() {
    const container = document.getElementById('deleteTasksModalList');
    if (!container) return;

    // Get all custom tasks from catalog and storage
    const customTasks = GamesCatalog.filter(g => g.isCustom);

    if (customTasks.length === 0) {
        container.innerHTML = `
                    <div style="text-align: center; padding: 42px 16px; background: #f8fafc; border: 1.5px dashed #cbd5e1; border-radius: 16px;">
                        <div style="font-size: 40px; margin-bottom: 8px;">📋</div>
                        <h4 style="font-family: var(--font-heading); font-size: 17px; color: #1e1b4b; margin-bottom: 6px;">No custom tasks found</h4>
                        <p style="color: var(--text-muted); font-size: 13.5px; margin: 0 0 16px;">You haven't created any custom tasks yet.</p>
                        <button type="button" class="btn-create-task-modal" style="margin: 0 auto;" onclick="closeDeleteTaskModal(); openCreateTaskModal();">
                            <span>✨</span> Create New Activity
                        </button>
                    </div>
                `;
        return;
    }

    container.innerHTML = customTasks.map(t => {
        const qCount = (t.questions || []).length;
        const cls = t.class || 'All';
        const sub = t.subject || 'General';
        const skill = t.skillArea || 'Custom Skill';
        const escapedTitle = (t.title || 'Untitled Task').replace(/'/g, "\\'");

        return `
                    <div style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 14px; padding: 14px 16px; display: flex; align-items: center; justify-content: space-between; gap: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
                        <div style="display: flex; flex-direction: column; gap: 4px; flex: 1; min-width: 0;">
                            <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
                                <span style="font-family: var(--font-heading); font-size: 11px; font-weight: 700; background: #f1f5f9; color: #475569; padding: 2px 8px; border-radius: 6px;">Class ${cls}</span>
                                <span class="tac-badge tac-badge-subject ${t.badgeClass || ''}" style="font-size: 10.5px; padding: 2px 8px;">${sub}</span>
                                <span class="tac-badge tac-badge-skill" style="font-size: 10.5px; padding: 2px 8px;">🎯 ${skill}</span>
                                <span style="font-size: 11px; color: #64748b; font-weight: 600;">• ${qCount} question${qCount === 1 ? '' : 's'}</span>
                            </div>
                            <h4 style="font-family: var(--font-heading); font-size: 15.5px; font-weight: 700; color: #0f172a; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${t.title}">
                                ${t.title}
                            </h4>
                        </div>
                        <button type="button" class="btn-delete-tasks-top" style="padding: 7px 14px; font-size: 12px; flex: none;" onclick="executeDeleteCustomTask('${t.id}', '${escapedTitle}')">
                            <span>🗑️</span> Delete
                        </button>
                    </div>
                `;
    }).join('');
}

function executeDeleteCustomTask(taskId, taskTitle) {
    // Delete from GamesCatalog
    const catIdx = GamesCatalog.findIndex(g => g.id === taskId);
    if (catIdx !== -1) {
        GamesCatalog.splice(catIdx, 1);
    }

    // Delete from localStorage
    let customTasks = loadCustomTasks();
    customTasks = customTasks.filter(t => t.id !== taskId);
    saveCustomTasks(customTasks);

    // Clean up related assignments
    AppState.assignments = AppState.assignments.filter(a => a.gameId !== taskId);
    saveAssignments();

    // Refresh app state
    updateSkillAreaOptions();
    updateKidStats();
    renderGamesGrid();
    renderTeacherHub();
    if (typeof renderSplitViews === 'function') renderSplitViews();

    // Refresh delete modal list
    renderDeleteTasksModalList();

    showToastNotification(`🗑️ Custom task "${taskTitle}" deleted.`);
}

// Backward compatibility alias
function deleteCustomTask(taskId) {
    const task = GamesCatalog.find(g => g.id === taskId);
    const title = task ? task.title : 'this task';
    executeDeleteCustomTask(taskId, title);
}

// Initialize App on DOM ready
window.addEventListener('DOMContentLoaded', () => {
    loadSavedAssignments();
    loadCustomTasksIntoCatalog();
    updateSkillAreaOptions();

    // Sync class dropdowns with AppState default
    const kidSel = document.getElementById('kidClassSelect');
    const teachSel = document.getElementById('teacherClassSelect');
    if (kidSel) kidSel.value = AppState.selectedClass;
    if (teachSel) teachSel.value = AppState.selectedClass;

    renderKidZone();
    renderTeacherHub();
    checkAiStatus();

    // Direct deep-link via URL hash or view parameter
    const viewQuery = new URLSearchParams(window.location.search).get('view');
    if (viewQuery === 'teacher' || viewQuery === 'split') {
        switchMainView(viewQuery);
    }

    // Direct deep-link via URL hash (e.g., #quest=II-ENG-05 or ?quest=II-ENG-05)
    const hashMatch = window.location.hash.match(/quest=([^&]+)/);
    const queryMatch = new URLSearchParams(window.location.search).get('quest');
    const targetQuestId = queryMatch || (hashMatch ? hashMatch[1] : null);
    if (targetQuestId) {
        const targetGame = GamesCatalog.find(g => g.id === targetQuestId);
        if (targetGame) {
            AppState.selectedClass = targetGame.class;
            openStudentSelectionModal(targetGame);
        }
    }

    // Keyboard shortcuts for Question Screen
    window.addEventListener('keydown', (e) => {
        const questModal = document.getElementById('questRunnerModal');
        if (!questModal || !questModal.classList.contains('active')) return;

        // Don't intercept typing when typing into text boxes
        if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) {
            if (e.key === 'Escape') closeQuestRunner();
            return;
        }

        const activeRunner = document.getElementById('questActiveRunner');
        if (!activeRunner || activeRunner.style.display === 'none') return;

        const game = AppState.activeMissionGame;
        if (!game || !game.questions) return;
        const q = game.questions[AppState.missionStep];
        if (!q) return;

        const key = e.key.toUpperCase();
        let choiceIdx = -1;
        if (key === '1' || key === 'A') choiceIdx = 0;
        else if (key === '2' || key === 'B') choiceIdx = 1;
        else if (key === '3' || key === 'C') choiceIdx = 2;
        else if (key === '4' || key === 'D') choiceIdx = 3;

        if (choiceIdx !== -1 && q.options && choiceIdx < q.options.length) {
            e.preventDefault();
            QuestAudio.playClick();
            AppState.missionAnswers[AppState.missionStep] = choiceIdx;
            renderQuestStep();
        } else if (e.key === 'Enter' || e.key === 'ArrowRight') {
            e.preventDefault();
            navigateQuest(1);
        } else if (e.key === 'ArrowLeft') {
            e.preventDefault();
            navigateQuest(-1);
        } else if (e.key === 'Escape') {
            closeQuestRunner();
        }
    });
});
