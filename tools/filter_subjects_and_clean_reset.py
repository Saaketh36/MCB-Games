with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# -------------------------------------------------------------------
# 1. Update Reset Confirmation Modal: Remove "Reset Class IV Only"
# -------------------------------------------------------------------
old_reset_modal = """    <!-- ====================================================
         RESET ASSIGNMENTS CONFIRMATION MODAL
         ==================================================== -->
    <div class="modal-overlay" id="resetConfirmModal" onclick="if(event.target===this) closeResetModal()">
        <div class="who-modal-card" style="max-width: 480px; text-align: center; border: 3px solid #fecaca; box-shadow: 0 25px 60px rgba(239, 68, 68, 0.2);">
            <div style="font-size: 46px; margin-bottom: 8px;">🗑️✨</div>
            <h3 style="font-family: var(--font-heading); font-size: 22px; color: #1e1b4b; margin-bottom: 8px;">Reset Assignments</h3>
            <p style="color: var(--text-muted); font-size: 14px; line-height: 1.5; margin-bottom: 22px;">
                Choose which assignments you would like to reset. This will remove assigned students and reset completion progress to zero.
            </p>
            <div style="display: flex; flex-direction: column; gap: 10px;">
                <button type="button" class="btn-start-challenge" id="btnResetCurrentClass" style="background: linear-gradient(135deg, #f59e0b, #d97706); justify-content: center;" onclick="clearClassAssignments()">
                    <span>🗑️</span> Reset Class <span id="resetModalClassLabel">IV</span> Only
                </button>
                <button type="button" class="btn-start-challenge" style="background: linear-gradient(135deg, #ef4444, #b91c1c); justify-content: center;" onclick="clearAllAssignments()">
                    <span>⚠️</span> Reset ALL Classes (Wipe to 0)
                </button>
                <button type="button" class="btn-clear-filters" style="margin: 6px auto 0; font-size: 13.5px;" onclick="closeResetModal()">
                    Cancel
                </button>
            </div>
        </div>
    </div>"""

new_reset_modal = """    <!-- ====================================================
         RESET ASSIGNMENTS CONFIRMATION MODAL
         ==================================================== -->
    <div class="modal-overlay" id="resetConfirmModal" onclick="if(event.target===this) closeResetModal()">
        <div class="who-modal-card" style="max-width: 460px; text-align: center; border: 3px solid #fecaca; box-shadow: 0 25px 60px rgba(239, 68, 68, 0.2);">
            <div style="font-size: 46px; margin-bottom: 8px;">🗑️✨</div>
            <h3 style="font-family: var(--font-heading); font-size: 22px; color: #1e1b4b; margin-bottom: 8px;">Reset All Assignments?</h3>
            <p style="color: var(--text-muted); font-size: 14px; line-height: 1.5; margin-bottom: 22px;">
                This will remove all assigned students and reset completion progress to zero across all activities.
            </p>
            <div style="display: flex; flex-direction: column; gap: 10px;">
                <button type="button" class="btn-start-challenge" style="background: linear-gradient(135deg, #ef4444, #b91c1c); justify-content: center;" onclick="clearAllAssignments()">
                    <span>🗑️</span> Reset All Assignments to 0
                </button>
                <button type="button" class="btn-clear-filters" style="margin: 6px auto 0; font-size: 13.5px;" onclick="closeResetModal()">
                    Cancel
                </button>
            </div>
        </div>
    </div>"""

if old_reset_modal in html:
    html = html.replace(old_reset_modal, new_reset_modal)
    print("Updated Reset modal: Removed 'Reset Class IV Only'!")
else:
    print("Warning: old_reset_modal not matched exactly!")

# -------------------------------------------------------------------
# 2. Update promptResetAssignments in JS: Clean up modal call
# -------------------------------------------------------------------
old_prompt_reset = """        function promptResetAssignments() {
            const cls = AppState.selectedClass;
            const lbl = document.getElementById('resetModalClassLabel');
            if (lbl) lbl.textContent = cls;
            const modal = document.getElementById('resetConfirmModal');
            if (modal) {
                modal.classList.add('active');
                modal.style.display = 'flex';
            }
        }"""

new_prompt_reset = """        function promptResetAssignments() {
            const modal = document.getElementById('resetConfirmModal');
            if (modal) {
                modal.classList.add('active');
                modal.style.display = 'flex';
            }
        }"""

if old_prompt_reset in html:
    html = html.replace(old_prompt_reset, new_prompt_reset)
    print("Updated promptResetAssignments!")
else:
    print("Warning: old_prompt_reset not matched exactly!")

# -------------------------------------------------------------------
# 3. Add id="kidSubjectChips" in Kid Zone markup
# -------------------------------------------------------------------
old_kid_chips_markup = """                    <div class="subject-filter-chips">
                        <button type="button" class="chip-btn active" onclick="filterBySubject('all', this)">All</button>"""

new_kid_chips_markup = """                    <div class="subject-filter-chips" id="kidSubjectChips">
                        <button type="button" class="chip-btn active" onclick="filterBySubject('all', this)">All</button>"""

