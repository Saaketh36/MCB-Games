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
            kidSubTab: 'explore', // Default to explore all games
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

        // Persistent Assignment Storage (Clean start: v7 with NO hardcoded demo assignments)
        const STORAGE_KEY = 'mcb_assignments_v7';

        function loadSavedAssignments() {
            try {
                // Clear any legacy test keys so stale test assignments never linger
                ['mcb_assignments', 'mcb_assignments_v1', 'mcb_assignments_v2', 'mcb_assignments_v3', 'mcb_assignments_v4', 'mcb_assignments_v5', 'mcb_assignments_v6', 'assignments'].forEach(k => {
                    try { localStorage.removeItem(k); } catch (e) { }
                });

                const stored = localStorage.getItem(STORAGE_KEY);
                if (stored) {
                    AppState.assignments = JSON.parse(stored);
                } else {
                    AppState.assignments = []; // True empty start: 0 assignments
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
                ['mcb_assignments', 'mcb_assignments_v1', 'mcb_assignments_v2', 'mcb_assignments_v3', 'mcb_assignments_v4', 'mcb_assignments_v5', 'mcb_assignments_v6', 'mcb_assignments_v7', 'assignments'].forEach(k => {
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
            AppState.currentView = view;

            document.getElementById('btnNavKid').classList.toggle('active', view === 'kid');
            document.getElementById('btnNavTeacher').classList.toggle('active', view === 'teacher');
            document.getElementById('btnNavSplit').classList.toggle('active', view === 'split');

            const kidView = document.getElementById('kidZoneView');
            const teacherView = document.getElementById('teacherHubView');
            const splitView = document.getElementById('splitViewContainer');

            kidView.style.display = view === 'kid' ? 'block' : 'none';
            teacherView.classList.toggle('active', view === 'teacher');
            splitView.classList.toggle('active', view === 'split');

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
            if (bEl) bEl.textContent = classAsgs.length;
        }

        function renderGamesGrid() {
            const grid = document.getElementById('gamesCardsGrid');
            if (!grid) return;
            grid.innerHTML = '';

            let list = GamesCatalog.filter(g => {
                // Class filter
                if (g.class && g.class !== AppState.selectedClass) return false;
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

            // Filter if "My assignments" tab selected
            if (AppState.kidSubTab === 'assigned') {
                const assignedGameIds = AppState.assignments
                    .filter(a => a.class === AppState.selectedClass)
                    .map(a => a.gameId);
                list = list.filter(g => assignedGameIds.includes(g.id));
            }

            // Update adventure count badge & clear filters button
            const badge = document.getElementById('filteredGamesCountBadge');
            if (badge) badge.textContent = `Showing ${list.length} adventure${list.length === 1 ? '' : 's'}`;

            const clearBtn = document.getElementById('btnClearFilters');
            if (clearBtn) {
                const hasFilters = AppState.selectedSubject !== 'all' || AppState.selectedSkillArea !== 'all' || AppState.selectedActivity !== 'all' || AppState.searchQuery !== '';
                clearBtn.style.display = hasFilters ? 'inline-flex' : 'none';
            }

            const kidResetBtn = document.getElementById('btnKidResetAssignments');
            if (kidResetBtn) {
                const hasAssigned = AppState.assignments.some(a => a.class === AppState.selectedClass);
                kidResetBtn.style.display = (AppState.kidSubTab === 'assigned' && hasAssigned) ? 'inline-flex' : 'none';
            }

            if (list.length === 0) {
                const isAssignedTab = AppState.kidSubTab === 'assigned';
                grid.innerHTML = `
                    <div style="grid-column: 1 / -1; padding: 48px; text-align: center; background: #ffffff; border-radius: 24px; border: 1px solid #e2e8f0; box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);">
                        <div style="font-size: 44px; margin-bottom: 12px;">${isAssignedTab ? '📋✨' : '🔍✨'}</div>
                        <h4 style="font-family: var(--font-heading); font-size: 22px; font-weight: 700; color: #1e1b4b; margin-bottom: 6px;">
                            ${isAssignedTab ? `No assigned activities for Class ${AppState.selectedClass} yet` : 'No adventures found'}
                        </h4>
                        <p style="font-size: 15px; color: var(--text-muted); margin-bottom: 18px;">
                            ${isAssignedTab ? 'Check back once your teacher assigns an activity, or switch to Explore Games!' : 'Try picking a different skill area, activity, or subject!'}
                        </p>
                        ${isAssignedTab ? `
                            <button type="button" class="btn-clear-filters" onclick="setKidSubTab('explore')" style="margin: 0 auto;">
                                🧭 Explore all games
                            </button>
                        ` : `
                            <button type="button" class="btn-clear-filters" onclick="resetAllFilters()" style="margin: 0 auto;">
                                Reset all filters ↺
                            </button>
                        `}
                    </div>
                `;
                return;
            }

            list.forEach(game => {
                // Check assignments for this game
                const assignedForThis = AppState.assignments.filter(a => a.class === AppState.selectedClass && a.gameId === game.id);
                const isCompleted = assignedForThis.some(a => a.status === 'completed');
                const compCount = assignedForThis.filter(a => a.status === 'completed').length;

                const card = document.createElement('div');
                card.className = 'game-card';
                card.innerHTML = `
                    <div class="game-thumb-wrap" style="height: 135px;">
                        <img src="${game.thumb}" alt="${game.title}" class="game-thumb-img" onerror="this.src='https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400&auto=format&fit=crop&q=80'">
                        <span class="subject-badge-pill ${game.badgeClass}">${game.subject}</span>
                        ${game.isCustom ? '<span class="tac-badge tac-badge-custom" style="position: absolute; top: 10px; right: 10px; z-index: 3; box-shadow: 0 2px 8px rgba(0,0,0,0.12);">⭐ Custom</span>' : ''}
                        ${isCompleted ? '<span class="game-status-pill"><span>✓</span> Completed</span>' : (assignedForThis.length > 0 ? '<span class="game-status-pill" style="background: rgba(254, 243, 199, 0.95); color: #b45309;"><span>⏳</span> Assigned</span>' : '')}
                    </div>
                    <div class="game-info-body" style="padding: 14px 16px;">
                        <div class="game-simple-tags">
                            ${(window.Class2Games && window.Class2Games.isClass2Interactive(game)) ? '<span class="simple-tag mini-game-tag">🎮 Mini-Game</span>' : ''}
                            <span class="simple-tag">${game.skillArea || 'General'}</span>
                        </div>
                        <h3 class="game-title" style="font-size: 16px; margin-bottom: 8px;">${game.title}</h3>

                        ${assignedForThis.length > 0 ? `
                        <div class="game-assigned-summary">
                            <span class="assigned-dot"></span>
                            <span>${assignedForThis.length} assigned</span>
                            ${compCount > 0 ? `<span class="assigned-comp-check">(${compCount} done ✓)</span>` : ''}
                        </div>
                        ` : ''}

                        <button type="button" class="btn-play-action ${isCompleted ? 'played' : ''}" style="margin-top: auto; padding: 9px 14px; font-size: 13px;" onclick="openWhoIsPlaying('${game.id}')">
                            <span>${(window.Class2Games && window.Class2Games.isClass2Interactive(game)) ? '🎮' : '▶'}</span> ${isCompleted ? 'Play again 🚀' : 'Play Activity 🚀'}
                        </button>
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

        function setKidSubTab(tab) {
            AppState.kidSubTab = tab;
            const tabExp = document.getElementById('tabExploreGames');
            const tabAsg = document.getElementById('tabMyAssignments');
            if (tabExp) tabExp.classList.toggle('active', tab === 'explore');
            if (tabAsg) tabAsg.classList.toggle('active', tab === 'assigned');
            const inlineCascade = document.getElementById('kidSkillActivityInline');
            if (inlineCascade) {
                inlineCascade.style.display = tab === 'explore' ? 'inline-flex' : 'none';
            }
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
                            <button type="button" class="btn-assign-modal" style="padding: 9px 18px; font-size: 13px;" onclick="closeWhoModal(); openAssignModalForGame('${game.id}');">
                                <span>+</span> Assign in Teacher Hub
                            </button>
                            <button type="button" class="btn-quest-ctrl" style="padding: 9px 18px; font-size: 13px; background: #ede9fe; color: #6d28d9; border-color: #ddd6fe;" onclick="startQuickPractice('${game.id}')">
                                <span>🎮</span> Quick Practice / Preview
                            </button>
                        </div>
                    </div>
                `;
                document.getElementById('btnStartSelectedChallenge').disabled = true;
                return;
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
                card.className = 'who-student-card';
                card.onclick = () => selectStudentForMission({ name: asg.student, roll: asg.roll }, card);

                card.innerHTML = `
                    <div class="who-avatar-badge" style="background: ${col.bg}; color: ${col.text};">
                        ${initials}
                    </div>
                    <div style="flex: 1;">
                        <div style="font-size: 14.5px; font-weight: 700; color: #0f172a;">${asg.student}</div>
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 3px;">
                            <span style="font-size: 11.5px; color: var(--text-muted);">Roll #${asg.roll}</span>
                            <span style="font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 999px; ${isCompleted ? 'background: #dcfce7; color: #15803d;' : 'background: #fef3c7; color: #b45309;'}">
                                ${isCompleted ? `✓ Done (${asg.score || 3}/3 ⭐)` : 'Ready to play! 🚀'}
                            </span>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            });
        }

        function filterWhoRoster(val) {
            renderWhoRoster(val);
        }

        function selectStudentForMission(student, cardElem) {
            AppState.selectedStudent = student;
            document.querySelectorAll('.who-student-card').forEach(c => c.classList.remove('selected'));
            cardElem.classList.add('selected');
            document.getElementById('btnStartSelectedChallenge').disabled = false;
        }

        function startSelectedMission() {
            if (!AppState.selectedStudent || !AppState.activeMissionGame) return;
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
                    playerEl.textContent = `${AppState.selectedStudent.name} (Roll #${AppState.selectedStudent.roll})`;
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

        function renderQuestStep() {
            const game = AppState.activeMissionGame;
            if (!game) return;

            const c2Container = document.getElementById('c2InteractiveGameContainer');
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

            // Standard MCQ / Visual Diagram Quest Runner
            if (c2Container) c2Container.style.display = 'none';
            standardElements.forEach(el => { if (el) el.style.display = ''; });

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

            document.getElementById('questPromptTitle').textContent = q.prompt;

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
            const keys = ['A', 'B', 'C', 'D'];
            const badgeClasses = ['badge-a', 'badge-b', 'badge-c', 'badge-d'];

            q.options.forEach((optText, idx) => {
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
                        <span class="choice-key-badge ${badgeClasses[idx]}">${keys[idx]}</span>
                        <span style="line-height: 1.4;">${optText}</span>
                    </div>
                    <div class="choice-check-indicator">✓</div>
                `;
                grid.appendChild(btn);
            });

            document.getElementById('btnQuestPrev').style.visibility = AppState.missionStep > 0 ? 'visible' : 'hidden';
            document.getElementById('btnQuestNext').innerHTML = AppState.missionStep === total - 1
                ? 'Submit Challenge <span>🚀</span>'
                : 'Next question <span>→</span>';
        }

        function navigateQuest(delta) {
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
            const q = AppState.activeMissionGame.questions[AppState.missionStep];
            if (!q) return;
            const utter = new SpeechSynthesisUtterance(q.prompt);
            utter.rate = 0.95;
            utter.pitch = 1.05;
            window.speechSynthesis.speak(utter);
        }

        function retakeCurrentQuest() {
            AppState.missionStep = 0;
            AppState.missionAnswers = {};
            document.getElementById('questActiveRunner').style.display = 'block';
            document.getElementById('questCelebrationRunner').style.display = 'none';
            renderQuestStep();
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
                if (AppState.missionAnswers[idx] === q.answer) correct++;
            });

            const wrong = total - correct;
            const pct = Math.round((correct / total) * 100);

            // Save completed state to assignments
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
            renderKidZone();
            renderTeacherHub();
            if (AppState.currentView === 'split') {
                renderSplitViews();
            }

            // Populate Review Header
            const trophyEl = document.getElementById('celebTrophyEmoji');
            const titleEl = document.getElementById('celebMainTitle');
            const subEl = document.getElementById('celebSubTitle');

            if (pct === 100) {
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
                const isAnswered = userChoice !== undefined && userChoice !== null;
                const isCorrect = isAnswered && userChoice === q.answer;
                const userText = isAnswered ? q.options[userChoice] : 'Not answered';
                const correctText = q.options[q.answer];

                const card = document.createElement('div');
                card.className = `review-q-card ${isCorrect ? 'is-correct' : 'is-wrong'}`;

                card.innerHTML = `
                    <div class="review-card-head">
                        <div style="flex: 1;">
                            <span style="font-size: 11px; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">Question ${idx + 1}</span>
                            <div class="review-q-prompt-text">${q.prompt}</div>
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
                            // Skill Area Header Row (Order of Skill Area, stated once, NOT on every game!)
                            const headerTr = document.createElement('tr');
                            headerTr.className = 'curriculum-skill-header-row';
                            headerTr.innerHTML = `
                                <td colspan="3" style="background: #f8fafc; padding: 11px 18px; border-top: 1.5px solid #e2e8f0; border-bottom: 1.5px solid #e2e8f0;">
                                    <div style="display: flex; align-items: center; justify-content: space-between;">
                                        <div style="display: flex; align-items: center; gap: 8px;">
                                            <span style="font-size: 15px;">🎯</span>
                                            <span style="font-family: var(--font-heading); font-size: 14.5px; font-weight: 800; color: #1e1b4b; letter-spacing: -0.2px;">${skillName}</span>
                                        </div>
                                        <span style="background: #ede9fe; color: #5b21b6; font-family: var(--font-heading); font-weight: 700; font-size: 11.5px; padding: 2px 10px; border-radius: 999px; border: 1px solid #ddd6fe;">
                                            ${gamesInSkill.length} ${gamesInSkill.length === 1 ? 'activity' : 'activities'}
                                        </span>
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
                                        <div class="curriculum-title-wrap" style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                                            ${!isSpecificSubject ? `<span class="tac-badge tac-badge-subject ${g.badgeClass || ''}">${g.subject}</span>` : ''}
                                            ${g.isCustom ? '<span class="tac-badge tac-badge-custom">⭐ Custom</span>' : ''}
                                            ${(window.Class2Games && window.Class2Games.isClass2Interactive(g)) ? '<span class="tac-badge" style="background:#fdf2f8; color:#be185d; border:1px solid #fbcfe8; font-size:10.5px; font-weight:800; border-radius:999px; padding:2px 7px;">🎮 Mini-Game</span>' : ''}
                                            <span class="curriculum-title" style="font-family: var(--font-heading); font-size: 15px; font-weight: 700; color: #0f172a;">${g.title}</span>
                                        </div>
                                    </td>
                                    <td>
                                        <div class="curriculum-progress-wrap">
                                            ${isAssigned ? `
                                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                                                <span class="curriculum-pct ${pct === 100 ? 'done' : 'in-prog'}">
                                                    <strong>${compCount}/${totalAssigned}</strong> completed (${pct}%)
                                                </span>
                                            </div>
                                            <div class="tac-progress-bar" style="height: 6px; background: #e2e8f0; border-radius: 999px; overflow: hidden;">
                                                <div class="tac-progress-fill ${pct === 100 ? 'full' : ''}" style="height: 100%; width: ${pct}%; border-radius: 999px; background: ${pct === 100 ? '#10b981' : 'linear-gradient(90deg, #f59e0b, #10b981)'};"></div>
                                            </div>
                                            ` : `
                                            <span style="color: #94a3b8; font-size: 12.5px; font-weight: 500;">Not assigned</span>
                                            `}
                                        </div>
                                    </td>
                                    <td>
                                        <div class="curriculum-students-cell" style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 6px;">
                                            <div style="display: flex; flex-wrap: wrap; gap: 4px; align-items: center;">
                                                ${isAssigned
                                        ? assigned.map(a => `
                                                        <span class="tac-chip ${a.status === 'completed' ? 'completed' : 'pending'}" style="font-size: 11px; padding: 2px 8px;">
                                                            ${a.status === 'completed' ? `✓ ${a.student}` : `⏳ ${a.student}`}
                                                        </span>
                                                    `).join('')
                                        : `<button type="button" class="btn-quick-assign" onclick="openAssignModalForGame('${g.id}')">+ Assign</button>`
                                    }
                                            </div>
                                            ${isAssigned ? `
                                                <button type="button" class="btn-clear-assignments-sm" style="padding: 2px 8px; font-size: 11px; border-radius: 6px;" title="Unassign this activity from Class ${cls}" onclick="unassignActivity('${g.id}')">
                                                    ✕ Clear
                                                </button>
                                            ` : ''}
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
                            // Section Banner for Skill Area in Grid
                            const banner = document.createElement('div');
                            banner.style.cssText = 'grid-column: 1 / -1; margin-top: 14px; margin-bottom: 6px; padding: 10px 16px; background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 12px; display: flex; align-items: center; justify-content: space-between;';
                            banner.innerHTML = `
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <span style="font-size: 16px;">🎯</span>
                                    <span style="font-family: var(--font-heading); font-size: 15px; font-weight: 800; color: #1e1b4b;">${skillName}</span>
                                </div>
                                <span style="background: #ede9fe; color: #5b21b6; font-family: var(--font-heading); font-weight: 700; font-size: 11.5px; padding: 2px 10px; border-radius: 999px; border: 1px solid #ddd6fe;">
                                    ${gamesInSkill.length} ${gamesInSkill.length === 1 ? 'activity' : 'activities'}
                                </span>
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
                                        <div class="tac-students-label" style="font-size: 11px; margin-bottom: 4px;">
                                            <span>Assigned Students (${totalAssigned})</span>
                                            ${isAssigned ? `<span style="font-weight: 700; color: ${pct === 100 ? '#15803d' : '#b45309'};">${pct === 100 ? '✓ Done' : `${compCount}/${totalAssigned} Done`}</span>` : ''}
                                        </div>
                                        <div class="tac-student-chips">
                                            ${isAssigned
                                        ? assigned.map(a => `
                                                    <span class="tac-chip ${a.status === 'completed' ? 'completed' : 'pending'}" style="font-size: 11px; padding: 2px 8px;">
                                                        ${a.status === 'completed' ? `✓ ${a.student}` : `⏳ ${a.student}`}
                                                        ${a.status === 'completed' ? `<span class="tac-chip-stars" style="font-size: 10px;">⭐ ${a.score || 3}/3</span>` : ''}
                                                    </span>
                                                `).join('')
                                        : `<span class="tac-no-students-notice" style="font-size: 11px; padding: 3px 8px;">No students assigned</span>`
                                    }
                                        </div>
                                    </div>

                                    <div class="tac-footer" style="padding-top: 8px;">
                                        <button type="button" class="btn-tac-assign" style="padding: 7px 12px; font-size: 12px;" onclick="openAssignModalForGame('${g.id}')">
                                            <span>+</span> Assign Students
                                        </button>
                                        <button type="button" class="btn-tac-preview" style="padding: 6px 10px; font-size: 11.5px;" onclick="openWhoIsPlaying('${g.id}')">
                                            <span>▶</span> Play
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
        function openAssignModal() {
            document.getElementById('modalAssignClass').value = AppState.selectedClass;
            updateModalSubjectOptions(AppState.teacherSubjectFilter !== 'all' ? AppState.teacherSubjectFilter : 'all');
            renderAssignStudentsList();
            document.getElementById('teacherAssignModal').classList.add('active');
        }

        function openAssignModalForGame(gameId) {
            const game = GamesCatalog.find(g => g.id === gameId);
            if (!game) {
                openAssignModal();
                return;
            }

            document.getElementById('modalAssignClass').value = game.class || AppState.selectedClass;
            renderAssignStudentsList();
            updateModalSubjectOptions(game.subject);

            const saSelect = document.getElementById('modalAssignSkillArea');
            if (saSelect) saSelect.value = game.skillArea;
            updateModalActivityOptions();

            const actSelect = document.getElementById('modalAssignActivity');
            if (actSelect) actSelect.value = game.activity;
            updateAssignGamesList();

            const gameSelect = document.getElementById('modalAssignGame');
            if (gameSelect) gameSelect.value = game.id;

            document.getElementById('teacherAssignModal').classList.add('active');
        }

        function closeAssignModal() {
            document.getElementById('teacherAssignModal').classList.remove('active');
        }

        function handleModalClassChange(cls) {
            renderAssignStudentsList();
            updateModalSubjectOptions();
        }

        function updateModalSubjectOptions(preferredSubject) {
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

            subSelect.innerHTML = '<option value="all">All Subjects</option>';
            presentSubjects.forEach(s => {
                const opt = document.createElement('option');
                opt.value = s;
                opt.textContent = s;
                subSelect.appendChild(opt);
            });

            if (currentVal && (currentVal === 'all' || presentSubjects.includes(currentVal))) {
                subSelect.value = currentVal;
            } else {
                subSelect.value = 'all';
            }

            updateModalSkillAreaOptions();
        }

        function handleModalSubjectChange(sub) {
            updateModalSkillAreaOptions();
        }

        function handleModalSkillAreaChange(sa) {
            updateModalActivityOptions();
        }

        function handleModalActivityChange(act) {
            updateAssignGamesList();
        }

        function updateModalSkillAreaOptions() {
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
            saSelect.innerHTML = '<option value="all">🎯 All Skill Areas</option>';
            uniqueSkills.forEach(s => {
                const opt = document.createElement('option');
                opt.value = s;
                opt.textContent = s;
                saSelect.appendChild(opt);
            });

            updateModalActivityOptions();
        }

        function updateModalActivityOptions() {
            const cls = document.getElementById('modalAssignClass').value;
            const sub = document.getElementById('modalAssignSubject').value;
            const sa = document.getElementById('modalAssignSkillArea').value;
            const actSelect = document.getElementById('modalAssignActivity');
            if (!actSelect) return;

            const games = GamesCatalog.filter(g => {
                if (g.class && g.class !== cls) return false;
                if (sub !== 'all' && g.subject !== sub) return false;
                if (sa !== 'all' && g.skillArea !== sa) return false;
                return true;
            });

            const uniqueActs = Array.from(new Set(games.map(g => g.activity).filter(Boolean))).sort();
            actSelect.innerHTML = '<option value="all">⚡ All Activities</option>';
            uniqueActs.forEach(a => {
                const opt = document.createElement('option');
                opt.value = a;
                opt.textContent = a;
                actSelect.appendChild(opt);
            });

            updateAssignGamesList();
        }

        function updateAssignGamesList() {
            const cls = document.getElementById('modalAssignClass').value;
            const sub = document.getElementById('modalAssignSubject').value;
            const sa = document.getElementById('modalAssignSkillArea').value;
            const act = document.getElementById('modalAssignActivity').value;
            const select = document.getElementById('modalAssignGame');
            if (!select) return;
            select.innerHTML = '';

            const games = GamesCatalog.filter(g => {
                if (g.class && g.class !== cls) return false;
                if (sub !== 'all' && g.subject !== sub) return false;
                if (sa !== 'all' && g.skillArea !== sa) return false;
                if (act !== 'all' && g.activity !== act) return false;
                return true;
            });

            if (games.length === 0) {
                const opt = document.createElement('option');
                opt.value = '';
                opt.textContent = 'No games match criteria';
                select.appendChild(opt);
                return;
            }

            const isSubSelected = sub !== 'all';
            games.forEach(g => {
                const opt = document.createElement('option');
                opt.value = g.id;
                const subPrefix = (!isSubSelected && g.subject) ? `[${g.subject}] ` : '';
                const skillPart = g.skillArea ? ` (🎯 ${g.skillArea})` : '';
                opt.textContent = `${subPrefix}${g.title}${skillPart}`;
                select.appendChild(opt);
            });
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
            const gameId = document.getElementById('modalAssignGame').value;
            const game = GamesCatalog.find(g => g.id === gameId);

            if (!gameId) {
                alert('Please select a game to assign.');
                return;
            }

            const checkedBoxes = Array.from(document.querySelectorAll('input[name="assignStudentCheck"]:checked'));
            if (checkedBoxes.length === 0) {
                alert('Please select at least one student to assign.');
                return;
            }

            checkedBoxes.forEach(box => {
                const roll = parseInt(box.value, 10);
                const name = box.dataset.name;

                // Avoid duplicate pending assignment
                const exists = AppState.assignments.some(a => a.class === cls && a.gameId === gameId && a.student === name);
                if (!exists) {
                    AppState.assignments.push({
                        id: "asg-" + Date.now() + "-" + roll + "-" + Math.random().toString(36).substr(2, 4),
                        class: cls,
                        subject: game ? game.subject : sub,
                        skillArea: game ? game.skillArea : '',
                        activity: game ? game.activity : '',
                        gameId: gameId,
                        gameTitle: game ? game.title : "Activity Quest",
                        student: name,
                        roll: roll,
                        status: 'pending'
                    });
                }
            });

            saveAssignments();
            closeAssignModal();
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
                            <div style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">Track completion & assign activities</div>
                        </div>
                        <button type="button" class="btn-assign-modal" style="padding: 7px 15px; font-size: 12.5px;" onclick="openAssignModal()">+ Assign</button>
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
                            <p style="font-size: 12.5px; color: var(--text-muted); margin-bottom: 12px;">Assign an activity or click 'All Curriculum' above to view all ${classGames.length} activities.</p>
                            <button type="button" class="btn-tac-assign-sm" style="margin: 0 auto;" onclick="openAssignModal()">+ Assign Activity</button>
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
                                        <button type="button" class="btn-tac-assign-sm" style="font-size: 11px; padding: 5px 10px;" onclick="openAssignModalForGame('${g.id}')">+ Assign</button>
                                        <button type="button" class="btn-tac-play-sm" style="font-size: 11px; padding: 4px 8px;" onclick="openWhoIsPlaying('${g.id}')">▶</button>
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

                                <!-- Assigned Students -->
                                <div style="display: flex; flex-wrap: wrap; gap: 4px; align-items: center;">
                                    <span style="font-size: 10.5px; color: #64748b; font-weight: 700;">Students:</span>
                                    ${isAssigned
                        ? assigned.map(a => `
                                            <span class="tac-chip ${a.status === 'completed' ? 'completed' : 'pending'}" style="font-size: 10.5px; padding: 2px 7px;">
                                                ${a.status === 'completed' ? `✓ ${a.student}` : `⏳ ${a.student}`}
                                            </span>
                                        `).join('')
                        : `<span style="font-size: 10.5px; color: #94a3b8; font-style: italic;">None yet</span>`
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
                            <p style="font-size: 12.5px; color: var(--text-muted); margin-bottom: 12px;">Assign an activity on the Teacher side to see it appear here instantly!</p>
                            <button type="button" class="btn-assign-modal" style="padding: 7px 14px; font-size: 12px; margin: 0 auto;" onclick="openAssignModal()">+ Assign First Activity</button>
                        </div>
                    ` : assignedGames.map(game => {
                const assignedSts = classAsgs.filter(a => a.gameId === game.id);
                const isDone = assignedSts.some(a => a.status === 'completed');

                return `
                            <div class="game-card" style="box-shadow: 0 4px 14px rgba(0,0,0,0.05); border-radius: 16px; overflow: hidden;">
                                <div class="game-thumb-wrap" style="height: 110px;">
                                    <img src="${game.thumb}" alt="${game.title}" class="game-thumb-img">
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

        function openCreateTaskModal(focusAi = false) {
            const cls = AppState.selectedClass || 'IV';
            const clsSelect = document.getElementById('newTaskClass');
            if (clsSelect) clsSelect.value = cls;

            // Reset inputs
            document.getElementById('newTaskTitle').value = '';
            document.getElementById('newTaskSkillArea').value = '';
            document.getElementById('newTaskDesc').value = '';
            document.getElementById('newTaskSubject').value = AppState.teacherSubjectFilter !== 'all' ? AppState.teacherSubjectFilter : 'EVS';
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

            // Reset AI status & feedback
            const aiStatus = document.getElementById('aiGenerationStatus');
            if (aiStatus) {
                aiStatus.style.display = 'none';
                aiStatus.className = 'ai-status-strip';
                aiStatus.innerHTML = '';
            }

            document.getElementById('teacherCreateTaskModal').classList.add('active');

            if (focusAi) {
                setTimeout(() => {
                    const promptEl = document.getElementById('aiTaskPrompt');
                    if (promptEl) {
                        promptEl.focus();
                        promptEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
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

        async function triggerAiTaskGeneration(forceRefresh = false) {
            const promptEl = document.getElementById('aiTaskPrompt');
            const prompt = (promptEl ? promptEl.value : '').trim();

            const cls = document.getElementById('newTaskClass')?.value || AppState.selectedClass || 'IV';
            const subject = document.getElementById('newTaskSubject')?.value || 'Science';
            const numQuestions = parseInt(document.getElementById('aiNumQuestions')?.value || '3', 10);
            const difficulty = document.getElementById('aiDifficulty')?.value || 'Medium';

            if (!prompt) {
                showAiStatus('Please enter a topic or details in the prompt box above.', 'warning');
                if (promptEl) promptEl.focus();
                return;
            }

            const btn = document.getElementById('btnGenerateAiTask');
            const btnFresh = document.getElementById('btnGenerateAiFresh');
            const btnIcon = document.getElementById('aiBtnIcon');
            const btnText = document.getElementById('aiBtnText');
            const origText = btnText ? btnText.textContent : 'Generate with AI';

            // Loading state
            if (btn) btn.disabled = true;
            if (btnFresh) btnFresh.disabled = true;
            if (btnIcon) btnIcon.innerHTML = '<span class="ai-spinner"></span>';
            if (btnText) btnText.textContent = forceRefresh ? 'Generating Fresh...' : 'Designing Game...';
            showAiStatus(forceRefresh
                ? `Generating ${numQuestions} fresh ${difficulty.toLowerCase()} questions via Gemini AI...`
                : `AI is checking question bank & designing ${numQuestions} ${difficulty.toLowerCase()} questions for Class ${cls} ${subject}...`, 'loading');

            try {
                const response = await fetch('/api/ai/generate-task', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        prompt: prompt,
                        class: cls,
                        subject: subject,
                        num_questions: numQuestions,
                        difficulty: difficulty,
                        force_refresh: forceRefresh
                    })
                });

                const result = await response.json();

                if (!response.ok || (result.status !== 'success' && !result.success)) {
                    throw new Error(result.message || result.error || 'Failed to generate task. Please try again.');
                }

                const task = result.task || (result.data ? result.data.task : null) || {};
                const questions = task.questions || (result.data ? result.data.questions : null) || [];

                // 1. Populate Task Info
                if (task.title) {
                    const titleEl = document.getElementById('newTaskTitle');
                    if (titleEl) titleEl.value = task.title;
                }

                const detectedSubject = task.subject || subject;
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
                            if (timeSelect.options[i].value.toLowerCase().includes(timeVal.toLowerCase())) {
                                timeSelect.selectedIndex = i;
                                break;
                            }
                        }
                    }
                }

                // 2. Populate Questions with Multi-Modal Assets
                if (Array.isArray(questions) && questions.length > 0) {
                    currentCreateTaskQuestions = questions.map(q => ({
                        prompt: q.prompt || '',
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

                const isCached = result.cached || (result.provider && result.provider.includes('Question Bank Cache'));
                const providerName = result.provider || (result.data && result.data.source === 'gemini' ? 'Google Gemini AI' : 'Smart Curriculum AI');
                const statusMsg = isCached
                    ? `⚡ Served instantly from Question Bank Cache (0s)! "${task.title || 'Task'}" ready with ${questions.length} questions (${difficulty}).`
                    : `✨ Generated "${task.title || 'Task'}" with ${questions.length} questions (${difficulty}) via ${providerName}! Review and publish below.`;
                showAiStatus(statusMsg, 'success');
                showToastNotification(`✨ AI generated ${questions.length} questions successfully!`);

                // Smooth scroll to task details so teacher sees what was generated
                setTimeout(() => {
                    const titleInput = document.getElementById('newTaskTitle');
                    if (titleInput) {
                        titleInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        titleInput.focus();
                    }
                }, 250);

            } catch (err) {
                console.error('AI Generation Error:', err);
                showAiStatus(`⚠️ ${err.message || 'Generation failed. Please try again.'}`, 'error');
            } finally {
                if (btn) btn.disabled = false;
                if (btnFresh) btnFresh.disabled = false;
                if (btnIcon) btnIcon.textContent = '✨';
                if (btnText) btnText.textContent = origText;
            }
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

        function closeCreateTaskModal() {
            document.getElementById('teacherCreateTaskModal').classList.remove('active');
        }

        function handleCreateTaskClassChange(cls) {
            renderCreateTaskStudentsList();
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
                alert('Please add at least 1 question to this task.');
                return;
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

            const taskId = 'CUSTOM-' + Date.now();
            const newTask = {
                id: taskId,
                title: title,
                class: cls,
                subject: subject,
                skillArea: skillArea,
                activity: 'Teacher Task',
                gameType: 'MCQ Quiz',
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
            renderKidZone();
            renderTeacherHub();
            checkAiStatus();

            // Keyboard shortcuts for Question Screen
            window.addEventListener('keydown', (e) => {
                const questModal = document.getElementById('questRunnerModal');
                if (!questModal || !questModal.classList.contains('active')) return;

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

                if (choiceIdx !== -1 && choiceIdx < q.options.length) {
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