if old_kid_chips_markup in html:
    html = html.replace(old_kid_chips_markup, new_kid_chips_markup)
    print("Added id='kidSubjectChips'!")

# -------------------------------------------------------------------
# 4. Implement updateTeacherSubjectChips() and updateKidSubjectChips()
# -------------------------------------------------------------------
old_filter_teacher_func = """        function handleTeacherClassChange(cls) {
            handleClassFilterChange(cls);
        }

        function filterTeacherSubject(sub, btn) {
            AppState.teacherSubjectFilter = sub;
            document.querySelectorAll('#teacherSubjectChips .chip-btn').forEach(b => b.classList.remove('active'));
            if (btn) btn.classList.add('active');
            renderTeacherHub();
        }"""

new_filter_teacher_func = """        function handleTeacherClassChange(cls) {
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
            allBtn.onclick = function() { filterTeacherSubject('all', this); };
            container.appendChild(allBtn);

            // Dynamically add ONLY subjects that have activities in this class
            presentSubjects.forEach(sub => {
                const meta = subjectMeta[sub] || { label: sub, dot: 'chip-dot-math' };
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = `chip-btn ${AppState.teacherSubjectFilter === sub ? 'active' : ''}`;
                btn.innerHTML = `<span class="chip-dot ${meta.dot}"></span> ${meta.label}`;
                btn.onclick = function() { filterTeacherSubject(sub, this); };
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
            allBtn.onclick = function() { filterBySubject('all', this); };
            container.appendChild(allBtn);

            presentSubjects.forEach(sub => {
                const meta = subjectMeta[sub] || { label: sub, dot: 'chip-dot-math' };
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = `chip-btn ${AppState.selectedSubject === sub ? 'active' : ''}`;
                btn.innerHTML = `<span class="chip-dot ${meta.dot}"></span> ${meta.label}`;
                btn.onclick = function() { filterBySubject(sub, this); };
                container.appendChild(btn);
            });
        }

        function filterTeacherSubject(sub, btn) {
            AppState.teacherSubjectFilter = sub;
            renderTeacherHub();
        }"""

if old_filter_teacher_func in html:
    html = html.replace(old_filter_teacher_func, new_filter_teacher_func)
    print("Added updateTeacherSubjectChips and updateKidSubjectChips!")
else:
    print("Warning: old_filter_teacher_func not matched exactly!")

# -------------------------------------------------------------------
# 5. Call updateTeacherSubjectChips() inside renderTeacherHub()
# -------------------------------------------------------------------
old_render_hub_top = """            // Get all activities for this class
            const classGames = GamesCatalog.filter(g => g.class === cls);"""

new_render_hub_top = """            // Update Subject Filter Chips to ONLY show subjects with activities in this class
            updateTeacherSubjectChips();

            // Get all activities for this class
            const classGames = GamesCatalog.filter(g => g.class === cls);"""

if old_render_hub_top in html:
    html = html.replace(old_render_hub_top, new_render_hub_top)
    print("Hooked updateTeacherSubjectChips into renderTeacherHub!")
else:
    print("Warning: old_render_hub_top not matched exactly!")

# -------------------------------------------------------------------
# 6. Call updateKidSubjectChips() inside renderKidZone()
# -------------------------------------------------------------------
old_render_kid_top = """        function renderKidZone() {
            updateKidStats();
            renderGamesGrid();
        }"""

new_render_kid_top = """        function renderKidZone() {
            updateKidSubjectChips();
            updateKidStats();
            renderGamesGrid();
        }"""

if old_render_kid_top in html:
    html = html.replace(old_render_kid_top, new_render_kid_top)
    print("Hooked updateKidSubjectChips into renderKidZone!")
else:
    print("Warning: old_render_kid_top not matched exactly!")

# -------------------------------------------------------------------
# 7. Update resetTeacherFilters to also reset correctly
# -------------------------------------------------------------------
old_reset_teacher_filters = """        function resetTeacherFilters() {
            AppState.teacherSubjectFilter = 'all';
            AppState.teacherSearchQuery = '';
            AppState.teacherStatusFilter = 'all';
            const input = document.getElementById('teacherSearchInput');
            if (input) input.value = '';
            document.querySelectorAll('#teacherSubjectChips .chip-btn').forEach((b, idx) => {
                b.classList.toggle('active', idx === 0);
            });
            const btnAll = document.getElementById('btnTeacherStatusAll');
            const btnAsg = document.getElementById('btnTeacherStatusAssigned');
            if (btnAll) btnAll.classList.add('active');
            if (btnAsg) btnAsg.classList.remove('active');
            renderTeacherHub();
        }"""

new_reset_teacher_filters = """        function resetTeacherFilters() {
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
        }"""

if old_reset_teacher_filters in html:
    html = html.replace(old_reset_teacher_filters, new_reset_teacher_filters)
    print("Updated resetTeacherFilters!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: index.html updated successfully!")
